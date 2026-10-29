__maintainer__ = "Wang, Xin3"
__team__ = "I_MN_ECE_RD_1_CN_SG_10_ANTARCTIC_GMS"
__email__ = "xin.3.wang@nokia-sbell.com"

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


_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

_PARAMS_TO_MODIFY_SCF = [
    dict(value="CI-TLDX0006", dist_name="MRBTS-1900", p_name="btsName"),
    dict(value="172.18.10.20", dist_name="LTE_x2", p_name="amfIPAddress"),
    dict(value="172.18.10.11", dist_name="CU_x2Cplane", p_name="localIpAddr"),
    dict(value="172.18.10.12", dist_name="CU_s1Uplane", p_name="localIpAddr"),
    dict(value="172.18.10.12", dist_name="CU_x2Uplane", p_name="localIpAddr"),
]


# gNB webUI info
_cu = CU(
    backhaul_site_oam_ip="10.57.233.50",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.233.50", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.233.50", username="Nemuadmin", password="nemuuser"
    ),
)


# _du = DU(airscale = Airscale([]))

# info for FACOM(PowerStation).
_gnb_pdu = FACOM(addr="10.57.242.36", port_numbers=[3])

_common_unit_0 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.233.50", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=None,
    pdu_port=_gnb_pdu.pdu_ports[3],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=None)

_cbts = ClassicalBts(cu=_cu, dus=[_du])

#########Testpc for run robot FRT cases##########
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.183.71.118", username="root", password="nokia123"
    )
)

#########LteEmu##########
_lteemu = LTEEmuCore(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.213.62", username="nokia", password="nokia123"
    ),
    dir_path="/home/nokia/LTEemu_core2_64_3252",
    cfg_filename="basic_wts_step1.cfg",
    mme_ip="",
    edaemon_port="22222",
    egate_port="9880",
)

_scf = SCF(
    project="5G18A",
    name="SBTS5G18A_5g_pid12_classical.xml",
    scf_params=_PARAMS_TO_MODIFY_SCF,
)

# Testline
tl = TestLine(test_pc=_test_pc, gnbs=[_cbts], core=_lteemu, tl_cloud_topology="")
tl.scf = _scf  # still a WA
PACKAGE_SERVER_IP = "10.183.71.27"
PACKAGE_SERVER_USER = "root"
PACKAGE_SERVER_PWD = "nokia123"
gNB_Package_path = "/ephemeral/package"
YAFT_path = "/ephemeral/yaft"
package_url = "https://artifactory-espoo1.ext.net.nokia.com/artifactory/mnp5g-central-public-local/System_Release/"


__all__ = ["tl"]
