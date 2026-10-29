*** Settings ***
Documentation   This is a keyword file for 5GC000710-B, part keywords
...             Team: 'MN 5G&SC SW Eng ULM L2PS 60 SG'
...             Email: 'I_ECE_RD_ULM_SQD_60_GMS@internal.nsn.com'
...             Author: Sylvia Schneider
#-------------------------------------------------------------------------------------------------------------

*** Variables ***

${wireshark_running}     false
${ue_id}                 51

*** Keywords ***

Create ips for simulated gnb
    [Documentation]    [PRIVATE]    create IPs used for WTS
    ...       :Autor: Sylvia Schneider
    Log To Console    \ncreate IPs 10.0.1.3 and 10.0.1.4 on VM eth3
    Configure IP on VM    ip=10.0.1.3    interface=eth3
    Configure IP on VM    ip=10.0.1.4    interface=eth3


get plmn nrarfcn tac version from gNB SCF
    [Documentation]    [PRIVATE]    get values from SCF for update in wts and commissioning
    ...       :Autor: Sylvia Schneider
    ${parsed_SCF}    parse XML    ${P_ORIG_SCF}
    ${nrarfcnDl}    get element text    ${parsed_SCF}
    ...    xpath=.//managedObject[@distName="${bts_distName}/NRCELL-3/NRCELL_FDD-1"]/p[@name="nrarfcnDl"]
    Set To Dictionary    ${SCF}   nrarfcnDl   ${nrarfcnDl}
    Log To Console    variable SCF.nrarfcnDl contains ${SCF.nrarfcnDl}

    ${nrarfcnUl}    get element text    ${parsed_SCF}
    ...    xpath=.//managedObject[@distName="${bts_distName}/NRCELL-3/NRCELL_FDD-1"]/p[@name="nrarfcnUl"]
    Set To Dictionary    ${SCF}   nrarfcnUl   ${nrarfcnUl}
    Log To Console    variable SCF.nrarfcnUl contains ${SCF.nrarfcnUl}

    ${mcc}    get element text          ${parsed_SCF}    xpath=.//managedObject[@distName="${bts_distName}/NRPLMN-1"]/p[@name="mcc"]
    Set To Dictionary    ${SCF}   mcc   ${mcc}
    Log To Console    variable SCF.mcc contains ${SCF.mcc}

    ${mnc}    get element text          ${parsed_SCF}    xpath=.//managedObject[@distName="${bts_distName}/NRPLMN-1"]/p[@name="mnc"]
    Set To Dictionary    ${SCF}   mnc   ${mnc}
    Log To Console    variable SCF.mnc contains ${SCF.mnc}

    ${mnclenght}    get element text    ${parsed_SCF}    xpath=.//managedObject[@distName="${bts_distName}/NRPLMN-1"]/p[@name="mncLength"]
    Set To Dictionary    ${SCF}   mnclenght   ${mnclenght}
    Log To Console    variable SCF.mnclenght contains ${SCF.mnclenght}

    ${fiveGsTac}    get element text    ${parsed_SCF}
    ...    xpath=.//managedObject[@class="com.nokia.srbts.nrbts:TRACKINGAREA"]/p[@name="fiveGsTac"]
    Set To Dictionary    ${SCF}   fiveGsTac   ${fiveGsTac}
    Log To Console    variable SCF.fiveGsTac contains ${SCF.fiveGsTac}

    ${version}    get element attribute    ${parsed_SCF}    version     xpath=.//managedObject[@distName="${bts_distName}"]
    Set To Dictionary    ${SCF}   version   ${version}
    Log To Console    variable SCF.version contains ${SCF.version}


start wireshark trace
    [Documentation]    [PRIVATE]    start wireshark trace
    ...       :Autor: Sylvia Schneider
    Start Tcpdump on TestPc
    ...  options=-i any sctp or icmp
    ...  collector=dump_testpc
    sleep     5s
    Set suite variable      ${wireshark_running}    true


