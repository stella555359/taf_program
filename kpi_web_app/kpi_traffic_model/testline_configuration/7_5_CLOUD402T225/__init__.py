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
from taf.config.testline.gnb.du import Cablink, Endpoint
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline import RealEnb
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
from taf.config.testline.testpc import Connection

__maintainer__ = "Chen Yin"  # TL owner name
__team__ = "I_NSB_MN_5GSC_5G_PZ_HZ_02_GMS <I_NSB_MN_5GSC_5G_PZ_HZ_02@internal.nsn.com>"  # TL owner's team
__email__ = "yin.1.chen@nokia-sbell.com"  # TL owner's email

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# 5GRU for classicalBTS
_ru1_pdu = HBTE(addr="10.57.172.78", port_numbers=[7])

_ru1 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.52", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    pdu_port=_ru1_pdu.pdu_ports[7],
    radio_type=RadioTypes.AHQK.value,
    signal_analyzer=None,
)

_ru2_pdu = HBTE(addr="10.57.172.78", port_numbers=[8])

_ru2 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.86", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.86", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    pdu_port=_ru2_pdu.pdu_ports[8],
    radio_type=RadioTypes.AHQK.value,
    signal_analyzer=None,
)


# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit1 = CapacityUnit(
    addr="192.168.253.20",
    hardware_type="ABIO",
)
_gnb_pdu = HBTE(addr="10.57.242.44", port_numbers=[4])

_ru_cablinks = [
    Cablink(
        source=Endpoint(unit=_capacity_unit1, label="SFP", port_id=1),
        target=Endpoint(unit=_ru1, label="SFP", port_id=1),
    ),
    Cablink(
        source=Endpoint(unit=_capacity_unit1, label="SFP", port_id=2),
        target=Endpoint(unit=_ru2, label="SFP", port_id=1),
    ),
]

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit1],
    pdu_port=_gnb_pdu.pdu_ports[4],
    hardware_type="ASIM",
)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(
    airscale=_airscale,
    rus=[_ru1, _ru2],
    f1_m_ip_addr="192.168.255.1",
    cablinks=_ru_cablinks,
)

# CU
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.57.223.239",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.57.223.225", ip_prefix_length=26),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.1", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.255.1", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.57.223.239",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.57.223.225", ip_prefix_length=26),
    ),
    x2u=NetworkAddress(
        v4="10.57.223.239",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.57.223.225", ip_prefix_length=26),
    ),
    s1u=NetworkAddress(
        v4="10.57.223.239",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.57.223.225", ip_prefix_length=26),
    ),
)

# RealEnb
_lmp_connection_enb = SshServiceDetails(
    addr="10.57.231.125", username="toor4nsn", password="oZPS0POrRieRtu"
)
_enb_pdu = HBTE(addr="10.57.242.44", port_numbers=[4])
_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection_enb,
    capacity_units=[],
    pdu_port=_enb_pdu.pdu_ports[4],
)
_real_enb = Airscale(common_units=[_common_unit_1])
_lte_real_enb = RealEnb(airscale=_real_enb, rms=None)

# cloud_topology
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ASIMR_ABIOB4_AHQK_ENB"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=225, global_bts_id=225)

# test pc
_gnb_testpc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.169.74", username="ute", password="ute"
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_classical_bts.dus[0].airscale.common_units[0],
            interface_type="lmp",
        )
    ],
)

_enb_testpc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.169.74", username="ute", password="ute"
    ),
    connections=[],
)


tl = TestLine(
    test_pc=_gnb_testpc,
    test_pcs=[_gnb_testpc],
    gnbs=[_classical_bts],
    enbs=[_lte_real_enb],
    core=RealCore(mcc=262, mnc=3),
    tl_cloud_topology=_tl_cloud_topology,
)
