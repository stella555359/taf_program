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
from taf.compatibility.configuration import TestlineWrapper

__maintainer__ = "Pan Yucheng"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_6_GMS <I_MN_5G_RAN_IV4_LINE_HZG_6@internal.nsn.com>"
)
__email__ = "yucheng.pan@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

_optical_switch = Mitron(addr="10.101.36.194", model="OXC1000-32X32-SM-1356-DD-50-LP")
_optical_switch_1 = Mitron(addr="10.101.36.198", model="OXC1000-32X32-SM-1356-DD-50-LP")

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.159.28", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

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

# Iperf
_appserver_ssh_on_qualcomm = SshServiceDetails(
    addr="10.57.191.248", username="vrf4_sg6", password="vrf4@sg6", port="56283"
)
_iperf_details_on_qualcomm = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh_on_qualcomm,
    network_interface_address="10.57.191.248",
    iperf_path="iperf",
    port="56983",
)
_iperf_details_on_qualcomm_1 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh_on_qualcomm,
    network_interface_address="10.57.191.248",
    iperf_path="iperf",
    port="56923",
)
_iperf_details_on_qualcomm_2 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh_on_qualcomm,
    network_interface_address="10.57.191.248",
    iperf_path="iperf",
    port="56924",
)
_iperf_details_on_qualcomm_3 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh_on_qualcomm,
    network_interface_address="10.57.191.248",
    iperf_path="iperf",
    port="56925",
)

_appserver = AppServer(_iperf_details_on_qualcomm)


_appserver_ssh_on_mtk = SshServiceDetails(
    addr="10.57.191.248", username="vrf4_sg6", password="vrf4@sg6", port="56883"
)

_iperf_on_mtk = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh_on_mtk,
    network_interface_address="10.57.191.248",
    iperf_path="/opt/app/iperf",
    port="56783",
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh_on_mtk,
    network_interface_address="10.57.191.248",
    iperf_path="/cygdrive/c",
    port="56783",
)

# # qualcomm SDX80
_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.68.86.243", username="nokia5G", password="noki@123"
    ),
    serial_number="d85cef38",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf_details_on_qualcomm,
    imsi="310260100010824",
    capabilities=["REAL_ANDROID_UE", "qct_dx50"],
    network_mode_switch_method="keyevents",
    # mobile_network_text="Mobile network",
    mobile_network_text="SIMs",
    setting_network_mode_text="Preferred network type",
)

_android_9 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.68.86.243", username="nokia5G", password="noki@123"
    ),
    serial_number="d85cef38",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf_details_on_qualcomm,
    imsi="310260800100625",
    capabilities=["REAL_ANDROID_UE_9", "qct_dx50"],
    network_mode_switch_method="keyevents",
    # mobile_network_text="Mobile network",
    mobile_network_text="SIMs",
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


# MTK M60
_ue_host_ssh_1 = SshServiceDetails(
    addr="10.101.47.6", username="mn5gran", password="nokia123@"
)

_mtk_ue_box = MediaTek(
    ssh_connection_details=_ue_host_ssh_1,
    server_dir="c:/pyro_server",
    server_port=8080,
    edb_file_path="C:/MTK/M60/edb_file/MDDB.EDB",
    log_filter="2.Gen99_Default_Standard",
    imei="0123456789ABCDEF",
    imsi="460023100015279",
    apn_url="dxdata1",
    iperf_details=_iperf,
    capabilities=["REAL_MEDIATEK_UE_1", "mtk"],
    serial_number="0123456789ABCDEF",
)

# # qualcomm SDX60
_android_1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.68.86.2", username="mn5gran", password="nokia123@"
    ),
    serial_number="cc646c7",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf_details_on_qualcomm_1,
    imsi="310260100011562",
    capabilities=["REAL_ANDROID_UE1", "qct_dx50"],
    network_mode_switch_method="keyevents",
    mobile_network_text="SIMs",
    setting_network_mode_text="Preferred network type",
)

# SDX55
_android_2 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.68.86.133", username="nokia5G", password="noki@123"
    ),
    serial_number="a9f1ce77",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf_details_on_qualcomm_1,
    imsi="310260800100625",
    capabilities=["REAL_ANDROID_UE2", "qct_dx50"],
    network_mode_switch_method="keyevents",
    # mobile_network_text="Mobile network",
    mobile_network_text="SIMs",
    setting_network_mode_text="Preferred network type",
)

