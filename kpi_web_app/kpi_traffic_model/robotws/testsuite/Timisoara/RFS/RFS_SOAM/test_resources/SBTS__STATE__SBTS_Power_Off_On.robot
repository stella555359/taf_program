*** Settings ***
Documentation    TC__SBTS__STATE__SBTS_Power_Off_On
Variables    tc_variables/sbts__state__sbts_power_off_on_alarms_definitions.py
Resource    ../../resources/rfs_frame_rfs_soam_taf.robot

*** Variables ***
${REPEAT_COUNTER}               3    # Number of SBTS BTS and RM power OFF/ON operations, default value 3
${Objects_To_Power_Off}         SM   # Objects to power off; possible values: SM (indicates that all SMs will be powered off/on) or
                                     # SM_RM (indicates that all SMs and all RMs will be powered off/on); default SM
${SBTS_POWER_ON_WRN_THR}        600  # If SBTS Reset exceeds SBTS_POWER_ON_WRN_THR, test verdict failed and snapshot at the end of the test
${SBTS_POWER_ON_MAX_WAIT_TIME}  900  # Maximum time for wait of LTE BTS to be OnAir (all cells up after reset).
${SWCONFIG_CHANGE_FLAG}  False  # Enable/disable HWF flags in swconfig.txt file. By default HWF flags change is disabled: False
${SWCONFIG_FLAG_ACTION}  add    # Action that should be done with the list of HWF flags in swconfig.txt. Possible values: add/remove
                                # - add: check requested HWF flags from swconfig.txt file and set if needed on 0 -> HWF will not be took into use
                                # - remove: check requested HWF flags from swconfig.txt file and remove if set on 0 -> HWF will be took into use
${SWCONFIG_FLAG_LIST}  0x4F0214  # List of HWF flags that will be added/removed in swconfig.txt. User provides the flags with spaces between them.
                                 # Possible values:
                                 # - 0x190030 (OAM_DBG_EnableHwfLoading) till SBTS00_ENB_9999_211214_000014 or on maintenance branches till SBTS22R1
                                 # - 0x4F0214 (ERadLteHas_BB_PERIPHERIES_EnableHwfLoading) from SBTS00_ENB_9999_211214_000014
                                 # For current SW trunk, flag 0x4F0214 should be used
