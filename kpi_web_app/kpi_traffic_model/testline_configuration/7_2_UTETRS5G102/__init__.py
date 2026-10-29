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
from taf.config.testline.gnb.du import Cablink, Endpoint
from taf.config.testline import NetworkAddress
from taf.config.testline import RoutingInformation
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.pdu import ATEN
from taf.config.testline.radio import RU
from taf.config.testline.core import RealCore, RealCore5GDetails, AMF

__all__ = ["tl"]

_lmp_vm_gnb_1 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.43.82.73", username="ute", password="ute"
    )
)

cfg_dir = os.path.dirname(os.path.abspath(__file__))

_cu_gnb_1 = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.63.86.206",
        v6="2a00:8a00:a000:11b0::3bce",
        vlan_id=237,
        routing_v4=RoutingInformation(gateway="10.63.86.193", ip_prefix_length=27),
        routing_v6=RoutingInformation(
            gateway="2a00:8a00:a000:11b0::3bc1", ip_prefix_length=123
        ),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.255.129", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.63.87.174",
        v6="2a00:8a00:a000:11b0::3cae",
        vlan_id=244,
        routing_v4=RoutingInformation(gateway="10.63.87.161", ip_prefix_length=27),
        routing_v6=RoutingInformation(
            gateway="2a00:8a00:a000:11b0::3ca1", ip_prefix_length=123
        ),
    ),
    x2u=NetworkAddress(
        v4="10.63.87.142",
        v6="2a00:8a00:a000:11b0::3c8e",
        vlan_id=243,
        routing_v4=RoutingInformation(gateway="10.63.87.129", ip_prefix_length=27),
        routing_v6=RoutingInformation(
            gateway="2a00:8a00:a000:11b0::3c81", ip_prefix_length=123
        ),
    ),
    s1u=NetworkAddress(
        v4="10.63.87.110",
        v6="2a00:8a00:a000:11b0::3c6e",
        vlan_id=242,
        routing_v4=RoutingInformation(gateway="10.63.87.97", ip_prefix_length=27),
        routing_v6=RoutingInformation(
            gateway="2a00:8a00:a000:11b0::3c61", ip_prefix_length=123
        ),
    ),
    ngu=NetworkAddress(
        v6="2a00:8a00:a000:11b0::3cce",
        v4="10.63.87.206",
        vlan_id=245,
        routing_v4=RoutingInformation(gateway="10.63.87.193", ip_prefix_length=27),
        routing_v6=RoutingInformation(
            gateway="2a00:8a00:a000:11b0::3cc1", ip_prefix_length=123
        ),
    ),
    ngc=NetworkAddress(
        v6="2a00:8a00:a000:11b0::3cee",
        v4="10.63.87.238",
        vlan_id=246,
        routing_v4=RoutingInformation(gateway="10.63.87.225", ip_prefix_length=27),
        routing_v6=RoutingInformation(
            gateway="2a00:8a00:a000:11b0::3ce1", ip_prefix_length=123
        ),
    ),
    xnc=NetworkAddress(
        v4="10.43.82.238",
        v6="2a00:8a00:a000:11b0::3dee",
        vlan_id=248,
        routing_v4=RoutingInformation(gateway="10.43.82.225", ip_prefix_length=27),
        routing_v6=RoutingInformation(
            gateway="2a00:8a00:a000:11b0::3de1", ip_prefix_length=123
        ),
    ),
    xnu=NetworkAddress(
        v4="10.43.82.206",
        v6="2a00:8a00:a000:11b0::3dce",
        vlan_id=247,
        routing_v4=RoutingInformation(gateway="10.43.82.193", ip_prefix_length=27),
        routing_v6=RoutingInformation(
            gateway="2a00:8a00:a000:11b0::3dc1", ip_prefix_length=123
        ),
    ),
)
_pdu_gnb = ATEN(addr="10.43.82.120", port_numbers=[2])
_pdu_gnb_ru = ATEN(addr="10.43.82.120", port_numbers=[2])
_gnb_ru = RU(
    ru_hw_group="AHLOA",
    radio_type="AHLOA",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52",
        username="root",
        password="umniedziala",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="root", password="umniedziala"
    ),
    pdu_port=_pdu_gnb_ru.pdu_ports[2],
)

_abil1_gnb_1_master = CapacityUnit(addr="192.168.253.20")

_abil1_gnb_1_slave = CapacityUnit(addr="192.168.253.21")

