__maintainer__ = "Sara Nowak"
__team__ = "I_MN_5GSC_KRK_AUTO"
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


def _set_abstract_lib_config_env(ue_config_file):
    tl_config_dir = os.path.dirname(os.path.abspath(__file__))
    ue_config_abs_path = os.path.join(tl_config_dir, ue_config_file)

    with open(ue_config_abs_path) as ta_ue_config:
        ue_config = yaml.safe_load(ta_ue_config)
    os.environ["ABSTRACT_LIB_CONFIG"] = ue_config_abs_path

    return ue_config


_test_pc_gnb_default_ssh_connection_details = SshServiceDetails(
    addr="7-7-UTE5GCLOUDT302.sc5g.krk-lab.nsn-rdnet.net", username="ute", password="ute"
)

_gnb_oam_ip = NetworkAddress(
    v4="192.168.255.129",
    routing=RoutingInformation(gateway="192.168.255.126", ip_prefix_length=23),
)
_gnb_instance_id = 75302
_gnb_global_bts_id = 75302
_gnb_du_common_unit_hardwarde_type = "ASIB"
_gnb_ru_ip = NetworkAddress(v4="192.168.254.49")
_gnb_ru_hw_group = "AHLOA"


_default_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
)

_default_oam_http_connection = HttpConnectionDetails(
    addr=_gnb_oam_ip.v4,
    username="Nemuadmin",
    password="nemuuser",
)

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

_abio_master_gnb = CapacityUnit(addr="fsp1_c")

_du_common_unit_gnb = CommonUnit(
    lmp_connection=_du_lmp_connection_gnb,
    capacity_units=[_abio_master_gnb],
    hardware_type=_gnb_du_common_unit_hardwarde_type,
    hardware_version="M02",
)

_ru_gnb = RU(
    ru_hw_group=_gnb_ru_hw_group,
    default_ssh_connection_details=SshServiceDetails(
        addr=_gnb_ru_ip.v4,
        username="root",
        password="w@=EIj7P6R0bVy85OjCVa^ho&8",
    ),
)

_airscale_gnb = Airscale(common_units=[_du_common_unit_gnb])

_du_gnb = DU(airscale=_airscale_gnb, rus=[_ru_gnb], f1_m_ip_addr="10.83.183.52")

_gnb = ClassicalBts(
    cu=_cu_gnb,
    dus=[_du_gnb],
    instance_id=_gnb_instance_id,
    global_bts_id=_gnb_global_bts_id,
)

_ue_config = _set_abstract_lib_config_env("ue_plugin_android.yaml")

tl = TestLine(
    test_pc=_test_pc_gnb,
    gnbs=[_gnb],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_ASIBL_ABIOB1_2xAHLOA_eCPRI",
)

__all__ = ["tl"]
