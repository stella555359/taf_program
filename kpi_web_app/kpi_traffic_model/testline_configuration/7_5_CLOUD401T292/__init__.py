import os
from taf.config.testline.cloud_hosting import (
    ControlNode,
    NCIR,
    CloudDeployment,
    DeploymentFlavorStack,
    DeploymentNetworkStack,
    DeploymentVnfStack,
)
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.core import EPCSim, LTEEmuCore, PrismaCore
from taf.config.testline import RU, DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import AirphoneCloud, Airphone, Prisma, TM500
from taf.config.testline import (
    Enb,
    SimEnb,
    RealEnb,
    RadioModule,
    LTEEmuEnb,
    PrismaEnb,
    DocomoEnb,
)
from taf.compatibility.configuration import TestlineWrapper

__maintainer__ = "He Jingmin"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_8_GMS <I_MN_5G_RAN_IV4_LINE_HZG_8@internal.nsn.com>"
)
__email__ = "jingmin.he@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

##host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.159.127", username="root", password="nokia123"
    )
)

_tl_cloud_topology = "CLOUD_5G_BB3"

_control = ControlNode(
    open_stack_connection_details=OpenStackConnectionDetails(
        ip_addr="10.57.137.36", username="sqg08", tenant="sqg08", password="nokia08"
    ),
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.137.36", username="sqg08", password="**Qpa8!"
    ),
    bmc_connection_details=BmcConnectionDetails(addr="", username="", password=""),
)

_cbts_flavor = DeploymentFlavorStack(
    name="sg8_flavor_j2he",
    env_files=[os.path.join(_cfg_dir, "config_flavor.env")],
    yaml_file=os.path.join(_cfg_dir, "5gbts_flavor.yaml"),
    default_vnf_prefix="sg8_flavor_j2he",
)
_cbts_vnf = DeploymentVnfStack(
    name="sg8_image_j2he",
    env_files=[os.path.join(_cfg_dir, "5gbts_heat.env")],
    yaml_file=os.path.join(_cfg_dir, "5gbts_heat.yaml"),
    configuration_data={"internal": 2566, "internal_srv": 2567, "internal_e1": 2568},
)
_cbts_net = DeploymentNetworkStack(
    name="sg8_net_j2he",
    env_files=[os.path.join(_cfg_dir, "5gbts_ext_net.env")],
    yaml_file=os.path.join(_cfg_dir, "5gbts_ext_net.yaml"),
)
_ncir = NCIR(
    compute_nodes=[],
    control_nodes=[_control],
    version="ncir_17a",
    cloud_deployments=None,
)
_cloud_deployment = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    flavors=[_cbts_flavor],
    networks=[_cbts_net],
    vnfs=[_cbts_vnf],
    cloud_hosting=_ncir,
)

_capacity_unit = CapacityUnit(addr="192.168.253.22")
_du_pdu = FACOM(addr="10.57.241.145", port_numbers=[5])
_common_unit = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.235.168", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_capacity_unit],
    pdu_port=_du_pdu.pdu_ports[5],
)
_airscale = Airscale(common_units=[_common_unit])
_du = DU(airscale=_airscale)

_cu = CU(
    backhaul_site_oam_ip="10.57.159.136",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.159.136", username="robot", password="rastre1"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.159.136", username="Nemuadmin", password="nemuuser"
    ),
)

_cbts = CloudBts(dus=[_du], cu=_cu, cloud_deployment=_cloud_deployment)

_epcsim = EPCSim(
    mme_ip="172.18.10.12",
    mcc=311,
    mnc=489,
    tac=788,
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.159.137", username="nokia", password="nokia123"
    ),
    dir_path="/home/nokia/WTS_QT",
    cfg_filename="basic_wts_step1.cfg",
    edaemon_port="22222",
    egate_port="20000",
)

tl = TestLine(
    test_pc=_host,
    gnbs=[_cbts],
    tl_cloud_topology=_tl_cloud_topology,
    core=_epcsim,
    cloud_hostings=[_ncir],
)
tl = TestlineWrapper(tl)
