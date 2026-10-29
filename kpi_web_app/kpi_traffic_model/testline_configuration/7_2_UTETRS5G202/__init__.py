__maintainer__ = "Prabakar Sanikommu"
__team__ = "TRSI&V"
__email__ = "prabakar.sanikommu@nokia.com"


import os
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
)
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline import RU
from taf.config.testline.enb import RealEnb
from taf.config.testline.core import RealCore, RealCore5GDetails, AMF
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.pdu import ATEN
from taf.config.testline.gnb.networkaddress import NetworkAddress, RoutingInformation
from taf.config.testline.gnb.du import Cablink, Endpoint

###############################################
# UTE BNG 5G Classical BTS TRS configuration #
###############################################

# General
cfg_dir = os.path.dirname(os.path.abspath(__file__))

# LMP virtual machine
_lmp_vm = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.43.82.76", username="ute", password="ute"
    )
)

# Power breakers
_pdu_du = ATEN(addr="10.43.82.120", port_numbers=[3, 7])
_pdu_ru = ATEN(addr="10.43.82.120", port_numbers=[3, 7])

# 5G Radio units
_ru_1 = RU(
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.148", username="root", password="root"
    ),
    ru_hw_group="NR_RADIO",
    radio_type="AHLOA",
    pdu_port=_pdu_ru.pdu_ports[7],
)

_radio_units_gnb = [_ru_1]

# 5G Cloud unit
_cloud_unit_gnb = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.63.86.209",
        v6="2a00:8a00:a000:11b0::3bd1",
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
        v4="10.63.87.177",
        v6="2a00:8a00:a000:11b0::3cb1",
        vlan_id=244,
        routing_v4=RoutingInformation(gateway="10.63.87.161", ip_prefix_length=27),
        routing_v6=RoutingInformation(
            gateway="2a00:8a00:a000:11b0::3ca1", ip_prefix_length=123
        ),
    ),
    x2u=NetworkAddress(
        v4="10.63.87.145",
        v6="2a00:8a00:a000:11b0::3c91",
        vlan_id=243,
        routing_v4=RoutingInformation(gateway="10.63.87.129", ip_prefix_length=27),
        routing_v6=RoutingInformation(
            gateway="2a00:8a00:a000:11b0::3c81", ip_prefix_length=123
        ),
    ),
    s1u=NetworkAddress(
        v4="10.63.87.113",
        v6="2a00:8a00:a000:11b0::3c71",
        vlan_id=242,
        routing_v4=RoutingInformation(gateway="10.63.87.97", ip_prefix_length=27),
        routing_v6=RoutingInformation(
            gateway="2a00:8a00:a000:11b0::3c61", ip_prefix_length=123
        ),
    ),
    ngu=NetworkAddress(
        v4="10.63.87.209",
        v6="2a00:8a00:a000:11b0::3cd1",
        vlan_id=245,
        routing_v4=RoutingInformation(gateway="10.63.87.193", ip_prefix_length=27),
        routing_v6=RoutingInformation(
            gateway="2a00:8a00:a000:11b0::3cc1", ip_prefix_length=123
        ),
    ),
    ngc=NetworkAddress(
        v4="10.63.87.241",
        v6="2a00:8a00:a000:11b0::3cf1",
        vlan_id=246,
        routing_v4=RoutingInformation(gateway="10.63.87.225", ip_prefix_length=27),
        routing_v6=RoutingInformation(
            gateway="2a00:8a00:a000:11b0::3ce1", ip_prefix_length=123
        ),
    ),
    xnc=NetworkAddress(
        v4="10.43.82.241",
        v6="2a00:8a00:a000:11b0::3df1",
        vlan_id=51,
        routing_v4=RoutingInformation(gateway="10.43.82.225", ip_prefix_length=27),
        routing_v6=RoutingInformation(
            gateway="2a00:8a00:a000:11b0::3de1", ip_prefix_length=123
        ),
    ),
    xnu=NetworkAddress(
        v4="10.43.82.209",
        v6="2a00:8a00:a000:11b0::3dd1",
        vlan_id=52,
        routing_v4=RoutingInformation(gateway="10.43.82.193", ip_prefix_length=27),
        routing_v6=RoutingInformation(
            gateway="2a00:8a00:a000:11b0::3dc1", ip_prefix_length=123
        ),
    ),
)

