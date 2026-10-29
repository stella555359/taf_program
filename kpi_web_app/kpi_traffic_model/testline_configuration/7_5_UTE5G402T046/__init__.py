import os
import yaml
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc, Connection
from taf.config.testline.gnb.du import DU, Cablink, Endpoint
from taf.config.testline.pdu import (
    FACOM,
    PduPort,
    Pdu,
    EPC,
    ATEN,
    RRB,
    APC,
    Gude,
    HBTE,
    TopYoung,
)
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
from taf.config.testline.attenuator import AttenuationPort

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
from taf.config.testline.attenuator import HBTE as ATTEN_HBTE
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

__maintainer__ = "Dandan Fang"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_4_GMS <I_MN_5G_RAN_IV4_LINE_HZG_4@internal.nsn.com>"
)
__email__ = "dandan.fang@nokia-sbell.com"

# common
__all__ = ["tl"]
_cfg_dir = os.path.dirname(os.path.abspath(__file__))


_attenuator = ATTEN_HBTE(
    ip_addr="10.71.204.116",
    port=5000,
    model="PA-16-16-6-127-0.5-B-S",
    attenuation_port_numbers=[
        129,
        159,
        162,
        192,
        195,
        228,
        133,
        166,
        199,
        222,
        232,
        137,
        170,
        203,
        223,
        236,
        253,
        256,
        141,
        174,
        207,
        240,
        145,
        178,
        211,
        244,
        149,
        182,
        215,
        248,
    ],
)
_appserver_ssh = SshServiceDetails(
    addr="10.57.191.194", username="vrf3_sg1", password="vrf3@sg1", port="41092"
)
_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.194",
    iperf_path="iperf",
    port="41092",
)


_appserver = AppServer(_iperf_details_on_appserver)

# #Qualcomm
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.194",
    iperf_path="/cygdrive/c/iperf",
    port="41093",
)

_android_0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.0.176.128", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="775afd09",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python38/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "sdx65", "qct_dx50"],
    clear_server_files="yes",
    clear_logs="yes",
    network_mode_switch_method="keyevents",
    mobile_network_text="Mobile network",
    setting_network_mode_text="Preferred network type",
)
# RealEnb---------------------------------------------------------
_real_enb_pdu = HBTE(addr="10.71.195.228", port_numbers=[8])

_capacity_unit_enb = CapacityUnit(addr="192.168.253.20", hardware_type="ABIA")

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.71.210.230", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_capacity_unit_enb],
    pdu_port=_real_enb_pdu.pdu_ports[8],
    hardware_type="ASIA",
)
_real_enb = Airscale(common_units=[_common_unit_2])
_lte_ru_0 = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=None,
    radio_type=RadioTypes.AHIB,
    serial_number="EA174610753",
    attenuation_ports=[
        _attenuator.attenuator_ports[222],
        _attenuator.attenuator_ports[253],
    ],
)
_lte_real_enb = RealEnb(
    airscale=_real_enb, rms=[_lte_ru_0], instance_id=11000, global_bts_id=11000
)


# 5GRU------------------------------------
_ru_pdu_046_0 = TopYoung(addr="10.71.195.230", port_numbers=[1])
_ru_pdu_046_1 = TopYoung(addr="10.71.195.230", port_numbers=[3])
_ru_pdu_046_2 = TopYoung(addr="10.71.195.230", port_numbers=[5])
_ru_pdu_046_3 = TopYoung(addr="10.71.195.230", port_numbers=[2])
_ru_pdu_046_4 = TopYoung(addr="10.71.195.230", port_numbers=[4])
_ru_pdu_046_5 = TopYoung(addr="10.71.195.230", port_numbers=[6])


