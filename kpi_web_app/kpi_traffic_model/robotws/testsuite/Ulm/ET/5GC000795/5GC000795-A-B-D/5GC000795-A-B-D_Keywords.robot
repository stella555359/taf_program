*** Settings ***
Documentation
...    author: Ulm SQD 65
...    Team: 'MN RAN L3 SW ULM L3NRT SQD 65'
...    Email: 'I_MN_RAN_L3_SW_ULM_SQD_65@internal.nsn.com'
...    Description: Keywords for 5GC000795-A-B-D

Resource    ../../resources/SQD65/sqd65_keywords.robot

Library     taf.config.wts    WITH NAME     wts_conf

*** Variables ***

${TEST_MODE}                auto

*** Keywords ***

Add Bearer on eNB for UE and verify if created
    [Documentation]
    ...    :param ue_id:    ue_id configured in WTS configuration
    ...    :param bearer_id:  bearer id configured in WTS configuration
    [Arguments]    ${ue_id}=101    ${bearer_id}=7   ${filter_value}=0   ${precedence_value}=7
    Send Egate Command and verify output    cmd=bearer_add ue=${ue_id} id=${bearer_id} filter=${filter_value} precedence=${precedence_value}
    ...    pass_regexp=Bearer-${bearer_id} .* created
    # start verification, if entries containing in egate_console.log
    @{add_bearer_seq}=  Create List
    ...               bearer_add ue=${ue_id}
    ...               rrcConnectionReconfiguration
    ...               drb-ToAddModList
    ...               eps-BearerIdentity 6
    ...               rrcConnectionReconfigurationComplete
    ...               PGW-1: UE${ue_id}: PGW-initiated Bearer Creation. Bearer-7.*created   # .* substitutes (EBI=6, QCI=7)
    ${console_log_to_verify}   Save EGATE Log   add_bearer
    Verify sequence in Egate file  ${console_log_to_verify}  @{add_bearer_seq}

Activate LTE-NR Dual Connectivity for bearer 2 and verifiy UE IDs
    [Documentation]    :Author: Manfred Haberer
    ...    Command to trigger LTE-NR dual connectivity
    ...    and verify UE IDs afterwards
    ...    :param ue_id:            ue_id configured in WTS configuration
    ...    :param bearer_id:        bearer id configured in WTS configuration
    ...    :param type:             type of dual connectivity (default=split_scg)
    ...    :param pass_expression:  string to verify in egate_console.log
    ...
    [Arguments]    ${ue_id}=101    ${bearer_id}=2
    ...    ${type}=split_scg    ${pass_expression}=Successfully reconfigured dual connectivity
    Send Egate Command and verify output
    ...    cmd=enb_ue_dc_start ue=${ue_id} bearer=${bearer_id} target_gnb=2 target_cells=1 type=${type}
    ...    pass_regexp=${pass_expression}
    @{sgnb_add_seq}=  Create List
    ...               ue_attach id=${ue_id}
    ...               message c1 : rrcConnectionRequest
    ...               message c1 : rrcConnectionSetup
    ...               message c1 : rrcConnectionSetupComplete
    ...               message c1 : rrcConnectionReconfiguration
    ...               message c1 : rrcConnectionReconfigurationComplete
    ...               enb_ue_dc_start   # EGATE Command
    ${console_log_to_verify}   Save EGATE Log   sgnb_add_request
    Verify sequence in Egate file  ${console_log_to_verify}  @{sgnb_add_seq}
    ${UE_X2AP_ID}=   Run   grep -A7 "value SgNBAdditionRequest :" ${console_log_to_verify} | grep UE-X2AP-ID | awk '{print $4}'
    ${SgNB_UE_X2AP_ID}=  Run  grep -A12 "value SgNBAdditionRequestAcknowledge :" ${console_log_to_verify} | grep SgNB-UE-X2AP-ID | awk '{print $4}'
    Set Suite Variable    ${UE_X2AP_ID}
    Set Suite Variable    ${SgNB_UE_X2AP_ID}

