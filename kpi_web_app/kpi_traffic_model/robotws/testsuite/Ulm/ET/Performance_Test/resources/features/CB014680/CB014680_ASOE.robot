*** Settings ***
Documentation
...  CB014680 Testcases

Resource   ../../performance_keywords.robot
Resource   ../../performance_multivm.robot

Suite Setup       Suite Setup for Performance Test
Suite Teardown    Suite Teardown for Performance Test
Test Setup        performance_multivm.Test case setup for Performance Test MultiVM
Test Teardown     performance_multivm.Test case Teardown for Performance Test MultiVM


*** Variables ***
${EGATE_FILES_DIR}    ${PERF_RESOURCES_DIR}/features/CB014680/egate/asoe/


*** Test Cases ***
CB014680_TC1
    [Setup]    performance_multivm.Test Case Setup For Performance Test MultiVM
    ...                                                              ENABLE_ACT_BSR=auto
    ...                                                 SCF_SET_reportingIntervalPm=5min
    ...                                                SCF_SET_VAR_NRPMRNL_miNrRSUP=5min

    ${args_str}    Catenate
    ...    {
    ...        "start_cell": 1,
    ...        "end_cell": 12,
    ...        "egate_script_delay_per_vm": "1s",
    ...        "expect_ue_count": "40,40,5,0,0,0,0,0,0,0,0,0",
    ...        "egate_files_dir": "${EGATE_FILES_DIR}",
    ...        "cfg_sim_files": [
    ...           [1, "CNI-138433_CA_Sector1_SA_PETSE_AP1.lua", "run_configuration()"],
    ...           [2, "CNI-138433_CA_Sector2_SA_PETSE_AP2.lua", "run_configuration()"],
    ...           [3, "CNI-138433_CA_Sector3_SA_PETSE_AP3.lua", "run_configuration()"]
    ...        ],
    ...        "wts_manager_args": [
    ...           [1, "/opt/iphy/latest/basic_attach.json", "--start 1 --end 40"],
    ...           [2, "/opt/iphy/latest/basic_attach.json", "--start 1 --end 40"],
    ...           [3, "/opt/iphy/latest/basic_attach.json", "--start 1 --end 5"]
    ...        ],
    ...        "wts_manager_async": false
    ...    }
    &{args_json}    Evaluate    json.loads('''${args_str}''')    modules=json
    &{args}    performance_keywords.Prepare WTS Manager Args    &{args_json}

    performance_multivm.Run MultiVM WTS Manager Testcase    ${args}


CB014680_TC5
    [Setup]    performance_multivm.Test Case Setup For Performance Test MultiVM
    ...                                                     ENABLE_ONLINE_REPORTING=true
    ...                                                              ENABLE_ACT_BSR=auto
    ...                                                 SCF_SET_reportingIntervalPm=5min
    ...                                                SCF_SET_VAR_NRPMRNL_miNrRSUP=5min

    ${QC_TEST_NAME}    Catenate     SEPARATOR=    [1] CB014680_B_TC05_B2_Verification_of_FD_scheduler_time_reservation_
    ...                                           changes_within_preventive_OLC_in_scheduler_performance_in_FR1
    Set Test Variable    ${QC_TEST_NAME}
    Set Test Variable    ${QC_PATH}         testsuite/Ulm/ET/Performance_Test/resources/qc/CB014680.qc

    ${args_str}    Catenate
    ...    {
    ...        "start_cell": 1,
    ...        "end_cell": 12,
    ...        "egate_script_delay_per_vm": "1s",
    ...        "expect_ue_count": "40,40,5,100,100,5,0,0,0,0,0,0",
    ...        "egate_files_dir": "${EGATE_FILES_DIR}",
    ...        "cfg_sim_files": [
    ...           [1, "CNI-138433_CA_Sector1_SA_PETSE_AP1.lua", "run_configuration()"],
    ...           [2, "CNI-138433_CA_Sector2_SA_PETSE_AP2.lua", "run_configuration()"],
    ...           [3, "CNI-138433_CA_Sector3_SA_PETSE_AP3.lua", "run_configuration()"]
    ...        ],
    ...        "wts_manager_args": [
    ...           [1, "/opt/iphy/latest/basic_attach_CB014680_B_TC05_cell1.json", "--start 1 --end 40"],
    ...           [1, "/opt/iphy/latest/basic_attach_CB014680_B_TC05_cell4.json", "--start 3591 --end 3690"],
    ...           [2, "/opt/iphy/latest/basic_attach_CB014680_B_TC05_cell2.json", "--start 1 --end 40"],
    ...           [2, "/opt/iphy/latest/basic_attach_CB014680_B_TC05_cell6.json", "--start 3401 --end 3405"],
    ...           [3, "/opt/iphy/latest/basic_attach_CB014680_B_TC05_cell3.json", "--start 1 --end 5"],
    ...           [3, "/opt/iphy/latest/basic_attach_CB014680_B_TC05_cell5.json", "--start 3591 --end 3690"]
    ...        ],
    ...        "wts_manager_async": false
    ...    }
    &{args_json}    Evaluate    json.loads('''${args_str}''')    modules=json
    &{args}    performance_keywords.Prepare WTS Manager Args    &{args_json}

    performance_multivm.Run MultiVM WTS Manager Testcase    ${args}

    ${total_ue_count}    performance_keywords.Get Total Expected UE Count    ${args}
    Run Keyword And Continue On Failure     performance_multivm.Wait Until Expected UE Count Reached
    ...    ${args}
    ...    ${total_ue_count}
    ...    expected_ue_count_per_cell=${args.expect_ue_count}
    Run Keyword And Continue On Failure     performance_multivm.Collect Traffic Logs    ${args}
    #ToDo: R&D counters verification