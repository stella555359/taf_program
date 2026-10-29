*** Settings ***

Documentation   This is a Robot Test Suite for Feature 5GC000795 'Multiple DRBs per UE in NSA'
...             Following Subfeatures are covered:
...                 5GC000795-A SgNB Addition and SgNG Release for multiple DRBs
...                 5GC000795-B SgNB modification for DRB addition or DRB release
...                 5GC000795-D inactivity detection with multiple DRBs
...             Team: ' MN RAN L3 SW ULM L3NRT 05 SG SQD65'
...             Email: 'I_MN_RAN_L3_SW_ULM_SQD_65@internal.nsn.com'
...             UTE Testline Type: CLOUD_5G_I_LO_AP_LO, VARIANT_SANSA_FS_CPRI_CMWV_FDD+ECPRI_CMWV_TDD_AEQE
#------------------------------------------------------------------------------------------------------------------------------------[150 characters]


Resource        5GC000795-A-B-D_Keywords.robot

Library         ./5GC000795-A-B-D.py


Suite Setup     Run Keywords
...             Sqd65 Common Setup                                                       AND
...             Activate 5GC000795 Feature                                               AND
...             Bring Airphone TL to on Air status

Suite Teardown  Run Keywords
...             Sqd65 Common Teardown                                                    AND
...             Reload Stored WTS Config

Test Teardown   Stop Logging

*** Test Cases ***

[1]TC_SgNB_Addition_with_several_E_RAB
    [Documentation]    check SgNB Addition and Release with 2 DRBs without traffic
    [Tags]  CIT
    [Setup]   Perform Preconditions of Test Scenario    pmcounter_enabled=${FALSE}
    Attach UE to LTE    ue_id=101
    Sleep   2s
    Add Bearer on eNB for UE and verify if created
    Sleep   2s
    Activate LTE-NR Dual Connectivity for bearers   bearer_id=2,7
    Sleep   2s
    Release UE dual connectivity bearers 2 and 7 and specified cause
    Sleep   2s
    Detach UE from LTE  ue_id=101


[2]TC_SgNB_Addition_with_several_E_RAB
    [Documentation]    check SgNB Addition and Release with 2 DRBs with traffic
    [Tags]  CRT    AP_REG
    [Setup]   Perform Preconditions of Test Scenario
    Attach UE to LTE     ue_id=101
    Sleep   2s
    Add Bearer on eNB for UE and verify if created   bearer_id=7
    Sleep   2s
    Start Data Traffic DL_UL on bearers 2 and 7
    Sleep   2s
    Activate LTE-NR Dual Connectivity for bearers   bearer_id=2,7
    Sleep   2s
    Release UE dual connectivity bearers 2 and 7 and specified cause
    Sleep   2s
    Stop Data Traffic on bearers 2 and 7
    Get Bearer Stats from 2 and 7
    Sleep   2s
    Detach UE from LTE  ue_id=101
    Verify SgNBadd_several_ERab_TC2 PMCounters


[1]5GC000795_B_TC100_Add_new_DRBs_with_UL_DL_traffic_by_SgNB_modification
    [Documentation]    check SgNB_modification for DRB addition and SgNB_modification for DRB release with traffic
    [Tags]   CRT    AP_REG
    [Setup]   Perform Preconditions of Test Scenario
    Attach UE to LTE  ue_id=101
    Sleep   2s
    Activate LTE-NR Dual Connectivity for bearers   bearer_id=2
    Sleep   2s
    Add Bearer on eNB for UE and verify if created   bearer_id=7
    Sleep   2s
    Activate LTE-NR DC modification    bearer_id=7   reason=bearer_to_add
    Sleep   2s
    Start Data Traffic DL_UL on bearer 7
    Sleep   2s
    Activate LTE-NR DC modification release   bearer_id=7
    Sleep   2s
    Stop Data Traffic on bearer 7
    Get Bearer Stats from 7
    Sleep   2s
    Detach UE from LTE  ue_id=101
    Verify B_TC100 PMCounters


