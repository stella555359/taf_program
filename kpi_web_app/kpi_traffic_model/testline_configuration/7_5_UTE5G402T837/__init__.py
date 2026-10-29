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
        addr="10.57.155.20", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_egen_server = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.232.154", username="ute", password="Ut3pa5s#ff97"
    )
)

_attenuator = HBTE(
    ip_addr="10.57.00.00",
    port="5000",
    attenuation_port_numbers=[1, 2, 3, 4],
    model="PA-16-16-6-127-0.5-B-S",
    version=None,
)

# 5GRU for classicalBTS
_ru_1_pdu = FACOM(addr="10.68.87.108", port_numbers=[1])
_ru_1 = RU(
    ru_hw_group="AWHQE",
    serial_number="EB2125R0083",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1",
        username="000",
        password="000",
    ),
    lmp_connection=SshServiceDetails(
        addr="1.1.1.1", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_1_pdu.pdu_ports[1],
)

##DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_1 = CapacityUnit(addr="192.168.253.20")


_gnb_pdu = PduHBTE(addr="10.68.87.106", port_numbers=[5])
_gnb_test_pc_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.20", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit_1],
    pdu_port=_gnb_pdu.pdu_ports[5],
    test_pc=_gnb_test_pc_0,
)

_airscale = Airscale(common_units=[_common_unit_0])


_du = DU(
    airscale=_airscale,
    rus=[_ru_1],
    f1_m_ip_addr="10.68.89.7",
)

##CU
_cu = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.68.89.7", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.68.89.7", username="Nemuadmin", password="nemuuser"
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
_classical_bts = ClassicalBts(
    dus=[_du], cu=_cu, global_bts_id=837, instance_id=837, dcap=_dcap_1
)

_appserver_ssh = SshServiceDetails(
    addr="10.57.191.238", username="vrf3_sg6", password="vrf3@sg6", port="57837"
)

_iperf0 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.238",
    iperf_path="/usr/bin/iperf",
    port=58837,
)

_appserver = AppServer(iperf_details=_iperf0)
_appserver.iperf_details.port = 57837


_android_0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.68.86.000", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="9YS0220818001000",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf0,
    capabilities=["REAL_ANDROID_UE", "HUAWEI"],
)

tl = TestLine(
    test_pc=_host,
    test_pcs=[_egen_server],
    gnbs=[_classical_bts],
    enbs=[],
    tl_cloud_topology=_tl_cloud_topology,
    appserver=_appserver,
    ues=[
        _android_0,
    ],
    attenuator=[_attenuator],
)
