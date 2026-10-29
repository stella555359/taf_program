__maintainer__ = "Shobha K Reddy"
__team__ = "I_MN_ECE_BLR_RD_TST_SQD_ELECTRON_GMS "
__email__ = "I_MN_ECE_BLR_RD_TST_SQD_ELECTRON@internal.nsn.com"

import os
from taf.config.testline.gnb import CloudBts, CU, DU
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
    TelnetConnectionDetails,
    SCRadioConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.core import EPCSim, LTEEmuCore, PrismaCore
from taf.config.testline import Airphone, AirphoneCloud, IPHY, TM500, Qualcomm, Prisma
from taf.config.testline.traffic_generators import ParagonX, Caffeine
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.config.testline.pdu import RRB
from taf.config.testline.attenuator import AttenuationPort
from taf.config.testline.nms import Netact
from taf.config.testline.enb import RealEnb, LTEEmuEnb, PrismaEnb, DocomoEnb
from taf.config.testline.hardware_controller import GPSPowerHardwareController
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline import RU, SC5GRadio, SC4GRadio, NetworkAddress

# **********************************************************************************
_network_address = NetworkAddress(v4="0.0.0.0", v6=None, vlan_id=703)
# **********************************************************************************
_CFG_DIR = os.path.dirname(os.path.abspath(__file__))
# **********************************************************************************
_pdu = RRB(addr="10.43.206.94", port_numbers=[3, 4])
# **********************************************************************************
_lteSim = LTEEmuEnb(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.43.204.103",
        username="ute",
        password="ute",
        port=22,
        private_key=None,
        proxy=None,
    ),
    dir_path="/home/ute/wts771",
    cfg_filename="basic_wts_step2.cfg",
)
# ********************************Airphone(UE)**************************************
_control_1 = ControlNode(
    open_stack_connection_details=OpenStackConnectionDetails(
        ip_addr="10.43.206.75",
        username="admin",
        tenant="admin",
        password="test123",
        port=5000,
        protocol="https",
        version="v3",
    ),
    default_ssh_connection_details=SshServiceDetails(
        addr="10.43.206.75",
        username="wrsroot",
        password="Fiveg@123",
        port=22,
        private_key=None,
        proxy=None,
    ),
    bmc_connection_details=BmcConnectionDetails(
        addr="10.43.206.68", username="admin", password="admin", type=None, port=443
    ),
)

_ncir_ap = NCIR(compute_nodes=[], control_nodes=[_control_1], version="ncir_17A")

_airphone_flavor = DeploymentFlavorStack(
    name="flavors_ap",
    env_files=[os.path.join(_CFG_DIR, "5gap_flavor.env")],
    yaml_file=[os.path.join(_CFG_DIR, "5gap_flavor.yaml")],
    default_vnf_prefix="5gbts",
)

_airphone_net = DeploymentNetworkStack(
    name="extnet_ap",
    env_files=[os.path.join(_CFG_DIR, "5gap_ext_net.env")],
    yaml_file=os.path.join(_CFG_DIR, "5gap_ext_net.yaml"),
)

_airphone_vnf = DeploymentVnfStack(
    name="stack_ap",
    env_files=[os.path.join(_CFG_DIR, "5gap_heat.env")],
    yaml_file=os.path.join(_CFG_DIR, "5gap_heat.yaml"),
)

airphone_deployment = CloudDeployment(
    default_cfg_dir=_CFG_DIR,
    flavors=[_airphone_flavor],
    networks=[_airphone_net],
    vnfs=[_airphone_vnf],
    cloud_hosting=_ncir_ap,
)

_airphone_cloud = AirphoneCloud(
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.125.2",
        username="robot",
        password="rastre1",
        port=22,
        private_key=None,
        proxy=None,
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.125.2", username="Nemuadmin", password="nemuuser"
    ),
)

_ap_capacity_unit_1 = CapacityUnit(addr="192.168.253.84")

ap_common_unit_1 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.2", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_ap_capacity_unit_1],
    pdu_port=_pdu.pdu_ports[4],
)

_l1 = Airscale(common_units=[ap_common_unit_1])

_l3 = SshServiceDetails(
    addr="10.43.206.88",
    username="robot",
    password="rastre1",
    port=22,
    private_key=None,
    proxy=None,
)

_l2 = SshServiceDetails(
    addr="10.43.206.88",
    username="robot",
    password="rastre1",
    port=22,
    private_key=None,
    proxy=None,
)

