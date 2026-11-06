" ─── Template: Managed RAP Business Object with Draft ───────────────────────
" Replace: ZMyEntity → your entity name, zmyentity → your table name
" Replace: ZI_ → your interface namespace prefix
" Replace: ZC_ → your consumption namespace prefix
" Replace: ZBP_ → your behavior pool prefix
" Replace: ZUI_MyEntity_O4 → your service name

" ─── 1. DDIC Table (SE11 / ADT) ──────────────────────────────────────────────
" @EndUserText.label: 'My Entity Table'
" define table zmyentity {
"   key client        : abap.clnt not null;
"   key entity_uuid   : sysuuid_x16 not null;
"   entity_id         : abap.numc(8);
"   description       : abap.char(100);
"   status            : abap.char(1);
"   created_at        : abp_creation_tstmpl;
"   created_by        : abp_creation_user;
"   last_changed_at   : abp_lastchange_tstmpl;
"   last_changed_by   : abp_lastchange_user;
"   local_last_changed_at : abp_locinst_lastchange_tstmpl;
" }

" ─── 2. Interface CDS View Entity ────────────────────────────────────────────
@AccessControl.authorizationCheck: #CHECK
@EndUserText.label: 'My Entity'
define root view entity ZI_MyEntity
  as select from zmyentity
{
  key entity_uuid          as EntityUUID,
      entity_id            as EntityID,
      description          as Description,
      status               as Status,
      @Semantics.systemDateTime.createdAt: true
      created_at           as CreatedAt,
      @Semantics.user.createdBy: true
      created_by           as CreatedBy,
      @Semantics.systemDateTime.lastChangedAt: true
      last_changed_at      as LastChangedAt,
      @Semantics.user.lastChangedBy: true
      last_changed_by      as LastChangedBy,
      @Semantics.systemDateTime.localInstanceLastChangedAt: true
      local_last_changed_at as LocalLastChangedAt
}

" ─── 3. Behavior Definition ──────────────────────────────────────────────────
managed implementation in class ZBP_MyEntity unique;
strict ( 2 );
with draft;

define behavior for ZI_MyEntity alias MyEntity
  persistent table zmyentity
  draft table zmyentity_d
  etag master LocalLastChangedAt
  lock master total etag LastChangedAt
  authorization master ( global )
{
  field ( readonly ) EntityUUID, EntityID, CreatedAt, CreatedBy, LastChangedAt, LastChangedBy, LocalLastChangedAt;
  field ( numbering : managed, readonly ) EntityUUID;

  create;
  update;
  delete;

  draft action Edit;
  draft action Activate optimized;
  draft action Discard;
  draft action Resume;

  mapping for zmyentity {
    EntityUUID          = entity_uuid;
    EntityID            = entity_id;
    Description         = description;
    Status              = status;
    CreatedAt           = created_at;
    CreatedBy           = created_by;
    LastChangedAt       = last_changed_at;
    LastChangedBy       = last_changed_by;
    LocalLastChangedAt  = local_last_changed_at;
  }
}

" ─── 4. Projection CDS View ──────────────────────────────────────────────────
@EndUserText.label: 'My Entity - Projection'
@AccessControl.authorizationCheck: #NOT_REQUIRED
define root view entity ZC_MyEntity
  provider contract transactional_ui
  as projection on ZI_MyEntity
{
  key EntityUUID,
      EntityID,
      @UI.lineItem: [{ position: 10 }]
      @UI.selectionField: [{ position: 10 }]
      Description,
      @UI.lineItem: [{ position: 20 }]
      Status
}

" ─── 5. Projection Behavior Definition ───────────────────────────────────────
projection;
strict ( 2 );
use draft;

define behavior for ZC_MyEntity alias MyEntity
{
  use create;
  use update;
  use delete;
  use draft action Edit;
  use draft action Activate;
  use draft action Discard;
  use draft action Resume;
}

" ─── 6. Service Definition ───────────────────────────────────────────────────
" @EndUserText.label: 'My Entity Service'
" define service ZUI_MyEntity_O4 {
"   expose ZC_MyEntity as MyEntity;
" }
