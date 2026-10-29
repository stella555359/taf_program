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

__maintainer__ = "Lin Stella"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_6_GMS <I_MN_5G_RAN_IV4_LINE_HZG_6@internal.nsn.com>"
)
__email__ = "stella.lin@nokia-sbell.com"

_licensekeeper = LicenseKeeper(username="HAZ4_SG6", password="HAZ4_SG6")

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))
_optical_switch = Mitron(addr="10.101.36.194", model="OXC1000-32X32-SM-1356-DD-50-LP")

# #pdn
_pdns = [
    PDN(PDPTypes.IPV4V6.value, "wap2nokiacom"),
    PDN(PDPTypes.IPV4V6.value, "dxdata2"),
]

# #realcore5g  # updated 2020/02/10
_amf_oam_ssh_connection_details = SshServiceDetails(
    addr="10.110.227.70", username="test", password="Nokia456"
)
_n2_address = NetworkAddress(v4="10.0.0.0", v6="100:00::000", vlan_id=1)
_amf = AMF(oam_ssh_connection_details=_amf_oam_ssh_connection_details, n2=_n2_address)
_real_5g_core_details = RealCore5GDetails(amf=_amf)

# #realcore5g
_realcore = RealCore(five_g=_real_5g_core_details, mcc="310", mnc="260", pdns=_pdns)

# _topyoung_mcs = mcs(
#     ip_addr="10.68.88.186",
#     port=28888,
#     mcs_port_numbers=[1, 2, 3, 4],
#     model="MCS2338A2-64B16-A4",
#     version="",
# )

# Iperf_qualcomm sdx60
_appserver_ssh_on_qualcomm = SshServiceDetails(
    addr="10.57.191.248", username="vrf4_sg6", password="vrf4@sg6", port="56873"
)
_iperf_details_on_qualcomm = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh_on_qualcomm,
    network_interface_address="10.57.191.248",
    iperf_path="iperf",
    port="56973",
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.207.160",
        username="vrf4_sg6",
        password="vrf4@sg6",
        port="56012",
    ),
    network_interface_address="10.71.207.160",
    iperf_path="/data/local/tmp/iperf",
    port="56212",
)
_appserver_ssh_on_mtk = SshServiceDetails(
    addr="10.57.191.248", username="vrf4_sg6", password="vrf4@sg6", port="56073"
)

_iperf_on_mtk = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh_on_mtk,
    network_interface_address="10.57.191.248",
    iperf_path="/opt/app/iperf",
    port="56773",
)

_appserver = AppServer(_iperf_details_on_qualcomm)

# # qualcomm SDX70
_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.162", username="mn5gran", password="nokia123@"
    ),
    serial_number="2f5b2d48",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf_details_on_qualcomm,
    imsi="460023100020745",
    capabilities=["REAL_ANDROID_UE14", "qct_dx50"],
    network_mode_switch_method="keyevents",
    mobile_network_text="Mobile network",
    # mobile_network_text="SIMs",
    setting_network_mode_text="Preferred network type",
)

# # only for mcs control pc
_mcspc = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.101.47.103", username="nokia5G", password="noki@123"
    ),
    serial_number="7d69ea",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf_details_on_qualcomm,
    imsi="310260100008444",
    capabilities=["dummyue", "qct_dx50"],
    network_mode_switch_method="keyevents",
    mobile_network_text="Mobile network",
    # mobile_network_text="SIMs",
    setting_network_mode_text="Preferred network type",
)

# Iperf_qualcomm sdx55
_appserver_ssh_on_qualcomm1 = SshServiceDetails(
    addr="10.57.191.248", username="vrf4_sg6", password="vrf4@sg6", port="56673"
)
_iperf_details_on_qualcomm1 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh_on_qualcomm1,
    network_interface_address="10.57.191.248",
    iperf_path="iperf",
    port="56573",
)

# # qualcomm SDX65, shared with TL283
_android1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.68.86.243", username="nokia5G", password="noki@123"
    ),
    serial_number="7d69ea",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf_details_on_qualcomm1,
    imsi="310260800100625",
    capabilities=["REAL_UE2", "qct_dx50"],
    network_mode_switch_method="keyevents",
    mobile_network_text="Mobile network",
    # mobile_network_text="SIMs",
    setting_network_mode_text="Preferred network type",
)