Activate LTE-NR Dual Connectivity for bearers 2 and 7
    [Documentation]
    ...    :param ue_id:      ue_id configured in WTS configuration   REWORK needed
    ...    :param bearer_id:  bearer id configured in WTS configuration
    [Arguments]    ${ue_id}=101    ${bearer_id}=2,7
    Trigger LTE-NR dual connectivity for bearers   ue_id=${ue_id}   bearer_id=${bearer_id}
    @{sgnb_add_seq}=  Create List
    ...               enb_ue_dc_start ue=${ue_id}
    ...               SgNBAdditionRequest
    ...               E-RABs-ToBeAdded-SgNBAddReqList
    ...               e-RAB-ID 5
    ...               qCI 9
    ...               e-RAB-ID 6
    ...               qCI 7
    ...               successfulOutcome
    ...               SgNBAdditionRequestAcknowledge
    ...               e-RAB-ID 5
    ...               e-RAB-ID 6
    ...               UEC-1: UE${ue_id}: UE${ue_id}: Successfully reconfigured dual connectivity
    ...               SgNBReconfigurationComplete
    ${console_log_to_verify}   Save EGATE Log   sgnb_add_request
    Verify sequence in Egate file  ${console_log_to_verify}  @{sgnb_add_seq}

Activate LTE-NR Dual Connectivity for bearers
    [Documentation]
    ...    :param ue_id:      ue_id configured in WTS configuration   REWORK needed
    ...    :param bearer_id:  bearer id configured in WTS configuration
    [Arguments]    ${ue_id}=101    ${bearer_id}=2
    Trigger LTE-NR dual connectivity for bearers  ue_id=${ue_id}   bearer_id=${bearer_id}
    @{sgnb_add_seq}=    IF    '${bearer_id}'=='2,7'
    ...       Set one sgnbadd verification list creation
    ...    ELSE IF     '${bearer_id}'=='2'
    ...       Set two sgnbadd verification list creation
    ...    ELSE     FAIL    Unsupported Test Name!
    ${console_log_to_verify}   Save EGATE Log   sgnb_add_request
    Verify sequence in Egate file  ${console_log_to_verify}  @{sgnb_add_seq}

Release UE dual connectivity bearers 2 and 7 and specified cause
    [Documentation]
    ...    :param ue_id:      ue_id configured in WTS configuration   REWORK needed
    ...    :param bearer_id:  bearer id configured in WTS configuration
    [Arguments]    ${ue_id}=101
    UE Dual Connectivity Release  ue_id=${ue_id}  bearer=2,7  cause=RN_action_desirable_for_radio_reasons
    @{ue_dc_release_seq}=  Create List
    ...           enb_ue_dc_release ue=${ue_id}
    ...           SgNBReleaseRequ
    ...           E-RABs-ToBeReleased-SgNBRelReqList
    ...           e-RAB-ID 5
    ...           e-RAB-ID 6
    ...           successfulOutcome
    ...           SgNBReleaseRequestAcknowledge
    ${console_log_to_verify}   Save EGATE Log   ue_dc_release
    Verify sequence in Egate file  ${console_log_to_verify}  @{ue_dc_release_seq}

