import os
import yaml
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.core import RealCore
from taf.config.testline import RU, DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, ATEN, RRB, APC, Gude, FPFH
from taf.config.testline.pdu import HBTE as pdu_HBTE
from taf.config.testline.pdu import TopYoung as pdu_TopYoung
from taf.config.testline.testline import TestLine
from taf.config.testline.ue import Android
from taf.config.testline.gnb import CU, ClassicalBts
from taf.config.testline.gnb.du import Cablink, Endpoint
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
from taf.config.testline import (
    Enb,
    SimEnb,
    RealEnb,
    LTEEmuEnb,
    PrismaEnb,
    DocomoEnb,
)

# from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)
from taf.config.testline.attenuator import AttenuationPort, TopYoung
from taf.config.testline.attenuator import HBTE as AHBTE
from taf.config.testline import NetworkAddress, RoutingInformation
from taf.config.testline.appserver import AppServer

__maintainer__ = "He,winnie"
__team__ = "NSB MN SRAN PROD IWK HZ GMS "
__email__ = "winnie.he@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

_attenuator = TopYoung(
    ip_addr="10.71.199.117",
    port=3000,
    attenuation_port_numbers=[i for i in range(1, 16)],
    model="TAS16T16-51-120-1S-DES",
)

_appserver_ssh = SshServiceDetails(
    addr="10.71.207.141",
    username="vrf3_sg8",
    password="vrf3@sg8",
    port="50002"
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.207.141",
    iperf_path="/usr/bin/",
    port="50002",
)
_appserver = AppServer(_iperf)

ue_config_path = os.path.join(_cfg_dir, "TestData/inseego.yml")
if os.path.isfile(ue_config_path):
    with open(ue_config_path) as f:
        ue_config = yaml.load(stream=f, Loader=yaml.FullLoader)
else:
    ue_config = ""

"""
# CI_Detail_UE_Type='Qualcomm'
"""
#_ue1 = Android(
#    ssh_connection_details=SshServiceDetails(
#        addr="10.68.86.137", username="nokia5G", password="noki@123"
#    ),
#    serial_number="5CG51711SD",
#    server_dir="/cygdrive/c/pyro_server",
#    python_path="C:/Python27/python.exe",
#    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
#    diag_cfg_path="C:/pyro_server/DIAG.cfg",
#    iperf_details=_iperf,
#    capabilities=["REAL_ANDROID_UE"],
#)

# 5GRU for classicalBTS RU PB
_ru0_pdu = pdu_TopYoung(addr="10.71.195.237", port_numbers=[1])
_ru0 = RU(
    ru_hw_group="AHEH",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.73.128", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.73.128", username="root", password="umniedziala"
    ),
    pdu_port=_ru0_pdu.pdu_ports[1],
    radio_type=RadioTypes.AHEH,
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[9],
    ],
)
_ru1_pdu = pdu_TopYoung(addr="10.71.195.237", port_numbers=[2])
_ru1 = RU(
    ru_hw_group="AKNB",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.73.128", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.73.128", username="root", password="umniedziala"
    ),
    pdu_port=_ru1_pdu.pdu_ports[2],
    radio_type=RadioTypes.AKNB,
    attenuation_ports=[
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
        _attenuator.attenuator_ports[11],
        _attenuator.attenuator_ports[12],
    ],
)

# DU for classicalBTS
_gnb_pdu = pdu_HBTE(addr="10.71.195.236", port_numbers=[3])
_lmp_connection = SshServiceDetails(
    addr="10.71.199.118", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(addr="192.168.253.20", hardware_type="ASIB")

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    hardware_type="ASIB",
    pdu_port=_gnb_pdu.pdu_ports[3],
)
_ru_cablinks = [
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=1),
        target=Endpoint(unit=_ru0, label="SFP", port_id=1),
    ),
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=2),
        target=Endpoint(unit=_ru0, label="SFP", port_id=2),
    ),
]
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(airscale=_airscale, rus=[_ru0, _ru1], f1_m_ip_addr="10.71.199.118")


# CU
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.71.199.118",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.199.113", ip_prefix_length=28),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.199.118", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.199.118", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.71.199.118",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.199.113", ip_prefix_length=28),
    ),
    x2u=NetworkAddress(
        v4="10.71.199.118",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.199.113", ip_prefix_length=28),
    ),
    s1u=NetworkAddress(
        v4="10.71.199.118",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.199.113", ip_prefix_length=28),
    ),
)

# RealEnb

_lmp_connection_enb = SshServiceDetails(
    addr="10.71.199.118", username="toor4nsn", password="oZPS0POrRieRtu"
)

_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection_enb,
    capacity_units=[],

)
_real_enb = Airscale(common_units=[_common_unit_1])
_lte_real_enb = RealEnb(airscale=_real_enb)

# cloud_topology
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ANDROID_SA_CA_ASIBL_ABIOB1_AHEH"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=37853, global_bts_id=37853)
# test pc
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.115", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    connections=[_classical_bts.dus[0].airscale.common_units[0], ue_config],
)

tl = TestLine(
    test_pc=_host,
    test_pcs=[_host],
    gnbs=[_classical_bts],
    enbs=[_lte_real_enb],
    tl_cloud_topology=_tl_cloud_topology,
    core=RealCore(mcc=460, mnc=2),
    appserver=_appserver,
    ues=[ue_config],
    attenuator=_attenuator,

)