*** Keywords ***
TC__SBTS__STATE__SBTS_Power_Off_On
     [Documentation]
    ...  [CASE LINK]: https://jiradc.ext.net.nokia.com/browse/TAT-21884
    ...
    ...  *****************
    ...  Basic information
    ...  *****************
    ...  SBTS test case for SBTS power OFF/ON operations, - x times sequence.
    ...  x - value of REPEAT_COUNTER parameter (default: 3)
    ...  The main steps performed for the test are:
    ...  - check initial SBTS state and alarms
    ...  - get RM list and associated info
    ...  - Power off SBTS site from PDU accroding to input parameter Objects_To_Power_Off_On
    ...  Either all SMs or all SMs and all RMs
    ...  - Power on SBTS site from PDU accroding to input parameter Objects_To_Power_Off_On
    ...  - check BTS reset behavior from ims file: reset number is 1
    ...  - check final BTS state and alarms
    ...  Pass criteria: SBTS power OFF/ON operations work as expected; states and alarms are as expected
    ...
    ...  ******************
    ...  History of changes
    ...  ******************
    ...  - 02.12.2021 - https://jiradc.ext.net.nokia.com/browse/TAT-21884 - [5G] [RFSplit] RFS_SBTS_RF_Split_SBTS_Power_OFF_ON
    ...  - 23.02.2022 - https://jiradc.ext.net.nokia.com/browse/TAT-22650 - [Cloud] [RFSplit] [Legacy] Particular teardown refactoring - SBTS part
    ...  - 22.03.2022 - https://jiradc.ext.net.nokia.com/browse/TAT-22800
    ...  - [5G][RFSplit]SBTS__STATE__BBMOD_LockUnlock_from_WEBEM fails due to IOT cells
    ...  - 17.05.2022 - https://jiradc.ext.net.nokia.com/browse/TAT-23098 - [5G][NR-SBTS] remove WCDMA cell administrativeState check in:
    ...  NR_SBTS__STATE__NR_RM_LockUnlock_Cell_BlockUnblock_from_WEBEM and other scenarios
    ...  - 02.01.2023 - https://jiradc.ext.net.nokia.com/browse/TAT-24519 -
    ...  [5G] Update scenarios to take reset number from ims2 power off/on tests - SBTS - with TAT-24518
    ...  - 03.01.2023 - https://jiradc.ext.net.nokia.com/browse/TAT-24518
    ...  [5G] KPI3: Adapt scenario to measure KPI#3 via ims2, when first cell goes UP - SBTS - with TAT-24519
    ...  - 19.06.2023 - https://jiradc.ext.net.nokia.com/browse/TAT-25546 - [5G][TC review] Possibility to perform power off/on for both Cores
    ...  (Dual Core BTS) for SBTS__STATE__SBTS_Power_Off_On
    ...  - 14.05.2024 - https://jiradc.ext.net.nokia.com/browse/TAT-27410 - [5G] [Infomodel] - P1 - Eliminate usage of KW Infomodel "Get baseband
    ...  pool allocation mode info" in test-cases - after TAT-27401
    ...  - 25.07.2024 - https://jiradc.ext.net.nokia.com/browse/TAT-27680 - [5G] SBTS__STATE__SBTS_Power_off_on
    ...  Reset message it's not detected as it should and test fails
    ...  - 13.08.2025 - https://jiradc.ext.net.nokia.com/browse/TAT-29672 - Add option for HWF for NRL__STATE__NR_SM_Power_Off_On - 27.08
    ...  - 03.09.2025 - https://jiradc.ext.net.nokia.com/browse/TAT-29815 -
    ...  Unify alarm container names between all tests in order to use ${${alias.upper()}}_ALARMS_CNI_127210 ${${alias.upper()}}_ALARMS_NO_CNI_127210
    ...
    ...  *******************
    ...  Test case flowchart
    ...  *******************
    ...  .. image:: https://gitlabe1.ext.net.nokia.com/panda-docs/hran_doc/-/blob/master/testsuite/RFS_SOAM/
    ...  TAT-21884_SBTS__STATE__SBTS_Power_Off_On.png

    Set Tags    CA-STATE    OWNER-sorin.saulescu@nokia.com    AUTHOR-florin.oprea@nokia.com    PHASE-QT    SW-SBTS22R1

    Configure Hardware File
    Step 1: Check initial BTS state
    Step 2: Check initial BTS alarms
    Step 3: Get initial baseband pool allocation mode info
    Step 4: Get RM list and info
    Step 5: Check PDU definition and reachability
    FOR  ${INDEX}  IN RANGE  1  ${REPEAT_COUNTER}+1
        Log  ==============================================================================  console=True
        Log  Start Cycle ${INDEX} of ${REPEAT_COUNTER}  console=True
        Log  ==============================================================================  console=True
        Step 6: Power Off SBTS
        Run Keyword If  '${Objects_To_Power_Off}' == 'SM_RM'
        ...  Step 7: Power OFF/ON RM
        ...  ELSE  Log  **** RM power OFF/ON option not selected by user. Proceed to power ON SBTS step ****  console=true
        Step 8: Power On SBTS
        Step 9: Check final number and state of Cells and RMs
        Step 10: Check BTS reset behavior
        Step 11: Get and check KPI3 info from IMS file for iteration ${INDEX}
    END
    Step 12: Check final BTS state
    Step 13: Check final BTS alarms

    [Teardown]  Particular Teardown

Configure Hardware File
    Return From Keyword If  '${SWCONFIG_CHANGE_FLAG}' == 'False'
    Set HWF Flags  swconfig_flag_action=${SWCONFIG_FLAG_ACTION}  swconfig_flag_list=${SWCONFIG_FLAG_LIST}  alias=${alias_local}

Step ${index}: Check ${when} BTS state
    [Documentation]
    ...  BTS state is checked according to Admin

    [Timeout]  15 min
    Log  Step ${index}: Check ${when} BTS state  console=True
    Admin Check BTS RAT Procedural State  alias=${alias_local}  timeout=600
    Admin Check BTS Procedural and Blocking states  ${OnAir_}  ${Unblocked_}  600  ${alias_local}
    Log  BTS site - proceduralState: OnAir, blockingState: Unblocked  console=True

