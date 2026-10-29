*** Settings ***
Documentation     author: ming.shi
...                 contact: ming.shi@nokia.com
...                 squad group: SG_03
...                 feature : CB008148_A case

Resource     testsuite/Hangzhou/RRM/RAN_PZ_HAZ_34/CB008148/Resources/CB008148_common_keywords.robot
Variables    testsuite/Hangzhou/RRM/RAN_PZ_HAZ_34/CB008148/Resources/CB008148_Variables.py
Library      testsuite/Hangzhou/RRM/RAN_PZ_HAZ_34/CB008148/Resources/CB008148_common_keywords.py

Suite Setup    Common Suite Setup For CB008148
Suite Teardown    Common Suite Teardown For CB008148
Test Setup    Common Test Setup for CB008148 without AP
#Test Teardown    Common Test Teardown for CB014044 without AP

*** Variables ***
${log_name_B_01_tc002_1}    log_name_B_01_tc002_1.pcap
${log_name_B_01_tc004_1}    log_name_B_01_tc004_1.pcap
${log_name_B_01_tc004_2}    log_name_B_01_tc004_2.pcap
${log_name_B_01_tc004_3}    log_name_B_01_tc004_3.pcap
${log_name_B_02_tc013_1}    log_name_B_02_tc013_1.pcap

${l2stream3_ttitrace_B_01_tc002_1}    l2stream3_ttitrace_B_01_tc002_1
${l2stream3_ttitrace_B_01_tc002_2}    l2stream3_ttitrace_B_01_tc002_2
${l2stream3_ttitrace_B_02_tc013_1}    l2stream3_ttitrace_B_02_tc013_1
${l2stream3_ttitrace_B_02_tc013_2}    l2stream3_ttitrace_B_02_tc013_2


*** Test Cases ***
[1]CB008148-A#B01_TC002_Verify_TP_On_for_Msg3_in_TDD_FR1_4Rx
    [Documentation]    CB008148A#B01_TC002 Steps:
    [Tags]    CB008148_A
    [Timeout]   2 hours
    paras change on BTS
    ...    paras=${PARAMETERS_CB008148_A_B01_TC002}
    ...    delta_file_name=${epc_log_path}${PARAMETERS_CB008148_A_B01_TC002_JSON_FILE}
#    get and check operationalState of required cells
#    ...    cells=${CB008148_A_B01_TC002_CELLS}
#    ...    states=${CB008148_A_B01_TC002_CELLS_STATUS}[0]
    Wait until keyword succeeds    2m    10s
    ...    get and check operationalState of required cells
    ...    cells=${CB008148_A_B01_TC002_CELLS}    states=${CB008148_A_B01_TC002_CELLS_STATUS}[1]
    PA set required cell to needed value and set other cells to max value
    ...    index=${A_B01_TC002}[index]    values=${A_B01_TC002}[cell_initial_values]
    Capture tcpdump during ue attach    filename=${log_name_B_01_tc002_1}    ues_index=${A_B01_TC002}[ues_index]
    UEs Start UL Data Transfer    ues_index=${A_B01_TC002}[ues_index]    ul_throughput=${A_B01_TC002}[ues_ul_throughput]
    UEs Check Throughput    tput_target=${A_B01_TC002}[ues_ul_tput_target]    ues_index=${A_B01_TC002}[ues_index]    direction=ul
    collect tti logs during adjust pa values
    ...    names=${l2stream3_ttitrace_B_01_tc002_1}
    ...    nr_phy_cell_ids=${A_B01_TC002}[tti_nr_phy_cell_ids]
    ...    start_value=${A_B01_TC002}[start_value]
    ...    end_value=${A_B01_TC002}[end_value]
    ...    step=${A_B01_TC002}[step]
    ...    index=${A_B01_TC002}[index]
    ...    pa_interval_time=${A_B01_TC002}[pa_interval_time]
    ...    direction=increase
    ...    target_dir=${A_B01_TC002}[log_path]
    collect tti logs during adjust pa values
    ...    names=${l2stream3_ttitrace_B_01_tc002_2}
    ...    nr_phy_cell_ids=${A_B01_TC002}[tti_nr_phy_cell_ids]
    ...    start_value=${A_B01_TC002}[end_value]
    ...    end_value=${A_B01_TC002}[start_value]
    ...    step=${A_B01_TC002}[step]
    ...    index=${A_B01_TC002}[index]
    ...    pa_interval_time=${A_B01_TC002}[pa_interval_time]
    ...    direction=decrease
    ...    target_dir=${A_B01_TC002}[log_path]
    get values to check
    ...    names=${l2stream3_ttitrace_B_01_tc002_1}
    ...    fields=${${"ulFdSchedData.dciFormat"},${"ulFdSchedData.puschTPstate"}}
    get values to check
    ...    names=${l2stream3_ttitrace_B_01_tc002_2}
    ...    fields=${${"ulFdSchedData.dciFormat"},${"ulFdSchedData.puschTPstate"}}
    [Teardown]    Run Keywords
    ...    Run keyword if    '${TEST STATUS}' == 'FAIL'    Run keyword and continue on failure    get gnb snapshot
    ...    AND    UEs Stop UL Data Transfer    ues_index=${A_B01_TC002}[ues_index]
    ...    AND    UEs Detach    ues_index=${A_B01_TC002}[ues_index]
    ...    AND    client.stoplog      service=pioneer
    ...    AND    paras change on BTS
    ...    paras=${PARAMETERS_RECOVER_CB008148_A_B01_TC002}
    ...    delta_file_name=${epc_log_path}${PARAMETERS_RECOVER_CB008148_A_B01_TC002_JSON_FILE}
