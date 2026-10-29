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
from taf.config.testline.pdu import PduPort, Pdu
from taf.config.testline import RealEnb
from taf.config.testline.core import EPCSim
from taf.config.testline.gnb.networkaddress import NetworkAddress, RoutingInformation

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.66.31.11", username="ute", password="uteUTE!"
    )
)
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.66.30.47",
        vlan_id=30,
        routing=RoutingInformation(gateway="10.66.30.1", ip_prefix_length=24),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.255.129", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(v4="10.66.23.33", vlan_id=23),
    x2u=NetworkAddress(v4="172.16.230.33", vlan_id=230),
    s1c=NetworkAddress(v4="10.66.23.33", vlan_id=23),
    s1u=NetworkAddress(v4="172.16.230.33", vlan_id=230),
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

_ru_1 = SC5GRadio(
    ru_hw_group="ASIR-HUB",
    sc_radio_connection_details=SCRadioConnectionDetails(
        ssh_connection_details=SshServiceDetails(
            addr="192.168.255.129",
            username="toor4nsn",
            password="oZPS0POrRieRtu",
            proxy=SshServiceDetails(
                addr="10.66.31.13", username="ute", password="uteUTE!"
            ),
        ),
        telnet_connection_details=TelnetConnectionDetails(
            addr="tty-server", username="toor4nsn", password="oZPS0POrRieRtu"
        ),
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    # pdu_port=PduPort(
    #     pdu=Pdu(addr='1.1.1.1', port_numbers=[1, 2]), port_no=1)
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
                addr="10.66.31.14", username="ute", password="uteUTE!"
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

_cbts = ClassicalBts(cu=_cu, dus=[_du], instance_id=4034, global_bts_id=4034)

_epcsim = EPCSim(
    mme_ip="172.30.1.10",
    edaemon_port=10000,
    egate_port=20000,
    mcc=460,
    mnc=6,
    tac=500,
    default_ssh_connection_details=SshServiceDetails(
        addr="10.66.31.11",
        username="ute",
        password="uteUTE!",
    ),
    dir_path="/opt/core",
    cfg_filename="epcsim.cfg",
)

from taf.config.testline.attenuator import AttenuationPort, TopYoung, HBTE, RadioRack

_gnb_rf_att = RadioRack(
    ip_addr="10.66.25.85",
    port="50000",
    attenuation_port_numbers=[5, 6, 7, 8, 9, 10, 11, 12],
)

_lteenb = RealEnb(x2_link_addr=NetworkAddress(v4="172.31.1.10"))

""" UE Configuration
In order to import UE configuration into the runtime environment of the robot framework,
the variable `ue_config` MUST NOT start with an underscore.
"""


def _set_abstract_lib_config_env(ue_config_file):
    ue_config_abs_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), ue_config_file
    )
    with open(ue_config_abs_path) as ta_ue_config:
        ue_config = yaml.safe_load(ta_ue_config)

    os.environ["ABSTRACT_LIB_CONFIG"] = ue_config_abs_path

    return ue_config


ue_config = _set_abstract_lib_config_env("ue_config.yaml")

tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    enbs=[_lteenb],
    ues=None,
    core=_epcsim,
    attenuator=_gnb_rf_att,
    tl_cloud_topology="CLOUD_5G CLASSICAL ASIR_ASIKR_ABILB4_2xAPHG_3xAWHHC_SA",
)
tl.ue_config = ue_config

__all__ = ["tl"]
