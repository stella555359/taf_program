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
from taf.config.testline.pdu import ATEN, Gude, APC
from taf.config.testline.radio import RU
from taf.config.testline.core import RealCore, RealCore5GDetails, AMF

__all__ = ["tl"]
_lmp_vm_gnb_1 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.43.82.74", username="ute", password="ute"
    )
)
cfg_dir = os.path.dirname(os.path.abspath(__file__))
_cu_gnb_1 = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.63.86.205",
        v6="2a00:8a00:a000:11b0::3bcd",
        vlan_id=237,
        routing_v4=RoutingInformation(gateway="10.63.86.65", ip_prefix_length=26),
        routing_v6=RoutingInformation(
            gateway="2a00:8a00:a000:11b0::3bcd", ip_prefix_length=120
        ),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.255.129", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.63.87.173",
        v6="2A00:8A00:6000:607C::5B0C2a00:8a00:a000:11b0::3cad",
        vlan_id=244,
        routing_v4=RoutingInformation(gateway="10.63.87.193", ip_prefix_length=27),
        routing_v6=RoutingInformation(
            gateway="2a00:8a00:a000:11b0::3ca1", ip_prefix_length=120
        ),
    ),
    x2u=NetworkAddress(
        v4="10.63.87.141",
        v6="2a00:8a00:a000:11b0::3c8d",
        vlan_id=243,
        routing_v4=RoutingInformation(gateway="10.63.87.161", ip_prefix_length=27),
        routing_v6=RoutingInformation(
            gateway="2a00:8a00:a000:11b0::3c81", ip_prefix_length=120
        ),
    ),
    s1u=NetworkAddress(
        v4="10.63.87.109",
        v6="2a00:8a00:a000:11b0::3c6d",
        vlan_id=242,
        routing_v4=RoutingInformation(gateway="10.63.87.129", ip_prefix_length=27),
        routing_v6=RoutingInformation(
            gateway="2a00:8a00:a000:11b0::3c61", ip_prefix_length=120
        ),
    ),
    ngu=NetworkAddress(
        v6="2a00:8a00:a000:11b0::3ccd",
        v4="10.63.87.205",
        vlan_id=245,
        routing_v4=RoutingInformation(gateway="10.63.87.193", ip_prefix_length=27),
        routing_v6=RoutingInformation(
            gateway="2a00:8a00:a000:11b0::3cc1", ip_prefix_length=120
        ),
    ),
    ngc=NetworkAddress(
        v6="2a00:8a00:a000:11b0::3ced",
        v4="10.63.87.237",
        vlan_id=246,
        routing_v4=RoutingInformation(gateway="10.63.87.225", ip_prefix_length=27),
        routing_v6=RoutingInformation(
            gateway="2a00:8a00:a000:11b0::3ce1", ip_prefix_length=120
        ),
    ),
    xnc=NetworkAddress(
        v4="10.43.82.237",
        v6="2a00:8a00:a000:11b0::3ded",
        vlan_id=248,
        routing_v4=RoutingInformation(gateway="10.43.82.225", ip_prefix_length=27),
        routing_v6=RoutingInformation(
            gateway="2a00:8a00:a000:11b0::3de1", ip_prefix_length=120
        ),
    ),
    xnu=NetworkAddress(
        v4="10.43.82.205",
        v6="2a00:8a00:a000:11b0::3dcd",
        vlan_id=247,
        routing_v4=RoutingInformation(gateway="10.43.82.193", ip_prefix_length=27),
        routing_v6=RoutingInformation(
            gateway="2a00:8a00:a000:11b0::3dc1", ip_prefix_length=120
        ),
    ),
)
_pdu_gnb = ATEN(addr="10.43.82.120", port_numbers=[5])
_pdu_gnb_ru = ATEN(addr="10.43.82.120", port_numbers=[5])
_gnb_ru = RU(
    ru_hw_group="AHLOA",
    radio_type="AHLOA",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="root", password="umniedziala"
    ),
    pdu_port=_pdu_gnb_ru.pdu_ports[5],
)
_abil1_gnb_1_master = CapacityUnit(addr="192.168.253.20")
_abil1_gnb_1_slave = CapacityUnit(addr="192.168.253.21")
_abil1_gnb_1_loner = CapacityUnit(addr="192.168.253.22")
_asik_gnb_1 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_abil1_gnb_1_master, _abil1_gnb_1_loner, _abil1_gnb_1_slave],
    pdu_port=_pdu_gnb.pdu_ports[5],
)
_airscale_gnb_1 = Airscale(common_units=[_asik_gnb_1])
_ru_cablinks = [
    Cablink(
        source=Endpoint(unit=_abil1_gnb_1_master, label="QSFP", port_id=1),
        target=Endpoint(unit=_gnb_ru, label="SFP", port_id=2),
    ),
    Cablink(
        source=Endpoint(unit=_abil1_gnb_1_master, label="SFP", port_id=1),
        target=Endpoint(unit=_gnb_ru, label="SFP", port_id=1),
    ),
]
_du_1_gnb_1 = DU(airscale=_airscale_gnb_1, rus=[_gnb_ru], cablinks=_ru_cablinks)
_pdu_enb = ATEN(addr="10.43.82.120", port_numbers=[5])
_asik_enb_1 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_abil1_gnb_1_master, _abil1_gnb_1_loner, _abil1_gnb_1_slave],
    pdu_port=_pdu_enb.pdu_ports[5],
)
_airscale_enb_1 = Airscale(common_units=[_asik_enb_1])
_enb_1 = RealEnb(
    airscale=_airscale_enb_1,
    global_bts_id=40209,
    instance_id=40209,
    x2_link_addr=NetworkAddress(
        v6="2A00:8A00:6000:607C::5A0D",
        v4="10.44.65.77",
        vlan_id=460,
        routing_v4=RoutingInformation(gateway="10.44.65.65", ip_prefix_length=27),
        routing_v6=RoutingInformation(
            gateway="2A00:8A00:6000:607C::5A01", ip_prefix_length=120
        ),
    ),
)
_enb_1.oam_ip = NetworkAddress(
    v6="2A00:8A00:6000:607C::5B0D",
    v4="10.44.65.141",
    vlan_id=459,
    routing_v4=RoutingInformation(gateway="10.44.65.129", ip_prefix_length=26),
    routing_v6=RoutingInformation(
        gateway="2A00:8A00:6000:607C::5B01", ip_prefix_length=120
    ),
)
_cbts = ClassicalBts(
    cu=_cu_gnb_1, dus=[_du_1_gnb_1], global_bts_id=50209, instance_id=50209
)
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ASIBL_ABILB1_AHLOA_ENB"
_amf_ssh = SshServiceDetails(
    addr="to_be_updated", username="to_be_updated", password="to_be_updated"
)
_amf_n2_addr = NetworkAddress(
    v4="10.94.232.6", v6="2a00:8a00:4000:65ef:ffff:ffff:ffff:b804", vlan_id=None
)
_amf = AMF(oam_ssh_connection_details=_amf_ssh, n2=_amf_n2_addr)
_core = RealCore(five_g=RealCore5GDetails(amf=_amf), mcc=540, mnc=1)
_lmp_vm_enb_1 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.42.195.202", username="ute", password="ute"
    ),
    connections=[_enb_1],
)
_pdu_ue_1 = ATEN(addr="10.43.82.120", port_numbers=[5])
_pdu_ue_2 = APC(addr="10.44.205.67", port_numbers=[2])
_pdu_ue_3 = APC(addr="10.44.205.67", port_numbers=[3])
_pdu_ue_4 = APC(addr="10.44.205.67", port_numbers=[4])
_pdu_ue_5 = APC(addr="10.44.205.67", port_numbers=[5])
_pdu_ue_6 = APC(addr="10.44.205.67", port_numbers=[6])
_pdu_enb_2 = ATEN(addr="10.44.206.176", port_numbers=[7])
_pdu_enb_3 = ATEN(addr="10.44.206.126", port_numbers=[2])
_pdu_enb_4 = ATEN(addr="10.44.206.126", port_numbers=[4])
_pdu_enb_5 = ATEN(addr="10.44.206.126", port_numbers=[7])
_pdu_enb_6 = ATEN(addr="10.44.206.126", port_numbers=[5])
with open(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "askey_ue.yml")
) as ue_config:
    import yaml

    _askey_ue = yaml.load(ue_config, yaml.SafeLoader)
tl = TestLine(
    test_pc=_lmp_vm_gnb_1,
    ues=[_askey_ue],
    pdus=[
        _pdu_ue_1,
    ],
    gnbs=[_cbts],
    core=_core,
    tl_cloud_topology=_tl_cloud_topology,
    test_pcs=[_lmp_vm_gnb_1, _lmp_vm_enb_1],
)
