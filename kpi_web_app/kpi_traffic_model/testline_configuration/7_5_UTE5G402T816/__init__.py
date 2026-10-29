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
from taf.config.testline.pdu import TopYoung as pdu_TopYoung
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
from taf.config.testline.optical_switch import Leoni, Calient, Mitron
from taf.config.testline.appserver import AppServer
from taf.config.testline.pdn import PDN, PDPTypes
from taf.config.testline import LicenseKeeper


__maintainer__ = "Lin Stella"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_6_GMS <I_MN_5G_RAN_IV4_LINE_HZG_6@internal.nsn.com>"
)
__email__ = "stella.lin@nokia-sbell.com"

_licensekeeper = LicenseKeeper(username="lei.jia@nokia-sbell.com", password="nokia123")

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))
_optical_switch = Mitron(addr="10.101.36.194", model="OXC1000-32X32-SM-1356-DD-50-LP")


# #pdn
_pdns = [
    PDN(PDPTypes.IPV4V6.value, "wap2nokiacom"),
]

# #realcore5g  # updated 2020/02/10
_amf_oam_ssh_connection_details = SshServiceDetails(
    addr="10.110.227.70", username="test", password="Nokia456"
)
_n2_address = NetworkAddress(v4="10.0.0.0", v6="100:00::000", vlan_id=1)
_amf = AMF(oam_ssh_connection_details=_amf_oam_ssh_connection_details, n2=_n2_address)
_real_5g_core_details = RealCore5GDetails(amf=_amf)

# #realcore5g
_realcore = RealCore(five_g=_real_5g_core_details, mcc="460", mnc="02", pdns=_pdns)

# Iperf_qualcomm
_appserver_ssh_on_qualcomm = SshServiceDetails(
    addr="10.57.191.248", username="vrf4_sg6", password="vrf4@sg6", port="56816"
)

_iperf_details_on_qualcomm = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh_on_qualcomm,
    network_interface_address="10.57.191.248",
    iperf_path="iperf",
    port="56973",
)

# Iperf_Qualcomm
_appserver_ssh_1 = SshServiceDetails(
    addr="10.57.191.248", username="vrf4_sg6", password="vrf4@sg6", port="56883"
)
_iperf_1 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh_1,
    network_interface_address="10.57.191.248",
    iperf_path="iperf",
    port="57816",
)

_appserver = AppServer(_iperf_details_on_qualcomm)

# Iperf_samsung
_appserver_ssh_2 = SshServiceDetails(
    addr="10.57.191.248", username="vrf4_sg6", password="vrf4@sg6", port="57813"
)
_iperf_2 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh_2,
    network_interface_address="10.57.191.248",
    iperf_path="/data/local/tmp/iperf",
    port="57013",
)

# Qualcomm
_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.68.86.3", username="mn5gran", password="nokia123@"
    ),
    serial_number="e056865d",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf_details_on_qualcomm,
    capabilities=["REAL_ANDROID_UE0", "qct_dx50"],
)

# # qualcomm SDX70
_android_2 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.101.47.111", username="mn5gran", password="nokia123@"
    ),
    serial_number="4589066d",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf_details_on_qualcomm,
    imsi="310260100008444",
    capabilities=["REAL_ANDROID_UE9", "qct_dx50"],
    network_mode_switch_method="keyevents",
    mobile_network_text="Mobile network",
    # mobile_network_text="SIMs",
    setting_network_mode_text="Preferred network type",
)

# samsung
# _android = Android(
#     ssh_connection_details=SshServiceDetails(
#         addr="10.101.47.111", username="nokia5G", password="noki@123"
#     ),
#     serial_number="RFCR40P2N4K",
#     server_dir="/cygdrive/c/pyro_server",
#     python_path="C:/Python27/python.exe",
#     qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
#     diag_cfg_path="C:/pyro_server/DIAG.cfg",
#     iperf_details=_iperf_details_on_qualcomm,
#     capabilities=["REAL_ANDROID_UE0", "samsung"],
# )

