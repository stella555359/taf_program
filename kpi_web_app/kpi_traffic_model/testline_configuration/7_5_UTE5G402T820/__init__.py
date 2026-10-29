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
from taf.config.testline import TopYoung_PDU
from taf.config.testline import HBTE_PDU
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
from taf.config.testline.appserver import AppServer
from taf.config.testline.pdn import PDN, PDPTypes

__maintainer__ = "Ren Xianlin"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_6_GMS <I_MN_5G_RAN_IV4_LINE_HZG_6@internal.nsn.com>"
)
__email__ = "xianlin.ren@nokia-sbell.com"


# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# #host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.113", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)


# #app server
_appserver_ssh = SshServiceDetails(
    addr="10.71.207.153",
    username="vrf4_sg6",
    password="vrf4@sg6",
    port="56820",
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.207.153",
    iperf_path="/cygdrive/c",
    port="56821",
)

_appserver = AppServer(_iperf)

# MTK
_ue_host_ssh_mtk_sa = SshServiceDetails(
    addr="10.0.176.158", username="MN5GRAN", password="nokia123@"
)

_mtk_sa = MediaTek(
    ssh_connection_details=_ue_host_ssh_mtk_sa,
    server_dir="c:/pyro_server",
    server_port=8080,
    edb_file_path="auto",
    log_filter="2.Gen98_Default_Standard",
    imei="0123456789ABCDEF",
    imsi="450053032996593",
    apn_url="dxdata1",
    iperf_details=_iperf,
    capabilities=["REAL_MEDIATEK_UE1", "mtk"],
    serial_number="0123456789ABCDEF",
)

# MTK
_ue_host_ssh_mtk_nsa = SshServiceDetails(
    addr="10.0.176.134", username="MN5GRAN", password="nokia123@"
)

_mtk_nsa = MediaTek(
    ssh_connection_details=_ue_host_ssh_mtk_nsa,
    server_dir="c:/pyro_server",
    server_port=8080,
    edb_file_path="auto",
    imei="0123456789ABCDEF",
    imsi="450053032996593",
    apn_url="dxdata1",
    iperf_details=_iperf,
    capabilities=["REAL_MEDIATEK_UE2", "mtk"],
    serial_number="0123456789ABCDEF",
)

# Qualcomm
_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.218.133", username="mn5gran", password="nokia123@"
    ),
    serial_number="6306e004",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python/python.exe",
    qcat_path="C:/Program Files/Qualcomm/QCAT7/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE0", "qct_dx50"],
    imsi="450053100016782",
    network_mode_switch_method="keyevents",
    mobile_network_text="SIMs",
    setting_network_mode_text="Preferred network type",
)

# attenuator
_attenuator_0 = HBTE(
    ip_addr="10.71.205.162",
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
        17,
        18,
        19,
        20,
        21,
        22,
        23,
        24,
        27,
        28,
        29,
        30,
    ],
    model="PA-32-32-6-127-0.5",
)

_attenuator_1 = HBTE(
    ip_addr="10.71.205.174",
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
    model="PA-32-32-6-127-0.5",
)

# #4GRU for RealEnb
_enb_ru_pdu = TopYoung_PDU(addr="10.71.196.144", port_numbers=[5])

_ru_enb = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.84", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_enb_ru_pdu.pdu_ports[5],
    radio_type=RadioTypes.AHFIB.value,
    attenuation_ports=[
        _attenuator_0.attenuator_ports[27],
        _attenuator_0.attenuator_ports[28],
        _attenuator_0.attenuator_ports[29],
        _attenuator_0.attenuator_ports[30],
    ],
)


# #RealEnb
_common_unit_0 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.71.213.68", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
)
_real_enb = Airscale(common_units=[_common_unit_0])
_lte_real_enb = RealEnb(airscale=_real_enb, rms=_ru_enb)

# #5GRU for classicalBTS
_ru1_pdu = TopYoung_PDU(addr="10.71.196.148", port_numbers=[1])
_ru2_pdu = TopYoung_PDU(addr="10.71.196.150", port_numbers=[5])
_ru3_pdu = TopYoung_PDU(addr="10.71.196.152", port_numbers=[2])
_ru4_pdu = HBTE_PDU(addr="10.71.196.140", port_numbers=[2])
_ru5_pdu = HBTE_PDU(addr="10.71.196.146", port_numbers=[3])
_ru6_pdu = HBTE_PDU(addr="10.71.196.144", port_numbers=[5])
_ru7_pdu = TopYoung_PDU(addr="10.71.196.148", port_numbers=[4])


_ru8_pdu = TopYoung_PDU(addr="10.71.196.152", port_numbers=[3])

_ru8 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.84", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru8_pdu.pdu_ports[3],
    radio_type=RadioTypes.AEQK,
    attenuation_ports=[
        _attenuator_0.attenuator_ports[21],
        _attenuator_0.attenuator_ports[22],
        _attenuator_0.attenuator_ports[23],
        _attenuator_0.attenuator_ports[24],
    ],
    serial_number="DH214500181",
)

_ru9 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.84", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru8_pdu.pdu_ports[3],
    radio_type=RadioTypes.AEQK,
    attenuation_ports=[
        _attenuator_0.attenuator_ports[7],
        _attenuator_0.attenuator_ports[8],
    ],
    serial_number="1M222812800",
)

