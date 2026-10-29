__maintainer__ = "Sara Nowak"
__team__ = "5G_PZ_MMW_KRK_6_SG"
__email__ = "sara.nowak@nokia.com"

import os
import yaml
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
)
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline import NetworkAddress, RoutingInformation, RU
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.pdu import FPFH, PduPort, ATEN
from taf.config.testline.enb import RealEnb


def _set_abstract_lib_config_env(ue_config_file):
    tl_config_dir = os.path.dirname(os.path.abspath(__file__))
    ue_config_abs_path = os.path.join(tl_config_dir, ue_config_file)

    with open(ue_config_abs_path) as ta_ue_config:
        ue_config = yaml.safe_load(ta_ue_config)
    os.environ["ABSTRACT_LIB_CONFIG"] = ue_config_abs_path

    return ue_config


_test_pc_gnb_default_ssh_connection_details = SshServiceDetails(
    addr="7-7-UTE5GCLOUDT312.sc5g.krk-lab.nsn-rdnet.net", username="ute", password="ute"
)


_test_pc_enb_default_ssh_connection_details = SshServiceDetails(
    addr="7-7-UTE5GCLOUDT068.sc5g.krk-lab.nsn-rdnet.net", username="ute", password="ute"
)

_gnb_oam_ip = NetworkAddress(
    v4="10.83.183.62/23",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=503,
)

_gnb_instance_id = 75312
_gnb_global_bts_id = 75312
_gnb_du_common_unit_hardwarde_type = "ASIB"
_gnb_ru_ip = NetworkAddress(v4="172.16.73.128")
_gnb_ru2_ip = NetworkAddress(v4="172.16.73.130")
_gnb_ru3_ip = NetworkAddress(v4="172.16.73.129")


_default_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
)

_default_oam_http_connection = HttpConnectionDetails(
    addr=_gnb_oam_ip.v4, username="Nemuadmin", password="nemuuser", port=443
)

_pdu1 = FPFH(
    addr="fpfh-ba08-48-sc5g.sc5g-leg.krk-lab.nsn-rdnet.net",
    port_numbers=["1"],
    login="admin",
    password="admin",
)

_pdus = [_pdu1]
# port 1 ASIB
_pdu_port = PduPort(pdu=_pdu1, port_no=1)

_test_pc_gnb = TestPc(
    default_ssh_connection_details=_test_pc_gnb_default_ssh_connection_details
)

_cu_gnb = CU(
    backhaul_site_oam_ip=_gnb_oam_ip,
    x2c=_gnb_oam_ip,
    x2u=_gnb_oam_ip,
    s1u=_gnb_oam_ip,
    oam_ssh_connection_details=_default_ssh_lmp_connection,
    oam_http_connection_details=_default_oam_http_connection,
)

_du_lmp_connection_gnb = _default_ssh_lmp_connection
_du_lmp_connection_gnb.proxy = _test_pc_gnb_default_ssh_connection_details

_abil_master_gnb = CapacityUnit(
    addr="192.168.253.22", hardware_type="ABIL", hardware_version=""  # fsp1_c
)

_du_common_unit_gnb = CommonUnit(
    lmp_connection=_du_lmp_connection_gnb,
    capacity_units=[_abil_master_gnb],
    hardware_type=_gnb_du_common_unit_hardwarde_type,
    hardware_version="A.102",
)

_default_ssh_lmp_connection_enb = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT068.sc5g.krk-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    ),
)

_du_lmp_connection_enb = _default_ssh_lmp_connection_enb
_du_lmp_connection_enb.proxy = _test_pc_enb_default_ssh_connection_details
_capacity_units_enb = [CapacityUnit(addr="192.168.253.20", hardware_type="FSMF")]


_common_unit_enb = CommonUnit(
    lmp_connection=_du_lmp_connection_enb,
    capacity_units=[_capacity_units_enb],
    hardware_type="FSMF",
)

_airscale_enb = Airscale(common_units=[_common_unit_enb])

_bts_enb_0 = RealEnb(
    system_module=_airscale_enb,
    instance_id=75312,
    global_bts_id=75312,
    oam_ip=NetworkAddress(
        v4="10.83.182.68",
        routing_v4=RoutingInformation(gateway="10.84.165.254"),
    ),
    x2_link_addr=NetworkAddress(v4="10.83.182.68"),
)

pdu_port = (
    PduPort(
        pdu=ATEN(
            addr="fpfh-ba08-48-sc5g.sc5g-leg.krk-lab.nsn-rdnet.net",
            port_numbers=[2, 3, 4],
        ),
        port_no=1,
    ),
)

gnb_ru_0 = RU(
    ru_hw_group="AHHB",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.73.128", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    radio_type="AHHB",
    serial_number="EA214554326",
)

gnb_ru_1 = RU(
    ru_hw_group="AHHB",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.73.130", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    radio_type="AHHB",
    serial_number="EA214554119",
)

gnb_ru_2 = RU(
    ru_hw_group="AHHB",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.73.129", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    radio_type="AHHB",
    serial_number="EA214554120",
)

_test_pc_gnb_main = TestPc(
    default_ssh_connection_details=_test_pc_gnb_default_ssh_connection_details,
    connections=[_du_common_unit_gnb],
)
_test_pc_enb_0 = TestPc(
    default_ssh_connection_details=_test_pc_enb_default_ssh_connection_details,
    connections=[_bts_enb_0],
)

_airscale_gnb = Airscale(common_units=[_du_common_unit_gnb])

_du_gnb = DU(
    airscale=_airscale_gnb,
    rus=[gnb_ru_0, gnb_ru_1, gnb_ru_2],
    f1_m_ip_addr="10.83.183.62",
)

_gnb_main = ClassicalBts(
    cu=_cu_gnb,
    dus=[_du_gnb],
    instance_id=_gnb_instance_id,
    global_bts_id=_gnb_global_bts_id,
)

_ue_config = _set_abstract_lib_config_env("ue.yaml")

tl = TestLine(
    gnbs=[_gnb_main],
    enbs=[_bts_enb_0],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_QC_ASIBR_ABILB1_3xAHHB_ENB",
    test_pcs=[_test_pc_gnb_main, _test_pc_enb_0],
    test_pc=_test_pc_gnb_main,
    pdus=_pdus,
)

__all__ = ["tl"]
