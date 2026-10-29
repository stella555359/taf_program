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
from taf.config.testline.testpc import TestPc, Connection
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
from taf.config.testline.pdu import FPFH
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, ATEN, RRB, APC, Gude
from taf.config.testline.pdu import HBTE as pdu_HBTE
from taf.config.testline.testline import TestLine
from taf.config.testline.mcs import TopYoung as mcs
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
from taf.config.testline.optical_switch import Leoni, Calient, Mitron
from taf.config.testline import LicenseKeeper


__maintainer__ = "Qin Wei"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_6_GMS <I_MN_5G_RAN_IV4_LINE_HZG_6@internal.nsn.com>"
)
__email__ = "wei.2.qin@nokia-sbell.com"


# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.177.11", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# pdn
_pdns = [
    PDN(PDPTypes.IPV4V6.value, "weistatic"),
]

# Iperf_qualcomm
_spark_appserver_ssh = SshServiceDetails(
    addr="10.57.179.240", username="ute", password="Ut3pa5s#ff97", port="52761"

)
_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_spark_appserver_ssh,
    network_interface_address="10.57.179.240",
    iperf_path="iperf",
    port="52761",
)

_licensekeeper = LicenseKeeper(username="HAZ4_SG6", password="HAZ4_SG6")

_appserver = AppServer(_iperf_details_on_appserver)

# SIGSPARK
# _ue_host_ssh = SshServiceDetails(
#     addr="10.68.86.184", username="nokia5G", password="noki@123"
# )
_ue_host_ssh = SshServiceDetails(
    addr="10.101.36.239", username="spark", password="spark"
)

# Qualcomm X60
# _android = Android(
#     ssh_connection_details=SshServiceDetails(
#         addr="10.68.86.184", username="nokia5G", password="noki@123"
#     ),
#     serial_number="8450fe5d",
#     server_dir="/cygdrive/c/pyro_server",
#     python_path="C:/Python27/python.exe",
#     qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
#     diag_cfg_path="C:/pyro_server/DIAG.cfg",
#     iperf_details=_iperf_details_on_appserver,
#     imsi="310260100008744",
#     capabilities=["REAL_ANDROID_UE", "qct_dx50"],
#     network_mode_switch_method="keyevents",
#     # mobile_network_text="Mobile network",
#     mobile_network_text="SIMs",
#     setting_network_mode_text="Preferred network type",
# )
# samsung S22
# _android_1 = Android(
#     ssh_connection_details=SshServiceDetails(
#         addr="10.68.86.184", username="nokia5G", password="noki@123"
#     ),
#     serial_number="R3CW201VD5V",
#     server_dir="/cygdrive/c/pyro_server",
#     python_path="C:/Python27/python.exe",
#     qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
#     diag_cfg_path="C:/pyro_server/DIAG.cfg",
#     iperf_details=_iperf_details_on_appserver,
#     imsi="310260100008421",
#     capabilities=["REAL_ANDROID_UE", "samsung"],
#     network_mode_switch_method="keyevents",
#     mobile_network_text="Mobile networks",
#     setting_network_mode_text="Network mode",
# )

# Qualcomm X55
#_android = Android(
#    ssh_connection_details=SshServiceDetails(
#        addr="10.68.86.184", username="nokia5G", password="noki@123"
#    ),
#    serial_number="a9f1ce77",
#    server_dir="/cygdrive/c/pyro_server",
#    python_path="C:/Python27/python.exe",
#    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
#    diag_cfg_path="C:/pyro_server/DIAG.cfg",
#    iperf_details=_iperf_details_on_appserver,
#    imsi="310260100008744",
#    capabilities=["REAL_ANDROID_UE", "qct_dx50"],
#    network_mode_switch_method="keyevents",
#    # mobile_network_text="Mobile network",
#    mobile_network_text="SIMs",
#    setting_network_mode_text="Preferred network type",
#)

_sigspark = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.230.242", username="MTU", password="MTU"
    ),
    serial_number="58152b0",
    server_dir="C:/Spark/Bin/Spark.exe",
    python_path="C:/Python37",
    iperf_details=_iperf_details_on_appserver,
    imsi="460023100007868",
    licensekeeper=_licensekeeper,
    capabilities=["REAL_ANDROID_UE0", "huawei_sigspark"],
)


# #realcore5g
_realcore = RealCore(mcc="460", mnc="2", pdns=_pdns)

# RealEnb
#_real_enb_pdu = pdu_HBTE(addr="10.101.45.175", port_numbers=[5])

_common_unit_6 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.227.195", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
)

#_real_enb = Airscale(common_units=[_common_unit_6])

#_lte_real_enb = RealEnb(airscale=_real_enb, rms=None)

# Real ENB2
#_real_enb1_pdu = pdu_HBTE(addr="10.101.45.175", port_numbers=[2])

#_common_unit_2 = CommonUnit(
#    lmp_connection=SshServiceDetails(
#        addr="10.101.53.83", username="toor4nsn", password="oZPS0POrRieRtu"
#    ),
#    capacity_units=[],
#    pdu_port=_real_enb1_pdu.pdu_ports[2],
#)

