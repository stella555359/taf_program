*** Settings ***
Documentation
...    author: Rafal Kawa
...    contact: rafal.kawa@nokia.com
...    description: CRT test suite of feature CB009250

Resource    taf/rfrl/ue/robot/REAL_UE.robot
Resource    taf/rfrl/procedures/resources/robot/common_setups_and_teardowns.robot
Resource    taf/rfrl/procedures/resources/robot/Alarms.robot
#Resource    taf/rfrl/procedures/SISO/General_SiSo_HWPTA_Collect_RFSW_Logs_From_RU_Into_BTS_Snapshot.robot

Variables   taf/rfrl/procedures/resources/python/common_allowed_alarms.py
Variables   resources/deltas.py
Variables   resources/variables.py

Suite Setup       Common Suite Setup With OnAir Test Line Preparation
...                       increase_timeout_for_update_sw=${1800}
...                       list_of_additional_allowed_alarms=${CUSTOM_ALLOWED_ALARMS_DURING_TL_PREPARATION}
...                       swconfig_from_path=${SWCONFIG_PATH}
Suite Teardown    Common Suite Teardown

Test Setup        Common Preconditions With Watching Alarms
Test Teardown     Common Postconditions With Watching Alarms

*** Variables ***
${CUSTOM_ALLOWED_ALARMS_DURING_TL_PREPARATION}  ${None}
${SWCONFIG_PATH}                                commissionings/Krakow/swconfig/default_swconfig.txt

#*** Test Cases ***
#CB009250_General_SiSo_Collect_RFSW_logs_from_RU_into_BTS_Snapshot
#    [Setup]   Run Keywords
#    ...       Common Preconditions
#    ...       AND  Set Test Variable    ${logs_path}    ${LOG_PATH}
#    ...       AND  Start alarms watchdog    on_enb=${False}
#    General_SiSo_HWPTA_Collect_RFSW_Logs_From_RU_Into_BTS_Snapshot
#    ...    documentation_path=${CURDIR}/resources/custom_trbl_log_list.csv
#    [Teardown]  Run Keywords
#    ...         Check alarms and stop watchdog    on_enb=${False}    reset_allowed_alarms_gnb=${False}
#    ...         AND  Common Postconditions
