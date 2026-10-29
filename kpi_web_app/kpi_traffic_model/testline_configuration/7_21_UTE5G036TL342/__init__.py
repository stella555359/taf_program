__maintainer__ = "5G SC CRT"
__team__ = "5G SC CRT"
__email__ = "nj-fz-crt@list.nokia.com"

import os
import yaml

from taf.config.testline.cloud_hosting import (
    ControlNode,
    NCIR,
    CloudDeployment,
    DeploymentFlavorStack,
    DeploymentNetworkStack,
    DeploymentVnfStack,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU, DU, ClassicalBts
from taf.config.testline import SC4GRadio, SC5GRadio
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline import RealEnb
from taf.config.testline.core import EPCSim
from taf.config.testline.gnb.networkaddress import NetworkAddress, RoutingInformation
from taf.config.testline import RU, DU
from taf.config.testline.pdu import HBTE

from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    SCRadioConnectionDetails,
    TelnetConnectionDetails,
)

###########################################
# Test PC - server running the Robot tests
###########################################
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.66.24.233",
        username="ute",
        password="uteUTE!"
        # Login information for the VM where the test cases will be run
    )
)


###################
# gNB definition
###################

_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="172.30.1.10",  # <----
        vlan_id=815,
        routing=RoutingInformation(gateway="10.66.30.1", ip_prefix_length=24),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="172.30.1.10", username="toor4nsn", password="oZPS0POrRieRtu"  # <----
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="172.30.1.10", username="Nemuadmin", password="nemuuser"  # <----
    ),
    x2c=NetworkAddress(v4="172.30.1.11", vlan_id=815),  # <----
    x2u=NetworkAddress(v4="172.30.1.11", vlan_id=815),  # <----
    s1c=NetworkAddress(v4="172.30.1.11", vlan_id=815),  # <----
    s1u=NetworkAddress(v4="172.30.1.11", vlan_id=815),  # <----
)

_capacity_unit = CapacityUnit(
    addr="fsp1_c", hardware_type="ABIO", hardware_version="103"
)

_common_unit = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129",  # <----
        username="toor4nsn",
        password="oZPS0POrRieRtu",
        # proxy=SshServiceDetails(
        #    addr="10.66.24.233",
        #    username="ute",
        #    password="uteUTE!",  # Login information for the VM connected to gNB  #<----
        # ),
    ),
    capacity_units=[_capacity_unit],
    hardware_type="ASIB",
    hardware_version="102",
)

