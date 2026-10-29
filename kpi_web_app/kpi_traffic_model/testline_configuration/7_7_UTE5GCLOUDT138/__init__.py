__maintainer__ = "Kamil Gorski"
__team__ = "MN 5G&SC mmW&SC Pz KRK 5 SG"
__email__ = "OO_MN_5G_SC_MMW_SC_PZ_KRK_5_SG_1001325@internal.nsn.com"
__owner_email__ = "kamil.gorski@nokia.com"

import os
from taf.config.testline.testpc import TestPc
from taf.config.testline import DU, RU
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CU
from taf.config.testline.airscale import CommonUnit, Airscale, CapacityUnit
from taf.config.testline.gnb.gnb import CloudBts
from taf.config.testline.gnb.networkaddress import NetworkAddress
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
from taf.config.testline.pdu import FPFH, PduPort


_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

_asod_pdu = FPFH(
    addr="10.253.166.21",
    port_numbers=[1, 2, 3, 4, 5, 6],
    login="admin",
    password="admin",
    model="FPFH",
)

_test_pc_gnb_default_ssh_connection_details = SshServiceDetails(
    addr="7-7-UTE5GCLOUDT138.sc5g.krk-lab.nsn-rdnet.net",
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

_du_capacity_unit = CapacityUnit(addr="192.168.253.20")

_asod_du = CommonUnit(
    lmp_connection=_du_lmp_connection_gnb,
    capacity_units=[_du_capacity_unit],
    hardware_type="ASOD",
    pdu_port=PduPort(pdu=_asod_pdu, port_no=4),
)

_airscale = Airscale(common_units=[_asod_du])

_ru_du0 = RU(
    ru_hw_group="",
    radio_type="AEUD",
    default_ssh_connection_details=SshServiceDetails(addr="", username=""),
)

_du0 = DU(
    airscale=_airscale,
    rus=[_ru_du0],
)

_cu_m_route_du = NetworkAddress(v6="2a00:8a02:60:1c::1:138/112")

_cu_x2c_route_du = NetworkAddress(v6="2a00::138:111/112")

_cu_x2u_route_du = NetworkAddress(v6="2a00::138:112/112")

_cu_s1u_route_du = NetworkAddress(v6="2a00::138:112/112")

_cu_f1c_route_du = NetworkAddress(v6="2a00::287:102/112")

_cu_f1u_route_du = NetworkAddress(v6="2a00::287:103/112")

_cu = CU(
    backhaul_site_oam_ip=_cu_m_route_du,
    oam_ssh_connection_details=SshServiceDetails(
        addr="2a00:8a02:60:1c::1:138", username="robot", password="rastre1"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="[2a00:8a02:60:1c::1:138]", username="Nemuadmin", password="nemuuser"
    ),
    f1m=_cu_m_route_du,
    f1c=_cu_f1c_route_du,
    f1u=_cu_f1u_route_du,
    x2c=_cu_x2c_route_du,
    x2u=_cu_x2u_route_du,
    s1u=_cu_s1u_route_du,
)

_compute = ComputeNode(
    bmc_connection_details=BmcConnectionDetails(addr="", username="", password="")
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

_ncir = NCIR(compute_nodes=[_compute], control_nodes=[_control_0], version="ncir_19")

_cbts_flavor = DeploymentFlavorStack(
    name="TL_7_7_UTE5GCLOUDT138_FLAVOR",
    env_files=[os.path.join(_CFG_DIR, "config_flavor.env")],
    yaml_file=os.path.join(_CFG_DIR, "5gbts_flavor.yaml"),
    default_vnf_prefix="5gbts-138",
)
_cbts_net = DeploymentNetworkStack(
    name="TL_7_7_UTE5GCLOUDT138_EXT_NET",
    env_files=[os.path.join(_CFG_DIR, "config_ext_net.env")],
    yaml_file=os.path.join(_CFG_DIR, "5gbts_ext_net.yaml"),
)
_cbts_vnf = DeploymentVnfStack(
    name="TL_7_7_UTE5GCLOUDT138_BTS",
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
_gnb = CloudBts(
    cloud_deployment=_cloud_deployment,
    vnf_name="5gbts-138",
    cu=_cu,
    dus=[_du0],
)

_gnb.m_plane = NetworkAddress(v4="172.17.5.200", v6="[2000:1:2:3:4:5:6:138]")

_gnb.primary_autoconnection_parameters = NetworkAddress(
    v6="[2a00::287:30]",
    vlan_id=1638,
    routing_v6="[2a00::287:12]",
)
_gnb.secondary_autoconnection_parameters = NetworkAddress(
    v4="172.17.5.30",
    vlan_id=1787,
    routing_v4="172.17.5.138",
)
_gnb.primary_prefix_length = 112

_gnb.secondary_prefix_length = 24

tl = TestLine(
    test_pc=_test_pc_gnb,
    gnbs=[_gnb],
    cloud_hostings=[_ncir],
    tl_cloud_topology="CLOUD_5G_ASOD_AEUD_QOS_ENB_IPv6",
)

tl.ute_cplane_address = "2a00::287:12"
tl.ute_uplane_address = "2000:1:2:3:4:5:7:11"
tl.ute_mplane_address = "2000:1:2:3:4:5:6:191"

tl.gnb_cplane_address = "2a00::287:62"
tl.gnb_uplane_address = "2a00::287:72"
tl.gnb_uplane_address_2 = "2000:1:2:3:4:5:7:72"
tl.gnb_mplane_address = "2000:1:2:3:4:5:6:138"

tl.ip_address_version = "6"
tl.ip_address_prefix = "112"

tl.gnb_friendly_name = "7_7_UTE5GCLOUDT138"
tl.mrbts_name = "MRBTS-138"

tl.ip_913A_102r1 = "2000:1:2:3:4:5:6:0"

tl.ip_913A_103r1 = "2000:1:2:3:4:5:6:0"

tl.ip_913A_104r1 = "2017::0"
tl.ip_913A_104r4 = "2014::14"
tl.ip_913A_104r5 = "2014::15"
tl.ip_913A_104r6 = "2111::11"
tl.ip_913A_104r7 = "2111::12"
tl.ip_913A_104r8 = "2222::0"

tl.ip_913A_106r2 = "2000:1:2:3:4:5:6:138"
tl.ip_913A_106r3 = "2a00::287:0"
tl.ip_913A_107r2 = "2000:1:2:3:4:5:6:138"
tl.ip_913A_107r3 = "2a00::287:0"

__all__ = ["tl"]
