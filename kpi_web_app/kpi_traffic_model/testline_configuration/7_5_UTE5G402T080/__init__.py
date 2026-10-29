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
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, ATEN, RRB, APC, Gude
from taf.config.testline.pdu import HBTE as pdu_HBTE
from taf.config.testline.pdu import TopYoung as pdu_TopYoung
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

__maintainer__ = "Jiao Jasper"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_6_GMS <I_MN_5G_RAN_IV4_LINE_HZG_6@internal.nsn.com>"
)
__email__ = "jasper.jiao@nokia-sbell.com"


# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.177.88", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_licensekeeper = LicenseKeeper(
    username="xiangsheng.chu@nokia-sbell.com", password="nokia123"
)

# #pdn
_pdns = [
    PDN(PDPTypes.IPV4V6.value, "dxstatic8"),
]

# #realcore5g  # updated 2020/02/10
_amf_oam_ssh_connection_details = SshServiceDetails(
    addr="10.110.66.198", username="test", password="Nokia456"
)
_n2_address = NetworkAddress(v4="10.0.0.0", v6="100:00::000", vlan_id=1)
_amf = AMF(oam_ssh_connection_details=_amf_oam_ssh_connection_details, n2=_n2_address)
_real_5g_core_details = RealCore5GDetails(amf=_amf)

# #realcore5g
_realcore = RealCore(five_g=_real_5g_core_details, mcc="460", mnc="2", pdns=_pdns)


# Iperf
_iperf_ipv6 = IperfDataTransferDetails(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.207.160",
        username="vrf4_sg6",
        password="vrf4@sg6",
        port="56081",
    ),
    network_interface_address="10.71.207.160",
    iperf_path="/data/local/tmp/iperf",
    port="56181",
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.207.160",
        username="vrf4_sg6",
        password="vrf4@sg6",
        port="56080",
    ),
    network_interface_address="10.71.207.160",
    iperf_path="/data/local/tmp/iperf",
    port="56180",
)

_iperf_1 = IperfDataTransferDetails(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.207.160",
        username="vrf4_sg6",
        password="vrf4@sg6",
        port="56333",
    ),
    network_interface_address="10.71.207.160",
    iperf_path="/data/local/tmp/iperf",
    port="56444",
)

_iperf_2 = IperfDataTransferDetails(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.207.160",
        username="vrf4_sg6",
        password="vrf4@sg6",
        port="56380",
    ),
    network_interface_address="10.71.207.160",
    iperf_path="/data/local/tmp/iperf",
    port="58480",
)

_iperf_3 = IperfDataTransferDetails(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.207.160",
        username="vrf4_sg6",
        password="vrf4@sg6",
        port="56580",
    ),
    network_interface_address="10.71.207.160",
    iperf_path="/data/local/tmp/iperf",
    port="56680",
)

# #RealEnb1
_real_enb_pdu1 = FACOM(addr="10.71.206.82", port_numbers=[6])

_common_unit_2_1 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.0.183.35", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu1.pdu_ports[6],
)

_real_enb1 = Airscale(common_units=[_common_unit_2_1])

_lte_real_enb1 = RealEnb(
    airscale=_real_enb1, oam_ip=NetworkAddress(v4="10.57.231.5"), rms=None
)

# #RealEnb2
# _real_enb_pdu2 = FACOM(addr="10.71.206.82", port_numbers=[6])
#
# # _common_unit_2_1_2 = CommonUnit(
# #     lmp_connection=SshServiceDetails(
# #         addr="10.101.53.81", username="toor4nsn", password="oZPS0POrRieRtu"
# #     ),
# #     capacity_units=[],
# #     pdu_port=_real_enb_pdu2.pdu_ports[6],
# # )
#
# _real_enb2 = Airscale(common_units=[_common_unit_2_1_2])
#
# _lte_real_enb2 = RealEnb(
#     airscale=_real_enb2, oam_ip=NetworkAddress(v4="10.101.53.81"), rms=None
# )

