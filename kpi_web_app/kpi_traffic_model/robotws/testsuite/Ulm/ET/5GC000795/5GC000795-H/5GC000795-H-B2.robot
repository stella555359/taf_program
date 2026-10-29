*** Settings ***

Documentation
...    author: 'VRF Ulm Team #4'
...    Team: 'MN RAN RD VRF ULM 4'
...    Email: 'OU_MN_RAN_RD_VRF_ULM_4_53245007@internal.nsn.com'
...    Description: 5GC000795-H_B2 Intra-frequency Intra-DU PSCell change based on A3/A5 with SRB3, CBRA, successful


Library         taf.config.scf        WITH NAME    scf
Library         taf.config.wts        WITH NAME    wts_conf
Library         taf.gnb.oam.commissioning    WITH NAME    commission

Resource        ../../resources/SQD65/sqd65_keywords.robot
Resource        ../../resources/SQD65/sqd65_commissioning.robot
Resource        ../../5GC001926/ET/5GC001926_keywords.robot

Suite Setup      Run Keywords
...              Create Test Suite Log Folders                                            AND
...              ute_workarounds.Log TL Info as Metadata for UTE AP TL                    AND
...              5GC001926_keywords.Store Current SCF from gNB                            AND
...              Set Syslog Level in gNB swconfig                                         AND
...              Create CPlane Runtime File to gNB                                        AND
...              UTE Cloud Workaround                                                     AND
...              Delta Commissioning for 795-H-B2

*** Variables ***

${TC_SHORTNAME}  795-H-B2

@{IP_LIST}    10.0.1.131  10.0.1.132  10.0.1.133  10.0.1.134  10.0.1.135  10.0.1.136  10.0.1.137
...           10.0.1.121  10.0.1.122  10.0.1.123  10.0.1.124  10.0.1.125
...           10.0.1.12   10.0.1.102  10.0.1.103  10.0.1.104  10.0.1.105  10.0.1.106
&{plmn}=      mcc=311  mnc=489  mncLength=3

${UE_ID}      101

${ue_nr_capabilities_TDD}=  SEPARATOR=
...   ED007000479A4BBF5FFFFEF8001BD409A00CFDBFCB98AD7FFBF900001F53FFFFD1000000E77EF3FFF3FFFEC0001F78017FFE00002C7807E290401BFFEF0BFFEBC00E54D0015
...   8800000000023003CAA08
${ue_nr_capabilities_FDD}=  SEPARATOR=
...   e1201000014f5e0302c00201404820d9c4c3e140426c020ffcc31e50b03826010188a01014c200141f11b586368e9315047f2ca4d940220b64c1203063c63ff30c7942c0e07
...   0f0113804e0001083011b9343e01c8200000148200000548200000949280000d300f81b7953781b5bac0141000009652504000065949410000296525040000e594941000049
...   652524000154b29280ba07974ab2e81e4d2ac9a55915dc8020f00340201000000100


${ue_eutra_nr_capabilities_TDD}=  SEPARATOR=
...   BD1BA063058380713400000018062B000060400C1001830030600E268000010300C160801C4D000006060182C000389A00000C0C03058100713400001018060B0600E268000
...   02030048BC500C20002010080100257001004020080401008020100402008040100802010040200804010080201004020100402008040100800000040200804000000000004
...   0200000000000000004020080401008020100000008040100800000000000804000000000000000080401008020100402008040000002010040200804000000000000000080
...   4000000000000000000001009C00202008040080801010000000404008080000000000040400000000000000004020100401008020100402008040100802010040200804010
...   0802010040200808020100202000000080801010000000404000000000002020000000000010100402004040080800000020200404000000000002020040400000000000202
...   0000000000000000202700100802010040200000010080201000000080400000000000402000000000002010040200804000000201004020000001008000000000008040000
...   0000000401008020100402008040100802010040200804010080201004020080401008040100802010000000804010080000004020000001008000000402000000000002010
...   00000000001009C0020200404008080101002020000000808010100202000000000001010000000404008080101002020040400000010100202004040000000000020200000
...   0080801010020200404008080000002020040400808000000000004040000001008020100402008040100802010040200804010080201004020080401008020100402008040
...   1008040170010080101000000040400808000000000000000080800000000000000000000201002020000000808010100000000000000001010000000000000000000004020
...   0404000000101002020000000000000000202000000000000000000000804008080000002020040400808000000000004040000001010020200000000000000002020000000
...   809C40080180100300200600400C0080180100300200600400C0080180100300200600400C0080180100300200600400C0080180100300200600400C0080180100300200600
...   400C0080180100300200600400C0080180100300200600400C0080180100300200600400C0080180100300200600400C0080180100300200600400C00801801003002006004
...   00C0080180100300200600400C0080180100300200600400C008010800040202004008400040101002004
${ue_eutra_nr_capabilities_FDD}=  SEPARATOR=
...    B11BB02205818071180000011102C0C8388C0000048800803808C2F1002100008040401803080008020200C018

