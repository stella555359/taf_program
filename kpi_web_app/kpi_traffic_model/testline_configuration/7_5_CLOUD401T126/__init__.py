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
from taf.config.testline.ue import TM500
from taf.config.testline.core import LTEEmuCore, EPCSim
from taf.config.testline.enb import LTEEmuEnb, RealEnb
from taf.config.testline.gnb.du import DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.config.cbts import create_configuration_data
from taf.config.testline.radio import RU, RadioModule
from taf.config.testline.cbam import Cbam

__maintainer__ = "Gu Xinyu"
__team__ = "MN 5G RAN I&V 4 Pz HZG SG7"
__email__ = "I_MN_5G_RAN_IV4_LINE_HZG_7@internal.nsn.com"
__owner_email__ = "xinyu.gu@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# ########Testpc##########
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.110", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

########Cobham########
_tm500 = TM500(
    tma_host=SshServiceDetails(
        addr="10.57.243.55", username="CNHZ5GRAN1005+nokia", password="nokia123"
    ),
    tma_command_port=5030,
    pdu_port=None,
    tma_path="/cygdrive/c/Program Files (x86)/Aeroflex/TM500/5G NR - NLA 4.18.0/Test Mobile Application/TmaApplication.exe",
)

########EPCSim########
_epc_sim = EPCSim(
    mme_ip="",
    tac=788,
    mcc=3,
    mnc=262,
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.142", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    dir_path="/opt/iphy/WTS_405454",
    cfg_filename="TL121_epc_standalon_v4.lua",
    edaemon_port=10000,
    egate_port=20000,
)


# ########LTEEmuEnb##########
_real_enb_pdu = FACOM(addr="10.57.241.198", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_lmp_connection_enb = SshServiceDetails(
    addr="10.57.237.164", username="toor4nsn", password="oZPS0POrRieRtu"
)

_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection_enb,
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[1],
)

_real_enb = Airscale(common_units=[_common_unit_1])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=None)

# ########CU##########
_cu_oam_ip = "10.57.250.4"
_cu = CU(
    backhaul_site_oam_ip=_cu_oam_ip,
    oam_ssh_connection_details=SshServiceDetails(
        addr=_cu_oam_ip, username="robot", password="rastre1"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr=_cu_oam_ip, username="Nemuadmin", password="nemuuser"
    ),
)

########DU########
# DU1
_lmp_connection_0 = SshServiceDetails(
    addr="10.57.237.156", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_0 = CapacityUnit(addr="192.168.253.18")

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection_0, capacity_units=[_capacity_unit_0], pdu_port=None
)

#########5G RU##########
_5g_ru_pdu = FACOM(addr="10.57.249.7", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_ru = RU(
    ru_hw_group="mmw",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.17", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.17", username="root", password="umniedziala"
    ),
    pdu_port=_5g_ru_pdu.pdu_ports[3],
    radio_type="AEUD",
)

# airscale
_airscale_0 = Airscale(common_units=[_common_unit_0])

_du_0 = DU(airscale=_airscale_0, rus=[_ru], f1_m_ip_addr="10.57.237.156")

# ########CloudBts##########
flavor_env_files = [
    os.path.join(_cfg_dir, "5gbts_flavor.env"),
    os.path.join(_cfg_dir, "5gbts_flavor_ci.env"),
]

net_env_files = [
    os.path.join(_cfg_dir, "5gbts_ext_net.env"),
    os.path.join(_cfg_dir, "5gbts_ext_net_ci.env"),
]

vnf_env_files = [
    os.path.join(_cfg_dir, "5gbts_heat.env"),
    os.path.join(_cfg_dir, "5gbts_heat_ci.env"),
]

_cbts_flavor = DeploymentFlavorStack(
    name="sg7-tl126-flavor",
    env_files=flavor_env_files,
    yaml_file=os.path.join(_cfg_dir, "5gbts_flavor.yaml"),
    default_vnf_prefix="hgz-tl126",
)

_cbts_net = DeploymentNetworkStack(
    name="sg7-tl126-net",
    env_files=net_env_files,
    yaml_file=os.path.join(_cfg_dir, "5gbts_ext_net.yaml"),
)

_cbts_vnf = DeploymentVnfStack(
    name="sg7-tl126-vnfc",
    env_files=vnf_env_files,
    yaml_file=os.path.join(_cfg_dir, "5gbts_heat.yaml"),
)


_control = ControlNode(
    open_stack_connection_details=OpenStackConnectionDetails(
        ip_addr="10.57.137.2",
        username="sqg07",
        tenant="SQG07",
        password="Nokia07!",
        port=5000,
    ),
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.137.2", username="sqg07", password="Nokia07!"
    ),
    bmc_connection_details=BmcConnectionDetails(addr="", username="", password=""),
)

_ncir = NCIR(
    control_nodes=[_control],
    version="ncir_18",
    cloud_deployments=None,
    compute_nodes=[],
)

_cloud_deployment = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    flavors=[_cbts_flavor],
    networks=[_cbts_net],
    vnfs=[_cbts_vnf],
    cloud_hosting=_ncir,
)

_cbts = CloudBts(
    dus=[_du_0], cu=_cu, cloud_deployment=_cloud_deployment, vnf_name="hgz-tl126"
)

_cbam = Cbam(
    addr="10.57.157.100",
    client_id="cbam_test",
    client_secret="249a650a-092f-4654-83bd-924321efc87d",
)

# ########TestLine##########
_tl = TestLine(
    test_pc=_test_pc,
    ues=[_tm500],
    gnbs=[_cbts],
    cloud_hostings=[_ncir],
    enbs=[_lte_real_enb],
    core=_epc_sim,
    cbam=_cbam,
    tl_cloud_topology="CLOUD_5G_BB3_19",
)

tl = _tl