_ru1 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="rfsw", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.84", username="rfsw", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    pdu_port=_ru1_pdu.pdu_ports[1],
    radio_type=RadioTypes.AEHC,
    attenuation_ports=[
        _attenuator_0.attenuator_ports[9],
        _attenuator_0.attenuator_ports[10],
        _attenuator_0.attenuator_ports[11],
        _attenuator_0.attenuator_ports[12],
    ],
    serial_number="K9224908443",
)

_ru2 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="rfsw", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.84", username="rfsw", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    pdu_port=_ru2_pdu.pdu_ports[5],
    radio_type=RadioTypes.AEHC,
    attenuation_ports=[
        _attenuator_0.attenuator_ports[1],
        _attenuator_0.attenuator_ports[2],
        _attenuator_0.attenuator_ports[3],
        _attenuator_0.attenuator_ports[4],
    ],
    serial_number="K9223200770",
)

_ru3 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.84", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru3_pdu.pdu_ports[2],
    radio_type=RadioTypes.AEQK,
    attenuation_ports=[
        _attenuator_0.attenuator_ports[13],
        _attenuator_0.attenuator_ports[14],
        _attenuator_0.attenuator_ports[15],
        _attenuator_0.attenuator_ports[16],
    ],
    serial_number="DH214500041",
)

_ru4 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.84", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru4_pdu.pdu_ports[2],
    radio_type=RadioTypes.AHLOA,
    attenuation_ports=[
        _attenuator_1.attenuator_ports[1],
        _attenuator_1.attenuator_ports[2],
        _attenuator_1.attenuator_ports[3],
        _attenuator_1.attenuator_ports[4],
    ],
    serial_number="K9182103357",
)

_ru5 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.84", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru5_pdu.pdu_ports[3],
    radio_type=RadioTypes.AHLOA,
    attenuation_ports=[
        _attenuator_1.attenuator_ports[13],
        _attenuator_1.attenuator_ports[14],
        _attenuator_1.attenuator_ports[15],
        _attenuator_1.attenuator_ports[16],
    ],
    serial_number="K9182044961",
)

_ru6 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.84", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru6_pdu.pdu_ports[5],
    radio_type=RadioTypes.AHFIB,
    attenuation_ports=[
        _attenuator_0.attenuator_ports[27],
        _attenuator_0.attenuator_ports[28],
        _attenuator_0.attenuator_ports[29],
        _attenuator_0.attenuator_ports[30],
    ],
    serial_number="BL2215V01DW",
)

_ru7 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.84", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru7_pdu.pdu_ports[4],
    radio_type=RadioTypes.AHFIB,
    attenuation_ports=[
        _attenuator_1.attenuator_ports[9],
        _attenuator_1.attenuator_ports[10],
        _attenuator_1.attenuator_ports[11],
        _attenuator_1.attenuator_ports[12],
    ],
    serial_number="BL2231V05JV",
)
# #DU for classicalBTS
_lmp_connection_1 = SshServiceDetails(
    addr="10.71.213.66", username="toor4nsn", password="oZPS0POrRieRtu"
)
_lmp_connection_0 = SshServiceDetails(
    addr="10.71.213.68", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")
_capacity_unit_1 = CapacityUnit(addr="192.168.253.20")
_capacity_unit_11 = CapacityUnit(addr="192.168.253.21")
_capacity_unit_1_11 = CapacityUnit(addr="192.168.253.21")

_gnb_1_pdu = FACOM(addr="10.71.196.151", port_numbers=[3])
_gnb_0_pdu = FACOM(addr="10.71.196.151", port_numbers=[2])

_common_unit_1_0 = CommonUnit(
    lmp_connection=_lmp_connection_1,
    capacity_units=[_capacity_unit_1, _capacity_unit_1_11],
    pdu_port=_gnb_1_pdu.pdu_ports[3],
)

_common_unit_0_0 = CommonUnit(
    lmp_connection=_lmp_connection_0,
    capacity_units=[_capacity_unit, _capacity_unit_11],
    pdu_port=_gnb_0_pdu.pdu_ports[2],
)

_airscale_1 = Airscale(common_units=[_common_unit_1_0])
_airscale_0 = Airscale(common_units=[_common_unit_0_0])

_du_1_0 = DU(
    airscale=_airscale_1,
    rus=[_ru8, _ru9],
    f1_m_ip_addr="10.71.213.66",
)
_du_0_0 = DU(
    airscale=_airscale_0,
    rus=[_ru1, _ru2, _ru3, _ru4, _ru5, _ru6, _ru7],
    f1_m_ip_addr="10.71.213.68",
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

_cu_1 = CU(
    backhaul_site_oam_ip="10.71.213.66",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.213.66", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.213.66", username="Nemuadmin", password="nemuuser"
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

_cu_0 = CU(
    backhaul_site_oam_ip="10.71.213.68",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.213.68", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.213.68", username="Nemuadmin", password="nemuuser"
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
_classical_bts_0 = ClassicalBts(
    dus=[_du_0_0], cu=_cu_0, instance_id=10611, global_bts_id=10611
)
_classical_bts_1 = ClassicalBts(
    dus=[_du_1_0], cu=_cu_1, instance_id=10610, global_bts_id=10610
)


_tl_cloud_topology = "CLOUD_5G_BB3"

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts_0, _classical_bts_1],
    ues=[_mtk_sa, _mtk_nsa, _android],
    tl_cloud_topology=_tl_cloud_topology,
    enbs=[_lte_real_enb],
    attenuators=[_attenuator_0, _attenuator_1],
    appserver=_appserver,
)