# SDX55
_android_3 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.68.86.2", username="nokia5G", password="noki@123"
    ),
    serial_number="fc8f3632",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf_details_on_qualcomm_2,
    imsi="310260800100625",
    capabilities=["REAL_ANDROID_UE3", "qct_dx50"],
    network_mode_switch_method="keyevents",
    mobile_network_text="Mobile network",
    # mobile_network_text="SIMs",
    setting_network_mode_text="Preferred network type",
)

# samsung S23
_android_4 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.101.47.103", username="nokia5G", password="noki@123"
    ),
    serial_number="R3CW10X1S1N",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf_details_on_qualcomm_1,
    imsi="310260100008421",
    capabilities=["REAL_ANDROID_UE1", "samsung"],
    network_mode_switch_method="keyevents",
    mobile_network_text="Mobile networks",
    setting_network_mode_text="Network mode",
)

# samsung S22
_android_5 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.101.47.159", username="nokia5G", password="noki@123"
    ),
    serial_number="R5CT3250SWA",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf_details_on_qualcomm_2,
    imsi="310260100008421",
    capabilities=["REAL_ANDROID_UE1", "samsung"],
    network_mode_switch_method="keyevents",
    mobile_network_text="Mobile networks",
    setting_network_mode_text="Network mode",
)

# concurrent_eNB

# 5GRU for classicalBTS
# attenuator
_attenuator = HBTE(
    ip_addr="10.68.88.179",
    port=5000,
    attenuation_port_numbers=[1, 2, 3, 4, 9, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 16],
    model="PA-16-16-6-127-0.5-B-S",
)

_attenuator1 = HBTE(
    ip_addr="10.68.88.178",
    port=5000,
    attenuation_port_numbers=[1, 2, 3, 4, 9, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 16],
    model="PA-16-16-6-127-0.5-B-S",
)

_attenuator2 = HBTE(
    ip_addr="10.101.48.90",
    port=5000,
    attenuation_port_numbers=[1, 2, 3, 4, 9, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 16],
    model="PA-16-16-6-127-0.5-B-S",
)

_attenuator3 = HBTE(
    ip_addr="10.68.88.190",
    port=5000,
    attenuation_port_numbers=[1, 2, 3, 4, 9, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 16],
    model="PA-16-16-6-127-0.5-B-S",
)

_attenuator4 = HBTE(
    ip_addr="10.101.53.53",
    port=5000,
    attenuation_port_numbers=[1, 2, 3, 4],
    model="PA-16-16-6-127-0.5-B-S",
)

# #5GRU for classicalBTS
_ru_pdu_0 = FPFH(addr="10.68.87.68", port_numbers=[5])
_ru_0 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.73.129",
        username="serviceuser",
        password="7B+6yyInfX0uES/FP60uEyhjZHUxB2MoRWvZqUMW42g=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.73.129", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu_0.pdu_ports[5],
    radio_type=RadioTypes.AEHC.value,
    serial_number="L1212614389",
    optical_switch_channels=[
        _optical_switch.modules[21].channels[22],
        _optical_switch.modules[22].channels[21],
        _optical_switch.modules[23].channels[24],
        _optical_switch.modules[24].channels[23],
    ],
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
)

_ru_pdu_1 = pdu_HBTE(addr="10.68.87.88", port_numbers=[5])

_ru_1 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.73.130",
        username="serviceuser",
        password="7B+6yyInfX0uES/FP60uEyhjZHUxB2MoRWvZqUMW42g=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.73.130", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu_1.pdu_ports[5],
    radio_type=RadioTypes.AEHC.value,
    serial_number="L1205002767",
    optical_switch_channels=[
        _optical_switch_1.modules[17].channels[18],
        _optical_switch_1.modules[18].channels[17],
        _optical_switch_1.modules[19].channels[20],
        _optical_switch_1.modules[20].channels[19],
    ],
    attenuation_ports=[
        _attenuator3.attenuator_ports[5],
        _attenuator3.attenuator_ports[6],
        _attenuator3.attenuator_ports[7],
        _attenuator3.attenuator_ports[8],
    ],
)

_ru_pdu_2 = pdu_HBTE(addr="10.101.46.12", port_numbers=[6])

