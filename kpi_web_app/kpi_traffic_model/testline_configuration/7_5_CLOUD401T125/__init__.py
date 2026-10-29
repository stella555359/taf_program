__maintainer__ = "helen chen"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_7_GMS <I_MN_5G_RAN_IV4_LINE_HZG_7@internal.nsn.com>"
)
__email__ = "helen.1.chen@nokia-sbell.com"

import os

from taf.config.testline.cloud_hosting import (
    ControlNode,
    OSP,
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
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.ue import TM500
from taf.config.testline.core import EPCSim, LTEEmuCore
from taf.config.testline import RealEnb, LTEEmuEnb
from taf.config.testline import DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.radio import RU, RadioModule

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# ########Testpc##########
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.78", username="root", password="nokia123"
    )
)

# #######Cobham########
_iperf_details = IperfDataTransferDetails(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.157.141", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    network_interface_address="192.168.10.70",
    iperf_path=None,
)

_tm500 = TM500(
    tma_host=SshServiceDetails(addr="10.57.246.89", username="5G", password="5g"),
    tma_command_port=5030,
    pdu_port=None,
    tma_path="C:\\Program Files (x86)\\Aeroflex\\TM500\\5G NR - NLA 4.23.0 NG081020191\\Test Mobile Application\\"
    "TmaApplication.exe",
    iperf_details=_iperf_details,
)

# ########EPCSim##########
_epc_sim = EPCSim(
    mme_ip="",
    tac=788,
    mcc=489,
    mnc=311,
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.141", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    dir_path="/opt/iphy/WTS_405454",
    cfg_filename="TL125_epc_standalone_v4.lua",
    edaemon_port=10000,
    egate_port=20000,
)

# ########LTEEmuEnb##########
_lte_emu_enb = LTEEmuEnb(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.141", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    dir_path="/home/ute/AirPhone-wts_CIT",
    cfg_filename="1du.cfg",
)

# ########CU##########
_cu_oam_ip = "10.57.171.10"
_cu = CU(
    backhaul_site_oam_ip=_cu_oam_ip,
    oam_ssh_connection_details=SshServiceDetails(
        addr=_cu_oam_ip, username="robot", password="rastre1"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr=_cu_oam_ip, username="Nemuadmin", password="nemuuser"
    ),
)

# ########DU##########
# DU1
_lmp_connection_0 = SshServiceDetails(
    addr="10.57.242.84", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_0 = CapacityUnit(addr="ip")

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection_0, capacity_units=[_capacity_unit_0], pdu_port=None
)

# ########RU##########
_5g_ru_pdu = FACOM(addr="10.57.246.238", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_ru = RU(
    ru_hw_group="mmw",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.17", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.17", username="root", password="umniedziala"
    ),
    pdu_port=_5g_ru_pdu.pdu_ports[1],
    radio_type="AEUB",
)

# airscale
_airscale_0 = Airscale(common_units=[_common_unit_0])

_du_0 = DU(airscale=_airscale_0, rus=[_ru], f1_m_ip_addr="10.57.242.84")

# ########CloudBts##########
flavor_env_files = [os.path.join(_cfg_dir, "5gbts_flavor.env")]

net_env_files = [
    os.path.join(_cfg_dir, "5gbts_int_net.env"),
    os.path.join(_cfg_dir, "5gbts_int_net_ci.env"),
]

vnf_env_files = [
    os.path.join(_cfg_dir, "5gbts_heat.env"),
    os.path.join(_cfg_dir, "5gbts_heat_ci.env"),
]

_cbts_flavor = DeploymentFlavorStack(
    name="sq7-tl125-flavor",
    env_files=flavor_env_files,
    yaml_file=os.path.join(_cfg_dir, "5gbts_flavor.yaml"),
    default_vnf_prefix="hgz-tl125",
)

_cbts_net = DeploymentNetworkStack(
    name="sq7-tl125-int",
    env_files=net_env_files,
    yaml_file=os.path.join(_cfg_dir, "5gbts_int_net.yaml"),
)

_cbts_vnf = DeploymentVnfStack(
    name="sq7-tl125-vnf",
    env_files=vnf_env_files,
    yaml_file=os.path.join(_cfg_dir, "5gbts_heat.yaml"),
)

_control = ControlNode(
    open_stack_connection_details=OpenStackConnectionDetails(
        ip_addr="10.57.137.84",
        username="cit",
        tenant="nokia",
        password="cit",
        port=13000,
    ),
    default_ssh_connection_details=SshServiceDetails(addr="", username="", password=""),
    bmc_connection_details=BmcConnectionDetails(addr="", username="", password=""),
)

_osp = OSP(
    control_nodes=[_control], version="19A", cloud_deployments=None, compute_nodes=[]
)

_cloud_deployment = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    flavors=[_cbts_flavor],
    networks=[_cbts_net],
    vnfs=[_cbts_vnf],
    cloud_hosting=_osp,
)

_cbts = CloudBts(
    dus=[_du_0], cu=_cu, cloud_deployment=_cloud_deployment, vnf_name="sq7-tl125"
)

# ########TestLine##########
_tl = TestLine(
    test_pc=_test_pc,
    ues=[_tm500],
    gnbs=[_cbts],
    cloud_hostings=[_osp],
    enbs=[_lte_emu_enb],
    core=_epc_sim,
    tl_cloud_topology="CLOUD_5G_BB3_19",
)

tl = TestlineWrapper(_tl)

# tl.gnbs[0].cloud_deployment.vnfs[0].configuration_data["parameters"]["oam_ip"]=_cu_oam_ip

__all__ = ["tl"]