Activate LTE-NR DC modification release of unkown bearer
    [Documentation]    :Author: Manfred Haberer
    ...    Command to trigger LTE-NR dual connectivity modification release by sending hex-string
    ...    the base hex string may be taken from X2 logs of 5GC000795_B_TC01_Add_new... test case
    ...    ${UE_X2AP_ID}  and  ${SgNB_UE_X2AP_ID}  are global variables; they will be defined in
    ...    keyword  Activate LTE-NR Dual Connectivity for bearer 2 and verifiy UE IDs
    [Arguments]
    ${UE_X2AP_IDhex}=        Run   printf "%04x" ${UE_X2AP_ID}
    ${SgNB_UE_X2AP_IDhex}=   IF   ${SgNB_UE_X2AP_ID}<${65536}  Run   printf "%04x" ${SgNB_UE_X2AP_ID}
    ...                      ELSE    Run    printf "%06x" ${SgNB_UE_X2AP_ID}
    ${cmd4bit_short}    Catenate  SEPARATOR=  send_hex source=enb:1 target=gnb:2 hex=001d0045000006006f0002${UE_X2AP_IDhex}
    ...    00cf0002${SgNB_UE_X2AP_IDhex}000540020a80010d400313419800d7001c020000da4
    ...    0160c00301f0a0001870000001703e00a0001870000001800ce00050400801108
    ${cmd4bit_long}    Catenate  SEPARATOR=  send_hex source=enb:1 target=gnb:2 hex=001d0046000006006f0002${UE_X2AP_IDhex}
    ...    00cf000340${SgNB_UE_X2AP_IDhex}000540020a80010d400313419800d7001c020000d
    ...    a40160c00301f0a0001870000000303e00a0001870000000400ce00050400801108
    ${cmd6bit}    Catenate  SEPARATOR=  send_hex source=enb:1 target=gnb:2 hex=001d0047000006006f0002${UE_X2AP_IDhex}
    ...    00cf000480${SgNB_UE_X2AP_IDhex}000540020a80010d400313419800d7001c020000d
    ...    a40160c00301f0a0001870000000303e00a0001870000000400ce00050400801108
    ${CmdStr}=   Set Variable If   ${SgNB_UE_X2AP_ID}<${256}             ${cmd4bit_short}
    ...                            ${256}<${SgNB_UE_X2AP_ID}<${65536}    ${cmd4bit_long}
    ...                            ${65536}<${SgNB_UE_X2AP_ID}           ${cmd6bit}
    ute_wtssim.Execute Egate Command   ${CmdStr}   alias=ap_egate

Activate LTE-NR DC modification release
    [Documentation]
    ...    Command to trigger LTE-NR dual connectivity modification release
    ...
    ...    :param ue_id:            ue_id configured in WTS configuration
    ...    :param bearer_id:        bearer id configured in WTS configuration
    ...    :param reason:           reason to trigger SgNB modification (default=bearer_to_add)
    ...    :param by:               determines the initiator of the DC procedure (default=enb)
    ...    :param cause:            cause for the DC procedure (default=RN_CauseRadioNetwork_unspecified)
    ...    :param type:             type of dual connectivity (default=split_scg)
    ...    :param pass_expression:  string to verify in egate_console.log
    ...
    [Arguments]    ${ue_id}=101    ${bearer_id}=7    ${by}=enb    ${cause}=RN_CauseRadioNetwork_unspecified
    ...    ${type}=split_scg    ${pass_expression}=${None}
    Send Egate Command and verify output
    ...    cmd=enb_ue_dc_modify ue=${ue_id} bearer_to_release=${bearer_id} by=${by} cause=${cause} type=${type}
    ...    pass_regexp=${pass_expression}
    @{ue_dc_release_seq}=  Create List
    ...           enb_ue_dc_modify ue=${ue_id} bearer_to_release=${bearer_id}
    ...           SgNBModificationRequest
    ...           successfulOutcome
    ...           SgNBModificationRequestAcknowledge
    ...           E-RABs-Admitted-ToBeReleased-SgNBModAckList

    ${console_log_to_verify}   Save EGATE Log   ue_dc_release
    Verify sequence in Egate file  ${console_log_to_verify}  @{ue_dc_release_seq}

