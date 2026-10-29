__maintainer__ = "Marzena Skolucka"
__team__ = "I_MN_5G_SC_PZ_SC_5G_VRF_GMS"
__email__ = "I_MN_5G_SC_PZ_SC_5G_VRF@internal.nsn.com"

import os, yaml
from taf.config.testline.testline import TestLine
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import (
    SshServiceDetails,
    OpenStackConnectionDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
)
from taf.config.testline.cloud_hosting import (
    ControlNode,
    NCIR,
    CloudDeployment,
    DeploymentFlavorStack,
    DeploymentNetworkStack,
    DeploymentVnfStack,
    ComputeNode,
)
from taf.config.testline import RealEnb, Enb
from taf.config.testline.gnb import CloudBts, CU
from taf.config.testline import DU, RU
from taf.config.testline.gnb.networkaddress import NetworkAddress

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))


def _set_abstract_lib_config_env(ue_config_file):
    tl_config_dir = os.path.dirname(os.path.abspath(__file__))
    ue_config_abs_path = os.path.join(tl_config_dir, ue_config_file)

    with open(ue_config_abs_path) as ta_ue_config:
        ue_config = yaml.safe_load(ta_ue_config)

    os.environ["ABSTRACT_LIB_CONFIG"] = ue_config_abs_path

    return ue_config


# The most commonly used testline configuration. #
_test_pc_gnb_default_ssh_connection_details = SshServiceDetails(
    addr="7-7-UTE5GCLOUDT427.sc5g.krk-lab.nsn-rdnet.net'",
    username="ute",
    password="ute",
)

_test_pc_enb_default_ssh_connection_details = SshServiceDetails(
    addr="sc5g-enb-020.sc5g.krk-lab.nsn-rdnet.net", username="ute", password="ute"
)

_gnb_oam_ip = "2a00:8a02:60:1c::1:427"
_gnb_instance_id = 76008
_gnb_global_bts_id = 76008
_gnb_du_common_unit_hardwarde_type = "ASIK"
_gnb_ru_ip = NetworkAddress(v4="192.168.254.34")
_gnb_ru_hw_group = "AEWF"


##############################################################

# Default values
_default_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
)

_default_oam_http_connection = HttpConnectionDetails(
    addr=_gnb_oam_ip,
    username="Nemuadmin",
    password="nemuuser",
)

##############################################################


# Important!: check and change below if other than default #

# Test PCs
_test_pc_gnb = TestPc(
    default_ssh_connection_details=_test_pc_gnb_default_ssh_connection_details
)
_test_pc_enb = TestPc(
    default_ssh_connection_details=_test_pc_enb_default_ssh_connection_details
)

# gNB section

_cu = CU(
    backhaul_site_oam_ip=_gnb_oam_ip,
    oam_ssh_connection_details=SshServiceDetails(
        addr="2a00:8a02:60:1c::1:427", username="robot", password="rastre1"
    ),
    oam_http_connection_details=_default_oam_http_connection,
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")
_capacity_unit_2 = CapacityUnit(addr="192.168.253.20")

_common_unit = CommonUnit(
    _default_ssh_lmp_connection,
    capacity_units=[_capacity_unit, _capacity_unit_2],
)

_ru_gnb = RU(
    ru_hw_group=_gnb_ru_hw_group,
    default_ssh_connection_details=SshServiceDetails(
        addr=_gnb_ru_ip.v4,
        username="root",
        password="umniedziala",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="root", password="umniedziala"
    ),
)

_airscale = Airscale([_common_unit])

_compute = ComputeNode(
    bmc_connection_details=BmcConnectionDetails(
        addr="10.44.196.175", username="admin", password="admin"
    )
)
_control_0 = ControlNode(
    open_stack_connection_details=OpenStackConnectionDetails(
        ip_addr="10.83.245.1",
        username="admin",
        tenant="admin",
        password="uteadmin",
        protocol="https",
    ),
    default_ssh_connection_details=SshServiceDetails(
        addr="10.83.245.1", username="wrsroot", password="uteadmin"
    ),
    bmc_connection_details=BmcConnectionDetails(
        addr="1.1.1.1", username="admin", password="admin"
    ),
)
_ncir = NCIR(compute_nodes=[_compute], control_nodes=[_control_0], version="ncir_19")

_cbts_flavor = DeploymentFlavorStack(
    name="TL_7_7_CLOUDT427_FLAVOR",
    env_files=[os.path.join(_CFG_DIR, "5gbts_flavor.env")],
    yaml_file=os.path.join(_CFG_DIR, ""),
    default_vnf_prefix="5gbts-427",
)

_cbts_net = DeploymentNetworkStack(
    name="TL_7_7_CLOUDT427_EXT_NET",
    env_files=[os.path.join(_CFG_DIR, "5gbts_ext_net.env")],
    yaml_file=os.path.join(_CFG_DIR, ""),
)

_cbts_vnf = DeploymentVnfStack(
    name="TL_7_7_CLOUDT427_BTS",
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

_du = DU(
    airscale=_airscale,
    rus=[_ru_gnb],
    f1_c_ip_addr="2a00:2222:2222:2222:2222:2222:2222:61",
    f1_u_ip_addr="2a00:2222:2222:2222:2222:2222:2222:62",
    f1_m_ip_addr="2a00:2222:2222:2222:2222:2222:2222:60",
)

_cbts = CloudBts(
    cu=_cu,
    dus=[_du],
    cloud_deployment=_cloud_deployment,
    vnf_name="5gbts-427",
    instance_id=76008,
    global_bts_id=76008,
)
_lteenb = RealEnb(
    airscale=_du, x2_link_addr=NetworkAddress(v4="2a00:8a02:60:1c::1:427")
)

_ue_config = _set_abstract_lib_config_env("ue_config.yaml")

# Testline

tl = TestLine(
    test_pc=_test_pc_gnb,
    gnbs=[_cbts],
    enbs=[_lteenb],
    cloud_hostings=[_ncir],
    tl_cloud_topology="CLOUD_5G_QC_ASIKR_ABILB4B5_AEWF",
)

__all__ = ["tl"]