# #MTK1
_ue_host_ssh = SshServiceDetails(
    addr="10.0.176.16", username="MN5GRAN", password="nokia123@"
)
# MTK 80
_mtk = MediaTek(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.218.25", username="MN5GRAN", password="nokia123@"
    ),
    server_dir="c:/pyro_server",
    server_port=8080,
    edb_file_path="auto",
    log_filter="2.Gen98_Default_Standard",
    imei="0123456789ABCDEF",
    imsi="310260100011581",
    apn_url="dxstatic8",
    iperf_details=_iperf,
    capabilities=["REAL_MEDIATEK_UE", "mtk"],
    serial_number="0123456789ABCDEF",
)
ue_test = MediaTek(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.159.117", username="MN5GRAN", password="nokia123@"
    ),
    server_dir="c:/pyro_server",
    server_port=8080,
    edb_file_path="auto",
    log_filter="2.Gen98_Default_Standard",
    imei="0123456789ABCDEF",
    imsi="310260100011581",
    apn_url="dxstatic8",
    iperf_details=_iperf,
    capabilities=["REAL_MEDIATEK_UE_9", "mtk"],
    serial_number="0123456789ABCDEF",
)

used_for_enb0 = MediaTek(
    ssh_connection_details=SshServiceDetails(
        addr="10.0.183.35", username="MN5GRAN", password="nokia123@"
    ),
    server_dir="c:/pyro_server",
    server_port=8080,
    edb_file_path="auto",
    log_filter="2.Gen98_Default_Standard",
    imei="0123456789ABCDEF",
    imsi="310260100011581",
    apn_url="dxstatic8",
    iperf_details=_iperf,
    capabilities=["REAL_MEDIATEK_UE_10", "mtk"],
    serial_number="0123456789ABCDEF",
)

used_for_enb1 = MediaTek(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.231.163", username="MN5GRAN", password="nokia123@"
    ),
    server_dir="c:/pyro_server",
    server_port=8080,
    edb_file_path="auto",
    log_filter="2.Gen98_Default_Standard",
    imei="0123456789ABCDEF",
    imsi="310260100011581",
    apn_url="dxstatic8",
    iperf_details=_iperf,
    capabilities=["REAL_MEDIATEK_UE_11", "mtk"],
    serial_number="0123456789ABCDEF",
)

# MTK 80
_mtk_1 = MediaTek(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.218.25", username="MN5GRAN", password="nokia123@"
    ),
    server_dir="c:/pyro_server",
    server_port=8080,
    edb_file_path="auto",
    log_filter="2.Gen98_Default_Standard",
    imei="0123456789ABCDEF",
    imsi="310260100011581",
    apn_url="dxstatic8",
    iperf_details=_iperf_3,
    capabilities=["REAL_MEDIATEK_UE", "mtk"],
    serial_number="0123456789ABCDEF",
)

# MTK 70
# _mtk_1 = MediaTek(
#     ssh_connection_details=SshServiceDetails(
#         addr="10.71.217.253", username="nokia5G", password="noki@123"
#     ),
#     server_dir="c:/pyro_server",
#     server_port=8080,
#     edb_file_path="auto",
#     imei="0123456789ABCDEF",
#     imsi="310260100008740",
#     apn_url="dxstatic8",
#     iperf_details=_iperf_1,
#     capabilities=["REAL_MEDIATEK_UE", "mtk"],
#     serial_number="0123456789ABCDEF",
# )

# MTK 70
# _mtk_2 = MediaTek(
#     ssh_connection_details=SshServiceDetails(
#         addr="10.71.217.233", username="nokia5G", password="noki@123"
#     ),
#     server_dir="c:/pyro_server",
#     server_port=8080,
#     edb_file_path="auto",
#     imei="0123456789ABCDEF",
#     imsi="310260100011583",
#     apn_url="dxstatic8",
#     iperf_details=_iperf_2,
#     capabilities=["REAL_MEDIATEK_UE", "mtk"],
#     serial_number="0123456789ABCDEF",
# )