# # qualcomm SDX65 on TL73
_android2 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.228", username="mn5gran", password="nokia123@"
    ),
    serial_number="e4156499",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf_details_on_qualcomm,
    imsi="460023100024219",
    capabilities=["REAL_ANDROID_UE1", "qct_dx50"],
    network_mode_switch_method="keyevents",
    mobile_network_text="Mobile network",
    # mobile_network_text="SIMs",
    setting_network_mode_text="Preferred network type",
)

# MTK
_ue_host_ssh = SshServiceDetails(
    addr="10.101.47.180", username="nokia5G", password="noki@123"
)

_mtk = MediaTek(
    ssh_connection_details=_ue_host_ssh,
    server_dir="c:/pyro_server",
    server_port=8080,
    edb_file_path="auto",
    imei="0123456789ABCDEF",
    imsi="310260100010201",
    apn_url="wap2.nokia.com",
    iperf_details=_iperf_on_mtk,
    capabilities=["REAL_MEDIATEK_UE", "mtk"],
    serial_number="0123456789ABCDEF",
)

# # qualcomm SDX60 used spark
_sigspark = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.162", username="mn5gran", password="nokia123@"
    ),
    serial_number="7d69ea",
    server_dir="C:\Program Files (x86)\Spark1.1.2006.7\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_qualcomm,
    imsi="460023100024219",
    licensekeeper=_licensekeeper,
    capabilities=["REAL_ANDROID_UE0", "huawei_sigspark"],
)
# # qualcomm SDX55 used spark
_sigspark1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.228", username="mn5gran", password="nokia123@"
    ),
    serial_number="e4156499",
    server_dir="C:/Program Files (x86)/Spark1.1.2006.7/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_qualcomm,
    imsi="460023100024219",
    licensekeeper=_licensekeeper,
    capabilities=["REAL_ANDROID_UE1", "huawei_sigspark"],
)

_sigspark02 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.156.56", username="spark", password="spark"
    ),
    serial_number="33487b2b",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.24/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="460023100017081",
    licensekeeper=_licensekeeper,
    capabilities=["REAL_ANDROID_UE0", "huawei_sigspark"],
)

_sigspark03 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.156.56", username="spark", password="spark"
    ),
    serial_number="33487b2b",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.24/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="460023100017082",
    licensekeeper=_licensekeeper,
    capabilities=["REAL_ANDROID_UE0", "huawei_sigspark"],
)
_sigspark04 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.156.56", username="spark", password="spark"
    ),
    serial_number="33487b2b",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.24/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="460023100017083",
    licensekeeper=_licensekeeper,
    capabilities=["REAL_ANDROID_UE0", "huawei_sigspark"],
)

_sigspark05 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.156.56", username="spark", password="spark"
    ),
    serial_number="33487b2b",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.24/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="460023100017084",
    licensekeeper=_licensekeeper,
    capabilities=["REAL_ANDROID_UE0", "huawei_sigspark"],
)
_sigspark06 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.156.56", username="spark", password="spark"
    ),
    serial_number="33487b2b",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.24/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="460023100017085",
    licensekeeper=_licensekeeper,
    capabilities=["REAL_ANDROID_UE0", "huawei_sigspark"],
)

_sigspark07 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.156.56", username="spark", password="spark"
    ),
    serial_number="33487b2b",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.24/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="460023100017086",
    licensekeeper=_licensekeeper,
    capabilities=["REAL_ANDROID_UE0", "huawei_sigspark"],
)
_sigspark08 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.156.56", username="spark", password="spark"
    ),
    serial_number="33487b2b",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.24/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="460023100017087",
    licensekeeper=_licensekeeper,
    capabilities=["REAL_ANDROID_UE0", "huawei_sigspark"],
)

_sigspark09 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.156.56", username="spark", password="spark"
    ),
    serial_number="33487b2b",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.24/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="460023100017088",
    licensekeeper=_licensekeeper,
    capabilities=["REAL_ANDROID_UE0", "huawei_sigspark"],
)

_sigspark_2 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.156.56", username="spark", password="spark"
    ),
    serial_number="33487b2b",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.24/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="460023100017081",
    licensekeeper=_licensekeeper,
    capabilities=["REAL_ANDROID_UE1", "sigspark_multiUE"],
)

