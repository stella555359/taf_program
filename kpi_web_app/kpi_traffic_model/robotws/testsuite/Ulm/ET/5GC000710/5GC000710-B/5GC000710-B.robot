*** Settings ***

Documentation   This is a Robot Test Suite for subfeature 5GC000710-B
...             Team: 'MN RAN L3 SW ULM L3NRT 07 SG'
...             Author: Sylvia Schneider
#-------------------------------------------------------------------------------------------------------------
Resource        ../../5GC000480/keywordbook-480.robot
Resource        5GC000710-B-commissioning.robot
Resource        5GC000710-B-keywords.robot
Resource        5GC000710-B-verify.robot
Resource        5GC000710-B-wts.robot

Resource        ../../../resources/Common/reporting.robot

Library          taf.config.wts    WITH NAME    wts


Suite Setup       Suite Setup 710B
Suite Teardown    Suite Teardown 710B


*** Variables ***
${logs_collected}                     False
&{SCF}                                &{EMPTY}


*** Test Cases ***

5GC000710_B_SA_RFSP_index_transferred_and_stored_during_Xn_handover
    [Documentation]    This Test Scenario verifies RFSP index during XN handover
    [Tags]   t1    CDRT    CRT
    [Setup]   Perform Preconditions of Test Scenario 710B
    activate SCF and bring tl onAir
    start wireshark trace
    set AMF param indexToRFSP
    register UE and start PDU
    execute handover scenario
    stop wireshark trace
    stop PDU and deregister UE
    verify wireshark initialContextSetup and handover
    [Teardown]   Perform Postconditions of Test Scenario 710B


5GC000710_B_SA_UE_context_modification_request_with_index_to_RFSP
    [Documentation]    This Test Scenario verifies RFSP index in modify phase
    [Tags]   t2    CRT
    [Setup]   Perform Preconditions of Test Scenario 710B
    activate SCF and bring tl onAir
    start wireshark trace
    set AMF param indexToRFSP
    register UE and start PDU
    modify indexToRFSP
    send A3 measurement
    stop wireshark trace
    stop PDU and deregister UE
    verify wireshark UEContextModification
    [Teardown]   Perform Postconditions of Test Scenario 710B


5GC000710_B_SA_DL_NAS_transport_with_index_to_RFSP
    [Documentation]    This Test Scenario verifies RFSP index in NAS
    [Tags]   t3    CRT
    [Setup]   Perform Preconditions of Test Scenario 710B
    activate SCF and bring tl onAir
    start wireshark trace
    register UE and start PDU
    set AMF dl param indexToRFSP
    send A3 measurement
    stop wireshark trace
    stop PDU and deregister UE
    verify wireshark NAS dl
    [Teardown]   Perform Postconditions of Test Scenario 710B


*** Keywords ***
Suite Setup 710B
    [Documentation]    [PRIVATE]    Prepare TL for 5GC000710-B
    ...       :Autor: Sylvia Schneider
    Create ips for simulated gnb
    Create Test Suite Folders
    Get test variables and upload start SCF
    UTE Cloud Workaround
    Check TL Infos
    gnb.Store Current SCF from gNB
    get plmn nrarfcn tac version from gNB SCF
    gnb.Store Current swconfig from gNB
    Store Current swconfig from Airphone
    Store Current WTS Config
    Update wts file for TC 710B
    Upload Customized WTS Config    config_path=${resultBaseDir}/basic_wts_710B.cfg
    Update SCF


Perform Preconditions of Test Scenario 710B
    [Documentation]    [PRIVATE]    preconditions for 710B
    ...       :Autor: Sylvia Schneider
    Create a Test Scenario Folder


Perform Postconditions of Test Scenario 710B
    [Documentation]    [PRIVATE]    postconditions for 710B
    ...       :Autor: Sylvia Schneider
    Run Keyword And Continue On Failure   Set SCOUT TC ID for Reporting
    Run Keyword And Continue On Failure   stop wireshark trace     wireshark_store=${resultDir}/wireshark_test_teardown.pcap
    Run Keyword And Continue On Failure   Teardown Egate Connection for Airphone
    Run Keyword And Continue On Failure   Teardown Edaemon Connection for Airphone    edaemon_alias=edaemon
    IF    '${TEST STATUS}'=='FAIL'    Collect snapshot and sos report data     ${resultDir}


Suite Teardown 710B
    [Documentation]    [PRIVATE]    suite teardown for 710B
    ...       :Autor: Sylvia Schneider
    Run Keyword And Continue On Failure   stop wireshark trace      wireshark_store=${resultBaseDir}/wireshark_suite_teardown.pcap
    IF    '${SUITE STATUS}'=='FAIL' and '${logs_collected}'=='False'    Collect snapshot and sos report data   ${resultBaseDir}
    Reload Stored WTS Config
