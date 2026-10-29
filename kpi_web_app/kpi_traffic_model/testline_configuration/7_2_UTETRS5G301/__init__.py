__maintainer__ = "Prabakar Sanikommu"
__team__ = "TRSI&V"
__email__ = "prabakar.sanikommu@nokia.com"
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
from taf.config.testline.core import RealCore, RealCore5GDetails, AMF
from taf.config.testline.gnb.du import Cablink, Endpoint

__all__ = ["tl"]
_lmp_vm_gnb_1 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.43.82.77", username="ute", password="ute"
    )
)
cfg_dir = os.path.dirname(os.path.abspath(__file__))
_cu_gnb_1 = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.63.86.208",
        v6="2a00:8a00:a000:11b0::3bd0",
        vlan_id=237,
        routing_v4=RoutingInformation(gateway="10.63.86.193", ip_prefix_length=26),
        routing_v6=RoutingInformation(gateway="2a00:8a00:a000:11b0::3bc1", ip_prefix_length=120),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.255.129", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.43.87.144",
        v6="",
        vlan_id=244,
        routing_v4=RoutingInformation(gateway="10.63.87.161", ip_prefix_length=27),
        routing_v6=RoutingInformation(gateway="", ip_prefix_length=123),
    ),
    x2u=NetworkAddress(
        v4="10.43.87.144",
        v6="",
        vlan_id=243,
        routing_v4=RoutingInformation(gateway="10.63.87.161", ip_prefix_length=27),
        routing_v6=RoutingInformation(gateway="", ip_prefix_length=123),
    ),
    s1u=NetworkAddress(
        v4="10.63.87.111",
        v6="",
        vlan_id=242,
        routing_v4=RoutingInformation(gateway="10.63.87.129", ip_prefix_length=27),
        routing_v6=RoutingInformation(gateway="", ip_prefix_length=123),
    ),
    ngu=NetworkAddress(
        v4="10.63.87.208",
        v6="",
        vlan_id=245,
        routing_v4=RoutingInformation(gateway="10.63.87.193", ip_prefix_length=27),
        routing_v6=RoutingInformation(
            gateway="2A00:8A00:6000:607C::1:b901", ip_prefix_length=123
        ),
    ),
    ngc=NetworkAddress(
        v4="10.63.87.240",
        v6="",
        vlan_id=246,
        routing_v4=RoutingInformation(gateway="10.63.87.225", ip_prefix_length=27),
        routing_v6=RoutingInformation(gateway="", ip_prefix_length=123),
    ),
    xnc=NetworkAddress(
        v4="10.43.82.240",
        v6="",
        vlan_id=248,
        routing_v4=RoutingInformation(gateway="10.43.82.225", ip_prefix_length=27),
        routing_v6=RoutingInformation(gateway="", ip_prefix_length=123),
    ),
    xnu=NetworkAddress(
        v4="10.43.82.208",
        v6="",
        vlan_id=247,
        routing_v4=RoutingInformation(gateway="10.43.82.193", ip_prefix_length=27),
        routing_v6=RoutingInformation(gateway="", ip_prefix_length=123),
    ),
)
_pdu_gnb = ATEN(addr="10.43.82.120", port_numbers=[3, 6])
_pdu_gnb_ru = ATEN(addr="10.43.82.120", port_numbers=[1, 3])
_gnb_ru = RU(
    ru_hw_group="AEQN",
    radio_type="AEQN",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.10.1", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    pdu_port=_pdu_gnb_ru.pdu_ports[1],
)

_gnb_ru_2 = RU(
    ru_hw_group="AHLOA",
    radio_type="AHLOA",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.18.33", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="root", password="root"
    ),
    pdu_port=_pdu_gnb_ru.pdu_ports[1],
)