_ru_2 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.73.129",
        username="serviceuser",
        password="7B+6yyInfX0uES/FP60uEyhjZHUxB2MoRWvZqUMW42g=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.73.129", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu_2.pdu_ports[6],
    radio_type=RadioTypes.AEHC.value,
    serial_number="L1211203231",
    optical_switch_channels=[
        _optical_switch.modules[25].channels[26],
        _optical_switch.modules[26].channels[25],
        _optical_switch.modules[27].channels[28],
        _optical_switch.modules[28].channels[27],
    ],
    attenuation_ports=[
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[6],
        _attenuator.attenuator_ports[7],
        _attenuator.attenuator_ports[8],
    ],
)

_ru_pdu_3 = pdu_HBTE(addr="10.68.87.74", port_numbers=[6])

_ru_3 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.73.129",
        username="serviceuser",
        password="WAH26M0DHuXSxpqpUSLmklXrKUfF4iPrXQ+8YULFNuM=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.73.129", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu_3.pdu_ports[6],
    radio_type=RadioTypes.AHLOB.value,
    serial_number="BL2236D50B9",
    attenuation_ports=[
        _attenuator.attenuator_ports[15],
        _attenuator.attenuator_ports[16],
    ],
)

_ru_pdu_4 = pdu_HBTE(addr="10.68.87.75", port_numbers=[5])

_ru_4 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.73.129",
        username="serviceuser",
        password="WAH26M0DHuXSxpqpUSLmklXrKUfF4iPrXQ+8YULFNuM=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.73.129", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu_4.pdu_ports[5],
    radio_type=RadioTypes.AHLOB.value,
    serial_number="BL2236D50BC",
    attenuation_ports=[
        _attenuator.attenuator_ports[13],
        _attenuator.attenuator_ports[14],
    ],
)

_ru_pdu_5 = pdu_HBTE(addr="10.68.87.85", port_numbers=[6])

_ru_5 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.73.129",
        username="serviceuser",
        password="WAH26M0DHuXSxpqpUSLmklXrKUfF4iPrXQ+8YULFNuM=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.73.129", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu_5.pdu_ports[6],
    radio_type=RadioTypes.AHLOB.value,
    serial_number="BL2236D50BB",
    attenuation_ports=[
        _attenuator1.attenuator_ports[1],
        _attenuator1.attenuator_ports[2],
    ],
)

_ru_pdu_6 = FPFH(addr="10.68.87.88", port_numbers=[1])

_ru_6 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.73.129",
        username="serviceuser",
        password="WAH26M0DHuXSxpqpUSLmklXrKUfF4iPrXQ+8YULFNuM=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.73.129", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu_6.pdu_ports[1],
    radio_type=RadioTypes.AHFII.value,
    serial_number="K9245015579",
    attenuation_ports=[
        _attenuator.attenuator_ports[9],
        _attenuator.attenuator_ports[10],
        _attenuator.attenuator_ports[11],
        _attenuator.attenuator_ports[12],
    ],
)

_ru_pdu_7 = pdu_HBTE(addr="10.68.87.75", port_numbers=[2])

_ru_7 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.73.129",
        username="serviceuser",
        password="WAH26M0DHuXSxpqpUSLmklXrKUfF4iPrXQ+8YULFNuM=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.73.129", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu_7.pdu_ports[2],
    radio_type=RadioTypes.AHFII.value,
    serial_number="BL2346N4BNY",
    attenuation_ports=[
        _attenuator1.attenuator_ports[13],
        _attenuator1.attenuator_ports[14],
        _attenuator1.attenuator_ports[15],
        _attenuator1.attenuator_ports[16],
    ],
)

_ru_pdu_8 = pdu_HBTE(addr="10.68.87.71", port_numbers=[6])

_ru_8 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.73.129",
        username="serviceuser",
        password="WAH26M0DHuXSxpqpUSLmklXrKUfF4iPrXQ+8YULFNuM=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.73.129", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu_8.pdu_ports[6],
    radio_type=RadioTypes.AHFII.value,
    serial_number="BL2346N4BYV",
    attenuation_ports=[
        _attenuator1.attenuator_ports[9],
        _attenuator1.attenuator_ports[10],
        _attenuator1.attenuator_ports[11],
        _attenuator1.attenuator_ports[12],
    ],
)

_ru_pdu_9 = pdu_HBTE(addr="10.68.87.178", port_numbers=[4])
_ru_9 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.10.38",
        username="serviceuser",
        password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.10.38", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu_9.pdu_ports[4],
    radio_type=RadioTypes.AVQQA.value,
    serial_number="L1242100642",
    attenuation_ports=[
        _attenuator2.attenuator_ports[1],
        _attenuator2.attenuator_ports[2],
        _attenuator2.attenuator_ports[3],
        _attenuator2.attenuator_ports[4],
    ],
)