# 2UE module
_sigspark = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.101.47.141", username="nokia5G", password="noki@123"
    ),
    serial_number="145b5b48",
    server_dir="C:/Program Files (x86)/Spark1.1.2006.7/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_qualcomm,
    imsi="460023032996636",
    licensekeeper=_licensekeeper,
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.101.47.141", username="nokia5G", password="noki@123"
    ),
    serial_number="c69a08e3",
    server_dir="C:/Program Files (x86)/Spark1.1.2006.7/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_1,
    imsi="460020100011570",
    licensekeeper=_licensekeeper,
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

# samsung S22
# _android_1 = Android(
#     ssh_connection_details=SshServiceDetails(
#         addr="10.101.47.111", username="nokia5G", password="noki@123"
#     ),
#     serial_number="R5CT3250SWA",
#     server_dir="/cygdrive/c/pyro_server",
#     python_path="C:/Python27/python.exe",
#     qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
#     diag_cfg_path="C:/pyro_server/DIAG.cfg",
#     iperf_details=_iperf_2,
#     imsi="310260100010216",
#     capabilities=["REAL_ANDROID_UE1", "samsung"],
#     network_mode_switch_method="keyevents",
#     mobile_network_text="Mobile networks",
#     setting_network_mode_text="Network mode",
# )
# UE1
# _sigspark = Android(
#     ssh_connection_details=SshServiceDetails(
#         addr="10.101.53.85", username="spark", password="spark"
#     ),
#     serial_number="12345",
#     server_dir="C:/Program Files (x86)/Spark1.1.2001.117/Bin/Spark.exe",
#     python_path="C:/Python27",
#     iperf_details=_iperf_details_on_qualcomm,
#     imsi="460023100010143",
#     capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
# )
#
# # UE2
# _sigspark1 = Android(
#     ssh_connection_details=SshServiceDetails(
#         addr="10.101.53.85", username="spark", password="spark"
#     ),
#     serial_number="12345",
#     server_dir="C:/Program Files (x86)/Spark1.1.2001.117/Bin/Spark.exe",
#     python_path="C:/Python27",
#     iperf_details=_iperf_details_on_qualcomm,
#     imsi="460023100010140",
#     capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
# )
#
# # UE3
# _sigspark2 = Android(
#     ssh_connection_details=SshServiceDetails(
#         addr="10.101.53.85", username="spark", password="spark"
#     ),
#     serial_number="12345",
#     server_dir="C:/Program Files (x86)/Spark1.1.2001.117/Bin/Spark.exe",
#     python_path="C:/Python27",
#     iperf_details=_iperf_details_on_qualcomm,
#     imsi="460028001006180",
#     capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
# )

# UE4
# _sigspark3 = Android(
#     ssh_connection_details=SshServiceDetails(
#         addr="10.101.53.85", username="spark", password="spark"
#     ),
#     serial_number="12345",
#     server_dir="C:/Program Files (x86)/Spark1.1.2001.117/Bin/Spark.exe",
#     python_path="C:/Python27",
#     iperf_details=_iperf_details_on_qualcomm,
#     imsi="460023100010138",
#     capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
# )
#
# # UE5
# _sigspark4 = Android(
#     ssh_connection_details=SshServiceDetails(
#         addr="10.101.53.85", username="spark", password="spark"
#     ),
#     serial_number="12345",
#     server_dir="C:/Program Files (x86)/Spark1.1.2001.117/Bin/Spark.exe",
#     python_path="C:/Python27",
#     iperf_details=_iperf_details_on_qualcomm,
#     imsi="460023100010141",
#     capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
# )
#
# # UE6
# _sigspark5 = Android(
#     ssh_connection_details=SshServiceDetails(
#         addr="10.101.53.85", username="spark", password="spark"
#     ),
#     serial_number="12345",
#     server_dir="C:/Program Files (x86)/Spark1.1.2001.117/Bin/Spark.exe",
#     python_path="C:/Python27",
#     iperf_details=_iperf_details_on_qualcomm,
#     imsi="460023100010139",
#     capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
# )
#
# # UE7
# _sigspark6 = Android(
#     ssh_connection_details=SshServiceDetails(
#         addr="10.101.53.85", username="spark", password="spark"
#     ),
#     serial_number="12345",
#     server_dir="C:/Program Files (x86)/Spark1.1.2001.117/Bin/Spark.exe",
#     python_path="C:/Python27",
#     iperf_details=_iperf_details_on_qualcomm,
#     imsi="460028001006180",
#     capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
# )
#
# # UE8
# _sigspark7 = Android(
#     ssh_connection_details=SshServiceDetails(
#         addr="10.101.53.85", username="spark", password="spark"
#     ),
#     serial_number="12345",
#     server_dir="C:/Program Files (x86)/Spark1.1.2001.117/Bin/Spark.exe",
#     python_path="C:/Python27",
#     iperf_details=_iperf_details_on_qualcomm,
#     imsi="460023100010137",
#     capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
# )

