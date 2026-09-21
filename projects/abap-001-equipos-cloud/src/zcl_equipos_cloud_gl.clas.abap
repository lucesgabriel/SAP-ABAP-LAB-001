"! <p class="shorttext synchronized">Lista de equipos PM - version ABAP Cloud (consola ADT)</p>
"! Version cloud-ready de ZR_ALV_EQUIPOS_GL:
"! - EQUI / EQKT sustituidas por las vistas CDS liberadas I_Equipment / I_EquipmentText
"! - REPORT, pantalla de seleccion y ALV sustituidos por clase global + IF_OO_ADT_CLASSRUN
CLASS zcl_equipos_cloud_gl DEFINITION
  PUBLIC FINAL CREATE PUBLIC.

  PUBLIC SECTION.
    INTERFACES if_oo_adt_classrun.

    TYPES: BEGIN OF ty_equipo,
             equipment           TYPE i_equipment-equipment,
             equipmentname       TYPE i_equipmenttext-equipmentname,
             equipmentcategory   TYPE i_equipment-equipmentcategory,
             technicalobjecttype TYPE i_equipment-technicalobjecttype,
             manufacturer        TYPE i_equipment-assetmanufacturername,
             modelnumber         TYPE i_equipment-manufacturerparttypename,
             serialnumber        TYPE i_equipment-manufacturerserialnumber,
             creationdate        TYPE i_equipment-creationdate,
             createdbyuser       TYPE i_equipment-createdbyuser,
           END OF ty_equipo,
           ty_equipos TYPE STANDARD TABLE OF ty_equipo WITH EMPTY KEY.

    TYPES: ty_r_equipment TYPE RANGE OF i_equipment-equipment,
           ty_r_category  TYPE RANGE OF i_equipment-equipmentcategory,
           ty_r_objtype   TYPE RANGE OF i_equipment-technicalobjecttype,
           ty_r_credate   TYPE RANGE OF i_equipment-creationdate.

    " Criterios de seleccion (sustituyen a la pantalla de seleccion del report)
    TYPES: BEGIN OF ty_criterios,
             equipment    TYPE ty_r_equipment,
             category     TYPE ty_r_category,
             objecttype   TYPE ty_r_objtype,
             creationdate TYPE ty_r_credate,
             max_rows     TYPE i,
           END OF ty_criterios.

    "! Lee equipos desde las vistas CDS liberadas
    METHODS get_equipos
      IMPORTING is_criterios      TYPE ty_criterios
      RETURNING VALUE(rt_equipos) TYPE ty_equipos.

  PRIVATE SECTION.
    CONSTANTS c_max_rows_default TYPE i VALUE 500.

    "! Valores por defecto de la ejecucion en consola (F9)
    METHODS get_criterios_default
      RETURNING VALUE(rs_criterios) TYPE ty_criterios.

ENDCLASS.

CLASS zcl_equipos_cloud_gl IMPLEMENTATION.

  METHOD if_oo_adt_classrun~main.

    DATA(ls_criterios) = get_criterios_default( ).
    DATA(lt_equipos)   = get_equipos( ls_criterios ).

    IF lt_equipos IS INITIAL.
      out->write( TEXT-001 ). " No se encontraron equipos para la seleccion
      RETURN.
    ENDIF.

    " TEXT-002: Lista de equipos - registros:
    out->write( |{ TEXT-002 } { lines( lt_equipos ) }| ).
    out->write( lt_equipos ).

  ENDMETHOD.

  METHOD get_criterios_default.

    " Equivale a ejecutar el report con tipo de equipo = M
    rs_criterios-category = VALUE #( ( sign = 'I' option = 'EQ' low = 'M' ) ).
    rs_criterios-max_rows = c_max_rows_default.

  ENDMETHOD.

  METHOD get_equipos.
    DATA lv_language TYPE i_equipmenttext-language.

    DATA(lv_max_rows) = COND i( WHEN is_criterios-max_rows > 0
                                THEN is_criterios-max_rows
                                ELSE c_max_rows_default ).

    TRY.
        lv_language = cl_abap_context_info=>get_user_language_abap_format( ).
      CATCH cx_abap_context_info_error.
        lv_language = 'E'.
    ENDTRY.

    SELECT e~equipment,
           t~equipmentname,
           e~equipmentcategory,
           e~technicalobjecttype,
           e~assetmanufacturername    AS manufacturer,
           e~manufacturerparttypename AS modelnumber,
           e~manufacturerserialnumber AS serialnumber,
           e~creationdate,
           e~createdbyuser
      FROM i_equipment AS e
      LEFT OUTER JOIN i_equipmenttext AS t
        ON  t~equipment = e~equipment
        AND t~language  = @lv_language
      WHERE e~equipment           IN @is_criterios-equipment
        AND e~equipmentcategory   IN @is_criterios-category
        AND e~technicalobjecttype IN @is_criterios-objecttype
        AND e~creationdate        IN @is_criterios-creationdate
      ORDER BY e~equipment
      INTO CORRESPONDING FIELDS OF TABLE @rt_equipos
      UP TO @lv_max_rows ROWS.
  ENDMETHOD.

ENDCLASS.
