# ====================================================================================================[120 characters]
# This is a Python File, which helps to implement the Robot Keywords used in 5GC000795.robot
# Team: 'MN ECE ULM R&D L3NRT 07 SqdGp65'
# Email: 'I_MN_5GSC_SW_ENG_ULM_SQD_65@internal.nsn.com'
# ----------------------------------------------------------------------------------------------------[120 characters]

import sys
import csv
import json
import os
import time
import datetime
import glob
import re

# Robot Framework Libraries:
from robot.libraries.OperatingSystem import OperatingSystem
from robot.libraries.BuiltIn import BuiltIn

# TAF & UTE Libraries:
from ute_wtssim import ute_wtssim
from ute_fsmaccess import ute_fsmaccess
from taf.config.scf import scf
from taf.analyzer.pdml import pdml, PdmlReader  # noqa: E402
from taf.converters.pcaptopdml import PcapToPdmlFactory
from taf.converters.eventdecoder import eventdecoder
from taf.config.wts import wts
from taf.transport.ssh import ssh


# ====================================================================================================[120 characters]
#   Global Variables
# ====================================================================================================[120 characters]

logLevel = "INFO"
RED = '\033[31m'
GREEN = '\033[32m'
RESET = '\033[0m'
BOLD = '\033[1m'

rbi = BuiltIn()

# ====================================================================================================[120 characters]
#   Keywords for 5GC000795-A-B-D
# ====================================================================================================[120 characters]


def activate_5GC000795_feature():
    # ------------------------------------------------------------------------------------------------[120 characters]
    # Private Keyword: Activate 5GC000795 Feature
    # It performs online feature activation
    # ------------------------------------------------------------------------------------------------[120 characters]
    nrbtsStr = rbi.run_keyword("Get distNames from gNB DU", "MRBTS-\\\\d+/NRBTS-\\\\d+")
    nrbtsStr = nrbtsStr[0]
    para_list = [
        {'parameter': 'actMultiDrbNSA', 'value': 'true', 'dist_name': nrbtsStr},
        {'parameter': 'actNonGbrServiceDiff', 'value': 'false', 'dist_name': nrbtsStr},
        {'parameter': 'nsaInactivityTimer', 'value': '600', 'dist_name': nrbtsStr},
        {'parameter': 'reportingIntervalPm', 'value': '5min', 'dist_name': 'MNL-1/MNLENT-1/PMCADM-1'},
        {'value': 'disabled', 'dist_name': '%s/NRPMRNL-1' % nrbtsStr, 'parameter': 'miNrPaging'},
        {'value': 'disabled', 'dist_name': '%s/NRPMRNL-1' % nrbtsStr, 'parameter': 'miNrRelReportCu'},
        {'value': '5min', 'dist_name': '%s/NRPMRNL-1' % nrbtsStr, 'parameter': 'miNrHighRlcReport'},
        {'value': '5min', 'dist_name': '%s/NRPMRNL-1' % nrbtsStr, 'parameter': 'miNrLowRlcReport'},
        {'value': '5min', 'dist_name': '%s/NRPMRNL-1' % nrbtsStr, 'parameter': 'miNrMacPduTput'},
        {'value': '5min', 'dist_name': '%s/NRPMRNL-1' % nrbtsStr, 'parameter': 'miNrMacSduReport'},
        {'value': '5min', 'dist_name': '%s/NRPMRNL-1' % nrbtsStr, 'parameter': 'miNrNgInterface'},
        {'value': '5min', 'dist_name': '%s/NRPMRNL-1' % nrbtsStr, 'parameter': 'miNrNgUReport'},
        {'value': '5min', 'dist_name': '%s/NRPMRNL-1' % nrbtsStr, 'parameter': 'miNrPDCP1Report'},
        {'value': '5min', 'dist_name': '%s/NRPMRNL-1' % nrbtsStr, 'parameter': 'miNrPDCP2Report'},
        {'value': '5min', 'dist_name': '%s/NRPMRNL-1' % nrbtsStr, 'parameter': 'miNrX2CB'},
        {'value': '5min', 'dist_name': '%s/NRPMRNL-1' % nrbtsStr, 'parameter': 'miNrX2CC'},
        {'value': '5min', 'dist_name': '%s/NRPMRNL-1' % nrbtsStr, 'parameter': 'miNrRacCu'},
        {'value': '5min', 'dist_name': '%s/NRPMRNL-1' % nrbtsStr, 'parameter': 'miNrX2UInterface'}
    ]
    oamType = rbi.run_keyword("Get OAM Type")
    if oamType.lower() == "coam":
        rbi.run_keyword("connect.Setup OAM HTTP Session")
        rbi.run_keyword("Update List of SCF parameters", para_list, 120)
        rbi.log_to_console(GREEN + "Activate 5GC000795 Feature: done on cOAM!" + RESET + "")
    else:
        rbi.log_to_console(RED + "Activate 5GC000795 Feature: OAM Type is not supported!" + RESET + "")
    rbi.run_keyword("Store Current WTS Config")
    tl = rbi.get_variable_value("${tl}")
    wtsConfigFilePath = ''.join([tl.core.dir_path, '/', tl.core.cfg_filename])
    wtsObj = wts()
    wtsObj.load_wts_cfg(file_path=wtsConfigFilePath)
    wtsObj.insert(u"set_bearer id=7 ue=101 qci=7", u"after", u"set_bearer id=2 ue=101")
    wtsObj.save_wts_cfg(file_path=wtsConfigFilePath)


