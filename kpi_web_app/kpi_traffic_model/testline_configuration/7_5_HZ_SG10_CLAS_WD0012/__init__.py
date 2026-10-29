__maintainer__ = "Nandyala, Soori"
__team__ = "I_MN_ECE_RD_1_CN_SG_10_ANTARCTIC_GMS"
__email__ = "soori.nandyala@nokia-sbell.com"

import os
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
)
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline.core import LTEEmuCore
from taf.config.testline.ue import Airphone, AirphoneCloud
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.compatibility.configuration import TestlineWrapper
from taf.config.cbts import create_configuration_data
from taf.config.testline.legacy import SCF


_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

_PARAMS_TO_MODIFY_SCF = [
    dict(value="CI-TLDX0012", dist_name="MRBTS-1900", p_name="btsName"),
    dict(value="172.18.10.20", dist_name="LTE_x2", p_name="amfIPAddress"),
    dict(value="172.18.10.11", dist_name="CU_x2Cplane", p_name="localIpAddr"),
    dict(value="172.18.10.12", dist_name="CU_s1Uplane", p_name="localIpAddr"),
    dict(value="172.18.10.12", dist_name="CU_x2Uplane", p_name="localIpAddr"),
]


# gNB webUI info
_cu = CU(
    backhaul_site_oam_ip="10.57.233.167",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.233.167", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.233.167", username="Nemuadmin", password="nemuuser"
    ),
)


# _du = DU(airscale = Airscale([]))

# info for FACOM(PowerStation). port1=gNB  port5= Airphone
_gnb_pdu = FACOM(addr="10.57.242.44", port_numbers=[1])
_ap_pdu = FACOM(addr="10.57.242.43", port_numbers=[5])

# ABIL, solid content, just keep
_capacity_unit = CapacityUnit(addr="192.168.253.22")

# ASIK
_common_unit = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="0.57.233.167", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[1],
)


_common_unit_0 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.233.167", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=None,
    pdu_port=_gnb_pdu.pdu_ports[1],
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
        addr="10.57.195.9", username="nokia", password="nokia123"
    ),
    dir_path="/home/nokia/WTS",
    cfg_filename="basic_wts_step2.cfg",
    mme_ip="",
    edaemon_port="22222",
    egate_port="20000",
)

_scf = SCF(
    project="5G18A",
    name="SBTS5G18A_5g_pid12_classical.xml",
    scf_params=_PARAMS_TO_MODIFY_SCF,
)

# Airphone
##login AP BB1, root@fct-0a:~ >arp -a, get fsp-5-1a (192.168.253.84)##
_airphone_capacity_unit_1 = CapacityUnit(addr="192.168.253.84")

# AP BB1
_airphone_common_unit_1 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.233.177", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_airphone_capacity_unit_1],
    pdu_port=_ap_pdu.pdu_ports[5],
)

_airphone_airscale = Airscale(common_units=[_airphone_common_unit_1])

# AP BB3
_airphone_cloud = AirphoneCloud(
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.195.8", username="robot", password="rastre1"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.195.8", username="Nemuadmin", password="nemuuser"
    ),
)

_airphone = Airphone(
    egate=None,
    airphone_cloud=_airphone_cloud,
    l1=_airphone_airscale,
    l3_ssh_connection_details=None,
    l2_ssh_connection_details=None,
)


airphone_scf = SCF(project="5G18A", name="SBTS5G18A_5g_pid12.xml", scf_params="")

# Testline
tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    core=_lteemu,
    tl_cloud_topology="CLOUD_5G_BB3_18A",
    pdus=[_gnb_pdu, _ap_pdu],
    ues=[_airphone],
)
tl = TestlineWrapper(tl)

tl.scf = _scf  # still a WA

PACKAGE_SERVER_IP = "10.183.71.27"
PACKAGE_SERVER_USER = "root"
PACKAGE_SERVER_PWD = "nokia123"
gNB_Package_path = "/ephemeral/package"
YAFT_path = "/ephemeral/yaft"
package_url = "https://artifactory-espoo1.ext.net.nokia.com/artifactory/mnp5g-central-public-local/System_Release/"


__all__ = ["tl"]
