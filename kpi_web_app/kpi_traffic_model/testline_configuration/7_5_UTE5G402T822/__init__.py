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
from taf.config.testline.hardware_controller import (
    AmiaFanHardwareController,
    GPSPowerHardwareController,
)
from taf.config.testline.signal_analyzer import KeysightN9935A
from taf.config.testline.nms import Netact
from taf.config.testline.optical_switch import Leoni
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
        addr="10.57.167.140", username="ute", password="iW_K#8.ute%A10h0m0ra"
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

# #MTK
_ue_host_ssh = SshServiceDetails(
    addr="10.71.217.88", username="nokia5G", password="noki@123"
)

_mtk_appserver_ssh = SshServiceDetails(
    addr="10.57.191.237", username="vrf4_sg6", password="Nokia@1234567", port="56822"
)
_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_mtk_appserver_ssh,
    network_interface_address="10.57.191.237",
    iperf_path="iperf",
    port=56922,
)

_mtk = MediaTek(
    ssh_connection_details=_ue_host_ssh,
    server_dir="c:/pyro_server",
    server_port=8080,
    edb_file_path="auto",
    imei="0123456789ABCDEF",
    imsi="460023100008500",
    apn_url="wap2.nokia.com",
    iperf_details=_iperf_details_on_appserver,
    capabilities=["REAL_MEDIATEK_UE", "mtk"],
    serial_number="0123456789ABCDEF",
)


# #app server
_appserver_ssh = SshServiceDetails(
    addr="10.57.191.237", username="vrf4_sg6", password="Nokia@1234567", port="56822"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.237",
    iperf_path="/cygdrive/c",
    port="56922",
)

_appserver = AppServer(_iperf)


# #5GRU for classicalBTS
# attenuator
_attenuator = HBTE(
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
# _enb_ru_pdu = TopYoung_PDU(addr="10.71.196.148", port_numbers=[2])

# _ru_enb = RU(
#    ru_hw_group="Below6GHz",
#    default_ssh_connection_details=SshServiceDetails(
#        addr="192.168.254.52", username="toor4nsn", password="oZPS0POrRieRtu"
#    ),
#    lmp_connection=SshServiceDetails(
#        addr="192.168.254.84", username="toor4nsn", password="oZPS0POrRieRtu"
#    ),
#    pdu_port=_enb_ru_pdu.pdu_ports[2],
#    radio_type=RadioTypes.AHFIB.value,
#    attenuation_ports=[
#        _attenuator_0.attenuator_ports[27],
#        _attenuator_0.attenuator_ports[28],
#    ],
# )


# #RealEnb
# _common_unit_0 = CommonUnit(
#    lmp_connection=SshServiceDetails(
#        addr="10.71.213.67", username="toor4nsn", password="oZPS0POrRieRtu"
#    ),
#    capacity_units=[],
# )
# _real_enb = Airscale(common_units=[_common_unit_0])
# _lte_real_enb = RealEnb(airscale=_real_enb, rms=_ru_enb)


# #5GRU for classicalBTS
_ru1_pdu = HBTE_PDU(addr="10.71.196.147", port_numbers=[2])
_ru2_pdu = HBTE_PDU(addr="10.71.196.147", port_numbers=[3])
_ru3_pdu = HBTE_PDU(addr="10.71.196.147", port_numbers=[1])


_ru1 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.73.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.73.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru1_pdu.pdu_ports[2],
    radio_type=RadioTypes.AWHQE,
    attenuation_ports=[
        _attenuator.attenuator_ports[13],
        _attenuator.attenuator_ports[14],
        _attenuator.attenuator_ports[15],
        _attenuator.attenuator_ports[16],
    ],
)

_ru2 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.73.128", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.73.128", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru2_pdu.pdu_ports[3],
    radio_type=RadioTypes.AWHQE,
    attenuation_ports=[
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[6],
        _attenuator.attenuator_ports[7],
        _attenuator.attenuator_ports[8],
    ],
)

_ru3 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.73.130", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.73.130", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru3_pdu.pdu_ports[1],
    radio_type=RadioTypes.AWHQE,
    attenuation_ports=[
        _attenuator.attenuator_ports[13],
        _attenuator.attenuator_ports[14],
        _attenuator.attenuator_ports[15],
        _attenuator.attenuator_ports[16],
    ],
)

# RealEnb
_real_enb_pdu = FACOM(addr="10.57.242.5", port_numbers=[1])

_common_unit_6 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.231.81", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[1],
)

_real_enb = Airscale(common_units=[_common_unit_6])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=None)


# #DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.71.213.70", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")

_gnb_pdu = FACOM(addr="10.71.196.151", port_numbers=[4])

_common_unit = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[4],
)


_airscale = Airscale(common_units=[_common_unit])

_du = DU(airscale=_airscale, rus=[_ru1, _ru2, _ru3], f1_m_ip_addr="10.71.213.70")

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
    backhaul_site_oam_ip="10.71.213.70",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.213.70", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.213.70", username="Nemuadmin", password="nemuuser"
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
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=10612, global_bts_id=10612)


_tl_cloud_topology = "CLOUD_5G_BB3"

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    enbs=[_lte_real_enb],
    core=_realcore,
    ues=[_mtk],
    tl_cloud_topology=_tl_cloud_topology,
    attenuators=[_attenuator],
    appserver=_appserver,
)