def activate_reduced_pdcpBufDiscardThreshold():
    # ------------------------------------------------------------------------------------------------[120 characters]
    # Private Keyword: Activate Reduced pdcpBufDiscardThreshold
    # It performs online feature activation
    # ------------------------------------------------------------------------------------------------[120 characters]
    pdcp_list = rbi.run_keyword("Get distNames from gNB SCF", "MRBTS-\\\\d+/NRBTS-\\\\d+/NRDRB_PDCP-\\\\d+")
    para_list = [{'value': '100', 'dist_name': i, 'parameter': 'pdcpBufDiscardThreshold'} for i in pdcp_list]
    oamType = rbi.run_keyword("Get OAM Type")
    if oamType.lower() == "coam":
        rbi.run_keyword("connect.Setup OAM HTTP Session")
        rbi.run_keyword("Update List of SCF parameters", para_list)
        rbi.log_to_console(GREEN + " Activate Reduced pdcpBufDiscardThreshold: done on cOAM!" + RESET + "")
    else:
        rbi.log_to_console(RED + " Activate Reduced pdcpBufDiscardThreshold: OAM Type is not supported!" + RESET + "")


def set_inactivity_timer_parameters(inactivity_detection, inactivity_timer, notification_level):
    # ------------------------------------------------------------------------------------------------[120 characters]
    # Private Keyword: Set Inactivity Timer Parameters
    # It performs online commissioning changes
    # ------------------------------------------------------------------------------------------------[120 characters]
    nrbtsStr = rbi.run_keyword("Get distNames from gNB DU", "regex=MRBTS-\\\\d+/NRBTS-\\\\d+")
    nrbtsStr = nrbtsStr[0]
    para_list = [
        {'parameter': 'actInactDetNSAUe', 'value': inactivity_detection, 'dist_name': nrbtsStr},
        {'parameter': 'nsaInactivityTimer', 'value': inactivity_timer, 'dist_name': nrbtsStr},
        {'parameter': 'nsaActivityNotificationLevel', 'value': notification_level, 'dist_name': nrbtsStr},
    ]
    oamType = rbi.run_keyword("Get OAM Type")
    if oamType.lower() == "coam":
        rbi.run_keyword("connect.Setup OAM HTTP Session")
        rbi.run_keyword("Update List of SCF parameters", para_list)
        rbi.log_to_console(GREEN + "Activate 5GC000795 Feature: done on cOAM!" + RESET + "")
    else:
        rbi.log_to_console(RED + "Activate 5GC000795 Feature: OAM Type is not supported!" + RESET + "")
