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
        addr="10.57.157.108", username="ute", password="iW_K#8.ute%A10h0m0ra"
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
    addr="10.71.207.161", username="vrf4_sg6", password="vrf4@sg6", port="56272"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.237",
    iperf_path="/cygdrive/c",
    port="56372",
)

_appserver = AppServer(_iperf)

_iperf_1 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.237",
    iperf_path="/cygdrive/c",
    port="56376",
)

_ue_pdu = FACOM(addr="1.1.1.1", port_numbers=[1])


_ue_host_ssh_dingli = SshServiceDetails(
    addr="10.57.231.52", username="root", password="123456"
)
# CI_Detail_UE_Type='Qualcomm;Qualcomm'
_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.91", username="mn5gran", password="nokia123@"
    ),
    serial_number="9f6495f3",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["qct_dx50"],
    pdu_port=_ue_pdu.pdu_ports[1],
)

_sigspark_1 = Android(
    ssh_connection_details=_ue_host_ssh_dingli,
    serial_number="38287075",
    server_dir="D:\Program Files (x86)\DingLi\Pilot PioneerX11.0.9.0---09181643\Pioneer.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    capabilities=["pioneer", "huawei_sigspark"],
    imsi="460023100024193",
)

_sigspark_2 = Android(
   ssh_connection_details=_ue_host_ssh_dingli,
   serial_number="19054461",
   server_dir="D:\Program Files (x86)\DingLi\Pilot PioneerX11.0.9.0---09181643\Pioneer.exe",
   python_path="C:/Python27",
   iperf_details=_iperf,
   capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
   imsi="460023100015274",
)

_sigspark_3 = Android(
    ssh_connection_details=_ue_host_ssh_dingli,
    serial_number="39362191",
    server_dir="D:\Program Files (x86)\DingLi\Pilot PioneerX11.0.9.0---09181643\Pioneer.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_1,
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="460023100015275",
)

_sigspark_4 = Android(
    ssh_connection_details=_ue_host_ssh_dingli,
    serial_number="28240829",
    server_dir="D:\Program Files (x86)\DingLi\Pilot PioneerX11.0.9.0---09181643\Pioneer.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_1,
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="460023100015273",
)
_sigspark_5 = Android(
    ssh_connection_details=_ue_host_ssh_dingli,
    serial_number="2fbc2b8f",
    server_dir="D:\Program Files (x86)\DingLi\Pilot PioneerX11.0.9.0---09181643\Pioneer.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_1,
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="460023100024192",
)
_sigspark_6 = Android(
    ssh_connection_details=_ue_host_ssh_dingli,
    serial_number="2fbc2b8f",
    server_dir="D:\Program Files (x86)\DingLi\Pilot PioneerX11.0.9.0---09181643\Pioneer.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_1,
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="460023100024210",
)
_sigspark_7 = Android(
    ssh_connection_details=_ue_host_ssh_dingli,
    serial_number="2fbc2b8f",
    server_dir="D:\Program Files (x86)\DingLi\Pilot PioneerX11.0.9.0---09181643\Pioneer.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_1,
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="460023100024191",
)
_sigspark_8 = Android(
    ssh_connection_details=_ue_host_ssh_dingli,
    serial_number="2fbc2b8f",
    server_dir="D:\Program Files (x86)\DingLi\Pilot PioneerX11.0.9.0---09181643\Pioneer.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_1,
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="460023100015272",
)

# #5GRU for classicalBTS
# attenuator
_attenuator_0 = HBTE(
    ip_addr="10.57.156.68",
    port=5000,
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    model="PA-16-16-6-127-0.5-B-S",
)

_attenuator_1 = TopYoung(
    ip_addr="10.57.156.69",
    port=28888,
    attenuation_port_numbers=[1, 2, 3, 4],
    model="MCS2350A2-64B16-E6",
)

# #5GRU for classicalBTS
_ru1_pdu = FACOM(addr="10.57.172.29", port_numbers=[2])
_ru2_pdu = FACOM(addr="10.57.172.29", port_numbers=[5])
_ru3_pdu = FACOM(addr="10.57.172.29", port_numbers=[1])


_ru1 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="serviceuser", password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og="
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.34", username="serviceuser", password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og="
    ),
    pdu_port=_ru1_pdu.pdu_ports[2],
    radio_type=RadioTypes.AVQC,
    attenuation_ports=[
        _attenuator_0.attenuator_ports[9],
        _attenuator_0.attenuator_ports[10],
        _attenuator_0.attenuator_ports[11],
        _attenuator_0.attenuator_ports[12],
    ],
    serial_number="1M244205941",
)

_ru2 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.85", username="serviceuser", password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og="
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.34", username="serviceuser", password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og="
    ),
    pdu_port=_ru2_pdu.pdu_ports[5],
    radio_type=RadioTypes.AVQC,
    attenuation_ports=[
        _attenuator_0.attenuator_ports[5],
        _attenuator_0.attenuator_ports[6],
        _attenuator_0.attenuator_ports[7],
        _attenuator_0.attenuator_ports[8],
    ],
    serial_number="1M244205937",
)

_ru3 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52",
        username="serviceuser",
        password="3Is6ezFJ7dFlB29cgs0yp3RCM3fUF1zNO1+6Z08tlAc=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.34",
        username="serviceuser",
        password="3Is6ezFJ7dFlB29cgs0yp3RCM3fUF1zNO1+6Z08tlAc=",
    ),
    pdu_port=_ru3_pdu.pdu_ports[1],
    radio_type=RadioTypes.AQQF,
    attenuation_ports=[
        _attenuator_0.attenuator_ports[1],
        _attenuator_0.attenuator_ports[2],
        _attenuator_0.attenuator_ports[3],
        _attenuator_0.attenuator_ports[4],
    ],
    serial_number="1M232010507",
)


# RealEnb
_real_enb_pdu = FACOM(addr="10.57.172.21", port_numbers=[1])

_common_unit_6 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.223.101", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[1],
)

_real_enb = Airscale(common_units=[_common_unit_6])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=None)


# #DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.57.223.114", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")
_capacity_unit_11 = CapacityUnit(addr="192.168.253.21")

_gnb_pdu = TopYoung_PDU(addr="10.57.172.21", port_numbers=[4])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit, _capacity_unit_11],
    pdu_port=_gnb_pdu.pdu_ports[4],
)


_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru1, _ru2, _ru3], f1_m_ip_addr="10.57.223.114")

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
    backhaul_site_oam_ip="10.57.223.66",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.223.114", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.223.114", username="Nemuadmin", password="nemuuser"
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
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=4294967250, global_bts_id=2147483646)


_tl_cloud_topology = "CLOUD_5G_BB3"

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    enbs=[_lte_real_enb],
    core=_realcore,
    # ues=[_mtk_1, _sigspark_1, _sigspark_3, _sigspark_4],
    ues=[_android, _sigspark_1, _sigspark_2, _sigspark_3, _sigspark_4, _sigspark_5, _sigspark_6, _sigspark_7, _sigspark_8],
    tl_cloud_topology=_tl_cloud_topology,
    attenuator=[_attenuator_0, _attenuator_1],
    appserver=_appserver,
)
