*** Settings ***
Documentation   This is a keyword file for 5GC000710-B, part verification
...             Team: 'MN RAN L3 SW ULM L3NRT 07 SG'
...             Author: Sylvia Schneider
#-------------------------------------------------------------------------------------------------------------

*** Variables ***
${xnap_version}     xnap

${filter_intialContextSetupRequest}   ngap.procedureCode == 14
${filter_UEContextModification}       ngap.procedureCode == 40
${filter_handover}                    ${xnap_version}.procedureCode==0
${filter_NAS_authentication_request}  nas_5gs.mm.message_type == 0x56
${filter_NAS_security_mode}           nas_5gs.security_header_type == 3
${filter_NAS}                         (ngap.procedureCode == 4) && (ngap.id == 0)
${filter_NAS_configuration_update}    nas_5gs.mm.message_type == 0x54

${xpath_setup_modify_config_NASdl}      .//field[@name="ngap.IndexToRFSP"]
${successfulOutcome_setup_modify}       .//field[@name="ngap.successfulOutcome_element"]
${xpath_handover}                       .//field[@name="${xnap_version}.indexToRatFrequencySelectionPriority"]


*** Keywords ***
verify successful xn setup
    [Documentation]    [PRIVATE]    verify that xn setup is successful
    ...       :Autor: Sylvia Schneider
    [Arguments]     ${wireshark_store}
    setup tshark    eth1
    Log To Console    filter successful XNSetupResponse message
    read_pcap_and_save_to_file
    ...   filename=${resultDir}/XN_setup.xml
    ...   packet_filter=${xnap_version}
    ...   output_type=pdml
    ...   pcap_file_path=${wireshark_store}
    teardown tshark
    ${pdml_xml}    parse xml    ${resultDir}/XN_setup.xml

    ${successful_msg}    Get Element Count      ${pdml_xml}
    ...    xpath=.//field[@name="${xnap_version}.successfulOutcome_element"]
    Should Not Be Equal As Integers    ${successful_msg}    ${0}
    ...     NO successful XNSetupResponse message


verify wireshark initialContextSetup and handover
    [Documentation]    [PRIVATE]    verify initialContextSetup and handover request in wireshark
    ...       :Autor: Sylvia Schneider
    Log To Console    \nverify initialContextSetup
    setup tshark    eth1
    Log To Console    create xml file with filter "${filter_intialContextSetupRequest}"
    read_pcap_and_save_to_file
    ...   filename=${resultDir}/X2_setup.xml
    ...   packet_filter=${filter_intialContextSetupRequest}
    ...   output_type=pdml
    ...   pcap_file_path=${resultDir}/wireshark.pcap
    teardown tshark
    ${pdml_xml}    parse xml    ${resultDir}/X2_setup.xml
    Log To Console    verify that ${xpath_setup_modify_config_NASdl} contains 99
    Run Keyword And Continue On Failure   Element Attribute should match    ${pdml_xml}
    ...    show
    ...    99
    ...    xpath=${xpath_setup_modify_config_NASdl}
    verify successful acknowledge    ${pdml_xml}
    verify 3 handover IndexToRFSP 99


verify wireshark UEContextModification
    [Documentation]    [PRIVATE]    verify UEContextModification in wireshark
    ...       :Autor: Sylvia Schneider
    Log To Console    \nverify UEContextModification
    setup tshark    eth1
    Log To Console    create xml file with filter "${filter_UEContextModification}"
    read_pcap_and_save_to_file
    ...   filename=${resultDir}/X2_modify.xml
    ...   packet_filter=${filter_UEContextModification}
    ...   output_type=pdml
    ...   pcap_file_path=${resultDir}/wireshark.pcap
    teardown tshark
    ${pdml_xml}    parse xml    ${resultDir}/X2_modify.xml
    Run Keyword And Continue On Failure   Element Attribute should match    ${pdml_xml}
    ...    show
    ...    77
    ...    xpath=${xpath_setup_modify_config_NASdl}
    verify successful acknowledge    ${pdml_xml}
    verify handover IndexToRFSP 77


