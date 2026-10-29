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
from taf.config.testline import SC5GRadio, SC4GRadio, RU
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline import RealEnb
from taf.config.testline.core import EPCSim
from taf.config.testline.gnb.networkaddress import NetworkAddress, RoutingInformation

###########################################
# Test PC - server running the Robot tests
###########################################
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.66.31.158", username="ute", password="uteUTE!"    # Login information for the VM where the test cases will be run
    )
)

###################
# gNB definition
###################

_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.66.31.158",
        vlan_id=30,
        routing=RoutingInformation(gateway="10.66.31.0", ip_prefix_length=24),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.255.129", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(v4="172.30.1.11", vlan_id=23),
    x2u=NetworkAddress(v4="172.30.1.11", vlan_id=230),
    s1c=NetworkAddress(v4="172.30.1.12", vlan_id=23),
    s1u=NetworkAddress(v4="172.30.1.12", vlan_id=230),
)

_capacity_unit0 = CapacityUnit(
    addr="192.168.253.20", hardware_type="ABIP", hardware_version="102"
)

_capacity_unit1 = CapacityUnit(
    addr="192.168.253.24", hardware_type="ABIP", hardware_version="101"
)

_capacity_unit2 = CapacityUnit(
    addr="192.168.253.28", hardware_type="ABIO", hardware_version="103"
)

_common_unit = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129",
        username="toor4nsn",
        password="oZPS0POrRieRtu",
        proxy=SshServiceDetails(
            addr="10.66.31.158", username="ute", password="uteUTE!"    # Login information for the VM connected to gNB
        ),
    ),
    capacity_units=[_capacity_unit0, _capacity_unit1, _capacity_unit2],
    hardware_type="ASIL",
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
                addr="10.66.31.160", username="ute", password="uteUTE!"    # Login information for the VM connected to 5G sHUB
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

_ru_2 = SC5GRadio(
    ru_hw_group="ASIR-HUB",
    sc_radio_connection_details=SCRadioConnectionDetails(
        ssh_connection_details=SshServiceDetails(
            addr="192.168.255.129",
            username="toor4nsn",
            password="oZPS0POrRieRtu",
            proxy=SshServiceDetails(
                addr="10.66.31.161", username="ute", password="uteUTE!"    # Login information for the VM connected to 5G sHUB
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

_ru_3 = SC5GRadio(
    ru_hw_group="ASIR-HUB",
    sc_radio_connection_details=SCRadioConnectionDetails(
        ssh_connection_details=SshServiceDetails(
            addr="192.168.255.129",
            username="toor4nsn",
            password="oZPS0POrRieRtu",
            proxy=SshServiceDetails(
                addr="10.66.31.159", username="ute", password="uteUTE!"    # Login information for the VM connected to 5G sHUB
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

_ru_4 = RU(
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.1.34", username="root", password="I9LzXPHVEqLorL/x0tAG5ztQ/Y8vVmhmlN9LSkVW4CQ="
    ),
    ru_hw_group="GEN4-RRH",
    radio_type="AWHQX",
)

_airscale = Airscale(common_units=[_common_unit])
_du = DU(airscale=_airscale, rus=[_ru_1, _ru_2, _ru_3, _ru_4])
_cbts = ClassicalBts(
    cu=_cu,
    dus=[_du],
    instance_id=37140,            # ID of MRBTS object
    global_bts_id=39107           # ID of LNBTS object
)
###################
# eNB definition
###################

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
    tl_cloud_topology="CLOUD_5G_CLASSICAL_ASIR_ASILL_ABIPB1B2_ABIOB3_3xAPHG_1xAWHQX_4xAWHGEQH_2xAWHHC_2xAWHHIQB_CPRI_eCPRI_SA",
)

tl.ue_config = ue_config

__all__ = ["tl"]
