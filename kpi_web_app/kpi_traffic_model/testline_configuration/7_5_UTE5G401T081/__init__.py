import os
from taf.config.testline.cloud_hosting import (
    ControlNode,
    NCIR,
    CloudDeployment,
    DeploymentFlavorStack,
    DeploymentNetworkStack,
    DeploymentVnfStack,
    DeploymentSecurityGroupStack,
    ComputeNode,
    OSP,
)
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.core import (
    EPCSim,
    LTEEmuCore,
    PrismaCore,
    RealCore,
    RealCore4GDetails,
    RealCore5GDetails,
    AMF,
    MME,
)
from taf.config.testline.gnb.du import DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, ATEN, RRB, APC, Gude
from taf.config.testline.pdu import HBTE as pdu_HBTE
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import (
    AirphoneCloud,
    Airphone,
    Prisma,
    TM500,
    Qualcomm,
    QualcommUeType,
    Android,
    MediaTek,
)
from taf.config.testline.enb import (
    Enb,
    SimEnb,
    RealEnb,
    LTEEmuEnb,
    PrismaEnb,
    DocomoEnb,
)
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.config.testline.attenuator import (
    AttenuationPort,
    TopYoung,
    JFW,
    HBTE,
    Hytem,
    RadioRack,
)
from taf.config.testline.gnb.networkaddress import NetworkAddress, RoutingInformation
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)
from taf.config.testline.hardware_controller import (
    AmiaFanHardwareController,
    GPSPowerHardwareController,
)
from taf.config.testline.signal_analyzer import KeysightN9935A
from taf.config.testline.nms import Netact
from taf.config.testline.optical_switch import Leoni, Calient
from taf.config.testline.appserver import AppServer
from taf.config.testline.pdn import PDN, PDPTypes

__maintainer__ = "Lin Stella"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_6_GMS <I_MN_5G_RAN_IV4_LINE_HZG_6@internal.nsn.com>"
)
__email__ = "stella.lin@nokia-sbell.com"


# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.207", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# Iperf_qualcomm
_appserver_ssh_on_qualcomm = SshServiceDetails(
    addr="10.57.191.248", username="vrf4_sg6", password="vrf4@sg6", port="56081"
)
_iperf_details_on_qualcomm = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh_on_qualcomm,
    network_interface_address="10.57.191.248",
    iperf_path="/opt/app/iperf",
    port="56481",
)

_appserver_ssh = SshServiceDetails(
    addr="10.57.191.248", username="vrf4_sg6", password="vrf4@sg6", port="56881"
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.248",
    iperf_path="/data/local/tmp/iperf",
    port="56581",
)

_appserver = AppServer(_iperf)

# Oneplus
# _android = Android(
#     ssh_connection_details=SshServiceDetails(
#         addr="10.101.47.159", username="nokia5G", password="noki@123"
#     ),
#     serial_number="4cc393b1",
#     server_dir="/cygdrive/c/pyro_server",
#     python_path="C:/Python27/python.exe",
#     qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
#     diag_cfg_path="C:/pyro_server/DIAG.cfg",
#     iperf_details=_iperf,
#     capabilities=["REAL_ANDROID_UE0", "oneplus"],
# )

# 'Qualcomm UE'
# Iperf
_appserver_ssh = SshServiceDetails(
    addr="10.57.191.248", username="vrf4_sg6", password="vrf4@sg6", port="56081"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.248",
    iperf_path="/usr/bin/iperf",
    port="56181",
)

_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.101.47.159", username="nokia5G", password="noki@123"
    ),
    serial_number="8450fe5d",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_UE1", "qct_dx50"],
)

# samsung
# _android_1 = Android(
#    ssh_connection_details=SshServiceDetails(
#        addr="10.68.86.2", username="nokia5G", password="noki@123"
#    ),
#    serial_number="R5CN20B0SGH",
#    server_dir="/cygdrive/c/pyro_server",
#    python_path="C:/Python27/python.exe",
#    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
#    diag_cfg_path="C:/pyro_server/DIAG.cfg",
#    iperf_details=_iperf,
#    capabilities=["REAL_ANDROID_UE1", "samsung"],
# )

