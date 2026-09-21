# Diagnostico CSRF - API_MAINTNOTIFICATION en CROWN S4H
# Ejecutar en PowerShell desde la maquina Windows (NO desde el shell del sandbox).
#
# Que hace:
#   1. Pide token CSRF y captura la cookie de sesion.
#   2. Reinyecta la cookie a mano, con Secure = $false, para que .NET la envie
#      por HTTP (SAP la marca "secure" y los clientes que cumplen el estandar
#      se niegan a reenviarla sobre http://).
#   3. Lanza el POST y muestra status + cuerpo completo del error.
#
# La contrasena se pide por prompt: no queda en el script ni en el historial.

$ErrorActionPreference = "Stop"

$base   = "http://crown.sapvista.com:50000"
$svc    = "/sap/opu/odata/sap/API_MAINTNOTIFICATION"
$client = "100"
$host_  = "crown.sapvista.com"

$cred = Get-Credential -UserName "SV5_000202" -Message "Password SAP CROWN (mandante $client)"
$pair = "$($cred.UserName):$($cred.GetNetworkCredential().Password)"
$auth = "Basic " + [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes($pair))

Write-Host "`n=========== 1) GET token CSRF ===========" -ForegroundColor Cyan

$r1 = Invoke-WebRequest -Uri "$base$svc/?sap-client=$client" -Method GET -UseBasicParsing `
      -Headers @{ Authorization = $auth; "X-CSRF-Token" = "Fetch"; Accept = "application/json" }

$token = $r1.Headers["x-csrf-token"]
$rawCookies = $r1.Headers["Set-Cookie"]

Write-Host "Status      : $($r1.StatusCode)"
Write-Host "Token CSRF  : $token"
Write-Host "Set-Cookie  : $rawCookies"

if (-not $token -or $token -eq "Required") {
    Write-Host "`n>>> El servidor no devolvio token. Se detiene aqui." -ForegroundColor Red
    exit 1
}

# --- Reconstruir las cookies a mano, desactivando el flag Secure ---
$session = New-Object Microsoft.PowerShell.Commands.WebRequestSession
$added = 0
foreach ($m in [regex]::Matches($rawCookies, '(?<n>[A-Za-z0-9_\-\.]+)=(?<v>[^;,]+)')) {
    $n = $m.Groups['n'].Value
    $v = $m.Groups['v'].Value
    if ($n -match '^(path|domain|expires|max-age|samesite|secure|httponly|version)$') { continue }
    $c = New-Object System.Net.Cookie($n, $v, "/", $host_)
    $c.Secure   = $false   # <-- la clave de todo el asunto
    $c.HttpOnly = $false
    $session.Cookies.Add($c)
    Write-Host "Cookie forzada: $n"
    $added++
}
Write-Host "Cookies inyectadas: $added"

Write-Host "`n=========== 2) POST crear aviso ===========" -ForegroundColor Cyan

$body = '{"NotificationType":"M2","NotificationText":"Prueba POST OData - laboratorio CROWN"}'

try {
    $r2 = Invoke-WebRequest -Uri "$base$svc/MaintenanceNotification?sap-client=$client" `
          -Method POST -UseBasicParsing -WebSession $session -Body $body `
          -Headers @{ Authorization  = $auth
                      "X-CSRF-Token" = $token
                      "Content-Type" = "application/json"
                      Accept         = "application/json" }

    Write-Host "Status: $($r2.StatusCode)" -ForegroundColor Green
    Write-Host "`n--- Respuesta ---"
    Write-Host $r2.Content
}
catch {
    $resp = $_.Exception.Response
    if ($resp) {
        Write-Host "Status: $($resp.StatusCode.value__) $($resp.StatusDescription)" -ForegroundColor Red
        Write-Host "`n--- Cabeceras de respuesta ---"
        foreach ($h in $resp.Headers.AllKeys) { Write-Host ("{0}: {1}" -f $h, $resp.Headers[$h]) }
        Write-Host "`n--- Cuerpo ---"
        $sr = New-Object IO.StreamReader($resp.GetResponseStream())
        Write-Host $sr.ReadToEnd()
    } else {
        Write-Host "Fallo sin respuesta HTTP: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host "`n=========== 3) Control: dos tokens seguidos ===========" -ForegroundColor Cyan
Write-Host "Si los dos tokens salen DISTINTOS, cada peticion abre sesion nueva."

foreach ($i in 1..2) {
    $rx = Invoke-WebRequest -Uri "$base$svc/?sap-client=$client" -Method GET -UseBasicParsing `
          -WebSession $session `
          -Headers @{ Authorization = $auth; "X-CSRF-Token" = "Fetch"; Accept = "application/json" }
    Write-Host ("  intento {0} -> token {1}" -f $i, $rx.Headers["x-csrf-token"])
}