# samsung S23
_android_1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.218.254", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="R3CW201VD5V",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf_3,
    imsi="310260100011562",
    capabilities=["REAL_ANDROID_UE3", "samsung"],
    network_mode_switch_method="keyevents",
    mobile_network_text="Mobile networks",
    setting_network_mode_text="Network mode",
)

_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.0.176.31", username="mn5gran", password="nokia123@"
    ),
    serial_number="a9f1ce77",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf_2,
    imsi="310260100008450",
    capabilities=["REAL_ANDROID_UE", "qct_dx50"],
    network_mode_switch_method="keyevents",
    # mobile_network_text="Mobile network",
    mobile_network_text="SIMs",
    setting_network_mode_text="Preferred network type",
)


# # qualcomm SDX70
_android_2 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.205.135", username="mn5gran", password="nokia123@"
    ),
    serial_number="7469cccb",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf_ipv6,
    imsi="310260100008444",
    capabilities=["REAL_ANDROID_UE9", "qct_dx50"],
    network_mode_switch_method="keyevents",
    mobile_network_text="Mobile network",
    # mobile_network_text="SIMs",
    setting_network_mode_text="Preferred network type",
)
# _sigspark = Android(
#     ssh_connection_details=SshServiceDetails(
#         addr="10.71.205.135", username="MN5GRAN", password="nokia123@"
#     ),
#     serial_number="33487b2b",
#     server_dir="C:/Program Files (x86)/Spark/Bin/Spark.exe",
#     python_path="C:/Python27",
#     iperf_details=_iperf,
#     imsi="460023100017060",
#     licensekeeper=_licensekeeper,
#     capabilities=["REAL_ANDROID_UE0", "huawei_sigspark"],
# )
#
# _sigspark_1 = Android(
#     ssh_connection_details=SshServiceDetails(
#         addr="10.71.205.135", username="MN5GRAN", password="nokia123@"
#     ),
#     serial_number="33487b2b",
#     server_dir="C:/Program Files (x86)/Spark/Bin/Spark.exe",
#     python_path="C:/Python27",
#     iperf_details=_iperf,
#     imsi="460023100009137",
#     licensekeeper=_licensekeeper,
#     capabilities=["REAL_ANDROID_UE1", "huawei_sigspark"],
# )
_sigspark = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.205.132", username="spark", password="spark"
    ),
    serial_number="33487b2b",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.27/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="460023100017060",
    licensekeeper=_licensekeeper,
    capabilities=["REAL_ANDROID_UE0", "huawei_sigspark"],
)

_sigspark_1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.205.132", username="spark", password="spark"
    ),
    serial_number="33487b2b",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.27/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="460023100009137",
    licensekeeper=_licensekeeper,
    capabilities=["REAL_ANDROID_UE10", "huawei_sigspark"],
)

_sigspark_2 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.205.132", username="spark", password="spark"
    ),
    serial_number="33487b2b",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.27/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="460023100017049",
    licensekeeper=_licensekeeper,
    capabilities=["REAL_ANDROID_UE1", "sigspark_multiUE"],
)

_sigspark_3 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.205.132", username="spark", password="spark"
    ),
    serial_number="33487b2b",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.27/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="460023100017047",
    licensekeeper=_licensekeeper,
    capabilities=["REAL_ANDROID_UE2", "sigspark_multiUE"],
)

_sigspark_4 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.205.132", username="spark", password="spark"
    ),
    serial_number="33487b2b",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.27/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="460023100017054",
    licensekeeper=_licensekeeper,
    capabilities=["REAL_ANDROID_UE3", "sigspark_multiUE"],
)

_sigspark_5 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.205.132", username="spark", password="spark"
    ),
    serial_number="33487b2b",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.27/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="460023100017053",
    licensekeeper=_licensekeeper,
    capabilities=["REAL_ANDROID_UE4", "sigspark_multiUE"],
)

_sigspark_6 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.205.132", username="spark", password="spark"
    ),
    serial_number="33487b2b",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.27/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="460023100017052",
    licensekeeper=_licensekeeper,
    capabilities=["REAL_ANDROID_UE5", "sigspark_multiUE"],
)

