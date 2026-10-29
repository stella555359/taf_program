__maintainer__ = "Jakub Kupiec"
__team__ = "5G_PZ_MMW_KRK_4_SG"
__email__ = "jakub.kupiec@nokia.com"

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
from taf.config.testline import DU, RU
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline import NetworkAddress, RealEnb

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))


def _set_abstract_lib_config_env(ue_config_file):
    tl_config_dir = os.path.dirname(os.path.abspath(__file__))
    ue_config_abs_path = os.path.join(tl_config_dir, ue_config_file)

    with open(ue_config_abs_path) as ta_ue_config:
        ue_config = yaml.safe_load(ta_ue_config)
    os.environ["ABSTRACT_LIB_CONFIG"] = ue_config_abs_path

    return ue_config


_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT4SK020.p04.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_control_0 = ControlNode(
    open_stack_connection_details=OpenStackConnectionDetails(
        ip_addr="10.84.160.245",
        username="za91user1",
        tenant="ZA91tenant1",
        password="5Guser@7",
    ),
    default_ssh_connection_details=SshServiceDetails(
        addr="10.84.160.245", username="za91user1", password="5Guser@7"
    ),
    bmc_connection_details=BmcConnectionDetails(addr="", username="", password=""),
)

_compute = ComputeNode(
    bmc_connection_details=BmcConnectionDetails(addr="", username="", password="")
)

_ncir = NCIR(compute_nodes=[_compute], control_nodes=[_control_0], version="ncir_19")

_cbts_flavor = DeploymentFlavorStack(
    name="TL_7_7_UTE5GCLOUDTSK020_FLAVOR",
    env_files=[os.path.join(_CFG_DIR, "5gbts_flavor.env")],
    yaml_file=os.path.join(_CFG_DIR, "5gbts_flavor.yaml"),
    default_vnf_prefix="5gbts-20",
)

_cbts_net = DeploymentNetworkStack(
    name="TL_7_7_UTE5GCLOUDTSK020_EXT_NET",
    env_files=[os.path.join(_CFG_DIR, "5gbts_ext_net.env")],
    yaml_file=os.path.join(_CFG_DIR, "5gbts_ext_net.yaml"),
)

_cbts_vnf = DeploymentVnfStack(
    name="TL_7_7_UTE5GCLOUDTSK020_BTS",
    env_files=[os.path.join(_CFG_DIR, "5gbts_heat.env")],
    yaml_file=os.path.join(_CFG_DIR, "5gbts_heat.yaml"),
)

_cloud_deployment = CloudDeployment(
    default_cfg_dir=_CFG_DIR,
    flavors=[_cbts_flavor],
    networks=[_cbts_net],
    vnfs=[_cbts_vnf],
    cloud_hosting=_ncir,
)

_cu = CU(
    backhaul_site_oam_ip="10.84.144.17",  # '10.83.182.143',
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.84.144.17", username="robot", password="rastre1"  # '10.83.182.143',
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.84.144.17",  # '10.83.182.143',
        username="Nemuadmin",
        password="nemuuser",
    ),
    instance_id=77020,
    global_bts_id=1,
    f1u=NetworkAddress(v4="10.255.1.145"),
    s1u=NetworkAddress(v4="10.255.1.81"),
)

_abil1_du1 = CapacityUnit(addr="192.168.253.20")

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
    radio_type="AEUB",
)

_gnb_oam_ip = NetworkAddress(v4="10.84.190.20")

_du1 = DU(
    airscale=Airscale(common_units=[_asik_du1]),
    instance_id=77020,
    global_bts_id=77020,
    rus=[_ru_du1],
    oam_ip=_asik_du1.lmp_connection.addr,
    f1_m_ip_addr=_gnb_oam_ip.v4,
    f1_c_ip_addr=_gnb_oam_ip.v4,
    f1_u_ip_addr=_gnb_oam_ip.v4,
)

_cbts = CloudBts(
    cu=_cu, cloud_deployment=_cloud_deployment, vnf_name="5gbts-20", dus=[_du1]
)

_enb = RealEnb(
    oam_ip=NetworkAddress(v4="10.84.190.21"),
    instance_id=77021,
    global_bts_id=77021,
    x2_link_addr=NetworkAddress(v4="10.84.190.21"),
)

_ue_config = _set_abstract_lib_config_env("ue_config.yaml")

_vlans_config = {
    "511": "10.255.0.49",
    "512": "10.255.0.57",
    "513": "10.255.0.65",
    "514": "10.255.0.73",
}

tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    cloud_hostings=[_ncir],
    tl_cloud_topology="CLOUD_5G_QC_ASIKR_ABILB4_AEUB",
    enbs=[_enb],
    ues=[_ue_config],
    switches=[_vlans_config],
)

__all__ = ["tl"]
