__maintainer__ = "Kamil Pielka"
__team__ = "MN RAN Pz KRK 7 SG"
__email__ = "I_5G_PZ_MMW_KRK_7SG_TEST@internal.nsn.com"
__owner_email__ = "kamil.pielka@nokia.com"

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
from taf.config.testline import DU, RU, Netact, NOM, RoutingInformation
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline import NetworkAddress, RealEnb
from taf.config.testline.pdu import FPFH, PduPort

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))


_test_pc_gnb_default_ssh_connection_details = SshServiceDetails(
    addr="7-7-UTE5GCLOUDT287.sc5g.krk-lab.nsn-rdnet.net",
    username="ute",
    password="ute",
)

_test_pc_gnb = TestPc(
    default_ssh_connection_details=_test_pc_gnb_default_ssh_connection_details
)

_default_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
)

_du_lmp_connection_gnb = _default_ssh_lmp_connection
_du_lmp_connection_gnb.proxy = _test_pc_gnb_default_ssh_connection_details

_du0_pdu = FPFH(
    addr="10.253.166.21",
    port_numbers=[1, 2, 3, 4, 5, 6],
    login="admin",
    password="admin",
    model="FPFH",
)

_cu_m_route_du = NetworkAddress(v6="2a00:8a02:60:1c:0:0:1:287/112")

_cu_x2c_route_du = NetworkAddress(v6="2a00::138:1111/112")

_cu_x2u_route_du = NetworkAddress(v6="2a00::138:1112/112")

_cu_s1u_route_du = NetworkAddress(v6="2a00::138:1112/112")

_cu_f1c_route_du = NetworkAddress(v6="2a00::287:1102/112")

_cu_f1u_route_du = NetworkAddress(v6="2a00::287:1103/112")

_du_m_ip = NetworkAddress(
    v6="2000:1:2:3:4:5:6:287/112",
    routing_v6=RoutingInformation(gateway="2000:1:2:3:4:5:6:0/112"),
    vlan_id=1787,
)

_oam_ip = NetworkAddress(v4="192.168.255.129")

_du_f1c_ip = NetworkAddress(
    v6="2a00::287:61/112",
    routing_v6=RoutingInformation(gateway="2a00::287:1102/112"),
    vlan_id=1638,
)

_du_f1u_ip = NetworkAddress(
    v6="2000:1:2:3:4:5:7:71/112",
    routing_v6=RoutingInformation(gateway="2a00::287:1103/112"),
    vlan_id=1287,
)

_du_m_route_cu = NetworkAddress(
    routing_v6=RoutingInformation(gateway="2000:1:2:3:4:5:6:0/112")
)

_du_f1c_route_cu = NetworkAddress(
    routing_v6=RoutingInformation(gateway="2a00::287:1102/112")
)

_du_f1u_route_cu = NetworkAddress(
    routing_v6=RoutingInformation(gateway="2a00::287:1103/112")
)

_control_0 = ControlNode(
    open_stack_connection_details=OpenStackConnectionDetails(
        ip_addr="10.83.190.225",
        username="5Guser1",
        tenant="5Gtenant1",
        password="5Guser@10",
    ),
    default_ssh_connection_details=SshServiceDetails(
        addr="10.83.190.225", username="5Guser1", password="5Guser@10"
    ),
    bmc_connection_details=BmcConnectionDetails(addr="", username="", password=""),
)

_compute = ComputeNode(
    bmc_connection_details=BmcConnectionDetails(addr="", username="", password="")
)

_ncir = NCIR(compute_nodes=[_compute], control_nodes=[_control_0], version="ncir_19")

_cbts_flavor = DeploymentFlavorStack(
    name=None,
    env_files=[os.path.join(_CFG_DIR, "5gbts_flavor.env")],
    yaml_file=os.path.join(_CFG_DIR, "5gbts_flavor.yaml"),
    default_vnf_prefix="5gbts-138-287",
)

_cbts_net = DeploymentNetworkStack(
    name=None,
    env_files=[os.path.join(_CFG_DIR, "5gbts_ext_net.env")],
    yaml_file=os.path.join(_CFG_DIR, "5gbts_ext_net.yaml"),
)

