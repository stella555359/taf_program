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
from taf.compatibility.configuration import TestlineWrapper


__maintainer__ = "Pan Yucheng"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_6_GMS <I_MN_5G_RAN_IV4_LINE_HZG_6@internal.nsn.com>"
)
__email__ = "yucheng.pan@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# #host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.112", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# QC Iperf
_appserver_ssh = SshServiceDetails(
    addr="10.57.191.248", username="vrf4_sg6", password="vrf4@sg6", port="56278"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.248",
    iperf_path="/opt/app/iperf",
    port="56378",
)

_iperf_2 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.248",
    iperf_path="/opt/app/iperf",
    port="56478",
)

_iperf_3 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.248",
    iperf_path="/opt/app/iperf",
    port="56578",
)

_iperf_4 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.248",
    iperf_path="/opt/app/iperf",
    port="56678",
)

# MTK UE Iperf
_appserver_ssh2 = SshServiceDetails(
    addr="10.57.191.248", username="vrf4_sg6", password="vrf4@sg6", port="56878"
)

_iperf2 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh2,
    network_interface_address="10.57.191.248",
    iperf_path="/opt/app/iperf",
    port="56978",
)

# Qualcomm
_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.101.47.252", username="nokia5G", password="noki@123"
    ),
    serial_number="e00435bb",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_UE0", "qct_dx50"],
)

# MTK
_ue_host_ssh = SshServiceDetails(
    addr="10.68.86.174", username="mn5gran", password="nokia123@"
)

_ue_host_ssh_dingli = SshServiceDetails(
    addr="10.101.42.194", username="root", password="123456"
)

_mtk = MediaTek(
    ssh_connection_details=_ue_host_ssh,
    server_dir="c:/pyro_server",
    server_port=8080,
    edb_file_path="auto",
    imei="0123456789ABCDEF",
    imsi="310260100008511",
    apn_url="wap2.nokia.com",
    iperf_details=_iperf2,
    capabilities=["REAL_MEDIATEK_UE", "mtk"],
    serial_number="0123456789ABCDEF",
)

_sigspark_1 = Android(
    ssh_connection_details=_ue_host_ssh_dingli,
    serial_number="42a02a28",
    server_dir="D:/Program Files (x86)/Pilot PioneerX11.0.9.0---07041809/Pioneer.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    capabilities=["pioneer", "huawei_sigspark"],
    imsi="460023100012861",
)

_sigspark_2 = Android(
    ssh_connection_details=_ue_host_ssh_dingli,
    serial_number="33b112ae",
    server_dir="D:/Program Files (x86)/Pilot PioneerX11.0.9.0---07041809/Pioneer.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_2,
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="460020100011567",
)

_sigspark_3 = Android(
    ssh_connection_details=_ue_host_ssh_dingli,
    serial_number="f4bfad87",
    server_dir="D:/Program Files (x86)/Pilot PioneerX11.0.9.0---07041809/Pioneer.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_3,
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="460028001006308",
)

_sigspark_4 = Android(
    ssh_connection_details=_ue_host_ssh_dingli,
    serial_number="2f1a3f5e",
    server_dir="D:/Program Files (x86)/Pilot PioneerX11.0.9.0---07041809/Pioneer.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_4,
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="460020100011568",
)

_sigspark_5 = Android(
    ssh_connection_details=_ue_host_ssh_dingli,
    serial_number="6cf1536a",
    server_dir="D:/Program Files (x86)/Pilot PioneerX11.0.9.0---07041809/Pioneer.exe",
    python_path="C:/Python27",
    iperf_details=_iperf2,
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="460023100001218",
)

_sigspark_6 = Android(
    ssh_connection_details=_ue_host_ssh_dingli,
    serial_number="7cccf279",
    server_dir="D:/Program Files (x86)/Pilot PioneerX11.0.9.0---07041809/Pioneer.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="460023100001212",
)

_sigspark_7 = Android(
    ssh_connection_details=_ue_host_ssh_dingli,
    serial_number="7d6254bd",
    server_dir="D:/Program Files (x86)/Pilot PioneerX11.0.9.0---07041809/Pioneer.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="460023100001216",
)


# #Concurrent Enb
_real_enb_pdu = pdu_HBTE(addr="10.101.45.174", port_numbers=[4])
_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.101.53.86", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[4],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=None)

# #Anchor Enb
_anchor_enb_pdu = pdu_HBTE(addr="10.101.45.174", port_numbers=[5])
_common_unit_3 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.101.53.67", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_anchor_enb_pdu.pdu_ports[5],
)

_real_enb1 = Airscale(common_units=[_common_unit_3])

_anchor_enb = RealEnb(airscale=_real_enb1, rms=None)
# #5GRU for classicalBTS
# TopYoung mcs
_attenuator = TopYoung(
    ip_addr="10.101.53.130",
    port=28888,
    attenuation_port_numbers=[1, 2, 3, 4],
    model="MCS2338A2-64B16-A4",
)

_ru = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="rfsw", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.84", username="root", password="umniedziala"
    ),
    radio_type=RadioTypes.AAHF,
    signal_analyzer=None,
)
# #DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.101.42.162", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="10.101.42.162")

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(
    airscale=_airscale,
    rus=[_ru],
    f1_m_ip_addr="10.101.42.162",
)

# #CU
_cu = CU(
    backhaul_site_oam_ip="10.101.42.162",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.42.162", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.42.162", username="Nemuadmin", password="nemuuser"
    ),
)


# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=4294967248, global_bts_id=2147483647)

_tl_cloud_topology = "CLOUD_5G_BB3"

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    tl_cloud_topology=_tl_cloud_topology,
    enbs=[_lte_real_enb, _anchor_enb],
    ues=[_mtk,
        _sigspark_1,
        _sigspark_2,
        _sigspark_3,
        _sigspark_4,
        _sigspark_5,
        _sigspark_6,
        _sigspark_7,],
    attenuator=[_attenuator],
)


# old version keyword under robotws5g/resource compatibility workaround
# tl = TestlineWrapper(tl)
