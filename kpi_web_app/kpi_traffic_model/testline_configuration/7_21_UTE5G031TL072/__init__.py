__maintainer__ = "NSB 5G SC SYSTEM"
__team__ = "NSB 5G SC SYSTEM"
__email__ = "nj-nm-systemteam@LIST.NOKIA.COM"

import os
import yaml

from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    SCRadioConnectionDetails,
)
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline import SC5GRadio
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline import RealEnb
from taf.config.testline.core import EPCSim
from taf.config.testline.gnb.networkaddress import NetworkAddress, RoutingInformation

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.66.29.13", username="ute", password="ute"
    )
)
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="172.30.1.12",
        vlan_id=119,
        routing=RoutingInformation(gateway="172.30.1.10", ip_prefix_length=24),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.255.129", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(v4="172.30.1.12", vlan_id=119),
    x2u=NetworkAddress(v4="172.30.1.12", vlan_id=119),
    s1c=NetworkAddress(v4="172.30.1.12", vlan_id=119),
    s1u=NetworkAddress(v4="172.30.1.12", vlan_id=119),
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
                addr="10.66.29.183", username="ute", password="Nokia666@ute!"
            ),
        ),
        telnet_connection_details=None,
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
                addr="10.66.29.184", username="ute", password="Nokia666@ute!"
            ),
        ),
        telnet_connection_details=None,
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=None,
)

_airscale = Airscale(common_units=[_common_unit])

_du = DU(airscale=_airscale, rus=[_ru, _ru_2])

_instance_id = 1
cbts = ClassicalBts(cu=_cu, dus=[_du], instance_id=_instance_id, global_bts_id=1)

_epcsim = EPCSim(
    mme_ip="172.30.1.10",
    edaemon_port=10000,
    egate_port=20000,
    mcc=460,
    mnc=6,
    tac=663,
    default_ssh_connection_details=SshServiceDetails(
        addr="10.66.29.13",
        username="ute",
        password="Nokia666@ute!",
    ),
    dir_path="/opt/core",
    cfg_filename="sim_ipv4.cfg",
)

_lteenb = RealEnb(x2_link_addr=NetworkAddress(v4="172.30.1.11"))


def _set_abstract_lib_config_env(ue_config_file):
    ue_config_abs_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), ue_config_file
    )
    with open(ue_config_abs_path) as ta_ue_config:
        ue_config = yaml.safe_load(ta_ue_config)

    os.environ["ABSTRACT_LIB_CONFIG"] = ue_config_abs_path

    return ue_config


ue_config = _set_abstract_lib_config_env("ue_config.yaml")
ant_number = 2
epcsim_config = [
    {
        "key": "PGW_ADDR",
        "value": "27.168.1.200",
    },
    {
        "key": "SEC_KEY",
        "value": "11111111111111111111111111111111",
    },
    {
        "key": "OPC_KEY",
        "value": "11111111111111111111111111111111",
    },
    # Support up to 10 UEs. from IMSI_1 ~ IMSI_10, UE_IP_1 ~ UE_IP_10
    {
        "key": "IMSI_1",
        "value": "460:06:4100000025",
    },
    {
        "key": "UE_IP_1",
        "value": "27.168.1.10",
    },
]

tl = TestLine(
    test_pc=_test_pc,
    gnbs=[cbts],
    enbs=[_lteenb],
    ues=None,
    core=_epcsim,
    tl_cloud_topology="CLOUD_5G_CLASSICAL_ASIR_ASIKL_ABILB1_2xAWHQC",
)
tl.ue_config = ue_config
tl.ant_number = ant_number
tl.epcsim_config = epcsim_config

__all__ = ["tl"]
