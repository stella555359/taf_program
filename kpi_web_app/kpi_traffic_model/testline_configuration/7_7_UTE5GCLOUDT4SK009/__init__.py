__maintainer__ = "Tomasz Romanowski"
__team__ = "5G_PZ_MMW_KRK_6_SG"
__email__ = "tomasz.1.romanowski.com"

import os
import yaml
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

_5g_bts_id = 77009
_4g_bts_id = 77011

_ncir_vnf = "5gbts" + str(_5g_bts_id)

# HD15
_ncir_ip = "10.84.160.245"
_ncir_user = "za91user1"
_ncir_pass = "5Guser@4"
_ncir_tenant = "ZA91tenant1"

_cu_oam_ip = NetworkAddress(
    v4="10.84.144.16/27", routing_v4=RoutingInformation(gateway="10.84.144.30")
)
_cu_f1c_ip = NetworkAddress(
    v4="10.255.1.112/27",
    routing_v4=RoutingInformation(gateway="10.255.1.126", destIpAddr="10.84.190.9/32"),
)
_cu_x2c_ip = NetworkAddress(
    v4="10.255.1.16/27",
    routing_v4=RoutingInformation(gateway="10.255.1.30", destIpAddr="10.84.190.11/32"),
)
_cu_f1u_ip = NetworkAddress(
    v4="10.255.1.144/27",
    routing_v4=RoutingInformation(gateway="10.255.1.158", destIpAddr="10.84.190.9/32"),
)
_cu_x2u_ip = NetworkAddress(
    v4="10.255.1.48/27",
    routing_v4=RoutingInformation(gateway="10.255.1.62", destIpAddr="10.84.190.11/32"),
)
_cu_s1u_ip = NetworkAddress(
    v4="10.255.1.80/27", routing_v4=RoutingInformation(gateway="10.255.1.94")
)

_du_ip = NetworkAddress(
    v4="10.84.190.9/23", routing_v4=RoutingInformation(gateway="10.84.191.254")
)

_4g_ip = NetworkAddress(v4="10.84.190.11")


_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

_control_0 = ControlNode(
    open_stack_connection_details=OpenStackConnectionDetails(
        ip_addr=_ncir_ip,
        username=_ncir_user,
        tenant=_ncir_tenant,
        password=_ncir_pass,
    ),
    default_ssh_connection_details=SshServiceDetails(
        addr=_ncir_ip, username=_ncir_user, password=_ncir_pass
    ),
    bmc_connection_details=BmcConnectionDetails(addr="", username="", password=""),
)

_compute = ComputeNode(
    bmc_connection_details=BmcConnectionDetails(addr="", username="", password="")
)

_ncir = NCIR(compute_nodes=[_compute], control_nodes=[_control_0], version="ncir_19")

_cbts_flavor = DeploymentFlavorStack(
    name="TL_7_7_UTE5GCLOUDT4SK009_FLAVOR",
    env_files=[os.path.join(_CFG_DIR, "config_flavor.env")],
    default_vnf_prefix=_ncir_vnf,
)

_cbts_net = DeploymentNetworkStack(
    name="TL_7_7_UTE5GCLOUDT4SK009_EXT_NET_DUMMY",
    env_files=[os.path.join(_CFG_DIR, "config_ext_net_dummy.env")],
)

_cbts_vnf = DeploymentVnfStack(
    name="TL_7_7_UTE5GCLOUDT4SK009_BTS",
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
        addr=_cu_oam_ip.v4.split("/")[0], username="robot", password="rastre1"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr=_cu_oam_ip.v4.split("/")[0], username="Nemuadmin", password="nemuuser"
    ),
    f1c=_cu_f1c_ip,
    x2c=_cu_x2c_ip,
    f1u=_cu_f1u_ip,
    x2u=_cu_x2u_ip,
    s1u=_cu_s1u_ip,
    instance_id=_5g_bts_id,
    global_bts_id=_5g_bts_id,
)


_gnb1_du_capu = CapacityUnit(addr="192.168.253.17")

_asod_du1 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_gnb1_du_capu],
)

_ru_du1 = RU(
    ru_hw_group="Gen4",
    default_ssh_connection_details=SshServiceDetails(addr="", username=""),
    lmp_connection=SshServiceDetails(addr="", username=""),
    radio_type="AEWD",
)

_du1 = DU(
    Airscale(common_units=[_asod_du1]),
    instance_id=_5g_bts_id,
    global_bts_id=_5g_bts_id,
    rus=[_ru_du1],
    oam_ip=_du_ip,
    f1_c_ip_addr=_du_ip,
    f1_u_ip_addr=_du_ip,
)

_cbts = CloudBts(
    cu=_cu, cloud_deployment=_cloud_deployment, vnf_name=_ncir_vnf, dus=[_du1]
)

_abia_enb = CapacityUnit(addr="192.168.253.20")

_asia_enb = Airscale(
    common_units=[
        CommonUnit(
            lmp_connection=SshServiceDetails(
                addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
            ),
            capacity_units=[_abia_enb],
        )
    ]
)

_enb = RealEnb(
    system_module=_asia_enb,
    oam_ip=_4g_ip,
    instance_id=_4g_bts_id,
    global_bts_id=_4g_bts_id,
    x2_link_addr=_4g_ip,
)


_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT4SK009.p04.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_test_pc_enb = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT4SK011.p04.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    ),
    connections=[_enb],
)

_core = RealCore5G(mcc=244, mnc=8)


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
    test_pcs=[_test_pc, _test_pc_enb],
    gnbs=[_cbts],
    cloud_hostings=[_ncir],
    tl_cloud_topology="CLOUD_5G_ASOD_AEWD_ENB",
    enbs=[_enb],
    core=_core,
)

__all__ = ["tl"]
