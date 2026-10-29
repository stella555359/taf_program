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
from taf.config.testline.enb import RealEnb
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.pdu import PduPort, ATEN, FPFH
from taf.config.testline.testline import TestLine
from taf.config.testline.connection_details import IperfDataTransferDetails


# Test PCs configuration (VMs)
_test_pc_gnb_1_default_ssh_connection_details = SshServiceDetails(
    addr="7-7-UTE5GCLOUDT266.sc5g.krk-lab.nsn-rdnet.net", username="ute", password="ute"
)

_test_pc_gnb_main = TestPc(
    default_ssh_connection_details=_test_pc_gnb_1_default_ssh_connection_details
)


# gNBs configuration
_gnb_1_bc_ip = NetworkAddress(v4="10.83.183.16/23")

_default_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
)

_default_gnb_1_oam_http_connection = HttpConnectionDetails(
    addr="10.83.183.16",
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
                                hardware_type="ABIO")

_gnb_pdu = FPFH(
    port_numbers=[1],
    addr="fpfh-ga16-24-sc5g.sc5g-leg.krk-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

_du_common_unit_gnb_1 = CommonUnit(
    pdu_port=_gnb_pdu.pdu_ports[1],
    lmp_connection=_du_lmp_connection_gnb_1,
    capacity_units=[_abil_master_gnb],
    hardware_type="ASIB",
    hardware_version="102",
)

_ru_gnb_1 = RU(
    ru_hw_group="RF5.1",
    default_ssh_connection_details=SshServiceDetails(
        addr=NetworkAddress(v4="172.16.19.33").v4,
        username="root",
        password="asmr",
    ),
    pdu_port=PduPort(
        pdu=FPFH(addr="FPFH-GA16-48-SC5G.sc5g-leg.krk-lab.nsn-rdnet.net", port_numbers=[1, 2],login="admin", password="admin"), port_no=3
    ),
)

_airscale_gnb_1 = Airscale(common_units=[_du_common_unit_gnb_1])

_du_gnb_1 = DU(airscale=_airscale_gnb_1, rus=[_ru_gnb_1])


# gNBs configuration
_gnb_main = ClassicalBts(
    cu=_cu_gnb_1,
    dus=[_du_gnb_1],
    instance_id="75266",
    global_bts_id="75266",
)

_enb_0 = RealEnb(
    system_module=_airscale_gnb_1,
    oam_ip=NetworkAddress(v4="10.83.183.16"),
    instance_id=75266,
    global_bts_id=78266,
    x2_link_addr=NetworkAddress(v4="10.83.253.16"),
)

# UE configuration
_ue_pc_ssh = SshServiceDetails("10.83.178.5", "user-lab0", password="Bts2003")
_iperf_details_on_mtk = IperfDataTransferDetails(
    ssh_connection_details=_ue_pc_ssh,
    network_interface_address="",
    iperf_path="",
    port=52029,
)


def _set_abstract_lib_config_env(ue_config_file):
    tl_config_dir = os.path.dirname(os.path.abspath(__file__))
    ue_config_abs_path = os.path.join(tl_config_dir, ue_config_file)

    with open(ue_config_abs_path) as ta_ue_config:
        ue_config = yaml.safe_load(ta_ue_config)

    os.environ["ABSTRACT_LIB_CONFIG"] = ue_config_abs_path

    return ue_config


_ue_config = _set_abstract_lib_config_env("ue.yaml")


# TL configuration
tl = TestLine(
    test_pc=_test_pc_gnb_main,
    gnbs=[_gnb_main],
    enbs=[_enb_0],
    test_pcs=[_test_pc_gnb_main],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_ANDROID_ASIBL_ABIOB1_AHEGC_AHFIB_AHFII",
)


__all__ = ["tl"]