Release UE dual connectivity
    [Documentation]
    ...    Command to trigger LTE-NR dual connectivity release
    ...
    ...    :param ue_id:            ue_id configured in WTS configuration
    ...    :param bearer_id:        bearer id configured in WTS configuration
    ...    :param reason:           reason to trigger SgNB modification (default=bearer_to_add)
    ...    :param by:               determines the initiator of the DC procedure (default=enb)
    ...    :param cause:            cause for the DC procedure (default=RN_CauseRadioNetwork_unspecified)
    ...    :param type:             type of dual connectivity (default=split_scg)
    ...    :param pass_expression:  string to verify in egate_console.log
    ...
    [Arguments]    ${ue_id}=101    ${bearer_id}=7    ${by}=enb    ${cause}=RN_CauseRadioNetwork_unspecified
    ...    ${type}=split_scg    ${pass_expression}=${None}
    Send Egate Command and verify output
    ...    cmd=enb_ue_dc_release ue=${ue_id} bearer=${bearer_id} by=${by} cause=${cause} type=${type}
    ...    pass_regexp=${pass_expression}
    @{ue_dc_release_seq}=  Create List
    ...           enb_ue_dc_release ue=${ue_id}
    ...           SgNBReleaseRequest
    ...           E-RABs-ToBeReleased-SgNBRelReqList
    ...           e-RAB-ID 5
    ...           e-RAB-ID 6
    ...           successfulOutcome
    ...           SgNBReleaseRequestAcknowledge
    ${console_log_to_verify}   Save EGATE Log   ue_dc_release
    Verify sequence in Egate file  ${console_log_to_verify}  @{ue_dc_release_seq}

Activate LTE-NR DC modification
    [Documentation]
    ...    Command to trigger LTE-NR dual connectivity modification
    ...
    ...    :param ue_id:            ue_id configured in WTS configuration
    ...    :param bearer_id:        bearer id configured in WTS configuration
    ...    :param reason:           reason to trigger SgNB modification (default=bearer_to_add)
    ...    :param by:               determines the initiator of the DC procedure (default=enb)
    ...    :param cause:            cause for the DC procedure (default=RN_CauseRadioNetwork_unspecified)
    ...    :param type:             type of dual connectivity (default=split_scg)
    ...    :param pass_expression:  string to verify in egate_console.log
    ...
    [Arguments]    ${ue_id}=101    ${bearer_id}=7    ${reason}=bearer_to_add    ${by}=enb    ${cause}=RN_CauseRadioNetwork_unspecified
    ...    ${pass_expression}=rrcConnectionReconfigurationComplete
    Send Egate Command and verify output
    ...    cmd=enb_ue_dc_modify ue=${ue_id} ${reason}=${bearer_id} by=${by} cause=${cause}    # removed type
    ...    pass_regexp=${pass_expression}
    Log    LTE-NR dual connectivity modification with reason ${reason} for bearer ${bearer_id} is successful    console=${P_console}
    @{ue_dc_modify_seq}=
    ...    IF  '${TEST NAME}'=='5GC000795_B_TC11_SgNB_Reconfiguration_Failure_during_SgNB_Modification_Successful_SgNB_Release'
    ...           Set LTE-NR DC modification list creation B_TC11  ue_id=${ue_id}
    ...    ELSE   Set LTE-NR DC modification list creation  ue_id=${ue_id}
    ${console_log_to_verify}   Save EGATE Log   ue_dc_modify
    Verify sequence in Egate file  ${console_log_to_verify}  @{ue_dc_modify_seq}

Set LTE-NR DC modification list creation
    [Arguments]  ${ue_id}=101
    @{ue_dc_modify_seq}=  Create List
    ...           enb_ue_dc_modify ue=${ue_id} bearer_to_add=7
    ...           SgNBModificationRequest
    ...           successfulOutcome
    ...           SgNBModificationRequestAcknowledge
    ...           E-RABs-Admitted-ToBeAdded-SgNBModAckList
    ...           rrcConnectionReconfiguration
    ...           rrcConnectionReconfigurationComplete
    RETURN      @{ue_dc_modify_seq}

