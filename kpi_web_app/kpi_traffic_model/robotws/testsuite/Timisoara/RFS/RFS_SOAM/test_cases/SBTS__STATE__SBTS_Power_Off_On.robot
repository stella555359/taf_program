*** Settings ***
Documentation    Test Suite
Resource    ../test_resources/SBTS__STATE__SBTS_Power_Off_On.robot

*** Test Cases ***
[1]SBTS__STATE__SBTS_Power_Off_On
    [Setup]    TC Setup
    [Teardown]    TC Teardown
    TC__SBTS__STATE__SBTS_Power_Off_On