_egate = SshServiceDetails(
    addr="0.0.0.0",
    username="user2",
    password="password2",
    port=22,
    private_key=None,
    proxy=None,
)

_airphone = Airphone(
    egate=_egate,
    l3_ssh_connection_details=_l3,
    l2_ssh_connection_details=_l2,
    l1=_l1,
    edaemon_port=20000,
    egate_port=10000,
    l3_port=7777,
    airphone_cloud=_airphone_cloud,
    deployment_configuration="C",
)
# **********************************************************************************
_tl_cloud_topology = "CLOUD_5G_BB3"
# **********************************RealEnb*****************************************
_capacity_unit_9 = CapacityUnit(addr="192.168.253.20")

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.99", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_capacity_unit_9],
)
_airscale1 = Airscale(common_units=[_common_unit_2])

_lteenb = RealEnb(airscale=_airscale1, x2_link_addr="192.168.4.111")
# **********************************************************************************
_epcsim = EPCSim(
    mme_ip="192.168.4.120",
    default_ssh_connection_details=SshServiceDetails(
        addr="10.43.204.103",
        username="ute",
        password="ute",
        port=22,
        private_key=None,
        proxy=None,
    ),
    dir_path="/home/ute/wts",
    cfg_filename="basic_wts_step2.cfg",
    mcc=311,
    mnc=489,
    tac=333,
    edaemon_port=22222,
    egate_port=10000,
)
# *******************************NCIR***********************************************
_control_0 = ControlNode(
    open_stack_connection_details=OpenStackConnectionDetails(
        ip_addr="10.43.206.75",
        username="admin",
        tenant="admin",
        password="test123",
        port=5000,
        protocol="https",
        version="v3",
    ),
    default_ssh_connection_details=SshServiceDetails(
        addr="10.43.206.75",
        username="wrsroot",
        password="Fiveg@123",
        port=22,
        private_key=None,
        proxy=None,
    ),
    bmc_connection_details=BmcConnectionDetails(
        addr="10.43.206.68", username="admin", password="admin", type=None, port=443
    ),
)
_ncir = NCIR(compute_nodes=[], control_nodes=[_control_0], version="ncir_17a")
# ********************************gNB***********************************************
_cbts_flavor = DeploymentFlavorStack(
    name="flavors_gnb",
    env_files=[os.path.join(_CFG_DIR, "5gbts_flavor.env")],
    yaml_file=[os.path.join(_CFG_DIR, "5gbts_flavor.yaml")],
    default_vnf_prefix="5gbts",
)

_cbts_net = DeploymentNetworkStack(
    name="extnet_gnb",
    env_files=[os.path.join(_CFG_DIR, "5gbts_ext_net.env")],
    yaml_file=os.path.join(_CFG_DIR, "5gbts_ext_net.yaml"),
)

_cbts_vnf = DeploymentVnfStack(
    name="stack_gnb",
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
    backhaul_site_oam_ip="192.168.125.10",
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.125.10",
        username="robot",
        password="rastre1",
        port=22,
        private_key=None,
        proxy=None,
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.125.10", username="Nemuadmin", password="nemuuser", port=443
    ),
    f1m="192.168.2.111",
    f1c="192.168.2.112",
    f1u="192.168.2.113",
    x2c="192.168.4.111",
    x2u="192.168.4.112",
    s1c="192.168.4.111",
    s1u="192.168.4.113",
    tracing=None,
)
# ABIL
_capacity_unit_1 = CapacityUnit(addr="192.168.253.20")

_common_unit_0 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.3",  # ethlmp0
        username="toor4nsn",
        password="oZPS0POrRieRtu",
        port=22,
        private_key=None,
        proxy=None,
    ),
    capacity_units=[_capacity_unit_1],
    pdu_port=_pdu.pdu_ports[3],
)
# DU
_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale)  # If ru is not present then you do not have to add it here

_cbts = CloudBts(
    dus=[_du], cu=_cu, cloud_deployment=_cloud_deployment, vnf_name="tl02-5gbts19"
)
# **********************************************************************************
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.43.204.103",
        username="ute",
        password="ute",
        port=22,
        private_key=None,
        proxy=None,
    )
)
# **********************************************************************************
tl = TestLine(
    test_pc=_host,
    gnbs=[_cbts],
    cloud_hostings=[_ncir],
    core=_epcsim,
    enbs=[_lteenb, _lteSim],
    tl_cloud_topology=_tl_cloud_topology,
    ues=[_airphone],
    pdus=[_pdu],
)

__all__ = ["tl"]
