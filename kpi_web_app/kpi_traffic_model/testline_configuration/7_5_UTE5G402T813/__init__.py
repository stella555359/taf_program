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

__maintainer__ = "Liu Tingting"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_6_GMS <I_MN_5G_RAN_IV4_LINE_HZG_6@internal.nsn.com>"
)
__email__ = "tingting.1.liu@nokia-sbell.com"


# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# mtk
# _ue_host_ssh = SshServiceDetails(
#     addr="10.57.150.141", username="nokia5G", password="noki@123"
# )

# host
# _host = TestPc(
#     default_ssh_connection_details=SshServiceDetails(
#         addr="10.57.155.152", username="ute", password="iW_K#8.ute%A10h0m0ra"
#     )
# )

# #pdn
_pdns = [
    PDN(PDPTypes.IPV4V6.value, "dxdata2"),
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
_realcore = RealCore(five_g=_real_5g_core_details, mcc="310", mnc="260", pdns=_pdns)

# Iperf_Qualcomm X65
_appserver_ssh = SshServiceDetails(
    addr="10.57.191.248", username="vrf4_sg6", password="vrf4@sg6", port="56583"
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.248",
    iperf_path="iperf",
    port="56483",
)

# Iperf_mtk
_appserver_ssh_1 = SshServiceDetails(
    addr="10.57.191.248", username="vrf4_sg6", password="vrf4@sg6", port="57813"
)
_iperf_1 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh_1,
    network_interface_address="10.57.191.248",
    iperf_path="iperf",
    port="57013",
)

# Iperf_mtk_1
_appserver_ssh_2 = SshServiceDetails(
    addr="10.57.191.248", username="vrf4_sg6", password="vrf4@sg6", port="58813"
)
_iperf_2 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh_2,
    network_interface_address="10.57.191.248",
    iperf_path="/cygdrive/c",
    port="58013",
)

# Iperf_Qualcomm X55
_appserver_ssh = SshServiceDetails(
    addr="10.57.191.248", username="vrf4_sg6", password="vrf4@sg6", port="59813"
)
_iperf_3 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.248",
    iperf_path="iperf",
    port="59013",
)

_appserver = AppServer(_iperf)

# Qualcomm X65
# _android = Android(
#     ssh_connection_details=SshServiceDetails(
#         addr="10.57.130.26", username="nokia5G", password="noki@123"
#     ),
#     serial_number="d9bfca57",
#     server_dir="/cygdrive/c/pyro_server",
#     python_path="C:/Python27/python.exe",
#     qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
#     diag_cfg_path="C:/pyro_server/DIAG.cfg",
#     iperf_details=_iperf,
#     imsi="310260100008744",
#     capabilities=["REAL_ANDROID_UE", "qct_dx50"],
#     network_mode_switch_method="keyevents",
#     # mobile_network_text="Mobile network",
#     mobile_network_text="SIMs",
#     setting_network_mode_text="Preferred network type",
# )

# Qualcomm X85
_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.26", username="mn5gran", password="nokia123@"
    ),
    serial_number="30efec9d",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    imsi="310260100008744",
    capabilities=["REAL_ANDROID_UE", "qct_dx50"],
    network_mode_switch_method="keyevents",
    # mobile_network_text="Mobile network",
    mobile_network_text="SIMs",
    setting_network_mode_text="Preferred network type",
)
# Qualcomm X65
_android_1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.7", username="mn5gran", password="nokia123@"
    ),
    serial_number="2af32376",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    imsi="310260100010824",
    capabilities=["REAL_ANDROID_UE1", "qct_dx50"],
    network_mode_switch_method="keyevents",
    # mobile_network_text="Mobile network",
    mobile_network_text="SIMs",
    setting_network_mode_text="Preferred network type",
)
# MTK70
_mtk = MediaTek(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.7", username="mn5gran", password="nokia123@"
    ),
    serial_number="0123456789ABCDEF",
    server_dir="c:/pyro_server",
    server_port=8080,
    edb_file_path="auto",
    apn_url="dxdata2",
    iperf_details=_iperf_1,
    imsi="310260100008740",
    imei="0123456789ABCDEF",
    capabilities=["REAL_MEDIATEK_UE", "mtk"],
)

