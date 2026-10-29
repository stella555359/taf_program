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

from taf.config.testline.pdu import ATEN, PduPort
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline import RU

from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.ue import AirphoneCloud, Airphone
from taf.config.testline.ue import Prisma
from taf.config.testline.core import PrismaCore

# from taf.config.testline.enb import PrismaEnb
from taf.config.testline import PrismaEnb
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from collections import OrderedDict


########################################################
TL_NPS_name = "TL17"
TL_name = "7_20_QT" + TL_NPS_name
IPV = "IPV4"
########################################################
# to be removed  ASAP   ( we lost optimizedrobotws5g  code  ??)
asik_addr_lmp = "10.14.62.97"
asik_addr_eif = "10.14.49.160"
asik_addr = asik_addr_lmp
# asik_addr = asik_addr_eif
asik_username = "toor4nsn"
asik_password = "oZPS0POrRieRtu"
#
# DEBUG   run fron TL CV35
# host_addr='10.5.114.94'
host_addr = "10.157.211.64"
host_username = "ute"
host_password = "ute"


_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr=host_addr, username="ute", password="ute"
    )
)


_du_lmp_connection = SshServiceDetails(
    addr=asik_addr_lmp, username="toor4nsn", password="oZPS0POrRieRtu"
)


_cu = CU(
    backhaul_site_oam_ip=asik_addr,
    oam_ssh_connection_details=SshServiceDetails(
        addr=asik_addr, username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr=asik_addr, username="Nemuadmin", password="nemuuser"
    ),
)


_du_capacity_unit = CapacityUnit(addr="6.6.6.6")
#          cpri_id='id')

_du_pdu = ATEN(addr="10.5.113.126", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9])

_du_pdu_port = PduPort(pdu=_du_pdu, port_no=2)

_du_common_unit = CommonUnit(
    lmp_connection=_du_lmp_connection,
    capacity_units=[_du_capacity_unit],
    pdu_port=_du_pdu_port,
)

_airscale = Airscale(common_units=[_du_common_unit])

# _du = DU(airscale=_airscale, rus=[_ru])
_du = DU(airscale=_airscale, rus=[])

_cbts = ClassicalBts(cu=_cu, dus=[_du])


# _ru_pdu = ATEN(
#    addr='',
#    port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9])

# _ru_pdu_port = PduPort(
#    pdu=_ru_pdu,
#    port_no=2)

# _ru = RU(
#    ru_hw_group='AEQD???',
#    default_ssh_connection_details=SshServiceDetails(
#        addr='1.1.1.1',
#        username='root',
#        password='umniedziala'),
#    lmp_connection=SshServiceDetails(
#        addr='1.1.1.1',
#        username='user5',
#        password='password5'),
#    pdu_port=_ru_pdu_port)

# TODO: remove AirPhone config or rename variable to distinguish gNB and AirPhone
_airphone_cloud = AirphoneCloud(
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.245", username="_rcpadmin", password="RCP_owner"
    ),
    oam_http_connection_details=HttpConnectionDetails(addr="192.168.255.245"),
)

_egate = SshServiceDetails(addr="0.0.0.0", username="user2", password="password2")

_l3 = SshServiceDetails(
    addr="192.168.255.245", username="_rcpadmin", password="RCP_owner"
)

_l2 = SshServiceDetails(
    addr="192.168.255.245", username="_rcpadmin", password="RCP_owner"
)

_lmp_connection = SshServiceDetails(
    addr=asik_addr_lmp, username="toor4nsn", password="oZPS0POrRieRtu"
)

capacity_unit = CapacityUnit(addr="6.6.6.6")

_common_unit = CommonUnit(
    lmp_connection=_lmp_connection, capacity_units=[capacity_unit]
)

_l1 = Airscale(common_units=[_common_unit])

_airphone = Airphone(
    egate=_egate,
    l3_ssh_connection_details=_l3,
    l2_ssh_connection_details=_l2,
    l1=_l1,
    airphone_cloud=_airphone_cloud,
)


_epcsim = EPCSim(
    mme_ip="10.5.112.66",
    mcc=-1,
    mnc=-1,
    tac=-1,
    default_ssh_connection_details=SshServiceDetails(
        addr="10.5.112.66", username="ute", password="ute"
    ),
    dir_path="/home/ute/3GPPDEC2",
    cfg_filename="basic_wts_step1.cfg",
)


tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    core=_epcsim,
    ues=[_airphone],
    tl_cloud_topology=TL_NPS_name,
)

tl = TestlineWrapper(tl)


Config_with_airphone = "True"


# please define the key-value mapping dict like the order like below
# _swpool_tools = "/ffs/run/swpool/TOOLS/"
# _5G_L1NODE = "/ffs/run/swpool/5G/L1NODE/"
# _5G_L1PLTF = "/ffs/run/swpool/5G/L1PLTF/"
# _swpool_5g = "/ffs/run/swpool/5G/"
# path_map_file_dict = OrderedDict()
# path_map_file_dict[_swpool_tools] = ["lfs-install-helper"]
# path_map_file_dict[_5G_L1NODE] = ["*.bin"]
# path_map_file_dict[_5G_L1PLTF] = ["5GL1SW.itb"]
# path_map_file_dict[_swpool_5g] = ["default-install.sh"]

# variables for install loner package
# loner_name = '5GL1SW.tgz'
# local_modify_file_path = _CFG_DIR
# swconfig_path = os.path.join(_CFG_DIR, 'WA_file', 'swconfig_local.txt')
# oamagentjs_path = os.path.join(_CFG_DIR, 'WA_file', 'oamagentjs.tgz')

# SVN_PATH = "/home/ute/svn/trunk"
# SW_PATH = "/home/ute/sw_download"


########################################################
fsp_addr = "192.168.253.22"
fct_addr = "192.168.253.17"
########################################################


########################################################
edaemon_port = "22224"
egate_port = "20000"
########################################################

# WMP_flag = False
# WMP_flag = True

# No RF on TL17
# rf_addr = '172.16.1.5'
# rf_username = 'root'
# rf_password = 'umniedziala'
# For test compatibility
cfg_dir = _CFG_DIR

__all__ = ["tl"]

# __all__ = ['tl','fct_addr' ,  'fsp_addr',  'edaemon_port' , 'egate_port' ,  'enb_id' , 'target_id' ]