# RealEnb
# _real_enb_pdu = pdu_HBTE(addr="10.101.45.174", port_numbers=[8])
#
# _common_unit_6 = CommonUnit(
#     lmp_connection=SshServiceDetails(
#         addr="10.101.53.80", username="toor4nsn", password="oZPS0POrRieRtu"
#     ),
#     capacity_units=[],
#     pdu_port=_real_enb_pdu.pdu_ports[8],
# )
#
# _real_enb = Airscale(common_units=[_common_unit_6])
#
# _lte_real_enb = RealEnb(airscale=_real_enb, rms=None)
#
# # Real ENB2
# _real_enb1_pdu = pdu_HBTE(addr="10.101.45.174", port_numbers=[6])
#
# _common_unit_2 = CommonUnit(
#     lmp_connection=SshServiceDetails(
#         addr="10.101.53.74", username="toor4nsn", password="oZPS0POrRieRtu"
#     ),
#     capacity_units=[],
#     pdu_port=_real_enb1_pdu.pdu_ports[6],
# )
#
# _real_enb1 = Airscale(common_units=[_common_unit_2])
#
# _lte_real_enb1 = RealEnb(airscale=_real_enb1, rms=None, instance_id=816816)
# 5GRU for classicalBTS
# attenuator
_attenuator = HBTE(
    ip_addr="10.101.42.163",
    port=5000,
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    model="PA-16-16-6-127-0.5-B-S",
)

_attenuator_1 = HBTE(
    ip_addr="10.101.42.164",
    port=5000,
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    model="PA-16-16-6-127-0.5-B-S",
)

_ru_pdu_0 = pdu_HBTE(addr="10.101.45.142", port_numbers=[6])

_ru_0 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.177",
        username="serviceuser",
        password="wcdjLlTpqEY3cAmOe11u6aELwGI3rDvpGJQvCkcyHZc=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu_0.pdu_ports[6],
    radio_type=RadioTypes.AZHL.value,
    serial_number="AH211400577",
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
    optical_switch_channels=[
        _optical_switch.modules[14].channels[13],
        _optical_switch.modules[13].channels[14],
        _optical_switch.modules[16].channels[15],
        _optical_switch.modules[15].channels[16],
    ],
)

#_ru_pdu_1 = pdu_HBTE(addr="10.101.45.175", port_numbers=[3])
_ru_pdu_1 = FPFH(addr="10.101.45.170", port_numbers=[3])

_ru_1 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.145",
        username="serviceuser",
        password="wcdjLlTpqEY3cAmOe11u6aELwGI3rDvpGJQvCkcyHZc=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu_1.pdu_ports[3],
    radio_type=RadioTypes.AZHL.value,
    serial_number="YK210500045",
    attenuation_ports=[
        _attenuator.attenuator_ports[9],
        _attenuator.attenuator_ports[10],
        _attenuator.attenuator_ports[11],
        _attenuator.attenuator_ports[12],
        _attenuator_1.attenuator_ports[1],
        _attenuator_1.attenuator_ports[2],
        _attenuator_1.attenuator_ports[3],
        _attenuator_1.attenuator_ports[4],
    ],
)

