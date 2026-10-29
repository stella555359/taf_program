__maintainer__ = "QT NPS"
__team__ = "MN 5G RAN Pz NPS CI"
__email__ = "I_MN_5GRAN_CI_PS_RDTEAM@groups.nokia.com"


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
from taf.config.testline.gnb import CloudBts, CU, DU
from taf.config.testline.core import EPCSim
from taf.config.testline.ue import Airphone
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.compatibility.configuration import TestlineWrapper

from taf.config.cbts import create_configuration_data
from taf.config.testline.ue import Prisma
from taf.config.testline.core import PrismaCore
from taf.config.testline import PrismaEnb
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
)


_CFG_DIR = os.path.dirname(os.path.abspath(__file__))
TL_NPS_name = "CV07"
TL_name = "7_20_QT" + TL_NPS_name

asik_addr = "192.168.2.60"

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.5.112.42", username="ute", password="ute"
    )
)

# TODO check login/pass
_control_0 = ControlNode(
    open_stack_connection_details=OpenStackConnectionDetails(
        ip_addr="10.14.57.208", username="wrsroot", tenant="admin", password="uteadmin"
    ),
    default_ssh_connection_details=SshServiceDetails(
        addr="10.14.57.208", username="admin", password="uteadmin"
    ),
    bmc_connection_details=BmcConnectionDetails(addr="", username="", password=""),
)


_ncir = NCIR(compute_nodes=[], control_nodes=[_control_0], version="ncir_17A")

flavor_env_files = [os.path.join(_CFG_DIR, "5gbts_flavor.env")]
flavor_config = create_configuration_data(flavor_env_files)

net_env_files = [os.path.join(_CFG_DIR, "5gbts_ext_net.env")]
net_config = create_configuration_data(net_env_files)

# STATIC
# vnf_env_files = [os.path.join(_CFG_DIR, '5gbts_heat.env')]
# vnf_config = create_configuration_data(vnf_env_files)

# MERGE
vnf_env_files = [
    os.path.join(_CFG_DIR, "5gbts_heat.env"),
    os.path.join(_CFG_DIR, "5gbts_heat_QT.env"),
]
# vnf_config = create_configuration_data(vnf_env_files)


_cbts_flavor = DeploymentFlavorStack(
    name="flavor_" + TL_NPS_name,
    env_files=flavor_env_files,
    # yaml_file=os.path.join(_CFG_DIR, '5gbts_flavor_aio.yaml'),  #not used
    # for CV07
    yaml_file=os.path.join(_CFG_DIR, "5gbts_flavor.yaml"),
    configuration_data=flavor_config,
    default_vnf_prefix="cv07-5gbts",
)

_cbts_net = DeploymentNetworkStack(
    name="net_" + TL_NPS_name,
    env_files=net_env_files,
    yaml_file=os.path.join(_CFG_DIR, "5gbts_ext_net.yaml"),
    configuration_data=net_config,
)

_cbts_vnf = DeploymentVnfStack(
    name="deploy_" + TL_NPS_name,
    env_files=vnf_env_files,
    # STATIC
    #    yaml_file=os.path.join(_CFG_DIR, '5gbts_heat.yaml'),
    #    configuration_data=vnf_config)
    # MERGE
    yaml_file=os.path.join(_CFG_DIR, "5gbts_heat.yaml"),
)
#    configuration_data=vnf_config)


_cloud_deployment = CloudDeployment(
    default_cfg_dir=_CFG_DIR,
    flavors=[_cbts_flavor],
    networks=[_cbts_net],
    vnfs=[_cbts_vnf],
    cloud_hosting=_ncir,
)


_cu = CU(
    backhaul_site_oam_ip="10.14.48.07",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.14.48.07", username="robot", password="rastre1"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.14.48.07", username="Nemuadmin", password="nemuuser"
    ),
)

_lmp_connection = SshServiceDetails(
    addr=asik_addr, username="toor4nsn", password="oZPS0POrRieRtu"
)

capacity_unit = CapacityUnit(addr="6.6.6.6")

_common_unit = CommonUnit(
    lmp_connection=_lmp_connection, capacity_units=[capacity_unit]
)

_airscale = Airscale(common_units=[_common_unit])

