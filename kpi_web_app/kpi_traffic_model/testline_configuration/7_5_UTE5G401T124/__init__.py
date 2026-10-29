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
from taf.config.testline.core import EPCSim, LTEEmuCore, PrismaCore
from taf.config.testline.gnb.du import DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, ATEN, RRB, APC, Gude
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import AirphoneCloud, Airphone, Prisma, TM500
from taf.config.testline.enb import (
    Enb,
    SimEnb,
    RealEnb,
    LTEEmuEnb,
    PrismaEnb,
    DocomoEnb,
)
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch

# added in taf.meta 5.4
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
from taf.config.testline.cbam import Cbam

__maintainer__ = "Dong Tingting"
__team__ = (
    "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_02_GMS <I_NSB_MN_5GSC_MMW_SC_PZ_HZ_02@internal.nsn.com>"
)
__email__ = "tingting.dong@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# Testpc
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.78", username="root", password="nokia123"
    )
)
# RealEnb
_real_enb_pdu = FACOM(addr="10.57.241.147", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_lmp_connection_enb = SshServiceDetails(
    addr="10.57.235.211", username="toor4nsn", password="oZPS0POrRieRtu"
)

_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection_enb,
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[2],
)

_real_enb = Airscale(common_units=[_common_unit_1])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=None)

# #5GRU_0 for cloudBTS
_5g_ru_pdu = FACOM(addr="10.57.249.7", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_ru = RU(
    ru_hw_group="Above6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.10.41", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.10.41", username="root", password="umniedziala"
    ),
    pdu_port=_5g_ru_pdu.pdu_ports[1],
    radio_type="AEUB",
)

# #DU_0 for cloudlBTS
_du_lmp_ip = "10.57.229.99"
_lmp_connection_0 = SshServiceDetails(
    addr=_du_lmp_ip, username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_0 = CapacityUnit(addr="192.168.253.18")

_du_pdu = FACOM(addr="10.57.241.194", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection_0,
    capacity_units=[_capacity_unit_0],
    pdu_port=_du_pdu.pdu_ports[6],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru], f1_m_ip_addr=_du_lmp_ip)

# #CU
_cu_oam_ip = "10.57.165.4"
_f1m = NetworkAddress(v4="172.16.5.100", v6="xxxx", vlan_id=1862)
_f1c = NetworkAddress(v4="172.16.15.100", v6="xxxx", vlan_id=1863)
_f1u = NetworkAddress(v4="172.16.25.100", v6="xxxx", vlan_id=1864)
_x2c = NetworkAddress(v4="10.57.159.138", v6="xxxx", vlan_id=10)
_x2u = NetworkAddress(v4="10.57.159.139", v6="xxxx", vlan_id=10)
_s1c = NetworkAddress(v4="10.57.159.138", v6="xxxx", vlan_id=10)
_s1u = NetworkAddress(v4="10.57.159.139", v6="xxxx", vlan_id=10)
_tracing = NetworkAddress(v4="172.16.4.109", v6="xxxx", vlan_id=1316)

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
    tracing=_tracing,
)

# cloud
_control = ControlNode(
    open_stack_connection_details=OpenStackConnectionDetails(
        ip_addr="10.57.166.244",
        username="nokiauser",
        tenant="FiveG",
        password="HZnoki@123!",
        port=5000,
        protocol="https",
        version="v3",
    ),
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.166.244", username="nokiauser", password="HZnoki@123!"
    ),
    bmc_connection_details=BmcConnectionDetails(
        addr="5.5.5.5", username="admin", password="admin"
    ),
)

_osp = OSP(
    compute_nodes=[],
    control_nodes=[_control],
    version="osp_16",
    cloud_deployments=None,
)

# #cloudbts
_cbts_flavor = DeploymentFlavorStack(
    name="mmw-sg02-tl124-flavor",
    env_files=[
        os.path.join(_cfg_dir, "5gbts_flavor.env"),
        os.path.join(_cfg_dir, "config_flavor_ci.env"),
    ],
    yaml_file=os.path.join(_cfg_dir, "5gbts_flavor.yaml"),
    default_vnf_prefix="cbts_prefix",
)

_cbts_net = DeploymentNetworkStack(
    name="tl124_ext_net",
    env_files=os.path.join(_cfg_dir, "config_ext_net_ci.env"),
    yaml_file=os.path.join(_cfg_dir, "5gbts_ext_net.yaml"),
)

_cbts_vnf = DeploymentVnfStack(
    name="mmw-sg02-tl124-vnfc",
    env_files=[
        os.path.join(_cfg_dir, "5gbts_heat.env"),
        os.path.join(_cfg_dir, "config_bts_ci.env"),
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

_cbts = CloudBts(
    dus=[_du],
    cu=_cu,
    vnf_name=_cbts_vnf.name,
    cloud_deployment=_cloud_deployment,
    instance_id="0",
    global_bts_id="1",
)

_cbam = Cbam(
    addr="10.57.165.11",
    client_id="auto_mmw2",
    client_secret="8584aa54-8abd-4efb-8bb0-cf4824694457",
)

# #cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

# CI_Detail_UE_Type=''

# TestLine
_tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    cloud_hostings=[_osp],
    enbs=[_lte_real_enb],
    cbam=_cbam,
    tl_cloud_topology=_tl_cloud_topology,
)
tl = _tl
