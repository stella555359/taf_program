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
from taf.config.testline import LicenseKeeper
from taf.config.testline.gnb.du import DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, ATEN, RRB, APC, Gude
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
        addr="10.57.177.38", username="ute", password="iW_K#8.ute%A10h0m0ra"
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
    addr="10.57.191.237", username="vrf4_sg6", password="Nokia@1234567", port="56077"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.237",
    iperf_path="/cygdrive/c",
    port="56177",
)

_iperf_for_spark = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.237",
    iperf_path="/data/local/tmp/iperf",
    port="56277",
)

_appserver = AppServer(_iperf)

_licensekeeper = LicenseKeeper(username="jay.hu@nokia-sbell.com", password="nokia123")
# #MTK1
_ue_host_ssh = SshServiceDetails(
    addr="10.57.150.163", username="MN5GRAN", password="nokia123@"
)

# CI_Detail_UE_Type='MTK phoneB'

_iperf_details_on_mtk = IperfDataTransferDetails(
    ssh_connection_details=_ue_host_ssh,
    network_interface_address="",
    iperf_path="/usr/bin/iperf",
    port=53077,
)

_mtk_ue_box = MediaTek(
    ssh_connection_details=_ue_host_ssh,
    server_dir="c:/pyro_server",
    server_port=8080,
    edb_file_path="C:/MTK/M60/edb_file/MDDB.EDB",
    log_filter="2.Gen99_Default_Standard",
    imei="0123456789ABCDEF",
    imsi="001013100011544",
    apn_url="dxdata1",
    iperf_details=_iperf,
    capabilities=["REAL_MEDIATEK_UE", "mtk"],
    serial_number="0123456789ABCDEF",
)

_sigspark = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.246", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="416113a8",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.11/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_for_spark,
    imsi="460023100009137",
    licensekeeper=_licensekeeper,
    capabilities=["REAL_ANDROID_UE1", "huawei_sigspark"],
)

_iperf_details_on_appserver_for_caymus_ul = IperfDataTransferDetails(
    ssh_connection_details=_ue_host_ssh,
    network_interface_address="10.57.150.163",
    iperf_path="/usr/bin/iperf",
    port=54077,
    ports=[54077, 54009, 54006, 54007],
)

_appserver_for_caymus_ul = AppServer(_iperf_details_on_appserver_for_caymus_ul)

# #5GRU for classicalBTS
# attenuator
_attenuator_0 = RadioRack(
    ip_addr="10.57.156.4",
    port=50000,
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
)

# #5GRU for classicalBTS
_ru1_pdu = FACOM(addr="10.57.172.15", port_numbers=[3])
_ru2_pdu = FACOM(addr="10.57.172.15", port_numbers=[2])
_ru3_pdu = FACOM(addr="10.57.172.15", port_numbers=[1])


_ru1 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="rfsw", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.34", username="rfsw", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    pdu_port=_ru1_pdu.pdu_ports[3],
    radio_type=RadioTypes.AHPF,
    attenuation_ports=[
        _attenuator_0.attenuator_ports[1],
        _attenuator_0.attenuator_ports[2],
        _attenuator_0.attenuator_ports[3],
        _attenuator_0.attenuator_ports[4],
    ],
    serial_number="EA224853377",
)

_ru2 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.85", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.34", username="root", password="umniedziala"
    ),
    pdu_port=_ru2_pdu.pdu_ports[2],
    radio_type=RadioTypes.AHLOA,
    attenuation_ports=[
        _attenuator_0.attenuator_ports[13],
        _attenuator_0.attenuator_ports[14],
        _attenuator_0.attenuator_ports[15],
        _attenuator_0.attenuator_ports[16],
    ],
    serial_number="BL2118G1DNS",
)

_ru3 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52",
        username="rfsw",
        password="3Is6ezFJ7dFlB29cgs0yp3RCM3fUF1zNO1+6Z08tlAc=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.34",
        username="rfsw",
        password="3Is6ezFJ7dFlB29cgs0yp3RCM3fUF1zNO1+6Z08tlAc=",
    ),
    pdu_port=_ru3_pdu.pdu_ports[1],
    radio_type=RadioTypes.AHFIB,
    attenuation_ports=[
        _attenuator_0.attenuator_ports[9],
        _attenuator_0.attenuator_ports[10],
        _attenuator_0.attenuator_ports[11],
        _attenuator_0.attenuator_ports[12],
    ],
    serial_number="BL2108V05IK",
)

_ru4 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52",
        username="rfsw",
        password="3Is6ezFJ7dFlB29cgs0yp3RCM3fUF1zNO1+6Z08tlAc=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.34",
        username="rfsw",
        password="3Is6ezFJ7dFlB29cgs0yp3RCM3fUF1zNO1+6Z08tlAc=",
    ),
    pdu_port=_ru3_pdu.pdu_ports[1],
    radio_type=RadioTypes.AHFIB,
    attenuation_ports=[
        _attenuator_0.attenuator_ports[9],
        _attenuator_0.attenuator_ports[10],
        _attenuator_0.attenuator_ports[11],
        _attenuator_0.attenuator_ports[12],
    ],
    serial_number="BL2108V05IK",
)

# #DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.57.223.19", username="toor4nsn", password="oZPS0POrRieRtu"
)
_lmp_connection_1 = SshServiceDetails(
    addr="10.57.223.20", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")
_capacity_unit_1 = CapacityUnit(addr="192.168.253.20")
_capacity_unit_11 = CapacityUnit(addr="192.168.253.21")
_capacity_unit_1_11 = CapacityUnit(addr="192.168.253.21")

_gnb_pdu = FACOM(addr="10.57.172.21", port_numbers=[5])
_gnb_1_pdu = FACOM(addr="10.57.172.21", port_numbers=[5])
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit, _capacity_unit_11],
    pdu_port=_gnb_pdu.pdu_ports[5],
)
_common_unit_1_0 = CommonUnit(
    lmp_connection=_lmp_connection_1,
    capacity_units=[_capacity_unit_1, _capacity_unit_1_11],
    pdu_port=_gnb_1_pdu.pdu_ports[5],
)

_airscale = Airscale(common_units=[_common_unit_0])
_airscale_1 = Airscale(common_units=[_common_unit_1_0])

_du = DU(airscale=_airscale, rus=[_ru1, _ru2, _ru3], f1_m_ip_addr="10.57.223.19")
_du_1_0 = DU(
    airscale=_airscale_1,
    rus=[_ru4],
    f1_m_ip_addr="10.57.223.20",
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
    backhaul_site_oam_ip="10.57.223.19",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.223.19", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.223.19", username="Nemuadmin", password="nemuuser"
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
    backhaul_site_oam_ip="10.57.223.20",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.223.20", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.223.20", username="Nemuadmin", password="nemuuser"
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
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=77, global_bts_id=77)
_classical_bts_1 = ClassicalBts(
    dus=[_du_1_0], cu=_cu_1, instance_id=825, global_bts_id=825
)

_tl_cloud_topology = "CLOUD_5G_BB3"

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    core=_realcore,
    ues=[_mtk_ue_box, _sigspark],
    tl_cloud_topology=_tl_cloud_topology,
    enbs=[],
    attenuator=[_attenuator_0],
    appservers=[_appserver, _appserver_for_caymus_ul],
)