_abil1_gnb_1_loner = CapacityUnit(addr="192.168.253.22")

_asik_gnb_1 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_abil1_gnb_1_master, _abil1_gnb_1_loner, _abil1_gnb_1_slave],
    pdu_port=_pdu_gnb.pdu_ports[2],
)

_airscale_gnb_1 = Airscale(common_units=[_asik_gnb_1])

_ru_cablinks = [
    Cablink(
        source=Endpoint(unit=_abil1_gnb_1_master, label="SFP", port_id=1),
        target=Endpoint(unit=_gnb_ru, label="SFP", port_id=1),
    )
]

_du_1_gnb_1 = DU(airscale=_airscale_gnb_1, rus=[_gnb_ru], cablinks=_ru_cablinks)

_pdu_enb = ATEN(addr="10.43.82.120", port_numbers=[2])

_asik_enb_1 = CommonUnit(
    hardware_type="ASIK",
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_abil1_gnb_1_master, _abil1_gnb_1_loner, _abil1_gnb_1_slave],
    pdu_port=_pdu_enb.pdu_ports[2],
)

_airscale_enb_1 = Airscale(common_units=[_asik_enb_1])

_enb_1 = RealEnb(
    airscale=_airscale_enb_1,
    global_bts_id=40206,
    instance_id=40206,
    x2_link_addr=NetworkAddress(
        v6="2A00:8A00:6000:607C::5B19",
        v4="10.44.65.155",
        vlan_id=460,
        routing_v4=RoutingInformation(gateway="10.44.65.129", ip_prefix_length=26),
        routing_v6=RoutingInformation(
            gateway="2A00:8A00:6000:607C::5B01", ip_prefix_length=120
        ),
    ),
)

_enb_1.m_plane = NetworkAddress(
    v6="2A00:8A00:6000:607C::5A19",
    v4="10.44.65.91",
    vlan_id=459,
    routing_v4=RoutingInformation(gateway="10.44.65.65", ip_prefix_length=26),
    routing_v6=RoutingInformation(
        gateway="2A00:8A00:6000:607C::5A01", ip_prefix_length=120
    ),
)

_cbts = ClassicalBts(
    cu=_cu_gnb_1, dus=[_du_1_gnb_1], global_bts_id=50290, instance_id=50290
)

_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ASIK_ABIL_AHLOA_ENB"

_amf_ssh = SshServiceDetails(
    addr="to_be_updated", username="to_be_updated", password="to_be_updated"
)

_amf_n2_addr = NetworkAddress(
    v4="100.70.20.75", v6="2a00:8a00:4000:65ef:ffff:ffff:ffff:b804", vlan_id=None
)

_amf = AMF(oam_ssh_connection_details=_amf_ssh, n2=_amf_n2_addr)

_core = RealCore(
    five_g=RealCore5GDetails(amf=_amf, tac=400),
    mcc=404,
    mnc=99,
)
# temp _cu_gnb_1.m
_cu_gnb_1.m = (
    NetworkAddress(
        v4="10.44.65.90",
        v6="2A00:8A00:6000:607C::5A18",
        vlan_id=459,
        routing_v4=RoutingInformation(gateway="10.44.65.65", ip_prefix_length=26),
        routing_v6=RoutingInformation(
            gateway="2A00:8A00:6000:607C::5A01", ip_prefix_length=120
        ),
    ),
)
# temp _enb_1.m
_enb_1.m = NetworkAddress(
    v6="2A00:8A00:6000:607C::5A19",
    v4="10.44.65.91",
    vlan_id=459,
    routing_v4=RoutingInformation(gateway="10.44.65.65", ip_prefix_length=26),
    routing_v6=RoutingInformation(
        gateway="2A00:8A00:6000:607C::5A01", ip_prefix_length=120
    ),
)

_lmp_vm_enb_1 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.44.156.187", username="ute", password="ute"
    ),
    connections=[_enb_1],
)

with open(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "nokia_ue.yaml")
) as ue_config:
    import yaml

    _nokia_ue = yaml.load(ue_config, yaml.SafeLoader)

tl = TestLine(
    test_pc=_lmp_vm_gnb_1,
    gnbs=[_cbts],
    core=_core,
    ues=[_nokia_ue],
    tl_cloud_topology=_tl_cloud_topology,
    test_pcs=[_lmp_vm_gnb_1, _lmp_vm_enb_1],
)