_sigspark_3 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.156.56", username="spark", password="spark"
    ),
    serial_number="33487b2b",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.24/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="460023100017082",
    licensekeeper=_licensekeeper,
    capabilities=["REAL_ANDROID_UE2", "sigspark_multiUE"],
)

_sigspark_4 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.156.56", username="spark", password="spark"
    ),
    serial_number="33487b2b",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.24/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="460023100017083",
    licensekeeper=_licensekeeper,
    capabilities=["REAL_ANDROID_UE3", "sigspark_multiUE"],
)

_sigspark_5 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.156.56", username="spark", password="spark"
    ),
    serial_number="33487b2b",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.24/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="460023100017084",
    licensekeeper=_licensekeeper,
    capabilities=["REAL_ANDROID_UE4", "sigspark_multiUE"],
)

_sigspark_6 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.156.56", username="spark", password="spark"
    ),
    serial_number="33487b2b",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.24/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="460023100017085",
    licensekeeper=_licensekeeper,
    capabilities=["REAL_ANDROID_UE5", "sigspark_multiUE"],
)

_sigspark_7 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.156.56", username="spark", password="spark"
    ),
    serial_number="33487b2b",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.24/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="460023100017086",
    licensekeeper=_licensekeeper,
    capabilities=["REAL_ANDROID_UE6", "sigspark_multiUE"],
)

_sigspark_8 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.156.56", username="spark", password="spark"
    ),
    serial_number="33487b2b",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.24/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="460023100017087",
    licensekeeper=_licensekeeper,
    capabilities=["REAL_ANDROID_UE7", "sigspark_multiUE"],
)

_sigspark_9 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.156.56", username="spark", password="spark"
    ),
    serial_number="33487b2b",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.24/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="460023100017088",
    licensekeeper=_licensekeeper,
    capabilities=["REAL_ANDROID_UE8", "sigspark_multiUE"],
)

# # Samsung S21
# _sigspark_1 = Android(
#     ssh_connection_details=SshServiceDetails(
#         addr="10.68.86.2", username="nokia5G", password="noki@123"
#     ),
#     serial_number="RFCR10JZ0AZ",
#     server_dir="C:/Program Files (x86)/Spark1.1.2000.16/Bin/Spark.exe",
#     python_path="C:/Python27",
#     iperf_details=_iperf_details_on_qualcomm,
#     imsi="310260800100607",
#     capabilities=["REAL_ANDROID_UE0", "huawei_sigspark"],
# )

# # Samsung S20
# _sigspark_2 = Android(
#     ssh_connection_details=SshServiceDetails(
#         addr="10.68.86.2", username="nokia5G", password="noki@123"
#     ),
#     serial_number="R5CN20JWC6H",
#     server_dir="C:/Program Files (x86)/Spark1.1.2000.16/Bin/Spark.exe",
#     python_path="C:/Python27",
#     iperf_details=_iperf_details_on_qualcomm,
#     imsi="310260100008422",
#     capabilities=["REAL_ANDROID_UE0", "huawei_sigspark"],
# )

# # STU-M UE1
# _sigspark_3 = Android(
#     ssh_connection_details=SshServiceDetails(
#         addr="10.68.86.47", username="nokia5G", password="noki@123"
#     ),
#     serial_number="0420A1012125001",
#     server_dir="C:/Program Files (x86)/Spark1.1.2001.112/Bin/Spark.exe",
#     python_path="C:/Python27",
#     iperf_details=_iperf_details_on_qualcomm,
#     imsi="460023032996636",
#     capabilities=["REAL_ANDROID_UE0", "huawei_sigspark"],
# )

# # STU-M UE2
# _sigspark_4 = Android(
#     ssh_connection_details=SshServiceDetails(
#         addr="10.68.86.47", username="nokia5G", password="noki@123"
#     ),
#     serial_number="0420A1012125002",
#     server_dir="C:/Program Files (x86)/Spark1.1.2001.112/Bin/Spark.exe",
#     python_path="C:/Python27",
#     iperf_details=_iperf_details_on_qualcomm,
#     imsi="310260100008737",
#     capabilities=["REAL_ANDROID_UE0", "huawei_sigspark"],
# )

