---
name: abap-rap
description: >
  Use when building business objects with the ABAP RESTful Application Programming Model
  (RAP): CDS view entity, behavior definition BDEF, behavior implementation ABAP class,
  managed RAP, unmanaged RAP, validation, determination, action, draft-enabled, service
  definition, service binding, OData V4, projection view, business object BO, S/4HANA
  BTP ABAP environment cloud development.
metadata:
  category: abap
  version: "1.0.0"
  keywords: [ABAP, RAP, BDEF, CDS view entity, managed, unmanaged, draft, validation, determination, action, behavior definition, behavior implementation, service binding, OData V4, S/4HANA, BTP ABAP]
  related:
    fiori-elements-floorplans: expose RAP business objects via Fiori Elements UI
    fiori-annotations: add UI annotations to RAP CDS projection views
    btp-deployment: deploy RAP applications to BTP ABAP environment
---

# ABAP RAP — Best Practices

> **Primary reference**: https://help.sap.com/docs/abap-cloud/abap-rap
> **BDEF syntax**: https://help.sap.com/doc/abapdocu_cp_index_htm/CLOUD/en-US/abenbdl_define_beh.htm
> **Cheat sheets**: https://github.com/SAP-samples/abap-cheat-sheets

## RAP architecture — three layers

RAP business objects are defined through CDS data modeling views, CDS behavior definitions, and behavior implementations in ABAP classes.

```
Database table          (DDIC table — stores active data)
    ↓
CDS view entity         (data model — root + child entities)
    ↓
Behavior Definition     (BDEF — what operations are allowed)
    ↓
Behavior Implementation (ABAP class — business logic)
    ↓
Projection view         (UI-specific subset + aliases)
    ↓
Service Definition      (what to expose)
    ↓
Service Binding         (OData V2 or V4 protocol)
```

---

## Managed vs Unmanaged — choose carefully

In Managed RAP, the framework automatically handles all CRUD persistence — the developer focuses only on business logic. In Unmanaged RAP, the developer must implement each save operation manually. Managed RAP is ideal for new development; Unmanaged is chosen when integrating complex existing logic or legacy systems.

**Use Managed when:** greenfield development, direct table access, new S/4HANA or BTP apps
**Use Unmanaged when:** integrating existing BAPI/function modules, complex legacy logic, external persistence

---

## CDS view entity — root and child

```abap
" Root CDS view entity
@AccessControl.authorizationCheck: #CHECK
@EndUserText.label: 'Travel'
define root view entity ZI_Travel
  as select from ztravel
  composition [0..*] of ZI_TravelItem as _Items
{
  key travel_uuid        as TravelUUID,
      travel_id          as TravelID,
      agency_id          as AgencyID,
      customer_id        as CustomerID,
      begin_date         as BeginDate,
      end_date           as EndDate,
      booking_fee        as BookingFee,
      total_price        as TotalPrice,
      currency_code      as CurrencyCode,
      overall_status     as OverallStatus,
      @Semantics.systemDateTime.createdAt: true
      created_at         as CreatedAt,
      @Semantics.user.createdBy: true
      created_by         as CreatedBy,
      @Semantics.systemDateTime.lastChangedAt: true
      last_changed_at    as LastChangedAt,
      @Semantics.user.lastChangedBy: true
      last_changed_by    as LastChangedBy,
      @Semantics.systemDateTime.localInstanceLastChangedAt: true
      local_last_changed_at as LocalLastChangedAt,
      _Items
}
```

---

## Behavior Definition — Managed with Draft

```abap
managed implementation in class ZBP_Travel unique;
strict ( 2 );
with draft;

define behavior for ZI_Travel alias Travel
  persistent table ztravel
  draft table ztravel_d
  etag master LocalLastChangedAt
  lock master total etag LastChangedAt
  authorization master ( global )
{
  field ( readonly ) TravelUUID, TravelID, CreatedAt, CreatedBy, LastChangedAt, LastChangedBy;
  field ( numbering : managed, readonly ) TravelUUID;

  create;
  update;
  delete;

  action ( features : instance ) acceptTravel result [1] $self;
  action ( features : instance ) rejectTravel result [1] $self;

  validation validateDates on save { field BeginDate, EndDate; }
  validation validateStatus on save { field OverallStatus; }

  determination calculateTotalPrice on modify { field BookingFee; }

  draft action Edit;
  draft action Activate optimized;
  draft action Discard;
  draft action Resume;

  association _Items { create; with draft; }

  mapping for ztravel {
    TravelUUID = travel_uuid;
    TravelID   = travel_id;
    AgencyID   = agency_id;
  }
}
```

---

## Behavior Implementation — key methods

