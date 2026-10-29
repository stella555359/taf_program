__maintainer__ = "Grzegorz Hajto"
__team__ = "5G_PZ_MMW_KRK_3_SG"
__email__ = "grzegorz.hajto@nokia.com"

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
    ComputeNode,
)
from taf.config.testline.gnb import CloudBts, CU
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline import DU, RU
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline import NetworkAddress, RealEnb

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="sc5g-enb-319.sc5g.krk-lab.nsn-rdnet.net", username="ute", password="ute"
    )
)

_control_0 = ControlNode(
    open_stack_connection_details=OpenStackConnectionDetails(
        ip_addr="10.83.190.225",
        username="5Guser1",
        tenant="5Gtenant1",
        password="5Guser@1",
    ),
    default_ssh_connection_details=SshServiceDetails(
        addr="10.83.190.225", username="5Guser1", password="5Guser@1"
    ),
    bmc_connection_details=BmcConnectionDetails(addr="", username="", password=""),
)

_compute = ComputeNode(
    bmc_connection_details=BmcConnectionDetails(addr="", username="", password="")
)

_ncir = NCIR(compute_nodes=[_compute], control_nodes=[_control_0], version="ncir_19")

_cbts_flavor = DeploymentFlavorStack(
    name="TL_7_7_UTE5GCLOUDT319_FLAVOR",
    env_files=[os.path.join(_CFG_DIR, "config_flavor.env")],
    yaml_file=os.path.join(_CFG_DIR, "5gbts_flavor.yaml"),
    default_vnf_prefix="5gbts-319",
)

_cbts_net = DeploymentNetworkStack(
    name="TL_7_7_UTE5GCLOUDT319_EXT_NET",
    env_files=[os.path.join(_CFG_DIR, "config_ext_net.env")],
    yaml_file=os.path.join(_CFG_DIR, "5gbts_ext_net.yaml"),
)

_cbts_vnf = DeploymentVnfStack(
    name="TL_7_7_UTE5GCLOUDT319_BTS",
    env_files=[os.path.join(_CFG_DIR, "config_bts.env")],
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
    backhaul_site_oam_ip="10.83.183.69",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.83.183.69", username="robot", password="rastre1"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.83.183.69", username="Nemuadmin", password="nemuuser"
    ),
)

_abil_du = CapacityUnit(addr="192.168.253.36")

_test_pc_gnb_default_ssh_connection_details = SshServiceDetails(
    addr="sc5g-enb-319.sc5g.krk-lab.nsn-rdnet.net", username="ute", password="ute"
)

_asik_du = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129",
        username="toor4nsn",
        password="oZPS0POrRieRtu",
        proxy=_test_pc_gnb_default_ssh_connection_details,
    ),
    capacity_units=[_abil_du],
)

_ru1_du = RU(
    ru_hw_group="",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.145", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(addr="", username=""),
    radio_type="AEUB",
)

_ru2_du = RU(
    ru_hw_group="",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.147", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(addr="", username=""),
    radio_type="AEUB",
)

_du = DU(
    Airscale(common_units=[_asik_du]),
    rus=[_ru1_du, _ru2_du],
    f1_m_ip_addr="172.16.5.61",
)

_cbts = CloudBts(
    cu=_cu,
    cloud_deployment=_cloud_deployment,
    vnf_name="5gbts-319",
    dus=[_du],
    instance_id=3191,
    global_bts_id=3191,
)

_enb = RealEnb(
    oam_ip=NetworkAddress(v4="172.16.2.8"),
    instance_id=10008,
    global_bts_id=10008,
    x2_link_addr=NetworkAddress(v4="172.16.2.8"),
)

tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    cloud_hostings=[_ncir],
    tl_cloud_topology="CLOUD_5G_ASIKA101L_ABILA101_AEUB",
    enbs=[_enb],
)

tl = TestlineWrapper(tl)

__all__ = ["tl"]
