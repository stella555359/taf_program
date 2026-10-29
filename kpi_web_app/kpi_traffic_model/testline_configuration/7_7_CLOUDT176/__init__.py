__maintainer__ = "Daniel Wenecki"
__team__ = "I_MN_5G_SC_MMW_SC_PZ_KRK_5_SG_TEST_GMS"
__email__ = "I_MN_5G_SC_MMW_SC_PZ_KRK_5_SG_TEST@internal.nsn.com"
__owner_email__ = "daniel.wenecki@nokia.com"

import os
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import (
    SshServiceDetails,
    OpenStackConnectionDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.cloud_hosting import (
    NCIR,
    ControlNode,
    CloudDeployment,
    DeploymentFlavorStack,
    DeploymentNetworkStack,
    DeploymentVnfStack,
)
from taf.config.testline.gnb import CloudBts, CU, DU
from taf.config.testline.pdu import APC, PduPort
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.config.testline import RU, RealEnb

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

# DU 176 is connected to port 3, DU 301 is connected to port 6
_pdu = APC(addr="10.253.166.21", port_numbers=[6])

_common_unit_pdu_port1 = PduPort(pdu=_pdu, port_no=6)

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="sc5g-enb-301.sc5g.krk-lab.nsn-rdnet.net", username="ute", password="ute"
    )
)


_cbts_flavors = DeploymentFlavorStack(
    name="Flavors_176",
    env_files=[os.path.join(_CFG_DIR, "5gbts_flavour.env")],
    yaml_file=os.path.join(_CFG_DIR, "5gbts_flavour.yaml"),
    default_vnf_prefix="5gbts-176",
)

_cbts_nets = DeploymentNetworkStack(
    name="Networks_176",
    env_files=[os.path.join(_CFG_DIR, "5gbts_ext_net.env")],
    yaml_file=os.path.join(_CFG_DIR, "5gbts_ext_net.yaml"),
)

_cbts_vnf = DeploymentVnfStack(
    name="VNF_176",
    env_files=[os.path.join(_CFG_DIR, "5gbts_heat.env")],
    yaml_file=os.path.join(_CFG_DIR, "5gbts_heat.yaml"),
)

# _control = ControlNode(
#     open_stack_connection_details=OpenStackConnectionDetails(
#         ip_addr='10.83.190.243',
#         username='sb14user1',
#         tenant='SB14tenant1',
#         password='Sb14pwd@1',
#         version='v3',
#         protocol='http'),
#     default_ssh_connection_details=SshServiceDetails(
#         addr='10.83.190.243',
#         username='sb14user1',
#         password='sb14user1'),
#     bmc_connection_details=BmcConnectionDetails(
#         addr='1.1.1.1',
#         username='dummy',
#         password='dummy'
#     )
# )

_ncir = NCIR(
    compute_nodes=[],
    # control_nodes=[_control],
    control_nodes=[],
    version="osp_10",
)

_cloud_deployment = CloudDeployment(
    default_cfg_dir=_CFG_DIR,
    flavors=[_cbts_flavors],
    networks=_cbts_nets,
    vnfs=[_cbts_vnf],
    cloud_hosting=_ncir,
)

_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(v4="10.83.182.176"),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.83.182.176", username="robot", password="rastre1"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.83.182.176", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(v4="172.16.2.101", vlan_id=2676),
    x2u=NetworkAddress(v4="172.16.2.101", vlan_id=2676),
    instance_id=176,
    global_bts_id=176,
)

_ru = RU(
    ru_hw_group="5Ggen3_HighF_2T2R",
    radio_type="AEUA",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="root", password="umniedziala"
    ),
)
# lmp_connection=SshServiceDetails(addr='192.168.1.1',
#                                  username='root',
#                                  password='umniedziala')
# )

_capacity_unit = CapacityUnit(addr="192.168.253.20")

_common_unit_1 = CommonUnit(
    SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_capacity_unit],
    pdu_port=_common_unit_pdu_port1,
)

_airscale_1 = Airscale([_common_unit_1])

_du_1 = DU(
    airscale=_airscale_1,
    rus=[_ru],
    f1_c_ip_addr=NetworkAddress(v4="172.16.5.61", vlan_id=2676),
    f1_u_ip_addr=NetworkAddress(v4="172.16.5.61", vlan_id=2676),
    f1_m_ip_addr=NetworkAddress(v4="10.83.251.6", vlan_id=539),
    instance_id=301,
    global_bts_id=301,
)

_cbts = CloudBts(
    cu=_cu, dus=[_du_1], cloud_deployment=_cloud_deployment, vnf_name="5gbts_176"
)

_lteenb = RealEnb(
    airscale=_du_1, x2_link_addr=NetworkAddress(v4="172.16.2.101", vlan_id=2676)
)

tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    enbs=[_lteenb],
    ues=None,
    cloud_hostings=[_ncir],
    tl_cloud_topology="CLOUD_5G_ASIKL_ABILB1_AEUA_20B",
    pdus=[_pdu],
)

__all__ = ["tl"]
