*** Settings ***
Documentation     [SUITE PURPOSE]  TCs and KWs of CB012733 step A
...               Test Case Scenario author   : axel.gouilly-frossard@nokia.com
...               Test Case Scenario contact  : axel.gouilly-frossard@nokia.com
...               Test Case automation author : axel.gouilly-frossard@nokia.com
...               Test Case automation contact: axel.gouilly-frossard@nokia.com
...               Creation Date               : 1-february-2026
...               Last Modified by            :
...               Modification:
...                       1-february-2026   | Creation
...

Library            taf.sbts.oam.coam.admin             WITH NAME      sbts_coam
Library            ../../../../resources/SWENG/python/CoamParameter.py      WITH NAME     coam_parameter

Library            taf.wts.runner                          WITH NAME    wtsemu
Library            Dialogs

Resource          ../../../../resources/SWENG/robot/Connect.robot
Resource          ../../../../resources/SWENG/robot/GenericTest.robot
Resource          ../../../../resources/SWENG/robot/Traffic.robot
Resource          ../../../../resources/SWENG/robot/KPIs.robot

Resource          ../../resources/common/TtiTrace/ttitrace.robot
Resource          ../../../../resources/SWENG/robot/TtiConvertInterface.robot
Resource          ../../../../resources/SWENG/robot/TtiAnalysisInterface.robot


*** Variables ***

${path_to_json}                      /home/ute/Downloads/TTI.json    # internal usage for decoding TTI pcap
${gnb_alias}                         gnb_under_test

${CB012733_constraints}          testsuite/Paris/RRM/ET/CB012733/config/CB012733_constraints.csv

${gp_duration}                       300

${egatelogoutput}       ${True}


*** Keywords ***

CB012733 Setup With Custom Config
    [Documentation]
    ...     Actions:     Apply customized configuration then launch cell setup.
    ...     Parameters:  SCF: customized SCF
    ...                  CFG: customized basic CFG file
    ...                  IPHY: airphone iphy file
    ...                  rdParam: list of RAD parameters
    ...                  vendorParam: list of vendor parameters
    ...     Return:      None
    [Arguments]              ${SCF}    ${CFG}=${EMPTY}
    # ...                      ${IPHY}=${EMPTY}     ${rdParam}=${EMPTY}    ${vendorParam}=${EMPTY}

    setup.Apply Custom Config
    ...      scfc=${SCF}
    ...      cfg=${CFG}
    # ...      iphy=${IPHY}
    # ...      rad_params=@{rdParam}
    # ...      vendor_params=@{vendorParam}

CB012733 Configuration SCF Delta
    [Documentation]               Dedicated KW to add use a delta commissioning file
    ...                           configure cell2 with specific parameters for CB012733-A test case

    [Arguments]                   ${12733_delta_file}     ${gnb_alias}

    # Open connection towards cOAM
    sbts_coam.connect_to          name=${gnb_alias}

    Dated Log New Line            delta_file=${12733_delta_file}
    # Apply delta scf
    coam_parameter.perform_scf_delta_commission
    ...                           delta_file=${12733_delta_file}
    ...                           connection=${gnb_alias}

    OAM wait available
    sbts_coam.teardown            connection=${gnb_alias}

CB012733 Test Teardown

   # Disable traffic control drop mode before leaving test
   # SSH Connect and Cmd     command=sudo tc qdisc del dev eth3 root netem            host=${HOST_EPCSIM}

    setup.Suite Teardown

CB12733_LaunchWTS
    [Arguments]            ${luafile}

    Dated Log              Starting LaunchWTS
    ${alias}               SSH Wait For Connect                    host=${HOST_EPCSIM}
    # WTS Clear              #Stop WTSEmu, kill eDaemon and eGate processes, and purge WTS logs  toomuch already done on Restart.Restart TL
    WTS Start processes    telnet_egate_addr=${tl.core.default_ssh_connection_details.addr}

    Dated Log              LaunchWTS cfg file= ${luafile}
    wtsemu.sim_cfg         file=${luafile}
    ...                    entry=run_configuration(3600)
    Dated Log              LaunchWTS Waiting CHANGE STATE: ACTIVE - SimMode is ready now
    Flush Egate Console Buffer    # Flush the buffer to be sure to have all egate console log
    wtsemu.Read Wtsemu Output Until Re
	...                    expected=CHANGE STATE: ACTIVE - SimMode is ready now
	...                    timeout=300
	sleep                  30s