#    ...    AND    get and check operationalState of required cells
#    ...    cells=${CB008148_A_B01_TC002_CELLS}
#    ...    states=${CB008148_A_B01_TC002_CELLS_STATUS}[0]
    ...    AND    Wait until keyword succeeds    2m    10s
    ...    get and check operationalState of required cells
    ...    cells=${CB008148_A_B01_TC002_CELLS}    states=${CB008148_A_B01_TC002_CELLS_STATUS}[1]
    ...    AND    Stop capture syslog via btslog on ute
    ...    AND    syslog analysis via regex file
    ...    AND    Common Test Teardown for CB014044 without AP


[1]CB008148-A#B01_TC004_Verify_TP_On_for_Msg3_during_HO_and_RRE
    [Documentation]    CB008148-A#B01_TC004 Steps:
    [Tags]    CB008148_A
    [Timeout]   2 hours
    paras change on BTS
    ...    paras=${PARAMETERS_CB008148_A_B01_TC004}
    ...    delta_file_name=${epc_log_path}${PARAMETERS_CB008148_A_B01_TC004_JSON_FILE}
    get and check operationalState of required cells
    ...    cells=${CB008148_A_B01_TC004_CELLS}
    ...    states=${CB008148_A_B01_TC004_CELLS_STATUS}[0]
    Wait until keyword succeeds    2m    10s
    ...    get and check operationalState of required cells
    ...    cells=${CB008148_A_B01_TC004_CELLS}    states=${CB008148_A_B01_TC004_CELLS_STATUS}[1]
    PA set required cell to needed value and set other cells to max value
    ...    index=${A_B01_TC004}[index]    values=${A_B01_TC004}[cell_initial_values]
    Capture tcpdump during ue attach    filename=${log_name_B_01_tc004_1}    ues_index=${A_B01_TC004}[ues_index]
    UEs Start DL Data Transfer    ues_index=${A_B01_TC004}[ues_index]    dl_tput_multiue=${A_B01_TC004}[ues_dl_throughput]
    UEs Check Throughput    tput_target=${A_B01_TC004}[ues_dl_tput_target]    ues_index=${A_B01_TC004}[ues_index]    direction=dl
    UEs Start UL Data Transfer    ues_index=${A_B01_TC004}[ues_index]    ul_throughput=${A_B01_TC004}[ues_ul_throughput]
    UEs Check Throughput    tput_target=${A_B01_TC004}[ues_ul_tput_target]    ues_index=${A_B01_TC004}[ues_index]    direction=ul
    Capture tcpdump during loop ho
    ...    filename=${log_name_B_01_tc004_2}
    ...    start_value=${A_B01_TC004}[start_value]
    ...    end_value=${A_B01_TC004}[end_value]
    ...    step=${A_B01_TC004}[step]
    ...    index=${A_B01_TC004}[index]
    ...    pa_interval_time=${A_B01_TC004}[pa_interval_time]
    ...    ho_times=${A_B01_TC004}[ho_times]
    Capture tcpdump during loop Reestablish
    ...    filename=${log_name_B_01_tc004_3}
    ...    source_initial_value=${A_B01_TC004}[reestablish_source_initial_value]
    ...    target_initial_value=${A_B01_TC004}[reestablish_target_initial_value]
    ...    source_index=${A_B01_TC004}[reestablish_source_index]
    ...    target_index=${A_B01_TC004}[reestablish_target_index]
    ...    pa_interval_time=${A_B01_TC004}[reestablish_pa_interval_time]
    ...    Reestablish_times=${A_B01_TC004}[reestablish_times]
    [Teardown]    Run Keywords
    ...    Run keyword if    '${TEST STATUS}' == 'FAIL'    Run keyword and continue on failure    get gnb snapshot
    ...    AND    UEs Stop DL Data Transfer    ues_index=${A_B01_TC004}[ues_index]
    ...    AND    UEs Stop UL Data Transfer    ues_index=${A_B01_TC004}[ues_index]
    ...    AND    UEs Detach    ues_index=${A_B01_TC004}[ues_index]
    ...    AND    client.stoplog      service=pioneer
    ...    AND    paras change on BTS
    ...    paras=${PARAMETERS_RECOVER_CB008148_A_B01_TC004}
    ...    delta_file_name=${epc_log_path}${PARAMETERS_RECOVER_CB008148_A_B01_TC004_JSON_FILE}
    ...    AND    get and check operationalState of required cells
    ...    cells=${CB008148_A_B01_TC004_CELLS}
    ...    states=${CB008148_A_B01_TC004_CELLS_STATUS}[0]
    ...    AND    Wait until keyword succeeds    2m    10s
    ...    get and check operationalState of required cells
    ...    cells=${CB008148_A_B01_TC004_CELLS}    states=${CB008148_A_B01_TC004_CELLS_STATUS}[1]
    ...    AND    Stop capture syslog via btslog on ute
    ...    AND    syslog analysis via regex file
    ...    AND    Common Test Teardown for CB014044 without AP