Step ${index}: Check ${when} BTS alarms
    [Documentation]
    ...  BTS alarms are compared with values from expected, ignored and critical alarms lists. BTS alarms are get from Admin

    [Timeout]  15 min
    Log  Step ${index}: Check ${when} BTS alarms  console=True
    Get and Check Alarms SOAM  alias=${alias_local}  expected_alarms=@{EMPTY}  ignored_alarms=${${alias_local.upper()}_IGNORED_ALARMS}
    ...  critical_alarms=${${alias_local.upper()}_CRITICAL_ALARMS}
    Log  BTS site - expected, ignored and critical alarms checked  console=True

Step ${index}: Get initial baseband pool allocation mode info
    [Documentation]
    ...  Get initial baseband pool allocation mode info

    Log  Step ${index}: Get initial baseband pool allocation mode info   console=True
    Get baseband pool allocation mode info from SCF  alias=${alias_local}

Step ${index}: Get RM list and info
    [Documentation]
    ...  RM list is get from Admin

    [Timeout]  5 min
    Log  Step ${index}: Get RM list and info  console=True
    ${RM_list}=  Get Ids For All  class_name=RMOD  connection=${alias_local}
    ${SM_list}=  Get Ids For All  class_name=SMOD  connection=${alias_local}
    Sort List  ${RM_list}
    ${RM_ID_SN_dict}=  Get RM ID SN dict  ${RM_list}
    Set Test Variable  ${RM_ID_SN_dict}
    Run Keyword If  ${RM_list}
    ...  Log  BTS RM info:  console=True
    ...  ELSE
    ...  Fail  No BTS RM available in runtime view!
    FOR  ${item}  IN  @{RM_list}
        ${RM_SN}=  Get From Dictionary  ${RM_ID_SN_dict}  ${item}
        Log  - RM ID ${item}: SN ${RM_SN}  console=True
    END
    Set Test Variable  ${RM_list}
    ${RM_count}=  Get Length  ${RM_list}
    Set Test Variable  ${RM_count}

    ${RM_CELL_dict}=  Get RM CELL mapping info dict  ${RM_list}
    Set Test Variable  ${RM_CELL_dict}

    ${NR_CELL_list}=  Get Ids For All  class_name=NRCEL  connection=${alias_local}
    ${LTE_CELL_list}  ${LTE_CELL_IOT_list}=  Admin Get LTE CELL Ids list  ${alias_local}
    ${WCDMA_CELL_list}=  Get Ids For All  class_name=WNCEL  connection=${alias_local}
    ${GSM_CELL_list}=  Get Ids For All  class_name=GNCEL  connection=${alias_local}
    ${CELL_list}=  Combine Lists   ${NR_CELL_list}  ${LTE_CELL_list}  ${WCDMA_CELL_list}  ${GSM_CELL_list}
    Set Test Variable  ${NR_CELL_list}
    Set Test Variable  ${LTE_CELL_list}
    Set Test Variable  ${WCDMA_CELL_list}
    Set Test Variable  ${GSM_CELL_list}
    Set Test Variable  ${CELL_list}
    ${CELL_count}=  Get Length  ${CELL_list}
    Set Test Variable  ${CELL_count}

Step ${index}: Check PDU definition and reachability
    [Documentation]
    ...  Check if PDU for RM and BTS SMs are defined, can be reached and their status is on

    Log  Step ${index}: Check RM PDU definition and reachability  console=True
    FOR  ${item}  IN  @{RM_list}
        ${RM_SN}=  Get From Dictionary  ${RM_ID_SN_dict}  ${item}
        Check PDU port status  RMOD_${RM_SN}  on
    END
    Log  Step ${index}: Check BTS SMs PDU definition and reachability  console=True
    ${BTS_SM_PDU_if_name_list}=  Check BTS SMs PDU info definition  ${alias_local}
    Set Test Variable  ${BTS_SM_PDU_if_name_list}
    ${status}=  Check BTS SMs PDU port status  ${BTS_SM_PDU_if_name_list}  on
    Run Keyword If  ${status}
    ...  Log  BTS SMs PDU port status as expected  console=True
    ...  ELSE  Run Keywords
    ...  Log  PDU for BTS SMs is either not reachable or not switched on!  level=ERROR
    ...  AND  Fail  PDU for BTS SMs is either not reachable or not switched on!