*** Test Cases ***

5GC000795_H_B2_Successful_CBRA_Intra_frequency_Intra_DU_PSCell_change_based_on_A3_A5_with_SRB3
    [Setup]    Perform Preconditions of Testcase
    Wait until the next Measurement Period starts
    Start Tcpdump on TestPc   options=-i eth3
    Send Egate Command and verify output   enb_param id=1 endc_capable_qci=all
    Attach UE to LTE   ue_id=${UE_ID}
    Add bearer   ue_id=${UE_ID}   bearer_id=7   filter_id=7
    Trigger LTE-NR dual connectivity for bearers  ue_id=${UE_ID}   bearer_id=2,7   target_gnb=2   target_cells=1   type=split_scg
    Start Data Traffic
    Get Average Data Rate
    Trigger intra-handover for CBRA
    Get Average Data Rate
    Stop Data Traffic
    Detach UE from LTE   ue_id=${UE_ID}
    Wait until the current Measurement Period stops
    Collect and verify PM counters
    [Teardown]    Perform Postconditions of Testcase

*** Keywords ***

Perform Preconditions of Testcase
    ${CELL_TECHNOLOGY}=        wts_ue.Get cellTechnology Info
    Set Suite Variable        ${CELL_TECHNOLOGY}
    Prepare WTS Config
    Bring Airphone TL to on Air status   cfg_file=basic_setup_${TC_SHORTNAME}.cfg
    Store Current WTS Config
    Create Testcase Log Directory


Perform Postconditions of Testcase
    ${log_dir}=       testline.Get Testcase Log Directory
    Send Egate Command and verify output    cmd=sim_log_set flush
    Copy File         ${tl.core.dir_path}/egate_console.log   ${log_dir}/egate_console.log
    Stop Tcpdump on TestPc   target_dir=${log_dir}
    IF   '${TEST_MODE}' == 'auto'
         Run Keyword and Warn on Failure    Set SCOUT TC ID for Reporting
         Collect sos report logs
    END


Suite Teardown for 795-H-B2
    Kill WTS services
    Run Keyword and Ignore Error    Check TL connectivity and PDU status
    Run Keyword and Ignore Error    5GC001926_keywords.Reload stored SCF


Prepare Delta Commissioning for 795-H-B2
    scf.load_scf      ${P_ORIG_SCF}

    Existing Parameter List to be updated
    Add NRREL to Cell        cell_id=1
    Add NRREL to Cell        cell_id=2
    Enable A3 Meas           cell_id=1
    Enable A3 Meas           cell_id=2

    ${tc_conf_dir}=          Get Test Suite Config Directory
    ${new_scf}=              Set Variable   ${tc_conf_dir}/scf_${TC_SHORTNAME}.xml
    ${delta_scf}=            Set Variable   ${tc_conf_dir}/delta_scf_${TC_SHORTNAME}.json
    scf.save_scf             ${new_scf}
    scf.calculate_delta_scf  ${new_scf}  ${P_ORIG_SCF}  ${delta_scf}

    RETURN    ${delta_scf}