_cbts_vnf = DeploymentVnfStack(
    name=None,
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
    backhaul_site_oam_ip=_cu_m_route_du,
    oam_ssh_connection_details=SshServiceDetails(
        addr="2a00:8a02:60:1c::1:287", username="robot", password="rastre1"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="[2a00:8a02:60:1c::1:287]", username="Nemuadmin", password="nemuuser"
    ),
    f1m=_cu_m_route_du,
    f1c=_cu_f1c_route_du,
    f1u=_cu_f1u_route_du,
    x2c=_cu_x2c_route_du,
    x2u=_cu_x2u_route_du,
    s1u=_cu_s1u_route_du,
)

_du0_capacity_unit = CapacityUnit(addr="192.168.253.20")

_asik_du0 = CommonUnit(
    lmp_connection=_du_lmp_connection_gnb,
    capacity_units=[_du0_capacity_unit],
    pdu_port=PduPort(pdu=_du0_pdu, port_no=5),
    hardware_type="ASIK",
)

_airscale = Airscale(common_units=[_asik_du0])

_ru_du0 = RU(
    ru_hw_group="",
    radio_type="AEUB",
    default_ssh_connection_details=SshServiceDetails(addr="", username=""),
)

_du0 = DU(
    airscale=_airscale,
    instance_id=1,
    global_bts_id=75287,
    rus=[_ru_du0],
    oam_ip=_oam_ip,
    f1_m_ip_addr=_du_m_ip,
    f1_c_ip_addr=_du_f1c_ip,
    f1_u_ip_addr=_du_f1u_ip,
    f1_m_cu=_du_m_route_cu,
    f1_c_cu=_du_f1c_route_cu,
    f1_u_cu=_du_f1u_route_cu,
)

_cbts = CloudBts(
    cu=_cu, cloud_deployment=_cloud_deployment, vnf_name="5gbts-287", dus=[_du0]
)

_cbts.m_plane = NetworkAddress(v4="172.16.5.61", v6="[2000:1:2:3:4:5:6:287]")
_cbts.primary_autoconnection_parameters = NetworkAddress(
    v6="[2a00::287:32]",
    vlan_id=1638,
    routing_v6="[2a00::287:190]",
)
_cbts.secondary_autoconnection_parameters = NetworkAddress(
    v4="172.17.5.32",
    vlan_id=1787,
    routing_v4="172.16.5.3",
)
_cbts.primary_prefix_length = 112
_cbts.secondary_prefix_length = 24

tl = TestLine(
    test_pc=_test_pc_gnb,
    gnbs=[_cbts],
    cloud_hostings=[_ncir],
    tl_cloud_topology="CLOUD_5G_ASIK_ABIL_AEUB_QOS_ENB_IPv6",
)

__all__ = ["tl"]

tl.ute_cplane_address = "2a00::287:190"
tl.ute_uplane_address = "2000:1:2:3:4:5:7:190"
tl.ute_mplane_address = "2000:1:2:3:4:5:6:190"

tl.gnb_cplane_address = "2a00::287:61"
tl.gnb_uplane_address = "2a00::287:71"
tl.gnb_uplane_address_2 = "2000:1:2:3:4:5:7:71"
tl.gnb_mplane_address = "2000:1:2:3:4:5:6:287"

tl.ip_address_version = "6"
tl.ip_address_prefix = "112"

tl.gnb_friendly_name = "7_7_UTE5GCLOUDT287"
tl.mrbts_name = "MRBTS-75287"

tl.ip_913A_102r1 = "2000:1:2:3:4:5:6:0"
tl.ip_913A_103r1 = "2000:1:2:3:4:5:6:0"

tl.ip_913A_104r1 = "2017::0"
tl.ip_913A_104r4 = "2014::14"
tl.ip_913A_104r5 = "2014::15"
tl.ip_913A_104r6 = "2111::11"
tl.ip_913A_104r7 = "2111::12"
tl.ip_913A_104r8 = "2222::0"

tl.ip_913A_106r2 = "2000:1:2:3:4:5:6:287"
tl.ip_913A_106r3 = "2a00::287:0"
tl.ip_913A_107r2 = "2000:1:2:3:4:5:6:287"
tl.ip_913A_107r3 = "2a00::287:0"
