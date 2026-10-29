__maintainer__ = "Marzena Skolucka"
__team__ = "I_MN_5G_SC_PZ_SC_5G_VRF_GMS"
__email__ = "I_MN_5G_SC_PZ_SC_5G_VRF@internal.nsn.com"
__owner_email__ = "marzena.skolucka@nokia.com"

import os
from taf.config.testline.testpc import TestPc
from taf.config.testline import RU, DU
from taf.config.testline.testline import TestLine
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.gnb import CloudBts, CU
from taf.config.testline.airscale import CommonUnit, CapacityUnit, Airscale
from taf.config.testline.core import EPCSim
from taf.config.testline.enb import RealEnb
from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.config.testline.cloud_hosting import (
    ControlNode,
    NCIR,
    CloudDeployment,
    DeploymentFlavorStack,
    DeploymentNetworkStack,
    DeploymentVnfStack,
    ComputeNode,
)
from taf.config.testline.connection_details import (
    SshServiceDetails,
    OpenStackConnectionDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
)

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDTSK028.ska.krk-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_compute = ComputeNode(
    bmc_connection_details=BmcConnectionDetails(
        addr="10.44.196.175", username="admin", password="admin"
    )
)

_control_0 = ControlNode(
    open_stack_connection_details=OpenStackConnectionDetails(
        ip_addr="10.83.190.241",
        username="sb14user1",
        tenant="sb14tenant1",
        password="5Guser@2",
    ),
    default_ssh_connection_details=SshServiceDetails(
        addr="10.83.190.241", username="sb14user1", password="5Guser@2"
    ),
    bmc_connection_details=BmcConnectionDetails(
        addr="1.1.1.1", username="admin", password="admin"
    ),
)


_ru_1 = RU(
    ru_hw_group="hw_group",
    radio_type="AEUD",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.253.150", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="TO_UPDATE", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
)

_ncir = NCIR(compute_nodes=[_compute], control_nodes=[_control_0], version="ncir_19")

_cbts_flavor = DeploymentFlavorStack(
    name="TL_7_7_UTE5GCLOUDT191_FLAVOR",
    env_files=[os.path.join(_CFG_DIR, "5gbts_flavor.env")],
    yaml_file=os.path.join(_CFG_DIR, "5gbts_flavor.yaml"),
    default_vnf_prefix="Flavors_28",
)

_cbts_net = DeploymentNetworkStack(
    name="TL_7_7_UTE5GCLOUDT191_EXT_NET",
    env_files=[os.path.join(_CFG_DIR, "5gbts_ext_net.env")],
    yaml_file=os.path.join(_CFG_DIR, "5gbts_ext_net.yaml"),
)

_cbts_vnf = DeploymentVnfStack(
    name="TL_7_7_UTE5GCLOUDT191_BTS",
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
    backhaul_site_oam_ip="10.83.250.7",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.83.250.7", username="robot", password="rastre1"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.83.250.7", username="Nemuadmin", password="nemuuser"
    ),
    instance_id=280000,
    global_bts_id=1,
)

_du_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_du_capacity_unit = CapacityUnit(
    addr="192.168.253.36", hardware_type="ABIL", hardware_version="A02"
)

_du_common_unit = CommonUnit(
    lmp_connection=_du_lmp_connection,
    capacity_units=[_du_capacity_unit],
    hardware_type="ASIK",
    hardware_version="A01",
)

_airscale = Airscale(common_units=[_du_common_unit])

_du = DU(airscale=_airscale, rus=[_ru_1], global_bts_id=1, instance_id=28)

_cbts = CloudBts(
    cu=_cu, cloud_deployment=_cloud_deployment, vnf_name="VNF_28", dus=[_du]
)


_core = EPCSim(
    default_ssh_connection_details=SshServiceDetails(
        addr="SKA-029-ute.ska.krk-lab.nsn-rdnet.net", username="ute", password="ute"
    ),
    dir_path="/home/ute/epcsim",
    cfg_filename="sim.cfg",
    mme_ip="10.253.180.29",
    mcc="244",
    mnc="8",
    tac=1024,
    edaemon_port=10000,
    egate_port=60001,
)


_lteenb = RealEnb(x2_link_addr=NetworkAddress(v4="10.83.250.40"))

tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    enbs=[_lteenb],
    core=_core,
    cloud_hostings=[_ncir],
    tl_cloud_topology="CLOUD_5G_ASIKL_ABILB1_AEUD_ENB_20B",
)

__all__ = ["tl"]