# attenuator
_attenuator = HBTE(
    ip_addr="10.57.156.51",
    port=5000,
    attenuation_port_numbers=[
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        12,
        13,
        14,
        15,
        16,
    ],
    model="PA-16-16-6-127-0.5-B-S",
)

_attenuator1 = HBTE(
    ip_addr="10.57.156.54",
    port=5000,
    attenuation_port_numbers=[
        1,
        2,
        3,
        4,
        9,
        10,
        13,
        14,
        15,
        16,
    ],
    model="PA-16-16-6-127-0.5-B-S",
)

_attenuator2 = TopYoung(
    ip_addr="10.57.156.55",
    port=28888,
    attenuation_port_numbers=[
        1,
        2,
        3,
        4,
    ],
    model="TAS32B32-0.7G8.4-90-0.5S-DES",
)

# _attenuator3 = HBTE(
#     ip_addr="10.101.53.54",
#     port=5000,
#     attenuation_port_numbers=[
#         1,
#         2,
#         3,
#         4,
#         9,
#         10,
#         13,
#         14,
#         15,
#         16,
#     ],
#     model="PA-16-16-6-127-0.5-B-S",
# )
#
# # attenuator for TL283, used by ue1
# _attenuator2 = HBTE(
#     ip_addr="10.68.88.179",
#     port=5000,
#     attenuation_port_numbers=[1, 2, 3, 4, 9, 10, 11, 12, 15, 16],
#     model="PA-16-16-6-127-0.5-B-S",
# )

# 5GRU for classicalBTS
_ru_pdu_0 = pdu_HBTE(addr="10.57.172.32", port_numbers=[1])

_ru_0 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.145",
        username="serviceuser",
        password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu_0.pdu_ports[1],
    radio_type=RadioTypes.AVHA,
    serial_number="L1250304102",
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
)

# _ru_0_1 = RU(
#     ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
#     default_ssh_connection_details=SshServiceDetails(
#         addr="192.168.254.145", username="serviceuser", password="bdS%ztWG3v7%SjreCVA79wTPb"
#     ),
#     lmp_connection=SshServiceDetails(
#         addr="172.16.1.5", username="root", password="umniedziala"
#     ),
#     pdu_port=_ru_pdu_0.pdu_ports[5],
#     radio_type=RadioTypes.AEHC,
#     serial_number="L1212614389",
#     attenuation_ports=[
#         _attenuator2.attenuator_ports[1],
#         _attenuator2.attenuator_ports[2],
#         _attenuator2.attenuator_ports[3],
#         _attenuator2.attenuator_ports[4],
#     ],
# )

_ru_pdu_1 = pdu_HBTE(addr="10.57.172.29", port_numbers=[3])

_ru_1 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.209",
        username="serviceuser",
        password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu_1.pdu_ports[3],
    radio_type=RadioTypes.AVHA,
    serial_number="L1245003395",
    # attenuation_ports=[
    #     _attenuator.attenuator_ports[13],
    #     _attenuator.attenuator_ports[14],
    #     _attenuator.attenuator_ports[15],
    #     _attenuator.attenuator_ports[16],
    # ],
)

_ru_pdu_2 = FPFH(addr="10.57.172.13", port_numbers=[5])

_ru_2 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.177",
        username="serviceuser",
        password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu_2.pdu_ports[5],
    radio_type=RadioTypes.AVHA,
    serial_number="L1244106478",
    # attenuation_ports=[
    #     _attenuator.attenuator_ports[21],
    #     _attenuator.attenuator_ports[22],
    #     _attenuator.attenuator_ports[23],
    #     _attenuator.attenuator_ports[24],
    # ],
    # optical_switch_channels=[
    #     _optical_switch.modules[26].channels[25],
    #     _optical_switch.modules[25].channels[26],
    #     _optical_switch.modules[28].channels[27],
    #     _optical_switch.modules[27].channels[28],
    #     _optical_switch.modules[30].channels[29],
    #     _optical_switch.modules[29].channels[30],
    #     _optical_switch.modules[32].channels[31],
    #     _optical_switch.modules[31].channels[32],
    # ],
)

_ru_pdu_3 = pdu_HBTE(addr="10.57.172.32", port_numbers=[6])

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
    pdu_port=_ru_pdu_3.pdu_ports[6],
    radio_type=RadioTypes.AHLOB,
    serial_number="BL2243D50WR",
    attenuation_ports=[
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[6],
        _attenuator.attenuator_ports[7],
        _attenuator.attenuator_ports[8],
    ],
)