[1]5GC000795_D_TC34_UE_Inactivity_detection_on_all_the_bearers_SGNB_release
    [Documentation]   This test shall validate UE Inactivity detection on all the bearers and SgNB release for nsaActivityNotificationLevel = drb
    [Tags]   CRT  TC34
    [Setup]   Perform Preconditions of Test Scenario    pmcounter_enabled=${FALSE}
    Set Inactivity Timer Parameters     true  1  drb
    Attach UE to LTE  ue_id=101
    Sleep   2s
    Add Bearer on eNB for UE and verify if created   bearer_id=7
    Sleep   2s
    Start Data Traffic DL on bearers 2 and 7
    Activate LTE-NR Dual Connectivity for bearers   bearer_id=2,7
    Sleep   2s
    Get Average Data Rate via Egate   ue_id=101    dir=dl   trf_id=1   id=2
    Stop Data Traffic DL on bearer 2
    Sleep  20s
    Get Average Data Rate via Egate   ue_id=101    dir=dl   trf_id=1   id=7
    Stop Data Traffic DL on bearer 7
    Sleep  20s
    Get Bearer Stats from 2 and 7
    Sleep   2s
    Detach UE from LTE  ue_id=101
    Set Inactivity Timer Parameters     false  60  ue
    ${final_log_to_verify}   Save EGATE Log   tc34_1_end
    Verify final log for D_TC34   ${final_log_to_verify}


[2]5GC000795_D_TC34_UE_Inactivity_detection_on_all_the_bearers_SGNB_release
    [Documentation]   This test shall validate UE Inactivity detection on all the bearers and SgNB release for nsaActivityNotificationLevel = ue
    [Tags]   CRT  TC34
    [Setup]   Perform Preconditions of Test Scenario    pmcounter_enabled=${FALSE}
    Set Inactivity Timer Parameters     true  1  ue
    Attach UE to LTE  ue_id=101
    Sleep   2s
    Add Bearer on eNB for UE and verify if created   bearer_id=7
    Sleep   2s
    Start Data Traffic DL on bearers 2 and 7
    Sleep   2s
    Activate LTE-NR Dual Connectivity for bearers   bearer_id=2,7
    Sleep   2s
    Get Average Data Rate via Egate   ue_id=101    dir=dl   trf_id=1   id=2
    Stop Data Traffic DL on bearer 2
    Sleep  20s
    Get Average Data Rate via Egate   ue_id=101    dir=dl   trf_id=1   id=7
    Stop Data Traffic DL on bearer 7
    Sleep  20s
    Get Bearer Stats from 2 and 7
    Sleep   2s
    Detach UE from LTE  ue_id=101
    Set Inactivity Timer Parameters     false  60  ue
    ${final_log_to_verify}   Save EGATE Log   tc34_2_end
    Verify final log for D_TC34   ${final_log_to_verify}


[1]5GC000795-A-5GC000425-X_unbalanced_traffic_on_different_bearers
    [Documentation]   This test shall check that  DL traffic on one DRB bigger than radio capability
    ...               shall not kill DL traffic on DRBs with low troughput.
    ...               In order to reduce the cell radio capability to 25Mbps we shall disable Radio Link Adaptation
    ...               and set to 0 the initial MCS
    [Tags]   CRT
    [Setup]   Perform Preconditions of Test Scenario
    Activate Reduced pdcpBufDiscardThreshold
    Attach UE to LTE  ue_id=101
    Sleep   2s
    Add Bearer on eNB for UE and verify if created   bearer_id=7
    Sleep   2s
    Activate LTE-NR Dual Connectivity for bearers   bearer_id=2,7
    Sleep   2s
    Start Unbalanced Data Traffic DL on bearers 2 and 7
    Sleep  20s
    Get Average Data Rate via Egate   ue_id=101    dir=dl   trf_id=1   id=2
    Get Average Data Rate via Egate   ue_id=101    dir=dl   trf_id=1   id=7
    Release UE dual connectivity bearers 2 and 7 and specified cause
    Sleep   2s
    Get Bearer Stats from 2 and 7
    Sleep   2s
    Detach UE from LTE  ue_id=101
    Verify PMCounters 5GC000425-X unbalanced traffic