Set LTE-NR DC modification list creation B_TC11
    [Arguments]  ${ue_id}=101
    @{ue_dc_modify_seq}=  Create List
    ...           enb_endc_param
    ...           enb_ue_dc_modify ue=${ue_id} bearer_to_add=7
    ...           SgNBModificationRequest
    ...           successfulOutcome
    ...           SgNBModificationRequestAcknowledge
    ...           E-RABs-Admitted-ToBeAdded-SgNBModAckList
    ...           rrcConnectionReconfiguration
    ...           rrcConnectionReconfigurationComplete
    ...           SgNBReleaseRequired
    ...           SgNBReleaseConfirm
    RETURN      @{ue_dc_modify_seq}

Set one sgnbadd verification list creation
    [Arguments]  ${ue_id}=101
    @{sgnb_add_seq}=  Create List
    ...               enb_ue_dc_start ue=${ue_id}
    ...               SgNBAdditionRequest
    ...               E-RABs-ToBeAdded-SgNBAddReqList
    ...               e-RAB-ID 5
    ...               qCI 9
    ...               e-RAB-ID 6
    ...               qCI 7
    ...               successfulOutcome
    ...               SgNBAdditionRequestAcknowledge
    ...               e-RAB-ID 5
    ...               e-RAB-ID 6
    ...               UEC-1: UE${ue_id}: UE${ue_id}: Successfully reconfigured dual connectivity
    ...               SgNBReconfigurationComplete
    RETURN      @{sgnb_add_seq}

Set two sgnbadd verification list creation
    [Arguments]  ${ue_id}=101
    @{sgnb_add_seq}=  Create List
    ...              ue_attach id=${ue_id}
    ...              message c1 : rrcConnectionRequest
    ...              message c1 : rrcConnectionSetup
    ...              message c1 : rrcConnectionSetupComplete
    ...              message c1 : rrcConnectionReconfiguration
    ...              message c1 : rrcConnectionReconfigurationComplete
    ...              enb_ue_dc_start ue=${ue_id}
    ...              SgNBAdditionRequest
    ...              SgNBAdditionRequestAcknowledge
    ...              e-RAB-ID 5
    ...              SgNBReconfigurationComplete
    RETURN      @{sgnb_add_seq}

Collect PMCounters
    pmcounters.Wait until the current Measurement Period stops
    ${pm_files}    pmcounters.Collect PM Counter
    RETURN  ${pm_files}

Verify B_TC100 PMCounters
    ${expected_pm_counter_list}=   Create List
    ...   M55112C03001  ==  2
    ...   M55112C03002  ==  2
    ...   M55114C00001  ==  2
    ...   M55114C00002  ==  2
    ...   M55114C00003  ==  2
    ${pm_files}    Collect PMCounters
    Verify PM Counter Reference Table     reference_table=${expected_pm_counter_list}
    ...  pm_dir=${pm_files}        distname_suffix=1

Verify SgNBadd_several_ERab_TC2 PMCounters
    ${expected_pm_counter_list}=   Create List
    ...   M55112C03001  ==  2
    ...   M55112C03002  ==  2
    ...   M55114C00001  ==  1
    ...   M55114C00002  ==  1
    ...   M55114C00003  ==  2
    ...   M55112C00003  ==  1
    ...   M55112C00004  ==  1
    ${pm_files}    Collect PMCounters
    Verify PM Counter Reference Table     reference_table=${expected_pm_counter_list}
    ...  pm_dir=${pm_files}        distname_suffix=1

