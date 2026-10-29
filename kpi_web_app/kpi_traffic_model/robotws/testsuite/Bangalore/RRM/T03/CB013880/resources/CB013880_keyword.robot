*** Settings ***

Documentation   :copyright: Nokia
...             :authors: Priya Bakshi
...             :contact: Priya.Bakshi@nokia.com
...             TEST SET NAME:    CB013880
...             TESTING SPLIT:    Refer CB013880 Test Plan
...             CONTACTS:         I_MN_RAN_L2_5G_BLR_ET_ALL_GMS <I_MN_RAN_L2_5G_BLR_ET_ALL@internal.nsn.com>
...             REFERENCES:       CB013880_CFAM



Library        ute_wtssim
Library        ta5g_commissioning
Library        ute_fsmaccess
Library        Telnet
Library        ta5g_file_system
Library        ta5g_enb
Library        ta5g_iphy
Library        ta5g_testline_management


*** Variables ***
@{REMOTE_HOSTS}


*** Keywords ***

perform delta and add 3rd slice
   CoamAdmin.Setup Admin     bts_host=${BTS_ADDRESS}    bts_port=${BTS_PORT}    use_ssl=${USE_SSL}    name=a8
    CoamAdmin.perform_delta_recommissioning    delta_file=${delta_add_slice3}    skip_parameter_relation_errors=True
    ...      connection=a8
    CoamAdmin.Teardown admin      connection=a8

perform delta and delete 3rd slice
   CoamAdmin.Setup Admin     bts_host=${BTS_ADDRESS}    bts_port=${BTS_PORT}    use_ssl=${USE_SSL}    name=a9
    CoamAdmin.perform_delta_recommissioning    delta_file=${delta_delete_slice3}    skip_parameter_relation_errors=True
    ...      connection=a9
    CoamAdmin.Teardown admin      connection=a9

Disable feature
    CoamAdmin.Setup Admin     bts_host=${BTS_ADDRESS}    bts_port=${BTS_PORT}    use_ssl=${USE_SSL}    name=a5
    CoamAdmin.perform_delta_recommissioning    delta_file=${delta_configuration_decommission}    skip_parameter_relation_errors=True
    ...      connection=a5
    CoamAdmin.Teardown admin      connection=a5

Enable feature
    CoamAdmin.Setup Admin    bts_host=${BTS_ADDRESS}    bts_port=${BTS_PORT}    use_ssl=${USE_SSL}    name=ABC
    CoamAdmin.perform_delta_recommissioning    delta_file=${delta_configuration_commission}    skip_parameter_relation_errors=True
    ...      connection=ABC
    CoamAdmin.Teardown admin      connection=ABC

Check If Alarm Disappeared_tc7
    [Documentation]    This keyword is used to check if alarm disappeared
    [Arguments]    ${fault_id}
    CoamAdmin.Setup Admin  bts_host=${BTS_ADDRESS}    bts_port=${BTS_PORT}    use_ssl=${USE_SSL}     name=a7     timeout=120
    @{alarms}=    CoamAdmin.Get Active Alarms     connection=a7    #both $ and @ are OK
    @{active_fault_list}=    Create List
    FOR    ${alarm}    IN    @{alarms}    # get list right, must @
         ${fault}=    Get From Dictionary    ${alarm}    faultId
         Append To List    ${active_fault_list}    ${fault}    #${fault} is a number,not a string
    END
    ${fault_id}=    Convert To Integer    ${fault_id}    #${fault_id} is a string,it must be changed to number
    List Should Not Contain Value    ${active_fault_list}    ${fault_id}
    [Teardown]    CoamAdmin.Teardown Admin         connection=a7

Check If Alarm Appeared for NRCELL5_tc9
    [Documentation]    This keyword is used to check if alarm appeared
    [Arguments]    ${fault_id}    ${configObjectName_id}
    CoamAdmin.Setup Admin    bts_host=${BTS_ADDRESS}    bts_port=${BTS_PORT}    use_ssl=${USE_SSL}    name=a6     timeout=120
    @{alarms}=    CoamAdmin.Get Active Alarms    connection=a6    #both $ and @ are OK
    @{active_fault_list}=    Create List
    FOR    ${alarm}    IN    @{alarms}    # get list right, must @
         ${fault}=    Get From Dictionary    ${alarm}    faultId
         Append To List    ${active_fault_list}    ${fault}    #${fault} is a number,not a string
    END
    ${fault_id}=    Convert To Integer    ${fault_id}    #${fault_id} is a string,it must be changed to number
    List Should Contain Value    ${active_fault_list}    ${fault_id}
    ${count}=    Count Values In List     ${active_fault_list}      ${fault_id}

     @{active_fault_list_1}=    Create List
    FOR    ${configObjectName}   IN    @{alarms}    # get list right, must @
         ${configObjectName}=    Get From Dictionary    ${configObjectName}    configObjectName

         Append To List    ${active_fault_list_1}   ${configObjectName}   #${fault} is a number,not a string
    END
     Get Matches   ${active_fault_list_1}    *${configObjectName_id}*
    [Teardown]    CoamAdmin.Teardown Admin     connection=a6

