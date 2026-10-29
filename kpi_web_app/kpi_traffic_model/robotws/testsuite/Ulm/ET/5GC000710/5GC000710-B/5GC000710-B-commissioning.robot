*** Settings ***
Documentation   This is a keyword file for 5GC000710-B, part commissioning
...             Team: 'MN RAN L3 SW ULM L3NRT 07 SG 60'
...             Author: Sylvia Schneider
#-------------------------------------------------------------------------------------------------------------

*** Keywords ***

set sw release version
    [Documentation]    [PRIVATE]    set sw release version from gnb sw version
    ...       :Autor: Sylvia Schneider
    @{gnb_sw_version_parts}   split string    ${gnb_swVersion}    _
    set suite variable    ${release}   ${gnb_sw_version_parts}[0]


Update SCF
    [Documentation]    [PRIVATE]    update SCF
    ...       :Autor: Sylvia Schneider
    set sw release version
    Log To Console    \nupdate SCF and store in ${resultBaseDir}/SCFC_710B.xml
    ${xml}    parse xml    ${resultBaseDir}/SCFC_start.xml
    set suite variable    ${xml}
    FOR      ${param}             ${value}   IN
       ...   actIntraFreqHoSA     true
       ...   actRfspIndex         true
       ...   miNrRelReportCu      15min
       ...   actIncXn             true
       Log To Console    set param "${param}" to value "${value}"
       Set Element Text   ${xml}    text=${value}         xpath=.//p[@name="${param}"]
    END

    FOR   ${nrcell_id}   IN    3   4
       Log To Console    set param a3MeasEnabled for ${bts_distName}/NRCELL-${nrcell_id} to value "rsrp"
       Set Element Text   ${xml}   text=rsrp     xpath=.//managedObject[@distName="${bts_distName}/NRCELL-${nrcell_id}"]/p[@name="a3MeasEnabled"]
    END

    ${timerXnDataFwdGuard}    set variable    <p name="timerXnDataFwdGuard">250</p>
    Add Element        ${xml}     ${timerXnDataFwdGuard}   xpath=.//managedObject[@distName="${bts_distName}"]

    FOR   ${obj}   IN
    ...    NRREL
    ...    NRADJGNB-1
    ...    NRADJNRCELL-1
    ...    XNLINK
       run keyword    Create ${obj}
    END

    Save xml     ${xml}    ${resultBaseDir}/SCFC_710B.xml


activate SCF and bring tl onAir
    [Documentation]    [PRIVATE]    activate SCF and bring tl onAir
    ...       :Autor: Sylvia Schneider
    Kill WTS services
    ${oam_alias}    connect.Setup OAM http session    node_type=gnb  node_id=${0}
    Log To Console    activate ${resultBaseDir}/SCFC_710B.xml started
    admin.perform commissioning
    ...    scf_file=${resultBaseDir}/SCFC_710B.xml
    ...    skip_parameter_relation_errors=True
    ...    timeout=660
    ...    connection=${oam_alias}
    Log To Console    activate ${resultBaseDir}/SCFC_710B.xml finished
    Run Keyword and Ignore Error    connect.Teardown OAM http session    node_type=gnb  node_id=${0}
    Wait until all DUs up
    check all radio units online
    start wireshark trace
    Log To Console    start to bring tl on air without reboot
    Bring Airphone TL to on Air status without reboot
    stop wireshark trace and verify successful xn setup
    check wts in active state
    Log To Console    save final scf ${resultDir}/SCF_final.xml
    get scf coam   ${resultDir}    SCF_final.xml


Create NRREL
    [Documentation]    [PRIVATE]    create NRREL object in SCF
    ...       :Autor: Sylvia Schneider
    Log To Console    \nBuilding object ${bts_distName}/NRCELL-3/NRREL-1
    ${NRREL}   set variable   <managedObject class="NRREL" distName="${bts_distName}/NRCELL-3/NRREL-1"
    ${NRREL}   Catenate     SEPARATOR=${SPACE}   ${NRREL}   version="${SCF.version}" operation="create">
    FOR     ${line}   IN
           ...    <p name="cellIndividualSsbRsrpOffset">-2dB</p>
           ...    <p name="cellIndividualSsbRsrqOffset">-2dB</p>
           ...    <p name="gNbId">38</p>
           ...    <p name="gNbIdLength">22</p>
           ...    <p name="handoverAllowedSA">allowed</p>
           ...    <p name="handoverAllowedSARedCap">forbidden</p>
           ...    <p name="isRplCellForPSCell">false</p>
           ...    <p name="lcrId">1</p>
           ...    <p name="nrDcAllowed">false</p>
           ...    <p name="removeNotAllowed">false</p>
           ...    <list name="gnbPlmn">
           ...    <item>
           ...    <p name="mcc">${SCF.mcc}</p>
           ...    <p name="mnc">${SCF.mnc}</p>
           ...    <p name="mncLength">${SCF.mnclenght}</p>
           ...    </item>
           ...    </list>
           ...    </managedObject>
           ${NRREL}   Catenate     SEPARATOR=\n         ${NRREL}   ${line}
    END
    Add Element     ${xml}     ${NRREL}         xpath=.//cmData


