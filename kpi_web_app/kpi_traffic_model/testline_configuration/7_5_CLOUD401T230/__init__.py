import os
from taf.config.testline.cloud_hosting import (
    ControlNode,
    NCIR,
    CloudDeployment,
    DeploymentFlavorStack,
    DeploymentNetworkStack,
    DeploymentVnfStack,
    ComputeNode,
    OSP,
)
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.core import EPCSim, LTEEmuCore, PrismaCore
from taf.config.testline.gnb.du import DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, ATEN, RRB, APC, Gude
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import (
    AirphoneCloud,
    Airphone,
    Prisma,
    TM500,
    Qualcomm,
    QualcommUeType,
    Android,
)  # added in taf.meta.5.4
from taf.config.testline.enb import (
    Enb,
    SimEnb,
    RealEnb,
    LTEEmuEnb,
    PrismaEnb,
    DocomoEnb,
)
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.config.testline.attenuator import (
    AttenuationPort,
    TopYoung,
)  # added in taf.meta 5.4
from taf.config.testline.gnb.networkaddress import NetworkAddress  # add in taf.meta 5.4
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)
from taf.config.testline.hardware_controller import (
    AmiaFanHardwareController,
    GPSPowerHardwareController,
)
from taf.config.testline.signal_analyzer import KeysightN9935A
from taf.config.testline.nms import Netact
from taf.compatibility.configuration import TestlineWrapper

__maintainer__ = "Shi Ming"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_3_GMS <I_MN_5G_RAN_IV4_LINE_HZG_3@internal.nsn.com>"
)
__email__ = "ming.shi@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# #host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.48", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# #Prisma
_airmosaic_ssh = SshServiceDetails(
    addr="10.57.249.82", username="CNHZ5GRAN1112+tester", password="nokia123"
)

_airmosaic_harness = HttpConnectionDetails(addr="10.57.249.82", port=8090)

_lsu_uu_ssh = SshServiceDetails(addr="10.57.249.83", username="user", password="user")

_tstm_uu_ssh = SshServiceDetails(addr="10.57.249.83", username="user", password="user")

_prisma_ue = Prisma(
    airmosaic_ssh_connection_details=_airmosaic_ssh,
    airmosaic_harness_connection_details=_airmosaic_harness,
    lsu_uu_ssh_connection_details=_lsu_uu_ssh,
    tstm_uu_ssh_connection_details=_tstm_uu_ssh,
)

# #RealEnb
_real_enb_pdu = FACOM(addr="10.57.241.151", port_numbers=[4])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.236.3", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[4],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=None)

# #5GRU_0 for cloudBTS
_ru_0_pdu = FACOM(addr="5.5.5.5", port_numbers=[3])

_ru_0 = RU(
    ru_hw_group="mmw",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.17", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.17", username="root", password="umniedziala"
    ),
    pdu_port=_ru_0_pdu.pdu_ports[3],
    radio_type="AEUB",
)

