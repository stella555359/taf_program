__maintainer__ = "Krzysztof Domino"
__team__ = "5G_PZ_MMW_KRK_3_SG"
__email__ = "krzysztof.domino@nokia.com"

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
from taf.config.testline.pdu import FPFH

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

_cu_m_route_du = NetworkAddress(
    v4="10.83.183.217",
)
_cu_x2c_route_du = NetworkAddress(
    v4="172.16.2.161",
)
_cu_x2u_route_du = NetworkAddress(
    v4="172.16.2.162",
)
_cu_s1u_route_du = NetworkAddress(
    v4="172.16.2.162",
)
_cu_f1c_route_du = NetworkAddress(
    v4="172.16.5.102",
)
_cu_f1u_route_du = NetworkAddress(
    v4="172.16.5.103",
)
_du_m_ip = NetworkAddress(
    v4="172.16.5.60",
    v6="2a00:2222:2222:2222:2222:2222:2222:467",
    routing_v4=RoutingInformation(gateway="172.16.5.254", ip_prefix_length=24),
)
_oam_ip = NetworkAddress(v4="192.168.255.129")
_du_f1c_ip = NetworkAddress(
    v4="172.16.5.60",
    routing_v4=RoutingInformation(gateway="172.16.5.102", ip_prefix_length=24),
)
_du_f1u_ip = NetworkAddress(
    v4="172.16.5.60",
    routing_v4=RoutingInformation(gateway="172.16.5.103", ip_prefix_length=24),
)
_du_m_route_cu = NetworkAddress(
    routing_v4=RoutingInformation(gateway="172.16.5.254", ip_prefix_length=0)
)
_du_f1c_route_cu = NetworkAddress(
    routing_v4=RoutingInformation(gateway="172.16.5.102", ip_prefix_length=24)
)
_du_f1u_route_cu = NetworkAddress(
    routing_v4=RoutingInformation(gateway="172.16.5.103", ip_prefix_length=24)
)

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT467.sc5g.krk-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_control_0 = ControlNode(
    open_stack_connection_details=OpenStackConnectionDetails(
        ip_addr="10.83.190.241",
        username="sb14user1",
        tenant="SB14tenant1",
        password="5Guser@7",
    ),
    default_ssh_connection_details=SshServiceDetails(
        addr="10.83.190.241", username="sb14user1", password="5Guser@6"
    ),
    bmc_connection_details=BmcConnectionDetails(addr="", username="", password=""),
)

_compute = ComputeNode(
    bmc_connection_details=BmcConnectionDetails(addr="", username="", password="")
)

_ncir = NCIR(compute_nodes=[_compute], control_nodes=[_control_0], version="ncir_19")

_cbts_flavor = DeploymentFlavorStack(
    name="TL_7_7_UTE5GCLOUDT467_FLAVOR",
    env_files=[os.path.join(_CFG_DIR, "config_flavor.env")],
    yaml_file=os.path.join(_CFG_DIR, "5gbts_flavor.yaml"),
    default_vnf_prefix="5gbts-467",
)

_cbts_net = DeploymentNetworkStack(
    name="TL_7_7_UTE5GCLOUDT467_EXT_NET",
    env_files=[os.path.join(_CFG_DIR, "config_ext_net.env")],
    yaml_file=os.path.join(_CFG_DIR, "5gbts_ext_net.yaml"),
)

_cbts_vnf = DeploymentVnfStack(
    name="TL_7_7_UTE5GCLOUDT467_BTS",
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
        addr="10.83.183.217", username="robot", password="rastre1"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.83.183.217", username="Nemuadmin", password="nemuuser"
    ),
    f1m=_cu_m_route_du,
    f1c=_cu_f1c_route_du,
    f1u=_cu_f1u_route_du,
    x2c=_cu_x2c_route_du,
    x2u=_cu_x2u_route_du,
    s1u=_cu_s1u_route_du,
)

_pdu1 = FPFH(
    port_numbers=[3],
    addr="10.253.166.99",
    login="admin",
    password="admin",
)

_abil1_du1 = CapacityUnit(addr="192.168.253.20")

_asod_du1 = CommonUnit(
    pdu_port=_pdu1.pdu_ports[3],
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_abil1_du1],
)

_ru_du1 = RU(
    ru_hw_group="",
    default_ssh_connection_details=SshServiceDetails(addr="", username=""),
    lmp_connection=SshServiceDetails(addr="", username=""),
    radio_type="AEUD",
)

_du1 = DU(
    Airscale(common_units=[_asod_du1]),
    rus=[_ru_du1],
    oam_ip=_oam_ip,
    f1_m_ip_addr=_du_m_ip,
    f1_c_ip_addr=_du_f1c_ip,
    f1_u_ip_addr=_du_f1u_ip,
    f1_m_cu=_du_m_route_cu,
    f1_c_cu=_du_f1c_route_cu,
    f1_u_cu=_du_f1u_route_cu,
)

_cbts = CloudBts(
    cu=_cu,
    cloud_deployment=_cloud_deployment,
    vnf_name="5gbts-467",
    dus=[_du1],
    instance_id=467,
    global_bts_id=2957,
)

_enb = RealEnb(
    oam_ip=NetworkAddress(v4="172.16.2.8"),
    instance_id=10008,
    global_bts_id=10008,
    x2_link_addr=NetworkAddress(v4="172.16.2.8"),
)

_netAct = Netact(
    addr="10.43.115.148",
    nom=NOM(
        ssh_connections_info=SshServiceDetails(
            addr="10.42.115.148", username="5gsc", password="Qwer_1234"
        )
    ),
)

_lss = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.83.178.2", username="coam", password="zO&n1W*ktp7"
    ),
    connections=[
        NetworkAddress(v4="172.16.5.121", v6="2a00:2222:2222:2222:2222:2222:2222:150"),
        NetworkAddress(v4="10.83.177.28", v6="2a00:8a02:60:3a:5054:f2ff:fef2:1e0"),
    ],
)

tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    test_pcs=[_lss],
    cloud_hostings=[_ncir],
    tl_cloud_topology="CLOUD_5G_ASOD_AEUD",
    nms=_netAct,
    enbs=[_enb],
)

__all__ = ["tl"]