_sigspark_7 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.205.132", username="spark", password="spark"
    ),
    serial_number="33487b2b",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.27/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="460023100017051",
    licensekeeper=_licensekeeper,
    capabilities=["REAL_ANDROID_UE6", "sigspark_multiUE"],
)

_sigspark_8 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.205.132", username="spark", password="spark"
    ),
    serial_number="33487b2b",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.27/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="460023100017050",
    licensekeeper=_licensekeeper,
    capabilities=["REAL_ANDROID_UE7", "sigspark_multiUE"],
)

_sigspark_9 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.205.132", username="spark", password="spark"
    ),
    serial_number="33487b2b",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.27/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="460023100017048",
    licensekeeper=_licensekeeper,
    capabilities=["REAL_ANDROID_UE8", "sigspark_multiUE"],
)

_mtk_ue_box = MediaTek(
    ssh_connection_details=_ue_host_ssh,
    server_dir="c:/pyro_server",
    server_port=8080,
    edb_file_path="C:/MTK/M60/edb_file/MDDB.EDB",
    log_filter="2.Gen99_Default_Standard",
    imei="0123456789ABCDEF",
    imsi="001013100011544",
    apn_url="dxdata2",
    iperf_details=_iperf,
    capabilities=["REAL_MEDIATEK_UE_2", "mtk"],
    serial_number="0123456789ABCDEF",
)

_sigspark_02 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.205.132", username="spark", password="spark"
    ),
    serial_number="33487b2b",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.27/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="460023100017049",
    licensekeeper=_licensekeeper,
    capabilities=["REAL_ANDROID_UE1", "huawei_sigspark"],
)

_sigspark_03 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.205.132", username="spark", password="spark"
    ),
    serial_number="33487b2b",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.27/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="460023100017047",
    licensekeeper=_licensekeeper,
    capabilities=["REAL_ANDROID_UE2", "huawei_sigspark"],
)

_sigspark_04 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.205.132", username="spark", password="spark"
    ),
    serial_number="33487b2b",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.27/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="460023100017054",
    licensekeeper=_licensekeeper,
    capabilities=["REAL_ANDROID_UE3", "huawei_sigspark"],
)

_sigspark_05 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.205.132", username="spark", password="spark"
    ),
    serial_number="33487b2b",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.27/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="460023100017053",
    licensekeeper=_licensekeeper,
    capabilities=["REAL_ANDROID_UE4", "huawei_sigspark"],
)

_sigspark_06 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.205.132", username="spark", password="spark"
    ),
    serial_number="33487b2b",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.27/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="460023100017052",
    licensekeeper=_licensekeeper,
    capabilities=["REAL_ANDROID_UE5", "huawei_sigspark"],
)

_sigspark_07 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.205.132", username="spark", password="spark"
    ),
    serial_number="33487b2b",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.27/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="460023100017051",
    licensekeeper=_licensekeeper,
    capabilities=["REAL_ANDROID_UE6", "huawei_sigspark"],
)

_sigspark_08 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.205.132", username="spark", password="spark"
    ),
    serial_number="33487b2b",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.27/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="460023100017050",
    licensekeeper=_licensekeeper,
    capabilities=["REAL_ANDROID_UE7", "huawei_sigspark"],
)

_sigspark_09 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.205.132", username="spark", password="spark"
    ),
    serial_number="33487b2b",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.27/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="460023100017048",
    licensekeeper=_licensekeeper,
    capabilities=["REAL_ANDROID_UE8", "huawei_sigspark"],
)


# #RealEnb

# attenuator
_attenuator_1 = HBTE(
    ip_addr="10.71.205.170",
    port=5000,
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    model="PA-16-16-6-127-0.5-B-S",
)

_attenuator_2 = HBTE(
    ip_addr="10.71.205.169",
    port=5000,
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    model="PA-16-16-6-127-0.5-B-S",
)

