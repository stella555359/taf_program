*** Settings ***
Documentation
...         author: Lixia.tang
...         contact: lixia.tang@nokia-sbell.com
...         squad group: 5G_PZ_MMW_HZ_3_SG
...         Robust test

Resource    ./Resources/CB013125_Common_Keywords.robot


*** Test Cases ***
[1]CB013125_SCF_Commission_in_Loops
    [Setup]    Test Case setup
    [Timeout]    500min
    # NPI_Type1.xml loop 10 times
    FOR    ${i}    IN RANGE    10
        ${scf_path}=    CI_commssion.Get SCF File Path    testline=7_5_UTE5G402T594    stream=NPI_Type1
        Set Suite Variable    ${SCF_Path}    ${scf_path}
        SCF Commission 1 times
    END
    # NPI_Type2.1.xml loop 10 times
    FOR    ${i}    IN RANGE    10
        ${scf_path}=    CI_commssion.Get SCF File Path    testline=7_5_UTE5G402T594    stream=NPI_Type2.1
        Set Suite Variable    ${SCF_Path}    ${scf_path}
        SCF Commission 1 times
    END
    # NPI_Type3.1.xml loop 10 times
    FOR    ${i}    IN RANGE    10
        ${scf_path}=    CI_commssion.Get SCF File Path    testline=7_5_UTE5G402T594    stream=NPI_Type3.1
        Set Suite Variable    ${SCF_Path}    ${scf_path}
        SCF Commission 1 times
    END
    [Teardown]    Test Case teardown

[1]CB013125_BB_Reset_in_Loops
    [Setup]    Site Reset 1 Times
    [Timeout]    500min
    BBMOD Reset 30 Times
    [Teardown]    Test Case teardown

[1]CB013125_RAT_Reset_in_Loops
    [Setup]    Site Reset 1 Times
    [Timeout]    500min
    LTE RAT Reset 30 Times
    NR RAT Reset 30 Times
    [Teardown]    Test Case teardown