#_real_enb1 = Airscale(common_units=[_common_unit_2])

#_lte_real_enb1 = RealEnb(airscale=_real_enb1, rms=None)

# 5GRU for classicalBTS

_topyoung_mcs = mcs(
    ip_addr="10.57.230.243",
    port=28888,
    mcs_port_numbers=[1, 2, 3, 4],
    model="MCS2350A2-128B16-E6",
    version="",
)


_ru_pdu_0 = FPFH(addr="10.57.176.236", port_numbers=[4])
_ru_0 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.209", username="serviceuser", password="WAH26M0DHuXSxpqpUSLmklXrKUfF4iPrXQ+8YULFNuM="
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu_0.pdu_ports[4],
    radio_type=RadioTypes.AHLOB,
    serial_number="AH251802798",
)

_ru_pdu_1 = FPFH(addr="10.57.176.237", port_numbers=[6])

_ru_1 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.209", username="serviceuser", password="WAH26M0DHuXSxpqpUSLmklXrKUfF4iPrXQ+8YULFNuM="
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu_1.pdu_ports[6],
    radio_type=RadioTypes.AHLOB,
    serial_number="AH251802741",
)

_ru_pdu_2 = FPFH(addr="10.57.176.237", port_numbers=[5])

_ru_2 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.209", username="serviceuser", password="WAH26M0DHuXSxpqpUSLmklXrKUfF4iPrXQ+8YULFNuM="
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu_2.pdu_ports[5],
    radio_type=RadioTypes.AHLOB,
    serial_number="AH251802740",
)
# AH251802798
# AH251802741
# AH251802740
# K9245120752
# K9245120903
# K9245120906

_ru_pdu_3 = FPFH(addr="10.57.176.236", port_numbers=[5])

_ru_3 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.209",
        username="serviceuser",
        password="WAH26M0DHuXSxpqpUSLmklXrKUfF4iPrXQ+8YULFNuM=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu_3.pdu_ports[5],
    radio_type=RadioTypes.AHFII,
    serial_number="K9245120752",
)

_ru_pdu_4 = FPFH(addr="10.57.176.236", port_numbers=[6])

_ru_4 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.209",
        username="serviceuser",
        password="WAH26M0DHuXSxpqpUSLmklXrKUfF4iPrXQ+8YULFNuM=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu_4.pdu_ports[6],
    radio_type=RadioTypes.AHFII,
    serial_number="K9245120903",
)

_ru_pdu_5 = FPFH(addr="10.57.176.237", port_numbers=[3])
_ru_5 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.209",
        username="serviceuser",
        password="WAH26M0DHuXSxpqpUSLmklXrKUfF4iPrXQ+8YULFNuM=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu_5.pdu_ports[3],
    radio_type=RadioTypes.AHFII,
    serial_number="K9245120906",
)

# L1250304101
# L1250304103
# L1243403633


_ru_pdu_6 = FPFH(addr="10.57.176.236", port_numbers=[2])

_ru_6 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.145",
        username="serviceuser",
        password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu_6.pdu_ports[2],
    radio_type=RadioTypes.AVHA,
    serial_number="L1250304101",
)


_ru_pdu_7 = FPFH(addr="10.57.176.237", port_numbers=[2])

_ru_7 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.145",
        username="serviceuser",
        password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu_7.pdu_ports[2],
    radio_type=RadioTypes.AVHA,
    serial_number="L1250304103",
)

_ru_pdu_8 = FPFH(addr="10.57.176.236", port_numbers=[1])
_ru_8 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.145",
        username="serviceuser",
        password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu_8.pdu_ports[1],
    radio_type=RadioTypes.AVHA,
    serial_number="L1243403633",
)




# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.57.227.195", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.40")

_gnb_pdu = FPFH(addr="10.57.176.237", port_numbers=[1])

_common_unit_4 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[1],
)

_airscale = Airscale(common_units=[_common_unit_4])

_du = DU(
    airscale=_airscale,
    rus=[
        _ru_0,
        _ru_1,
        _ru_2,
        _ru_3,
        _ru_4,
        _ru_5,
        _ru_6,
        _ru_7,
        _ru_8,
    ],
    f1_m_ip_addr="10.57.227.195",
)

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
    backhaul_site_oam_ip=NetworkAddress(v4="10.57.227.195"),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.227.195", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.227.195", username="Nemuadmin", password="nemuuser"
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


# log server pc
server_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.150.11", username="MN5GRAN", password="nokia123@"
    )
)

# cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"
# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=76, global_bts_id=76)
tl = TestLine(
    test_pc=_host,
    test_pcs=[_host, server_pc],
    gnbs=[_classical_bts],
    core=_realcore,
    tl_cloud_topology=_tl_cloud_topology,
    enbs=[],
    ues=[
        _sigspark,
    ],
    appserver=_appserver,
)

# old version keyword under robotws5g/resource compatibility workaround
# tl = TestlineWrapper(tl)