CB012733_A_Feature_activation_static

    [Documentation]     The purpose of this test case is to perform a basic check for feature actThreeSymbolPdcch
    ...                 with a simple configuration of Cell2 with 40MHz BW and 50 UEs, and to validate the workflow
    ...                 of capturing and analyzing TTI traces in CB012733 test case.


    Init Sequence           "CB012733_A_Feature_activation_static"

    # Dated Log New Line              ---> Restart TL
    # Critical Step               Restart TL

    Dated Log New Line              ---> WTS setup SA
    Critical Step          CB12733_LaunchWTS        luafile=${basic_cf_12733}

    Critical Step          CB012733 Check MIB SIB

    sleep                  20s

    Critical step            CB012733 LaunchTraffic

    Step                     CB012733 start TTI Capture       suffix=DL_UL
    Traced Sleep             duration=3s                      msg=start DL UL traffic TTI capture...
    Step                     CB012733 stop TTI Capture        suffix=DL_UL_Traffic
    Traced Sleep             duration=30s                     msg=stop TTI waiting for 60seconds
	Step                     CB012733 TTI Post Processing   	TTIpcap=${TTIpcap}
    Step                     CB012733 Format and check TTI Trace
    Step                     CB012733 Format TTI Trace Combined DL UL   ${TTIcsv_decoded}

    ${zoi}                          ZOI Start
    ${zoi_end_remain}=              ZOI Remaining Sec           ${zoi}
    ${start_loop_remaining}=        Evaluate                    ${zoi_end_remain} - ${GP_DEF}


        # To be sure to have a GP fully filled with the same events inside every loop and avoid changing KPIs/counters:
        # If ZOI start is T0, ZOI end is T0 + ${GUARD_DELAY_DEF} + ${GP_DEF} + ${PM_AVAIL_DELAY_DEF}
        # So, test is started at the beginning of the GP before ZOI end, so:
        # ZOI End - ${GP_DEF}
        # Ex. 1: ZOI start is 10h02 => ZOI End is 10h02 + 40s (GUARD_DELAY_DEF) + 1 GP + 1 mn (PM_AVAIL_DELAY_DEF)
        #        => Time for next GP for ZOI End is 10h11, so test is started at 10h06 and KPIs retrieved at 10h11
        # Ex. 2: ZOI start is 10h14:40s => ZOI End is 10h14:40 + 40s (GUARD_DELAY_DEF) + 1 GP + 1 mn (PM_AVAIL_DELAY_DEF)
        #        => Time for next GP for ZOI End is 10h26 as gaurd delay excedd thenext GP frontier,
        #        so test is started at 10h21 and KPIs retrieved at 10h26
        # And, test duration must not exceed 1 GP - 1 mn per loop

    Traced Sleep                    ${start_loop_remaining} seconds
    ...                             msg=before starting scenario

    Dated Log New Line              **** Waiting for end of ZOI ****
    ZOI Wait End                     zoi=${zoi}

    ${pm_path}                      Counters.Collect PM files from BTS    ${LOG_PATH}/PM
    Step                            KPI Evaluate                    pmFile=${pm_path}
    ...                             constraintsFile=${CB012733_constraints}
    ...                             failOnError=${True}

    [Teardown]               Display diagnosis

CB012733 Check MIB SIB
    Dated Log              Waiting MIB-SIB
    wtsemu.script          file=${CURDIR}/../config/custom/multi_ue_sa_script_new.lua
    ...                    entry=check_CellSetup(1,4)
    Dated Log              Checking SIBs
    # Flush Egate Console Buffer    # Flush the buffer to be sure to have all egate console log
    # wtsemu.Read Wtsemu Output Until Re
	# ...                    expected= Cell Setup Check Script Complet
	# ...                    timeout=300

    FOR    ${cid}  IN RANGE    1    5
            Dated Log      AEP Waiting Cell Setup Check Script Completion CellSetup(${cid})
            Run Keyword    wtsemu.Read Wtsemu Output Until Re
             ...            expected=Cell Setup for${cid}: Cell Setup Found    timeout=60
    END


CB012733 LaunchTraffic
    [Documentation]
    ...         Actions : Launch basic traffic with DTX
    ...         Params :  none
    ...         Return :  none
    [Arguments]
    CB012733_run_script_once     ${CURDIR}/../config/custom/eGate_macros_2.lua entry=run_test_50Ue_CELL2