Check If Alarm Appeared for NRCELL6_tc9
    [Documentation]    This keyword is used to check if alarm appeared
    [Arguments]    ${fault_id}    ${configObjectName_id}
    CoamAdmin.Setup Admin    bts_host=${BTS_ADDRESS}    bts_port=${BTS_PORT}    use_ssl=${USE_SSL}    name=a10     timeout=120
    @{alarms}=    CoamAdmin.Get Active Alarms    connection=a10    #both $ and @ are OK
    @{active_fault_list}=    Create List
    FOR    ${alarm}    IN    @{alarms}    # get list right, must @
         ${fault}=    Get From Dictionary    ${alarm}    faultId
         Append To List    ${active_fault_list}    ${fault}    #${fault} is a number,not a string
    END
    ${fault_id}=    Convert To Integer    ${fault_id}    #${fault_id} is a string,it must be changed to number
    List Should Contain Value    ${active_fault_list}    ${fault_id}
    ${count}=    Count Values In List     ${active_fault_list}      ${fault_id}

     @{active_fault_list_1}=    Create List
    FOR    ${configObjectName}   IN    @{alarms}    # get list right, must @
         ${configObjectName}=    Get From Dictionary    ${configObjectName}    configObjectName

         Append To List    ${active_fault_list_1}   ${configObjectName}   #${fault} is a number,not a string
    END
     Get Matches   ${active_fault_list_1}    *${configObjectName_id}*
    [Teardown]    CoamAdmin.Teardown Admin     connection=a10

Check If Alarm Appeared for NRCELL6_tc7
    [Documentation]    This keyword is used to check if alarm appeared
    [Arguments]    ${fault_id}     ${configObjectName_id}
    CoamAdmin.Setup Admin    bts_host=${BTS_ADDRESS}    bts_port=${BTS_PORT}    use_ssl=${USE_SSL}    name=a6     timeout=120
    @{alarms}=    CoamAdmin.Get Active Alarms    connection=a6    #both $ and @ are OK
    @{active_fault_list}=    Create List
    FOR    ${alarm}    IN    @{alarms}    # get list right, must @
         ${fault}=    Get From Dictionary    ${alarm}    faultId
         Append To List    ${active_fault_list}    ${fault}    #${fault} is a number,not a string
    END
    ${fault_id}=    Convert To Integer    ${fault_id}    #${fault_id} is a string,it must be changed to number
    List Should Contain Value    ${active_fault_list}    ${fault_id}
    ${count}=    Count Values In List     ${active_fault_list}      ${fault_id}


     @{active_fault_list_1}=    Create List
    FOR    ${configObjectName}   IN    @{alarms}    # get list right, must @
         ${configObjectName}=    Get From Dictionary    ${configObjectName}    configObjectName

         Append To List    ${active_fault_list_1}   ${configObjectName}   #${fault} is a number,not a string
    END
     Get Matches   ${active_fault_list_1}    *${configObjectName_id}*
    [Teardown]    CoamAdmin.Teardown Admin     connection=a6


block cells
    CoamAdmin.Setup Admin     bts_host=${BTS_ADDRESS}    bts_port=${BTS_PORT}    use_ssl=${USE_SSL}     name=a2
    CoamAdmin.Setup Admin     bts_host=${BTS_ADDRESS}    bts_port=${BTS_PORT}    use_ssl=${USE_SSL}     name=a3
    CoamAdmin.Setup Admin     bts_host=${BTS_ADDRESS}    bts_port=${BTS_PORT}    use_ssl=${USE_SSL}     name=a4
    CoamAdmin.block_cell     dist_name=MRBTS-3/NRBTS-3/NRCELL-6   connection=a2
    CoamAdmin.block_cell     dist_name=MRBTS-3/NRBTS-3/NRCELL-7   connection=a3
    CoamAdmin.block_cell     dist_name=MRBTS-3/NRBTS-3/NRCELL-8   connection=a4
    CoamAdmin.teardown_all_aliases_for_admin


unblock cell-6
    CoamAdmin.Setup Admin      bts_host=${BTS_ADDRESS}    bts_port=${BTS_PORT}    use_ssl=${USE_SSL}    name=a1
    CoamAdmin.unblock_cell   dist_name=MRBTS-3/NRBTS-3/NRCELL-6    connection=a1
    CoamAdmin.Teardown admin      connection=a1

Initiate sgnb addition
    wtsrunner.ue_meas_cfg_disp    id=1
    sleep    2s
    wtsrunner.ue_measurement_send_nr    id=1    meas_id=1    event=A4    phycell_id=52    nrsrp_nr=80
    sleep    2s

detach_ue_with_power_off
    [Arguments]  ${ue_id}=1
    wtsrunner.ue_deregister   id=${ue_id}   ue_deregister_type=switch_off
    log to console  \nUE-${ue_id} Detached!


Register UE and start data traffic
         wtsrunner.ue_register    id=1
         sleep    2s
   	     wtsrunner.set_pdu_param    ue=1  pdu=1    trf_type=internal
   	     sleep    10s
         wtsrunner.ue_pdu_session_setup    pdu=1    ue=1    nwslice=1  gw=1
         sleep   2s
         wtsrunner.trf_data_start    ue=1    pdu=1    dir=dl    mbps=5
         wtsrunner.trf_data_start    ue=1    pdu=1    dir=ul    mbps=5
         sleep   5s