Verify PMCounters 5GC000425-X unbalanced traffic
    ${expected_pm_counter_list}=   Create List
    ...   M55320C05001  >=  0
    ...   M55320C05002  >=  0
    ...   M55320C05003  >=  0
    ...   M55320C05004  >=  0
    ...   M55320C05005  >=  0
    ...   M55320C05006  >=  0
    ...   M55320C05007  >=  0
    ...   M55320C05008  >=  0
    ...   M55320C05009  >=  175000000
    ...   M55320C05010  >=  0
    ...   M55320C05011  >=  0
    ...   M55320C05012  >=  0
    ...   M55320C05013  >=  0
    ...   M55320C05014  >=  0
    ...   M55320C05015  >=  0
    ...   M55320C05016  >=  0
    ...   M55320C05017  >=  0
    ...   M55320C05018  >=  0
    ...   M55320C05019  >=  0
    ...   M55320C05020  >=  0
    ...   M55320C06001  >=  0
    ...   M55320C06002  >=  0
    ...   M55320C06003  >=  0
    ...   M55320C06004  >=  0
    ...   M55320C06005  >=  0
    ...   M55320C06006  >=  0
    ...   M55320C06007  >=  0
    ...   M55320C06008  >=  0
    ...   M55320C06009  >=  175000
    ...   M55320C06010  >=  0
    ...   M55320C06011  >=  0
    ...   M55320C06012  >=  0
    ...   M55320C06013  >=  0
    ...   M55320C06014  >=  0
    ...   M55320C06015  >=  0
    ...   M55320C06016  >=  0
    ...   M55320C06017  >=  0
    ...   M55320C06018  >=  0
    ...   M55320C06019  >=  0
    ...   M55320C06020  >=  0
    ${pm_files}    Collect PMCounters
    Verify PM Counter Reference Table     reference_table=${expected_pm_counter_list}
    ...  pm_dir=${pm_files}        distname_suffix=1

Verify B_TC10 PMCounters
    ${expected_pm_counter_list}=   Create List
    ...   M55326C01001  >=  29980  PDCP_SDU_USDAT_NUM_DL_PLMN
    ...   M55326C01002  >=  29980  PDCP_SDU_USDAT_NUM_UL_PLMN
    ${pm_files}    Collect PMCounters
    Verify PM Counter Reference Table     reference_table=${expected_pm_counter_list}
    ...  pm_dir=${pm_files}        distname_suffix=489   # distname_suffix need to be 489 to find correct part in xml-file

Run simple Egate Command
    [Documentation]
    ...     execute only simple command on EGATE
    ...    :param cmd:   contain the command to be executed
    [Arguments]    ${cmd}="info"
    ute_wtssim.Execute Egate Command   ${cmd}   alias=ap_egate
    Sleep  2s

Start Data Traffic DL_UL on bearers 2 and 7
    [Documentation]
    ...     clear defined behaviour - start DL and UL traffic on bearer 2 and bearer 7
    ...     :param ue_id:   choice to select different id for a ue; default = 101
    [Arguments]    ${ue_id}=101
    ute_wtssim.Execute Egate Command And Wait For Data
    ...      cmd=trf_data_start ue=${ue_id} id=2 dir=dl mbps=1 trf_id=1   alias=ap_egate   # DL on bearer 2
    ute_wtssim.Execute Egate Command And Wait For Data
    ...      cmd=trf_data_start ue=${ue_id} id=2 dir=ul kbps=500 trf_id=1   alias=ap_egate   # UL on bearer 2
    ute_wtssim.Execute Egate Command And Wait For Data
    ...      cmd=trf_data_start ue=${ue_id} id=7 dir=dl mbps=1 trf_id=1   alias=ap_egate   # DL on bearer 7
    ute_wtssim.Execute Egate Command And Wait For Data
    ...      cmd=trf_data_start ue=${ue_id} id=7 dir=ul kbps=500 trf_id=1   alias=ap_egate

Start Data Traffic DL on bearers 2 and 7
    [Documentation]
    ...     clear defined behaviour - start only DL traffic on bearer 2 and bearer 7
    ...     :param ue_id:   choice to select different id for a ue; default = 101
    [Arguments]    ${ue_id}=101
    ute_wtssim.Execute Egate Command And Wait For Data
    ...      cmd=trf_data_start ue=${ue_id} id=2 dir=dl mbps=1 trf_id=1   alias=ap_egate
    ute_wtssim.Execute Egate Command And Wait For Data
    ...      cmd=trf_data_start ue=${ue_id} id=7 dir=dl mbps=1 trf_id=1   alias=ap_egate

