import os
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.gnb.du import DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, ATEN, RRB, APC, Gude, FPFH
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

__maintainer__ = "Chen Jun"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_6_GMS <I_MN_5G_RAN_IV4_LINE_HZG_6@internal.nsn.com>"
)
__email__ = "jun.8.chen@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# #host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.95", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# #pdn
_pdns = [
    PDN(PDPTypes.IPV4V6.value, "wap2.nokia.com"),
    PDN(PDPTypes.IPV4V6.value, "wap1.nokia.com"),
]


# #app server
_appserver_ssh = SshServiceDetails(
    addr="10.71.207.145", username="vrf4_sg6", password="vrf4@sg6", port="56273"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.207.145",
    iperf_path="/cygdrive/c",
    port="56373",
)

_appserver = AppServer(_iperf)

_iperf_1 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.237",
    iperf_path="/cygdrive/c",
    port="56377",
)


# #MTK1
_ue_host_ssh_1 = SshServiceDetails(
    addr="10.57.130.13", username="nokia5G", password="noki@123"
)

_ue_host_ssh_dingli = SshServiceDetails(
    addr="10.57.156.9", username="root", password="123456"
)

# CI_Detail_UE_Type='MTK phoneB'
_mtk_1 = MediaTek(
    ssh_connection_details=_ue_host_ssh_1,
    server_dir="c:/pyro_server",
    server_port=8080,
    edb_file_path="auto",
    imei="0123456789ABCDEF",
    imsi="460023100010157",
    apn_url="wap2.nokia.com",
    iperf_details=_iperf,
    capabilities=["REAL_MEDIATEK_UE1", "mtk"],
    serial_number="0123456789ABCDEF",
    log_filter="2.Gen97_Default_Standard",
)


_sigspark_1 = Android(
    ssh_connection_details=_ue_host_ssh_dingli,
    serial_number="9bdd0bfe",
    server_dir="D:\Program Files (x86)\DingLi\Pilot PioneerX11.0.9.0---03061009\Pioneer.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    capabilities=["pioneer"],
    imsi="460023100016992",
)

_sigspark_2 = Android(
    ssh_connection_details=_ue_host_ssh_dingli,
    serial_number="b81b15b",
    server_dir="D:\Program Files (x86)\DingLi\Pilot PioneerX11.0.9.0---03061009\Pioneer.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    capabilities=["pioneer"],
    imsi="460023100016989",
)

_sigspark_3 = Android(
    ssh_connection_details=_ue_host_ssh_dingli,
    serial_number="96b0c8e7",
    server_dir="D:\Program Files (x86)\DingLi\Pilot PioneerX11.0.9.0---03061009\Pioneer.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_1,
    capabilities=["pioneer"],
    imsi="460023100016990",
)

_sigspark_4 = Android(
    ssh_connection_details=_ue_host_ssh_dingli,
    serial_number="4a4e5220",
    server_dir="D:\Program Files (x86)\DingLi\Pilot PioneerX11.0.9.0---03061009\Pioneer.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_1,
    capabilities=["pioneer"],
    imsi="460023100016992",
)

# #5GRU for classicalBTS
# attenuator
_attenuator_0 = RadioRack(
    ip_addr="10.57.156.7",
    port=50000,
    attenuation_port_numbers=[1, 2, 3, 4],
)

_attenuator_1 = TopYoung(
    ip_addr="10.57.156.8",
    port=28888,
    attenuation_port_numbers=[1, 2, 3, 4],
    model="MCS2338A2-64B16-B4",
)

# #5GRU for classicalBTS
_ru1_pdu = FACOM(addr="10.57.172.27", port_numbers=[3])
_ru2_pdu = FPFH(addr="10.57.172.2", port_numbers=[6])
_ru3_pdu = FPFH(addr="10.57.172.2", port_numbers=[4])


_ru1 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="serviceuser", password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og="
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.34", username="serviceuser", password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og="
    ),
    pdu_port=_ru1_pdu.pdu_ports[3],
    radio_type=RadioTypes.AVQC,
    serial_number="K9223200778",
)

_ru2 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52",
        username="serviceuser",
        password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.34",
        username="serviceuser",
        password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og=",
    ),
    pdu_port=_ru2_pdu.pdu_ports[6],
    radio_type=RadioTypes.AVQC,
    serial_number="L1233410011",
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
    pdu_port=_ru3_pdu.pdu_ports[4],
    radio_type=RadioTypes.AQQF,
    attenuation_ports=[
        _attenuator_0.attenuator_ports[1],
        _attenuator_0.attenuator_ports[2],
        _attenuator_0.attenuator_ports[3],
        _attenuator_0.attenuator_ports[4],
    ],
    serial_number="1M223638060",
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
    addr="10.57.223.6", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")
_capacity_unit_11 = CapacityUnit(addr="192.168.253.21")

_gnb_pdu = FACOM(addr="10.57.172.4 ", port_numbers=[8])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit, _capacity_unit_11],
    pdu_port=_gnb_pdu.pdu_ports[8],
)


_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru1, _ru2, _ru3], f1_m_ip_addr="10.57.223.6")

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
    backhaul_site_oam_ip="10.57.223.6",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.223.6", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.223.6", username="Nemuadmin", password="nemuuser"
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
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=37260, global_bts_id=37260)


_tl_cloud_topology = "CLOUD_5G_BB3"

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    enbs=[_lte_real_enb],
    ues=[_mtk_1, _sigspark_1, _sigspark_2, _sigspark_3, _sigspark_4],
    tl_cloud_topology=_tl_cloud_topology,
    attenuator=[_attenuator_0, _attenuator_1],
    appserver=_appserver,
)