# RealEnb
_real_enb_pdu = pdu_HBTE(addr="10.101.45.175", port_numbers=[1])

_common_unit_6 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.101.53.77", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[1],
)

_real_enb = Airscale(common_units=[_common_unit_6])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=None)

# Real ENB2
_real_enb1_pdu = pdu_HBTE(addr="10.101.45.175", port_numbers=[1])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.101.53.78", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb1_pdu.pdu_ports[1],
)

_real_enb1 = Airscale(common_units=[_common_unit_2])

_lte_real_enb1 = RealEnb(airscale=_real_enb1, rms=None)
# 5GRU for classicalBTS
# attenuator
_attenuator = HBTE(
    ip_addr="10.68.88.179",
    port=5000,
    attenuation_port_numbers=[9, 10, 11, 12],
    model="TAS16T16-51-120-1SDES",
)

_ru_pdu_0 = pdu_HBTE(addr="10.101.45.142", port_numbers=[1])

_ru_0 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.145", username="root", password="a2%FgSz3$fHmdusap354xujw7a"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu_0.pdu_ports[1],
    radio_type=RadioTypes.AEHC.value,
)

_ru_pdu_1 = pdu_HBTE(addr="10.68.87.88", port_numbers=[1])

_ru_1 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.177", username="root", password="a2%FgSz3$fHmdusap354xujw7a"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu_1.pdu_ports[1],
    radio_type=RadioTypes.AEHC.value,
    attenuation_ports=[
        _attenuator.attenuator_ports[9],
        _attenuator.attenuator_ports[10],
        _attenuator.attenuator_ports[11],
        _attenuator.attenuator_ports[12],
    ],
)

_ru_pdu_2 = pdu_HBTE(addr="10.68.87.49", port_numbers=[2])

_ru_2 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.209", username="root", password="a2%FgSz3$fHmdusap354xujw7a"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu_2.pdu_ports[2],
    radio_type=RadioTypes.AEHC.value,
)

# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.101.53.79", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.40")

_gnb_pdu = pdu_HBTE(addr="10.101.45.175", port_numbers=[2])

_common_unit_4 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[2],
)

_airscale = Airscale(common_units=[_common_unit_4])

_du = DU(airscale=_airscale, rus=[_ru_0, _ru_1, _ru_2], f1_m_ip_addr="10.101.53.79")

# #CU
_f1m = NetworkAddress(v4="9.9.1.1", v6="xxxx", vlan_id=1)
_f1c = NetworkAddress(v4="9.9.1.2", v6="xxxx", vlan_id=2)
_f1u = NetworkAddress(v4="9.9.1.3", v6="xxxx", vlan_id=3)
_x2c = NetworkAddress(v4="9.9.2.1", v6="xxxx", vlan_id=1)
_x2u = NetworkAddress(v4="9.9.2.2", v6="xxxx", vlan_id=2)
_s1c = NetworkAddress(v4="9.9.3.1", v6="xxxx", vlan_id=1)
_s1u = NetworkAddress(v4="9.9.3.2", v6="xxxx", vlan_id=2)
_tracing = NetworkAddress(v4="9.9.1.2", v6="xxxx", vlan_id=1)
_cu = CU(
    backhaul_site_oam_ip="192.168.243.170",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.53.79", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.53.79", username="Nemuadmin", password="nemuuser"
    ),
    f1m=_f1m,
    f1c=_f1c,
    f1u=_f1u,
    x2c=_x2c,
    x2u=_x2u,
    s1c=_s1c,
    s1u=_s1u,
    tracing=_tracing,
)

# cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"
# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=81, global_bts_id=81)

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    tl_cloud_topology=_tl_cloud_topology,
    enbs=[_lte_real_enb, _lte_real_enb1],
    ues=[_android],
    appserver=_appserver,
    attenuator=_attenuator,
)

# old version keyword under robotws5g/resource compatibility workaround
# tl = TestlineWrapper(tl)
