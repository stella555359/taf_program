__maintainer__ = "5G SC CRT"
__team__ = "5G SC CRT"
__email__ = "nj-fz-crt@list.nokia.com"

import os
import yaml

from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    SCRadioConnectionDetails,
    TelnetConnectionDetails,
)
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline import SC5GRadio
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline import RealEnb
from taf.config.testline.core import EPCSim
from taf.config.testline.gnb.networkaddress import NetworkAddress, RoutingInformation
from taf.config.testline.pdu import PduPort, ATEN


_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.66.11.190", username="ute", password="ute"
    )
)
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="172.31.1.65",
        vlan_id=33,
        routing=RoutingInformation(gateway="172.31.1.64", ip_prefix_length=24),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.255.129", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(v4="172.31.1.65", vlan_id=33),
    x2u=NetworkAddress(v4="172.31.1.65", vlan_id=33),
    s1c=NetworkAddress(v4="172.31.1.65", vlan_id=33),
    s1u=NetworkAddress(v4="172.31.1.65", vlan_id=33),
)

_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(
    addr="fsp1_c", hardware_type="ABIL", hardware_version="102"
)

_common_unit = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    hardware_type="ASIK",
    hardware_version="101",
)

_ru = SC5GRadio(
    ru_hw_group="ASIR-HUB",
    sc_radio_connection_details=SCRadioConnectionDetails(
        ssh_connection_details=SshServiceDetails(
            addr="192.168.255.129",
            username="toor4nsn",
            password="oZPS0POrRieRtu",
            proxy=SshServiceDetails(
                addr="10.66.11.191", username="ute", password="ute"
            ),
        ),
        telnet_connection_details=TelnetConnectionDetails(
            addr="tty-server", username="toor4nsn", password="oZPS0POrRieRtu"
        ),
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=None,
)

_airscale = Airscale(common_units=[_common_unit])

_du = DU(airscale=_airscale, rus=[_ru])

_cbts = ClassicalBts(cu=_cu, dus=[_du], instance_id=1, global_bts_id=1)

_lteenb = RealEnb(x2_link_addr=NetworkAddress(v4="172.31.1.63"))

tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    enbs=[_lteenb],
    ues=None,
    core=None,
    tl_cloud_topology="CLOUD_5G_CLASSICAL_ASIR_ASIKL_ABILB1_AWHQJ_COAM",
)

__all__ = ["tl"]
