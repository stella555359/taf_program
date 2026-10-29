__maintainer__ = "I_MN_5GSC_KRK_AUTO"
__team__ = "I_MN_5GSC_KRK_AUTO"
__email__ = "I_MN_5GSC_KRK_AUTO@internal.nsn.com"

from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.ue import Android
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline import NetworkAddress, RoutingInformation, RU
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.pdu import PduPort, SWH, FPFH, ATEN
from taf.config.testline.nms import NMS, NOM
import os
import yaml


def _set_abstract_lib_config_env(ue_config_file):
    tl_config_dir = os.path.dirname(os.path.abspath(__file__))
    ue_config_abs_path = os.path.join(tl_config_dir, ue_config_file)

    with open(ue_config_abs_path) as ta_ue_config:
        ue_config = yaml.safe_load(ta_ue_config)
    os.environ["ABSTRACT_LIB_CONFIG"] = ue_config_abs_path

    return ue_config


# The most commonly used testline configuration. #
_test_pc_gnb_default_ssh_connection_details = SshServiceDetails(
    addr="7-7-UTE5GCLOUDT109.sc5g.krk-lab.nsn-rdnet.net",
    username="ute",
    password="ute",
)

_gnb_oam_ip = NetworkAddress(
    v4="10.83.182.109/23",
    routing_v4=RoutingInformation(gateway="10.83.182.254"),
)
_gnb_instance_id = 75109
_gnb_global_bts_id = 75109
_gnb_du_common_unit_hardwarde_type = "ASIK"
_gnb_ru0_ip = NetworkAddress(v4="172.16.73.128")
_gnb_ru_hw_group = "AZQG"

##############################################################

# Default values
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


# Important!: check and change below if other than default #

# Test PCs
_test_pc_gnb = TestPc(
    default_ssh_connection_details=_test_pc_gnb_default_ssh_connection_details
)

# gNB section

_cu_gnb = CU(
    backhaul_site_oam_ip=_gnb_oam_ip,
    x2c=_gnb_oam_ip,
    x2u=_gnb_oam_ip,
    s1u=_gnb_oam_ip,
    oam_ssh_connection_details=_default_ssh_lmp_connection,  # replace if other than default
    oam_http_connection_details=_default_oam_http_connection,
)  # replace if other than default

_du_lmp_connection_gnb = _default_ssh_lmp_connection
_du_lmp_connection_gnb.proxy = _test_pc_gnb_default_ssh_connection_details

_abio_master_gnb = CapacityUnit(addr="fsp1_c")  # 192.168.253.20

_du_common_unit_gnb = CommonUnit(
    lmp_connection=_du_lmp_connection_gnb,
    capacity_units=[_abio_master_gnb],
    hardware_type=_gnb_du_common_unit_hardwarde_type,
    hardware_version="102",
)

_ru_0_gnb = RU(
    ru_hw_group=_gnb_ru_hw_group,
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
    ),
)

_airscale_gnb = Airscale(common_units=[_du_common_unit_gnb])

_du_gnb = DU(
    airscale=_airscale_gnb,
    rus=[_ru_0_gnb],
    f1_m_ip_addr="10.83.182.109",
)

_gnb = ClassicalBts(
    cu=_cu_gnb,
    dus=[_du_gnb],
    instance_id=_gnb_instance_id,
    global_bts_id=_gnb_global_bts_id,
)

##############################################################

# _ue_config = _set_abstract_lib_config_env("ue_config.yaml")

_ue_pc_ssh = SshServiceDetails(
    addr="10.83.177.231", username="user-lab0", password="Bts2003"
)

_appserver_ssh = SshServiceDetails(
    addr="10.83.249.130",
    username="5g",
    password="5g",
)
_android_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.83.249.189",
    iperf_path="/data/user/0/com.nokia.syve.uemanager.mobile/",
)
_android_ue = Android(
    ssh_connection_details=_ue_pc_ssh,
    serial_number="f3a45026",
    server_dir="C:/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    dmc_path="C:/Users/user-lab0/adam.dmc",
    diag_com="COM31",
    iperf_details=_android_iperf,
    capabilities=["REAL_ANDROID_UE", "REAL_UE"],
)

_nms = NMS(
    addr="nie_wiem_jaki",
    nom=NOM(
        https_user_mgmt_info=HttpConnectionDetails(
            addr="https://user-mgmt.srncnms05.srnblr.nsn-rdnet.net",
            username="cnms01",
            password="Qwer_1234",
        ),
        https_rest_info=HttpConnectionDetails(
            addr="https://apigw.srncnms05.srnblr.nsn-rdnet.net",
            username="neonetics",
            password="Nokia_150",
        ),
    ),
)

# Testline

tl = TestLine(
    test_pc=_test_pc_gnb,
    gnbs=[_gnb],
    nms=_nms,
    ues=[_android_ue],
    test_pcs=[_test_pc_gnb],
    tl_cloud_topology="test",
)

__all__ = ["tl"]