verify wireshark NAS dl
    [Documentation]    [PRIVATE]    verify NAS DL in wireshark
    ...       :Autor: Sylvia Schneider
    Log To Console    \nverify NAS DL
    setup tshark    eth1
    Log To Console    create xml file with filter "${filter_NAS_authentication_request}" message NAS authentication request
    read_pcap_and_save_to_file
    ...   filename=${resultDir}/X2_NASauth.xml
    ...   packet_filter=${filter_NAS_authentication_request}
    ...   output_type=pdml
    ...   pcap_file_path=${resultDir}/wireshark.pcap
    ${pdml_xml}    parse xml    ${resultDir}/X2_NASauth.xml
    Log To Console    verify no element ${xpath_setup_modify_config_NASdl} contained
    Run Keyword And Continue On Failure   Element Should Not Exist    ${pdml_xml}
    ...    xpath=${xpath_setup_modify_config_NASdl}
    ...    message=Error NAS authentication request contains IndexToRFSP

    Log To Console    create xml file with filter "${filter_NAS_security_mode}" message NAS security mode
    read_pcap_and_save_to_file
    ...   filename=${resultDir}/X2_NASsec.xml
    ...   packet_filter=${filter_NAS_security_mode}
    ...   output_type=pdml
    ...   pcap_file_path=${resultDir}/wireshark.pcap
    ${pdml_xml}    parse xml    ${resultDir}/X2_NASsec.xml
    Log To Console    verify no element ${xpath_setup_modify_config_NASdl} contained
    Run Keyword And Continue On Failure   Element Should Not Exist    ${pdml_xml}
    ...    xpath=${xpath_setup_modify_config_NASdl}
    ...    message=Error NAS security mode contains IndexToRFSP

    Log To Console    create xml file with filter "${filter_NAS}" message NAS
    read_pcap_and_save_to_file
    ...   filename=${resultDir}/X2_NAS.xml
    ...   packet_filter=${filter_NAS}
    ...   output_type=pdml
    ...   pcap_file_path=${resultDir}/wireshark.pcap
    ${pdml_xml}    parse xml    ${resultDir}/X2_NAS.xml
    Log To Console    verify no element ${xpath_setup_modify_config_NASdl} contained
    Run Keyword And Continue On Failure   Element Should Not Exist    ${pdml_xml}
    ...    xpath=${xpath_setup_modify_config_NASdl}
    ...    message=Error NAS message contains IndexToRFSP

    Log To Console    create xml file with filter "${filter_NAS_configuration_update}" message NAS configuration update
    read_pcap_and_save_to_file
    ...   filename=${resultDir}/X2_NAS_config.xml
    ...   packet_filter=${filter_NAS_configuration_update}
    ...   output_type=pdml
    ...   pcap_file_path=${resultDir}/wireshark.pcap
    ${pdml_xml}    parse xml    ${resultDir}/X2_NAS_config.xml
    Log To Console    verify element ${xpath_setup_modify_config_NASdl} contained with value 88
    Run Keyword And Continue On Failure   Element Attribute should match    ${pdml_xml}
    ...    show
    ...    88
    ...    xpath=${xpath_setup_modify_config_NASdl}
    teardown tshark
    verify handover IndexToRFSP 88
    verify initial context setup request contains no IndexToRFSP

verify successful acknowledge
    [Documentation]    [PRIVATE]    verify successful handover in wireshark
    ...       :Autor: Sylvia Schneider
    [Arguments]    ${pdml_xml}
    Log To Console    verify that successful outcome message present
    Run Keyword And Continue On Failure   Element Attribute should match    ${pdml_xml}
    ...    showname
    ...    successfulOutcome
    ...    xpath=${successfulOutcome_setup_modify}


verify handover IndexToRFSP ${value_IndexToRFSP}
    [Documentation]    [PRIVATE]    verify IndexToRFSP in handover message in wireshark
    ...       :Autor: Sylvia Schneider
    Log To Console    verify handoverRequest
    setup tshark    eth1
    Log To Console    create xml file with filter "${filter_handover}"
    read_pcap_and_save_to_file
    ...   filename=${resultDir}/X2_handover.xml
    ...   packet_filter=${filter_handover}
    ...   output_type=pdml
    ...   pcap_file_path=${resultDir}/wireshark.pcap
    ${pdml_xml}    parse xml    ${resultDir}/X2_handover.xml
    Log To Console    verify that ${xpath_handover} contains ${value_IndexToRFSP}
    Run Keyword And Continue On Failure   Element Attribute should match    ${pdml_xml}
    ...    show
    ...    ${value_IndexToRFSP}
    ...    xpath=${xpath_handover}
    [Teardown]    teardown tshark


verify 3 handover IndexToRFSP ${value_IndexToRFSP}
    [Documentation]    [PRIVATE]    verify IndexToRFSP in handover message in wireshark
    ...       :Autor: Sylvia Schneider
    ${filter_handoverReq_RFSP}    set variable
    ...    (${xnap_version}.procedureCode==0) && (${xnap_version}.indexToRatFrequencySelectionPriority == ${value_IndexToRFSP})
    Log To Console    verify handoverRequest
    setup tshark    eth1
    Log To Console    create xml file with filter "${filter_handoverReq_RFSP}"
    read_pcap_and_save_to_file
    ...   filename=${resultDir}/X2_handover.xml
    ...   packet_filter=${filter_handoverReq_RFSP}
    ...   output_type=pdml
    ...   pcap_file_path=${resultDir}/wireshark.pcap
    ${pdml_xml}    parse xml    ${resultDir}/X2_handover.xml
    Log to console    verify 3 HandoverRequest messages present
    ${numberOfHOReq}    Get Element Count      ${pdml_xml}
    ...    xpath=.//field[@name="${xnap_version}.HandoverRequest_element"][@showname="HandoverRequest"]
    Run Keyword And Continue On Failure   Should Be Equal    ${numberOfHOReq}    ${3}
    ...     Wrong number of HandoverRequest messages with (${xnap_version}.indexToRatFrequencySelectionPriority==${value_IndexToRFSP})
    [Teardown]    teardown tshark


verify initial context setup request contains no IndexToRFSP
    [Documentation]    [PRIVATE]    verify that there is no IndexToRFSP in initial context setup request message in wireshark
    ...       :Autor: Sylvia Schneider
    Log To Console    inital context setup request contains no IndexToRFSP
    setup tshark    eth1
    Log To Console    create xml file with filter "${filter_intialContextSetupRequest}"
    read_pcap_and_save_to_file
    ...   filename=${resultDir}/X2_noIndexToRFSP.xml
    ...   packet_filter=${filter_intialContextSetupRequest}
    ...   output_type=pdml
    ...   pcap_file_path=${resultDir}/wireshark.pcap
    ${pdml_xml}    parse xml    ${resultDir}/X2_noIndexToRFSP.xml
    Log To Console    verify no element ${xpath_setup_modify_config_NASdl} contained
    Run Keyword And Continue On Failure   Element Should Not Exist    ${pdml_xml}
    ...    xpath=${xpath_setup_modify_config_NASdl}
    ...    message=Error inital context setup request contains IndexToRFSP
    [Teardown]    teardown tshark

