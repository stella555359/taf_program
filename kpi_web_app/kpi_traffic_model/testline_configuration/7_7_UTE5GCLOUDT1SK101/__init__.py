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
    IperfDataTransferDetails,
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


_ue_config = _set_abstract_lib_config_env("ue_mtk.yaml")

_test_pc_gnb_default_ssh_connection_details = SshServiceDetails(
    addr="7-7-UTE5GCLOUDT1SK101.p01.ska-lab.nsn-rdnet.net",
    username="ute",
    password="ute",
)

_lmp_ip = "192.168.255.129"
_gnb_bh_ip = "10.84.164.101"
_gnb_oam_ip = _gnb_bh_ip
_gnb_oam_backhaul_ip = NetworkAddress(
    v4="{}/23".format(_gnb_bh_ip),
    routing_v4=RoutingInformation(gateway="10.84.165.254"),
    vlan_id=504,
)
_gnb_u_plane_ip = NetworkAddress(v4="10.84.164.101", vlan_id=504)
_gnb_c_plane_ip = NetworkAddress(v4="10.84.164.101", vlan_id=504)
_gnb_s1_plane_ip = NetworkAddress(v4="10.84.164.101", vlan_id=504)
_gnb_instance_id = 76101
_gnb_global_bts_id = 76101
_gnb_du_common_unit_hardware_type = "ASIB"
_gnb_ru1_ip = NetworkAddress(v4="172.22.0.154")  # FHED
_gnb_ru2_ip = NetworkAddress(v4="172.16.33.128")  # FHFB
_gnb_ru3_ip = NetworkAddress(v4="172.16.33.131")  # AZQC
_gnb_ru4_ip = NetworkAddress(v4="172.16.33.133")  # AZQC


_ahfii_hw_group = "FRMr6.2_4T4R"
_awhqn_hw_group = "ScRMTDr6.2_4T4R"

_gnb_pdu1 = FPFH(
    port_numbers=[1, 3, 4],
    addr="fpfh-zd06-46-p01.p01-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

_gnb_pdu2 = FPFH(
    port_numbers=[4, 6],
    addr="fpfh-zd06-48-p01.p01-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

##############################################################
_default_ssh_lmp_connection = SshServiceDetails(
    addr=_lmp_ip, username="toor4nsn", password="oZPS0POrRieRtu"
)
_default_oam_http_connection = HttpConnectionDetails(
    addr=_gnb_oam_ip, username="Nemuadmin", password="nemuuser", port=443
)
##############################################################

_ru_1_gnb = RU(
    radio_type="AWHQN",
    ru_hw_group=_awhqn_hw_group,
    serial_number="EB2244R1896",
    default_ssh_connection_details=SshServiceDetails(
        addr=_gnb_ru1_ip.v4, username="root", password="root"
    ),
    pdu_port=_gnb_pdu1.pdu_ports[4],
)
_ru_2_gnb = RU(
    radio_type="AHFII",
    ru_hw_group=_ahfii_hw_group,
    serial_number="BL2228N410X",
    default_ssh_connection_details=SshServiceDetails(
        addr=_gnb_ru2_ip.v4, username="root", password="root"
    ),
    pdu_port=_gnb_pdu2.pdu_ports[4],
)
_ru_3_gnb = RU(
    radio_type="AHFII",
    ru_hw_group=_ahfii_hw_group,
    serial_number="BL2227N40LX",
    default_ssh_connection_details=SshServiceDetails(
        addr=_gnb_ru3_ip.v4, username="root", password="root"
    ),
    pdu_port=_gnb_pdu1.pdu_ports[1],
)
_ru_4_gnb = RU(
    radio_type="AHFII",
    ru_hw_group=_ahfii_hw_group,
    serial_number="BL2228N40TJ",
    default_ssh_connection_details=SshServiceDetails(
        addr=_gnb_ru4_ip.v4, username="root", password="root"
    ),
    pdu_port=_gnb_pdu2.pdu_ports[6],
)

_radio_units_gnb = [_ru_1_gnb, _ru_2_gnb, _ru_3_gnb, _ru_4_gnb]

# gNB section
_cu_gnb = CU(
    oam_ssh_connection_details=_default_ssh_lmp_connection,  # replace if other than default
    oam_http_connection_details=_default_oam_http_connection,
    backhaul_site_oam_ip=_gnb_oam_backhaul_ip,
    x2c=_gnb_c_plane_ip,
    x2u=_gnb_u_plane_ip,
    s1u=_gnb_s1_plane_ip,
)

_abio_L = CapacityUnit(addr="192.168.253.20", hardware_type="ABIO", rus=_radio_units_gnb)
_capacity_units = [_abio_L]
_du_lmp_connection_gnb = _default_ssh_lmp_connection
_du_lmp_connection_gnb.proxy = _test_pc_gnb_default_ssh_connection_details
_du_common_unit_gnb = CommonUnit(
    lmp_connection=_du_lmp_connection_gnb,
    pdu_port=_gnb_pdu1.pdu_ports[3],
    hardware_type=_gnb_du_common_unit_hardware_type,
    capacity_units=_capacity_units,
)

########################################################################################
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

tl = TestLine(
    test_pc=_test_pc_gnb_main,
    gnbs=[_gnb_main],
    pdus=[_gnb_pdu1, _gnb_pdu2],
    test_pcs=[_test_pc_gnb_main],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_ASIBL_ABIOB1_3xAHFII_AWHQN",
)
__all__ = ["tl"]