[1]CB008148-A#B02_TC013_Verify_TP_On_for_DCI_0_0_with_8Rx_16Rx_Configs
    [Documentation]    CB008148-A#B02_TC013 Steps:
    [Tags]    CB008148_A
    [Timeout]   2 hours
    paras change on BTS
    ...    paras=${PARAMETERS_CB008148_A_B02_TC013}
    ...    delta_file_name=${epc_log_path}${PARAMETERS_CB008148_A_B02_TC013_JSON_FILE}
    get and check operationalState of required cells
    ...    cells=${CB008148_A_B02_TC013_CELLS}
    ...    states=${CB008148_A_B02_TC013_CELLS_STATUS}[0]
    Wait until keyword succeeds    2m    10s
    ...    get and check operationalState of required cells
    ...    cells=${CB008148_A_B02_TC013_CELLS}    states=${CB008148_A_B02_TC013_CELLS_STATUS}[1]
    PA set required cell to needed value and set other cells to max value
    ...    index=${A_B02_TC013}[index]    values=${A_B02_TC013}[cell_initial_values]
    Capture tcpdump during ue attach    filename=${log_name_B_02_tc013_1}    ues_index=${A_B02_TC013}[ues_index]
    UEs Start UL Data Transfer    ues_index=${A_B02_TC013}[ues_index]    ul_throughput=${A_B02_TC013}[ues_ul_throughput]
    UEs Check Throughput    tput_target=${A_B02_TC013}[ues_ul_tput_target]    ues_index=${A_B02_TC013}[ues_index]    direction=ul
    collect tti logs during adjust pa values
    ...    names=${l2stream3_ttitrace_B_02_tc013_1}
    ...    nr_phy_cell_ids=${A_B02_TC013}[tti_nr_phy_cell_ids]
    ...    start_value=${A_B02_TC013}[start_value]
    ...    end_value=${A_B02_TC013}[end_value]
    ...    step=${A_B02_TC013}[step]
    ...    index=${A_B02_TC013}[index]
    ...    pa_interval_time=${A_B02_TC013}[pa_interval_time]
    ...    direction=increase
    ...    target_dir=${A_B02_TC013}[log_path]
    collect tti logs during adjust pa values
    ...    names=${l2stream3_ttitrace_B_02_tc013_2}
    ...    nr_phy_cell_ids=${A_B02_TC013}[tti_nr_phy_cell_ids]
    ...    start_value=${A_B02_TC013}[end_value]
    ...    end_value=${A_B02_TC013}[start_value]
    ...    step=${A_B02_TC013}[step]
    ...    index=${A_B02_TC013}[index]
    ...    pa_interval_time=${A_B02_TC013}[pa_interval_time]
    ...    direction=decrease
    ...    target_dir=${A_B02_TC013}[log_path]
    get values to check
    ...    names=${l2stream3_ttitrace_B_02_tc013_1}
    ...    fields=${${"ulFdSchedData.dciFormat"},${"ulFdSchedData.puschTPstate"}}
    get values to check
    ...    names=${l2stream3_ttitrace_B_02_tc013_2}
    ...    fields=${${"ulFdSchedData.dciFormat"},${"ulFdSchedData.puschTPstate"}}
    [Teardown]    Run Keywords
    ...    Run keyword if    '${TEST STATUS}' == 'FAIL'    Run keyword and continue on failure    get gnb snapshot
    ...    AND    UEs Stop UL Data Transfer    ues_index=${A_B02_TC013}[ues_index]
    ...    AND    UEs Detach    ues_index=${A_B02_TC013}[ues_index]
    ...    AND    client.stoplog      service=pioneer
    ...    AND    paras change on BTS
    ...    paras=${PARAMETERS_RECOVER_CB008148_A_B02_TC013}
    ...    delta_file_name=${epc_log_path}${PARAMETERS_RECOVER_CB008148_A_B02_TC013_JSON_FILE}
    ...    AND    get and check operationalState of required cells
    ...    cells=${CB008148_A_B02_TC013_CELLS}
    ...    states=${CB008148_A_B02_TC013_CELLS_STATUS}[0]
    ...    AND    Wait until keyword succeeds    2m    10s
    ...    get and check operationalState of required cells
    ...    cells=${CB008148_A_B02_TC013_CELLS}    states=${CB008148_A_B02_TC013_CELLS_STATUS}[1]
    ...    AND    Stop capture syslog via btslog on ute
    ...    AND    syslog analysis via regex file
    ...    AND    Common Test Teardown for CB014044 without AP


