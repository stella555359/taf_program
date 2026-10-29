__maintainer__ = "5G SC CIT"
__team__ = "5G CIT"
__email__ = "nj-fz-crt@list.nokia.com"

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

from taf.config.testline.enb import RealEnb
from taf.config.testline.core import EPCSim
from taf.config.testline.gnb.networkaddress import NetworkAddress
import os
import yaml

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.66.29.108", username="ute", password="Nokia666@ute!"
    )
)

_cu = CU(
    backhaul_site_oam_ip="192.168.255.129",
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.1", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.255.1", username="Nemuadmin", password="nemuuser"
    ),
)

_du_lmp_connection = SshServiceDetails(
    addr="192.168.255.1", username="toor4nsn", password="oZPS0POrRieRtu"
)

_du_capacity_unit = CapacityUnit(
    addr="192.168.253.20", hardware_type="ABIL", hardware_version="A102"
)

_du_common_unit = CommonUnit(
    lmp_connection=_du_lmp_connection,
    capacity_units=[_du_capacity_unit],
    hardware_type="ASIB",
    hardware_version="A101",
)

_ru = SC5GRadio(
    ru_hw_group="ASIR-HUB",
    sc_radio_connection_details=SCRadioConnectionDetails(
        ssh_connection_details=SshServiceDetails(
            addr="192.168.255.129",
            username="toor4nsn",
            password="oZPS0POrRieRtu",
            proxy=SshServiceDetails(
                addr="10.66.29.110", username="ute", password="Nokia666@ute!"
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

_airscale = Airscale([_du_common_unit])

_du = DU(airscale=_airscale, rus=[_ru])

_cbts = ClassicalBts(cu=_cu, dus=[_du], instance_id=2558, global_bts_id=2558)

_core = EPCSim(
    mme_ip="172.30.1.1",
    edaemon_port=10000,
    egate_port=20000,
    mcc=460,
    mnc=2,
    tac=1,
    default_ssh_connection_details=SshServiceDetails(
        addr="10.66.29.108",
        username="ute",
        password="uteUTE!",
    ),
    dir_path="/opt/core",
    cfg_filename="epcsim.cfg",
)


# Real ENB
_ru_2 = SC4GRadio(
    sc_radio_connection_details=SCRadioConnectionDetails(
        ssh_connection_details=SshServiceDetails(
            addr="192.168.255.129",
            username="toor4nsn",
            password="oZPS0POrRieRtu",
            proxy=SshServiceDetails(
                addr="10.66.29.109", username="ute", password="Nokia666@ute!"
            ),
        ),
        telnet_connection_details=TelnetConnectionDetails(
            addr="tty-server", username="toor4nsn", password="oZPS0POrRieRtu"
        ),
    )
)

_common_unit_enb = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_du_capacity_unit],
    hardware_type="ASIA",
    hardware_version="A.203",
)

_real_enb = Airscale(common_units=[_common_unit_enb])

lteenb = RealEnb(
    system_module=_real_enb,
    rms=[_ru_2],
    x2_link_addr=NetworkAddress(v4="10.66.36.29"),
    instance_id=2558,
    global_bts_id=25581,
)

################
#  UE config   #
################
def _set_abstract_lib_config_env(ue_config_file):
    tl_config_dir = os.path.dirname(os.path.abspath(__file__))
    ue_config_abs_path = os.path.join(tl_config_dir, ue_config_file)

    with open(ue_config_abs_path) as ta_ue_config:
        ue_config = yaml.safe_load(ta_ue_config)

    os.environ["ABSTRACT_LIB_CONFIG"] = ue_config_abs_path

    return ue_config


""" UE Configuration
In order to import UE configuration into the runtime environment of the robot framework,
the variable `ue_config` MUST NOT start with an underscore.
"""
ue_config = _set_abstract_lib_config_env("ue_config.yml")

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
        "value": "460:02:1000000009",
    },
    {
        "key": "UE_IP_1",
        "value": "27.168.1.14",
    },
]

tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    enbs=[lteenb],
    ues=[],
    core=_core,
    tl_cloud_topology="CLOUD_5G_CLASSICAL_ASIR_ASIKR_ABILB4_APHA_RFSHARING",
)
tl.ue_config = ue_config
tl.epcsim_config = epcsim_config

__all__ = ["tl"]
