*** Settings ***
Documentation   This is a keyword file for 5GC000710-B, part wts
...             Team: 'MN 5G&SC SW Eng ULM L2PS 60 SG'
...             Email: 'I_ECE_RD_ULM_SQD_60_GMS@internal.nsn.com'
...             Author: Sylvia Schneider
#-------------------------------------------------------------------------------------------------------------
Library         taf.config.wts    WITH NAME    wts

*** Keywords ***
Update wts file for TC 710B
    [Documentation]    [PRIVATE]    update wts cfg file
    ...       :Autor: Sylvia Schneider
    Log To Console    \nupdate wts cfg
    ${wtsconfig}   Get WTS Config    target_dir=${resultBaseDir}
    wts.Load wts cfg             ${wtsconfig}
    wts.Insert    set GNB_XN_ADDR="10.0.1.2"   after   set GNB_NG_ADDR="10.0.1.2"
    wts.Insert    set GNB3_XN_ADDR="10.0.1.3"   after    set GNB_XN_ADDR="10.0.1.2"
    wts.Insert    set GNB3_NG_ADDR="10.0.1.4"   after    set GNB3_XN_ADDR="10.0.1.3"
    wts.Modify    set_gnb id=2    gnb_id=0x1:22 xn=$GNB_XN_ADDR
    wts.Modify    set_cell id=3 gnb=2  nr_arfcn=${SCF.nrarfcnUl}:${SCF.nrarfcnDl} gscn=1582
    ${plmn}   wts.get parameter    set_gnb id=2     plmn
    wts.Insert    set_gnb id=3 type=simulated plmn=${plmn} ng=$GNB3_NG_ADDR gnb_id=0x26:22    after   set_cell id=1 gnb=2
    wts.Modify    set_gnb id=3    daemon=$DAEMON_IP:$DAEMON_PORT x2_peers=none xn=$GNB3_XN_ADDR amf=1 plmnList=311:489 nssai=0x1:0xd143a5
    wts.Insert    set_cell id=1 gnb=3 pci=16:0 tac=${SCF.fiveGsTac} nrci=0x01 tdd_cell=off     after   set_gnb id=3
    wts.Modify    set_cell id=1 gnb=3   proxy=$GNB3_NG_ADDR:9999|$GNB3_NG_ADDR:8890
    wts.Modify    set_cell id=1 gnb=3   nr_arfcn=${SCF.nrarfcnUl}:${SCF.nrarfcnDl} mandatory_for_activation=off gscn=1582
    wts.Insert    gnb_param id=3 xn_listening_socket=1 send_xn_setup=true	  after     set_cell id=1 gnb=3
    wts.Save wts cfg             	${resultBaseDir}/basic_wts_710B.cfg
    Log To Console    \nwts cfg saved as ${resultBaseDir}/basic_wts_710B.cfg


check wts in active state
    [Documentation]    [PRIVATE]    check that wts is in state active
    ...       :Autor: Sylvia Schneider
    Log To Console    \ncheck if wts in active state
    Wait Until Keyword Succeeds    5 min    20 sec    check wts state
    Log To Console    check if wts in active state ended


check wts state
    [Documentation]    [PRIVATE]    check that wts is in state active
    ...       :Autor: Sylvia Schneider
    ute_wtssim.execute egate command and wait for data
    ...    cmd=sim_state_disp
    ...    pass_regexp=The state is ACTIVE   alias=ap_egate