_ru_046_0 = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_ru_pdu_046_0.pdu_ports[1],
    radio_type=RadioTypes.AWHHF,
    serial_number="AH222300359",
    attenuation_ports=[
        _attenuator.attenuator_ports[129],
        _attenuator.attenuator_ports[162],
        _attenuator.attenuator_ports[195],
        _attenuator.attenuator_ports[228],
    ],
)
_ru_046_1 = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_ru_pdu_046_1.pdu_ports[3],
    radio_type=RadioTypes.AWHHF,
    serial_number="AH222300371",
    attenuation_ports=[
        _attenuator.attenuator_ports[133],
        _attenuator.attenuator_ports[166],
        _attenuator.attenuator_ports[199],
        _attenuator.attenuator_ports[232],
    ],
)

_ru_046_2 = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_ru_pdu_046_2.pdu_ports[5],
    radio_type=RadioTypes.AWHHF,
    serial_number="AH222300357",
    attenuation_ports=[
        _attenuator.attenuator_ports[137],
        _attenuator.attenuator_ports[170],
        _attenuator.attenuator_ports[203],
        _attenuator.attenuator_ports[236],
    ],
)

_ru_046_3 = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_ru_pdu_046_3.pdu_ports[2],
    radio_type=RadioTypes.AWHHF,
    serial_number="AH222300378",
    attenuation_ports=[
        _attenuator.attenuator_ports[141],
        _attenuator.attenuator_ports[174],
        _attenuator.attenuator_ports[207],
        _attenuator.attenuator_ports[240],
    ],
)

_ru_046_4 = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_ru_pdu_046_4.pdu_ports[4],
    radio_type=RadioTypes.AWHHF,
    serial_number="AH222300379",
    attenuation_ports=[
        _attenuator.attenuator_ports[145],
        _attenuator.attenuator_ports[178],
        _attenuator.attenuator_ports[211],
        _attenuator.attenuator_ports[244],
    ],
)

_ru_046_5 = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_ru_pdu_046_5.pdu_ports[6],
    radio_type=RadioTypes.AWHHF,
    serial_number="AH222300351",
    attenuation_ports=[
        _attenuator.attenuator_ports[149],
        _attenuator.attenuator_ports[182],
        _attenuator.attenuator_ports[215],
        _attenuator.attenuator_ports[248],
    ],
)

# #DU
_lmp_connection_046 = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_046 = CapacityUnit(addr="192.168.253.20", hardware_type="ABIO")
_capacity_unit_046_2 = CapacityUnit(addr="192.168.253.24", hardware_type="ABIO")
_ru_cablinks = [
    Cablink(
        source=Endpoint(unit=_capacity_unit_046, label="OPT", port_id=1),
        target=Endpoint(unit=_ru_046_0, label="OPT", port_id=1),
    ),
    Cablink(
        source=Endpoint(unit=_capacity_unit_046, label="OPT", port_id=2),
        target=Endpoint(unit=_ru_046_1, label="OPT", port_id=1),
    ),
    Cablink(
        source=Endpoint(unit=_capacity_unit_046, label="OPT", port_id=3),
        target=Endpoint(unit=_ru_046_2, label="OPT", port_id=1),
    ),
    Cablink(
        source=Endpoint(unit=_capacity_unit_046, label="OPT", port_id=7),
        target=Endpoint(unit=_ru_046_3, label="OPT", port_id=1),
    ),
    Cablink(
        source=Endpoint(unit=_capacity_unit_046, label="OPT", port_id=8),
        target=Endpoint(unit=_ru_046_4, label="OPT", port_id=1),
    ),
    Cablink(
        source=Endpoint(unit=_capacity_unit_046, label="OPT", port_id=9),
        target=Endpoint(unit=_ru_046_5, label="OPT", port_id=1),
    ),
    Cablink(
        source=Endpoint(unit=_capacity_unit_046_2, label="OPT", port_id=1),
        target=Endpoint(unit=_ru_046_0, label="OPT", port_id=2),
    ),
    Cablink(
        source=Endpoint(unit=_capacity_unit_046_2, label="OPT", port_id=2),
        target=Endpoint(unit=_ru_046_1, label="OPT", port_id=2),
    ),
    Cablink(
        source=Endpoint(unit=_capacity_unit_046_2, label="OPT", port_id=3),
        target=Endpoint(unit=_ru_046_2, label="OPT", port_id=2),
    ),
    Cablink(
        source=Endpoint(unit=_capacity_unit_046_2, label="OPT", port_id=7),
        target=Endpoint(unit=_ru_046_3, label="OPT", port_id=2),
    ),
    Cablink(
        source=Endpoint(unit=_capacity_unit_046_2, label="OPT", port_id=8),
        target=Endpoint(unit=_ru_046_4, label="OPT", port_id=2),
    ),
    Cablink(
        source=Endpoint(unit=_capacity_unit_046_2, label="OPT", port_id=9),
        target=Endpoint(unit=_ru_046_5, label="OPT", port_id=2),
    ),
]

