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
        addr="10.66.17.134", username="ute", password="uteUTE!"
    )
)

_pdu_1 = FPFH(port_numbers=[1], addr="10.66.47.26", login="admin", password="admin", model="FPFH",)
_pdus = [_pdu_1]
_cu1 = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.66.23.123",
        vlan_id=23,
        routing=RoutingInformation(gateway="10.66.23.1", ip_prefix_length=24),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.66.14.220", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.255.129", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(v4="10.66.23.123", vlan_id=23),
    x2u=NetworkAddress(v4="10.66.23.123", vlan_id=23),
    s1c=NetworkAddress(v4="10.66.23.123", vlan_id=23),
    s1u=NetworkAddress(v4="10.66.23.123", vlan_id=23),
    f1m=NetworkAddress(v4="10.66.23.123", vlan_id=23),
    f1c=NetworkAddress(v4="10.66.23.123", vlan_id=23),
    f1u=NetworkAddress(v4="10.66.23.123", vlan_id=23),
)

_lmp_connection1 = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=SshServiceDetails(addr="10.66.17.134", username="ute", password="ute"),
)

_capacity_unit1 = CapacityUnit(
    addr="fsp1_c", hardware_type="ABIO", hardware_version="104"
)

_common_unit1 = CommonUnit(
    lmp_connection=_lmp_connection1,
    capacity_units=[_capacity_unit1],
    hardware_type="ASIL",
    hardware_version="102",
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
                addr="10.66.17.233", username="ute", password="ute"
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

_cbts1 = ClassicalBts(cu=_cu1, dus=[_du1], instance_id=11464, global_bts_id=11464)

_cu2 = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.66.23.149",
        vlan_id=23,
        routing=RoutingInformation(gateway="10.66.23.1", ip_prefix_length=24),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.66.17.82", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.66.17.82", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(v4="10.66.23.149", vlan_id=23),
    x2u=NetworkAddress(v4="10.66.23.149", vlan_id=23),
    s1c=NetworkAddress(v4="10.66.23.149", vlan_id=23),
    s1u=NetworkAddress(v4="10.66.23.149", vlan_id=23),
)

_lmp_connection2 = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=SshServiceDetails(addr="10.66.17.163", username="ute", password="ute"),
)

_capacity_unit2 = CapacityUnit(
    addr="fsp1_c", hardware_type="ABIO", hardware_version="104"
)

_common_unit2 = CommonUnit(
    lmp_connection=_lmp_connection2,
    capacity_units=[_capacity_unit2],
    hardware_type="ASIL",
    hardware_version="101",
)

_ru2 = SC5GRadio(
    ru_hw_group="ASIR-HUB",
    sc_radio_connection_details=SCRadioConnectionDetails(
        ssh_connection_details=SshServiceDetails(
            addr="192.168.255.129",
            username="toor4nsn",
            password="oZPS0POrRieRtu",
            proxy=SshServiceDetails(
                addr="10.66.17.234", username="ute", password="ute"
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

_airscale2 = Airscale(common_units=[_common_unit2])

_du2 = DU(airscale=_airscale2, rus=[_ru2])

_cbts2 = ClassicalBts(cu=_cu2, dus=[_du2], instance_id=11472, global_bts_id=11472)

_cu3 = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.66.23.145",
        vlan_id=23,
        routing=RoutingInformation(gateway="10.66.23.1", ip_prefix_length=24),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.66.14.15", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.66.14.15", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(v4="10.66.23.145", vlan_id=23),
    x2u=NetworkAddress(v4="10.66.23.145", vlan_id=23),
    s1c=NetworkAddress(v4="10.66.23.145", vlan_id=23),
    s1u=NetworkAddress(v4="10.66.23.145", vlan_id=23),
)

_lmp_connection3 = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=SshServiceDetails(addr="10.66.17.113", username="ute", password="ute"),
)

_capacity_unit3 = CapacityUnit(
    addr="fsp1_c", hardware_type="ABIL", hardware_version="102"
)

_common_unit3 = CommonUnit(
    lmp_connection=_lmp_connection3,
    capacity_units=[_capacity_unit3],
    hardware_type="ASIB",
    hardware_version="102",
)

_ru3 = SC5GRadio(
    ru_hw_group="ASIR-HUB",
    sc_radio_connection_details=SCRadioConnectionDetails(
        ssh_connection_details=SshServiceDetails(
            addr="192.168.255.129",
            username="toor4nsn",
            password="oZPS0POrRieRtu",
            proxy=SshServiceDetails(
                addr="10.66.17.144", username="ute", password="ute"
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
_airscale3 = Airscale(common_units=[_common_unit3])
_du3 = DU(airscale=_airscale3, rus=[_ru3])
_cbts3 = ClassicalBts(cu=_cu3, dus=[_du3], instance_id=11427, global_bts_id=11427)


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
    tl_cloud_topology="CLOUD_5G_CLASSICAL_SA_ASILL_ABIOB1_2xAPHG_5xAWHQT_3xAWHHC_APHH_TDD",
)

tl.ue_config = ue_config
tl.src_gnbs = [_cbts2, _cbts3]

__all__ = ["tl"]