Prepare WTS Config
    wts_conf.load_wts_cfg    file_path=${tl.core.dir_path}/basic_setup.cfg
    ${nia}=    wts_conf.get_parameter    set_ue id=1    nia
    ${nea}=    wts_conf.get_parameter    set_ue id=1    nea
    wts_conf.modify          set_ue id=${UE_ID}    nea=${nea} nia=${nia}
    wts_conf.modify          ue_param id=${UE_ID}
    ...    ue_nr_capabilities=${ue_nr_capabilities_${CELL_TECHNOLOGY}} ue_eutra_nr_capabilities=${ue_eutra_nr_capabilities_${CELL_TECHNOLOGY}}
    wts_conf.insert          set_bearer id=7 ue=${UE_ID} qci=7  after  set_bearer id=2 ue=${UE_ID}
    wts_conf.save_wts_cfg    file_path=${tl.core.dir_path}/basic_setup_${TC_SHORTNAME}.cfg


Existing Parameter List to be updated
    scf.modify_scf_element  value=true  dist_name=NRBTS-1                  p_name=actMultiDrbNSA
    scf.modify_scf_element  value=true  dist_name=NRBTS-1                  p_name=actIntraFreqIntraGnbMobilityNSA
    scf.modify_scf_element  value=true  dist_name=NRBTS-1                  p_name=srb3SupportEnabled
    scf.modify_scf_element  value=5min  dist_name=MNL-1/MNLENT-1/PMCADM-1  p_name=reportingIntervalPm
    scf.modify_scf_element  value=5min  dist_name=NRBTS-1/NRPMRNL-1        p_name=miNrPsCellChange


Trigger intra-handover for CBRA
    Send Egate Command and verify output   ue_meas_cfg_disp id=${UE_ID}
    ${cmd}    Catenate    ue_measurement_send_nr id=${UE_ID} meas_id=1 event=A3 srsrp_nr=11 srsrq_nr=11 phycell_id=51 nrsrp_nr=30 nrsrq_nr=30
    ...   rs_type=ssb index=0 nrs_result=30:20:59
    Send Egate Command and verify output   cmd=${cmd}   pass_regexp=reported successful RA
    Sleep   3s


Get Average Data Rate
    Get Average Data Rate via Egate    ue_id=${UE_ID}    id=2    dir=dl    trf_id=1
    Get Average Data Rate via Egate    ue_id=${UE_ID}    id=2    dir=ul    trf_id=1
    Get Average Data Rate via Egate    ue_id=${UE_ID}    id=7    dir=dl    trf_id=1
    Get Average Data Rate via Egate    ue_id=${UE_ID}    id=7    dir=ul    trf_id=1


Start Data Traffic
    Start data traffic in egate   ue_id=${UE_ID}   direction=dl   trf_id=1   id=2   mbps=1
    Start data traffic in egate   ue_id=${UE_ID}   direction=ul   trf_id=1   id=2   mbps=1
    Start data traffic in egate   ue_id=${UE_ID}   direction=dl   trf_id=2   id=7   mbps=1
    Start data traffic in egate   ue_id=${UE_ID}   direction=ul   trf_id=2   id=7   mbps=1


Stop Data Traffic
    Stop data traffic in egate   ue_id=${UE_ID}   direction=dl   trf_id=1   id=2
    Stop data traffic in egate   ue_id=${UE_ID}   direction=ul   trf_id=1   id=2
    Stop data traffic in egate   ue_id=${UE_ID}   direction=dl   trf_id=2   id=7
    Stop data traffic in egate   ue_id=${UE_ID}   direction=ul   trf_id=2   id=7


Collect and verify PM counters
    [Documentation]
    ...    This keyword collects and verifies the PM counters M55120C01002 and M55120C00501
    ...    M55120C01002 INTRA_DU_HO_ATT_NSA_SRB3 is the number of intra gNB intra frequency intra DU PS-Cell change attempts for NSA 3x via SRB3
    ...    M55120C00501 INT_FR_PSCEL_CHA_ATT_SRB3  indicates the number of intra gNB intra frequency PS-Cell change attempts
    ...    when NR RRC Reconfiguration is sent via NSA NR SRB3
    @{counters}     Create List
    ...             M55120C01002  ==  1  INTRA_DU_HO_ATT_NSA_SRB3
    ...             M55120C00501  ==  1  INT_FR_PSCEL_CHA_ATT_SRB3
    ${PM_dir}=    Collect PM Counter
    Verify PM Counter Reference Table    reference_table=${counters}      pm_dir=${PM_dir}   distname_suffix=NRBTS-1/NRCELL-1

