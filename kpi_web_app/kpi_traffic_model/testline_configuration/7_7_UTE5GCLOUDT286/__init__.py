__maintainer__ = "Marzena Skolucka"
__team__ = "I_MN_5G_SC_PZ_SC_5G_VRF_GMS"
__email__ = "I_MN_5G_SC_PZ_SC_5G_VRF@internal.nsn.com"
__owner_email__ = "pabjan.michal@nokia.com"

import os
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
from taf.config.testline.core import EPCSim
from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.config.testline.hardware_controller import GPSPowerHardwareController

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

_test_pc_ssh = SshServiceDetails(
    addr="7-7-UTE5GCLOUDT286.sc5g.krk-lab.nsn-rdnet.net", username="ute", password="ute"
)

_test_pc = TestPc(default_ssh_connection_details=_test_pc_ssh)

_ru = RU(
    ru_hw_group="5Ggen3_HighF_2T2R",
    radio_type="AEUA",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.34", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="root", password="umniedziala"
    ),
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")

_common_unit_ssh = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_common_unit = CommonUnit(
    _common_unit_ssh,
    capacity_units=[_capacity_unit],
)

_airscale = Airscale([_common_unit])

_compute = ComputeNode(
    bmc_connection_details=BmcConnectionDetails(
        addr="10.44.196.175", username="admin", password="admin"
    )
)
_control_0 = ControlNode(
    open_stack_connection_details=OpenStackConnectionDetails(
        ip_addr="10.83.245.124",
        username="gNB286",
        tenant="gNB286",
        password="Uteadmin111.",
        protocol="https",
    ),
    default_ssh_connection_details=SshServiceDetails(
        addr="10.83.245.124", username="wrsroot", password="uteadmin"
    ),
    bmc_connection_details=BmcConnectionDetails(
        addr="1.1.1.1", username="admin", password="admin"
    ),
)

_ncir = NCIR(compute_nodes=[_compute], control_nodes=[_control_0], version="ncir_19")

_cbts_flavor = DeploymentFlavorStack(
    name="TL_7_7_UTE5GCLOUDT286_FLAVOR",
    env_files=[os.path.join(_CFG_DIR, "5gbts_flavor.env")],
    yaml_file=os.path.join(_CFG_DIR, ""),
    default_vnf_prefix="5gbts-286",
)

_cbts_net = DeploymentNetworkStack(
    name="TL_7_7_UTE5GCLOUDT286_EXT_NET",
    env_files=[os.path.join(_CFG_DIR, "5gbts_ext_net.env")],
    yaml_file=os.path.join(_CFG_DIR, ""),
)

_cbts_vnf = DeploymentVnfStack(
    name="TL_7_7_UTE5GCLOUDT286_BTS",
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
    backhaul_site_oam_ip="2a00:8a02:60:1c::1:286",
    oam_ssh_connection_details=SshServiceDetails(
        addr="2a00:8a02:60:1c::1:286", username="robot", password="rastre1"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="[2a00:8a02:60:1c::1:286]", username="Nemuadmin", password="nemuuser"
    ),
)

_du = DU(
    airscale=_airscale,
    rus=[_ru],
    f1_c_ip_addr="2a00:2222:2222:2222:2222:2222:2222:61",
    f1_u_ip_addr="2a00:2222:2222:2222:2222:2222:2222:62",
    f1_m_ip_addr="2a00:2222:2222:2222:2222:2222:2222:60",
)

_cbts = CloudBts(
    cu=_cu,
    dus=[_du],
    cloud_deployment=_cloud_deployment,
    vnf_name="5gbts-286",
    instance_id=1900,
    global_bts_id=1900,
)

_lteenb = RealEnb(
    airscale=_du, x2_link_addr=NetworkAddress(v4="2a00:8a02:60:1c::2:286")
)

_rpi = GPSPowerHardwareController(
    default_ssh_connection_details=SshServiceDetails(
        addr="GpsBreaker.lab0.krk-lab.nsn-rdnet.net",
        username="pi",
        password="gpsbreaker",
    )
)

tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    enbs=[_lteenb],
    ues=None,
    cloud_hostings=[_ncir],
    hardware_controllers=[_rpi],
    tl_cloud_topology="CLOUD_5G_ASIKL_ABILB1_AEUA_19B",
)

__all__ = ["tl"]
