__maintainer__ = "5G SC CRT"
__team__ = "5G SC CRT"
__email__ = "nj-fz-crt@list.nokia.com"

import os
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
from taf.config.testline.pdu import PduPort, Pdu
from taf.config.testline import RealEnb
from taf.config.testline.core import EPCSim
from taf.config.testline.gnb.networkaddress import NetworkAddress, RoutingInformation
from taf.config.testline.pdu import PduPort, ATEN, FACOM, Pdu, EPC
import yaml


def _set_abstract_lib_config_env(ue_config_file):
    tl_config_dir = os.path.dirname(os.path.abspath(__file__))
    ue_config_abs_path = os.path.join(tl_config_dir, ue_config_file)

    with open(ue_config_abs_path) as ta_ue_config:
        ue_config = yaml.safe_load(ta_ue_config)

    os.environ["ABSTRACT_LIB_CONFIG"] = ue_config_abs_path

    return ue_config


ue_config = _set_abstract_lib_config_env("ue_config.yaml")

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.66.11.193", username="ute", password="Nokia666@ute!"
    )
)


_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="172.31.1.72",
        vlan_id=1,
        routing_v4=RoutingInformation(gateway="172.31.1.71", ip_prefix_length=24),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.66.36.34", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.66.36.34", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(v4="172.31.1.72", vlan_id=1),
    x2u=NetworkAddress(v4="172.31.1.72", vlan_id=1),
    s1c=NetworkAddress(v4="172.31.1.72", vlan_id=1),
    s1u=NetworkAddress(v4="172.31.1.72", vlan_id=1),
)

_du_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_du_capacity_unit = CapacityUnit(
    addr="192.168.253.22", hardware_type="ABIL", hardware_version="102"
)

_du_pdu = ATEN("1.1.1.1", [0])
_du_pdu_port = PduPort(_du_pdu, 0)

_du_common_unit = CommonUnit(
    lmp_connection=_du_lmp_connection,
    capacity_units=[_du_capacity_unit],
    hardware_type="ASIK",
    hardware_version="101",
    pdu_port=_du_pdu_port,
)

_ru0 = SC5GRadio(
    ru_hw_group="ASIR-HUB",
    sc_radio_connection_details=SCRadioConnectionDetails(
        ssh_connection_details=SshServiceDetails(
            addr="192.168.255.129",
            username="toor4nsn",
            password="oZPS0POrRieRtu",
            proxy=SshServiceDetails(
                addr="10.66.11.194", username="ute", password="Nokia666@ute!"
            ),
        ),
        telnet_connection_details=None,
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=None,
)

_ru1 = SC5GRadio(
    ru_hw_group="ASIR-HUB",
    sc_radio_connection_details=SCRadioConnectionDetails(
        ssh_connection_details=SshServiceDetails(
            addr="192.168.255.129",
            username="toor4nsn",
            password="oZPS0POrRieRtu",
            proxy=SshServiceDetails(
                addr="10.66.11.230", username="ute", password="Nokia666@ute!"
            ),
        ),
        telnet_connection_details=None,
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=None,
)

_ru2 = SC5GRadio(
    ru_hw_group="ASIR-HUB",
    sc_radio_connection_details=SCRadioConnectionDetails(
        ssh_connection_details=SshServiceDetails(
            addr="192.168.255.129",
            username="toor4nsn",
            password="oZPS0POrRieRtu",
            proxy=SshServiceDetails(
                addr="10.66.11.231", username="ute", password="Nokia666@ute!"
            ),
        ),
        telnet_connection_details=None,
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=None,
)

_airscale = Airscale(common_units=[_du_common_unit])

_du = DU(airscale=_airscale, rus=[_ru0, _ru1, _ru2])

_bts = ClassicalBts(cu=_cu, dus=[_du], instance_id=1, global_bts_id=1)

# lteenb = NetworkAddress(v4="172.31.1.71")
_lteenb = RealEnb(x2_link_addr=NetworkAddress(v4="172.31.1.70"))

# ABSTRACT_LIB_CONFIG = _set_abstract_lib_config_env("ue_config.yaml")

tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_bts],
    enbs=[_lteenb],
    ues=None,
    tl_cloud_topology="CLOUD_5G_CLASSICAL_ASIR_ASIK101L_ABIL102B1",
)
tl.ue_config = ue_config

__all__ = ["tl"]