_ru_pdu_4 = pdu_HBTE(addr="10.57.172.21", port_numbers=[6])

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
    radio_type=RadioTypes.AHLOB,
    serial_number="BL2243D50WK",
    # attenuation_ports=[
    #     _attenuator.attenuator_ports[27],
    #     _attenuator.attenuator_ports[28],
    # ],
)

_ru_pdu_5 = pdu_HBTE(addr="10.57.172.24", port_numbers=[2])

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
    pdu_port=_ru_pdu_5.pdu_ports[2],
    radio_type=RadioTypes.AHLOB,
    serial_number="BL2243D50XF",
    # attenuation_ports=[
    #     _attenuator.attenuator_ports[29],
    #     _attenuator.attenuator_ports[30],
    # ],
)

_ru_pdu_6 = pdu_HBTE(addr="10.57.172.33", port_numbers=[5])

_ru_6 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.209",
        username="serviceuser",
        password="WAH26M0DHuXSxpqpUSLmklXrKUfF4iPrXQ+8YULFNuM=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu_6.pdu_ports[5],
    radio_type=RadioTypes.AHFII,
    serial_number="BL2408N4EKG",
    attenuation_ports=[
        _attenuator.attenuator_ports[9],
        _attenuator.attenuator_ports[10],
        _attenuator.attenuator_ports[11],
        _attenuator.attenuator_ports[12],
    ],
)

_ru_pdu_7 = pdu_HBTE(addr="10.57.172.24", port_numbers=[4])

_ru_7 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.209",
        username="serviceuser",
        password="WAH26M0DHuXSxpqpUSLmklXrKUfF4iPrXQ+8YULFNuM=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu_7.pdu_ports[4],
    radio_type=RadioTypes.AHFII,
    serial_number="BL2408N4EI1",
    attenuation_ports=[
        _attenuator.attenuator_ports[13],
        _attenuator.attenuator_ports[14],
        _attenuator.attenuator_ports[15],
        _attenuator.attenuator_ports[16],
    ],
)

_ru_pdu_8 = pdu_HBTE(addr="10.57.172.21", port_numbers=[5])

_ru_8 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.209",
        username="serviceuser",
        password="WAH26M0DHuXSxpqpUSLmklXrKUfF4iPrXQ+8YULFNuM=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu_8.pdu_ports[5],
    radio_type=RadioTypes.AHFII,
    serial_number="BL2408N4EHK",
    # attenuation_ports=[
    #     _attenuator.attenuator_ports[17],
    #     _attenuator.attenuator_ports[18],
    #     _attenuator.attenuator_ports[19],
    #     _attenuator.attenuator_ports[20],
    # ],
)

_ru9_pdu = pdu_HBTE(addr="10.57.172.21", port_numbers=[2])

_ru_9 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.297",
        username="serviceuser",
        password="WAH26M0DHuXSxpqpUSLmklXrKUfF4iPrXQ+8YULFNuM=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_ru9_pdu.pdu_ports[2],
    radio_type=RadioTypes.AHFII.value,
    serial_number="K9245008202",
)

_ru10_pdu = FPFH(addr="10.57.172.2", port_numbers=[3])

_ru_10 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.297",
        username="serviceuser",
        password="WAH26M0DHuXSxpqpUSLmklXrKUfF4iPrXQ+8YULFNuM=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_ru10_pdu.pdu_ports[3],
    radio_type=RadioTypes.AHFII.value,
    serial_number="K9245015583",
)

_ru11_pdu = FPFH(addr="10.57.172.2", port_numbers=[2])

_ru_11 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.297",
        username="serviceuser",
        password="WAH26M0DHuXSxpqpUSLmklXrKUfF4iPrXQ+8YULFNuM=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_ru11_pdu.pdu_ports[2],
    radio_type=RadioTypes.AHFII.value,
    serial_number="K9245008234",
)

_ru_pdu_12 = pdu_HBTE(addr="10.57.172.21", port_numbers=[3])
_ru_12 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.10.38",
        username="serviceuser",
        password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.10.38", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu_12.pdu_ports[3],
    radio_type=RadioTypes.AVQQA.value,
    serial_number="L1250710366",
    attenuation_ports=[
        _attenuator1.attenuator_ports[1],
        _attenuator1.attenuator_ports[2],
        _attenuator1.attenuator_ports[3],
        _attenuator1.attenuator_ports[4],
    ],
)