_attenuator_3 = HBTE(
    ip_addr="10.71.202.99",
    port=5000,
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    model="PA-16-16-6-127-0.5-B-S",
)

_attenuator_4 = HBTE(
    ip_addr="10.71.206.82",
    port=5000,
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    model="PA-16-16-6-127-0.5-B-S",
)

# 5GRU for classicalBTS
_ru_pdu_0 = pdu_TopYoung(addr="10.71.196.134", port_numbers=[1])

_ru_0 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.145",
        username="serviceuser",
        password="7B+6yyInfX0uES/FP60uEyhjZHUxB2MoRWvZqUMW42g=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu_0.pdu_ports[1],
    radio_type=RadioTypes.AEHC.value,
    serial_number="K9220312558",
    attenuation_ports=[
        _attenuator_2.attenuator_ports[11],
        _attenuator_2.attenuator_ports[12],
        _attenuator_2.attenuator_ports[13],
        _attenuator_2.attenuator_ports[14],
    ],
)

_ru_0_1 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.145",
        username="serviceuser",
        password="7B+6yyInfX0uES/FP60uEyhjZHUxB2MoRWvZqUMW42g=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu_0.pdu_ports[1],
    radio_type=RadioTypes.AEHC.value,
    serial_number="L1202407672",
    attenuation_ports=[
        _attenuator_4.attenuator_ports[1],
        _attenuator_4.attenuator_ports[2],
        _attenuator_4.attenuator_ports[3],
        _attenuator_4.attenuator_ports[4],
    ],
)

_ru_1_1 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.145", username="rfsw", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu_0.pdu_ports[1],
    radio_type=RadioTypes.AHLOA.value,
    serial_number="BL2116G1CHL",
    attenuation_ports=[
        _attenuator_4.attenuator_ports[9],
        _attenuator_4.attenuator_ports[10],
        _attenuator_4.attenuator_ports[11],
        _attenuator_4.attenuator_ports[12],
    ],
)

_ru_2_1 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.145", username="rfsw", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu_0.pdu_ports[1],
    radio_type=RadioTypes.AHFIG.value,
    serial_number="BL2233W2DCJ",
    attenuation_ports=[
        _attenuator_4.attenuator_ports[5],
        _attenuator_4.attenuator_ports[6],
        _attenuator_4.attenuator_ports[7],
        _attenuator_4.attenuator_ports[8],
    ],
)
_ru_pdu_1 = pdu_HBTE(addr="10.71.196.132", port_numbers=[4])

_ru_1 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.145",
        username="serviceuser",
        password="7B+6yyInfX0uES/FP60uEyhjZHUxB2MoRWvZqUMW42g=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu_1.pdu_ports[4],
    radio_type=RadioTypes.AEHC.value,
    serial_number="K9221730261",
    attenuation_ports=[
        _attenuator_2.attenuator_ports[1],
        _attenuator_2.attenuator_ports[2],
        _attenuator_2.attenuator_ports[3],
        _attenuator_2.attenuator_ports[4],
    ],
)

_ru_pdu_2 = pdu_HBTE(addr="10.71.196.131", port_numbers=[4])

_ru_2 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.145",
        username="serviceuser",
        password="7B+6yyInfX0uES/FP60uEyhjZHUxB2MoRWvZqUMW42g=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu_2.pdu_ports[4],
    radio_type=RadioTypes.AEHC.value,
    serial_number="K9221730202",
    attenuation_ports=[
        _attenuator_3.attenuator_ports[1],
        _attenuator_3.attenuator_ports[2],
        _attenuator_3.attenuator_ports[3],
        _attenuator_3.attenuator_ports[4],
    ],
)

_ru_pdu_3 = pdu_HBTE(addr="10.71.196.131", port_numbers=[1])

