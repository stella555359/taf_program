__maintainer__ = "Mao, Cathy"
__team__ = "NSB MN ECE RD 2 CN 06 SG"
__email__ = "cathy.mao@nokia-sbell.com"

import os
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
)
from taf.config.testline.gnb import ClassicalBts, CU
from taf.config.testline.core import LTEEmuCore
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC
from taf.config.testline import RU, DU
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit

from taf.config.testline.legacy import SCF
from taf.config.testline.ue import *

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

_PARAMS_TO_MODIFY_SCF = [
    dict(value="CI-TLDX0832", dist_name="MRBTS-1900", p_name="btsName"),
    dict(value="172.18.10.20", dist_name="LTE_x2", p_name="amfIPAddress"),
    dict(value="172.18.10.11", dist_name="CU_x2Cplane", p_name="localIpAddr"),
    dict(value="172.18.10.12", dist_name="CU_s1Uplane", p_name="localIpAddr"),
    dict(value="172.18.10.12", dist_name="CU_x2Uplane", p_name="localIpAddr"),
]


_cu = CU(
    backhaul_site_oam_ip="10.57.146.165",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.146.165", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.146.165", username="Nemuadmin", password="nemuuser"
    ),
)

# _du = DU(airscale = Airscale([]))

_gnb_pdu = FACOM(addr="10.57.247.204", port_numbers=[4])

_common_unit_0 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.146.165", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=None,
    pdu_port=_gnb_pdu.pdu_ports[4],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=None)

_cbts = ClassicalBts(cu=_cu, dus=[_du])

#########Testpc##########
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.212.88", username="ute", password="ute"
    )
)

#########LteEmu##########
_lteemu = LTEEmuCore(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.195.80", username="ute", password="ute"
    ),
    dir_path="/home/ute/WTS_1908_WK33_4.0.8221_1263168.1",
    cfg_filename="basic_WK33_4.0.8221_1263168.cfg",
    mme_ip="",
    edaemon_port="22222",
    egate_port="9880",
)

_scf = SCF(
    project="5G19",
    name="SBTS5G19_5g_pid12_classical.xml",
    scf_params=_PARAMS_TO_MODIFY_SCF,
)


# #Airphone


# Testline
tl = TestLine(test_pc=_test_pc, gnbs=[_cbts], core=_lteemu, tl_cloud_topology="")
tl.scf = _scf  # still a WA
PACKAGE_SERVER_IP = "10.57.212.88"
PACKAGE_SERVER_USER = "root"
PACKAGE_SERVER_PWD = "uteadmin"
gNB_Package_path = "/home/package"
YAFT_path = "/home/yaft"
package_url = "https://artifactory-espoo1.ext.net.nokia.com/artifactory/mnp5g-central-public-local/System_Release/"
Baseband = "ABIL"
__all__ = ["tl"]
