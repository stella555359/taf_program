__maintainer__ = "Sara Nowak"
__team__ = "MN_RAN_Pz_KRK_6_SG"
__email__ = "sara.nowak@nokia.com"

from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
)
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline.gnb.networkaddress import NetworkAddress, RoutingInformation
from taf.config.testline.radio import RU, RUExtension
from taf.config.testline.enb import RealEnb
from taf.config.testline.airscale import (
    Airscale,
    CommonUnit,
    CapacityUnit,
    SlotId,
    TRSInterfaces,
)
from taf.config.testline.pdu import FPFH, PduPort, ATEN
import os
import yaml


def _set_abstract_lib_config_env(ue_config_file):
    tl_config_dir = os.path.dirname(os.path.abspath(__file__))
    ue_config_abs_path = os.path.join(tl_config_dir, ue_config_file)

    with open(ue_config_abs_path) as ta_ue_config:
        ue_config = yaml.safe_load(ta_ue_config)
    os.environ["ABSTRACT_LIB_CONFIG"] = ue_config_abs_path

    return ue_config


_ue_config = _set_abstract_lib_config_env("ue.yaml")

_gnb_s1u_ip = NetworkAddress(
    v4="10.83.182.203",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_xnu_ip = NetworkAddress(
    v4="10.83.182.203",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_f1m_ip = NetworkAddress(
    v4="10.83.182.203",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_f1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_oam_ip = NetworkAddress(
    v4="10.83.182.203/23",
    routing_v4=RoutingInformation(gateway="10.83.183.254"),
    vlan_id=503,
)

_gnb_ngc_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_x2c_ip = NetworkAddress(
    v4="10.83.182.203",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_ngu_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_xnc_ip = NetworkAddress(
    v4="10.83.182.203",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_x2u_ip = NetworkAddress(
    v4="10.83.182.203",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_f1u_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_pdu1 = FPFH(
    addr="fpfh-gd06-48-sc5g.sc5g-leg.krk-lab.nsn-rdnet.net",
    port_numbers=["6"],
    login="admin",
    password="admin",
)

_pdus = [_pdu1]
_pdu_port = PduPort(pdu=_pdu1, port_no=6)

_gnb_instance_id = 75203
_gnb_global_bts_id = 75203
_gnb_du_common_unit_hardwarde_type = "ASIK"

_test_pc_gnb_default_ssh_connection_details = SshServiceDetails(
    addr="7-7-UTE5GCLOUDT203.sc5g.krk-lab.nsn-rdnet.net", username="ute", password="ute"
)
_test_pc_enb_default_ssh_connection_details = SshServiceDetails(
    addr="7-7-UTE5GCLOUDT020.sc5g.krk-lab.nsn-rdnet.net", username="ute", password="ute"
)

_default_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
)

_default_oam_http_connection = HttpConnectionDetails(
    addr=_gnb_oam_ip.v4, username="Nemuadmin", password="nemuuser", port=443
)

_du_lmp_connection_gnb = _default_ssh_lmp_connection
_du_lmp_connection_gnb.proxy = _test_pc_gnb_default_ssh_connection_details

_asik_master_gnb = CapacityUnit(
    addr="192.168.253.22", hardware_type="ASIK", hardware_version=""  # fsp1_c
)

_du_common_unit_gnb = CommonUnit(
    lmp_connection=_du_lmp_connection_gnb,
    capacity_units=[_asik_master_gnb],
    hardware_type=_gnb_du_common_unit_hardwarde_type,
    hardware_version="A.102",
)

_test_pc_gnb_main = TestPc(
    default_ssh_connection_details=_test_pc_gnb_default_ssh_connection_details,
    connections=[_du_common_unit_gnb],
)

_enb_instance_id = 75020
_enb_global_bts_id = 75020

enb_capacity_unit_0 = CapacityUnit(
    addr="",
    hardware_type="Flexi",
    hardware_version="A.101",
    serial_number="NK171330749",
    product_code="472797A.101",
    slot_id=SlotId.C1,
)

enb_common_unit_0 = CommonUnit(
    lmp_connection=_default_ssh_lmp_connection,
    capacity_units=[enb_capacity_unit_0],
    hardware_type="Flexi",
    hardware_version="",
    serial_number="L1212506106",
    mac_addr="",
    trs_connections=[],
)

_airscale_enb = Airscale(common_units=[enb_common_unit_0], product_code="473098A")

_bts_enb_0 = RealEnb(
    system_module=_airscale_enb,
    instance_id=75020,
    global_bts_id=75020,
    oam_ip=NetworkAddress(
        v4="10.83.182.20",
        routing_v4=RoutingInformation(gateway="10.84.165.254"),
    ),
    x2_link_addr=NetworkAddress(v4="10.83.182.20"),
)

_test_pc_enb_0 = TestPc(
    default_ssh_connection_details=_test_pc_enb_default_ssh_connection_details,
    connections=[_bts_enb_0],
)

_cu_gnb = CU(
    backhaul_site_oam_ip=_gnb_oam_ip,
    oam_ssh_connection_details=_default_ssh_lmp_connection,
    oam_http_connection_details=_default_oam_http_connection,
    f1m=_gnb_f1m_ip,
    f1c=_gnb_f1c_ip,
    f1u=_gnb_f1u_ip,
    x2c=_gnb_x2c_ip,
    x2u=_gnb_x2u_ip,
    s1c=_gnb_s1c_ip,
    s1u=_gnb_s1u_ip,
    xnc=_gnb_xnc_ip,
    xnu=_gnb_xnu_ip,
    ngc=_gnb_ngc_ip,
    ngu=_gnb_ngu_ip,
    instance_id=_gnb_instance_id,
    global_bts_id=_gnb_global_bts_id,
)

gnb_capacity_unit_0 = CapacityUnit(
    addr="192.168.253.26",
    hardware_type="ABIL",
    hardware_version="B.102",
    serial_number="DH213638391",
    product_code="474020B.102",
    slot_id=SlotId.B2,
)

gnb_capacity_unit_1 = CapacityUnit(
    addr="192.168.253.30",
    hardware_type="ABIL",
    hardware_version="B.102",
    serial_number="DH213743557",
    product_code="474020B.102",
    slot_id=SlotId.B3,
)

gnb_capacity_unit_2 = CapacityUnit(
    addr="192.168.253.22",
    hardware_type="ABIL",
    hardware_version="B.102",
    serial_number="L1203611798",
    product_code="474020B.102",
    slot_id=SlotId.B1,
)

gnb_common_unit_0 = CommonUnit(
    lmp_connection=_default_ssh_lmp_connection,
    capacity_units=[gnb_capacity_unit_0, gnb_capacity_unit_1, gnb_capacity_unit_2],
    hardware_type="ASIK",
    hardware_version="A.102",
    serial_number="L1204210517",
    mac_addr="00:77:e4:1c:46:28",
    trs_connections=[TRSInterfaces.EIF1],
    slot_id=SlotId.C1,
)

gnb_radio_unit_0 = RU(
    ru_hw_group="AEQB",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.50.166", username="root", password="umniedziala"
    ),
    radio_type="AEQB",
    serial_number="1M193616977",
    product_code="474413A.X21",
)

gnb_radio_unit_1 = RU(
    ru_hw_group="AEQB",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.49.162", username="root", password="umniedziala"
    ),
    radio_type="AEQB",
    serial_number="6Q194803017",
    product_code="474413A.X21",
)

gnb_radio_unit_2 = RU(
    ru_hw_group="AEQB",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.48.166", username="root", password="umniedziala"
    ),
    radio_type="AEQB",
    serial_number="1M201014584",
    product_code="474413A.101",
)

_airscale_gnb = Airscale(common_units=[gnb_common_unit_0], product_code="473098A")

_du_gnb = DU(
    airscale=_airscale_gnb,
    rus=[gnb_radio_unit_0, gnb_radio_unit_1, gnb_radio_unit_2],
    oam_ip=_gnb_oam_ip,
    f1_m_ip_addr=_gnb_f1m_ip,
    f1_c_ip_addr=_gnb_f1c_ip,
    f1_u_ip_addr=_gnb_f1u_ip,
    f1_m_cu=_gnb_f1m_ip,
    f1_c_cu=_gnb_f1c_ip,
    f1_u_cu=_gnb_f1u_ip,
    instance_id=_gnb_instance_id,
    global_bts_id=_gnb_global_bts_id,
)

_gnb = ClassicalBts(
    cu=_cu_gnb,
    dus=[_du_gnb],
    instance_id=_gnb_instance_id,
    global_bts_id=_gnb_global_bts_id,
)

_enb_f1m_ip = NetworkAddress(
    v4="10.83.182.20",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

tl = TestLine(
    test_pc=_test_pc_gnb_main,
    gnbs=[_gnb],
    enbs=[_bts_enb_0],
    test_pcs=[_test_pc_gnb_main, _test_pc_enb_0],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_ANDROID_ASIKL_ABILB1B2B3_3xAEQB_ENB",
    pdus=_pdus,
)

__all__ = ["tl"]