_abil1_gnb_1_master = CapacityUnit(addr="192.168.253.20")
_abil1_gnb_1_slave = CapacityUnit(addr="192.168.253.21")
_abil1_gnb_1_loner = CapacityUnit(addr="192.168.253.22")
_asik_gnb_1 = CommonUnit(
    hardware_type="ASIL",
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_abil1_gnb_1_master, _abil1_gnb_1_loner, _abil1_gnb_1_slave],
    pdu_port=_pdu_gnb.pdu_ports[3],
)
_airscale_gnb_1 = Airscale(common_units=[_asik_gnb_1])
_ru_cablinks = [
    Cablink(
        source=Endpoint(unit=_abil1_gnb_1_master, label="SFP", port_id=1),
        target=Endpoint(unit=_gnb_ru, label="SFP", port_id=2),
    )
]
_du_1_gnb_1 = DU(airscale=_airscale_gnb_1, rus=[_gnb_ru], cablinks=_ru_cablinks)
_pdu_enb = ATEN(
    addr="0.0.0.0", port_numbers=[3]
)  # <------------------------------------- need to fill
_asik_enb_1 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_abil1_gnb_1_master, _abil1_gnb_1_loner, _abil1_gnb_1_slave],
    pdu_port=_pdu_enb.pdu_ports[3],
)
_airscale_enb_1 = Airscale(common_units=[_asik_enb_1])
_enb_1 = RealEnb(
    airscale=_airscale_enb_1,
    global_bts_id=3914,
    instance_id=3914,
    x2_link_addr=NetworkAddress(
        v6="",  # No LTE
        v4="",  # No LTE
        vlan_id=455,
        routing_v4=RoutingInformation(gateway="10.44.64.65", ip_prefix_length=26),
        routing_v6=RoutingInformation(
            gateway="2A00:8A00:6000:607C::5601", ip_prefix_length=123
        ),
    ),
)
_enb_1.m_plane = NetworkAddress(
    v6="",  # No LTE
    v4="",  # No LTE
    vlan_id=454,
    routing_v4=RoutingInformation(gateway="10.44.64.1", ip_prefix_length=26),
    routing_v6=RoutingInformation(
        gateway="2A00:8A00:6000:607C::5501", ip_prefix_length=123
    ),
)
_cbts = ClassicalBts(
    cu=_cu_gnb_1, dus=[_du_1_gnb_1], global_bts_id=3914, instance_id=3914
)
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_SA_ASIL_ABIO_AEQN_AHLOA"
_amf_ssh = SshServiceDetails(
    addr="to_be_updated", username="to_be_updated", password="to_be_updated"
)
_amf_n2_addr = NetworkAddress(
    v4="10.94.232.6", v6="2a00:8a00:4000:65ef:ffff:ffff:ffff:b804", vlan_id=None
)
_amf = AMF(oam_ssh_connection_details=_amf_ssh, n2=_amf_n2_addr)
_core = RealCore(five_g=RealCore5GDetails(amf=_amf, tac=7150), mcc=310, mnc=260)
# temp _cu_gnb_1.m
_cu_gnb_1.m = (
    NetworkAddress(
        v4="10.44.90.161",
        v6="2a00:8a00:6000:607c::1:be20",
        vlan_id=488,
        routing_v4=RoutingInformation(gateway="10.44.90.129", ip_prefix_length=26),
        routing_v6=RoutingInformation(
            gateway="2A00:8A00:6000:607C::1:be01", ip_prefix_length=123
        ),
    ),
)
# temp _enb_1.m
_enb_1.m = NetworkAddress(
    v6="",  # No LTE
    v4="",  # No LTE
    vlan_id=454,
    routing_v4=RoutingInformation(gateway="10.44.64.1", ip_prefix_length=26),
    routing_v6=RoutingInformation(
        gateway="2A00:8A00:6000:607C::5501", ip_prefix_length=123
    ),
)
_lmp_vm_enb_1 = TestPc(
    default_ssh_connection_details=SshServiceDetails(addr="", username="", password=""),
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
