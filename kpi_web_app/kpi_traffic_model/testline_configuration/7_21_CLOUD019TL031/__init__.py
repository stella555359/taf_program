__maintainer__ = "Xie Shanshan"
__team__ = "MG_5G_NJN_Vrf_Hope"
__email__ = "I_EXT_NJ_APPS_PNP_TEST@internal.nsn.com"
__owner_email__ = "shanshan.a.xie@nokia-sbell.com"

from taf.config.testline.ue import Android
from taf.config.testline.testline import TestLine
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    SCRadioConnectionDetails,
    TelnetConnectionDetails,
)
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline import SC5GRadio

# from taf.config.testline.core import EPCSim
from taf.config.testline.pdu import PduPort, ATEN
from taf.config.testline.pdu import PduPort, Pdu
from taf.config.testline.enb import RealEnb
from taf.config.testline.pdu import PduPort, ATEN, FACOM, Pdu, EPC
from taf.config.testline.gnb.networkaddress import NetworkAddress
import os
import yaml


def _set_abstract_lib_config_env(ue_config_file):
    tl_config_dir = os.path.dirname(os.path.abspath(__file__))
    ue_config_abs_path = os.path.join(tl_config_dir, ue_config_file)

    with open(ue_config_abs_path) as ta_ue_config:
        ue_config = yaml.safe_load(ta_ue_config)

    os.environ["ABSTRACT_LIB_CONFIG"] = ue_config_abs_path

    return ue_config


_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.66.29.43", username="ute", password="ute"
    )
)

_cu = CU(
    backhaul_site_oam_ip="172.30.1.11",
    oam_ssh_connection_details=SshServiceDetails(
        addr="172.30.1.11", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="172.30.1.11", username="Nemuadmin", password="nemuuser"
    ),
)

_du_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_du_capacity_unit = CapacityUnit(
    addr="192.168.253.38", hardware_type="ABIL", hardware_version="102"
)
_du_pdu = ATEN("1.1.1.1", [0])
_du_pdu_port = PduPort(_du_pdu, 0)

_du_common_unit = CommonUnit(
    lmp_connection=_du_lmp_connection,
    capacity_units=[_du_capacity_unit],
    hardware_type="ASIK",
    hardware_version="101",
)

_ru_0 = SC5GRadio(
    ru_hw_group="ASIR-HUB",
    sc_radio_connection_details=SCRadioConnectionDetails(
        ssh_connection_details=SshServiceDetails(
            addr="192.168.255.129",
            username="toor4nsn",
            password="oZPS0POrRieRtu",
            proxy=SshServiceDetails(addr="10.66.29.46", username="ute", password="ute"),
        ),
        telnet_connection_details=TelnetConnectionDetails(
            addr="tty-server", username="toor4nsn", password="oZPS0POrRieRtu"
        ),
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=PduPort(pdu=ATEN(addr="1.1.1.1", port_numbers=[1, 2]), port_no=1),
)

_cu = CU(
    backhaul_site_oam_ip="172.30.1.11",
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.255.129", username="Nemuadmin", password="nemuuser"
    ),
)

_airscale = Airscale(common_units=[_du_common_unit])

_du = DU(airscale=_airscale, rus=[_ru_0])

_cbts = ClassicalBts(cu=_cu, dus=[_du], instance_id=4007, global_bts_id=4007)

_ue_config = _set_abstract_lib_config_env("ue_config.yaml")
ue_config = _set_abstract_lib_config_env("ue_config.yaml")

tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    ues=[_ue_config],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_ASIR_ASIKA101L_ABILA102B1_PERF",
)

__all__ = ["tl"]
