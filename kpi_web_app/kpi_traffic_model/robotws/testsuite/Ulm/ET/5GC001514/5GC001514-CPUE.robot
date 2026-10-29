*** Settings ***

Documentation   This is a Robot Test Suite for subfeature 5GC001514 'CPUE crash and recovery'
...             Team: 'MN RAN L3 SW ULM L3NRT 07 SG 60'
#-------------------------------------------------------------------------------------------------------------

Resource        5GC001514-keywords.robot
Resource        5GC001514-keywords-traffic.robot
Resource        5GC001514-keywords-wireshark.robot
Resource        ../5GC000480/keywordbook-480-resourceUsage.robot


Suite Setup       5GC001514-keywords.Prepare TL
Suite Teardown    5GC001514-keywords.Perform Suite Teardown


*** Variables ***

${logs_collected}       False

${tcpdump_running}      false
${process}              cpue
${process_name}         CPUENODE

${unit1}                fsp5s0icom
${unit1_container1}     0x2734
${unit1_container2}     0x2735

${unit2}                fsp6s0icom
${unit2_container1}     0x2834
${unit2_container2}     0x2835


${kill_cmd}             pkill -15 cp_ue

${ue_id}                101
${cell_id}              1


*** Test Cases ***

5GC001514_Partial_CPUE_crash_and_recovery
    [Documentation]    This Test Scenario verifies that CPUE is successfully restarted after crash of one process

    [Tags]     t1
    [Setup]    5GC001514-keywords.Perform Test Setup

    5GC001514-keywords.set actForceUnitAutoReset to false
    keywordbook-480-resourceUsage.Get Resources Taken before_test
    5GC001514-keywords.Lock BBMOD2 And Attach UE And Unlock BBMOD2 And Run Traffic

    Crash CPUE Process And Wait For Cell onAir   number_of_CPUE=1
    5GC001514-keywords.Trigger sgNBaddition And Run Traffic
    5GC001514-keywords.Detach Single UE

    keywordbook-480-resourceUsage.Get Resources Taken after_test
    keywordbook-480-resourceUsage.No Check Of Resource nbOfFreeCRNTI
    keywordbook-480-resourceUsage.No Check Of Resource postTimerWheel
    keywordbook-480-resourceUsage.Verify Resource Usage
    5GC001514-keywords-traffic.Verify Traffic Statistics After Crash
    5GC001514-keywords-wireshark.Verify Wireshark Cell Not Available

    [Teardown]   5GC001514-keywords.Perform Test Teardown



5GC001514_CPUE_crash_and_recovery
    [Documentation]    This Test Scenario verifies that CPUE is successfully restarted after crash of 2 processes

    [Tags]     t2
    [Setup]    5GC001514-keywords.Perform test setup

    5GC001514-keywords.set actForceUnitAutoReset to false
    keywordbook-480-resourceUsage.Get Resources Taken before_test
    5GC001514-keywords.Lock BBMOD2 And Attach UE And Unlock BBMOD2 And Run Traffic

    Crash CPUE Process And Wait For Cell onAir   number_of_CPUE=2
    5GC001514-keywords.Trigger sgNBaddition And Run Traffic
    5GC001514-keywords.Detach Single UE

    keywordbook-480-resourceUsage.Get Resources Taken after_test
    keywordbook-480-resourceUsage.No Check Of Resource nbOfFreeCRNTI
    keywordbook-480-resourceUsage.No Check Of Resource postTimerWheel
    keywordbook-480-resourceUsage.Verify Resource Usage
    5GC001514-keywords-traffic.Verify Traffic Statistics After Crash
    5GC001514-keywords-wireshark.Verify Wireshark X2AP NGAP Reset

    [Teardown]   5GC001514-keywords.Perform Test Teardown


*** Keywords ***

Crash CPUE Process And Wait For Cell onAir
    [Documentation]    [PRIVATE]   crash CPUE process, wait for integratedToRan, wait for cell onAir
    ...     :Autor: Sylvia Schneider
    [Arguments]      ${number_of_CPUE}
    5GC001514-keywords.Start Tcpdump Recording
    Run Keyword   Kill Process ${number_of_CPUE} CPUE
    5GC001514-keywords.Check gNB onAir
    5GC001514-keywords.Stop Tcpdump Recording


