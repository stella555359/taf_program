__maintainer__ = "Krystian Lachut"
__team__ = "5G_PZ_MMW_KRK_2_SG"
__email__ = "krystian.lachut@nokia.com"


import os
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import (
    SshServiceDetails,
    OpenStackConnectionDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    TelnetConnectionDetails,
)
from taf.config.testline.gnb import CloudBts, CU, DU
from taf.config.testline import NetworkAddress, RU
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.pdu import PduPort, ATEN
from taf.config.testline.enb import RealEnb
from taf.config.testline import SC5GRadio
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    SCRadioConnectionDetails,
    TelnetConnectionDetails,
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

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

_test_pc_gnb_default_ssh_connection_details = SshServiceDetails(
    addr="7-7-CLOUDT389.sc5g.krk-lab.nsn-rdnet.net", username="ute", password="ute"
)

_test_pc_enb_default_ssh_connection_details = SshServiceDetails(
    addr="7-7-CLOUDT389.sc5g.krk-lab.nsn-rdnet.net", username="ute", password="ute"
)

_gnb_oam_ip = NetworkAddress(v4="192.168.255.129")
_gnb_instance_id = 389
_gnb_global_bts_id = 389
_gnb_du_common_unit_hardwarde_type = "ASIK"
_gnb_ru_ip = NetworkAddress(v4="192.168.254.49")
_gnb_ru_hw_group = "AEUD"

_default_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
)

_default_oam_http_connection = HttpConnectionDetails(
    addr=_gnb_oam_ip.v4,
    username="Nemuadmin",
    password="nemuuser",
)

_test_pc_gnb = TestPc(
    default_ssh_connection_details=_test_pc_gnb_default_ssh_connection_details
)
_test_pc_enb = TestPc(
    default_ssh_connection_details=_test_pc_enb_default_ssh_connection_details
)

_control_0 = ControlNode(
    open_stack_connection_details=OpenStackConnectionDetails(
        ip_addr="10.83.190.225",
        username="5Guser1",
        tenant="5Gtenant1",
        password="5Guser@3",
    ),
    default_ssh_connection_details=SshServiceDetails(
        addr="10.83.190.225", username="5Guser1", password="5Guser@3"
    ),
    bmc_connection_details=BmcConnectionDetails(addr="", username="", password=""),
)

_compute = ComputeNode(
    bmc_connection_details=BmcConnectionDetails(addr="", username="", password="")
)

_ncir = NCIR(compute_nodes=[_compute], control_nodes=[_control_0], version="ncir_19")

_cbts_flavor = DeploymentFlavorStack(
    name="TL_7_7_UTE5GCLOUDT389_FLAVOR",
    env_files=[os.path.join(_CFG_DIR, "5gbts_flavor.env")],
    yaml_file=os.path.join(_CFG_DIR, "5gbts_flavor.yaml"),
    default_vnf_prefix="5gbts-389",
)

_cbts_net = DeploymentNetworkStack(
    name="TL_7_7_UTE5GCLOUDT389_EXT_NET",
    env_files=[os.path.join(_CFG_DIR, "5gbts_ext_net.env")],
    yaml_file=os.path.join(_CFG_DIR, "5gbts_ext_net.yaml"),
)

_cbts_vnf = DeploymentVnfStack(
    name="TL_7_7_UTE5GCLOUDT389_BTS",
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

_f1c = NetworkAddress(v4="172.16.5.102", v6="xxxx", vlan_id=2)

_cu = CU(
    backhaul_site_oam_ip="10.83.183.139",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.83.183.139", username="robot", password="rastre1"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.83.183.139", username="Nemuadmin", password="nemuuser"
    ),
    instance_id=2957,
    f1c=_f1c,
    global_bts_id=1,
)

_du_lmp_connection_gnb = _default_ssh_lmp_connection
_du_lmp_connection_gnb.proxy = _test_pc_gnb_default_ssh_connection_details

_abil_master_gnb = CapacityUnit(addr="192.168.253.20")
_abil_slave_gnb = CapacityUnit(addr="192.168.253.21")
_abil_loner_gnb = CapacityUnit(addr="192.168.253.22")

_asik_du1 = CommonUnit(
    lmp_connection=_du_lmp_connection_gnb,
    capacity_units=[_abil_master_gnb, _abil_slave_gnb, _abil_loner_gnb],
    hardware_type=_gnb_du_common_unit_hardwarde_type,
    hardware_version="M01",
)

_ru_du1 = RU(
    default_ssh_connection_details=SshServiceDetails(addr="", username=""),
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    radio_type="AEUD",
    ru_hw_group="ASIR-HUB",
    pdu_port=PduPort(pdu=ATEN(addr="1.1.1.1", port_numbers=[1, 2]), port_no=1),
)

_du1 = DU(
    Airscale(common_units=[_asik_du1]),
    instance_id=389,
    global_bts_id=389,
    rus=[_ru_du1],
    oam_ip="10.83.251.15",
    f1_m_ip_addr=_gnb_oam_ip.v4,
    f1_c_ip_addr=_gnb_oam_ip.v4,
    f1_u_ip_addr=_gnb_oam_ip.v4,
)

_cbts = CloudBts(
    cu=_cu, cloud_deployment=_cloud_deployment, vnf_name="5gbts-389", dus=[_du1]
)

_enb = RealEnb(
    oam_ip=NetworkAddress(v4="192.168.255.129"),
    instance_id=1,
    global_bts_id=1,
    x2_link_addr=NetworkAddress(v4="192.168.255.129"),
)

tl = TestLine(
    test_pc=_test_pc_gnb,
    test_pcs=[_test_pc_enb],
    gnbs=[_cbts],
    cloud_hostings=[_ncir],
    tl_cloud_topology="CLOUD_5G_ASIKR_ABILB4_AEUD",
    enbs=[_enb],
)

__all__ = ["tl"]