CB012733_run_script_once
    [Documentation]        This KW start on egate command a script file=<path><file.sce> to perform egate commande
    ...                    recorded on a .sce file

    [Arguments]                    ${script_path_name}
    Dated Log                      Script sce used: ${script_path_name}

    wtsemu.script                  file=${script_path_name}
    ${output}                      wtsemu.read_wtsemu_output_until    PROCESSING    600
    Run Keyword If                ${egatelogoutput}    Dated Log                  output:${output}
    ${output}                      wtsemu.read_wtsemu_output_until_prompt    5
    Run Keyword If                ${egatelogoutput}    Dated Log                  output:${output}
    ${script_status}               wait until keyword succeeds    12hours    1s    CB012733_is_script_finished
    ${error_in_status}=            Run Keyword And Return Status    Should Contain    ${script_status}    error
    Dated Log                      output:${error_in_status}

CB012733_is_script_finished
    [Documentation]        This KW is a part of CB012733_run_script_once

    wtsemu.script_status
    ${output}                      wtsemu.read_wtsemu_output_until    ALL UE REGISTERED ON CELL2    600
    Run Keyword If                ${egatelogoutput}    Dated Log                  output:${output}
    ${script_status}               wtsemu.read_wtsemu_output_until_prompt    5
    # ${log_string}          remove string using regexp    ${script_status}    (=|-| {6,}|\n)
    # ${log_string}          replace string   ${log_string}    description    description${\n}${SPACE}
    # ${log_string}          catenate    Script status:${\n}    ${log_string}
    # Dated Log              ${log_string}    first=True
    should not match regexp        ${script_status}    ( active | paused )
    [Return]

CB012733 start TTI Capture
    [Arguments]            ${suffix}=${EMPTY}
    # TTI capture configuration
    ${TTIdir}              Get TTI Trace Path    dir_suffix=${suffix}
    set Suite Variable     ${TTIdir}

    # Start TTI capture
    Dated Log New Line     ===> start TTI traces capture
    Start TTI Traces in Streaming mode    src_ip=10.0.1.2



CB012733 stop TTI Capture
    [Arguments]            ${suffix}=${EMPTY}
    # Stop TTI capture
    Dated Log New Line     ===> stop TTI traces capture
    ${TTIpcap}             Stop TTI Traces in Streaming mode    tti_trace_path=${TTIdir}    tti_trace_filename=TTI_${suffix}
    set Suite Variable     ${TTIpcap}


CB012733 TTI Post Processing
    [Documentation]     The purpose of this test case is to analyze TTI traces captured during CB012733_A_SQUELETON
    ...                 test case to check that actThreeSymbolPdcch is activated (at least some pdch have start symbol
    ...                 equal to 2)
    ...                 First step is to convert TTI pcap to JSON using TtiConvertInterface,
    ...                 then decode JSON to CSV using TtitraceReaderEvtDec, and finally analyze the decoded
    ...                 traces with TtiAnalysisInterface to check the value of start symbol for pdsch.


    [Arguments]            ${TTIpcap}
    Dated Log New Line     ===> CB012733 TTI Post Processing Workflow
    Dated Log              Step 1: Converting TTI PCAP to JSON using TtiConvertInterface


    # STEP 1: CONVERT PCAP TO JSON
    # Uses TtiConvertInterface.Convert TTI capture which:
    # - Decodes PCAP file

    ${TTIjson}             Convert TTI trace from pcap to others    input_file_path=${TTIpcap}
    Dated Log              TTI conversion complete: ${TTIjson}

    # STEP 2: DECODE/EXTRACT TTI TRACES
    ${TTIcsv_decoded}      decode_tti_traces_json_using_TtitraceReaderEvtDec    jsonPathName=${TTIjson}    num_of_events=100000
    Dated Log New Line     Step 2: JSON decoded and ready for analysis
    Dated Log              TTI json file : ${TTIjson}
    Dated Log              TTI csv file : ${TTIcsv_decoded}
    set global variable    ${path_to_json}    ${TTIjson}
    Set Suite Variable      ${TTIcsv_decoded}