```abap
CLASS ZBP_Travel DEFINITION PUBLIC ABSTRACT FINAL FOR BEHAVIOR OF ZI_Travel.
  PUBLIC SECTION.
    " Validation
    METHODS validateDates    FOR VALIDATE ON SAVE
      IMPORTING keys FOR Travel~validateDates.
    " Determination
    METHODS calculateTotalPrice FOR DETERMINE ON MODIFY
      IMPORTING keys FOR Travel~calculateTotalPrice.
    " Action
    METHODS acceptTravel     FOR MODIFY
      IMPORTING keys FOR ACTION Travel~acceptTravel RESULT result.
ENDCLASS.

CLASS ZBP_Travel IMPLEMENTATION.
  METHOD validateDates.
    READ ENTITIES OF ZI_Travel IN LOCAL MODE
      ENTITY Travel
        FIELDS ( BeginDate EndDate )
        WITH CORRESPONDING #( keys )
      RESULT DATA(lt_travel)
      FAILED failed.

    LOOP AT lt_travel INTO DATA(ls_travel).
      IF ls_travel-EndDate < ls_travel-BeginDate.
        APPEND VALUE #(
          %tky = ls_travel-%tky )
          TO failed-travel.
        APPEND VALUE #(
          %tky        = ls_travel-%tky
          %state_area = 'VALIDATE_DATES'
          %msg        = new_message_with_text(
                          severity = if_abap_behv_message=>severity-error
                          text     = 'End date must be after begin date' )
          %element-EndDate = if_abap_behv=>mk-on )
          TO reported-travel.
      ENDIF.
    ENDLOOP.
  ENDMETHOD.

  METHOD calculateTotalPrice.
    " Always use IN LOCAL MODE inside behavior handlers
    MODIFY ENTITIES OF ZI_Travel IN LOCAL MODE
      ENTITY Travel
        UPDATE FIELDS ( TotalPrice )
        WITH VALUE #( FOR key IN keys (
          %tky       = key-%tky
          TotalPrice = '0.00' ) ).
  ENDMETHOD.

  METHOD acceptTravel.
    MODIFY ENTITIES OF ZI_Travel IN LOCAL MODE
      ENTITY Travel
        UPDATE FIELDS ( OverallStatus )
        WITH VALUE #( FOR key IN keys (
          %tky          = key-%tky
          OverallStatus = 'A' ) )
      FAILED   failed
      REPORTED reported.

    READ ENTITIES OF ZI_Travel IN LOCAL MODE
      ENTITY Travel ALL FIELDS WITH CORRESPONDING #( keys )
      RESULT result
      FAILED failed.
  ENDMETHOD.
ENDCLASS.
```

---

## Projection view + BDEF

```abap
" Projection CDS view (UI-facing)
@EndUserText.label: 'Travel - Projection'
@AccessControl.authorizationCheck: #NOT_REQUIRED
define root view entity ZC_Travel
  provider contract transactional_ui
  as projection on ZI_Travel
{
  key TravelUUID,
      TravelID,
      @UI.lineItem: [{ position: 10 }]
      @UI.selectionField: [{ position: 10 }]
      AgencyID,
      BeginDate,
      EndDate,
      @UI.lineItem: [{ position: 50, criticality: 'OverallStatusCriticality' }]
      OverallStatus,
      _Items : redirected to composition child ZC_TravelItem
}

" Projection BDEF — thin layer, no business logic here
projection;
strict ( 2 );
use draft;

define behavior for ZC_Travel alias Travel
{
  use create;
  use update;
  use delete;
  use action acceptTravel;
  use action rejectTravel;
  use draft action Edit;
  use draft action Activate;
  use draft action Discard;
  use draft action Resume;
  use association _Items { create; with draft; }
}
```

---

## Service Definition + Binding

```abap
" Service Definition
@EndUserText.label: 'Travel Service'
define service ZUI_Travel_O4 {
  expose ZC_Travel as Travel;
  expose ZC_TravelItem as TravelItem;
  expose /DMO/I_Agency as Agency;
}
```

Activate the Service Binding `ZUI_Travel_O4_VR` as OData V4 UI binding in ADT.

---

## Common mistakes to avoid

- ❌ Adding business logic in the projection BDEF or projection view
- ✅ Keep projection thin — UI labels, field aliases, and `use` statements only. Interface behavior = business logic layer.

- ❌ Calling `MODIFY ENTITIES` without `IN LOCAL MODE` inside a handler
- ✅ Always use `IN LOCAL MODE` for internal modifications to avoid authority checks and lock issues

- ❌ Skipping draft handling and adding it later
- ✅ Enable draft from the start — retrofitting draft into an existing RAP BO is complex

- ❌ Using `strict ( 1 )` in new development
- ✅ Always use `strict ( 2 )` — enables the most comprehensive BDEF syntax checks

- ❌ Implementing CRUD in unmanaged when you have direct table access
- ✅ Use managed implementation for greenfield with direct table access

- ❌ Forgetting `etag master` and `lock master` in the root BDEF
- ✅ Always define ETag for optimistic locking and lock master for draft

- ❌ Missing `@Semantics.systemDateTime` and `@Semantics.user` annotations on admin fields
- ✅ These annotations are required for managed RAP to auto-populate timestamps and users