_du = DU(airscale=_airscale, rus=[])

_cbts = CloudBts(
    cu=_cu, dus=[_du], cloud_deployment=_cloud_deployment, vnf_name=TL_NPS_name
)
#      vnf_name='5gbts')


_EIF1_connection_Asik1 = SshServiceDetails(
    addr="192.168.2.60", username="toor4nsn", password="oZPS0POrRieRtu"
)


# _epcsim = EPCSim( mme_ip='192.168.4.120', mcc=311, mnc=489, tac=333,
#    default_ssh_connection_details=SshServiceDetails(addr='10.42.68.44', username='ute', password='ute'),
#    dir_path='/home/ute/Robot_LteEmu',
#    cfg_filename='Robot_LteEmu_Config')


# add param for  but need to clean and use TestLine object

# WEBUI Anthentication
WEBUI_USER = "Nemuadmin"
WEBUI_USER_NAME = "Nemuadmin"
WEBUI_PASSWORD = "nemuuser"

_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)


# TL_IP_info
asik_addr = "192.168.255.129"  # asik ip
asik_username = "toor4nsn"
asik_password = "oZPS0POrRieRtu"

# Control_pc_info for gNB
pc_addr = "10.14.57.204"
pc_username = "cv5g1_2"
pc_password = "@udreyH5G"

fsp_addr = "192.168.253.22"  # loner ip
fct_addr = "192.168.253.17"  # slave ip
fsp1a_addr = "192.168.253.20"  # abil master ip

rf_addr = "172.16.1.5"  # rf ip
rf_username = "root"
rf_password = "umniedziala"

# TestVM_IP_info
# host_addr = '10.14.34.175'
# host_username = 'root'
# host_password = 'root'


# prisma relevant setting
_airmosaic_ssh = SshServiceDetails(
    addr="10.14.57.212", username="cv5g1_2", password="@udreyH5G"
)
_airmosaic_harness = HttpConnectionDetails(addr="10.14.57.212", port=8090)
_lsu_uu_ssh = SshServiceDetails(addr="10.5.115.113", username="user", password="user")
_tstm_uu_ssh = SshServiceDetails(addr="10.5.115.113", username="user", password="user")

_prisma_ue = Prisma(
    airmosaic_ssh_connection_details=_airmosaic_ssh,
    airmosaic_harness_connection_details=_airmosaic_harness,
    lsu_uu_ssh_connection_details=_lsu_uu_ssh,
    tstm_uu_ssh_connection_details=_tstm_uu_ssh,
)

_lsu_s1_ssh = SshServiceDetails(addr="10.5.115.112", username="user", password="user")
_tstm_s1_ssh = SshServiceDetails(addr="10.5.115.112", username="user", password="user")

_prisma_core = PrismaCore(
    lsu_s1_ssh_connection_details=_lsu_s1_ssh,
    tstm_s1_ssh_connection_details=_tstm_s1_ssh,
)

# tl = TestLine(test_pc=None, gnbs=None, tl_cloud_topology=None, core=_prisma_core, ues=[_prisma_ue])

tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    cloud_hostings=[_ncir],
    tl_cloud_topology="CLOUD_5G_TYPE",
    core=_prisma_core,
    ues=[_prisma_ue],
)
tl = TestlineWrapper(tl)

tl2 = TestLine(
    test_pc=None, gnbs=None, tl_cloud_topology=None, core=_prisma_core, ues=[_prisma_ue]
)

cfg_dir = _CFG_DIR


lmp_connection = _lmp_connection
EIF1_connection_Asik1 = _EIF1_connection_Asik1


IPV = "IPV4"

# TODO to be modified

if IPV == "IPV4":
    #    WEBUI_URL = 'https://' + tl.cbts.oam.addr
    WEBUI_URL = "https://" + tl.gnbs[0].cu.oam_ssh_connection_details.addr
if IPV == "IPV6":
    #    WEBUI_URL = 'https://['+tl.cbts.oam.addr + ']'
    WEBUI_URL = "https://[" + tl.gnbs[0].cu.oam_ssh_connection_details.addr + "]"


# __all__ = [
#     'tl',
#     'tl2',
#     'lmp_connection']

__all__ = ["tl"]