# 5G Distributed unit
"""
192.168.253.36 fsp-2-5a fsp1 fsp1_a
192.168.253.37 fsp-2-5b  fsp1_b
192.168.253.38 fsp-2-5c  fsp1_c
"""

_abil_master = CapacityUnit(addr="fsp-5a")
_abil_slave = CapacityUnit(addr="fsp-5b")
_abil_loner = CapacityUnit(addr="fsp-5c")

_capacity_units_gnb = [_abil_master, _abil_slave, _abil_loner]

_common_unit_gnb = CommonUnit(
    hardware_type="ASIB",
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=_capacity_units_gnb,
    pdu_port=_pdu_du.pdu_ports[7],
)

_airscale_gnb = Airscale(common_units=[_common_unit_gnb])

_ru_cablinks = [
    Cablink(
        source=Endpoint(unit=_abil_master, label="SFP", port_id=1),
        target=Endpoint(unit=_ru_1, label="SFP", port_id=1),
    )
]

_distributed_unit_gnb = DU(
    airscale=_airscale_gnb, rus=_radio_units_gnb, cablinks=_ru_cablinks
)

# 5G Classical BTS
_classical_bts_gnb = ClassicalBts(
    cu=_cloud_unit_gnb,
    dus=[_distributed_unit_gnb],
    instance_id=3915,
    global_bts_id=3915,
)

# 4G radio units
_radio_units_enb = [
    RU(ru_hw_group="LTE_RADIO", radio_type="FRIG", pdu_port=_pdu_ru.pdu_ports[7])
]

# 4G anchor BTS
_capacity_units_enb = [CapacityUnit(addr="192.168.253.20", hardware_type="ABIA")]

_common_unit_enb = CommonUnit(
    hardware_type="ASIA",
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=_capacity_units_enb,
    pdu_port=_pdu_du.pdu_ports[7],
)

_airscale_enb = Airscale(common_units=[_common_unit_enb])

_lte_enb = RealEnb(
    airscale=_airscale_enb,
    rms=_radio_units_enb,
    instance_id=3916,
    global_bts_id=3916,
    oam_ip=NetworkAddress(
        v4="10.63.86.210",
        v6="2a00:8a00:4000:11b0::3bd2",
        routing_v4=RoutingInformation(gateway="10.35.86.193", ip_prefix_length=26),
        routing_v6=RoutingInformation(
            gateway="2a00:8a00:a000:11b0::3bc1", ip_prefix_length=120
        ),
    ),
    x2_link_addr=NetworkAddress(
        v4="10.63.86.50",
        v6="2a00:8a00:a000:11b0::3b32",
        routing_v4=RoutingInformation(gateway="10.35.86.193", ip_prefix_length=26),
        routing_v6=RoutingInformation(
            gateway="2a00:8a00:a000:11bo::3b21", ip_prefix_length=120
        ),
    ),
)

# enb test VM
_test_pc_enb = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.43.82.70", username="ute", password="ute"
    ),
    connections=[_lte_enb],
)

# Core network
_amf_oam_ssh_connection_details = SshServiceDetails(
    addr=None, username=None, password=None
)
_n2_address = NetworkAddress(v4="10.103.226.38", v6="2a00:8a00:4000:4a22::8086")
_amf = AMF(oam_ssh_connection_details=_amf_oam_ssh_connection_details, n2=_n2_address)
_real_5g_core_details = RealCore5GDetails(amf=_amf, tac=8000)
_core = RealCore(mcc=244, mnc=9, five_g=_real_5g_core_details)

# Testline
tl = TestLine(
    test_pc=_lmp_vm,
    test_pcs=[_lmp_vm, _test_pc_enb],
    gnbs=[_classical_bts_gnb],
    core=_core,
    tl_cloud_topology="CLOUD_5G_CLASSICAL_ASIB_ABIL_AHLOA_ENB",
)

__all__ = ["tl"]
