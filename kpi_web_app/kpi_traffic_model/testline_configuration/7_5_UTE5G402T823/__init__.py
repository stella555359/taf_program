import os
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
from taf.config.testline.pdu import TopYoung as pdu_TopYoung
from taf.config.testline import TopYoung_PDU
from taf.config.testline import HBTE_PDU
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
from taf.config.testline.appserver import AppServer
from taf.config.testline.pdn import PDN, PDPTypes

__maintainer__ = "Hu Jay"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_6_GMS <I_MN_5G_RAN_IV4_LINE_HZG_6@internal.nsn.com>"
)
__email__ = "jay.hu@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# #host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.29", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# #pdn
_pdns = [
    PDN(PDPTypes.IPV4V6.value, "wap2.nokia.com"),
    PDN(PDPTypes.IPV4V6.value, "wap1.nokia.com"),
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

# #app server
_appserver_ssh = SshServiceDetails(
    addr="10.71.207.161", username="vrf4_sg6", password="Nokia@1234567", port="56823"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.240",
    iperf_path="/cygdrive/c",
    port="56923",
)

_appserver = AppServer(_iperf)

_iperf_1 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.237",
    iperf_path="/cygdrive/c",
    port="56376",
)
# MTK
_ue_host_ssh = SshServiceDetails(
    addr="10.68.86.165///", username="nokia5G", password="noki@123"
)
_ue_host_ssh_dingli = SshServiceDetails(
    addr="10.101.37.147", username="root", password="123456"
)
_mtk = MediaTek(
    ssh_connection_details=_ue_host_ssh,
    server_dir="c:/pyro_server",
    server_port=8080,
    edb_file_path="auto",
    imei="0123456789ABCDEF",
    imsi="310260100008511",
    apn_url="wap2.nokia.com",
    iperf_details=_iperf,
    capabilities=["REAL_MEDIATEK_UE", "mtk"],
    serial_number="0123456789ABCDEF",
)
_sigspark_1 = Android(
    ssh_connection_details=_ue_host_ssh_dingli,
    serial_number="a3aa0f43",
    server_dir="C:\Program Files (x86)\DingLi\Pilot PioneerX11.0.9.0---01161331/Pioneer.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    capabilities=["pioneer", "huawei_sigspark"],
    imsi="460023100024202",
)

_sigspark_2 = Android(
   ssh_connection_details=_ue_host_ssh_dingli,
   serial_number="31cc6e4a",
   server_dir="C:\Program Files (x86)\DingLi\Pilot PioneerX11.0.9.0---01161331/Pioneer.exe",
   python_path="C:/Python27",
   iperf_details=_iperf,
   capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
   imsi="460023100024126",
)

_sigspark_3 = Android(
    ssh_connection_details=_ue_host_ssh_dingli,
    serial_number="3c6994a3",
    server_dir="C:\Program Files (x86)\DingLi\Pilot PioneerX11.0.9.0---01161331/Pioneer.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_1,
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="460023100024125",
)

_sigspark_4 = Android(
    ssh_connection_details=_ue_host_ssh_dingli,
    serial_number="2fbc2b8f",
    server_dir="C:\Program Files (x86)\DingLi\Pilot PioneerX11.0.9.0---01161331/Pioneer.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_1,
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="460023100024201",
)
_ru = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="rfsw", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.84", username="root", password="umniedziala"
    ),
    radio_type=RadioTypes.APHA,
    signal_analyzer=None,
)
# #DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.68.89.130", username="toor4nsn", password="oZPS0POrRieRtu"
)

_gnb_pdu = pdu_TopYoung(addr="10.71.196.151", port_numbers=[5])
_capacity_unit = CapacityUnit(addr="10.68.89.130")

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[5],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(
    airscale=_airscale,
    rus=[_ru],
    f1_m_ip_addr="10.68.89.130",
)

# #CU
_cu = CU(
    backhaul_site_oam_ip="10.68.89.130",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.68.89.130", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.68.89.130", username="Nemuadmin", password="nemuuser"
    ),
)


# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=823, global_bts_id=823)

_tl_cloud_topology = "CLOUD_5G_BB3"

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    ues=[_sigspark_1, _sigspark_2, _sigspark_3, _sigspark_4],
    tl_cloud_topology=_tl_cloud_topology,
    #    enbs=[_lte_real_enb],
    # attenuator=[_attenuator],
    appserver=_appserver,
)


# old version keyword under robotws5g/resource compatibility workaround
# tl = TestlineWrapper(tl)
