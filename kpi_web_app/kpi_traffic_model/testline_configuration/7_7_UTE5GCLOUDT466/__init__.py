__maintainer__ = "Lukasz Rzodeczko"
__team__ = "5G_PZ_MMW_KRK_3_SG"
__email__ = "lukasz.rzodeczko@nokia.com"

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
from taf.config.testline.nom import NOM
from taf.config.testline.nms import NMS, Netact

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT466.sc5g.krk-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_control_0 = ControlNode(
    open_stack_connection_details=OpenStackConnectionDetails(
        ip_addr="10.83.190.225",
        username="5Guser1",
        tenant="5Gtenant1",
        password="5Guser@8",
    ),
    default_ssh_connection_details=SshServiceDetails(
        addr="10.83.190.225", username="5Guser1", password="5Guser@8"
    ),
    bmc_connection_details=BmcConnectionDetails(addr="", username="", password=""),
)

_compute = ComputeNode(
    bmc_connection_details=BmcConnectionDetails(addr="", username="", password="")
)

_ncir = NCIR(compute_nodes=[_compute], control_nodes=[_control_0], version="ncir_19")

_cbts_flavor = DeploymentFlavorStack(
    name="TL_7_7_UTE5GCLOUDT466_FLAVOR",
    env_files=[os.path.join(_CFG_DIR, "config_flavor.env")],
    yaml_file=os.path.join(_CFG_DIR, "5gbts_flavor.yaml"),
    default_vnf_prefix="5gbts-466",
)

_cbts_net = DeploymentNetworkStack(
    name="TL_7_7_UTE5GCLOUDT466_EXT_NET",
    env_files=[os.path.join(_CFG_DIR, "config_ext_net.env")],
    yaml_file=os.path.join(_CFG_DIR, "5gbts_ext_net.yaml"),
)

_cbts_vnf = DeploymentVnfStack(
    name="TL_7_7_UTE5GCLOUDT466_BTS",
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
    backhaul_site_oam_ip="10.83.183.216",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.83.183.216", username="robot", password="rastre1"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.83.183.216", username="Nemuadmin", password="nemuuser"
    ),
)

_abil1_du1 = CapacityUnit(addr="192.168.253.20")

_asik_du1 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_abil1_du1],
)

_asik_du2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.83.251.17",
        username="toor4nsn",
        password="oZPS0POrRieRtu",
    ),
    capacity_units=[_abil1_du1],
)

_xtower = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="SC5G-Xtower-04.sc5g.krk-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    ),
    capacity_units=[_abil1_du1],
)

_ru_du1 = RU(
    ru_hw_group="",
    default_ssh_connection_details=SshServiceDetails(addr="", username=""),
    lmp_connection=SshServiceDetails(addr="", username=""),
    radio_type="AEUB",
)

_du1 = DU(
    Airscale(common_units=[_asik_du1, _asik_du2, _xtower]),
    rus=[_ru_du1],
    f1_m_ip_addr="172.16.5.60",
)

_cbts = CloudBts(
    cu=_cu,
    cloud_deployment=_cloud_deployment,
    vnf_name="5gbts-466",
    dus=[_du1],
    instance_id=2466,
    global_bts_id=466,
)

_enb = RealEnb(
    oam_ip=NetworkAddress(v4="172.16.2.8"),
    instance_id=10008,
    global_bts_id=10008,
    x2_link_addr=NetworkAddress(v4="172.16.2.8"),
)
_netAct = Netact(
    addr="srnclab1023lbwas.srnblr.nsn-rdnet.net",
    nom=NOM(
        ssh_connections_info=SshServiceDetails(
            addr="10.41.147.215", username="omc", password="Medsql!_1893"
        )
    ),
)
_instance_id_du = 1466

tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    cloud_hostings=[_ncir],
    tl_cloud_topology="CLOUD_5G_ASOD_AEUB_XTOWER",
    enbs=[_enb],
    nms=_netAct,
)

tl = TestlineWrapper(tl)

__all__ = ["tl"]