Create NRADJGNB-1
    [Documentation]    [PRIVATE]    create NRADJGNB object in SCF
    ...       :Autor: Sylvia Schneider
     Log To Console    Building object ${bts_distName}/NRADJGNB-0
    ${NRADJGNB}    set variable  <managedObject class="NRADJGNB" distName="${bts_distName}/NRADJGNB-1"
    ${NRADJGNB}   Catenate     SEPARATOR=${SPACE}   ${NRADJGNB}    version="${SCF.version}" operation="create">
    FOR     ${line}   IN
           ...    <p name="administrativeState">Unlocked</p>
           ...    <p name="gNbIdLength">22</p>
           ...    <p name="gNodeBId">38</p>
           ...    <p name="gNodeBIdCtrl">oamControlled</p>
           ...    <p name="xnLinkRef">1</p>
           ...    <list name="gnbPlmn">
           ...    <item>
           ...    <p name="mcc">${SCF.mcc}</p>
           ...    <p name="mnc">${SCF.mnc}</p>
           ...    <p name="mncLength">${SCF.mnclenght}</p>
           ...    </item>
           ...    </list>
           ...    </managedObject>
           ${NRADJGNB}   Catenate     SEPARATOR=\n         ${NRADJGNB}   ${line}
    END
    Add Element     ${xml}     ${NRADJGNB}      xpath=.//cmData


Create NRADJNRCELL-1
    [Documentation]    [PRIVATE]    create NRADJNRCELL object in SCF
    ...       :Autor: Sylvia Schneider
    Log To Console    Building object ${bts_distName}/NRADJNRCELL-1
    ${NRADJNRCELL}    set variable   <managedObject class="NRADJNRCELL" distName="${bts_distName}/NRADJNRCELL-1"
    ${NRADJNRCELL}   Catenate     SEPARATOR=${SPACE}   ${NRADJNRCELL}    version="${SCF.version}" operation="create">
    FOR     ${line}   IN
           ...    <p name="cellDepType">SA</p>
           ...    <p name="cellReservedForOperatorUse">notReserved</p>
           ...    <p name="fiveGsTac">${SCF.fiveGsTac}</p>
           ...    <p name="freqBandIndicatorNR">71</p>
           ...    <p name="gNbId">38</p>
           ...    <p name="gNbIdLength">22</p>
           ...    <p name="lcrId">1</p>
           ...    <p name="nrarfcn">${SCF.nrarfcnDl}</p>
           ...    <p name="physCellId">48</p>
           ...    <p name="ssbFrequency">126530</p>
           ...    <list name="gnbPlmn">
           ...    <item>
           ...    <p name="mcc">${SCF.mcc}</p>
           ...    <p name="mnc">${SCF.mnc}</p>
           ...    <p name="mncLength">${SCF.mnclenght}</p>
           ...    </item>
           ...    </list>
           ...    </managedObject>
           ${NRADJNRCELL}   Catenate     SEPARATOR=\n         ${NRADJNRCELL}   ${line}
    END
    Add Element     ${xml}     ${NRADJNRCELL}   xpath=.//cmData


Create XNLINK
    [Documentation]    [PRIVATE]    create XNLINK object in SCF
    ...       :Autor: Sylvia Schneider
    Log To Console    Building object ${bts_distName}/XNLINK-1
    ${new_obj}    set variable   <managedObject class="XNLINK" distName="${bts_distName}/XNLINK-1"
    ${new_obj}   Catenate     SEPARATOR=${SPACE}   ${new_obj}    version="${SCF.version}" operation="create">
    FOR     ${line}   IN
           ...    <p name="cPlaneIpAddr">10.0.1.3</p>
           ...    <p name="cPlaneIpAddrCtrl">oamControlled</p>
           ...    </managedObject>
           ${new_obj}   Catenate     SEPARATOR=\n         ${new_obj}   ${line}
    END
    Add Element     ${xml}     ${new_obj}   xpath=.//cmData
