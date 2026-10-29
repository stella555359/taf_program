__maintainer__ = "Piotr Brzezicki"
__team__ = "5G_PZ_MMW_KRK_6_SG"
__email__ = "piotr.brzezicki@nokia.com"

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
    Android,
    AppServer,
)
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline import NetworkAddress, RealEnb
from taf.config.testline.core import RealCore, RealCore4GDetails, MME

_5g_bts_id = 77018
_4g_bts_id = 77019

_cu_m_ip = NetworkAddress(
    v4="10.84.190.18",
    vlan_id=504,
    routing_v4=RoutingInformation(gateway="10.84.19.254", ip_prefix_length=23),
)

_4g_ip = NetworkAddress(v4="10.84.190.19")

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT4SK018.p04.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_ssh = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_cu = CU(
    backhaul_site_oam_ip=_cu_m_ip,
    oam_ssh_connection_details=_ssh,
    oam_http_connection_details=HttpConnectionDetails(
        addr=_cu_m_ip.v4, username="Nemuadmin", password="nemuuser"
    ),
    instance_id=_5g_bts_id,
    global_bts_id=_5g_bts_id,
)

_abil1_du1 = CapacityUnit(addr="192.168.253.20")
_abil2_du1 = CapacityUnit(addr="192.168.253.24")


_asik_du1 = CommonUnit(
    lmp_connection=_ssh,
    capacity_units=[_abil1_du1, _abil2_du1],
)

_aweua = RU(
    ru_hw_group="",
    default_ssh_connection_details=SshServiceDetails(addr="", username=""),
    lmp_connection=SshServiceDetails(addr="", username=""),
    radio_type="AWEUA",
)

_du1 = DU(
    Airscale(common_units=[_asik_du1]),
    rus=[_aweua, _aweua],
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
    global_bts_id=_4g_bts_id,
    x2_link_addr=_4g_ip,
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

_ue_pc_27 = SshServiceDetails(
    addr="plkr-wmp-ue27.intra.noklab.net",
    username="PLKR-WMP-UE27+user-lab0",
    password="Bts2003",
)

_ue_pc_55 = SshServiceDetails(
    addr="plkr-wmp-ue55.intra.noklab.net",
    username="PLKR-WMP-UE55+user-lab0",
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

_pyro_server_dir = "C:/pyro_server"
_ue_pc_python_path = "C:/Python36/python.exe"

_qc_sdx60 = Android(
    ssh_connection_details=_ue_pc_55,
    serial_number="7445384d",
    server_dir=_pyro_server_dir,
    python_path=_ue_pc_python_path,
    iperf_details=_app_serv_iperf,
    capabilities=["QC_MTP_SDX60", "ANDROID_PLUGIN", "MTP"],
    is_rooted=True,
    network_mode_switch_method="adb",
    clear_server_files=True,
)

_samsung_s20 = Android(
    ssh_connection_details=_ue_pc_27,
    serial_number="R3CN90QJ3WX",
    server_dir=_pyro_server_dir,
    python_path=_ue_pc_python_path,
    iperf_details=_app_serv_iperf,
    capabilities=["SAMSUNG_S20", "ANDROID_PLUGIN", "COMMERCIAL"],
    is_rooted=False,
    network_mode_switch_method="adb",
    clear_server_files=True,
)


def _set_abstract_lib_config_env(ue_config_file):
    tl_config_dir = os.path.dirname(os.path.abspath(__file__))
    ue_config_abs_path = os.path.join(tl_config_dir, ue_config_file)

    with open(ue_config_abs_path) as ta_ue_config:
        ue_config = yaml.safe_load(ta_ue_config)

    os.environ["ABSTRACT_LIB_CONFIG"] = ue_config_abs_path

    return ue_config


_ue_yaml_config = _set_abstract_lib_config_env("ue.yaml")

tl = TestLine(
    tl_cloud_topology="CLOUD_5G_CLASSICAL_QC_ASIKL_ABILB1_AWEUA",
    gnbs=[_gnb],
    enbs=[_enb],
    core=_core,
    # ues=[_samsung_s20, _qc_sdx60],
    test_pc=_test_pc,
    appserver=_appserver,
)

__all__ = ["tl"]