_ru_3 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.209",
        username="rfsw",
        password="0q/7SXKjF2AlAba+yisrCxQiKz1PRJJ0IVDZuh/sOaA=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5",
        username="rfsw",
        password="0q/7SXKjF2AlAba+yisrCxQiKz1PRJJ0IVDZuh/sOaA=",
    ),
    pdu_port=_ru_pdu_3.pdu_ports[1],
    radio_type=RadioTypes.AHLOB.value,
    serial_number="BL2231D5045",
    attenuation_ports=[
        _attenuator_1.attenuator_ports[5],
        _attenuator_1.attenuator_ports[6],
        _attenuator_1.attenuator_ports[11],
        _attenuator_1.attenuator_ports[12],
    ],
)

_ru_pdu_4 = pdu_HBTE(addr="10.71.196.132", port_numbers=[1])

_ru_4 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.209",
        username="rfsw",
        password="0q/7SXKjF2AlAba+yisrCxQiKz1PRJJ0IVDZuh/sOaA=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5",
        username="rfsw",
        password="0q/7SXKjF2AlAba+yisrCxQiKz1PRJJ0IVDZuh/sOaA=",
    ),
    pdu_port=_ru_pdu_4.pdu_ports[1],
    radio_type=RadioTypes.AHLOB.value,
    serial_number="BL2231D5040",
    attenuation_ports=[
        _attenuator_2.attenuator_ports[5],
        _attenuator_2.attenuator_ports[6],
        _attenuator_2.attenuator_ports[15],
        _attenuator_2.attenuator_ports[16],
    ],
)

_ru_pdu_5 = pdu_HBTE(addr="10.71.196.131", port_numbers=[6])

_ru_5 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.209",
        username="rfsw",
        password="0q/7SXKjF2AlAba+yisrCxQiKz1PRJJ0IVDZuh/sOaA=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5",
        username="rfsw",
        password="0q/7SXKjF2AlAba+yisrCxQiKz1PRJJ0IVDZuh/sOaA=",
    ),
    pdu_port=_ru_pdu_5.pdu_ports[6],
    radio_type=RadioTypes.AHLOB.value,
    serial_number="BL2231D503Y",
    attenuation_ports=[
        _attenuator_3.attenuator_ports[5],
        _attenuator_3.attenuator_ports[6],
        _attenuator_3.attenuator_ports[11],
        _attenuator_3.attenuator_ports[12],
    ],
)

_ru_pdu_6 = pdu_HBTE(addr="10.71.196.130", port_numbers=[5])

_ru_6 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.209",
        username="rfsw",
        password="0q/7SXKjF2AlAba+yisrCxQiKz1PRJJ0IVDZuh/sOaA=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5",
        username="rfsw",
        password="0q/7SXKjF2AlAba+yisrCxQiKz1PRJJ0IVDZuh/sOaA=",
    ),
    pdu_port=_ru_pdu_6.pdu_ports[5],
    radio_type=RadioTypes.AHFII.value,
    serial_number="BL2317N44Z6",
    attenuation_ports=[
        _attenuator_1.attenuator_ports[7],
        _attenuator_1.attenuator_ports[8],
        _attenuator_1.attenuator_ports[9],
        _attenuator_1.attenuator_ports[10],
    ],
)

_ru_pdu_7 = pdu_HBTE(addr="10.71.196.130", port_numbers=[6])

_ru_7 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.209",
        username="rfsw",
        password="0q/7SXKjF2AlAba+yisrCxQiKz1PRJJ0IVDZuh/sOaA=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5",
        username="rfsw",
        password="0q/7SXKjF2AlAba+yisrCxQiKz1PRJJ0IVDZuh/sOaA=",
    ),
    pdu_port=_ru_pdu_7.pdu_ports[6],
    radio_type=RadioTypes.AHFII.value,
    serial_number="BL2224N40AJ",
    attenuation_ports=[
        _attenuator_2.attenuator_ports[7],
        _attenuator_2.attenuator_ports[8],
        _attenuator_2.attenuator_ports[9],
        _attenuator_2.attenuator_ports[10],
    ],
)

_ru_pdu_8 = pdu_HBTE(addr="10.71.196.130", port_numbers=[1])

