__maintainer__ = "Jakub Kupiec"
__team__ = "5G_PZ_MMW_KRK_4_SG"
__email__ = "jakub.kupiec@nokia.com"

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
from taf.config.testline import DU, RU
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline import NetworkAddress
from taf.config.testline.pdu import FPFH

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT190.sc5g.krk-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
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
    name="TL_7_7_UTE5GCLOUDT190_FLAVOR",
    env_files=[os.path.join(_CFG_DIR, "5gbts_flavor.env")],
    default_vnf_prefix="5gbts-190",
)

_cbts_net = DeploymentNetworkStack(
    name="TL_7_7_UTE5GCLOUDT190_EXT_NET",
    env_files=[os.path.join(_CFG_DIR, "5gbts_ext_net.env")],
)

_cbts_vnf = DeploymentVnfStack(
    name="TL_7_7_UTE5GCLOUDT190_BTS",
    env_files=[os.path.join(_CFG_DIR, "5gbts_heat.env")],
)

_cloud_deployment = CloudDeployment(
    default_cfg_dir=_CFG_DIR,
    flavors=[_cbts_flavor],
    networks=[_cbts_net],
    vnfs=[_cbts_vnf],
    cloud_hosting=_ncir,
)

_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(v4="10.83.182.190"),  # '10.83.182.143',
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.83.182.190", username="robot", password="rastre1"  # '10.83.182.143',
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.83.182.190",  # '10.83.182.143',
        username="Nemuadmin",
        password="nemuuser",
    ),
    instance_id=190,
    global_bts_id=190,
)
_asik_du_1_pdu = FPFH(addr="10.253.166.50", port_numbers=[5], login="admin", password="admin")

_abil1_du1 = CapacityUnit(addr="192.168.253.20", hardware_type="ABIL")

_asik_du1 = CommonUnit(
    pdu_port=_asik_du_1_pdu.pdu_ports[5],
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_abil1_du1],
    hardware_type="ASIK"
)

_ru_du1 = RU(
    ru_hw_group="",
    default_ssh_connection_details=SshServiceDetails(addr="", username=""),
    lmp_connection=SshServiceDetails(addr="", username=""),
    radio_type="AEUD",
)

_gnb_oam_ip = NetworkAddress(v4="10.83.251.4")

_du1 = DU(
    airscale=Airscale(common_units=[_asik_du1]),
    instance_id=75190,
    global_bts_id=75190,
    rus=[_ru_du1],
    oam_ip=_asik_du1.lmp_connection.addr,
    f1_m_ip_addr=_gnb_oam_ip.v4,
    f1_c_ip_addr=_gnb_oam_ip.v4,
    f1_u_ip_addr=_gnb_oam_ip.v4,
)

_cbts = CloudBts(
    cu=_cu, cloud_deployment=_cloud_deployment, vnf_name="5gbts-190", dus=[_du1]
)

_enb_capacity_unit = CapacityUnit(
    addr="",
    hardware_type=""
)

_enb_common_unit = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_enb_capacity_unit],
    hardware_type="ASIK"
)

tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    cloud_hostings=[_ncir],
    tl_cloud_topology="CLOUD_5G_ASIKL_ABILB1_AEUD",
)

__all__ = ["tl"]
