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
from taf.config.testline import SC5GRadio, SC4GRadio
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline import RealEnb
from taf.config.testline.gnb.networkaddress import NetworkAddress, RoutingInformation

###########################################
# Test PC - server running the Robot tests
###########################################
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.66.41.18", username="ute", password="uteUTE!"
    )
)

###################
# gNB definition
###################

_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.66.30.149",
        vlan_id=30,
        routing=RoutingInformation(gateway="10.66.30.0", ip_prefix_length=24),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.66.30.149", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.66.30.149", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(v4="10.66.23.95", vlan_id=23),
    x2u=NetworkAddress(v4="10.66.23.95", vlan_id=23),
    s1c=NetworkAddress(v4="172.16.230.95", vlan_id=230),
    s1u=NetworkAddress(v4="172.16.230.95", vlan_id=230),
)

_capacity_unit = CapacityUnit(
    addr="fsp1_c", hardware_type="ASOE", hardware_version="102"
)

_common_unit = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129",
        username="toor4nsn",
        password="oZPS0POrRieRtu",
        proxy=SshServiceDetails(addr="10.66.41.18", username="ute", password="uteUTE!"),
    ),
    capacity_units=[_capacity_unit],
    hardware_type="ASOE",
    hardware_version="102",
)

_ru_1 = SC5GRadio(
    ru_hw_group="ASIR-HUB",
    sc_radio_connection_details=SCRadioConnectionDetails(
        ssh_connection_details=SshServiceDetails(
            addr="192.168.255.129",
            username="toor4nsn",
            password="oZPS0POrRieRtu",
            proxy=SshServiceDetails(
                addr="10.66.41.164", username="ute", password="Nokia666@ute!"
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
    serial_number="NH211600064",
)

_ru_2 = SC5GRadio(
    ru_hw_group="ASIR-HUB",
    sc_radio_connection_details=SCRadioConnectionDetails(
        ssh_connection_details=SshServiceDetails(
            addr="192.168.255.129",
            username="toor4nsn",
            password="oZPS0POrRieRtu",
            proxy=SshServiceDetails(addr="10.66.41.20", username="ute", password="ute"),
        ),
        telnet_connection_details=TelnetConnectionDetails(
            addr="tty-server", username="toor4nsn", password="oZPS0POrRieRtu"
        ),
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=None,
    serial_number="NH211300666",
)

_ru_3 = SC5GRadio(
    ru_hw_group="ASIR-HUB",
    sc_radio_connection_details=SCRadioConnectionDetails(
        ssh_connection_details=SshServiceDetails(
            addr="192.168.255.129",
            username="toor4nsn",
            password="oZPS0POrRieRtu",
            proxy=SshServiceDetails(addr="10.66.41.21", username="ute", password="ute"),
        ),
        telnet_connection_details=TelnetConnectionDetails(
            addr="tty-server", username="toor4nsn", password="oZPS0POrRieRtu"
        ),
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=None,
    serial_number="NH182801388",
)

_airscale = Airscale(common_units=[_common_unit])
_du = DU(airscale=_airscale, rus=[_ru_1, _ru_2, _ru_3])
_cbts = ClassicalBts(
    cu=_cu,
    dus=[_du],
    instance_id=51375,
    global_bts_id=51375,
)


def _set_abstract_lib_config_env(ue_config_file):
    ue_config_abs_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), ue_config_file
    )
    with open(ue_config_abs_path) as ta_ue_config:
        ue_config = yaml.safe_load(ta_ue_config)

    os.environ["ABSTRACT_LIB_CONFIG"] = ue_config_abs_path

    return ue_config


ue_config = _set_abstract_lib_config_env("ue_config.yaml")

####################################################################################################
# Example of testline definition consists of both 5G and 4G.
# Add other definitions, such as "ues", "core", etc. according to actual test line configurations.
####################################################################################################
tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_SA_ASOE_2xAPHG_APHA_AWHGEQH_2xAWHQJ_2xAWHENHD_TDD",
)
tl.ue_config = ue_config

__all__ = ["tl"]
