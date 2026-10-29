######################################
#  TestLine Cloud TL2 HZ                   #
######################################
__maintainer__ = "Mao, Cathy"
__team__ = "NSB MN ECE RD 2 CN 06 SG"
__email__ = "cathy.mao@nokia-sbell.com"
import os
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
)
from taf.config.testline.gnb import CloudBts, CU, DU
from taf.config.testline.core import LTEEmuCore
from taf.config.testline.ue import Airphone
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit

# from taf.compatibility.configuration import TestlineWrapper
# from taf.config.cbts import create_configuration_data, CbtsProvider

# from taf.config.testline.legacy import (CONFIG_5G, AirPhone, Control, Host, Lteemu, SCF, EPCSim, RF, Pdu)
from taf.config.testline.legacy import SCF


_CFG_DIR = os.path.dirname(os.path.abspath(__file__))
CFG_DIR = _CFG_DIR

#########Testpc##########
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.212.88", username="ute", password="ute"
    )
)

#########NCIR##########
_control_0 = ControlNode(
    open_stack_connection_details=OpenStackConnectionDetails(
        ip_addr="10.57.138.18",
        username="TL401",
        tenant="CI-TestLine2",
        password="Ncir123!",
    ),
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.138.18", username="TL401", password="Ncir123!"
    ),
    bmc_connection_details=BmcConnectionDetails(addr="", username="", password=""),
)

_ncir = NCIR(compute_nodes=[], control_nodes=[_control_0], version="ncir_19")

flavor_env_files = [os.path.join(_CFG_DIR, "config_flavor.env")]
# flavor_config = create_configuration_data(flavor_env_files)

net_env_files = [os.path.join(_CFG_DIR, "config_ext_net.env")]
# net_config = create_configuration_data(net_env_files)

vnf_env_files = [os.path.join(_CFG_DIR, "config_bts.env")]
# vnf_config = create_configuration_data(vnf_env_files)

_cbts_flavor = DeploymentFlavorStack(
    name="tl401-Flavors",
    env_files=[os.path.join(_CFG_DIR, "config_flavor.env")],
    yaml_file=os.path.join(_CFG_DIR, "5gbts_flavor.yaml"),
    # configuration_data=flavor_config,
    default_vnf_prefix="tl401",
)

_cbts_net = DeploymentNetworkStack(
    name="tl401-Networks",
    env_files=[os.path.join(_CFG_DIR, "config_ext_net.env")],
    # configuration_data=net_config,
    yaml_file=os.path.join(_CFG_DIR, "5gbts_ext_net.yaml"),
)

_cbts_vnf = DeploymentVnfStack(
    name="tl401-Stack",
    env_files=[os.path.join(_CFG_DIR, "config_bts.env")],
    # configuration_data=vnf_config,
    yaml_file=os.path.join(_CFG_DIR, "5gbts_heat.yaml"),
)

_cloud_deployment = CloudDeployment(
    default_cfg_dir=_CFG_DIR,
    flavors=[_cbts_flavor],
    networks=[_cbts_net],
    vnfs=[_cbts_vnf],
    cloud_hosting=_ncir,
)
# ABIL
_capacity_unit = CapacityUnit(addr="192.168.253.22")

# ASIK
_common_unit = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.233.4", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_capacity_unit],
)

_airscale = Airscale(common_units=[_common_unit])
_du = DU(airscale=_airscale)

_cu = CU(
    backhaul_site_oam_ip="10.57.219.63",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.219.63", username="robot", password="rastre1"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.219.63", username="Nemuadmin", password="nemuuser"
    ),
)

_cbts = CloudBts(
    cu=_cu, dus=[_du], cloud_deployment=_cloud_deployment, vnf_name="ci-tl2"
)


#########LTEemuSim##########
_lteemu = LTEEmuCore(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.209.221", username="ute", password="ute"
    ),
    dir_path="/home/nokia/LTEemu_core2_64_3252",
    cfg_filename="basic_wts_step1.cfg",
    mme_ip="",
    edaemon_port="22222",
    egate_port="9880",
)

# TL specific values to be used in GNB scf file
_PARAMS_TO_MODIFY_SCF = [
    dict(value="Nokia 5G_HZ_ECE_TL2", dist_name="MRBTS-1900", p_name="btsName"),
    dict(value="172.16.1.130", dist_name="DU_f1Cplane", p_name="localIpAddr"),
    dict(value="172.16.1.132", dist_name="DU_f1Mplane", p_name="localIpAddr"),
    dict(value="172.16.1.131", dist_name="DU_f1Uplane", p_name="localIpAddr"),
    dict(
        value="38",
        dist_name="MRBTS-1900/NRBTS-1/NRCELL-1",
        p_name="prachConfigurationIndex",
    ),
]

_scf = SCF(
    project="5G19",
    name="SBTS5G19_5g_pid11_abil_l2rt.xml",
    scf_params=_PARAMS_TO_MODIFY_SCF,
)


# Testline
tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    cloud_hostings=[_ncir],
    core=_lteemu,
    tl_cloud_topology="CLOUD_5G_BB3_18A",
)
# tl = TestlineWrapper(tl)

tl.scf = _scf  # still a WA


# custom variables

Baseband = "ABIL"
airscaleNodeID = ["0x10", "0x12"]


__all__ = ["tl"]