# _ru_pdu_2 = pdu_HBTE(addr="10.101.45.175", port_numbers=[4])
#
# _ru_2 = RU(
#     ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
#     default_ssh_connection_details=SshServiceDetails(
#         addr="192.168.254.209",
#         username="rfsw",
#         password="5rfS2qmWC0AiFYvir7k8JekCN8/NklqDK5E6OWXuUVQ=",
#     ),
#     lmp_connection=SshServiceDetails(
#         addr="172.16.1.5", username="root", password="umniedziala"
#     ),
#     pdu_port=_ru_pdu_2.pdu_ports[4],
#     radio_type=RadioTypes.AZHL.value,
#     attenuation_ports=[
#         _attenuator.attenuator_ports[13],
#         _attenuator.attenuator_ports[14],
#         _attenuator.attenuator_ports[15],
#         _attenuator.attenuator_ports[16],
#     ],
# )

_ru2_pdu = pdu_HBTE(addr="10.101.45.142", port_numbers=[3])

_ru_2 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.297", username="root", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_ru2_pdu.pdu_ports[3],
    radio_type=RadioTypes.AHLOA.value,
    serial_number="BL2145G1Q6M",
    attenuation_ports=[
        _attenuator.attenuator_ports[13],
        _attenuator.attenuator_ports[14],
        _attenuator.attenuator_ports[15],
        _attenuator.attenuator_ports[16],
    ],
)

_ru3_pdu = pdu_HBTE(addr="10.101.45.142", port_numbers=[1])

_ru_3 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.297", username="root", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_ru3_pdu.pdu_ports[1],
    radio_type=RadioTypes.AHLOA.value,
    serial_number="BL2118G1DPE",
    attenuation_ports=[
        _attenuator_1.attenuator_ports[9],
        _attenuator_1.attenuator_ports[10],
    ],
)

_ru4_pdu = pdu_HBTE(addr="10.101.45.172", port_numbers=[3])

_ru_4 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.297", username="root", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_ru4_pdu.pdu_ports[3],
    radio_type=RadioTypes.AHLOA.value,
    serial_number="BL2118G1DPF",
    attenuation_ports=[
        _attenuator_1.attenuator_ports[13],
        _attenuator_1.attenuator_ports[14],
    ],
)

_ru5_pdu = FPFH(addr="10.101.45.144", port_numbers=[2])

_ru_5 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.297",
        username="serviceuser",
        password="WAH26M0DHuXSxpqpUSLmklXrKUfF4iPrXQ+8YULFNuM=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_ru5_pdu.pdu_ports[2],
    radio_type=RadioTypes.AHFII.value,
    serial_number="K9245008203",
    attenuation_ports=[
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[6],
        _attenuator.attenuator_ports[7],
        _attenuator.attenuator_ports[8],
    ],
)

_ru6_pdu = FPFH(addr="10.101.45.144", port_numbers=[5])

_ru_6 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.297",
        username="serviceuser",
        password="WAH26M0DHuXSxpqpUSLmklXrKUfF4iPrXQ+8YULFNuM=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_ru6_pdu.pdu_ports[5],
    radio_type=RadioTypes.AHFII.value,
    serial_number="K9245008282",
    attenuation_ports=[
        _attenuator_1.attenuator_ports[11],
        _attenuator_1.attenuator_ports[12],
        _attenuator_1.attenuator_ports[15],
        _attenuator_1.attenuator_ports[16],
    ],
)

_ru7_pdu = FPFH(addr="10.101.45.176", port_numbers=[5])

_ru_7 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.297",
        username="serviceuser",
        password="WAH26M0DHuXSxpqpUSLmklXrKUfF4iPrXQ+8YULFNuM=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_ru7_pdu.pdu_ports[5],
    radio_type=RadioTypes.AHFII.value,
    serial_number="K9245015586",
    attenuation_ports=[
        _attenuator_1.attenuator_ports[5],
        _attenuator_1.attenuator_ports[6],
        _attenuator_1.attenuator_ports[7],
        _attenuator_1.attenuator_ports[8],
    ],
)

