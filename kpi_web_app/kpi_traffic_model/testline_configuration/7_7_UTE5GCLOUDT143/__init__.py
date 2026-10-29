__maintainer__ = "Jakub Kupiec"
__team__ = "5G_PZ_MMW_KRK_4_SG"
__email__ = "jakub.kupiec@nokia.com"

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
from taf.config.testline import DU, RU
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline import NetworkAddress, RealEnb

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT143.sc5g.krk-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_secgw_vm = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.83.177.53",
        username="ute",
        password="ute",
    ),
    connections=["eth2"],
)

_control_0 = ControlNode(
    open_stack_connection_details=OpenStackConnectionDetails(
        ip_addr="10.83.190.225",
        username="5Guser1",
        tenant="5Gtenant1",
        password="5Guser@4",
    ),
    default_ssh_connection_details=SshServiceDetails(
        addr="10.83.190.225", username="5Guser1", password="5Guser@4"
    ),
    bmc_connection_details=BmcConnectionDetails(addr="", username="", password=""),
)

_compute = ComputeNode(
    bmc_connection_details=BmcConnectionDetails(addr="", username="", password="")
)

_ncir = NCIR(compute_nodes=[_compute], control_nodes=[_control_0], version="ncir_19")

_cbts_flavor = DeploymentFlavorStack(
    name="TL_7_7_UTE5GCLOUDT143_FLAVOR",
    env_files=[os.path.join(_CFG_DIR, "5gbts_flavor.env")],
    yaml_file=os.path.join(_CFG_DIR, "5gbts_flavor.yaml"),
    default_vnf_prefix="5gbts-143",
)

_cbts_net = DeploymentNetworkStack(
    name="TL_7_7_UTE5GCLOUDT143_EXT_NET",
    env_files=[os.path.join(_CFG_DIR, "5gbts_ext_net.env")],
    yaml_file=os.path.join(_CFG_DIR, "5gbts_ext_net.yaml"),
)

_cbts_vnf = DeploymentVnfStack(
    name="TL_7_7_UTE5GCLOUDT143_BTS",
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
    backhaul_site_oam_ip="10.83.182.143",  # '10.83.182.143',
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.83.182.143", username="robot", password="rastre1"  # '10.83.182.143',
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.83.182.143",  # '10.83.182.143',
        username="Nemuadmin",
        password="nemuuser",
    ),
    instance_id=2957,
    global_bts_id=2957,
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
    radio_type="AEUD",
)

_gnb_oam_ip = NetworkAddress(v4="172.16.5.61")

_du1 = DU(
    airscale=Airscale(common_units=[_asik_du1]),
    instance_id=143,
    global_bts_id=143,
    rus=[_ru_du1],
    oam_ip=_asik_du1.lmp_connection.addr,
    f1_m_ip_addr=_gnb_oam_ip.v4,
    f1_c_ip_addr=_gnb_oam_ip.v4,
    f1_u_ip_addr=_gnb_oam_ip.v4,
)

_cbts = CloudBts(
    cu=_cu, cloud_deployment=_cloud_deployment, vnf_name="5gbts-143", dus=[_du1]
)

_enb = RealEnb(
    oam_ip=NetworkAddress(v4="172.16.2.2"),
    instance_id=77034,
    global_bts_id=77034,
)

tl = TestLine(
    test_pc=_test_pc,
    test_pcs=[_secgw_vm],
    gnbs=[_cbts],
    cloud_hostings=[_ncir],
    tl_cloud_topology="CLOUD_5G_ASIKL_ABILB1_AEUD",
    enbs=[_enb],
)

__all__ = ["tl"]
