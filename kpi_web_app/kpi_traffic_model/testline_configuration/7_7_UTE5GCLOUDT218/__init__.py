__maintainer__ = "Joanna Wojtowicz"
__team__ = "5G_PZ_MMW_KRK_3_SG"
__email__ = "joanna.wojtowicz@nokia.com"

import os
import yaml
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
)
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline import RU
from taf.config.testline import NetworkAddress, RoutingInformation, RealEnb
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.pdu import FPFH


def _set_abstract_lib_config_env(ue_config_file):
    tl_config_dir = os.path.dirname(os.path.abspath(__file__))
    ue_config_abs_path = os.path.join(tl_config_dir, ue_config_file)

    with open(ue_config_abs_path) as ta_ue_config:
        ue_config = yaml.safe_load(ta_ue_config)
    os.environ["ABSTRACT_LIB_CONFIG"] = ue_config_abs_path

    return ue_config


_test_pc_gnb_default_ssh_connection_details = SshServiceDetails(
    addr="7-7-UTE5GCLOUDT218.sc5g.krk-lab.nsn-rdnet.net",
    username="ute",
    password="ute",
)

_test_pc_enb_default_ssh_connection_details = SshServiceDetails(
    addr="S7-7-UTE5GCLOUDT151.krk-lab.nsn-rdnet.net",
    username="ute",
    password="ute",
)

_gnb_pdu = FPFH(
    port_numbers=[6],
    addr="10.253.166.89",
    login="admin",
    password="admin",
)

_pdus = [_gnb_pdu]

_gnb_oam_ip = NetworkAddress(
    v4="10.83.183.32",
    vlan_id=503,
)

_ru_1 = RU(
    ru_hw_group="",
    radio_type="AEQB",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.73.128",
        username="root",
        password="umniedziala",
    ),
)
_ru_2 = RU(
    ru_hw_group="",
    radio_type="AEQB",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.73.129", username="root", password="umniedziala"
    ),
)

_ru_3 = RU(
    ru_hw_group="hw_group",
    radio_type="AEQB",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.73.130", username="root", password="umniedziala"
    ),
)

_gnb_instance_id = 75218
_gnb_global_bts_id = 75218
_gnb_du_common_unit_hardwarde_type = "ASIB"
_gnb_ru_hw_group = "AEQB"

##############################################################

_default_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
)
_default_oam_http_connection = HttpConnectionDetails(
    addr="192.168.255.129",
    username="Nemuadmin",
    password="nemuuser",
    port=443,
)

##############################################################


# Test PCs
_test_pc_gnb = TestPc(
    default_ssh_connection_details=_test_pc_gnb_default_ssh_connection_details
)
_test_pc_enb = TestPc(
    default_ssh_connection_details=_test_pc_enb_default_ssh_connection_details
)

# gNB section

_cu_gnb = CU(
    backhaul_site_oam_ip=_gnb_oam_ip,
    x2c=_gnb_oam_ip,
    oam_ssh_connection_details=_default_ssh_lmp_connection,  # replace if other than default
    oam_http_connection_details=_default_oam_http_connection,
)

_du_lmp_connection_gnb = _default_ssh_lmp_connection
_du_lmp_connection_gnb.proxy = _test_pc_gnb_default_ssh_connection_details

_abio_master_gnb = CapacityUnit(
    addr="192.168.253.22", hardware_type="ABIL", hardware_version=""  # fsp1_c
)
_abio_slave_gnb = CapacityUnit(
    addr="192.168.253.26", hardware_type="ABIO", hardware_version=""  # fsp2_c
)
_abio_loner_gnb = CapacityUnit(
    addr="192.168.253.30", hardware_type="ABIO", hardware_version=""  # fsp3_c
)

_du_common_unit_gnb = CommonUnit(
    lmp_connection=_du_lmp_connection_gnb,
    capacity_units=[_abio_master_gnb, _abio_slave_gnb, _abio_loner_gnb],
    hardware_type=_gnb_du_common_unit_hardwarde_type,
    hardware_version="A.103",
)


_airscale_gnb = Airscale(common_units=[_du_common_unit_gnb])

_du_gnb = DU(airscale=_airscale_gnb, rus=[_ru_1, _ru_2, _ru_3])

_gnb = ClassicalBts(
    cu=_cu_gnb,
    dus=[_du_gnb],
    instance_id=_gnb_instance_id,
    global_bts_id=_gnb_global_bts_id,
)

_enb = RealEnb(
    oam_ip=NetworkAddress(v6="10.83.182.151"),
    instance_id=75151,
    global_bts_id=75151,
    x2_link_addr=NetworkAddress(v6="10.83.182.151"),
)

##############################################################

_ue_config = _set_abstract_lib_config_env("ue.yaml")

# Testline

tl = TestLine(
    test_pc=_test_pc_gnb,
    gnbs=[_gnb],
    pdus=_pdus,
    test_pcs=[_test_pc_enb],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_ASIBL_ABIOB1_3xAEQB",
    enbs=[_enb],
)

__all__ = ["tl"]