_ru = SC5GRadio(
    ru_hw_group="ASIR-HUB",
    sc_radio_connection_details=SCRadioConnectionDetails(
        ssh_connection_details=SshServiceDetails(
            addr="10.66.24.235",  # <----
            username="toor4nsn",
            password="oZPS0POrRieRtu",
            proxy=SshServiceDetails(
                addr="10.66.24.235",
                username="ute",
                password="uteUTE!",  # Login information for the VM connected to 5G sHUB   #<----
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
_cbts = ClassicalBts(
    cu=_cu,
    dus=[_du],
    instance_id=36951,  # ID of MRBTS object   #<----
    global_bts_id=36951,  # ID of NRBTS object   #<----
)


###################
# eNB definition
###################
_capacity_units_enb = [CapacityUnit(addr="192.168.253.20", hardware_type="ABIP")]

_common_unit_enb = CommonUnit(
    hardware_type="ASIL",
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129",
        username="toor4nsn",
        password="oZPS0POrRieRtu",
        proxy=SshServiceDetails(
            addr="10.66.24.233",
            username="ute",
            password="uteUTE!",  # Login information for the VM connected to eNB
        ),
    ),
    capacity_units=_capacity_units_enb,
)

_radio1_modules_enb = SC4GRadio(
    sc_radio_connection_details=SCRadioConnectionDetails(
        ssh_connection_details=SshServiceDetails(
            addr="192.168.255.129",
            username="toor4nsn",
            password="oZPS0POrRieRtu",
            proxy=SshServiceDetails(
                addr="10.66.24.235",
                username="ute",
                password="uteUTE!",  # Login information for the VM connected to 4G sHUB
            ),
        ),
        telnet_connection_details=TelnetConnectionDetails(
            addr="tty-server", username="toor4nsn", password="oZPS0POrRieRtu"
        ),
    ),
)

_radio2_modules_enb = SC4GRadio(
    sc_radio_connection_details=SCRadioConnectionDetails(
        ssh_connection_details=SshServiceDetails(
            addr="192.168.255.129",
            username="toor4nsn",
            password="oZPS0POrRieRtu",
            proxy=SshServiceDetails(
                addr="10.66.24.236",
                username="ute",
                password="uteUTE!",  # Login information for the VM connected to 4G sHUB
            ),
        ),
        telnet_connection_details=TelnetConnectionDetails(
            addr="tty-server", username="toor4nsn", password="oZPS0POrRieRtu"
        ),
    ),
)

_radio3_modules_enb = SC4GRadio(
    sc_radio_connection_details=SCRadioConnectionDetails(
        ssh_connection_details=SshServiceDetails(
            addr="192.168.255.129",
            username="toor4nsn",
            password="oZPS0POrRieRtu",
            proxy=SshServiceDetails(
                addr="10.66.24.221",
                username="ute",
                password="uteUTE!",  # Login information for the VM connected to 4G sHUB
            ),
        ),
        telnet_connection_details=TelnetConnectionDetails(
            addr="tty-server", username="toor4nsn", password="oZPS0POrRieRtu"
        ),
    ),
)

_radio4_modules_enb = SC4GRadio(
    sc_radio_connection_details=SCRadioConnectionDetails(
        ssh_connection_details=SshServiceDetails(
            addr="192.168.255.129",
            username="toor4nsn",
            password="oZPS0POrRieRtu",
            proxy=SshServiceDetails(
                addr="10.66.24.222",
                username="ute",
                password="uteUTE!",  # Login information for the VM connected to 4G sHUB
            ),
        ),
        telnet_connection_details=TelnetConnectionDetails(
            addr="tty-server", username="toor4nsn", password="oZPS0POrRieRtu"
        ),
    ),
)

_radio5_modules_enb = SC4GRadio(
    sc_radio_connection_details=SCRadioConnectionDetails(
        ssh_connection_details=SshServiceDetails(
            addr="192.168.255.129",
            username="toor4nsn",
            password="oZPS0POrRieRtu",
            proxy=SshServiceDetails(
                addr="10.66.24.223",
                username="ute",
                password="uteUTE!",  # Login information for the VM connected to 4G sHUB
            ),
        ),
        telnet_connection_details=TelnetConnectionDetails(
            addr="tty-server", username="toor4nsn", password="oZPS0POrRieRtu"
        ),
    ),
)

_radio6_modules_enb = SC4GRadio(
    sc_radio_connection_details=SCRadioConnectionDetails(
        ssh_connection_details=SshServiceDetails(
            addr="192.168.255.129",
            username="toor4nsn",
            password="oZPS0POrRieRtu",
            proxy=SshServiceDetails(
                addr="10.66.24.224",
                username="ute",
                password="uteUTE!",  # Login information for the VM connected to 4G sHUB
            ),
        ),
        telnet_connection_details=TelnetConnectionDetails(
            addr="tty-server", username="toor4nsn", password="oZPS0POrRieRtu"
        ),
    ),
)
_airscale_enb = Airscale(common_units=[_common_unit_enb])

_lteenb = RealEnb(
    system_module=_airscale_enb,
    rms=[
        _radio1_modules_enb,
        _radio2_modules_enb,
        _radio3_modules_enb,
        _radio4_modules_enb,
        _radio5_modules_enb,
        _radio6_modules_enb,
    ],
    instance_id=36951,  # ID of MRBTS object
    global_bts_id=36951,  # ID of LNBTS object
    oam_ip=NetworkAddress(v4="172.30.1.10"),
    x2_link_addr=NetworkAddress(v4="172.30.1.10"),
)

_epcsim = EPCSim(
    mme_ip="172.30.1.1",
    edaemon_port=10000,
    egate_port=20000,
    mcc=460,
    mnc=2,
    tac=2,
    default_ssh_connection_details=SshServiceDetails(
        addr="10.66.24.233",
        username="ute",
        password="uteUTE!",
    ),
    dir_path="/opt/core",
    cfg_filename="epcsim.cfg",
)

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
        "value": "460:02:3100007448",
    },
    {
        "key": "UE_IP_1",
        "value": "27.168.1.10",
    },
    {
        "key": "IMSI_2",
        "value": "460:02:3100010831",
    },
    {
        "key": "UE_IP_2",
        "value": "27.168.1.20",
    },
]


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
    enbs=[_lteenb],
    gnbs=[_cbts],
    core=_epcsim,
    tl_cloud_topology="CLOUD_5G_CLASSICAL_ASILL_ABIPB1_6xAPHG_6xAWHHIQB_2xAWHGEQK_3xAHGEHA_1xAHENB",
)

tl.ue_config = ue_config
tl.epcsim_config = epcsim_config

__all__ = ["tl"]