5GC000795_B_TC10_Unsuccessful_SgNB_Modification_due_to_deletion_of_unknown_bearer
    [Documentation]   This test shall validate unsuccessful SgNB-modification cause by deletion of unknown bearer
    [Tags]   CRT
    [Setup]   Perform Preconditions of Test Scenario
    Attach UE to LTE  ue_id=101
    Sleep   2s
    Activate LTE-NR Dual Connectivity for bearer 2 and verifiy UE IDs
    Start Data Traffic with defined conditions   trf_id=1   direction=dl
    Start Data Traffic with defined conditions   trf_id=2   direction=ul
    Sleep  10s   let traffic run for a while
    Add bearer    ue_id=101    bearer_id=7
    Sleep   2s
    Trigger LTE-NR dual connectivity modification    ue_id=101   bearer_id=7   reason=bearer_to_add
    Sleep   2s
    Trigger LTE-NR dual connectivity modification    ue_id=101   bearer_id=7   reason=bearer_to_release
    Sleep   2s
    Activate LTE-NR DC modification release of unkown bearer
    Sleep  120s   time needed to transmit all 30000 packets
    Get Average Data Rate via Egate   ue_id=101    dir=dl   trf_id=1   id=2
    Get Average Data Rate via Egate   ue_id=101    dir=ul   trf_id=2   id=2
    Sleep   2s
    Detach UE from LTE  ue_id=101
    ${final_log_to_verify}   Save EGATE Log   tc10_end
    Verify B_TC10 PMCounters
    Verify final log for B_TC10   ${final_log_to_verify}


[1]5GC000795_B_TC01_Add_new_DRBs_without_traffic_by_SgNB_modification
    [Documentation]    check SgNB_modification for DRB addition and SgNB_modification for DRB release without traffic
    [Tags]  CRT
    [Setup]   Perform Preconditions of Test Scenario  pmcounter_enabled=${FALSE}
    Attach UE to LTE  ue_id=101
    Sleep   2s
    Activate LTE-NR Dual Connectivity for bearers   bearer_id=2
    Sleep   2s
    Add Bearer on eNB for UE and verify if created
    Sleep   2s
    Activate LTE-NR DC modification   bearer_id=7   reason=bearer_to_add
    Sleep   2s
    Activate LTE-NR DC modification release   bearer_id=7
    Sleep   2s
    Detach UE from LTE  ue_id=101


5GC000795_B_TC11_SgNB_Reconfiguration_Failure_during_SgNB_Modification_Successful_SgNB_Release
    [Documentation]   This test shall validate SgNB-reconfiguration failure during SgNB-modification successful SgNB-release
    [Tags]   CRT
    [Setup]   Perform Preconditions of Test Scenario  pmcounter_enabled=${FALSE}
    Attach UE to LTE  ue_id=101
    Sleep   2s
    Activate LTE-NR Dual Connectivity for bearers   bearer_id=2
    Sleep   2s
    Add Bearer on eNB for UE and verify if created   bearer_id=7   filter_value=7   precedence_value=7
    Sleep   2s
    Run simple Egate Command
    ...              enb_endc_param id=1 menb_failure_scenario=dont_send_sgnb_reconf_complete
    Activate LTE-NR DC modification    bearer_id=7   reason=bearer_to_add   pass_expression=SgNBReleaseRequired
    Sleep   2s
    Run simple Egate Command
    ...              enb_endc_param id=1 reset
    Detach UE from LTE  ue_id=101


*** Keywords ***


Perform Preconditions of Test Scenario
    [Arguments]    ${pmcounter_enabled}=${TRUE}
    Create Testcase Log Directory
    IF    '${PREV_TEST_STATUS}'=='FAIL'
        Teardown Egate Connection for Airphone
        Teardown Edaemon Connection for Airphone
        Bring Airphone TL to on Air status
    END
    Send Egate Command and verify output     cmd=enb_param id=1 endc_capable_qci=all
    Start Logging    ${pmcounter_enabled}