# MTK
_mtk_1 = MediaTek(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.90", username="nokia5G", password="noki@123"
    ),
    server_dir="c:/pyro_server",
    server_port=8080,
    edb_file_path="auto",
    imei="0123456789ABCDEF",
    imsi="310260100008447",
    apn_url="dxdata2",
    iperf_details=_iperf_2,
    capabilities=["REAL_MEDIATEK_UE", "mtk"],
    serial_number="0123456789ABCDEF",
)

# Qualcomm X55
_android_2 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.11", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="a9f1ce77",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf_3,
    imsi="310260100008737",
    capabilities=["REAL_ANDROID_UE2", "qct_dx50"],
    network_mode_switch_method="keyevents",
    # mobile_network_text="Mobile network",
    mobile_network_text="SIMs",
    setting_network_mode_text="Preferred network type",
)

_ue_host_ssh_dingli = SshServiceDetails(
    addr="10.57.156.24", username="root", password="123456"
)
# CI_Detail_UE_Type='Qualcomm;Qualcomm'
_sigspark_1 = Android(
    ssh_connection_details=_ue_host_ssh_dingli,
    serial_number="38287075",
    server_dir="D:\Program Files (x86)\DingLi\Pilot PioneerX11.0.9.0---09241107\Pioneer.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    capabilities=["pioneer", "huawei_sigspark"],
    imsi="262033100012216",
)

_sigspark_2 = Android(
   ssh_connection_details=_ue_host_ssh_dingli,
   serial_number="19054461",
   server_dir="DD:\Program Files (x86)\DingLi\Pilot PioneerX11.0.9.0---09241107\Pioneer.exe",
   python_path="C:/Python27",
   iperf_details=_iperf,
   capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
   imsi="262033100012217",
)

_sigspark_3 = Android(
    ssh_connection_details=_ue_host_ssh_dingli,
    serial_number="39362191",
    server_dir="D:\Program Files (x86)\DingLi\Pilot PioneerX11.0.9.0---09241107\Pioneer.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_1,
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="262033100012211",
)
_sigspark_4 = Android(
    ssh_connection_details=_ue_host_ssh_dingli,
    serial_number="28240829",
    server_dir="D:\Program Files (x86)\DingLi\Pilot PioneerX11.0.9.0---09241107\Pioneer.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_1,
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="262033100012212",
)
_sigspark_5 = Android(
    ssh_connection_details=_ue_host_ssh_dingli,
    serial_number="2fbc2b8f",
    server_dir="D:\Program Files (x86)\DingLi\Pilot PioneerX11.0.9.0---09241107\Pioneer.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_1,
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="262033100012213",
)
_sigspark_6 = Android(
    ssh_connection_details=_ue_host_ssh_dingli,
    serial_number="2fbc2b8f",
    server_dir="D:\Program Files (x86)\DingLi\Pilot PioneerX11.0.9.0---09241107\Pioneer.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_1,
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="262033100012210",
)
# Qualcomm_Spark
# _sigspark = Android(
#     ssh_connection_details=SshServiceDetails(
#         addr="10.57.130.26", username="nokia5G", password="noki@123"
#     ),
#     serial_number="7d69ea",
#     server_dir="C:/Program Files (x86)/Spark1.1.2003.11/Bin/Spark.exe",
#     python_path="C:/Python27",
#     iperf_details=_iperf,
#     imsi="310260100008444",
#     capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
#     network_mode_switch_method="keyevents",
# )


# RealEnb
_real_enb_pdu = pdu_HBTE(addr="10.57.172.12", port_numbers=[5])

_common_unit_6 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.223.39", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[5],
)

_real_enb = Airscale(common_units=[_common_unit_6])

_lte_real_enb = RealEnb(
    airscale=_real_enb, rms=None, instance_id=8132, global_bts_id=8132
)

# Real ENB2
_real_enb1_pdu = pdu_HBTE(addr="10.57.172.12", port_numbers=[5])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.243.171", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb1_pdu.pdu_ports[5],
    test_pc=None,
    hardware_type=None,
)

_real_enb1 = Airscale(common_units=[_common_unit_2])