_ru_pdu_13 = FPFH(addr="10.57.172.5", port_numbers=[2])
_ru_13 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.10.7",
        username="serviceuser",
        password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.10.7", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu_13.pdu_ports[2],
    radio_type=RadioTypes.AVQQA.value,
    serial_number="L1243807638",
    # attenuation_ports=[
    #     _attenuator3.attenuator_ports[13],
    #     _attenuator3.attenuator_ports[14],
    #     _attenuator3.attenuator_ports[15],
    #     _attenuator3.attenuator_ports[16],
    # ],
)

_ru_pdu_14 = FPFH(addr="10.57.172.5", port_numbers=[3])
_ru_14 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.73.129",
        username="serviceuser",
        password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.73.129", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu_14.pdu_ports[3],
    radio_type=RadioTypes.AVQQA.value,
    serial_number="L1251202482",
)

# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.57.243.172", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.40")

_gnb_pdu = pdu_HBTE(addr="10.57.172.33", port_numbers=[6])

_common_unit_4 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[6],
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
        _ru_9,
        _ru_10,
        _ru_11,
        _ru_12,
        _ru_13,
        _ru_14,
    ],
    f1_m_ip_addr="10.57.243.172",
)

# _du_1 = DU(
#     airscale=_airscale,
#     rus=[
#         _ru_0_1,
#         _ru_1_1,
#         _ru_2_1,
#         _ru_3_1,
#         _ru_4_1,
#         _ru_5_1,
#         _ru_6_1,
#         _ru_7_1,
#         _ru_8_1,
#     ],
#     f1_m_ip_addr="10.101.46.68",
# )

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
    backhaul_site_oam_ip=NetworkAddress(v4="10.57.243.172"),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.243.172", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.243.172", username="Nemuadmin", password="nemuuser"
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

# _cu_1 = CU(
#     backhaul_site_oam_ip=NetworkAddress(v4="10.101.46.68"),
#     oam_ssh_connection_details=SshServiceDetails(
#         addr="10.101.46.68", username="toor4nsn", password="oZPS0POrRieRtu"
#     ),
#     oam_http_connection_details=HttpConnectionDetails(
#         addr="10.101.46.68", username="Nemuadmin", password="nemuuser"
#     ),
#     f1m=_f1m,
#     f1c=_f1c,
#     f1u=_f1u,
#     x2c=_x2c,
#     x2u=_x2u,
#     s1c=_s1c,
#     s1u=_s1u,
#     tracing=_tracing,
# )

# cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"
# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=73, global_bts_id=73)

# _classical_bts_1 = ClassicalBts(
#     dus=[_du_1], cu=_cu_1, instance_id=283, global_bts_id=283
# )

# host
_lmp_vm_gnb = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.177.65", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_classical_bts.dus[0].airscale.common_units[0],
            interface_type="lmp",
        ),
        _android,
    ],
)

tl = TestLine(
    test_pc=_lmp_vm_gnb,
    test_pcs=[_lmp_vm_gnb],
    # gnbs=[_classical_bts, _classical_bts_1],
    gnbs=[_classical_bts],
    core=_realcore,
    tl_cloud_topology=_tl_cloud_topology,
    enbs=[],
    ues=[
        _android2,
        _android1,
        _mtk,
        _sigspark,
        _sigspark1,
        _mcspc,
        _sigspark_2,
        _sigspark_3,
        _sigspark_4,
        _sigspark_5,
        _sigspark_6,
        _sigspark_7,
        _sigspark_8,
        _sigspark_9,
        _android,
        _sigspark02,
        _sigspark03,
        _sigspark04,
        _sigspark05,
        _sigspark06,
        _sigspark07,
        _sigspark08,
        _sigspark09,
    ],
    appserver=_appserver,
    # attenuator=[_attenuator, _attenuator1],
    attenuator=[_attenuator, _attenuator1, _attenuator2],
    # mcses=[_topyoung_mcs],
    optical_switches=[_optical_switch],
)

# old version keyword under robotws5g/resource compatibility workaround
# tl = TestlineWrapper(tl)
