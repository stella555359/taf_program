__maintainer__ = "Aleksander Lagierski"
__team__ = "I_MN_5G_SC_PZ_SC_5G_VRF_GMS"
__email__ = "I_MN_5G_SC_PZ_SC_5G_VRF@internal.nsn.com"
__owner_email__ = "aleksander.lagiersk@nokia.com"

import os
from taf.config.testline.testpc import TestPc
from taf.config.testline import RU, DU, RoutingInformation
from taf.config.testline.pdu import PduPort, FPFH
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU
from taf.config.testline.airscale import CommonUnit, CapacityUnit, Airscale  # , SlotId
from taf.config.testline.core import EPCSim
from taf.config.testline.enb import RealEnb
from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.config.testline.cloud_hosting import (
    ControlNode,
    NCIR,
    CloudDeployment,
    DeploymentFlavorStack,
    DeploymentNetworkStack,
    DeploymentVnfStack,
    ComputeNode,
)
from taf.config.testline.connection_details import (
    SshServiceDetails,
    OpenStackConnectionDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
)

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT191.sc5g.krk-lab.nsn-rdnet.net",
        username="ute",
        password="uteUTE!",
    )
)

_compute = ComputeNode(
    bmc_connection_details=BmcConnectionDetails(
        addr="10.44.196.175", username="admin", password="admin"
    )
)
_control_0 = ControlNode(
    open_stack_connection_details=OpenStackConnectionDetails(
        ip_addr="10.83.190.225",
        username="5Guser1",
        tenant="5Gtenant1",
        password="5Guser@7",
        protocol="https",
    ),
    default_ssh_connection_details=SshServiceDetails(
        addr="10.83.190.225", username="5Guser1", password="5Guser@7"
    ),
    bmc_connection_details=BmcConnectionDetails(
        addr="1.1.1.1", username="admin", password="admin"
    ),
)

_ru_pdu = FPFH(
    port_numbers=[1],
    addr="FPFH-GL05-1.sc5g-leg.krk-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

_ru_1 = RU(
    ru_hw_group="hw_group",
    radio_type="AEUD",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.253.150", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="TO_UPDATE", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru_pdu.pdu_ports[1],
    serial_number="L1193108297",
)

_ncir = NCIR(compute_nodes=[_compute], control_nodes=[_control_0], version="ncir_19")

_cbts_flavor = DeploymentFlavorStack(
    name="TL_7_7_UTE5GCLOUDT191_FLAVOR",
    env_files=[os.path.join(_CFG_DIR, "5gbts_flavor.env")],
    yaml_file=os.path.join(_CFG_DIR, "5gbts_flavor.yaml"),
    default_vnf_prefix="gNB191",
)

_cbts_net = DeploymentNetworkStack(
    name="TL_7_7_UTE5GCLOUDT191_EXT_NET",
    env_files=[os.path.join(_CFG_DIR, "5gbts_ext_net.env")],
    yaml_file=os.path.join(_CFG_DIR, "5gbts_ext_net.yaml"),
)

_cbts_vnf = DeploymentVnfStack(
    name="TL_7_7_UTE5GCLOUDT191_BTS",
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

_cu_f1c_ip = NetworkAddress(
    v4="172.16.5.102/24", routing_v4=RoutingInformation(gateway="172.16.5.1")
)
_cu_f1u_ip = NetworkAddress(
    v4="172.16.5.103/24", routing_v4=RoutingInformation(gateway="172.16.5.1")
)
_cu_x2c_ip = NetworkAddress(
    v4="172.16.2.101/24", routing_v4=RoutingInformation(gateway="172.16.2.1")
)
_cu_x2u_ip = NetworkAddress(
    v4="172.16.2.102/24", routing_v4=RoutingInformation(gateway="172.16.2.1")
)
_cu_s1u_ip = NetworkAddress(
    v4="172.16.2.102/24", routing_v4=RoutingInformation(gateway="172.16.2.1")
)

_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.83.182.191/23", routing_v4=RoutingInformation(gateway="10.83.183.254")
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.83.182.191", username="robot", password="rastre1"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.83.182.191", username="Nemuadmin", password="nemuuser"
    ),
    f1c=_cu_f1c_ip,
    x2c=_cu_x2c_ip,
    f1u=_cu_f1u_ip,
    x2u=_cu_x2u_ip,
    s1u=_cu_s1u_ip,
    global_bts_id=75191,
    instance_id=75191,
)

_du_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc.default_ssh_connection_details,
)

_du_capacity_unit = CapacityUnit(
    addr="192.168.253.36",
    hardware_type="ABIL",
    hardware_version="A02",
    # slot_id=SlotId.B4,
)


_common_unit_pdu = FPFH(
    port_numbers=[6],
    addr="FPFH-GL03-6.sc5g-leg.krk-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

_du_common_unit = CommonUnit(
    lmp_connection=_du_lmp_connection,
    capacity_units=[_du_capacity_unit],
    hardware_type="ASIK",
    hardware_version="A01",
    pdu_port=PduPort(pdu=_common_unit_pdu, port_no=6),
    # slot_id=SlotId.C2,
)

_airscale = Airscale(common_units=[_du_common_unit])

_gnb_oam_ip = NetworkAddress(
    v4="10.83.252.191/23",
    routing_v4=RoutingInformation(gateway="10.83.252.254", destIpAddr="10.83.183.254"),
    vlan_id=541,
)

_f1_ip = NetworkAddress(
    v4="172.16.5.60/24",
    routing_v4=RoutingInformation(gateway="172.16.5.0", destIpAddr="172.16.5.1"),
    vlan_id=1691,
)

_du = DU(
    airscale=_airscale,
    rus=[_ru_1],
    oam_ip=_gnb_oam_ip.v4.split("/")[0],
    f1_m_ip_addr=_gnb_oam_ip,
    f1_c_ip_addr=_f1_ip,
    f1_u_ip_addr=_f1_ip,
    global_bts_id=75191,
    instance_id=75191,
)

_cbts = CloudBts(
    cu=_cu, cloud_deployment=_cloud_deployment, vnf_name="gNB191", dus=[_du]
)

_core = EPCSim(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT191.sc5g.krk-lab.nsn-rdnet.net",
        username="ute",
        password="uteUTE!",
    ),
    dir_path="/home/ute/epcsim",
    cfg_filename="sim.cfg",
    mme_ip="172.16.2.191",
    mcc=244,
    mnc=8,
    tac=1024,
    edaemon_port=10000,
    egate_port=60001,
)

_lteenb = RealEnb(x2_link_addr=NetworkAddress(v4="172.16.2.250"))

tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    enbs=[_lteenb],
    core=_core,
    cloud_hostings=[_ncir],
    tl_cloud_topology="CLOUD_5G_ASIKR_ABILB4_AEUD",
)

__all__ = ["tl"]
