__maintainer__ = "Damian Siwa"
__team__ = "TRSSEC"
__email__ = "I_EXT_5G_IV_TRSSEC@internal.nsn.com"

import os
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline.enb import RealEnb
from taf.config.testline import NetworkAddress
from taf.config.testline import RoutingInformation
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.pdu import ATEN
from taf.config.testline.radio import RU
from taf.config.testline.gnb.du import Cablink, Endpoint
from taf.config.testline.core import RealCore, RealCore5GDetails, AMF

__all__ = ["tl"]

_lmp_vm_gnb_1 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.43.82.79", username="ute", password="ute"
    )
)

cfg_dir = os.path.dirname(os.path.abspath(__file__))

_cu_gnb_1 = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="",
        v6="",
        vlan_id=480,
        routing_v4=RoutingInformation(gateway="", ip_prefix_length=26),
        routing_v6=RoutingInformation(
            gateway="2A00:8A00:6000:607C::1:b901", ip_prefix_length=120
        ),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.255.129", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.63.87.179",
        v6="",
        vlan_id=481,
        routing_v4=RoutingInformation(gateway="10.63.87.161", ip_prefix_length=26),
        routing_v6=RoutingInformation(
            gateway="2A00:8A00:6000:607C::1:b901", ip_prefix_length=120
        ),
    ),
    x2u=NetworkAddress(
        v4="10.63.87.147",
        v6="",
        vlan_id=482,
        routing_v4=RoutingInformation(gateway="10.63.87.129", ip_prefix_length=26),
        routing_v6=RoutingInformation(
            gateway="2A00:8A00:6000:607C::1:b901", ip_prefix_length=120
        ),
    ),
    s1u=NetworkAddress(
        v4="10.63.87.115",
        v6="",
        vlan_id=483,
        routing_v4=RoutingInformation(gateway="10.63.87.97", ip_prefix_length=26),
        routing_v6=RoutingInformation(
            gateway="2A00:8A00:6000:607C::1:b901", ip_prefix_length=120
        ),
    ),
    ngu=NetworkAddress(
        v4="10.63.87.211",
        v6="",
        vlan_id=824,
        routing_v4=RoutingInformation(gateway="10.63.87.193", ip_prefix_length=26),
        routing_v6=RoutingInformation(
            gateway="2A00:8A00:6000:607C::1:b901", ip_prefix_length=120
        ),
    ),
    ngc=NetworkAddress(
        v4="10.63.87.243",
        v6="",
        vlan_id=895,
        routing_v4=RoutingInformation(gateway="10.63.87.225", ip_prefix_length=26),
        routing_v6=RoutingInformation(
            gateway="2A00:8A00:6000:607C::1:b901", ip_prefix_length=120
        ),
    ),
    xnc=NetworkAddress(
        v4="10.43.82.243",
        v6="",
        vlan_id=481,
        routing_v4=RoutingInformation(gateway="10.43.82.225", ip_prefix_length=26),
        routing_v6=RoutingInformation(
            gateway="2A00:8A00:6000:607C::1:b901", ip_prefix_length=120
        ),
    ),
    xnu=NetworkAddress(
        v4="10.43.82.211",
        v6="",
        vlan_id=482,
        routing_v4=RoutingInformation(gateway="10.43.82.193", ip_prefix_length=26),
        routing_v6=RoutingInformation(
            gateway="2A00:8A00:6000:607C::1:b901", ip_prefix_length=120
        ),
    ),
)

_pdu_gnb = ATEN(addr="10.43.82.120", port_numbers=[8])

_pdu_gnb_ru = ATEN(addr="10.43.82.120", port_numbers=[8])

_gnb_ru = RU(
    ru_hw_group="AEQN",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52",
        username="root",
        password="w@=EIj7P6R0bVy85OjCVa^ho&8",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    pdu_port=_pdu_gnb_ru.pdu_ports[8],
)

_abil1_gnb_1_master = CapacityUnit(addr="192.168.253.20")

_abil1_gnb_1_slave = CapacityUnit(addr="192.168.253.21")

_abil1_gnb_1_loner = CapacityUnit(addr="192.168.253.22")

_asik_gnb_1 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_abil1_gnb_1_master, _abil1_gnb_1_loner, _abil1_gnb_1_slave],
    pdu_port=_pdu_gnb.pdu_ports[8],
)

