*** Settings ***

Documentation    :copyright: Nokia

Library      ta5g_testline_management
Library      ta5g_admin_operations
Library      ta5g_ue_measurements
Library      ta5g_iphy
Library      ta5g_pm_counters

*** Variables ***
${UE_ID_A_B2_4}=    12
${UE_ID_A_B3_4}=    13
${UE_ID}=    11
${NRREL_OBJECT_CREATION_TIME}=    120
${EXPECTED_NRREL_OBJECTID}=    256

*** Keywords ***
Verify Existing NRREL
    Wait For Object To Exist    object_name=NRCELL_A-1/NRREL_A-${EXPECTED_NRREL_OBJECTID}    moc=NRREL_A    timeout=${NRREL_OBJECT_CREATION_TIME}

Verify Not Existing NRREL
    Wait For Object To Not Exist    object_name=NRCELL_A-1/NRREL_A-${EXPECTED_NRREL_OBJECTID}    moc=NRREL_A    timeout=${NRREL_OBJECT_CREATION_TIME}

Perform A2 And A5 Triggered Handover
    [Documentation]    Triggers A2/A5 HO. Depending on used regexp it expects HO to pass or fail.
    [Arguments]    ${PASS_REGEXP}

    Send Custom Ue Measurement Nr    id=${UE_ID_A_B3_4}    meas_id=1    event=A2    srsrp_nr=30
    ...                              pass_regexp=Sending SgNB Modification Confirm
    Send Custom Ue Measurement Nr    id=${UE_ID_A_B3_4}    meas_id=3    event=A5    srsrp_nr=19    phycell_id=51    nrsrp_nr=68
    ...                              pass_regexp=${PASS_REGEXP}
