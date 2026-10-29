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

# from taf.config.testline.pdu import PduPort, ATEN
from taf.config.testline.enb import RealEnb
from taf.config.testline.core import EPCSim
from taf.config.testline.gnb.networkaddress import NetworkAddress, RoutingInformation
import os
import yaml

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        #addr="10.66.12.235", username="ute", password="uteUTE!"
        addr="10.66.12.235", username="ute", password="Nokia666@ute!" 
    )
)

_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="172.30.1.11",
        vlan_id=69,
        routing=RoutingInformation(gateway="172.30.1.1", ip_prefix_length=24),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.1", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.255.1", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(v4="172.30.1.11", vlan_id=67),
    x2u=NetworkAddress(v4="172.30.1.11", vlan_id=67),
    s1c=NetworkAddress(v4="172.30.1.11", vlan_id=67),
    s1u=NetworkAddress(v4="172.30.1.11", vlan_id=67),
)

_du_lmp_connection = SshServiceDetails(
    addr="192.168.255.1", username="toor4nsn", password="oZPS0POrRieRtu"
)

_du_capacity_unit = CapacityUnit(
    addr="fsp1_c", hardware_type="ABIL", hardware_version="A102"
)

_du_common_unit = CommonUnit(
    lmp_connection=_du_lmp_connection,
    capacity_units=[_du_capacity_unit],
    hardware_type="ASIK",
    hardware_version="A101",
)

_ru_1 = SC5GRadio(
    ru_hw_group="ASIR-HUB",
    sc_radio_connection_details=SCRadioConnectionDetails(
        ssh_connection_details=SshServiceDetails(
            addr="192.168.255.129",
            username="toor4nsn",
            password="oZPS0POrRieRtu",
            #proxy=SshServiceDetails(addr="10.66.17.47", username="ute", password="ute"),
            proxy=SshServiceDetails(addr="10.66.17.47", username="ute", password="Nokia666@ute!"),
        ),
        telnet_connection_details=TelnetConnectionDetails(
            addr="tty-server", username="toor4nsn", password="oZPS0POrRieRtu"
        ),
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    # pdu_port=PduPort(pdu=ATEN(addr='1.1.1.1', port_numbers=[1, 2]), port_no=1)
    pdu_port=None,
)

_airscale = Airscale(common_units=[_du_common_unit])

_du = DU(airscale=_airscale, rus=[_ru_1])

_instance_id = 1
_bts = ClassicalBts(cu=_cu, dus=[_du], instance_id=_instance_id, global_bts_id=1)

_epcsim = EPCSim(
    mme_ip="172.30.1.1",
    edaemon_port=10000,
    egate_port=20000,
    mcc=460,
    mnc=6,
    tac=1,
    default_ssh_connection_details=SshServiceDetails(
        addr="10.66.12.235",
        username="ute",
        #password="uteUTE!",
        password="Nokia666@ute!",
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
                #addr="10.66.17.46", username="ute", password="ute"
                addr="10.66.17.46", username="ute", password="Nokia666@ute!"
            ),
        ),
        telnet_connection_details=TelnetConnectionDetails(
            addr="tty-server", username="toor4nsn", password="oZPS0POrRieRtu"
        ),
    )
)

_common_unit_enb = CommonUnit(
    lmp_connection=SshServiceDetails(
        #addr="172.30.1.10", username="toor4nsn", password="oZPS0POrRieRtu"
        addr="10.66.36.27", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_du_capacity_unit],
    hardware_type="ASIA",
    hardware_version="A.203",
)

_real_enb = Airscale(common_units=[_common_unit_enb])

lteenb = RealEnb(
    system_module=_real_enb,
    rms=[_ru_2],
    #x2_link_addr=NetworkAddress(v4="172.30.1.10"),
    x2_link_addr=NetworkAddress(v4="10.66.36.27"),
    instance_id=1,
    global_bts_id=1,
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
        "value": "460:06:4200000042",
    },
    {
        "key": "UE_IP_1",
        "value": "27.168.1.10",
    },
]

tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_bts],
    enbs=[lteenb],
    ues=[],
    core=_epcsim,
    tl_cloud_topology="CLOUD_5G_CLASSICAL_ASIR_ASIKR_ABILB4_APHA_RFSHARING",
)
tl.ue_config = ue_config
tl.epcsim_config = epcsim_config

__all__ = ["tl"]