CB012733_A_TEST_TTI

    [Documentation]     The purpose of this test case is to
    ...                 TBD


    ${TTIpcap}=               Set Variable     /home/ute/Downloads/TTI.pcap
    ${TTIcsv_decoded}=        Set Variable    /home/ute/Downloads/TTI_filtered.csv
    ${TTIjson}=               Set Variable    /home/ute/Downloads/TTI_filtered.json
	Dated Log New Line     ===> CB012733 TTI Post Processing Workflow
    Dated Log              Step 1: Converting TTI PCAP to JSON using TtiConvertInterface

    # STEP 1: CONVERT PCAP TO JSON
    # Uses TtiConvertInterface.Convert TTI capture which:
    # - Decodes PCAP file
    # - Adds required metadata (utcTimestampData, eventHeader, etc.)
    # - Creates properly formatted JSON for TtiAnalysisInterface
    @{list_events_to_filter}=         Create List        dlFdSchedData
    ${TTIjson}             Convert TTI trace from pcap to others    input_file_path=${TTIpcap}
    #TtiConvertInterface.Convert TTI capture    pcap_file_path=${TTIpcap}
    #...                                                          events_list=${list_events_to_filter}
    Dated Log              TTI conversion complete: ${TTIjson}

    #dialogs.Execute Manual Step       wait keyboard

    # STEP 2: DECODE/EXTRACT TTI TRACES
    ${TTIcsv_decoded}      decode_tti_traces_json_using_TtitraceReaderEvtDec    jsonPathName=${TTIjson}    num_of_events=100000
    Dated Log New Line     Step 2: JSON decoded and ready for analysis
    Dated Log              TTI json file : ${TTIjson}
    Dated Log              TTI csv file : ${TTIcsv_decoded}
    set global variable    ${path_to_json}    ${TTIjson}
    Set Suite Variable      ${TTIcsv_decoded}
    ${TTIFileName}                              set Variable         TTI12733
    Set Suite Variable                          ${TTIFileName}

    #dialogs.Execute Manual Step       wait keyboard
    ${TTI_LOG_PATH}      Set variable    /home/ute/Downloads/
    Set Suite Variable      ${TTI_LOG_PATH}
    CB012733 Format and check TTI Trace

    dialogs.Execute Manual Step       wait keyboard
    ${outputFilePath_full}            CB012733 Format TTI Trace Combined DL UL   ${TTIcsv_decoded}


    # STEP 3: ANALYZE WITH TtiAnalysisInterface
    # Creates TtiAnalyzer instance from the properly converted JSON
    # The JSON contains all required metadata fields added by TtiConvertInterface
    Dated Log New Line     Step 3: Creating TtiAnalyzer from converted JSON
    #${my_instance} =       Create Tti Analyzer    ${TTIjson}    ${None}
    Dated Log              TtiAnalyzer instance created successfully

    # STEP 4: EXPORT SCHEDULING PARAMETERS
    # Export top-level parameters that exist in the decoded TTI CSV
    # The second parameter should be the OUTPUT path where the exported CSV will be saved
    Dated Log New Line     Step 4: Exporting scheduling parameters to CSV


    ${TTIcsv_exported}=                Evaluate       "${TTIcsv_decoded}".replace(".csv", "_exported.csv")
    ${path_to_json}        Set Variable     ${TTIjson}

    dialogs.Execute Manual Step       wait keyboard

    Dated Log New Line     ===> CB012733 TTI Post Processing Complete
    Dated Log              Results: CSV file ${TTIcsv_exported} contains exported parameters

