__maintainer__ = "Venkata Rajesh"
__team__ = "I_MN_ECE_BLR_RD_UP_SQD_LAKSHYA "
__email__ = (
    "I_MN_ECE_BLR_RD_UP_SQD_LAKSHYA <I_MN_ECE_BLR_RD_UP_SQD_LAKSHYA@internal.nsn.com>"
)

import os

from taf.config.testline.cloud_hosting import (
    ControlNode,
    NCIR,
    CloudDeployment,
    DeploymentFlavorStack,
    DeploymentNetworkStack,
    DeploymentVnfStack,
    ComputeNode,
    OSP,
)
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.core import EPCSim, LTEEmuCore
from taf.config.testline import DU
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU
from taf.config.testline.airscale import Airscale, CommonUnit
from taf.config.testline.ue import Airphone, AirphoneCloud, Prisma, TM500
from taf.config.testline import Enb, SimEnb, RealEnb, RadioModule, LTEEmuEnb

_cfg_dir = os.path.dirname(os.path.abspath(__file__))
_control_0 = ControlNode(
    open_stack_connection_details=OpenStackConnectionDetails(
        ip_addr="10.41.169.74",
        username="wrsroot",
        tenant="wrsroot",
        password="Fiveg@123",
    ),
    default_ssh_connection_details=SshServiceDetails(
        addr="10.41.169.74", username="wrsroot", password="Fiveg@123"
    ),
    bmc_connection_details=BmcConnectionDetails(
        addr="10.41.169.74", username="wrsroot", password="Fiveg@123"
    ),
)

_ncir = NCIR(compute_nodes=[], control_nodes=[_control_0], version="ncir_17a")

_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="127.0.0.1", username="ute", password="ute"
    )
)

_epcsim = EPCSim(
    mme_ip="192.168.4.131",
    default_ssh_connection_details=SshServiceDetails(
        addr="10.41.169.78", username="ute", password="ute"
    ),
    dir_path="/home/ute/wts",
    cfg_filename="basic_wts_step2.cfg",
    mcc="311",
    mnc="489",
    tac="4",
)


_common_unit_0 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.2", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
)

# DU
_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale)  # If ru is not present then you do not have to add it here

_cbts_flavor = DeploymentFlavorStack(
    name="flavors",
    env_files=[os.path.join(_cfg_dir, "5gbts_flavor.env")],
    yaml_file=[os.path.join(_cfg_dir, "5gbts_flavor.yaml")],
    default_vnf_prefix="5gbts",
)

_cbts_net = DeploymentNetworkStack(
    name="extnet",
    env_files=[os.path.join(_cfg_dir, "5gbts_ext_net.env")],
    yaml_file=os.path.join(_cfg_dir, "5gbts_ext_net.yaml"),
)

_cbts_vnf = DeploymentVnfStack(
    name="CU_GNB",
    env_files=[os.path.join(_cfg_dir, "5gbts_heat.env")],
    yaml_file=os.path.join(_cfg_dir, "5gbts_heat.yaml"),
)

_cu = CU(
    backhaul_site_oam_ip="10.41.169.82",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.41.169.82", username="robot", password="rastre1"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.41.169.82", username="Nemuadmin", password="nemuuser", port=443
    ),
)

_cloud_deployment = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    flavors=[_cbts_flavor],
    networks=[_cbts_net],
    vnfs=[_cbts_vnf],
    cloud_hosting=_ncir,
)

_cbts = CloudBts(
    dus=[_du], cu=_cu, cloud_deployment=_cloud_deployment, vnf_name="5gbts"
)

_tl_cloud_topology = "CLOUD_5G_BB3"


########################Airphone################
_l3 = SshServiceDetails(addr="10.41.169.86", username="robot", password="rastre1")

_l2 = SshServiceDetails(addr="10.41.169.86", username="robot", password="rastre1")

_common_unit_1 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.2", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
)

_l1 = Airscale(common_units=[_common_unit_1])


_egate = SshServiceDetails(addr="0.0.0.0", username="user2", password="password2")

_airphone_cloud = AirphoneCloud(
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.41.169.87", username="robot", password="rastre1"
    ),
    oam_http_connection_details=HttpConnectionDetails(addr="10.41.169.87"),
)

_airphone = Airphone(
    egate=_egate,
    l3_ssh_connection_details=_l3,
    l2_ssh_connection_details=_l2,
    l1=_l1,
    airphone_cloud=_airphone_cloud,
)

_lteSim = LTEEmuEnb(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.41.169.78", username="ute", password="ute"
    ),
    dir_path="/home/ute/wts",
    cfg_filename="basic_wts_step2.cfg",
)


tl = TestLine(
    test_pc=_host,
    gnbs=[_cbts],
    cloud_hostings=[_ncir],
    core=_epcsim,
    enbs=[_lteSim],
    tl_cloud_topology=_tl_cloud_topology,
    ues=[_airphone],
)

__all__ = ["tl"]
