# Biblioteca de referencia

> Generado con `python scripts/workspace/books.py render`. No editar a mano: cambiar `config/books.json`.

Los libros viven fuera del repositorio, en la raíz de libros (`../books` o `SAP_LAB_BOOKS_ROOT`).
Se citan por `slug`, capítulo y página del PDF; nunca se copia su texto al KB ni a entregables.

| Slug | Libro | Dominios | Material adicional |
|---|---|---|---|
| `cookbook-2026` | ABAP Cookbook - Practical Recipes for Modern Programming (2026) | OO, API, ENH, MIX | Repositorio abapGit de la aplicación de ejemplo (abap-kochbuch-english), ABAP Cloud. |
| `rap-2025` | ABAP RESTful Application Programming Model (2025) | RAP, CDS, UI | Código de los escenarios managed, unmanaged save y unmanaged (capítulos 10-12). |
| `cds-2024` | Core Data Services for ABAP (2024) | CDS, RAP, SQL | Fuentes DDLS/DCLS/BDEF por capítulo. |
| `hana-2021` | ABAP Development for SAP HANA (2021) | SQL, CDS |  |
| `attf-2022` | ABAP to the Future (2022) | OO, SQL, RAP, UI, MIX | Archivos SAPlink y quiz; código clásico, revisar antes de reutilizar en ABAP Cloud. |
| `complete-2022` | Complete ABAP (2022) | OO, SQL, ENH, MIX |  |
| `gateway-2024` | SAP Gateway and OData (2024) | API, RAP, UI |  |
| `ui5-2025` | SAPUI5 - The Comprehensive Guide (2025) | UI | Apps de ejemplo (FCL, split app, navegación). |
| `btp-appdev-2023` | Application Development with SAP Business Technology Platform (2023) | MIX |  |
| `clean-abap-2020` | Clean ABAP - A Style Guide for Developers (Haeuptle et al., 2020) | OO |  |
| `adt-eclipse` | ABAP Eclipse Guide (ADT) | MIX |  |
| `rap-2302` | SAP ABAP RESTful Application Programming (2302) | RAP |  |
| `rap-joule` | SAP ABAP RAP + Joule: Full-Stack Development | RAP, UI |  |
| `fiori-joule` | SAP Fiori Implementation and Development with Joule | UI |  |
| `fiori-completo` | SAP Fiori Completo | UI |  |
| `workflow` | ABAP Development for SAP Business Workflow | MIX |  |
| `function-modules` | Function Modules in ABAP | OO |  |
| `s4-conversion` | SAP S/4HANA Conversion | MIX |  |
| `pm-config-2025` | Configuring Plant Maintenance in SAP S/4HANA (2025) | MIX |  |
| `pm-user-2021` | Plant Maintenance with SAP S/4HANA - Business User Guide (2021) | MIX |  |
| `am-2023` | SAP S/4HANA Asset Management: Configure, Equip and Manage (2023) | MIX |  |

## Capítulos por ruta de skill

### `rap` — RAP / business object

- `cookbook-2026` cap.2 The Application Scenario (p.41)
- `rap-2025` cap.1 Introduction to the ABAP RESTful Application Programming Model (p.25)
- `rap-2025` cap.3 Behavior Definition (p.119)
- `rap-2025` cap.4 Entity Manipulation Language: Accessing Business Logic (p.215)
- `rap-2025` cap.5 Behavior Implementation (p.239)
- `rap-2025` cap.6 Business Services (p.281)
- `rap-2025` cap.10 Managed Scenario: Developing an Application with SAP Fiori Elements (p.391)
- `rap-2025` cap.11 Managed Scenario with Unmanaged Save: Integrating an Existing Application (p.445)
- `rap-2025` cap.12 Unmanaged Scenario: Reusing Existing Source Code (p.505)
- `rap-2025` cap.13 Special Features in the Cloud Environment (p.541)
- `cds-2024` cap.11 Modeling Transactional Applications (p.361)
- `attf-2022` cap.8 Business Logic Using the ABAP RESTful Application Programming Model (p.453)
- `gateway-2024` cap.9 ABAP RESTful Application Programming Model (p.441)
- `rap-2302` libro completo
- `rap-joule` libro completo
- `rap-2025` cap.2 Core Data Services: Data Modeling (p.65)
- `rap-2025` cap.7 Extensibility of Business Objects (p.301)
- `rap-2025` cap.8 Application Interfaces and SAP Fiori Elements (p.347)