CB012733 Format and check TTI Trace
    [Documentation]             1/ Filter all lines containing ulFdSchedData
    ...                         then remove  lines containing DL_10 in TTI Capture
    ...                         (match "Dl_PdcchSendReq UL grant 0-1" or " Dl_PdcchSendReq DL grant 1-1" or "Ul_PuschReceiveReq" in Sherpa)
    ...                            and redirect the output in a file named "TTI_5GC001013_TestCase#_Filtered.csv"
    ...                         2/ Only keep MSGID, SFN, and Format columns.
    ...                         then format the 2 colums SFN Slot in one column SFN.Slot
    ...                         then add first line header describing colums
    ...                         and redirect the output in a file named "TTI_5GC001013_TestCase#_Formatted.csv"


    ${inputFilePath}     Set variable    ${TTIcsv_decoded}

    ${pathOfOutput}	   ${fileName}          	Split Path	                   ${input_file_path}
    @{words} 	       Split String	  ${fileName}	        .pcap
    ${output_file_path}           set variable      ${pathOfOutput}/${words[0]}

    ${outputFilePathDL}    Set variable    ${output_file_path}_DLFiltered.csv
    ${outputFilePathUL}    Set variable    ${output_file_path}_ULFiltered.csv

    # For DL file

    ${command}           Set variable
    ...                  grep -i -E "(dlFdSchedData)" <${inputFilePath} >${outputFilePathDL}
    ${returnCode}        Run And Return Rc    ${command}
    Should Be Equal As Integers    ${returnCode}    0
    Dated Log New Line     Filtered CSV File: ${outputFilePathDL}


    ${inputFilePathDL}     Set variable       ${outputFilePathDL}
    ${outputFilePathDL}  Set variable       ${output_file_path}_FormattedDL.csv
    ${command}           Set variable
    ...                  awk -F';' '{printf("%s %s %s %s \\n", $6, $8, $12, $413)}' <${inputFilePathDL} \|
    ${command}           Set variable
    ...                  ${command} awk -F' ' '{print $1 ";" $2 ";" $3 ";" $4 }' \|
    ${command}           Set variable
    ...                  ${command} sed -e '1i\SFN ; SLOT ; RNTI ; StartSymbol' \|
    ${command}           Set variable
    ...                  ${command} grep -i -vwE "(INVALID)" >${outputFilePathDL}

    Dated Log New Line    -----> Commande Awk: ${command}

    ${returnCode}        Run And Return Rc    ${command}
    Should Be Equal As Integers    ${returnCode}    0

    # For UL file

    ${command}           Set variable
    ...                  grep -i -E "(ulFdSchedData)" <${inputFilePath} >${outputFilePathUL}
    ${returnCode}        Run And Return Rc    ${command}
    Should Be Equal As Integers    ${returnCode}    0
    Dated Log New Line     Filtered CSV File: ${outputFilePathUL}


    ${inputFilePathUL}   Set variable       ${outputFilePathUL}
    ${outputFilePathUL}  Set variable       ${output_file_path}_FormattedUL.csv
    ${command}           Set variable
    ...                  awk -F';' '{printf("%s %s %s %s \\n", $6, $8, $12, $142)}' <${inputFilePathUL} \|
    ${command}           Set variable
    ...                  ${command} awk -F' ' '{print $1 ";" $2 ";" $3 ";" $4 }' \|
    ${command}           Set variable
    ...                  ${command} sed -e '1i\SFN ; SLOT ; RNTI ; StartSymbol' \|
    ${command}           Set variable
    ...                  ${command} grep -i -vwE "(INVALID)" >${outputFilePathUL}

    Dated Log New Line    -----> Commande Awk: ${command}

    ${returnCode}        Run And Return Rc    ${command}
    Should Be Equal As Integers    ${returnCode}    0
    Dated Log New Line     Formatted CSV File DL: ${outputFilePathDL}
    Dated Log New Line     Formatted CSV File UL: ${outputFilePathUL}

    # Exemple d'utilisation : récupère les valeurs de la colonne 3 (RNTI) où la colonne 4 (StartSymbol) = 2
    @{slot_listDL}=         CB012733 Get Values From CSV By Column Match
    ...                   csv_file_path=${outputFilePathDL}
    ...                   search_value=2
    ...                   search_column=4
    ...                   return_column=2
    ...                   delimiter=;

    @{slot_listUL}=         CB012733 Get Values From CSV By Column Match
    ...                   csv_file_path=${outputFilePathUL}
    ...                   search_value=2
    ...                   search_column=4
    ...                   return_column=2
    ...                   delimiter=;

    Dated Log New Line    Liste des slots DL avec StartSymbol=2 : @{slot_listDL}
    Dated Log New Line    Liste des slots UL avec StartSymbol=2 : @{slot_listUL}

    # Check that lists are not empty, which means that at least some pdsch have start symbol equal to 2 in DL and UL
    ${length_DL}=    Get Length    ${slot_listDL}
    ${length_UL}=    Get Length    ${slot_listUL}

    Should Not Be Equal As Integers    ${length_DL}    0
    ...    msg=ERREUR: La liste slot_listDL est vide - aucune correspondance trouvée pour StartSymbol=2 en DL

    Should Not Be Equal As Integers    ${length_UL}    0
    ...    msg=ERREUR: La liste slot_listUL est vide - aucune correspondance trouvée pour StartSymbol=2 en UL

    Dated Log New Line    ✓ Validation OK: ${length_DL} slots trouvés en DL, ${length_UL} slots trouvés en UL

