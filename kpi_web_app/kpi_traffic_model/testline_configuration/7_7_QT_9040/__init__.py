__maintainer__ = "I_MN_5GSC_KRK_AUTO"
__team__ = "I_MN_5GSC_KRK_AUTO"
__email__ = "I_MN_5GSC_KRK_AUTO@internal.nsn.com"
import os
import yaml
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    TelnetConnectionDetails,
)
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline import NetworkAddress, RU, RoutingInformation
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.pdu import PduPort, FPFH


def _set_abstract_lib_config_env(ue_config_file):
    tl_config_dir = os.path.dirname(os.path.abspath(__file__))

    ue_config_abs_path = os.path.join(tl_config_dir, ue_config_file)

    with open(ue_config_abs_path) as ta_ue_config:
        ue_config = yaml.safe_load(ta_ue_config)
    os.environ["ABSTRACT_LIB_CONFIG"] = ue_config_abs_path

    return ue_config


# The most commonly used testline configuration. #
_test_pc_gnb_default_ssh_connection_details = SshServiceDetails(
    addr="7-7-UTE5GCLOUDT11SK040.p11.ska-lab.nsn-rdnet.net",
    username="ute",
    password="ute",
)


_lmp_ip = "192.168.255.129"
_gnb_bh_ip = "10.82.28.40"
_gnb_oam_ip = _gnb_bh_ip
_gnb_oam_backhaul_ip = NetworkAddress(
    v4="{}/23".format(_gnb_bh_ip),
    routing_v4=RoutingInformation(gateway="10.82.29.254"),
    vlan_id=504,
)

_default_oam_http_connection = HttpConnectionDetails(
    addr="192.168.255.129",
    username="Nemuadmin",
    password="nemuuser",
    port=443,
)

_gnb_u_plane_ip = NetworkAddress(v4="10.82.28.40", vlan_id=504)
_gnb_c_plane_ip = NetworkAddress(v4="10.82.28.40", vlan_id=504)
_gnb_instance_id = 81040
_gnb_global_bts_id = 81040
_gnb_du_common_unit_hardware_type = "ASOE"
_gnb_ru1_ip = NetworkAddress(v4="172.16.33.128")

_aphg_hw_group = "aphg"

_gnb_pdu = FPFH(
    port_numbers=[4],
    addr="10.255.10.90",
    login="admin",
    password="admin",
)

##############################################################
# Default values
_default_ssh_lmp_connection = SshServiceDetails(
    addr=_lmp_ip, username="toor4nsn", password="oZPS0POrRieRtu"
)

_default_oam_http_connection = HttpConnectionDetails(
    addr=_gnb_oam_ip, username="Nemuadmin", password="nemuuser", port=443
)
##############################################################
# Important!: check and change below if other than default #
# gNB section
_cu_gnb = CU(
    oam_ssh_connection_details=_default_ssh_lmp_connection,  # replace if other than default
    oam_http_connection_details=_default_oam_http_connection,
    backhaul_site_oam_ip=_gnb_oam_backhaul_ip,
    x2c=_gnb_c_plane_ip,
    x2u=_gnb_u_plane_ip,
)  # replace if other than default

_asoe_L = CapacityUnit(addr="192.168.253.20", hardware_type="ASOE")
_capacity_units = [_asoe_L]
_du_lmp_connection_gnb = _default_ssh_lmp_connection
_du_lmp_connection_gnb.proxy = _test_pc_gnb_default_ssh_connection_details
_du_common_unit_gnb = CommonUnit(
    lmp_connection=_du_lmp_connection_gnb,
    pdu_port=_gnb_pdu.pdu_ports[4],
    hardware_type=_gnb_du_common_unit_hardware_type,
    capacity_units=_capacity_units,
)

########################################################################################
_ru_1_gnb = RU(
    radio_type="APHG",
    ru_hw_group=_aphg_hw_group,
    serial_number="NH211600064",
    default_ssh_connection_details=SshServiceDetails(
        addr=_gnb_ru1_ip.v4, username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_gnb_pdu.pdu_ports[4],
)

_radio_units_gnb = [_ru_1_gnb]
_airscale_gnb = Airscale(common_units=[_du_common_unit_gnb])
_du_gnb = DU(airscale=_airscale_gnb, rus=_radio_units_gnb)
_gnb_main = ClassicalBts(
    cu=_cu_gnb,
    dus=[_du_gnb],
    instance_id=_gnb_instance_id,
    global_bts_id=_gnb_global_bts_id,
)

# Test PCs
_test_pc_gnb_main = TestPc(
    default_ssh_connection_details=_test_pc_gnb_default_ssh_connection_details,
    connections=[_du_common_unit_gnb],
)

# Test line
_ue_config = _set_abstract_lib_config_env("ue_config.yaml")

tl = TestLine(
    test_pc=_test_pc_gnb_main,
    gnbs=[_gnb_main],
    pdus=[_gnb_pdu],
    ues=[_ue_config],
    tl_cloud_topology="krk-9040",
    test_pcs=[_test_pc_gnb_main],
)
__all__ = ["tl"]
