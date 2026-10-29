__maintainer__ = "ying.yao"
__team__ = "Nanjing ET"
__email__ = "I_NJ_SC_SYSTEM_VERF@internal.nsn.com"

from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc, Connection
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    SCRadioConnectionDetails,
    TelnetConnectionDetails,
)
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline import SC5GRadio
from taf.config.testline.core import EPCSim
from taf.config.testline import RealEnb
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit

from taf.config.testline.gnb.networkaddress import NetworkAddress, RoutingInformation
from taf.config.testline.pdu import FPFH, PduPort, HBTE
import os
import yaml

_cu = CU(
    backhaul_site_oam_ip="172.31.1.25",
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.255.129", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(v4="172.17.31.25", vlan_id=3731),
    x2u=NetworkAddress(v4="172.17.31.25", vlan_id=3731),
    s1c=NetworkAddress(v4="172.17.31.25", vlan_id=3731),
    s1u=NetworkAddress(v4="172.17.31.25", vlan_id=3731),
)

_du_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_du_capacity_unit = CapacityUnit(
    addr="fsp1_c", hardware_type="ABIL", hardware_version="A102"
)

_du_common_unit = CommonUnit(
    lmp_connection=_du_lmp_connection,
    capacity_units=[_du_capacity_unit],
    hardware_type="ASIB",
    hardware_version="A101",
    pdu_port=PduPort(
        pdu=HBTE(addr="10.66.47.21", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8]), port_no=7
    ),
)

_ru_1 = SC5GRadio(
    ru_hw_group="ASIR-HUB",
    sc_radio_connection_details=SCRadioConnectionDetails(
        ssh_connection_details=SshServiceDetails(
            addr="192.168.255.129",
            username="toor4nsn",
            password="oZPS0POrRieRtu",
            proxy=SshServiceDetails(addr="10.66.15.52", username="ute", password="ute"),
        ),
        telnet_connection_details=TelnetConnectionDetails(
            addr="tty-server", username="toor4nsn", password="oZPS0POrRieRtu"
        ),
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=PduPort(
        pdu=HBTE(addr="", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8]), port_no=1
    ),
    radio_type="ASIR-HUB",
)

_airscale = Airscale(common_units=[_du_common_unit])

_du = DU(airscale=_airscale, rus=[_ru_1])

_bts = ClassicalBts(cu=_cu, dus=[_du], instance_id=360, global_bts_id=360)


""" UE Configuration
In order to import UE configuration into the runtime environment of the robot framework,
the variable `ue_config` MUST NOT start with an underscore.
"""
# ue_config = _set_abstract_lib_config_env("ue_config.yml")
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.66.15.218", username="ute", password="uteUTE!"
    ),
    connections=[
        NetworkAddress(v4="192.168.255.126"),
        Connection(
            interface="eth1",
            interface_type="lmp",
            device=_bts.dus[0].airscale.common_units[0],
        ),
    ],
)

tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_bts],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_ASIBR_ABIOB4_APHG_AWHHIQB",
)

__all__ = ["tl"]
