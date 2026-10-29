__maintainer__ = "Karol Lapczyk"
__team__ = "5G_PZ_MMW_KRK_3_SG"
__email__ = "karol.lapczyk@nokia.com"

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
from taf.config.testline.gnb.networkaddress import NetworkAddress, RoutingInformation
from taf.config.testline.radio import RU, RUExtension, SC5GRadio
from taf.config.testline.pdu import PduPort, ATEN, HPE, FPFH
from taf.config.testline.airscale import (
    Airscale,
    CommonUnit,
    CapacityUnit,
    SlotId,
    TRSInterfaces,
)

# ------------------------FPFH_CONFIGURATION------------------------
_gnb_pdu_1 = FPFH(
    port_numbers=[1, 2],
    addr="fpfh-za06-48-p04.p04-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)
_gnb_pdu_2 = FPFH(
    port_numbers=[2],
    addr="fpfh-zb06-48-p04.p04-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)
# ------------------------GNB_CONFIGURATION------------------------

_gnb_oam_ip = NetworkAddress(
    v4="10.84.190.32/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=503,
)

_gnb_f1m_ip = NetworkAddress(
    v4="10.84.190.32/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)
_gnb_u_plane_ip = NetworkAddress(
    v4="10.255.22.32/23",
    routing_v4=RoutingInformation(gateway="10.255.23.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)
_test_pc_gnb = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT4SK032.p04.ska-lab.nsn-rdnet.net",
        username="ute",
        password="uteUTE!",
    ),
)

_gnb_instance_id = 77032
_gnb_global_bts_id = 77032

_default_gnb_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_gnb.default_ssh_connection_details,
)

_default_oam_http_connection = HttpConnectionDetails(
    addr=_gnb_oam_ip.v4.split("/")[0],
    username="Nemuadmin",
    password="nemuuser",
    port=443,
)
_cu_gnb = CU(
    backhaul_site_oam_ip=_gnb_oam_ip,
    oam_ssh_connection_details=_default_gnb_ssh_lmp_connection,
    oam_http_connection_details=_default_oam_http_connection,
    f1m=_gnb_f1m_ip,
    s1u=_gnb_u_plane_ip,
    instance_id=_gnb_instance_id,
    global_bts_id=_gnb_global_bts_id,
)

gnb_capacity_unit_0 = CapacityUnit(
    addr="",
    hardware_type="ABIA",
    hardware_version="A.107",
    serial_number="L1213412942",
    product_code="473096A.107",
)
gnb_capacity_unit_1 = CapacityUnit(
    addr="",
    hardware_type="ABIL",
    hardware_version="A.102",
    serial_number="L1192301758",
    product_code="474020A.102",
)

gnb_common_unit_0 = CommonUnit(
    lmp_connection=_default_gnb_ssh_lmp_connection,
    capacity_units=[gnb_capacity_unit_0],
    pdu_port=PduPort(pdu=_gnb_pdu_1, port_no=2),
    hardware_type="ABIL",
    hardware_version="A.102",
    serial_number="DH212766882",
    mac_addr="",
)

gnb_radio_unit_0 = RU(
    ru_hw_group="AHFIB",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.10.130", username="root", password="umniedziala"
    ),
    pdu_port=PduPort(pdu=_gnb_pdu_2, port_no=2),
    radio_type="AHFIB",
    serial_number="BL2044V0RIX",
    product_code="474216A.101",
)

gnb_radio_unit_1 = RU(
    ru_hw_group="AWEUB",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.10.128", username="rfsw", password="ckBW1r1CX7VUPHcoHd69to3UwvEVm+cGW1aXDlfr51Y="
    ),
    pdu_port=PduPort(pdu=_gnb_pdu_1, port_no=1),
    radio_type="AWEUB",
    serial_number="AH211400486",
    product_code="475167A.102",
)

_airscale_gnb = Airscale(common_units=[gnb_common_unit_0], product_code="475765A")

_du_gnb = DU(
    airscale=_airscale_gnb,
    rus=[gnb_radio_unit_0, gnb_radio_unit_1],
    oam_ip=_gnb_oam_ip,
    f1_m_ip_addr=_gnb_f1m_ip,
    instance_id=_gnb_instance_id,
    global_bts_id=_gnb_global_bts_id,
)

_gnb = ClassicalBts(
    cu=_cu_gnb,
    dus=[_du_gnb],
    instance_id=_gnb_instance_id,
    global_bts_id=_gnb_global_bts_id,
)

_test_pc_gnb = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT4SK032.p04.ska-lab.nsn-rdnet.net",
        username="ute",
        password="uteUTE!",
    ),
    connections=[_gnb],
)

def _set_abstract_lib_config_env(ue_config_file):
    tl_config_dir = os.path.dirname(os.path.abspath(__file__))
    ue_config_abs_path = os.path.join(tl_config_dir, ue_config_file)
    with open(ue_config_abs_path) as ta_ue_config:
        ue_config = yaml.safe_load(ta_ue_config)
    os.environ["ABSTRACT_LIB_CONFIG"] = ue_config_abs_path
    return ue_config

# ------------------------TL_CONFIGURATION------------------------
_ue_config = _set_abstract_lib_config_env("ue_config.yaml")

tl = TestLine(
    test_pc=_test_pc_gnb,
    gnbs=[_gnb],
    pdus=[_gnb_pdu_1, _gnb_pdu_2],
    test_pcs=[_test_pc_gnb],
	tl_cloud_topology="CLOUD_5G_CLASSICAL_ASIBL_ABIAB1_ABILB2_AWEUB_AHFIB_MRAT",
)

__all__ = ["tl"]