_ru_8 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.209",
        username="rfsw",
        password="0q/7SXKjF2AlAba+yisrCxQiKz1PRJJ0IVDZuh/sOaA=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5",
        username="rfsw",
        password="0q/7SXKjF2AlAba+yisrCxQiKz1PRJJ0IVDZuh/sOaA=",
    ),
    pdu_port=_ru_pdu_8.pdu_ports[1],
    radio_type=RadioTypes.AHFII.value,
    serial_number="BL2223N408Y",
    attenuation_ports=[
        _attenuator_2.attenuator_ports[7],
        _attenuator_2.attenuator_ports[8],
        _attenuator_2.attenuator_ports[9],
        _attenuator_2.attenuator_ports[10],
    ],
)

# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.0.183.26", username="toor4nsn", password="oZPS0POrRieRtu"
)
_lmp_connection_1 = SshServiceDetails(
    addr="10.0.183.34", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(addr="10.0.183.26")
_capacity_unit_1 = CapacityUnit(addr="10.0.183.34")
_gnb_pdu = pdu_HBTE(addr="10.71.196.132", port_numbers=[3])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[3],
)
_common_unit_0_1 = CommonUnit(
    lmp_connection=_lmp_connection_1,
    capacity_units=[_capacity_unit_1],
    pdu_port=_gnb_pdu.pdu_ports[3],
)
_airscale = Airscale(common_units=[_common_unit_0])
_airscale_1 = Airscale(common_units=[_common_unit_0_1])
_du = DU(
    airscale=_airscale,
    rus=[_ru_0, _ru_1, _ru_2, _ru_3, _ru_4, _ru_5, _ru_6, _ru_7, _ru_8],
    f1_m_ip_addr="10.0.183.26",
)

_du_1 = DU(
    airscale=_airscale_1,
    rus=[_ru_0_1, _ru_1_1, _ru_2_1],
    f1_m_ip_addr="10.0.183.34",
)

# #CU_0
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(v4="10.0.183.26"),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.0.183.26", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.0.183.26", username="Nemuadmin", password="nemuuser"
    ),
)

_cu_1 = CU(
    backhaul_site_oam_ip=NetworkAddress(v4="10.0.183.34"),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.0.183.34", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.0.183.34", username="Nemuadmin", password="nemuuser"
    ),
)
# cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"
# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=80, global_bts_id=80)
_classical_bts_1 = ClassicalBts(
    dus=[_du_1], cu=_cu_1, instance_id=282, global_bts_id=282
)

_lmp_vm_gnb = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.177.88", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_classical_bts.dus[0].airscale.common_units[0],
            interface_type="lmp",
        ),
        _android_2,
    ],
    # connections=[]
)


# log server pc
# server_pc = TestPc(
#     default_ssh_connection_details=SshServiceDetails(
#         addr="10.71.205.135", username="MN5GRAN", password="nokia123@"
#     )
# )

tl = TestLine(
    test_pc=_lmp_vm_gnb,
    # test_pcs=[_lmp_vm_gnb, server_pc],
    test_pcs=[_lmp_vm_gnb],
    gnbs=[_classical_bts, _classical_bts_1],
    core=_realcore,
    tl_cloud_topology=_tl_cloud_topology,
    enbs=[_lte_real_enb1],
    #    ues=[_mtk],
    ues=[
        _mtk,
        _android,
        _mtk_1,
        _android_1,
        _sigspark,
        _sigspark_1,
        _sigspark_2,
        _sigspark_3,
        _sigspark_4,
        _sigspark_5,
        _sigspark_6,
        _sigspark_7,
        _sigspark_8,
        _sigspark_9,
        _mtk_ue_box,
        _android_2,
        ue_test,
        used_for_enb0,
        used_for_enb1,
        _sigspark_02,
        _sigspark_03,
        _sigspark_04,
        _sigspark_05,
        _sigspark_06,
        _sigspark_07,
        _sigspark_08,
        _sigspark_09,
    ],
    attenuators=[_attenuator_1, _attenuator_2, _attenuator_3, _attenuator_4],
)

# old version keyword under robotws5g/resource compatibility workaround
# tl = TestlineWrapper(tl)