_ru_pdu_10 = pdu_HBTE(addr="10.68.87.74", port_numbers=[1])
_ru_10 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.10.7",
        username="serviceuser",
        password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.10.7", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu_10.pdu_ports[1],
    radio_type=RadioTypes.AVQQA.value,
    serial_number="L1241902051",
    attenuation_ports=[
        _attenuator3.attenuator_ports[13],
        _attenuator3.attenuator_ports[14],
        _attenuator3.attenuator_ports[15],
        _attenuator3.attenuator_ports[16],
    ],
)

_ru_pdu_11 = FPFH(addr="10.68.87.68", port_numbers=[2])
_ru_11 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.73.129",
        username="serviceuser",
        password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.73.129", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu_11.pdu_ports[2],
    radio_type=RadioTypes.AVQQA.value,
    serial_number="L1243806286",
)

_ru_pdu_0_1 = FPFH(addr="10.68.87.68", port_numbers=[6])
_ru_0_1 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.73.129",
        username="serviceuser",
        password="bdS%ztWG3v7%SjreCVA79wTPb",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.73.129", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu_0_1.pdu_ports[6],
    radio_type=RadioTypes.AHLOA.value,
    serial_number="BL2118G1DNS",
    attenuation_ports=[
        _attenuator4.attenuator_ports[1],
        _attenuator4.attenuator_ports[2],
        _attenuator4.attenuator_ports[3],
        _attenuator4.attenuator_ports[4],
    ],
)

# DU for classicalBTS
_lmp_connection_0 = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_lmp_connection_1 = SshServiceDetails(
    addr="192.168.255.119", username="toor4nsn", password="oZPS0POrRieRtu"
)

_lmp_connection_2 = SshServiceDetails(
    addr="10.68.88.166", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="10.101.46.68")
_capacity_unit_1 = CapacityUnit(addr="10.68.88.166")

_gnb_pdu = pdu_HBTE(addr="10.68.87.75", port_numbers=[1])
_gnb_pdu_1 = pdu_HBTE(addr="10.68.87.71", port_numbers=[7])

_gnb_test_pc_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.159.28", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_gnb_test_pc_1 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.35", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection_0,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[1],
    test_pc=_gnb_test_pc_0,
)

_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection_1,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[1],
    test_pc=_gnb_test_pc_1,
)

_common_unit_2 = CommonUnit(
    lmp_connection=_lmp_connection_2,
    capacity_units=[_capacity_unit_1],
    pdu_port=_gnb_pdu_1.pdu_ports[7],
)

_airscale = Airscale(common_units=[_common_unit_0, _common_unit_1])
_airscale_1 = Airscale(common_units=[_common_unit_2])

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
    f1_m_ip_addr="10.101.46.68",
)

_du_1 = DU(
    airscale=_airscale_1,
    rus=[
        _ru_0_1,
    ],
    f1_m_ip_addr="10.68.88.166",
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
    backhaul_site_oam_ip=NetworkAddress(v4="10.101.46.68"),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.46.68", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.46.68", username="Nemuadmin", password="nemuuser"
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

_cu_1 = CU(
    backhaul_site_oam_ip=NetworkAddress(v4="10.68.88.166"),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.68.88.166", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.68.88.166", username="Nemuadmin", password="nemuuser"
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

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=283, global_bts_id=283)
_classical_bts_1 = ClassicalBts(
    dus=[_du_1], cu=_cu_1, instance_id=825, global_bts_id=825
)

_lmp_vm_gnb = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.159.28", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_classical_bts.dus[0].airscale.common_units[0],
            interface_type="lmp",
        ),
    ],
)
_tl_cloud_topology = "CLOUD_5G_BB3"

tl = TestLine(
    test_pc=_lmp_vm_gnb,
    test_pcs=[_lmp_vm_gnb],
    gnbs=[_classical_bts, _classical_bts_1],
    core=_realcore,
    tl_cloud_topology=_tl_cloud_topology,
    enbs=[],
    ues=[
        _android,
        _android_1,
        _mtk,
        _android_2,
        _android_3,
        _android_4,
        _android_5,
        _android_9,
        _mtk_ue_box,
    ],
    attenuator=[_attenuator, _attenuator1, _attenuator2, _attenuator3, _attenuator4],
    optical_switches=[_optical_switch, _optical_switch_1],
)