Kill Process 1 CPUE
    [Documentation]    [PRIVATE]   kill 1 CPUE process
    ...     :Autor: Sylvia Schneider
    Log To Console    \nCPUE crash executed with ${kill_cmd} on 1 CPUE

    ${gNBCommUnit_alias}    Wait Until Keyword Succeeds
    ...    ${SSH_AUTHENTICATION_TIMEOUT}   ${SSH_AUTHENTICATION_RETRY_INTERVAL}
    ...    connect.Connect to Node Common Unit
    Sleep    2s

    ${rm_cmd}  Set Variable  rm /user/toor4nsn/.ssh/known_hosts${\n}
    ssh.Send Command    command=${rm_cmd}    timeout=60s     get_pty=True   connection=${gNBCommUnit_alias}

    Start Ssh Session With Address     ${gNBCommUnit_alias}  ${unit_addr1}
    Attach To Container    ${gNBCommUnit_alias}    ${unit1_container1}
    ssh.Write Input    ${kill_cmd}${\n}   connection=${gNBCommUnit_alias}
    ssh.Read Output Until   asp-5a:~${SPACE}>    timeout=10   connection=${gNBCommUnit_alias}
    sleep   40s
    [Teardown]   ssh.Disconnect   connection=${gNBCommUnit_alias}


Kill Process 2 CPUE
    [Documentation]    [PRIVATE]   kill CPUE 2 process
    ...     :Autor: Sylvia Schneider
    Log To Console    \nCPUE crash executed with ${kill_cmd} on 2 CPUEs

    ${gNBCommUnit_alias}    wait until keyword succeeds
    ...    ${SSH_AUTHENTICATION_TIMEOUT}   ${SSH_AUTHENTICATION_RETRY_INTERVAL}
    ...    connect.Connect to Node Common Unit
    Sleep    2s

    ${rm_cmd}  Set Variable  rm /user/toor4nsn/.ssh/known_hosts${\n}
    ssh.Send Command    command=${rm_cmd}    timeout=60s     get_pty=True   connection=${gNBCommUnit_alias}

    Start Ssh Session With Address     ${gNBCommUnit_alias}   ${unit_addr1}
    Attach To Container     ${gNBCommUnit_alias}    ${unit1_container1}
    ssh.Write Input         ${kill_cmd}${\n}        connection=${gNBCommUnit_alias}
    ssh.Read Output Until   asp-5a:~${SPACE}>       timeout=10   connection=${gNBCommUnit_alias}
    Attach To Container     ${gNBCommUnit_alias}    ${unit1_container2}
    ssh.Write Input         ${kill_cmd}${\n}        connection=${gNBCommUnit_alias}
    ssh.Read Output Until   asp-5a:~${SPACE}>       timeout=10   connection=${gNBCommUnit_alias}
    ssh.Write Input         exit${\n}               connection=${gNBCommUnit_alias}

    Start Ssh Session With Address     ${gNBCommUnit_alias}   ${unit_addr2}
    Attach To Container     ${gNBCommUnit_alias}    ${unit2_container1}
    ssh.Write Input         ${kill_cmd}${\n}        connection=${gNBCommUnit_alias}
    ssh.Read Output Until   asp-6a:~${SPACE}>       timeout=10   connection=${gNBCommUnit_alias}
    Attach To Container     ${gNBCommUnit_alias}    ${unit2_container2}
    ssh.Write Input    ${kill_cmd}${\n}   connection=${gNBCommUnit_alias}
    ssh.Read Output Until   asp-6a:~${SPACE}>    timeout=10   connection=${gNBCommUnit_alias}
    ssh.Write Input    exit${\n}   connection=${gNBCommUnit_alias}

    Sleep   40s
    [Teardown]   ssh.Disconnect   connection=${gNBCommUnit_alias}



Start Ssh Session With Address
    [Documentation]    [PRIVATE]   start ssh session to specified address
    ...     :Autor: Sylvia Schneider
    [Arguments]     ${gNBCommUnit_alias}  ${unit_addr}
    ${cmd}  Set Variable  ssh -o StrictHostKeyChecking=no toor4nsn@${unit_addr}${\n}
    ssh.Send Command    command=${cmd}    timeout=60s     get_pty=True   connection=${gNBCommUnit_alias}
    Sleep    1s
    ssh.Write Input    oZPS0POrRieRtu${\n}     connection=${gNBCommUnit_alias}
    ${output}    ssh.Read Output Until   ${SPACE}>    timeout=10   connection=${gNBCommUnit_alias}
    Sleep    1s