Step ${index}: Power OFF/ON RM
    Log  Step ${index}: Performing Power OFF/ON RFM steps in sequence  console=True
    Power OFF all RM
    Sleep  10s
    Power ON all RM
    Sleep  10s

Power OFF all RM
    Log  ***** Power OFF all RM *****  console=True
    FOR  ${item}  IN  @{RM_list}
        Perform power OFF RM  ${item}
    END

Power ON all RM
    Log  ***** Power ON all RM *****  console=True
    FOR  ${item}  IN  @{RM_list}
        Perform power ON RM  ${item}
    END

Step ${index}: Power ${action} SBTS
    Log  Step ${index}: ***** Power ${action} SBTS *****  console=True

    ${action_performed}=  Convert To Lowercase  ${action}
    ${status}=  Set BTS SMs PDU port status  ${BTS_SM_PDU_if_name_list}  ${action_performed}
    Get Current Date UTC info  start_reset_number

    Run Keyword If  ${status}
    ...  Log  BTS SMs PDU port status ${action_performed}, as expected  console=True
    ...  ELSE  Run Keywords
    ...  Log  Set BTS SMs PDU port status ${action_performed} failed!  level=ERROR
    ...  AND  Fail  Set BTS SMs PDU port status ${action_performed} failed!

    Run Keyword If  '${action}' == 'On'  Run Keywords
    ...  Get Current Date UTC info  start
    ...  AND  Log  Wait for SM to recover after power ON!!  console=True
    ...  AND  Check elapsed time after power on

Check elapsed time after power on
    Wait For Target To Be Reachable TAF  hostname=${${alias_local.upper()}}[${alias_local.upper()}_TECH_IP_ADDRESS]  timeout=180
    Sleep  120 sec
    Get Current Date UTC info  intermediate
    ${elapsed_time}=  DateTime.Subtract Date from Date  ${date_timestamp_intermediate_UTC}  ${date_timestamp_start_UTC}  number
    ${remained_time}=  BuiltIn.Evaluate  ${SBTS_POWER_ON_MAX_WAIT_TIME} - ${elapsed_time}
    ${CELL_state_enabled_check}=  Set Variable  operationalState=${Enabled_}, blockingState=${Unblocked_}
    Admin Check all BTS cells expected states  ${CELL_state_enabled_check}  ${alias_local}  ${remained_time}

Step ${index}: Check BTS reset behavior
    [Documentation]
    ...  Final RESET info are compared with initial RESET info.
    ...  Reset behavior as expected if: reset number is 1
    ...  Otherwise, reset behavior not as expected, then errors are added to report and failed.

    Log  Step ${index}: Check BTS reset behavior  console=True
    Get and check BTS RESET info from IMS file  expected_reset_number=1  alias=${alias_local}  remove_ims_file=False
    ...  start_point_timestamp_UTC=${date_timestamp_start_reset_number_UTC}  end_point_timestamp_UTC=${date_timestamp_end_UTC}

Step ${index}: Check final number and state of Cells and RMs
    [Documentation]
    ...  Following checks are performed:
    ...  - number of configured cells and radio modules in SCF are properly mapped on BTS running view ADMIN
    ...  - check cells states
    ...  - check radio modules states

    Log  Step ${index}: Check final number and state of Cells and RMs  console=True
    RFS Test Case Final Checks
    Get Current Date UTC info  end

Get RM ID SN dict
    [Arguments]   ${RM_list}
    ${RM_ID_SN_dict}=  Create Dictionary
    FOR  ${item}  IN  @{RM_list}
        ${RM_param}=  Get Parameters For  class_name=RMOD  id_num=${item}  connection=${alias_local}
        Set To Dictionary  ${RM_ID_SN_dict}  ${RM_param['id']}  ${RM_param['serialNumber']}
    END
    [Return]  ${RM_ID_SN_dict}

Get RM CELL mapping info dict
    [Arguments]   ${RM_list}
    ${RM_CELL_dict}=  Create Dictionary
    FOR  ${item}  IN  @{RM_list}
        ${CELL_list}=  Get Cell Mapping By Module Id  module_id=${item}  connection=${alias_local}
        Sort List  ${CELL_list}
        Set To Dictionary  ${RM_CELL_dict}  ${item}  ${CELL_list}
    END
    [Return]  ${RM_CELL_dict}