# _ru8_pdu = FPFH(addr="10.101.46.19", port_numbers=[2])
#
# _ru_8 = RU(
#     ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
#     default_ssh_connection_details=SshServiceDetails(
#         addr="192.168.254.297",
#         username="rfsw",
#         password="WAH26M0DHuXSxpqpUSLmklXrKUfF4iPrXQ+8YULFNuM=",
#     ),
#     lmp_connection=SshServiceDetails(
#         addr="172.16.1.5", username="root", password="umniedziala"
#     ),
#     pdu_port=_ru8_pdu.pdu_ports[2],
#     radio_type=RadioTypes.AHFII.value,
#     serial_number="K9245008234",
# )
#
# _ru9_pdu = FPFH(addr="10.101.46.19", port_numbers=[4])
#
# _ru_9 = RU(
#     ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
#     default_ssh_connection_details=SshServiceDetails(
#         addr="192.168.254.297",
#         username="rfsw",
#         password="WAH26M0DHuXSxpqpUSLmklXrKUfF4iPrXQ+8YULFNuM=",
#     ),
#     lmp_connection=SshServiceDetails(
#         addr="172.16.1.5", username="root", password="umniedziala"
#     ),
#     pdu_port=_ru9_pdu.pdu_ports[4],
#     radio_type=RadioTypes.AHFII.value,
#     serial_number="K9245015583",
# )
#
# _ru10_pdu = pdu_HBTE(addr="10.101.46.20", port_numbers=[1])
#
# _ru_10 = RU(
#     ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
#     default_ssh_connection_details=SshServiceDetails(
#         addr="192.168.254.297",
#         username="rfsw",
#         password="WAH26M0DHuXSxpqpUSLmklXrKUfF4iPrXQ+8YULFNuM=",
#     ),
#     lmp_connection=SshServiceDetails(
#         addr="172.16.1.5", username="root", password="umniedziala"
#     ),
#     pdu_port=_ru10_pdu.pdu_ports[1],
#     radio_type=RadioTypes.AHFII.value,
#     serial_number="K9245008202",
# )

# DU for classicalBTS
_lmp_connection_0 = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_lmp_connection_1 = SshServiceDetails(
    addr="192.168.255.119", username="toor4nsn", password="oZPS0POrRieRtu"
)

_lmp_connection_2 = SshServiceDetails(
    addr="10.101.46.67", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="10.101.46.67")

_gnb_pdu = pdu_HBTE(addr="10.101.45.174", port_numbers=[6])
_gnb_test_pc_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.177.46", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_gnb_test_pc_1 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.159.77", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection_0,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[6],
    test_pc=_gnb_test_pc_0,
)

_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection_1,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[6],
    test_pc=_gnb_test_pc_1,
)

#_common_unit_4 = CommonUnit(
#    lmp_connection=_lmp_connection_2,
#    capacity_units=[_capacity_unit],
#    pdu_port=_gnb_pdu.pdu_ports[6],
#    test_pc=_gnb_test_pc,
#)

_airscale = Airscale(common_units=[_common_unit_0, _common_unit_1])
#_airscale_1 = Airscale(common_units=[_common_unit_4])

_du = DU(
    airscale=_airscale,
    rus=[_ru_0, _ru_1, _ru_2, _ru_3, _ru_4, _ru_5, _ru_6, _ru_7],
    f1_m_ip_addr="10.101.46.67",
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
    backhaul_site_oam_ip=NetworkAddress(v4="10.101.46.67"),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.46.67", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.46.67", username="omc", password="Nokia123!"
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
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=816, global_bts_id=816)


# host
_lmp_vm_gnb = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.177.46", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_classical_bts.dus[0].airscale.common_units[0],
            interface_type="lmp",
        ),
        _android_2,
    ],
)


tl = TestLine(
    test_pc=_lmp_vm_gnb,
    test_pcs=[_lmp_vm_gnb],
    gnbs=[_classical_bts],
    tl_cloud_topology=_tl_cloud_topology,
    enbs=[],
    core=_realcore,
    ues=[_sigspark, _sigspark1, _android, _android_2],
    appserver=_appserver,
    attenuator=[_attenuator, _attenuator_1],
    optical_switches=[_optical_switch],
)

# old version keyword under robotws5g/resource compatibility workaround
# tl = TestlineWrapper(tl)
