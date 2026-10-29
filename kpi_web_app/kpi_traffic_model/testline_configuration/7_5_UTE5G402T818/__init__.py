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

__maintainer__ = "Li Liyu"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_6_GMS <I_MN_5G_RAN_IV4_LINE_HZG_6@internal.nsn.com>"
)
__email__ = "liyu.li@nokia-sbell.com"


# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# #host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.206", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)


# #app server
_appserver_ssh = SshServiceDetails(
    addr="10.57.191.237", username="vrf4_sg6", password="Nokia@1234567", port="56818"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.237",
    iperf_path="/cygdrive/c",
    port="56918",
)

_appserver = AppServer(_iperf)

# Qualcomm
_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.101.47.133", username="nokia5G", password="noki@123"
    ),
    serial_number="bde0d57c",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE0", "qct_dx50"],
)



# attenuator
_attenuator_0 = HBTE(
    ip_addr="10.101.52.72",
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
        25,
        26,
        27,
        28,
        29,
        30,
        31,
        32,
    ],
    model="PA-32-32-6-127-0.5",
)



# 4GRU for RealEnb
_enb_ru_pdu = TopYoung_PDU(addr="10.101.46.14", port_numbers=[3])

_ru_enb = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.84", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_enb_ru_pdu.pdu_ports[3],
    radio_type=RadioTypes.AHFIB.value,
    attenuation_ports=[
        _attenuator_0.attenuator_ports[27],
        _attenuator_0.attenuator_ports[28],
    ],
)


# #RealEnb
_common_unit_0 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.101.52.69", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
)
_real_enb = Airscale(common_units=[_common_unit_0])
_lte_real_enb = RealEnb(airscale=_real_enb, rms=_ru_enb)



# #5GRU for classicalBTS
_ru1_pdu = TopYoung_PDU(addr="10.101.46.18", port_numbers=[2])
_ru2_pdu = TopYoung_PDU(addr="10.101.46.14", port_numbers=[5])
_ru3_pdu = TopYoung_PDU(addr="10.101.46.18", port_numbers=[3])
_ru4_pdu = TopYoung_PDU(addr="10.101.46.18", port_numbers=[4])
_ru5_pdu = TopYoung_PDU(addr="10.101.46.14", port_numbers=[7])

_ru1 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.84", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru1_pdu.pdu_ports[2],
    radio_type=RadioTypes.AEHC,
    attenuation_ports=[
        _attenuator_0.attenuator_ports[1],
        _attenuator_0.attenuator_ports[2],
        _attenuator_0.attenuator_ports[3],
        _attenuator_0.attenuator_ports[4],
    ],
)

_ru2 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.84", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.84", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru2_pdu.pdu_ports[5],
    radio_type=RadioTypes.AEHC,
    attenuation_ports=[
        _attenuator_0.attenuator_ports[5],
        _attenuator_0.attenuator_ports[6],
        _attenuator_0.attenuator_ports[7],
        _attenuator_0.attenuator_ports[8],
    ],
)

_ru3 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.84", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru3_pdu.pdu_ports[3],
    radio_type=RadioTypes.AEQZ,
    attenuation_ports=[
        _attenuator_0.attenuator_ports[17],
        _attenuator_0.attenuator_ports[18],
        _attenuator_0.attenuator_ports[19],
        _attenuator_0.attenuator_ports[20],
    ],
)

_ru4 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.84", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru4_pdu.pdu_ports[4],
    radio_type=RadioTypes.AEQY,
    attenuation_ports=[
        _attenuator_0.attenuator_ports[21],
        _attenuator_0.attenuator_ports[22],
        _attenuator_0.attenuator_ports[23],
        _attenuator_0.attenuator_ports[24],
    ],
)

_ru5 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.84", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru5_pdu.pdu_ports[7],
    radio_type=RadioTypes.AEQY,
    attenuation_ports=[
        _attenuator_0.attenuator_ports[9],
        _attenuator_0.attenuator_ports[10],
        _attenuator_0.attenuator_ports[11],
        _attenuator_0.attenuator_ports[12],
    ],
)


# #DU for classicalBTS
_lmp_connection_0 = SshServiceDetails(
    addr="10.101.52.66", username="toor4nsn", password="oZPS0POrRieRtu"
)


_capacity_unit = CapacityUnit(addr="192.168.253.20")
_capacity_unit_11 = CapacityUnit(addr="192.168.253.21")

_gnb_0_pdu = FACOM(addr="10.101.46.16", port_numbers=[2])

_common_unit_0_0 = CommonUnit(
    lmp_connection=_lmp_connection_0,
    capacity_units=[_capacity_unit, _capacity_unit_11],
    pdu_port=_gnb_0_pdu.pdu_ports[2],
)


_airscale_0 = Airscale(common_units=[_common_unit_0_0])

_du_0_0 = DU(
    airscale=_airscale_0,
    rus=[_ru1, _ru2, _ru3, _ru4, _ru5],
    f1_m_ip_addr="10.101.52.66",
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

_cu_0 = CU(
    backhaul_site_oam_ip="10.101.52.66",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.52.66", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.52.66", username="Nemuadmin", password="nemuuser"
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
    dus=[_du_0_0], cu=_cu_0, instance_id=10127, global_bts_id=10127
)


_tl_cloud_topology = "CLOUD_5G_BB3"

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts_0],
    ues=[_android],
    tl_cloud_topology=_tl_cloud_topology,
    enbs=[_lte_real_enb],
    attenuators=[_attenuator_0],
    appserver=_appserver,
)
