__maintainer__ = "Micha Pudelko"
__team__ = "5G_PZ_MMW_KRK_6_SG"
__email__ = "michal.pudelko@nokia.com"

import os, yaml
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import (
    SshServiceDetails,
    OpenStackConnectionDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
)
from taf.config.testline.cloud_hosting import (
    NCIR,
    ControlNode,
    CloudDeployment,
    DeploymentFlavorStack,
    DeploymentNetworkStack,
    DeploymentVnfStack,
    ComputeNode,
)
from taf.config.testline.gnb import CloudBts, CU
from taf.config.testline import DU, RU, RoutingInformation
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline import NetworkAddress, RealEnb
from taf.config.testline.core import RealCore5G
from taf.config.testline.cbam import Cbam

_5g_bts_id = 75182
_4g_bts_id = 75079  # do poprawy

_ncir_vnf = "5gbts" + str(_5g_bts_id)

# SB00
_ncir_ip = "10.83.190.225"
_ncir_user = "5Guser1"
_ncir_pass = "5Guser@4"
_ncir_tenant = "5Gtenant1"

_cu_oam_ip = "10.83.250.2"
_4g_ip = NetworkAddress(v4="10.83.251.1")  # czy dobrze

_du_m_ip = NetworkAddress(
    v4="10.83.251.7",
    vlan_id=539,
    routing_v4=RoutingInformation(gateway="10.83.251.30", ip_prefix_length=27),
)
_du_f1c_ip = NetworkAddress(
    v4="10.83.250.199",
    vlan_id=537,
    routing_v4=RoutingInformation(gateway="10.83.250.222", ip_prefix_length=27),
)
_du_f1u_ip = NetworkAddress(
    v4="10.83.250.231",
    vlan_id=538,
    routing_v4=RoutingInformation(gateway="10.83.250.254", ip_prefix_length=27),
)

_du_m_route_cu = NetworkAddress(
    routing_v4=RoutingInformation(gateway="10.83.251.30", ip_prefix_length=27)
)
_du_f1c_route_cu = NetworkAddress(
    routing_v4=RoutingInformation(gateway="10.83.250.222", ip_prefix_length=27)
)
_du_f1u_route_cu = NetworkAddress(
    routing_v4=RoutingInformation(gateway="10.83.250.254", ip_prefix_length=27)
)

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT182.sc5g.krk-lab.nsn-rdnet.net",  # change
        username="ute",
        password="ute",
    )
)

_control_0 = ControlNode(
    open_stack_connection_details=OpenStackConnectionDetails(
        ip_addr=_ncir_ip,  # Nokia AirFrame Cloud Infrastructure
        username=_ncir_user,
        tenant=_ncir_tenant,
        password=_ncir_pass,
        protocol="https",
    ),
    default_ssh_connection_details=SshServiceDetails(
        addr=_ncir_ip,  # Nokia AirFrame Cloud Infrastructure
        username=_ncir_user,
        password=_ncir_pass,
    ),
    bmc_connection_details=BmcConnectionDetails(addr="", username="", password=""),
)

_compute = ComputeNode(
    bmc_connection_details=BmcConnectionDetails(addr="", username="", password="")
)

_ncir = NCIR(
    compute_nodes=[_compute], control_nodes=[_control_0], version="ncir_19"
)  # Nokia Cluod Infrastructure for Radio

_cbts_flavor = DeploymentFlavorStack(
    name="TL_7_7_UTE5GCLOUDT182_FLAVOR",
    env_files=[os.path.join(_CFG_DIR, "config_flavor.env")],
    default_vnf_prefix=_ncir_vnf,
)  # change

_cbts_net = DeploymentNetworkStack(
    name="TL_7_7_UTE5GCLOUDT182_EXT_NET_DUMMY",
    env_files=[os.path.join(_CFG_DIR, "config_ext_net_dummy.env")],
)

_cbts_vnf = DeploymentVnfStack(
    name="TL_7_7_UTE5GCLOUDT182_BTS",
    env_files=[os.path.join(_CFG_DIR, "config_bts.env")],
)

_cloud_deployment = CloudDeployment(
    default_cfg_dir=_CFG_DIR,
    flavors=[_cbts_flavor],
    networks=[_cbts_net],
    vnfs=[_cbts_vnf],
    cloud_hosting=_ncir,
)

_cu = CU(
    backhaul_site_oam_ip=_cu_oam_ip,
    oam_ssh_connection_details=SshServiceDetails(
        addr=_cu_oam_ip, username="robot", password="rastre1"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr=_cu_oam_ip, username="Nemuadmin", password="nemuuser"
    ),
    instance_id=_5g_bts_id,  # change
    global_bts_id=_5g_bts_id,
)

_abil1_du1 = CapacityUnit(addr="192.168.253.36")  # ??

_asik_du1 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_abil1_du1],
)

_ru_du1 = RU(
    ru_hw_group="",
    default_ssh_connection_details=SshServiceDetails(addr="", username=""),
    lmp_connection=SshServiceDetails(addr="", username=""),
    radio_type="AEUD",
)


_du1 = DU(
    Airscale(common_units=[_asik_du1]),
    instance_id=_5g_bts_id,  # change
    global_bts_id=_5g_bts_id,  # ??
    rus=[_ru_du1],
    oam_ip=_du_m_ip,
    f1_m_ip_addr=_du_m_ip,
    f1_c_ip_addr=_du_f1c_ip,
    f1_u_ip_addr=_du_f1u_ip,
    f1_m_cu=_du_m_route_cu,
    f1_c_cu=_du_f1c_route_cu,
    f1_u_cu=_du_f1u_route_cu,
)

_cbts = CloudBts(
    cu=_cu,
    cloud_deployment=_cloud_deployment,
    vnf_name=_ncir_vnf,  # change
    dus=[_du1],
)

_enb = RealEnb(
    oam_ip=_4g_ip,  # change DU WebEm SKA-039
    instance_id=_4g_bts_id,
    global_bts_id=_4g_bts_id,
    x2_link_addr=_4g_ip,  # change
)

_core = RealCore5G(mcc=244, mnc=8)
_cbam = Cbam(
    addr="10.83.182.251",
    client_id="cbam_client",
    client_secret="6373f4df-8f0b-4333-aa2a-7f2d72335d87",
)


def _set_abstract_lib_config_env(ue_config_file):
    tl_config_dir = os.path.dirname(os.path.abspath(__file__))
    ue_config_abs_path = os.path.join(tl_config_dir, ue_config_file)

    with open(ue_config_abs_path) as ta_ue_config:
        ue_config = yaml.safe_load(ta_ue_config)

    os.environ["ABSTRACT_LIB_CONFIG"] = ue_config_abs_path

    return ue_config


_ue_config = _set_abstract_lib_config_env("ue.yaml")

tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    cloud_hostings=[_ncir],
    tl_cloud_topology="CLOUD_5G_QC_ASOD_AEUD_ENB",  # ??
    enbs=[_enb],
    core=_core,
    cbam=_cbam,
)

__all__ = ["tl"]