### `cds` — CDS view entities

- `rap-2025` cap.2 Core Data Services: Data Modeling (p.65)
- `cds-2024` cap.1 Modeling Your First CDS Views (p.23)
- `cds-2024` cap.2 Fundamentals of CDS Data Modeling (p.53)
- `cds-2024` cap.3 Associations (p.107)
- `cds-2024` cap.4 Annotations (p.131)
- `cds-2024` cap.8 Modeling Application Data (p.249)
- `cds-2024` cap.9 The Virtual Data Model of SAP S/4HANA (p.275)
- `cds-2024` cap.10 Modeling Analytical Applications (p.303)
- `cds-2024` cap.12 Hierarchies in CDS (p.515)
- `cds-2024` cap.13 CDS-Based Search Functionality (p.549)
- `cds-2024` cap.14 Lifecycle and Stability (p.585)
- `cds-2024` cap.17 Troubleshooting (p.671)
- `hana-2021` cap.8 Core Data Services
- `cds-2024` cap.5 Access Controls (p.161)
- `cds-2024` cap.6 Business Services (p.211)
- `cds-2024` cap.7 Native SAP HANA Functions in CDS (p.235)
- `cds-2024` cap.11 Modeling Transactional Applications (p.361)
- `cds-2024` cap.15 Extensions of CDS Views and Other Entities (p.599)
- `cds-2024` cap.16 Automated Testing (p.631)

### `odata` — OData / servicios / APIs

- `cookbook-2026` cap.17 Using APIs (p.367)
- `cds-2024` cap.6 Business Services (p.211)
- `attf-2022` cap.9 Service Layer (p.521)
- `gateway-2024` cap.2 Introduction to OData (p.59)
- `gateway-2024` cap.5 Introduction to OData Service Creation (p.179)
- `gateway-2024` cap.6 Service Development (p.223)
- `gateway-2024` cap.7 Service Generation (p.337)
- `gateway-2024` cap.8 ABAP Programming Model for SAP Fiori (p.395)
- `gateway-2024` cap.16 Lifecycle Management: Testing, Service Deployment, and Operations (p.701)
- `rap-2025` cap.6 Business Services (p.281)
- `complete-2022` cap.19 Interfaces (p.699)
- `gateway-2024` cap.9 ABAP RESTful Application Programming Model (p.441)
- `gateway-2024` cap.12 Extensibility (p.551)
- `gateway-2024` cap.17 Security (p.731)
- `ui5-2025` cap.9 OData Service Integration (p.369)
- `ui5-2025` cap.11 OData Version 4 Model (p.409)

### `sql` — ABAP SQL / AMDP / HANA

- `cds-2024` cap.7 Native SAP HANA Functions in CDS (p.235)
- `hana-2021` cap.4 Native SQL
- `hana-2021` cap.5 SQLScript Programming
- `hana-2021` cap.6 ABAP-Managed Database Procedures
- `hana-2021` cap.9 Open SQL and ABAP SQL
- `hana-2021` cap.11 Performance and Optimization (p.99)
- `attf-2022` cap.6 Database Programming with SAP HANA (p.291)
- `complete-2022` cap.11 Persistent Data (p.405)

### `enh` — Extensiones / BAdI

