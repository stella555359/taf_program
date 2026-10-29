__maintainer__ = "QT NPS"
__team__ = "MN 5G_RAN Pz NPS CI"
__email__ = "5G_NPS_CI@nokia.com"


import os
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.cloud_hosting import (
    ControlNode,
    NCIR,
    CloudDeployment,
    DeploymentFlavorStack,
    DeploymentNetworkStack,
    DeploymentVnfStack,
)
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
)
from taf.config.testline.core import EPCSim
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.ue import AirphoneCloud, Airphone
from taf.config.testline.ue import Prisma
from taf.config.testline.core import PrismaCore
from taf.config.testline import PrismaEnb
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from collections import OrderedDict


########################################################
TL_NPS_name = "TL43"
TL_name = "7_20_QT" + TL_NPS_name
IPV = "IPV4"
# MODEM_BOARD='ABIL'  #ABIL   ABIK
asik_addr_webui = "10.14.63.35"
asik_addr = "10.14.63.35"
asik_username = "toor4nsn"
asik_password = "oZPS0POrRieRtu"
########################################################


_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.28.1.165", username="ute", password="ute"
    )
)

_lmp_connection = SshServiceDetails(
    addr=asik_addr, username="toor4nsn", password="oZPS0POrRieRtu"
)


_cu = CU(
    backhaul_site_oam_ip=asik_addr,
    oam_ssh_connection_details=SshServiceDetails(
        addr=asik_addr, username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(addr=asik_addr_webui),
)

capacity_unit = CapacityUnit(addr="6.6.6.6")

_common_unit = CommonUnit(
    lmp_connection=_lmp_connection, capacity_units=[capacity_unit]
)

_airscale = Airscale(common_units=[_common_unit])

_du = DU(airscale=_airscale, rus=[])


_cbts = ClassicalBts(cu=_cu, dus=[_du])

# _epcsim = EPCSim(
#    mme_ip='10.5.113.203',
#    mcc=-1,
#    mnc=-1,
#    tac=-1,
#    default_ssh_connection_details=SshServiceDetails(
#        addr='10.5.113.203',
#        username='ute',
#        password='ute'),
#    dir_path='/home/ute/lteemu_June18',
#    cfg_filename='TL10_basic_wts_step1.cfg')


_EIF1_connection_Asik1 = SshServiceDetails(
    addr="192.168.2.60", username="toor4nsn", password="oZPS0POrRieRtu"
)


# WEBUI Anthentication
WEBUI_USER = "Nemuadmin"
WEBUI_USER_NAME = "Nemuadmin"
WEBUI_PASSWORD = "nemuuser"

# Control_pc_info for gNB
# pc_addr = '10.14.57.204'
# pc_username = 'cv5g1_2'
# pc_password = '@udreyH5G'


# rf_addr = '172.16.1.5'        #rf ip
# rf_username = 'root'
# rf_password = 'umniedziala'


# prisma relevant setting
_airmosaic_ssh = SshServiceDetails(
    addr="135.238.24.246", username="ftps5g", password="Fr@TelS6"
)
_airmosaic_harness = HttpConnectionDetails(addr="135.238.24.246", port=8090)
# _airmosaic_ssh = SshServiceDetails(
#    addr='10.14.39.57',
#    username='localuser',
#    password='10c@1user')
# _airmosaic_harness = HttpConnectionDetails(addr='10.14.39.57', port=8090)
#
_lsu_uu_ssh = SshServiceDetails(addr="10.28.0.252", username="user", password="user")
_tstm_uu_ssh = SshServiceDetails(addr="10.28.0.252", username="user", password="user")

_prisma_ue = Prisma(
    airmosaic_ssh_connection_details=_airmosaic_ssh,
    airmosaic_harness_connection_details=_airmosaic_harness,
    lsu_uu_ssh_connection_details=_lsu_uu_ssh,
    tstm_uu_ssh_connection_details=_tstm_uu_ssh,
)

_lsu_s1_ssh = SshServiceDetails(addr="10.28.0.252", username="user", password="user")
_tstm_s1_ssh = SshServiceDetails(addr="10.28.0.252", username="user", password="user")

_prisma_core = PrismaCore(
    lsu_s1_ssh_connection_details=_lsu_s1_ssh,
    tstm_s1_ssh_connection_details=_tstm_s1_ssh,
)


tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    core=_prisma_core,
    ues=[_prisma_ue],
    tl_cloud_topology=TL_NPS_name,
)


tl = TestlineWrapper(tl)

tl2 = TestLine(
    test_pc=None, gnbs=None, tl_cloud_topology=None, core=_prisma_core, ues=[_prisma_ue]
)

lmp_connection = _lmp_connection
EIF1_connection_Asik1 = _EIF1_connection_Asik1


# please define the key-value mapping dict like the order like below
_swpool_tools = "/ffs/run/swpool/TOOLS/"
_5G_L1NODE = "/ffs/run/swpool/5G/L1NODE/"
_5G_L1PLTF = "/ffs/run/swpool/5G/L1PLTF/"
_swpool_5g = "/ffs/run/swpool/5G/"
path_map_file_dict = OrderedDict()
path_map_file_dict[_swpool_tools] = ["lfs-install-helper"]
path_map_file_dict[_5G_L1NODE] = ["*.bin"]
path_map_file_dict[_5G_L1PLTF] = ["5GL1SW.itb"]
path_map_file_dict[_swpool_5g] = ["default-install.sh"]

# variables for install loner package
loner_name = "5GL1SW.tgz"
local_modify_file_path = _CFG_DIR
swconfig_path = os.path.join(_CFG_DIR, "WA_file", "swconfig_local.txt")
oamagentjs_path = os.path.join(_CFG_DIR, "WA_file", "oamagentjs.tgz")

# powerswitch for ASIK
# powerstation_ip = '10.5.113.126'
# user:administrator ,passwd:uteadmin
# powerstation_asik_port = 2 . moved to robotws5g

SVN_PATH = "/home/ute/svn/trunk"
SW_PATH = "/home/ute/sw_download"
edaemon_port = "22222"
egate_port = "33333"

# classical_eoc_filename = '5g_pid12_classical_l2rt_eoc.json'
asik_swconfig_path = os.path.join(_CFG_DIR, "WA_file", "swconfig.txt")
# asik_eoc_path = os.path.join(_CFG_DIR, 'WA_file', classical_eoc_filename)

# For test compatibility
cfg_dir = _CFG_DIR
lmp_connection = _lmp_connection
# __all__ = [
#     'tl',
#     'tl2'
#     ]
__all__ = ["tl"]
