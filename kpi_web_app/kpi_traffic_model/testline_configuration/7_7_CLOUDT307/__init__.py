import os

__maintainer__ = "Tomasz Krol"
__email__ = "tomasz.krol@nokia.com"

from taf.config.cbts import create_configuration_data
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    TelnetConnectionDetails,
    BmcConnectionDetails,
    OpenStackConnectionDetails,
)
from taf.config.testline.gnb import CU, DU
from taf.config.testline import (
    NetworkAddress,
    RU,
    CloudBts,
    CloudDeployment,
    DeploymentVnfStack,
    DeploymentNetworkStack,
    DeploymentFlavorStack,
    NCIR,
    ComputeNode,
    ControlNode,
    EPCSim,
)
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.pdu import PduPort, ATEN
from taf.config.testline.enb import RealEnb
from taf.config.testline.radio import RadioTypes

# The most commonly used testline configuration. #
_test_pc_gnb_default_ssh_connection_details = SshServiceDetails(
    addr="7-7-CLOUDT307.sc5g.krk-lab.nsn-rdnet.net", username="ute", password="ute"
)

_test_pc_enb_default_ssh_connection_details = SshServiceDetails(
    addr="7-7-CLOUDT007.sc5g.krk-lab.nsn-rdnet.net", username="ute", password="ute"
)

_ncir_control0_ip = "10.83.245.1"

_gnb_oam_ip = NetworkAddress(
    v4="10.83.250.5",
    vlan_id=503,
)

_gnb_instance_id = 307
_gnb_global_bts_id = 1
_gnb_du_common_unit_hardwarde_type = "ASIK"
_gnb_ru_ip = NetworkAddress(v4="192.168.253.150")
_gnb_ru_hw_group = RadioTypes.AEUA

_enb_oam_ip = NetworkAddress(v4="172.16.2.7")
_enb_instance_id = 7
_enb_global_bts_id = 7
_enb_du_common_unit_hardware_type = "ASIA"
_enb_du_capacity_unit_hardware_type = "ABIA"

_cu_name = "Nemuadmin"
_cu_password = "nemuuser"

##############################################################
# Default values
_default_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
)

_default_oam_ssh_connection = SshServiceDetails(
    addr=_gnb_oam_ip.v4,
    username="robot",
    password="rastre1",
)

_default_oam_http_connection = HttpConnectionDetails(
    addr=_gnb_oam_ip.v4,
    username="Nemuadmin",
    password="nemuuser",
)
##############################################################


# Important!: check below and change if other than default #

# Test PCs
_test_pc_gnb = TestPc(
    default_ssh_connection_details=_test_pc_gnb_default_ssh_connection_details
)
_test_pc_enb = TestPc(
    default_ssh_connection_details=_test_pc_enb_default_ssh_connection_details
)

# cloud section
# Needed only for test line added to CM
# _CFG_DIR = os.path.dirname(os.path.abspath(__file__))
# vnf_env_files = [os.path.join(_CFG_DIR, '5gbts_heat.env')]
# vnf_config = create_configuration_data(vnf_env_files, deep_merge_enabled=False)
#
# _control_0 = ControlNode(
#     open_stack_connection_details=OpenStackConnectionDetails(
#         ip_addr=_ncir_control0_ip,
#         username='admin',
#         tenant='admin',
#         password='uteadmin'),
#     default_ssh_connection_details=SshServiceDetails(
#         addr=_ncir_control0_ip,
#         username='wrsroot',
#         password='uteadmin'),
#     bmc_connection_details=BmcConnectionDetails(
#         addr='10.0.0.0',
#         username='admin',
#         password='admin'))
#
# _compute = ComputeNode(
#     bmc_connection_details=BmcConnectionDetails(
#         addr='10.0.0.0',
#         username='admin',
#         password='admin')
# )
#
# _ncir = NCIR(
#     compute_nodes=[_compute],
#     control_nodes=[_control_0],
#     version='ncir_19')
#
# _cbts_flavor = DeploymentFlavorStack(
#     name='Flavors',
#     env_files=[os.path.join(_CFG_DIR, '5gbts_flavor.env')],
#     yaml_file=os.path.join(_CFG_DIR, '5gbts_flavor.yaml'),
#     default_vnf_prefix='c2800_T02')
#
# _cbts_net = DeploymentNetworkStack(
#     name='Networks_307',
#     env_files=[os.path.join(_CFG_DIR, '5gbts_ext_net.env')],
#     yaml_file=os.path.join(_CFG_DIR, '5gbts_ext_net.yaml'))
#
# _cbts_vnf = DeploymentVnfStack(
#     name='VNF_307',
#     env_files=[os.path.join(_CFG_DIR, '5gbts_heat.env')],
#     yaml_file=os.path.join(_CFG_DIR, '5gbts_heat.yaml'),
#     configuration_data=vnf_config)
#
# _cloud_deployment = CloudDeployment(
#     default_cfg_dir=_CFG_DIR,
#     flavors=[_cbts_flavor],
#     networks=[_cbts_net],
#     vnfs=[_cbts_vnf],
#     cloud_hosting=_ncir)