_lte_real_enb1 = RealEnb(
    airscale=_real_enb1,
    oam_ip=NetworkAddress(v4="10.57.243.171"),
    system_module=_real_enb1,
    rms=None,
    instance_id=8131,
    global_bts_id=8131,
)
# 5GRU for classicalBTS
# attenuator
_attenuator = HBTE(
    ip_addr="10.57.156.18",
    port=5000,
    attenuation_port_numbers=[1, 2, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    model="PA-16-16-6-127-0.5-B-S",
)

_attenuator1 = HBTE(
    ip_addr="10.57.156.19",
    port=5000,
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    model="PA-16-16-6-127-0.5-B-S",
)

# _attenuator2 = HBTE(
#     ip_addr="10.57.152.220",
#     port=5000,
#     attenuation_port_numbers=[5, 6, 7, 8],
#     model="PA-16-16-6-127-0.5-B-S",
# )

_ru_pdu_0 = FPFH(addr="10.57.172.13", port_numbers=[6])

_ru_0 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.177",
        username="serviceuser",
        password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu_0.pdu_ports[6],
    radio_type=RadioTypes.AVHA.value,
    serial_number="L1250405975",
    attenuation_ports=[
        _attenuator1.attenuator_ports[5],
        _attenuator1.attenuator_ports[6],
        _attenuator1.attenuator_ports[7],
        _attenuator1.attenuator_ports[8],
    ],
)

_ru_pdu_1 = FPFH(addr="10.57.172.13", port_numbers=[1])

_ru_1 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.73.128",
        username="serviceuser",
        password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.73.128", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu_1.pdu_ports[1],
    radio_type=RadioTypes.AVHA.value,
    serial_number="L1250405973",
    attenuation_ports=[
        _attenuator1.attenuator_ports[9],
        _attenuator1.attenuator_ports[10],
        _attenuator1.attenuator_ports[11],
        _attenuator1.attenuator_ports[12],
    ],
)

_ru_pdu_2 = pdu_HBTE(addr="10.57.172.18", port_numbers=[3])

_ru_2 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.209",
        username="serviceuser",
        password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu_2.pdu_ports[3],
    radio_type=RadioTypes.AVHA.value,
    serial_number="L1250405972",
    attenuation_ports=[
        _attenuator1.attenuator_ports[13],
        _attenuator1.attenuator_ports[14],
        _attenuator1.attenuator_ports[15],
        _attenuator1.attenuator_ports[16],
    ],
)

_ru_pdu_3 = FPFH(addr="10.57.172.13", port_numbers=[3])

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
    pdu_port=_ru_pdu_3.pdu_ports[3],
    radio_type=RadioTypes.AHLOB.value,
    serial_number="BL2243D50WL",
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
    ],
)

_ru_pdu_4 = FPFH(addr="10.57.172.13", port_numbers=[4])

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
    pdu_port=_ru_pdu_4.pdu_ports[4],
    radio_type=RadioTypes.AHLOB.value,
    serial_number="BL2244D50Y7",
    attenuation_ports=[
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[6],
    ],
)

_ru_pdu_5 = pdu_HBTE(addr="10.57.172.12", port_numbers=[4])

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
    pdu_port=_ru_pdu_5.pdu_ports[4],
    radio_type=RadioTypes.AHLOB.value,
    serial_number="BL2244D50YA",
    attenuation_ports=[
        _attenuator.attenuator_ports[13],
        _attenuator.attenuator_ports[14],
    ],
)

_ru_pdu_6 = pdu_HBTE(addr="10.57.172.12", port_numbers=[3])

_ru_6 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.209", username="root", password="a2%FgSz3$fHmdusap354xujw7a"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu_6.pdu_ports[3],
    radio_type=RadioTypes.AHFIG.value,
    serial_number="BL2137W2PMP",
    attenuation_ports=[
        _attenuator.attenuator_ports[9],
        _attenuator.attenuator_ports[10],
        _attenuator.attenuator_ports[11],
        _attenuator.attenuator_ports[12],
    ],
)

_ru_pdu_7 = pdu_HBTE(addr="10.57.172.11", port_numbers=[5])

