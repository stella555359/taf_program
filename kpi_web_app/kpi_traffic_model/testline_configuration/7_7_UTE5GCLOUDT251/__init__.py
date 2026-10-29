__maintainer__ = "Andrzej Pencak"
__team__ = "5G_PZ_MMW_KRK_6_SG"
__email__ = "andrzej.pencak@nokia.com"

import os
import yaml
from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
)
from taf.config.testline import NetworkAddress, RU
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.pdu import PduPort, ATEN, FPFH
from taf.config.testline.testline import TestLine


def _set_abstract_lib_config_env(ue_config_file):
    tl_config_dir = os.path.dirname(os.path.abspath(__file__))
    ue_config_abs_path = os.path.join(tl_config_dir, ue_config_file)

    with open(ue_config_abs_path) as ta_ue_config:
        ue_config = yaml.safe_load(ta_ue_config)
    os.environ["ABSTRACT_LIB_CONFIG"] = ue_config_abs_path

    return ue_config


_ue_config = _set_abstract_lib_config_env("ue_plugin_android.yaml")

# Test PCs configuration (VMs)
_test_pc_gnb_1_default_ssh_connection_details = SshServiceDetails(
    addr="7-7-UTE5GCLOUDT251.sc5g.krk-lab.nsn-rdnet.net", username="ute", password="ute"
)

# gNBs configuration
_gnb_1_bc_ip = NetworkAddress(v4="10.83.183.1")

_default_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
)

_default_gnb_1_oam_http_connection = HttpConnectionDetails(
    addr=_gnb_1_bc_ip.v4,
    username="Nemuadmin",
    password="nemuuser",
    port=443,
)

# CUs
_cu_gnb_1 = CU(
    backhaul_site_oam_ip=_gnb_1_bc_ip,
    oam_ssh_connection_details=_default_ssh_lmp_connection,
    oam_http_connection_details=_default_gnb_1_oam_http_connection,
)

# DUs
_du_lmp_connection_gnb_1 = _default_ssh_lmp_connection
_du_lmp_connection_gnb_1.proxy = _test_pc_gnb_1_default_ssh_connection_details

_abil_master_gnb = CapacityUnit(addr="fsp1_c",
                                hardware_type="ABIP")

_gnb_pdu = FPFH(
    port_numbers=[4],
    addr="fpfh-ga17-1.sc5g-leg.krk-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

_pdus = [_gnb_pdu]

_du_common_unit_gnb_1 = CommonUnit(
    pdu_port=_gnb_pdu.pdu_ports[4],
    lmp_connection=_du_lmp_connection_gnb_1,
    capacity_units=[_abil_master_gnb],
    hardware_type="ASIM",
    hardware_version="Y13",
)

_test_pc_gnb_main = TestPc(
    default_ssh_connection_details=_test_pc_gnb_1_default_ssh_connection_details,
    connections=[_du_common_unit_gnb_1],
)

_ru_gnb_1 = RU(
    ru_hw_group="RF5.1",
    default_ssh_connection_details=SshServiceDetails(
        addr=NetworkAddress(v4="172.16.19.33").v4,
        username="root",
        password="asmr",
    ),
    pdu_port=PduPort(
        pdu=FPFH(
            addr="10.253.166.111", port_numbers=[1, 2], login="admin", password="admin"
        ),
        port_no=3,
    ),
    radio_type="AHFII",
    serial_number="",
)

_airscale_gnb_1 = Airscale(common_units=[_du_common_unit_gnb_1])

_du_gnb_1 = DU(airscale=_airscale_gnb_1, rus=[_ru_gnb_1])


# gNBs configuration
main_gnb = ClassicalBts(
    cu=_cu_gnb_1,
    dus=[_du_gnb_1],
    instance_id="75251",
    global_bts_id="75251",
)

# TL configuration
tl = TestLine(
    test_pc=_test_pc_gnb_main,
    gnbs=[main_gnb],
    test_pcs=[_test_pc_gnb_main],
    pdus=_pdus,
    tl_cloud_topology="CLOUD_5G_CLASSICAL_ANDROID_ASIM_ABIP_AHFII",
)


__all__ = ["tl"]
