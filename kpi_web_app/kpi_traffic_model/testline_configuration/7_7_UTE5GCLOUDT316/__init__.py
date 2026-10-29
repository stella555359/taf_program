import os

__maintainer__ = "Krystian Lachut"
__team__ = "5G_PZ_MMW_KRK_2_SG"
__email__ = "krystian.alchut@nokia.com"


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
from taf.config.testline.hardware_controller import (
    GPSPowerHardwareController,
    AmiaFanHardwareController,
)
from taf.config.testline import NetworkAddress, RealEnb
from taf.config.testline.core import EPCSim

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT316.sc5g.krk-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_control_0 = ControlNode(
    open_stack_connection_details=OpenStackConnectionDetails(
        ip_addr="10.83.245.124", username="admin", tenant="admin", password="uteadmin"
    ),
    default_ssh_connection_details=SshServiceDetails(
        addr="10.83.245.124", username="wrsroot", password="uteadmin"
    ),
    bmc_connection_details=BmcConnectionDetails(addr="", username="", password=""),
)

_compute = ComputeNode(
    bmc_connection_details=BmcConnectionDetails(addr="", username="", password="")
)

_ncir = NCIR(compute_nodes=[_compute], control_nodes=[_control_0], version="ncir_19")

_cbts_flavor = DeploymentFlavorStack(
    name="TL_7_7_UTE5GCLOUDT316_FLAVOR",
    env_files=[os.path.join(_CFG_DIR, "5gbts_flavor.env")],
    yaml_file=os.path.join(_CFG_DIR, "5gbts_flavor.yaml"),
    default_vnf_prefix="5gbts-316",
)

_cbts_net = DeploymentNetworkStack(
    name="TL_7_7_UTE5GCLOUDT316_EXT_NET",
    env_files=[os.path.join(_CFG_DIR, "5gbts_ext_net.env")],
    yaml_file=os.path.join(_CFG_DIR, "5gbts_ext_net.yaml"),
)

_cbts_vnf = DeploymentVnfStack(
    name="TL_7_7_UTE5GCLOUDT316_BTS",
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
    backhaul_site_oam_ip="2a00:8a02:60:1c::1:316",
    oam_ssh_connection_details=SshServiceDetails(
        addr="2a00:8a02:60:1c::1:316", username="robot", password="rastre1"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="[2a00:8a02:60:1c::1:316]", username="Nemuadmin", password="nemuuser"
    ),
)

_abil1_du1 = CapacityUnit(addr="192.168.253.16")

_abil1_du2 = CapacityUnit(addr="192.168.253.32")

_asik_du1 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_abil1_du1],
)

_asik_du2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_abil1_du2],
)

_ru_du1 = RU(
    ru_hw_group="",
    default_ssh_connection_details=SshServiceDetails(addr="", username=""),
    lmp_connection=SshServiceDetails(addr="", username=""),
    radio_type="AEUD",
)

_ru_du2 = RU(
    ru_hw_group="",
    default_ssh_connection_details=SshServiceDetails(addr="", username=""),
    lmp_connection=SshServiceDetails(addr="", username=""),
    radio_type="AEUD",
)

_du1 = DU(
    Airscale(common_units=[_asik_du1]),
    rus=[_ru_du1],
    f1_c_ip_addr="2a00:2222:2222:2222:2222:2222:2222:61",
    f1_u_ip_addr="2a00:2222:2222:2222:2222:2222:2222:62",
    f1_m_ip_addr="2a00:2222:2222:2222:2222:2222:2222:60",
)

_du2 = DU(
    Airscale(common_units=[_asik_du2]),
    rus=[_ru_du2],
    f1_c_ip_addr="2a00:2222:2222:2222:2222:2222:2222:71",
    f1_u_ip_addr="2a00:2222:2222:2222:2222:2222:2222:72",
    f1_m_ip_addr="2a00:2222:2222:2222:2222:2222:2222:70",
)

_cbts = CloudBts(
    cu=_cu,
    cloud_deployment=_cloud_deployment,
    vnf_name="5gbts-316",
    dus=[_du1, _du2],
    instance_id=316,
    global_bts_id=10316,
)

_enb = RealEnb(x2_link_addr=NetworkAddress(v6="2a00:8a02:60:1c:0:0:2:390"))

tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    cloud_hostings=[_ncir],
    tl_cloud_topology="CLOUD_5G_MULTIDU_ASIKLR_ABILB1B4_AEUD_IPv6",
    enbs=[_enb],
)

tl = TestlineWrapper(tl)

__all__ = ["tl"]