Check SIB messagges for all cells
      Sleep    10s
      ${file_content}=    OperatingSystem.Get File    /opt/iphy/latest/egate_console.log
      Should Contain    ${file_content}          eNB 2 cell 1: SystemInformationBlockType1-NR updated
      Should Contain    ${file_content}          eNB 2 cell 2: SystemInformationBlockType1-NR updated
      Should Contain    ${file_content}          eNB 2 cell 3: SystemInformationBlockType1-NR updated
      Should Contain    ${file_content}          eNB 2 cell 4: SystemInformationBlockType1-NR updated

Kill WTS processes Using WTS_Runner
    wtsrunner.kill_wtsemu_edaemon    edaemon_port=10000   connection=${WTS.Connection}    sudo_password=ute
    sleep      5s
    wtsrunner.kill_wtsemu_egate      egate_port=20000     connection=${WTS.Connection}    sudo_password=ute


Run cfg file
    [Arguments]    ${wts_cfg_file_TC1}
    Stop Edaemon and Egate process
    Stop Sim_enb
    Connect To WTS VM
    wtsrunner.configure_wtsemu_edaemon    edaemon_ssh_alias=${WTS.Connection}
    ...                                   directory_path=${WTS_DIR}
    ...                                   port=10000
    ...                                   sudo_password=ute
    wtsrunner.configure_wtsemu_egate      egate_ssh_alias=${WTS.Connection}
    ...                                   directory_path=${WTS_DIR}
    ...                                   port=20000
    wtsrunner.start_wtsemu                egate_console_ip=${WTS.Ip}
    ...                                   egate_port=20000

    wtsrunner.configure                   file=${wts_cfg_file_TC1}
    Sleep    90s
    wtsrunner.Gnb Param    id=3    xn_listening_socket=1    send_xn_setup=true
    wtsrunner.Gnb Xn Link Up    gnb=3    target=2
    sleep    30s

Check If Alarm Appeared for NRCELL5_tc8
    [Documentation]    This keyword is used to check if alarm appeared
    [Arguments]    ${fault_id}    ${configObjectName_id}
    CoamAdmin.Setup Admin    bts_host=${BTS_ADDRESS}    bts_port=${BTS_PORT}    use_ssl=${USE_SSL}    name=a6     timeout=120
    @{alarms}=    CoamAdmin.Get Active Alarms    connection=a6    #both $ and @ are OK
    @{active_fault_list}=    Create List
    FOR    ${alarm}    IN    @{alarms}    # get list right, must @
         ${fault}=    Get From Dictionary    ${alarm}    faultId
         Append To List    ${active_fault_list}    ${fault}    #${fault} is a number,not a string
    END
    ${fault_id}=    Convert To Integer    ${fault_id}    #${fault_id} is a string,it must be changed to number
    List Should Contain Value    ${active_fault_list}    ${fault_id}

    ${count}=    Count Values In List     ${active_fault_list}      ${fault_id}
     @{active_fault_list_1}=    Create List
    FOR    ${configObjectName}   IN    @{alarms}    # get list right, must @
         ${configObjectName}=    Get From Dictionary    ${configObjectName}    configObjectName

         Append To List    ${active_fault_list_1}   ${configObjectName}   #${fault} is a number,not a string
    END
     Get Matches   ${active_fault_list_1}    *${configObjectName_id}*
    [Teardown]    CoamAdmin.Teardown Admin     connection=a6


Check If Alarm Appeared for NRCELL6_tc8
    [Documentation]    This keyword is used to check if alarm appeared
    [Arguments]    ${fault_id}    ${configObjectName_id}
    CoamAdmin.Setup Admin    bts_host=${BTS_ADDRESS}    bts_port=${BTS_PORT}    use_ssl=${USE_SSL}    name=a8     timeout=120
    @{alarms}=    CoamAdmin.Get Active Alarms    connection=a8    #both $ and @ are OK
    @{active_fault_list}=    Create List
    FOR    ${alarm}    IN    @{alarms}    # get list right, must @
         ${fault}=    Get From Dictionary    ${alarm}    faultId
         Append To List    ${active_fault_list}    ${fault}    #${fault} is a number,not a string
    END
    ${fault_id}=    Convert To Integer    ${fault_id}    #${fault_id} is a string,it must be changed to number
    List Should Contain Value    ${active_fault_list}    ${fault_id}

    ${count}=    Count Values In List     ${active_fault_list}      ${fault_id}
     @{active_fault_list_1}=    Create List
    FOR    ${configObjectName}   IN    @{alarms}    # get list right, must @
         ${configObjectName}=    Get From Dictionary    ${configObjectName}    configObjectName

         Append To List    ${active_fault_list_1}   ${configObjectName}   #${fault} is a number,not a string
    END
     Get Matches   ${active_fault_list_1}    *${configObjectName_id}*
    [Teardown]    CoamAdmin.Teardown Admin     connection=a8