stop wireshark trace
    [Documentation]    [PRIVATE]    stop wireshark trace
    ...       :Autor: Sylvia Schneider
    [Arguments]     ${wireshark_store}=${resultDir}/wireshark.pcap
    IF    '${wireshark_running}'=='false'   RETURN
    sleep     5s
    Stop Tcpdump on TestPc
    ...  collector=dump_testpc
    ...  target_dir=${resultDir}
    sleep     2s
    Move File    ${resultDir}/dump_testpc/dump_testpc.pcap    ${wireshark_store}
    sleep     2s
    Set suite variable      ${wireshark_running}    false


stop wireshark trace and verify successful xn setup
    [Documentation]    [PRIVATE]    stop wireshark trace and verify that xn setup is successful
    ...       :Autor: Sylvia Schneider
    stop wireshark trace            wireshark_store=${resultDir}/wireshark_startTL.pcap
    verify successful xn setup      wireshark_store=${resultDir}/wireshark_startTL.pcap


check all radio units online
    [Documentation]    [PRIVATE]   check that all radio units are online
    ...     :Autor: Sylvia Schneider
    Log To Console    Waiting until all RUs are online
    ${oam_alias}    connect.Setup OAM http session    node_type=gnb  node_id=${0}
    wait until keyword succeeds
    ...    10min   20sec
    ...    Verify All Radios are Online    connection=${oam_alias}
    Log to console    RUs ready
    [Teardown]     connect.Teardown OAM http session    node_type=gnb  node_id=${0}


set AMF param indexToRFSP
    [Documentation]    [PRIVATE]    set indexToRFSP in wts
    ...       :Autor: Sylvia Schneider
    ${cmd}   set variable   amf_ue_ics_param id=1 indexToRFSP=99
    Log To Console    execute on wts: ${cmd}
    sleep     5s
    ute_wtssim.execute egate command     cmd=${cmd}    alias=ap_egate


set AMF dl param indexToRFSP
    [Documentation]    [PRIVATE]    set indexToRFSP-NAS in wts
    ...       :Autor: Sylvia Schneider
    ${cmd}   set variable   amf_dl_nas_transport_param id=1 indexToRFSP=88
    Log To Console    execute on wts: ${cmd}
    sleep     5s
    ute_wtssim.execute egate command     cmd=${cmd}    alias=ap_egate

    ${cmd}   set variable       ue_send_dl_nas_transport id=${ue_id}
    Log To Console    execute on wts: ${cmd}
    sleep     5s
    ute_wtssim.execute egate command     cmd=${cmd}    alias=ap_egate


register UE and start PDU
    [Documentation]    [PRIVATE]    start UE connection
    ...       :Autor: Sylvia Schneider
    ${cmd}   set variable   ue_register id=${ue_id} nwslice=1
    ${pass}  set variable   REGISTRATION COMPLETE from UE
    Log To Console    execute on wts: ${cmd}
    Log To Console    check: ${pass}
    sleep     5s
    ute_wtssim.execute egate command and wait for data
    ...    cmd=${cmd}
    ...    pass_regexp=${pass}
    ...    alias=ap_egate

    ${cmd}   set variable   ue_pdu_session_setup pdu=1 ue=${ue_id} nwslice=1 gw=${ue_id}
    ${pass}  set variable   Initial Context Setup Successful
    Log To Console    execute on wts: ${cmd}
    Log To Console    check: ${pass}
    sleep     5s
    ute_wtssim.execute egate command and wait for data
    ...    cmd=${cmd}
    ...    pass_regexp=${pass}
    ...    alias=ap_egate


modify indexToRFSP
    [Documentation]    [PRIVATE]    modify indexToRFSP in wts
    ...       :Autor: Sylvia Schneider
    ${cmd}   set variable   ue_ctx_ng_mod id=${ue_id} indexToRFSP=77
    Log To Console    execute on wts: ${cmd}
    sleep     5s
    ute_wtssim.execute egate command and wait for data    cmd=${cmd}     alias=ap_egate


send A3 measurement
    [Documentation]    [PRIVATE]    trigger single handover by sending A3 measurement in wts
    ...       :Autor: Sylvia Schneider
    ${cmd}   set variable   ue_measurement_send_nr event=A3 srsrp_nr=50 phycell_id=48 nrsrp_nr=70 meas_id=1 id=${ue_id}
    ${pass}  set variable   rrcReconfigurationComplete
    Log To Console    execute on wts: ${cmd}
    Log To Console    check: ${pass}
    sleep     10s
    ute_wtssim.execute egate command and wait for data
    ...    cmd=${cmd}
    ...    pass_regexp=${pass}
    ...    alias=ap_egate


