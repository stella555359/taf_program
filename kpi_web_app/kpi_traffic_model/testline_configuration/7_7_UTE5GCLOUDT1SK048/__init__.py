__maintainer__ = "Olga Urbanska"
__team__ = "5G_PZ_MMW_KRK_6_SG"
__email__ = "olga.urbanska@nokia.com"

import os
import yaml
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.gnb import CU
from taf.config.testline import (
    DU,
    RU,
    RoutingInformation,
    ClassicalBts,
    AppServer,
)
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline import NetworkAddress, RealEnb
from taf.config.testline.core import RealCore, RealCore4GDetails, MME


_5g_bts_id = 76048
_4g_bts_id = 76252

_gnb_1_bc_ip = NetworkAddress(v4="10.84.164.48")

_4g_ip = NetworkAddress(v4="10.84.164.252")

_test_pc_gnb_1_default_ssh_connection_details = SshServiceDetails(
    addr="7-7-UTE5GCLOUDT1SK048-integration.p01.ska-lab.nsn-rdnet.net",
    username="ute",
    password="ute",
)

_test_pc = TestPc(
    default_ssh_connection_details=_test_pc_gnb_1_default_ssh_connection_details
)

_ssh = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_cu = CU(
    backhaul_site_oam_ip=_gnb_1_bc_ip,
    oam_ssh_connection_details=_ssh,
    oam_http_connection_details=HttpConnectionDetails(
        addr=_gnb_1_bc_ip.v4, username="Nemuadmin", password="nemuuser", port=443
    ),
    instance_id=_5g_bts_id,
    global_bts_id=_5g_bts_id,
)

_du_lmp_connection_gnb = _ssh
_du_lmp_connection_gnb.proxy = _test_pc_gnb_1_default_ssh_connection_details

_abia_du1 = CapacityUnit(addr="192.168.253.20")
_abil_du1 = CapacityUnit(addr="192.168.253.20")

_asil_du1 = CommonUnit(
    lmp_connection=_du_lmp_connection_gnb,
    capacity_units=[_abia_du1, _abil_du1, _abil_du1],
)

_aewd_1 = RU(
    ru_hw_group="",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.1.162", username="root"
    ),
    lmp_connection=SshServiceDetails(addr="", username=""),
    radio_type="AEWD",
)

_ahib = RU(
    ru_hw_group="",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.33.128", username="root"
    ),
    lmp_connection=SshServiceDetails(addr="", username=""),
    radio_type="AHIB",
)

_du1 = DU(
    Airscale(common_units=[_asil_du1]),
    rus=[_aewd_1, _ahib],
)

_gnb = ClassicalBts(
    cu=_cu,
    dus=[_du1],
    instance_id=_5g_bts_id,
    global_bts_id=_5g_bts_id,
)

_enb = RealEnb(
    oam_ip=_4g_ip,
    instance_id=_4g_bts_id,
    global_bts_id=_5g_bts_id,
)

_mme_dummy_ssh = SshServiceDetails(
    addr="1.1.1.1",
    username="dummy",
)

_core = RealCore(
    four_g=RealCore4GDetails(
        mme=MME(
            s1=NetworkAddress(v4="10.55.192.6"),
            oam_ssh_connection_details=_mme_dummy_ssh,
        )
    ),
    mcc=244,
    mnc=8,
)

_ue_pc_31 = SshServiceDetails(
    addr="plkr-wmp-ue31.intra.noklab.net",
    username="plkr-wmp-UE20+user-lab0",
    password="Bts2003",
)

_app_serv_iperf = IperfDataTransferDetails(
    ssh_connection_details=SshServiceDetails(
        addr="10.84.168.120", username="5g", password="5g"
    ),
    network_interface_address="10.84.169.60",
    iperf_path="/usr/bin/iperf",
)


_appserver = AppServer(iperf_details=_app_serv_iperf)


def _set_abstract_lib_config_env(ue_config_file):
    tl_config_dir = os.path.dirname(os.path.abspath(__file__))
    ue_config_abs_path = os.path.join(tl_config_dir, ue_config_file)

    with open(ue_config_abs_path) as ta_ue_config:
        ue_config = yaml.safe_load(ta_ue_config)

    os.environ["ABSTRACT_LIB_CONFIG"] = ue_config_abs_path

    return ue_config


_ue_yaml_config = _set_abstract_lib_config_env("ue.yaml")

tl = TestLine(
    tl_cloud_topology="CLOUD_5G_CLASSICAL_ANDROID_ASIL_ABIAB1_ABILB2_AEWD_AHIB",
    gnbs=[_gnb],
    enbs=[_enb],
    core=_core,
    test_pc=_test_pc,
    appserver=_appserver,
)

__all__ = ["tl"]
