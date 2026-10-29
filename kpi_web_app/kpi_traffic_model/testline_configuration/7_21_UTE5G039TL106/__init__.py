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
from taf.config.testline.core import EPCSim
from taf.config.testline.gnb.networkaddress import NetworkAddress, RoutingInformation

###########################################
# Test PC - server running the Robot tests
###########################################
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.66.31.154", username="ute", password="ute"    # Login information for the VM where the test cases will be run
    )
)

###################
# gNB definition
###################

_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.66.31.154",
        vlan_id=30,
        routing=RoutingInformation(gateway="10.66.24.0", ip_prefix_length=24),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.255.129", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(v4="172.30.1.11", vlan_id=23),
    x2u=NetworkAddress(v4="172.30.1.11", vlan_id=230),
    s1c=NetworkAddress(v4="172.30.1.11", vlan_id=23),
    s1u=NetworkAddress(v4="172.30.1.11", vlan_id=230),
)

_capacity_unit = CapacityUnit(
    addr="fsp1_c", hardware_type="ABIL", hardware_version="102"
)

_common_unit = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129",
        username="toor4nsn",
        password="oZPS0POrRieRtu",
        proxy=SshServiceDetails(
            addr="10.66.31.154", username="ute", password="ute"    # Login information for the VM connected to gNB
        ),
    ),
    capacity_units=[_capacity_unit],
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
                addr="10.66.31.156", username="ute", password="ute"    # Login information for the VM connected to 5G sHUB
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
                addr="10.66.24.50", username="ute", password="ute"    # Login information for the VM connected to 5G sHUB
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
_du = DU(airscale=_airscale, rus=[_ru_1, _ru_2])
_cbts = ClassicalBts(
    cu=_cu,
    dus=[_du],
    instance_id=39106,            # ID of MRBTS object
    global_bts_id=39106           # ID of NRBTS object
)


_epcsim = EPCSim(
    mme_ip="172.30.1.1",
    edaemon_port=10000,
    egate_port=20000,
    mcc=460,
    mnc=2,
    tac=1,
    default_ssh_connection_details=SshServiceDetails(
        addr="10.66.31.154",
        username="ute",
        password="uteUTE!",
    ),
    dir_path="/opt/iphy/WTS_3316040.4_4.0.17791/WTS_3316040.4_4.0.17791_SANDYBRIDGE",
    cfg_filename="sim_ipv4.cfg",
)

###################
# eNB definition
###################
_capacity_units_enb = [CapacityUnit(addr="192.168.253.20", hardware_type="ABIO")]

_common_unit_enb = CommonUnit(
    hardware_type="ASIB",
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129",
        username="toor4nsn",
        password="oZPS0POrRieRtu",
        proxy=SshServiceDetails(
            addr="10.66.31.154", username="ute", password="ute"    # Login information for the VM connected to eNB
        ),
    ),
    capacity_units=_capacity_units_enb,
)

_radio_modules_enb = SC4GRadio(
    sc_radio_connection_details=SCRadioConnectionDetails(
        ssh_connection_details=SshServiceDetails(
            addr="192.168.255.129",
            username="toor4nsn",
            password="oZPS0POrRieRtu",
            proxy=SshServiceDetails(
                addr="10.66.31.154", username="ute", password="ute"    # Login information for the VM connected to 4G sHUB
            ),
        ),
        telnet_connection_details=TelnetConnectionDetails(
            addr="tty-server", username="toor4nsn", password="oZPS0POrRieRtu"
        ),
    ),
)
_airscale_enb = Airscale(common_units=[_common_unit_enb])

_lteenb = RealEnb(
    x2_link_addr=NetworkAddress(v4="10.66.30.201"),
    system_module=_airscale_enb,
    rms=[_radio_modules_enb],
    instance_id=391061,                             # ID of MRBTS object
    global_bts_id=391061,                           # ID of LNBTS object
    oam_ip=NetworkAddress(v4="10.66.30.201"),
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
epcsim_config = [
    {
        "key": "PGW_ADDR",
        "value": "27.168.1.200",
    },
    {
        "key": "SEC_KEY",
        "value": "00112233445566778899AABBCCDDEEFF",
    },
    {
        "key": "OPC_KEY",
        "value": "0ED47545168EAFE2C39C075829A7B61F",
    },
    # Support up to 10 UEs. from IMSI_1 ~ IMSI_10, UE_IP_1 ~ UE_IP_10
    {
        "key": "IMSI_1",
        "value": "262:03:0000000021",
    },
    {
        "key": "UE_IP_1",
        "value": "27.168.1.10",
    },
]


####################################################################################################
# Example of testline definition consists of both 5G and 4G.
# Add other definitions, such as "ues", "core", etc. according to actual test line configurations.
####################################################################################################
tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    enbs=[_lteenb],
    core=_epcsim,
    tl_cloud_topology="CLOUD_5G_CLASSICAL_NSA_NR_ASIBR_ABIOB4_ABIOB5_ABINB6_6xAPHG_4xAWHGEQK_4xAWHENHD_3xAWHHC_FDD",
)

tl.ue_config = ue_config

__all__ = ["tl"]