Start Unbalanced Data Traffic DL on bearers 2 and 7
    [Documentation]
    ...     clear defined behaviour - start only DL traffic on bearer 2 and bearer 7
    ...                               but 150 Mbit on bearer 2 and 1 Mbit on bearer 7
    ...     :param ue_id:   choice to select different id for a ue; default = 101
    [Arguments]    ${ue_id}=101
    ute_wtssim.Execute Egate Command And Wait For Data
    ...      cmd=trf_data_start ue=${ue_id} id=2 dir=dl mbps=150 trf_id=1 size=1000  alias=ap_egate
    ute_wtssim.Execute Egate Command And Wait For Data
    ...      cmd=trf_data_start ue=${ue_id} id=7 dir=dl mbps=1 trf_id=1 size=1000   alias=ap_egate

Start Data Traffic DL_UL on bearer 7
    [Documentation]
    ...     clear defined behaviour - start DL and UL traffic on bearer 7
    ...     :param ue_id:   choice to select different id for a ue; default = 101
    [Arguments]    ${ue_id}=101
    ute_wtssim.Execute Egate Command And Wait For Data
    ...      cmd=trf_data_start ue=${ue_id} id=7 dir=dl mbps=1 trf_id=1   alias=ap_egate
    ute_wtssim.Execute Egate Command And Wait For Data
    ...      cmd=trf_data_start ue=${ue_id} id=7 dir=ul kbps=500 trf_id=1   alias=ap_egate

Start Data Traffic with defined conditions
    [Documentation]
    ...     clear defined behaviour - start traffic on only one bearer
    ...     define detailed parameters for desired traffic conditions
    ...     :param ue_id:       choice to select different id for a ue; default = 101
    ...     :param bearer_id:   bearer ID
    ...     :param trf_id:      traffic ID
    ...     :param direction:   traffic direction UL or DL
    [Arguments]    ${ue_id}=101   ${bearer_id}=2   ${trf_id}=1   ${direction}=dl
    ute_wtssim.Execute Egate Command And Wait For Data
    ...   cmd=trf_data_start ue=${ue_id} id=${bearer_id} trf_id=${trf_id} dir=${direction} size=300 burst=1 period_ms=4 packets=30000
    ...     alias=ap_egate   # start traffic
    Sleep    3s

Stop Data Traffic on bearers 2 and 7
    [Documentation]
    ...     clear defined behaviour - Stop DL and UL traffic on bearer 2 and bearer 7
    ...     :param ue_id:   choice to select different id for a ue; default = 101
    [Arguments]    ${ue_id}=101
    ute_wtssim.Execute Egate Command And Wait For Data
    ...      cmd=trf_data_stop ue=${ue_id} id=2 dir=dl   alias=ap_egate
    ute_wtssim.Execute Egate Command And Wait For Data
    ...      cmd=trf_data_stop ue=${ue_id} id=2 dir=ul   alias=ap_egate
    ute_wtssim.Execute Egate Command And Wait For Data
    ...      cmd=trf_data_stop ue=${ue_id} id=7 dir=dl   alias=ap_egate
    ute_wtssim.Execute Egate Command And Wait For Data
    ...      cmd=trf_data_stop ue=${ue_id} id=7 dir=ul   alias=ap_egate

Stop Data Traffic on bearer 7
    [Documentation]
    ...     clear defined behaviour - Stop DL and UL traffic on bearer 7
    ...     :param ue_id:   choice to select different id for a ue; default = 101
    [Arguments]    ${ue_id}=101
    ute_wtssim.Execute Egate Command And Wait For Data
    ...      cmd=trf_data_stop ue=${ue_id} id=7 dir=dl   alias=ap_egate
    ute_wtssim.Execute Egate Command And Wait For Data
    ...      cmd=trf_data_stop ue=${ue_id} id=7 dir=ul   alias=ap_egate