CB012733 Get Values From CSV By Column Match
    [Documentation]     Recherche une valeur dans une colonne d'un fichier CSV et retourne
    ...                 les valeurs correspondantes d'une autre colonne.
    ...
    ...                 Arguments:
    ...                 - csv_file_path: Chemin vers le fichier CSV
    ...                 - search_value: Valeur à rechercher dans la colonne de recherche
    ...                 - search_column: Index de la colonne où chercher (défaut: 4, base 1)
    ...                 - return_column: Index de la colonne à retourner (défaut: 2, base 1)
    ...                 - delimiter: Délimiteur CSV (défaut: ,)
    ...
    ...                 Retourne: Liste des valeurs de la colonne return_column où search_column contient search_value
    ...
    ...                 Exemple:
    ...                 @{values}=    Get Values From CSV By Column Match    /path/to/file.csv    ma_valeur    4    2

    [Arguments]    ${csv_file_path}    ${search_value}    ${search_column}=3    ${return_column}=1    ${delimiter}=,

    # Conversion des indices en base 0 pour Python
    ${search_idx}=    Evaluate    ${search_column} - 1
    ${return_idx}=    Evaluate    ${return_column} - 1

    # Lecture et filtrage du CSV avec Python (saute la première ligne = en-tête)
    ${py_expr}=    Catenate    SEPARATOR=
    ...    [row[${return_idx}].strip() for row in
    ...    [line.strip().split("${delimiter}") for line in open(r"${csv_file_path}", "r").readlines()[1:]]
    ...    if len(row) > max(${search_idx}, ${return_idx}) and row[${search_idx}].strip() == "${search_value}"]

    @{result_list}=    Evaluate    ${py_expr}

    ${list_length}=    Get Length    ${result_list}
    Dated Log New Line    Trouvé ${list_length} correspondance(s) pour la valeur '${search_value}' dans la colonne ${search_column}
    Run Keyword If    ${list_length} > 0    Dated Log New Line    Valeurs retournées: ${result_list}
    Run Keyword If    ${list_length} == 0    Dated Log New Line    ATTENTION: Aucune correspondance trouvée !

    [Return]    ${result_list}

CB012733 Format TTI Trace Combined DL UL
    [Documentation]     Formate les traces TTI en un seul fichier CSV combinant DL et UL.
    ...                 Pour DL (dlFdSchedData): extrait colonne 413 (StartSymbol)
    ...                 Pour UL (ulFdSchedData): extrait colonne 142 (StartSymbol)
    ...
    ...                 Arguments:
    ...                 - inputFilePath: Chemin vers le fichier CSV décodé
    ...                 - output_file_path: Chemin de base pour le fichier de sortie
    ...
    ...                 Retourne: Chemin du fichier CSV formaté

    [Arguments]    ${inputFilePath}

    ${pathOfOutput}	   ${fileName}          	Split Path	                   ${input_file_path}
    @{words} 	       Split String	  ${fileName}	        .pcap
    ${output_file_path}           set variable      ${pathOfOutput}/${words[0]}


    ${outputFilePath_full}    Set variable    ${output_file_path}_Full_Formatted.csv

    # Traitement unique pour DL et UL : prend colonne 413 si dlFdSchedData, colonne 142 si ulFdSchedData
    ${command}           Set variable
    ...                  awk -F';' '{if (\$1 ~ /dlFdSchedData/)
    ${command}           Set variable
    ...                  ${command} printf("%s %s %s %s\\n", \$6, \$8, \$12, \$413);
    ${command}           Set variable
    ...                  ${command} else if (\$1 ~ /ulFdSchedData/)
    ${command}           Set variable
    ...                  ${command} printf("%s %s %s %s\\n", \$6, \$8, \$12, \$142)}' <${inputFilePath} \|
    ${command}           Set variable
    ...                  ${command} awk -F' ' '{print \$1 ";" \$2 ";" \$3 ";" \$4 }' \|
    ${command}           Set variable
    ...                  ${command} sed -e '1i\\SFN ; SLOT ; RNTI ; StartSymbol' \|
    ${command}           Set variable
    ...                  ${command} grep -i -vwE "(INVALID)" >${outputFilePath_full}

    Dated Log New Line    -----> Commande Awk: ${command}

    ${returnCode}        Run And Return Rc    ${command}
    Should Be Equal As Integers    ${returnCode}    0
    Dated Log New Line     Formatted CSV File (DL + UL): ${outputFilePath_full}

    [Return]    ${outputFilePath_full}