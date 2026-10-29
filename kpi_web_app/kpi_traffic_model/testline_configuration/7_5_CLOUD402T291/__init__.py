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
from taf.config.testline.nms import Netact
from taf.config.testline.gnb.networkaddress import NetworkAddress

__maintainer__ = "Xie Jiali"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_8_GMS <I_MN_5G_RAN_IV4_LINE_HZG_8@internal.nsn.com>"
)
__email__ = "jia.xie@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# testPc(taf)
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.189.20", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# 5GRU for classicalBTS

# PB for RU
_ru_pdu = FACOM(addr="10.71.196.50", port_numbers=[5])

_ru = RU(
    ru_hw_group="AEQE",
    serial_number="1M203304676",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1",
        username="serviceuser",
        password="bobuWrUHk7Xq7WPpY9ZcjEi8zNdX3plZ+/y420RZ7W4=",
    ),
    lmp_connection=SshServiceDetails(
        addr="10.71.218.16", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu.pdu_ports[5],
)

_ru_pdu2 = FACOM(addr="10.71.196.51", port_numbers=[4])

_ru2 = RU(
    ru_hw_group="AEQP",
    serial_number="1M202010217",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1",
        username="serviceuser",
        password="bobuWrUHk7Xq7WPpY9ZcjEi8zNdX3plZ+/y420RZ7W4=",
    ),
    lmp_connection=SshServiceDetails(
        addr="10.71.218.17", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu2.pdu_ports[4],
)

_ru_pdu3 = FACOM(addr="10.71.196.50", port_numbers=[2])

_ru3 = RU(
    ru_hw_group="AQQY",
    serial_number="DH233082819",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    lmp_connection=SshServiceDetails(
        addr="10.71.217.157", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu3.pdu_ports[2],
)

_ru_pdu4 = FACOM(addr="10.71.196.48", port_numbers=[1])

_ru4 = RU(
    ru_hw_group="AQQY",
    serial_number="DH233082822",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    lmp_connection=SshServiceDetails(
        addr="10.71.217.123", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu4.pdu_ports[1],
)

# _ru_pdu5 = FACOM(addr="10.71.196.48", port_numbers=[3])
#
# _ru5 = RU(
#     ru_hw_group="AQQY",
#     serial_number="DH233082825",
#     default_ssh_connection_details=SshServiceDetails(
#         addr="192.168.101.1", username="serviceuser", password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY="
#     ),
#     lmp_connection=SshServiceDetails(
#         addr="10.71.217.157", username="ute", password="3edc4rfv%TGB"
#     ),
#     pdu_port=_ru_pdu5.pdu_ports[3],
# )

_ru_pdu6 = FACOM(addr="10.71.196.56", port_numbers=[6])

_ru6 = RU(
    ru_hw_group="AEQE",
    serial_number="1M202703151",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1",
        username="serviceuser",
        password="bobuWrUHk7Xq7WPpY9ZcjEi8zNdX3plZ+/y420RZ7W4=",
    ),
    lmp_connection=SshServiceDetails(
        addr="10.0.176.215", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu6.pdu_ports[6],
)

_ru_pdu7 = FACOM(addr="10.71.196.52", port_numbers=[3])

_ru7 = RU(
    ru_hw_group="AEQE",
    serial_number="1M211717562",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1",
        username="serviceuser",
        password="bobuWrUHk7Xq7WPpY9ZcjEi8zNdX3plZ+/y420RZ7W4=",
    ),
    lmp_connection=SshServiceDetails(
        addr="10.0.176.136", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu7.pdu_ports[3],
)

# gNB LMP IP
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
# ABIL internal ip
_capacity_unit = CapacityUnit(addr="192.168.253.20")
# gNB PB
_gnb_pdu = FACOM(addr="10.71.196.45", port_numbers=[5])
_gnb_test_pc_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.189.20", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[5],
    test_pc=_gnb_test_pc_0,
)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(
    airscale=_airscale,
    rus=[_ru, _ru2, _ru3, _ru4, _ru6, _ru7],
    f1_m_ip_addr="10.71.211.204",
)

# gNB OAM M-plane IP
_cu = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.211.204", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.211.204", username="Nemuadmin", password="nemuuser"
    ),
)

# RealEnb
_lmp_connection_enb = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
_enb_pdu = FACOM(addr="10.57.241.168", port_numbers=[6])
_enb_pc_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.17", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection_enb,
    capacity_units=[],
    pdu_port=_enb_pdu.pdu_ports[6],
    test_pc=_enb_pc_0,
    hardware_type=None,
)
_real_enb = Airscale(common_units=[_common_unit_1])
_lte_real_enb = RealEnb(
    system_module=_real_enb,
    rms=None,
    oam_ip=NetworkAddress(v4="10.57.237.37"),
    instance_id=4291,
)

##cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=291)
## switch Dtor
_dell_s4048on_ssh = SshServiceDetails(
    addr="10.57.129.120", port="1/9", username="5gran", password="nokia123"
)
_dell_s4048on_switch = DellS4048ONSwitch(_dell_s4048on_ssh)

## switch Mtor
_dell_s4048ton_ssh = SshServiceDetails(
    addr="10.57.129.136", port="1/18", username="5gran", password="nokia123"
)
_dell_s4048ton_switch = DellS4048TONSwitch(_dell_s4048ton_ssh)

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
    switches=[_dell_s4048on_switch, _dell_s4048ton_switch],
)