Perform power OFF RM
    [Arguments]  ${RM_ID}
    ${RM_SN}=  Get From Dictionary  ${RM_ID_SN_dict}  ${RM_ID}

    Log  Perform power OFF RM ${RM_ID} with SN ${RM_SN}:  console=True
    Pdu BTS Interface Off  RMOD_${RM_SN}
    Check PDU port status  RMOD_${RM_SN}  off
    Sleep  5s

Perform power ON RM
    [Arguments]  ${RM_ID}
    ${RM_SN}=  Get From Dictionary  ${RM_ID_SN_dict}  ${RM_ID}

    Log  Perform power ON RM ${RM_ID} with SN ${RM_SN}:  console=True
    Pdu BTS Interface On  RMOD_${RM_SN}
    Check PDU port status  RMOD_${RM_SN}  on
    Sleep  5s

Check Cell State
    [Arguments]   ${cell_class_name}  ${cell_list}  ${cell_state_check}  ${cell_state}  ${timeout}  ${alias}
    FOR  ${item}  IN  @{cell_list}
        Assert  class_name=${cell_class_name}  id=${item}  parameters=${cell_state_check}  timeout=${timeout}  connection=${alias_local}
        Log  ${alias} ${cell_class_name} ${item} status:\n - ${cell_state}  console=True
    END

Check PDU port status
    [Arguments]  ${item}  ${status}
    ${PDU_port_status}=  Pdu BTS Interface Get Status  ${item}
    Run Keyword if  '${PDU_port_status}' == '${status}'
    ...  Log  ${item} outlet ${INTERFACES['${item}']['OUTLET']} on ${INTERFACES['${item}']['IP']} switched ${PDU_port_status}  console=True
    ...  ELSE  Run Keywords
    ...  Log  ${item} outlet ${INTERFACES['${item}']['OUTLET']} on ${INTERFACES['${item}']['IP']} not switched ${PDU_port_status}!  level=ERROR
    ...  AND  Fail  ${item} outlet ${INTERFACES['${item}']['OUTLET']} on ${INTERFACES['${item}']['IP']} not switched ${PDU_port_status}!

Check if all PDU port status is on
    FOR  ${item}  IN  @{RM_list}
        ${RM_SN}=  Get From Dictionary  ${RM_ID_SN_dict}  ${item}
        Run Keyword and Ignore Error  Check if PDU port status is on  RMOD_${RM_SN}  120
    END
    Recover BTS SMs PDU port status  ${BTS_SM_PDU_if_name_list}  on  ${alias_local}

Step ${index}: Get and check KPI3 info from IMS file for iteration ${CYCLE}
    [Documentation]
    ...  Get and check KPI3 info from IMS file.

    Log  Step ${index}: Get and check KPI3 info from IMS file for iteration ${CYCLE}  console=True
    ${kpi_name_delta_dict}=  Get and check KPI info from IMS file
    ...  kpi_names=kpi3  kpi_thresholds=${SBTS_POWER_ON_WRN_THR}  alias=${alias_local}  start_point_timestamp_UTC=${date_timestamp_start_UTC}
    ...  end_point_timestamp_UTC=${date_timestamp_end_UTC}
    ${kpi_delta_list}=  Get From Dictionary  ${kpi_name_delta_dict}  kpi3

    Export KPI Results to File  alias=${alias_local}  obj=BTS  obj_type=SBTS  obj_id=${alias_local}  action_1=BTS_Power_On  kpi_reported_1=KPI_3
    ...  event_value_1=${kpi_delta_list[0]}  cycle=${CYCLE}  source_info=ims

Hardware File Teardown
    Return From Keyword If  '${SWCONFIG_CHANGE_FLAG}' == 'False'
    Recover HWF Flags  alias=${alias_local}


Particular Teardown
    Run Keyword And Continue On Failure  Check if all PDU port status is on
    Export KPI results to File Global  kpi_log_file_name=KpiTimeInfo
    Hardware File Teardown

TC Setup
    ${tech_preset_list}=  Create List  SBTS
    Common Test Setup  preset_techs=${tech_preset_list}  common_sbts=${TRUE}  infomodelSetup=${FALSE}

TC Teardown
    Common Test Teardown