_gnb_pdu = HBTE(addr="10.71.195.228", port_numbers=[1])

_common_unit_046 = CommonUnit(
    lmp_connection=_lmp_connection_046,
    capacity_units=[_capacity_unit_046, _capacity_unit_046_2],
    pdu_port=_gnb_pdu.pdu_ports[1],
    hardware_type="ASIL",
)
_airscale_046 = Airscale(common_units=[_common_unit_046])

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.217.78", username="ute", password="uteUTE!"
    ),
    connections=[
        Connection(interface="eth1", device=_common_unit_046, interface_type="lmp")
    ],
)

_du_046 = DU(
    airscale=_airscale_046,
    rus=[_ru_046_0, _ru_046_1, _ru_046_2, _ru_046_3, _ru_046_4, _ru_046_5],
    f1_m_ip_addr="192.168.255.129",
    cablinks=_ru_cablinks,
)
# CU
_cu_046 = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.71.210.233",
        vlan_id=None,
        routing_v4=RoutingInformation(gateway="10.71.210.225/27"),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.255.129", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.71.210.233",
        vlan_id=None,
        routing_v4=RoutingInformation(gateway="10.71.210.225/27"),
    ),
    x2u=NetworkAddress(
        v4="10.71.210.233",
        vlan_id=None,
        routing_v4=RoutingInformation(gateway="10.71.210.225/27"),
    ),
    s1u=NetworkAddress(
        v4="10.71.210.233",
        vlan_id=None,
        routing_v4=RoutingInformation(gateway="10.71.210.225/27"),
    ),
)

# classicalbts------------------------------------------------
_classical_bts_046 = ClassicalBts(
    dus=[_du_046], cu=_cu_046, instance_id=11433, global_bts_id=11433
)
# #cloud_topology------------------------------------------------
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ANDROID_ASILL_ABIOB1B2_6xAWHHF_ENB"
# #realcore4g
_mme_oam_ssh_connection_details = SshServiceDetails(
    addr="x.x.x.x", username="ute1", password="ute1"
)
_s1_address = NetworkAddress(v4="xxx.xxx.xx.xx", v6="xxx:xx::xxx", vlan_id=1)
_mme = MME(oam_ssh_connection_details=_mme_oam_ssh_connection_details, s1=_s1_address)
_real_4g_core_details = RealCore4GDetails(mme=_mme)
# #realcore5g
_amf_oam_ssh_connection_details = SshServiceDetails(
    addr="x.x.x.x", username="ute1", password="ute1"
)
_n2_address = NetworkAddress(v4="10.110.133.68")
_amf = AMF(oam_ssh_connection_details=_amf_oam_ssh_connection_details, n2=_n2_address)
_real_5g_core_details = RealCore5GDetails(amf=_amf)
_realcore = RealCore(
    four_g=_real_4g_core_details,
    five_g=_real_5g_core_details,
    mcc="262",
    mnc="3",
    pdn=None,
)

tl = TestLine(
    test_pc=_host,
    test_pcs=[_host],
    # enbs=[_lte_real_enb],
    gnbs=[_classical_bts_046],
    ues=[_android_0, _lte_real_enb],
    tl_cloud_topology=_tl_cloud_topology,
    appserver=_appserver,
    attenuators=[_attenuator],
    core=_realcore,
)