Add NRREL to Cell
    [Arguments]      ${cell_id}=1
    ${dist_name}=    Set Variable    NRBTS-1/NRCELL-${cell_id}/NRREL-1
    ${mo_exist}=    scf.is_object_in_scf    dist_name=${dist_name}
    IF    ${mo_exist}   RETURN
    ${nrrel.lcrId}=  Set Variable If    '${cell_id}' == '1'    2    1
    scf.add_object_to_scf     class_name=NRREL          dist_name=${dist_name}                version=NRBTSCL5G21B_2104_100
    scf.add_element_to_scf    dist_name=${dist_name}    p_name=cellIndividualSsbRsrpOffset    value=0dB
    scf.add_element_to_scf    dist_name=${dist_name}    p_name=cellIndividualSsbRsrqOffset    value=0dB
    scf.add_element_to_scf    dist_name=${dist_name}    p_name=gNbId                          value=1
    scf.add_element_to_scf    dist_name=${dist_name}    p_name=gNbIdLength                    value=22
    scf.add_element_to_scf    dist_name=${dist_name}    p_name=handoverAllowedSA              value=allowed
    scf.add_element_to_scf    dist_name=${dist_name}    p_name=lcrId                          value=${nrrel.lcrId}
    scf.add_element_to_scf    dist_name=${dist_name}    p_name=removeNotAllowed               value=false
    scf.add_list_to_scf       dist_name=${dist_name}    list_name=gnbPlmn
    scf.add_item_to_list      dist_name=${dist_name}    list_name=gnbPlmn                     elements=${plmn}
    scf.add_element_to_scf    dist_name=${dist_name}    p_name=nrDcAllowed    value=false
    scf.add_element_to_scf    dist_name=${dist_name}    p_name=handoverAllowedSARedCap  value=forbidden
    scf.add_element_to_scf    dist_name=${dist_name}    p_name=isRplCellForPSCell            value=false


Enable A3 Meas
    [Arguments]      ${cell_id}=1
    ${list_name}=             Set Variable    a3MeasSsbRsrq
    ${dist_name}=             Set Variable    NRBTS-1/NRCELL-${cell_id}

    scf.modify_scf_element    dist_name=${dist_name}   p_name=a3MeasEnabled                    value=rsrq
    scf.add_element_to_scf    dist_name=${dist_name}   p_name=absThreshSsbRsrqConsolidation    value=1

    ${list_exist}=            scf.is_list_in_object  dist_name=${dist_name}  list_name=${list_name}
    IF    ${list_exist}       RETURN

    scf.add_list_to_scf       dist_name=${dist_name}    list_name=${list_name}
    ${a3MeasSsbRsrq_dict}     Create dictionary
    ...                       a3HysteresisSsbRsrq  0
    ...                       a3OffsetSsbRsrq  6
    ...                       a3TimeToTriggerSsbRsrq  ms480
    scf.add_item_to_list      dist_name=${dist_name}   list_name=${list_name}    elements=${a3MeasSsbRsrq_dict}


Delta Commissioning for 795-H-B2
    [Documentation]    :Author: G. Sankaran and L. Medico
    ...    what this delta commissioning will do
    ...    most probably to be modified below scf_precondition_tc10.xml
    ${delta_scf}=            Prepare Delta Commissioning for 795-H-B2
    ${delta_size}=           Get File Size  ${delta_scf}
    IF  ${delta_size} <= 2   RETURN

    Log To Console    Perform delta commissioning...
    admin.Setup Admin    alias=cOAM
    admin.Perform Delta Recommissioning
    ...    delta_file=${delta_scf}
    ...    skip_parameter_relation_errors=True
    ...    should_activate=True
    ...    timeout=300
    ...    alias=cOAM
    [Teardown]    Run Keyword And Ignore Error    admin.Teardown Admin    alias=cOAM