_ru_7 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.209", username="root", password="a2%FgSz3$fHmdusap354xujw7a"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu_7.pdu_ports[5],
    radio_type=RadioTypes.AHFIG.value,
    serial_number="BL2050W2LG3",
    attenuation_ports=[
        _attenuator1.attenuator_ports[1],
        _attenuator1.attenuator_ports[2],
        _attenuator1.attenuator_ports[3],
        _attenuator1.attenuator_ports[4],
    ],
)

_ru_pdu_8 = pdu_HBTE(addr="10.57.172.8", port_numbers=[6])

_ru_8 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.209", username="root", password="a2%FgSz3$fHmdusap354xujw7a"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu_8.pdu_ports[6],
    radio_type=RadioTypes.AHFIG.value,
    serial_number="BL2233W2DIU",
    attenuation_ports=[
        _attenuator.attenuator_ports[7],
        _attenuator.attenuator_ports[8],
        _attenuator.attenuator_ports[15],
        _attenuator.attenuator_ports[16],
    ],
)

_ru_pdu_9 = FPFH(addr="10.57.172.2", port_numbers=[1])
_ru_9 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.209", username="root", password="a2%FgSz3$fHmdusap354xujw7a"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu_9.pdu_ports[1],
    radio_type=RadioTypes.AHFIG.value,
    serial_number="BL2233W2DD6",
    attenuation_ports=[
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[6],
    ],
)

_ru_pdu_10 = FPFH(addr="10.57.172.5", port_numbers=[1])
_ru_10 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.209", username="root", password="a2%FgSz3$fHmdusap354xujw7a"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu_10.pdu_ports[1],
    radio_type=RadioTypes.AHFIG.value,
    serial_number="BL2137W2PMV",
    attenuation_ports=[
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[6],
    ],
)

_ru_pdu_11 = FPFH(addr="10.57.172.34", port_numbers=[1])
_ru_11 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.209", username="root", password="a2%FgSz3$fHmdusap354xujw7a"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu_11.pdu_ports[1],
    radio_type=RadioTypes.AHFIG.value,
    serial_number="BL2233W2DIT",
    attenuation_ports=[
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[6],
    ],
)
# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.57.243.170", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.40")

_gnb_pdu = pdu_HBTE(addr="10.57.172.13", port_numbers=[6])

_gnb_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.152", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_common_unit_4 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[6],
    test_pc=_gnb_test_pc,
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
    ],
    # rus=[_ru_0, _ru_1, _ru_3, _ru_4, _ru_5, _ru_6, _ru_7, _ru_8],
    # rus=[_ru_0, _ru_3, _ru_4, _ru_5, _ru_6, _ru_7, _ru_8],
    # rus=[_ru_0, _ru_1, _ru_3, _ru_4, _ru_5, _ru_6, _ru_7],
    f1_m_ip_addr="10.57.243.170",
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
    backhaul_site_oam_ip=NetworkAddress(v4="10.57.243.170"),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.243.170", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.243.170", username="Nemuadmin", password="nemuuser"
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
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=813, global_bts_id=813)

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.152", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_classical_bts.dus[0].airscale.common_units[0],
            interface_type="lmp",
        ),
        # Connection(
        #     interface="eth1",
        #     device=_lte_real_enb1.system_module.common_units[0],
        #     interface_type="lmp",
        # ),
        _android_2,
    ],
)

_host1 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.108", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_lte_real_enb1.system_module.common_units[0],
            interface_type="lmp",
        ),
        _android_2,
    ],
)

tl = TestLine(
    test_pc=_host,
    test_pcs=[_host, _host1],
    gnbs=[_classical_bts],
    core=_realcore,
    tl_cloud_topology=_tl_cloud_topology,
    enbs=[_lte_real_enb1],
    ues=[_android,
         _android_1,
         _mtk_1,
         _android_2,
         _sigspark_1,
         _sigspark_2,
         _sigspark_3,
         _sigspark_4,
         _sigspark_5,
         _sigspark_6,
         ],
    appserver=_appserver,
    attenuator=[_attenuator, _attenuator1],
)

# old version keyword under robotws5g/resource compatibility workaround
# tl = TestlineWrapper(tl)