# eNB section

_du_lmp_connection_enb = _default_ssh_lmp_connection
_du_lmp_connection_enb.proxy = _test_pc_enb_default_ssh_connection_details

_du_capacity_unit_enb = CapacityUnit(
    addr="192.168.253.22",
    hardware_type=_enb_du_capacity_unit_hardware_type,
    hardware_version="M02",
)

_du_common_unit_enb = CommonUnit(
    lmp_connection=_du_lmp_connection_enb,
    capacity_units=[_du_capacity_unit_enb],
    hardware_type=_enb_du_common_unit_hardware_type,
    hardware_version="M01",
)

_airscale_enb = Airscale(common_units=[_du_common_unit_enb])

_enb = RealEnb(
    system_module=_airscale_enb,
    oam_ip=_enb_oam_ip,
    instance_id=_enb_instance_id,
    global_bts_id=_enb_global_bts_id,
    x2_link_addr=_enb_oam_ip,
)

# gNB section

_cu_gnb = CU(
    backhaul_site_oam_ip=_gnb_oam_ip.v4,
    oam_ssh_connection_details=_default_oam_ssh_connection,  # replace if other than default
    oam_http_connection_details=_default_oam_http_connection,  # replace if other than default
    f1m=_gnb_oam_ip,
    f1c=_gnb_oam_ip,
    f1u=_gnb_oam_ip,
    x2c=_gnb_oam_ip,
    x2u=_gnb_oam_ip,
    instance_id=220000,
    global_bts_id=1,
)

_du_lmp_connection_gnb = _default_ssh_lmp_connection
_du_lmp_connection_gnb.proxy = _test_pc_gnb_default_ssh_connection_details

_abil_master_gnb = CapacityUnit(addr="192.168.253.20", hardware_type="ABIL")

_du_common_unit_gnb = CommonUnit(
    lmp_connection=_du_lmp_connection_gnb,
    capacity_units=[_abil_master_gnb],
    hardware_type=_gnb_du_common_unit_hardwarde_type,
    hardware_version="M02",
)

_ru_gnb = RU(
    ru_hw_group=_gnb_ru_hw_group,
    default_ssh_connection_details=SshServiceDetails(
        addr=_gnb_ru_ip.v4,
        username="root",
        password="umniedziala",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="root", password="umniedziala"
    ),
    pdu_port=PduPort(pdu=ATEN(addr="1.1.1.1", port_numbers=[1, 2]), port_no=1),
)

_airscale_gnb = Airscale(common_units=[_du_common_unit_gnb])

_du0_gnb = DU(
    airscale=_airscale_gnb,
    rus=[_ru_gnb],
    instance_id=307,
    global_bts_id=1,
    oam_ip="10.83.251.1",
    f1_m_ip_addr=_gnb_oam_ip.v4,
    f1_c_ip_addr=_gnb_oam_ip.v4,
    f1_u_ip_addr=_gnb_oam_ip.v4,
)

_du1_gnb = DU(
    airscale=_airscale_gnb,
    rus=[_ru_gnb],
    instance_id=22,
    global_bts_id=1,
    oam_ip="10.44.2.229",
    f1_m_ip_addr=_gnb_oam_ip.v4,
    f1_c_ip_addr=_gnb_oam_ip.v4,
    f1_u_ip_addr=_gnb_oam_ip.v4,
)


_cbts = CloudBts(
    cu=_cu_gnb,
    cloud_deployment=None,  # _cloud_deployment,
    vnf_name="VNF_307",
    dus=[_du0_gnb, _du1_gnb],
)

_core = EPCSim(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-cloudt007.sc5g.krk-lab.nsn-rdnet.net", username="ute", password="ute"
    ),
    dir_path="/home/ute/epcsim",
    cfg_filename="sim1.cfg",
    mme_ip="172.16.2.2",
    mcc="244",
    mnc="8",
    tac=1024,
    edaemon_port=10000,
    egate_port=60001,
)

# Testline

tl = TestLine(
    test_pc=_test_pc_gnb,
    core=_core,
    enbs=[_enb],
    gnbs=[_cbts],
    # cloud_hostings=[_ncir],
    tl_cloud_topology="CLOUD_5G",
)

__all__ = ["tl"]
