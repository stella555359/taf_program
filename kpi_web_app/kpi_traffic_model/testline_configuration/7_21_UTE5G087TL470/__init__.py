__maintainer__ = "TDD SA 5G"
__team__ = "Syve NJ"
__email__ = "shen.a.zhao@nokia-sbell.com"

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
from taf.config.testline import RealEnb
from taf.config.testline.core import EPCSim
from taf.config.testline.gnb.networkaddress import NetworkAddress, RoutingInformation
from taf.config.testline.pdu import PduPort, ATEN, FACOM, Pdu, EPC , HBTE, FPFH

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.66.51.36", username="ute", password="ute"
    )
)

_pdu_1 = FPFH(port_numbers=[1], addr="10.66.47.26", login="admin", password="admin", model="FPFH",)
_pdus = [_pdu_1]
_cu1 = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.66.23.232",
        vlan_id=23,
        routing=RoutingInformation(gateway="10.66.23.1", ip_prefix_length=24),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.66.23.232", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.255.129", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(v4="10.66.23.232", vlan_id=23),
    x2u=NetworkAddress(v4="10.66.23.232", vlan_id=23),
    s1c=NetworkAddress(v4="10.66.23.232", vlan_id=23),
    s1u=NetworkAddress(v4="10.66.23.232", vlan_id=23),
    f1m=NetworkAddress(v4="10.66.23.232", vlan_id=23),
    f1c=NetworkAddress(v4="10.66.23.232", vlan_id=23),
    f1u=NetworkAddress(v4="10.66.23.232", vlan_id=23),
)

_lmp_connection1 = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=SshServiceDetails(addr="10.66.51.36", username="ute", password="ute"),
)

_capacity_unit1 = CapacityUnit(
    addr="fsp1_c", hardware_type="ABIP", hardware_version="101"
)

_common_unit1 = CommonUnit(
    lmp_connection=_lmp_connection1,
    capacity_units=[_capacity_unit1],
    hardware_type="ASIL",
    hardware_version="101",
    pdu_port=_pdus[0].pdu_ports[1],
)

_ru1 = SC5GRadio(
    ru_hw_group="ASIR-HUB",
    sc_radio_connection_details=SCRadioConnectionDetails(
        ssh_connection_details=SshServiceDetails(
            addr="192.168.255.129",
            username="toor4nsn",
            password="oZPS0POrRieRtu",
            proxy=SshServiceDetails(
                addr="10.66.51.37", username="ute", password="ute"
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

_airscale1 = Airscale(common_units=[_common_unit1])

_du1 = DU(airscale=_airscale1, rus=[_ru1])

_cbts1 = ClassicalBts(cu=_cu1, dus=[_du1], instance_id=37098, global_bts_id=37098)


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
    test_pcs=[_test_pc],
    gnbs=[_cbts1],
    ues=None,
    pdus=_pdus,
    tl_cloud_topology="CLOUD_5G_CLASSICAL_SA_2XASILL_1XABIPB1_APHH_TDD",
)

tl.ue_config = ue_config

__all__ = ["tl"]
