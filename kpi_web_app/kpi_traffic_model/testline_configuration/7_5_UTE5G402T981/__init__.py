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
from taf.config.testline import NetworkAddress, RoutingInformation
from taf.config.testline.appserver import AppServer

__maintainer__ = "zhang wei"  # TL owner name
__team__ = "I_NSB_MN_5GSC_5G_PZ_HZ_09 <I_NSB_MN_5GSC_5G_PZ_HZ_09@internal.nsn.com>"  # TL owner's team
__email__ = "wei.6.zhang@nokia-sbell.com"  # TL owner's email

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.211", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# 5GRU for classicalBTS
_ru_pdu = HBTE(addr="10.101.45.38", port_numbers=[2])

_ru = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.54", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.3", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu.pdu_ports[2],
    radio_type=RadioTypes.AEQV,
)

_ru1_pdu = HBTE(addr="10.101.45.38", port_numbers=[3])

_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.84", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.3", username="root", password="umniedziala"
    ),
    pdu_port=_ru1_pdu.pdu_ports[3],
    radio_type=RadioTypes.AEQV,
)

# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(addr="192.168.253.20")
_gnb_pdu = HBTE(addr="0.0.0.0", port_numbers=[6])
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[6],
)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(airscale=_airscale, rus=[_ru, _ru1], f1_m_ip_addr="10.101.49.4")

# CU
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.101.49.4",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.101.49.1", ip_prefix_length=24),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.49.4", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.49.4", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.101.49.4",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.101.49.1", ip_prefix_length=24),
    ),
    x2u=NetworkAddress(
        v4="10.101.49.4",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.101.49.1", ip_prefix_length=24),
    ),
    s1u=NetworkAddress(
        v4="10.101.49.4",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.101.49.1", ip_prefix_length=24),
    ),
)

# RealEnb
_lmp_connection_enb = SshServiceDetails(
    addr="10.101.49.5", username="toor4nsn", password="oZPS0POrRieRtu"
)
_enb_pdu = HBTE(addr="10.101.45.38", port_numbers=[4])
_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection_enb,
    capacity_units=[],
    pdu_port=_enb_pdu.pdu_ports[4],
)
_real_enb = Airscale(common_units=[_common_unit_1])
_lte_real_enb = RealEnb(airscale=_real_enb, rms=None)

# cloud_topology
_tl_cloud_topology = "I&V-HGZ-TL981"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=1154, global_bts_id=1154)

# switch Dtor
_dell_s4048on_ssh = SshServiceDetails(
    addr="0.0.0.0", port="1", username="5gran", password="nokia123"
)
_dell_s4048on_switch = DellS4048ONSwitch(_dell_s4048on_ssh)

# switch Mtor
_dell_s4048ton_ssh = SshServiceDetails(
    addr="0.0.0.0", port="1", username="5gran", password="nokia123"
)
_dell_s4048ton_switch = DellS4048TONSwitch(_dell_s4048ton_ssh)

_attenuator = TopYoung(ip_addr="x.x.x.x", port=23, attenuation_port_numbers=[7, 8])

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    enbs=[_lte_real_enb],
    core=RealCore(mcc=460, mnc=2),
    tl_cloud_topology=_tl_cloud_topology,
    attenuator=_attenuator,
    switches=[_dell_s4048on_switch, _dell_s4048ton_switch],
)
