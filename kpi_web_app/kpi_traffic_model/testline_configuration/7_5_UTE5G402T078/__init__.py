import os
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc, Connection
from taf.config.testline.gnb.du import DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, ATEN, RRB, APC, Gude, HBTE
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.core import RealCore  # Use RealCore() for Real Core TL
from taf.config.testline.gnb.du import Cablink, Endpoint
from taf.config.testline import NetworkAddress, RoutingInformation
from taf.config.testline.ue import (
    AirphoneCloud,
    Airphone,
    Prisma,
    TM500,
    Qualcomm,
    QualcommUeType,
    Android,
)  # added in taf.meta.5.4
from taf.config.testline.enb import (
    Enb,
    SimEnb,
    RealEnb,
    LTEEmuEnb,
    PrismaEnb,
    DocomoEnb,
)

# added in taf.meta 5.4
from taf.config.testline.attenuator import AttenuationPort, TopYoung
from taf.config.testline.gnb.networkaddress import NetworkAddress  # add in taf.meta 5.4
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)
#from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.appserver import AppServer


__maintainer__ = "Dong tony"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_6_GMS <I_MN_5G_RAN_IV4_LINE_HZG_6@internal.nsn.com>"
)
__email__ = "tony.1.dong@nokia.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# Iperf
_appserver_ssh = SshServiceDetails(
    addr="10.57.191.237", username="vrf4_sg6", password="Nokia@1234567", port="56277"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.237",
    iperf_path="/usr/bin/iperf",
    port="56377",
)

_appserver = AppServer(_iperf)

_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.93", username="mn5gran", password="nokia123@"
    ),
    serial_number="fe6c2643",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["qct_dx50"],
)

_attenuator = TopYoung(
    ip_addr="10.57.243.53",
    port=3000,
    attenuation_port_numbers=[7, 8, 9, 10],
    model="TAS16T16-51-120-1SDES",
)

# #5GRU for classicalBTS
_ru_0_pdu = HBTE(addr="10.71.196.138", port_numbers=[2])

_ru_0 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.54", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_ru_0_pdu.pdu_ports[2],
    radio_type=RadioTypes.AWHQE,
    signal_analyzer=None,
    attenuation_ports=[
        _attenuator.attenuator_ports[7],
        _attenuator.attenuator_ports[8],
        _attenuator.attenuator_ports[9],
        _attenuator.attenuator_ports[10],
    ],
)

_ru_1_pdu = HBTE(addr="10.71.196.138", port_numbers=[3])

_ru_1 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.54", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_ru_1_pdu.pdu_ports[3],
    radio_type=RadioTypes.AWHQE,
    signal_analyzer=None,
    attenuation_ports=[
        _attenuator.attenuator_ports[7],
        _attenuator.attenuator_ports[8],
        _attenuator.attenuator_ports[9],
        _attenuator.attenuator_ports[10],
    ],
)

_ru_2_pdu = HBTE(addr="10.71.196.140", port_numbers=[1])

_ru_2 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.54", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_ru_2_pdu.pdu_ports[1],
    radio_type=RadioTypes.AWHQE,
    signal_analyzer=None,
    attenuation_ports=[
        _attenuator.attenuator_ports[7],
        _attenuator.attenuator_ports[8],
        _attenuator.attenuator_ports[9],
        _attenuator.attenuator_ports[10],
    ],
)

_ru_3_pdu = HBTE(addr="10.71.196.142", port_numbers=[1])

_ru_3 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.54", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_ru_3_pdu.pdu_ports[1],
    radio_type=RadioTypes.AWHQE,
    signal_analyzer=None,
    attenuation_ports=[
        _attenuator.attenuator_ports[7],
        _attenuator.attenuator_ports[8],
        _attenuator.attenuator_ports[9],
        _attenuator.attenuator_ports[10],
    ],
)

_ru_4_pdu = HBTE(addr="10.71.196.140", port_numbers=[4])

_ru_4 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.54", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_ru_4_pdu.pdu_ports[4],
    radio_type=RadioTypes.AWHQE,
    signal_analyzer=None,
    attenuation_ports=[
        _attenuator.attenuator_ports[7],
        _attenuator.attenuator_ports[8],
        _attenuator.attenuator_ports[9],
        _attenuator.attenuator_ports[10],
    ],
)

# #DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(
    addr="192.168.253.20",
    hardware_type="ABIO",
)

_gnb_pdu = HBTE(addr="10.71.196.138", port_numbers=[4])

_capacity_unit1 = CapacityUnit(
    addr="192.168.253.20",
    hardware_type="ASOE",
)
#_capacity_unit2 = CapacityUnit(addr="192.168.253.24")


_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit1],
    pdu_port=_gnb_pdu.pdu_ports[4],
    hardware_type="ASOE",
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(
    airscale=_airscale,
    rus=[_ru_0, _ru_1],
    f1_m_ip_addr="192.168.255.129",
#    cablinks=_ru_cablinks,
)

# CU
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.71.213.67",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.213.65 ", ip_prefix_length=27),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.213.67", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.213.67", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.71.213.67",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.213.65", ip_prefix_length=27),
    ),
    x2u=NetworkAddress(
        v4="10.71.213.67",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.213.65", ip_prefix_length=27),
    ),
    s1u=NetworkAddress(
        v4="10.71.213.67",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.213.65", ip_prefix_length=27),
    ),
)


# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=277, global_bts_id=277)

# #host
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.2", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_classical_bts.dus[0].airscale.common_units[0],
            interface_type="lmp",
        )
    ],
)
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ANDROID_ASOE_2xAVQA"

tl = TestLine(
    test_pc=_test_pc,
   # test_pcs=[_test_pc],
    gnbs=[_classical_bts],
    ues=[_android],
    #enbs=[_lte_real_enb],
    core=RealCore(mcc=262, mnc=3),  # Use RealCore() for Real Core TL
    tl_cloud_topology=_tl_cloud_topology,
    attenuator=_attenuator,
    appserver=_appserver,
)

# old version keyword under robotws5g/resource compatibility workaround
# tl = TestlineWrapper(tl)