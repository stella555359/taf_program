import os
from taf.config.testline.cloud_hosting import (
    ControlNode,
    NCIR,
    CloudDeployment,
    DeploymentFlavorStack,
    DeploymentNetworkStack,
    DeploymentVnfStack,
)
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.core import EPCSim, LTEEmuCore, PrismaCore
from taf.config.testline import RU, DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import Qualcomm, QualcommUeType, Android
from taf.config.testline import Enb, SimEnb, RealEnb, LTEEmuEnb, PrismaEnb, DocomoEnb
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.nms import Netact
from taf.config.testline.gnb.networkaddress import NetworkAddress

__maintainer__ = "Casbo Xing"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_8_GMS <I_MN_5G_RAN_IV4_LINE_HZG_8@internal.nsn.com>"
)
__email__ = "casbo.xing@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# testPc(taf)
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.226", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# PB for RU
_ru_pdu = FACOM(addr="10.101.45.172", port_numbers=[5])

_ru = RU(
    ru_hw_group="AEHC",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="rfsw", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.101.47.17", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu.pdu_ports[5],
)

_ru_pdu2 = FACOM(addr="10.101.45.172", port_numbers=[6])

_ru2 = RU(
    ru_hw_group="AEHC",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="rfsw", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.101.47.12", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu2.pdu_ports[6],
)

# gNB LMP IP
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
# ABIL internal ip
_capacity_unit = CapacityUnit(addr="192.168.253.20")
# gNB PB
_gnb_pdu = FACOM(addr="110.68.87.61", port_numbers=[2])
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[2],
)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(airscale=_airscale, rus=[_ru, _ru2], f1_m_ip_addr="10.101.48.41")

# gNB OAM M-plane IP
_cu = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.48.41", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.48.41", username="Nemuadmin", password="nemuuser"
    ),
)

# RealEnb
_lmp_connection_enb = SshServiceDetails(
    addr="10.101.48.45", username="toor4nsn", password="oZPS0POrRieRtu"
)
_lmp_connection_enb2 = SshServiceDetails(
    addr="10.101.48.45", username="toor4nsn", password="oZPS0POrRieRtu"
)

_enb_pdu = FACOM(addr="10.68.87.61", port_numbers=[1])
_enb_pdu2 = FACOM(addr="10.68.87.61", port_numbers=[1])

_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection_enb,
    capacity_units=[],
    pdu_port=_enb_pdu.pdu_ports[1],
)
_common_unit_2 = CommonUnit(
    lmp_connection=_lmp_connection_enb2,
    capacity_units=[],
    pdu_port=_enb_pdu2.pdu_ports[1],
)

_real_enb = Airscale(common_units=[_common_unit_1, _common_unit_2])
_lte_real_enb = RealEnb(airscale=_real_enb)

##cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=841)

## switch Dtor
_dell_s4048on_ssh = SshServiceDetails(
    addr="10.68.85.28", port="1/12", username="5gran", password="nokia123"
)
_dell_s4048on_switch = DellS4048ONSwitch(_dell_s4048on_ssh)


_netact = Netact("10.107.178.214")

# QualComm UE
_appserver_ssh = SshServiceDetails(
    addr="10.57.162.10", username="cmw_sg7", password="Nokia07!"
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.162.10",
    iperf_path="/usr/bin/iperf",
    port=57291,
)

# remote UE CPC
_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.47", username="nokia5G", password="noki@123"
    ),
    serial_number="4b50ae0",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_UE", "REAL_ANDROID_UE"],
)

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    enbs=[_lte_real_enb],
    tl_cloud_topology=_tl_cloud_topology,
    nms=_netact,
    ues=[_android],
    switches=[_dell_s4048on_switch],
)

tl = TestlineWrapper(tl)