_airscale_gnb_1 = Airscale(common_units=[_asik_gnb_1])

_ru_cablinks = [
    Cablink(
        source=Endpoint(unit=_abil1_gnb_1_master, label="SFP", port_id=1),
        target=Endpoint(unit=_gnb_ru, label="SFP", port_id=2),
    )
]

_du_1_gnb_1 = DU(airscale=_airscale_gnb_1, rus=[_gnb_ru], cablinks=_ru_cablinks)

_pdu_enb = ATEN(addr="10.43.82.120", port_numbers=[8])

_asik_enb_1 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_abil1_gnb_1_master, _abil1_gnb_1_loner, _abil1_gnb_1_slave],
    pdu_port=_pdu_enb.pdu_ports[8],
)

_airscale_enb_1 = Airscale(common_units=[_asik_enb_1])

_enb_1 = RealEnb(
    airscale=_airscale_enb_1,
    global_bts_id=40277,
    instance_id=40277,
    x2_link_addr=NetworkAddress(
        # 2a00:8a00:6000:607c::1:bd2b	487		26	10.44.90.65	10.44.90.103
        v4="",
        v6="",
        vlan_id=487,
        routing_v4=RoutingInformation(gateway="10.44.90.65", ip_prefix_length=26),
        routing_v6=RoutingInformation(
            gateway="2a00:8a00:6000:607c::1:bd01", ip_prefix_length=120
        ),
    ),
)

_enb_1.m_plane = NetworkAddress(
    # 2a00:8a00:6000:607c::1:bc2b	486		26	10.44.90.1	10.44.90.39
    v4="",
    v6="",
    vlan_id=486,
    routing_v4=RoutingInformation(gateway="10.44.90.1", ip_prefix_length=26),
    routing_v6=RoutingInformation(
        gateway="2a00:8a00:6000:607c::1:bc01", ip_prefix_length=120
    ),
)

_cbts = ClassicalBts(
    cu=_cu_gnb_1, dus=[_du_1_gnb_1], global_bts_id=50287, instance_id=50287
)

_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ASIL_ABIO_AHLOA_eCPRI"


_amf_ssh = SshServiceDetails(
    addr="to_be_updated", username="to_be_updated", password="to_be_updated"
)

_amf_n2_addr = NetworkAddress(
    v4="100.70.20.75", v6="2a00:8a00:4000:65ef:ffff:ffff:ffff:b804", vlan_id=None
)

_amf = AMF(oam_ssh_connection_details=_amf_ssh, n2=_amf_n2_addr)

_core = RealCore(five_g=RealCore5GDetails(amf=_amf, tac=7151), mcc=540, mnc=1)
_cu_gnb_1.m = NetworkAddress(
    # 2a00:8a00:6000:607c::1:b637	480		26	10.44.88.129	10.44.88.177
    v4="10.44.88.177",
    v6="2a00:8a00:6000:607c::1:b637",
    vlan_id=480,
    routing_v4=RoutingInformation(gateway="10.44.88.129", ip_prefix_length=26),
    routing_v6=RoutingInformation(
        gateway="2a00:8a00:6000:607c::1:b601", ip_prefix_length=120
    ),
)
# temp _enb_1.m
_enb_1.m = NetworkAddress(
    # 2a00:8a00:6000:607c::1:bc2b	486		26	10.44.90.1	10.44.90.39
    v4="10.44.90.39",
    v6="2a00:8a00:6000:607c::1:bc2b",
    vlan_id=486,
    routing_v4=RoutingInformation(gateway="10.44.90.1", ip_prefix_length=26),
    routing_v6=RoutingInformation(
        gateway="2a00:8a00:6000:607c::1:bc01", ip_prefix_length=120
    ),
)
_lmp_vm_enb_1 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.44.149.85", username="ute", password="ute"  # need to fill
    ),
    connections=[_enb_1],
)

tl = TestLine(
    test_pc=_lmp_vm_gnb_1,
    gnbs=[_cbts],
    # core=_core,
    tl_cloud_topology=_tl_cloud_topology,
    test_pcs=[_lmp_vm_gnb_1, _lmp_vm_enb_1],
)
