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
from taf.config.testline.core import LTEEmuCore, EPCSim
from taf.config.testline.enb import LTEEmuEnb, RealEnb
from taf.config.testline.gnb.du import DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.config.testline.attenuator import (
    AttenuationPort,
    TopYoung,
)  # added in taf.meta 5.4
from taf.config.testline.gnb.networkaddress import NetworkAddress  # add in taf.meta 5.4
from taf.config.testline.radio import RU, RadioModule

__maintainer__ = "Yu Zhang"
__team__ = "MN 5G RAN I&V 4 Pz HZG SG7"
__email__ = "I_MN_5G_RAN_IV4_LINE_HZG_7@internal.nsn.com"
__owner_email__ = "yu.8.zhang@nokia-sbell.com"

# #######common########
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# #######Testpc########
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.42", username="root", password="nokia123"
    )
)

# #######Cobham########
_iperf_details = IperfDataTransferDetails(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.162.2", username="mmw_sg2", password="mm@2"
    ),
    network_interface_address="192.168.10.70",
    iperf_path=None,
    port=42324,
)

_tm500 = TM500(
    tma_host=SshServiceDetails(
        addr="10.57.161.6",
        username="nokia5G",
        password="noki@123",
        private_key="CNHZ5GRAN1366",
    ),
    tma_command_port=5030,
    pdu_port=None,
    iperf_details=_iperf_details,
    tma_path="/cygdrive/c/Program Files (x86)/Aeroflex/TM500/5G NR - NLA 4.25.0/Test Mobile Application/TMA.exe",
)


# #######RealEnb########
_real_enb_pdu = FACOM(addr="10.57.240.148", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_lmp_connection_enb = SshServiceDetails(
    addr="10.57.237.111", username="toor4nsn", password="oZPS0POrRieRtu"
)

_x2_link_addr = NetworkAddress(v4="10.57.237.111", v6="xxxx", vlan_id=1)

_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection_enb,
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[1],
)

_real_enb = Airscale(common_units=[_common_unit_1])

_lte_real_enb = RealEnb(airscale=_real_enb, x2_link_addr=_x2_link_addr, rms=None)

# #######CU########
_cu_oam_ip = "10.57.155.135"

_f1m = NetworkAddress(v4="192.168.135.10", v6="xxxx", vlan_id=1)
_f1c = NetworkAddress(v4="192.168.135.20", v6="xxxx", vlan_id=2)
_f1u = NetworkAddress(v4="192.168.135.30", v6="xxxx", vlan_id=3)
_x2c = NetworkAddress(v4="10.57.155.124", v6="xxxx", vlan_id=1)
_x2u = NetworkAddress(v4="10.57.155.125", v6="xxxx", vlan_id=2)
_s1c = NetworkAddress(v4="10.57.155.124", v6="xxxx", vlan_id=1)
_s1u = NetworkAddress(v4="10.57.155.125", v6="xxxx", vlan_id=2)
_cu = CU(
    backhaul_site_oam_ip=_cu_oam_ip,
    oam_ssh_connection_details=SshServiceDetails(
        addr=_cu_oam_ip, username="robot", password="rastre1"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr=_cu_oam_ip, username="Nemuadmin", password="nemuuser"
    ),
    f1m=_f1m,
    f1c=_f1c,
    f1u=_f1u,
    x2c=_x2c,
    x2u=_x2u,
    s1c=_s1c,
    s1u=_s1u,
)
# #######DU########
# DU1
_lmp_connection_0 = SshServiceDetails(
    addr="10.57.237.153", username="toor4nsn", password="oZPS0POrRieRtu"
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

_du_0 = DU(
    airscale=_airscale_0,
    rus=[_ru],
    f1_m_ip_addr="192.168.135.160",
    f1_c_ip_addr="192.168.135.161",
    f1_u_ip_addr="192.168.135.162",
)

# #######CloudBts########
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
    name="sg7-tl324-flavor",
    env_files=flavor_env_files,
    yaml_file=os.path.join(_cfg_dir, "5gbts_flavor.yaml"),
    default_vnf_prefix="hgz-tl324",
)

_cbts_net = DeploymentNetworkStack(
    name="sg7-tl324-int",
    env_files=net_env_files,
    yaml_file=os.path.join(_cfg_dir, "5gbts_int_net.yaml"),
)

_cbts_vnf = DeploymentVnfStack(
    name="sg7-tl324-vnfc",
    env_files=vnf_env_files,
    yaml_file=os.path.join(_cfg_dir, "5gbts_heat.yaml"),
)

_control = ControlNode(
    open_stack_connection_details=OpenStackConnectionDetails(
        ip_addr="10.57.155.3",
        username="sqg07",
        tenant="nokia",
        password="Osp07!",
        port=13000,
    ),
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.20", username="sqg07", password="Osp07!"
    ),
    bmc_connection_details=BmcConnectionDetails(
        addr="10.57.155.4", username="a", password="p"
    ),
)

_osp = OSP(
    control_nodes=[_control], version="19A", compute_nodes=[], cloud_deployments=None
)

_cloud_deployment = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    flavors=[_cbts_flavor],
    networks=[_cbts_net],
    vnfs=[_cbts_vnf],
    cloud_hosting=_osp,
)

_cbts = CloudBts(
    dus=[_du_0], cu=_cu, cloud_deployment=_cloud_deployment, vnf_name="hgz-tl324"
)

_topyoung0 = TopYoung(ip_addr="10.57.249.48", port=3000, attenuation_port_numbers=[])

# #######TestLine########
_tl = TestLine(
    test_pc=_test_pc,
    ues=[_tm500],
    gnbs=[_cbts],
    cloud_hostings=[_osp],
    enbs=[_lte_real_enb],
    tl_cloud_topology="CLOUD_5G_BB3_19",
    attenuator=_topyoung0,
)

tl = _tl