# #DU_0 for cloudlBTS
_lmp_connection_9 = SshServiceDetails(
    addr="10.57.235.7", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_9 = CapacityUnit(addr="6.6.6.6")

_du_0_pdu = FACOM(addr="10.57.241.135", port_numbers=[5])

_common_unit_9 = CommonUnit(
    lmp_connection=_lmp_connection_9,
    capacity_units=[_capacity_unit_9],
    pdu_port=_du_0_pdu.pdu_ports[5],
)

_airscale_0 = Airscale(common_units=[_common_unit_9])

_du_0 = DU(
    airscale=_airscale_0,
    rus=[_ru_0],
    f1_m_ip_addr=NetworkAddress(v4="10.57.227.15", vlan_id=1),
    f1_c_ip_addr=NetworkAddress(v4="10.57.227.15", vlan_id=2),
    f1_u_ip_addr=NetworkAddress(v4="10.57.227.15", vlan_id=3),
)

# #CU

_f1m = NetworkAddress(v4="10.57.165.201", vlan_id=1)
_f1c = NetworkAddress(v4="10.57.165.68", vlan_id=2)
_f1u = NetworkAddress(v4="10.57.165.69", vlan_id=3)
_x2c = NetworkAddress(v4="10.57.165.132", vlan_id=1)
_x2u = NetworkAddress(v4="10.57.165.133", vlan_id=2)
_s1c = NetworkAddress(v4="10.57.165.132", vlan_id=1)
_s1u = NetworkAddress(v4="10.57.165.133", vlan_id=2)
# _tracing = NetworkAddress(v4='10.57.165.202', vlan_id=1)

_cu = CU(
    backhaul_site_oam_ip="10.57.165.3",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.165.3", username="robot", password="rastre1"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.165.3", username="Nemuadmin", password="nemuuser"
    ),
    f1m=_f1m,
    f1c=_f1c,
    f1u=_f1u,
    x2c=_x2c,
    x2u=_x2u,
    s1c=_s1c,
    s1u=_s1u,
    # tracing=_tracing
)

# cloud
_control = ControlNode(
    open_stack_connection_details=OpenStackConnectionDetails(
        ip_addr="10.57.166.244",
        username="nokiauser",
        tenant="FiveG",
        password="HZnokia123!",
        port=13000,
        protocol="https",
        version="v3",
    ),
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.166.244", username="nokiauser", password="HZnokia123!"
    ),
    bmc_connection_details=BmcConnectionDetails(addr="", username="", password=""),
)

_compute = ComputeNode(
    bmc_connection_details=BmcConnectionDetails(addr="", username="", password="")
)

_osp = OSP(
    control_nodes=[_control],
    compute_nodes=[_compute],
    version="19B",
    cloud_deployments=None,
)

# #cloudbts
_cbts_flavor = DeploymentFlavorStack(
    name="sg3-tl230-flavor",
    env_files=[
        os.path.join(_cfg_dir, "5gbts_flavor.env"),
        os.path.join(_cfg_dir, "5gbts_flavor_ci.env"),
    ],
    yaml_file=os.path.join(_cfg_dir, "5gbts_flavor.yaml"),
    default_vnf_prefix="sg3-tl230",
)

_cbts_net = DeploymentNetworkStack(
    name="sg3-tl230-int-net",
    env_files=[
        os.path.join(_cfg_dir, "5gbts_int_net.env"),
        os.path.join(_cfg_dir, "5gbts_int_net_ci.env"),
    ],
    yaml_file=os.path.join(_cfg_dir, "5gbts_int_net.yaml"),
)

_cbts_vnf = DeploymentVnfStack(
    name="sg3-tl230-vnf",
    env_files=[
        os.path.join(_cfg_dir, "5gbts_heat.env"),
        os.path.join(_cfg_dir, "5gbts_heat_ci.env"),
    ],
    yaml_file=os.path.join(_cfg_dir, "5gbts_heat.yaml"),
)

_cloud_deployment = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    flavors=[_cbts_flavor],
    networks=[_cbts_net],
    vnfs=[_cbts_vnf],
    cloud_hosting=_osp,
)

_cbts = CloudBts(dus=[_du_0], cu=_cu, cloud_deployment=_cloud_deployment)

# #cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

# switch
_dell_s4048on_ssh = SshServiceDetails(
    addr="10.57.129.110", port=22, username="readonly", password="readonly"
)
_dell_s4048on_switch = DellS4048ONSwitch(_dell_s4048on_ssh)

# old version keyword under robotws5g/resource compatibility workaround
# tl = TestlineWrapper(tl)

tl = TestLine(
    test_pc=_host,
    gnbs=[_cbts],
    cloud_hostings=[_osp],
    enbs=[_lte_real_enb],
    ues=[_prisma_ue],
    tl_cloud_topology=_tl_cloud_topology,
)

# old version keyword under robotws5g/resource compatibility workaround
tl = TestlineWrapper(tl)
