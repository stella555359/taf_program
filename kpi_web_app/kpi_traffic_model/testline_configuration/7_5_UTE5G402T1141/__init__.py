import os
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.core import RealCore
from taf.config.testline import RU, DU
from taf.config.testline.pdu import HBTE
from taf.config.testline.testline import TestLine
from taf.config.testline.ue import Android
from taf.config.testline.gnb import CU, ClassicalBts
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
from taf.config.testline import RealEnb
from taf.compatibility.configuration import TestlineWrapper
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

__maintainer__ = "cai lanwen"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_8_GMS <I_MN_5G_RAN_IV8_LINE_HZG_5@internal.nsn.com>"
)
__email__ = "lanwen.cai@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

_attenuator = AHBTE(
    ip_addr="10.101.52.195",
    port=5000,
    attenuation_port_numbers=[13, 14, 15, 16],
    model="PA-16-16-6-127-0.5-B-S",
)
# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.11", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_appserver_ssh = SshServiceDetails(
    addr="10.57.162.11", username="cmw_sg8", password="Bestcm@8", port="58018"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.162.11",
    iperf_path="/usr/bin/iperf",
    port="58330",
)
_appserver = AppServer(_iperf)

# CI_Detail_UE_Type='Samsung'
_ue1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.68.86.226", username="nokia5G", password="noki@123"
    ),
    serial_number="RFCR20M0T2W",
    server_dir="/cygdrive/c/pyro_server",
    python_path="/cygdrive/c/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["Samsung"],
)

# 5GRU for classicalBTS RU PB
_ru_pdu = HBTE(addr="10.101.46.46", port_numbers=[2])

_ru = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.48.2", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.3", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu.pdu_ports[2],
    radio_type=RadioTypes.AZQU,
    attenuation_ports=[
        _attenuator.attenuator_ports[13],
        _attenuator.attenuator_ports[14],
        _attenuator.attenuator_ports[15],
        _attenuator.attenuator_ports[16],
    ],
)


# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.101.52.194", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(addr="192.168.253.20")
_gnb_pdu = HBTE(addr="10.101.45.202", port_numbers=[1])
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[1],
)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(airscale=_airscale, rus=[_ru], f1_m_ip_addr="10.101.52.194")

# CU
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.101.52.194",
        routing=RoutingInformation(gateway="10.101.52.193", ip_prefix_length=27),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.52.194", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.52.194", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.101.52.194",
        routing=RoutingInformation(gateway="10.101.52.193", ip_prefix_length=27),
    ),
    x2u=NetworkAddress(
        v4="10.101.52.194",
        routing=RoutingInformation(gateway="10.101.52.193", ip_prefix_length=27),
    ),
    s1u=NetworkAddress(
        v4="10.101.52.194",
        routing=RoutingInformation(gateway="10.101.52.193", ip_prefix_length=27),
    ),
)

# RealEnb
_lmp_connection_enb = SshServiceDetails(
    addr="10.101.52.200", username="toor4nsn", password="oZPS0POrRieRtu"
)
_enb_pdu = HBTE(addr="10.101.45.200", port_numbers=[1])
_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection_enb,
    capacity_units=[],
    pdu_port=_enb_pdu.pdu_ports[1],
)
_real_enb = Airscale(common_units=[_common_unit_1])
_lte_real_enb = RealEnb(airscale=_real_enb, rms=None)

# cloud_topology
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ASIB_ABIO_AEQZ"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=1141, global_bts_id=1141)

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    enbs=[_lte_real_enb],
    appserver=_appserver,
    ues=[_ue1],
    core=RealCore(mcc=262, mnc=3),
    attenuator=_attenuator,
    tl_cloud_topology=_tl_cloud_topology,
)
