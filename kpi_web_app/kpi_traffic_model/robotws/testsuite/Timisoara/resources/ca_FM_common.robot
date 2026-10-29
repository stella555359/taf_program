*** Settings ***
Documentation  This resource contains all common keywords from CBTS and SBTS FM CA.

Library  SSHLibrary


*** Keywords ***
Get POOR Reset Counter From RMOD /var/log/BBOX5 File
    [Documentation]  This keyword is used to retrieve POOR Reset Counter value from RMOD.
    ...  Connection to Radio Modules is opened beforehand, for SBTS or CBTS.
    ...  "Unzip BBOX5.zip file on RMOD" keyword is used.
    [Arguments]  ${rmod_sn}

    Unzip BBOX5.zip file on RMOD  ${rmod_sn}
    SSHLibrary.Write  cat BBOX5 | grep POOR
    ${file_output}  SSHLibrary.Read Until Prompt
    ${lines}  Get Regexp Matches  ${file_output}  \nPOOR Reset Counter:.*[0-9]+
    ${counter_value}  Fetch From Right  ${lines}[0]  ${SPACE}
    Should Not Be Empty  ${counter_value}  msg=POOR Counter not found in /var/log location on RMOD with serial_number: ${rmod_sn}.

    RETURN  ${counter_value}


Verify The List Of Operations From RMOD /var/volatile/log/BBOX5 File
    [Documentation]  This keyword is used to verify Operations on RMOD(Reset Reason and Reset Cause).
    ...  Connection to Radio Modules is opened beforehand, for SBTS or CBTS.
    ...  "Unzip BBOX5.zip file on RMOD" keyword is used.
    [Arguments]  ${rmod_sn}  ${reset_reason}  ${reset_cause}

    Unzip BBOX5.zip file on RMOD  ${rmod_sn}
    SSHLibrary.Write  cat BBOX5
    SSHLibrary.Set Client Configuration  timeout=30s
    ${file_output}  SSHLibrary.Read Until Prompt
    ${lines}  Get Lines Containing String  ${file_output}  Reset[0]
    ${reason_line}  Get Lines Containing String  ${lines}  Reset Reason
    ${cause_line}  Get Lines Containing String  ${lines}  Reset Cause
    Should Match Regexp  ${reason_line}  ${reset_reason}  msg=Reset Reason is not ok for RMOD with serial number: ${rmod_sn}.
    Should Contain  ${cause_line}  ${reset_cause}  msg=Reset Cause is not ok for RMOD with serial number: ${rmod_sn}.
    Log  Reset Reason and Cause are correct for RMOD with serial number: ${rmod_sn}. [OK]  console=true


Unzip BBOX5.zip file on RMOD
    [Documentation]  This keyword is used to unzip BBOX5.zip file on RMOD.
    ...  Connection to Radio Modules is opened beforehand, for SBTS or CBTS.
    [Arguments]  ${rmod_sn}

    SSHLibrary.Write  cd /var/log
    SSHLibrary.Set Client Configuration  prompt=#
    SSHLibrary.Read Until Prompt
    SSHLibrary.Write  ls
    ${ls_output}  SSHLibrary.Read Until Prompt
    Should Contain  ${ls_output}  BBOX5.zip  msg=BBOX5.zip not found in /var/log location on RMOD with serial_number: ${rmod_sn}.
    ${bbox5_is_unziped}  Run Keyword And Return Status  Should Contain  ${ls_output}  BBOX5
    IF  ${bbox5_is_unziped}
        SSHLibrary.Write  rm BBOX5
        Read Until Prompt
    END
    SSHLibrary.Write  unzip BBOX5.zip
    SSHLibrary.Read Until Prompt