execute handover scenario
    [Documentation]    [PRIVATE]    trigger handovers by sending A3 measurements in wts
    ...       :Autor: Sylvia Schneider
    ${cmd}   set variable   ue_measurement_send_nr event=A3 srsrp_nr=50 phycell_id=48 nrsrp_nr=70 meas_id=1 id=${ue_id}
    ${pass}  set variable   rrcReconfigurationComplete
    Log To Console    execute on wts: ${cmd}
    Log To Console    check: ${pass}
    sleep     10s
    ute_wtssim.execute egate command and wait for data
    ...    cmd=${cmd}
    ...    pass_regexp=${pass}
    ...    alias=ap_egate

    ${cmd}   set variable   ue_history_information_list_add_ngran id=1 gnb_id=3 cell_type=medium nrcgi=311:489|0x01 time_ue_stayed_in_cell=100
    Log To Console    execute on wts: ${cmd}
    sleep     10s
    ute_wtssim.execute egate command
    ...    cmd=${cmd}
    ...    alias=ap_egate

    ${cmd}   set variable   ue_history_information_list id=1 action=commit
    ${pass}  set variable   UE History List: 1 was committed
    Log To Console    execute on wts: ${cmd}
    Log To Console    check: ${pass}
    sleep     10s
    ute_wtssim.execute egate command and wait for data
    ...    cmd=${cmd}
    ...    pass_regexp=${pass}
    ...    alias=ap_egate

    Log To Console    execute on wts: ue_enb_param id=1 ue_history_list=1
    sleep     10s
    ute_wtssim.execute egate command
    ...   cmd=ue_enb_param id=1 ue_history_list=1    alias=ap_egate

    ${cmd}   set variable   ue_measurement_send_nr event=A3 srsrp_nr=50 phycell_id=52 nrsrp_nr=70 meas_id=3 id=${ue_id}
    ${pass}  set variable   rrcReconfigurationComplete
    Log To Console    execute on wts: ${cmd}
    Log To Console    check: ${pass}
    sleep     10s
    ute_wtssim.execute egate command and wait for data
    ...    cmd=${cmd}
    ...    pass_regexp=${pass}
    ...    alias=ap_egate

    ${cmd}   set variable   ue_measurement_send_nr event=A3 srsrp_nr=50 phycell_id=48 nrsrp_nr=70 meas_id=7 id=${ue_id}
    ${pass}  set variable   rrcReconfigurationComplete
    Log To Console    execute on wts: ${cmd}
    Log To Console    check: ${pass}
    sleep     10s
    ute_wtssim.execute egate command and wait for data
    ...    cmd=${cmd}
    ...    pass_regexp=${pass}
    ...    alias=ap_egate


stop PDU and deregister UE
    [Documentation]    [PRIVATE]    stop UE connection
    ...       :Autor: Sylvia Schneider
    ${cmd}   set variable   amf_ue_ics_param id=1 indexToRFSP=none
    Log To Console    execute on wts: ${cmd}
    sleep     5s
    ute_wtssim.execute egate command     cmd=${cmd}   alias=ap_egate

    ${cmd}   set variable   ue_pdu_session_release pdu=1 ue=${ue_id}
    ${pass}  set variable   Successfully released PDU Session
    Log To Console    execute on wts: ${cmd}
    Log To Console    check: ${pass}
    sleep     5s
    ute_wtssim.execute egate command and wait for data
    ...    cmd=${cmd}
    ...    pass_regexp=${pass}
    ...    alias=ap_egate

    ${cmd}   set variable   ue_deregister id=${ue_id} ue_deregister_type=switch_off
    ${pass}  set variable   Received UE Context Release Complete
    Log To Console    execute on wts: ${cmd}
    Log To Console    check: ${pass}
    sleep     5s
    ute_wtssim.execute egate command and wait for data
    ...    cmd=${cmd}
    ...    pass_regexp=${pass}
    ...    alias=ap_egate