Stop Data Traffic DL on bearer 2
    [Documentation]
    ...     clear defined behaviour - Stop only DL on bearer 2
    ...     :param ue_id:   choice to select different id for a ue; default = 101
    [Arguments]    ${ue_id}=101
    ute_wtssim.Execute Egate Command And Wait For Data
    ...      cmd=trf_data_stop ue=${ue_id} id=2 dir=dl   alias=ap_egate

Stop Data Traffic DL on bearer 7
    [Documentation]
    ...     clear defined behaviour - Stop only DL on bearer 7
    ...     :param ue_id:   choice to select different id for a ue; default = 101
    [Arguments]    ${ue_id}=101
    ute_wtssim.Execute Egate Command And Wait For Data
    ...      cmd=trf_data_stop ue=${ue_id} id=7 dir=dl   alias=ap_egate

Get Bearer Stats from 2 and 7
    [Documentation]
    ...     get status from bearers; only two fixed bearers no 2 and no 7
    ...    :param check_point:   python implementation uses check_point as command but Egate don't know this!
    [Arguments]    ${ue_id}=101
    ute_wtssim.Execute Egate Command    cmd=bearer_stats ue=${ue_id} id=2 dir=bi dc_cell_group=scg   alias=ap_egate
    ute_wtssim.Execute Egate Command    cmd=bearer_stats ue=${ue_id} id=2 dir=bi dc_cell_group=mcg   alias=ap_egate

    ute_wtssim.Execute Egate Command    cmd=bearer_stats ue=${ue_id} id=7 dir=bi dc_cell_group=scg   alias=ap_egate
    ute_wtssim.Execute Egate Command    cmd=bearer_stats ue=${ue_id} id=7 dir=bi dc_cell_group=mcg   alias=ap_egate

Get Bearer Stats from 7
    [Documentation]
    ...     get status from bearers; only two fixed bearers no 2 and no 7
    ...    :param check_point:   python implementation uses check_point as command but Egate don't know this!
    [Arguments]    ${ue_id}=101
    ute_wtssim.Execute Egate Command    cmd=bearer_stats ue=${ue_id} id=7 dir=bi dc_cell_group=scg   alias=ap_egate
    ute_wtssim.Execute Egate Command    cmd=bearer_stats ue=${ue_id} id=7 dir=bi dc_cell_group=mcg   alias=ap_egate

Verify final log for D_TC34
    [Documentation]
    ...     verification of the last bunch of messages/words... in finally stored egate_console_tcN_end.log
    ...      SgNBReleaseRequired, user-inactivity, message c1 : rrcConnectionRelease, detached
    ...    :param log_file_to_verify:  complete path and filename to be verified
    [Arguments]    ${log_file_to_verify}=""
    @{verification_list}=  Create List
    ...           SgNBReleaseRequired
    ...           user-inactivity
    ...           message c1 : rrcConnectionRelease :
    ...           detached
    Verify sequence in Egate file  ${log_file_to_verify}  @{verification_list}

Verify final log for B_TC10
    [Documentation]
    ...     verification of the last bunch of messages/words... in finally stored egate_console_tcN_end.log
    ...    :param log_file_to_verify:  complete path and filename to be verified
    [Arguments]    ${log_file_to_verify}=""
    @{verification_list}=  Create List
    ...            trf_data_start.*trf_id=1
    ...            trf_data_start.*trf_id=2
    ...            send_hex
    ...            unsuccessfulOutcome
    ...            SgNBModificationRequestReject
    ...            misc : unspecified
    ...            ue_detach
    Verify sequence in Egate file  ${log_file_to_verify}  @{verification_list}