- `cookbook-2026` cap.18 Extensions in ABAP Cloud (p.387)
- `rap-2025` cap.7 Extensibility of Business Objects (p.301)
- `cds-2024` cap.15 Extensions of CDS Views and Other Entities (p.599)
- `complete-2022` cap.20 Modifications and Enhancements (p.801)
- `gateway-2024` cap.12 Extensibility (p.551)

### `auth` — Autorizaciones / IAM

- `cookbook-2026` cap.16 Authorizations (p.351)
- `cds-2024` cap.5 Access Controls (p.161)
- `gateway-2024` cap.17 Security (p.731)
- `btp-appdev-2023` cap.13 Security (p.393)

### `cloud` — ABAP Cloud / clean core

- `cookbook-2026` cap.1 Introduction to Modern ABAP Development (p.21)
- `cookbook-2026` cap.3 Handling System Fields and Runtime Information (p.79)
- `btp-appdev-2023` cap.9 Developing ABAP Applications (p.239)
- `cookbook-2026` cap.2 The Application Scenario (p.41)
- `cookbook-2026` cap.17 Using APIs (p.367)
- `cookbook-2026` cap.18 Extensions in ABAP Cloud (p.387)
- `rap-2025` cap.13 Special Features in the Cloud Environment (p.541)
- `cds-2024` cap.9 The Virtual Data Model of SAP S/4HANA (p.275)
- `cds-2024` cap.14 Lifecycle and Stability (p.585)

### `migration` — Migración de código clásico

- `s4-conversion` libro completo
- `rap-2025` cap.11 Managed Scenario with Unmanaged Save: Integrating an Existing Application (p.445)
- `rap-2025` cap.12 Unmanaged Scenario: Reusing Existing Source Code (p.505)
- `gateway-2024` cap.6 Service Development (p.223)
- `gateway-2024` cap.8 ABAP Programming Model for SAP Fiori (p.395)

### `quality` — Calidad / Clean ABAP

- `cookbook-2026` cap.15 Documenting Development Objects (p.335)
- `attf-2022` cap.3 New Language Features in ABAP (p.145)
- `clean-abap-2020` libro completo
- `attf-2022` cap.4 Exception Classes and Design by Contract (p.199)

### `unit` — ABAP Unit

- `cds-2024` cap.16 Automated Testing (p.631)
- `attf-2022` cap.5 ABAP Unit and Test-Driven Development (p.233)
- `complete-2022` cap.21 Test and Analysis Tools (p.847)
- `clean-abap-2020` libro completo

### `atc` — ATC

- `complete-2022` cap.21 Test and Analysis Tools (p.847)

### `classic` — ABAP clásico

- `attf-2022` cap.10 ALV SALV Reporting Framework (p.567)
- `complete-2022` cap.5 Structures and Internal Tables (p.135)
- `complete-2022` cap.7 Modularization Techniques (p.213)
- `complete-2022` cap.12 Dialog Programming (p.439)
- `complete-2022` cap.14 Selection Screens (p.519)
- `complete-2022` cap.15 SAP List Viewer Reports (p.541)
- `complete-2022` cap.18 Forms (p.631)
- `complete-2022` cap.19 Interfaces (p.699)
- `function-modules` libro completo

### `utilities` — Utilidades de aplicación (cookbook)

- `cookbook-2026` cap.4 Table Analysis (p.99)
- `cookbook-2026` cap.5 Table Maintenance Using Business Configuration Maintenance Objects (p.111)
- `cookbook-2026` cap.6 Application Logs (p.151)
- `cookbook-2026` cap.7 Change Documents (p.177)
- `cookbook-2026` cap.8 Lock Objects (p.199)
- `cookbook-2026` cap.9 Number Range Objects (p.217)
- `cookbook-2026` cap.10 Background Processing (p.237)
- `cookbook-2026` cap.11 Email Dispatch (p.261)
- `cookbook-2026` cap.12 Parallelizing Application Logic (p.279)
- `cookbook-2026` cap.13 File Upload (p.299)
- `cookbook-2026` cap.14 Using Excel Files (p.309)
- `attf-2022` cap.11 ABAP2XLSX and Beyond (p.631)
- `complete-2022` cap.11 Persistent Data (p.405)