*** Keywords ***
Capture tcpdump during ue attach
    [Arguments]    ${filename}    ${ues_index}
    Start capture gNB log on master    filename=${filename}
    multi_ues_attach_and_verify    ues_index=${ues_index}
    [Teardown]    Stop and download the Logs    filename=${filename}

collect tti logs during adjust pa values
    [Arguments]
    ...    ${names}
    ...    ${nr_phy_cell_ids}
    ...    ${start_value}
    ...    ${end_value}
    ...    ${step}
    ...    ${index}
    ...    ${pa_interval_time}
    ...    ${direction}
    ...    ${target_dir}
    Start Ttitrace With Admin Mode
    ...    names=${names}
    ...    nr_phy_cell_ids=${nr_phy_cell_ids}
    Set the attenuation value of ports simultaneously step by step
    ...    start_value=${start_value}
    ...    end_value=${end_value}
    ...    step=${step}
    ...    index=${index}
    ...    pa_interval_time=${pa_interval_time}
    ...    direction=${direction}
    [Teardown]    Stop Ttitrace With Admin Mode
    ...    names=${names}
    ...    target_dir=${target_dir}

get values to check
    [Arguments]
    ...    ${names}
    ...    ${fields}=${${"ulFdSchedData.dciFormat"},${"ulFdSchedData.puschTPstate"}}
    ${fileds_values}=    get_field_values
    ...    csv_file=${names}
    ...    fields=${fields}
    ${dciFormat_list}=    Create List
    ${puschTPstate_list}=    Create List
    FOR    ${filed_value}    IN    @{fileds_values}
        Comment    check ulFdSchedData.dciFormat and ulFdSchedData.puschTPstate
        Append To List    ${dciFormat_list}    ${filed_value}[ulFdSchedData.dciFormat]
        Append To List    ${puschTPstate_list}    ${filed_value}[ulFdSchedData.puschTPstate]
#        Should Be Equal    ${filed_value}[ulFdSchedData.dciFormat]    UL_00_FORCE
#        Should Be Equal    ${filed_value}[ulFdSchedData.puschTPstate]    disabled
    END
    Should Contain    ${dciFormat_list}    UL_00_FORCE
    Should Contain    ${puschTPstate_list}    disabled

Capture tcpdump during loop ho
    [Arguments]
    ...    ${filename}
    ...    ${start_value}
    ...    ${end_value}
    ...    ${step}
    ...    ${index}
    ...    ${pa_interval_time}
    ...    ${ho_times}
    Start capture gNB log on master    filename=${filename}
    FOR    ${t}    IN RANGE    ${ho_times}
        Set the attenuation value of ports simultaneously by step for loop ho
        ...    start_value=${start_value}
        ...    end_value=${end_value}
        ...    step=${step}
        ...    index=${index}
        ...    pa_interval_time=${pa_interval_time}
    END
    [Teardown]    Stop and download the Logs    filename=${filename}

Capture tcpdump during loop Reestablish
    [Arguments]
    ...    ${filename}
    ...    ${source_initial_value}
    ...    ${target_initial_value}
    ...    ${source_index}
    ...    ${target_index}
    ...    ${pa_interval_time}
    ...    ${Reestablish_times}
    Start capture gNB log on master    filename=${filename}
    FOR    ${t}    IN RANGE    ${Reestablish_times}
        Set the attenuation value of ports simultaneously by step for loop Reestablish
        ...    source_initial_value=${source_initial_value}
        ...    target_initial_value=${target_initial_value}
        ...    source_index=${source_index}
        ...    target_index=${target_index}
        ...    pa_interval_time=${pa_interval_time}
    END
    [Teardown]    Stop and download the Logs    filename=${filename}
