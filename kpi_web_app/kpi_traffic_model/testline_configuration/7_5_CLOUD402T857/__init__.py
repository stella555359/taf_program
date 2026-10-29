import os
import re
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
from taf.config.testline.pdu import HBTE as PduHBTE
from taf.config.testline.pdu import TopYoung as PduTopYoung
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import AirphoneCloud, Airphone, Prisma, TM500, MediaTek
from taf.config.testline import Enb, SimEnb, RealEnb, LTEEmuEnb, PrismaEnb, DocomoEnb
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.nms import Netact
from taf.config.testline.appserver import AppServer
from taf.config.testline.dcap import DcapRnD, DcapBasic
from taf.config.testline.ue import Qualcomm, QualcommUeType, Android
from taf.config.testline.attenuator import (
    AttenuationPort,
    TopYoung,
    HBTE,
)
from taf.config.testline.gnb.networkaddress import NetworkAddress

__maintainer__ = "Wang lei"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_8_GMS <I_MN_5G_RAN_IV4_LINE_HZG_8@internal.nsn.com>"
)
__email__ = "lei.24.wang@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

##host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.91", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_attenuator = HBTE(
    ip_addr="10.57.236.3",
    port="5000",
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 9, 10, 11, 12, 13, 14],
    model="PA-16-16-6-127-0.5-B-S",
    version=None,
)

# 5GRU for classicalBTS
_ru1_pdu = PduHBTE(addr="10.57.241.161", port_numbers=[1])

_ru1 = RU(
    ru_hw_group="AWHHF",
    serial_number="AH234401001",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="1.1.1.1", username="root", password="umniedziala"
    ),
    pdu_port=_ru1_pdu.pdu_ports[1],
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[4],
        _attenuator.attenuator_ports[9],
        _attenuator.attenuator_ports[12],
    ],
)
_ru2_pdu = PduHBTE(addr="10.57.241.160", port_numbers=[2])
_ru2 = RU(
    ru_hw_group="AWHHF",
    serial_number="EB2050R0478",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="1.1.1.1", username="root", password="umniedziala"
    ),
    pdu_port=_ru2_pdu.pdu_ports[2],
    attenuation_ports=[
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[10],
        _attenuator.attenuator_ports[13],
    ],
)

##DU for classicalBTS
_gnb_lmp_connection_0 = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")


_gnb_pdu_0 = PduHBTE(addr="10.57.241.160", port_numbers=[4])
_gnb_test_pc_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.91", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_gnb_common_unit_0 = CommonUnit(
    lmp_connection=_gnb_lmp_connection_0,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu_0.pdu_ports[4],
    test_pc=_gnb_test_pc_0,
)

_gnb_airscale_0 = Airscale(common_units=[_gnb_common_unit_0])


_gnb_du_0 = DU(
    airscale=_gnb_airscale_0,
    rus=[_ru1, _ru2],
    f1_m_ip_addr="10.57.236.163",
)

##CU
_gnb_cu_0 = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.236.163", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.236.163", username="Nemuadmin", password="nemuuser"
    ),
)

##dcap
_dcap_1 = DcapBasic(
    connection_details=HttpConnectionDetails(
        addr="10.101.60.40", port="443", username="dcapuser", password="dcapadmin!"
    )
)

##cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB1"

# classicalbts
_classical_bts_0 = ClassicalBts(
    dus=[_gnb_du_0], cu=_gnb_cu_0, global_bts_id=857, instance_id=857, dcap=_dcap_1
)

_ue_host_ssh = SshServiceDetails(
    addr="10.57.239.51", username="spark", password="spark"
)

_appserver_ssh = SshServiceDetails(
    addr="10.57.191.238", username="vrf3_sg6", password="vrf3@sg6"
)

_appserver_ssh_0 = SshServiceDetails(
    addr="10.57.191.238", username="vrf3_sg6", password="vrf3@sg6", port=51857
)

_appserver_ssh_1 = SshServiceDetails(
    addr="10.57.191.238", username="vrf3_sg6", password="vrf3@sg6", port=52857
)

_appserver_ssh_2 = SshServiceDetails(
    addr="10.57.191.238", username="vrf3_sg6", password="vrf3@sg6", port=53857
)

_iperf0 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh_0,
    network_interface_address="10.57.191.238",
    iperf_path="/usr/bin/iperf",
    port=55857,
)

_iperf1 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh_1,
    network_interface_address="10.57.191.238",
    iperf_path="/usr/bin/iperf",
    port=56857,
)

_iperf2 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh_2,
    network_interface_address="10.57.191.238",
    iperf_path="/usr/bin/iperf",
    port=57857,
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.238",
    iperf_path="/usr/bin/iperf",
    port=57857,
)

_appserver = AppServer(_iperf)
_appserver.iperf_details.port = 58000

# CI_Detail_UE_Type='Huawei honor 30s'
_android_0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.34", username="nokia5G", password="noki@123"
    ),
    serial_number="QKXUT20422012341",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf0,
    capabilities=["REAL_ANDROID_UE", "huawei"],
)

_android_3 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.34", username="nokia5G", password="noki@123"
    ),
    serial_number="20aca6bb",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "askey"],
)

_netact = Netact("10.107.178.214")
tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts_0],
    enbs=[],
    tl_cloud_topology=_tl_cloud_topology,
    nms=_netact,
    appserver=_appserver,
    ues=[
        _android_0,
        _android_3,
    ],
    attenuator=[_attenuator],
)