### `ddic` — DDIC

- `complete-2022` cap.10 ABAP Data Dictionary (p.341)

### `oo` — ABAP Objects

- `attf-2022` cap.4 Exception Classes and Design by Contract (p.199)
- `complete-2022` cap.8 Object-Oriented ABAP (p.267)
- `complete-2022` cap.9 Exception Handling (p.319)
- `complete-2022` cap.16 Dynamic Programming (p.579)
- `attf-2022` cap.3 New Language Features in ABAP (p.145)
- `complete-2022` cap.5 Structures and Internal Tables (p.135)
- `clean-abap-2020` libro completo

### `ui` — Fiori / UI5

- `rap-2025` cap.8 Application Interfaces and SAP Fiori Elements (p.347)
- `attf-2022` cap.13 SAPUI5 (p.755)
- `gateway-2024` cap.10 SAPUI5 Application Development (p.507)
- `ui5-2025` cap.9 OData Service Integration (p.369)
- `ui5-2025` cap.11 OData Version 4 Model (p.409)
- `ui5-2025` cap.14 SAP Fiori Elements (p.533)
- `ui5-2025` cap.16 Deployment (p.639)
- `ui5-2025` cap.17 SAP Fiori Launchpad Configuration (p.667)
- `ui5-2025` cap.18 Debugging and Code Quality (p.699)
- `btp-appdev-2023` cap.11 Developing SAP Fiori Applications (p.319)
- `fiori-joule` libro completo
- `fiori-completo` libro completo
- `rap-2025` cap.10 Managed Scenario: Developing an Application with SAP Fiori Elements (p.391)
- `cds-2024` cap.4 Annotations (p.131)
- `cds-2024` cap.13 CDS-Based Search Functionality (p.549)
- `rap-joule` libro completo

### `transport` — Transportes / gCTS

- `attf-2022` cap.2 abapGit (p.99)
- `btp-appdev-2023` cap.12 DevOps Implementation (p.355)
- `gateway-2024` cap.16 Lifecycle Management: Testing, Service Deployment, and Operations (p.701)
- `ui5-2025` cap.16 Deployment (p.639)

### `tooling` — ADT / herramientas

- `attf-2022` cap.1 Integrated Development Environment (p.31)
- `complete-2022` cap.17 Debugging (p.611)
- `adt-eclipse` libro completo

### `pm` — Dominio Plant Maintenance

- `pm-config-2025` libro completo
- `pm-user-2021` libro completo
- `am-2023` libro completo
- `cds-2024` cap.9 The Virtual Data Model of SAP S/4HANA (p.275)

### `workflow` — Business Workflow

- `workflow` libro completo

## Fuera del alcance de este laboratorio

- Cloud Integration with SAP Integration Suite (2024), SAP Cloud Integration Cookbook (2026), Practical SAP Integration Suite, SAP CPI DS Doc, preguntas C_CPI, Integration Flow Design Guidelines 2026: usar en labs de CPI / Integration Suite.
- Nuevos recursos (AIG10, BTP100, CLD900, AI Core, Generative AI hub, vídeos .mp4): usar en labs de BTP / SAP Business AI.
- SAP Cloud Platform / BTP Integration (Otro Libros), Material Requirements Planning (2020), Sourcing and Procurement (2024): contexto funcional no ABAP.
- zabapgit_standalone.prog.abap.txt: no instalar; abapGit ICF está inactivo en este sistema (CTS-001).

## Uso

```bash
python scripts/workspace/books.py index                       # una vez; genera artifacts/books-index/
python scripts/workspace/books.py search "draft" "etag" --route rap
python scripts/workspace/books.py chapters --route cds
```
