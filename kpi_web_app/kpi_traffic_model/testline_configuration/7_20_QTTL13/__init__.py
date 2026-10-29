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
from taf.config.testline.gnb import CloudBts, CU
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.ue import AirphoneCloud, Airphone
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.cbts import create_configuration_data

##################################################################
# NPS add on
TL_NPS_name = "TL13"
TL_name = "7_20_QT" + TL_NPS_name
# MODEM_BOARD='ABIL'  #ABIL   ABIK
##################################################################

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.5.112.41", username="ute", password="ute"
    )
)

_control = ControlNode(
    open_stack_connection_details=OpenStackConnectionDetails(
        ip_addr="10.14.33.84",
        username="wrsroot",
        tenant="admin",
        password="uteadmin5G!",
    ),
    default_ssh_connection_details=SshServiceDetails(
        addr="10.14.33.83", username="admin", password="uteadmin5G!"
    ),
    bmc_connection_details=BmcConnectionDetails(addr="", username="", password=""),
)


_ncir = NCIR(compute_nodes=[], control_nodes=[_control], version="ncir_17A")


# epcsim = EPCSim(
#    mme_ip='135.120.10.17',
#    default_ssh_connection_details=SshServiceDetails(
#        addr='135.120.10.17',
#        username='ute',
#        password='ute'
#    ),
#    dir_path='/home/ute/LTEemu_WTS_32Bits-core2-3252',
#    cfg_filename='TL10_basic_wts_step1.cfg')


_airphone_cloud = AirphoneCloud(
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.5.113.155", username="_rcpadmin", password="RCP_owner"
    ),
    oam_http_connection_details=HttpConnectionDetails(addr="10.5.113.155"),
)

_egate = SshServiceDetails(addr="0.0.0.0", username="user2", password="password2")

_l3 = SshServiceDetails(addr="10.5.113.155", username="_rcpadmin", password="RCP_owner")

_l2 = SshServiceDetails(addr="10.5.113.155", username="_rcpadmin", password="RCP_owner")

_lmp_connection = SshServiceDetails(
    # addr='10.14.32.66',
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
)

_lmp_connection2 = SshServiceDetails(
    addr="10.14.32.67", username="toor4nsn", password="oZPS0POrRieRtu"
)

_EIF1_connection_Asik1 = SshServiceDetails(
    addr="192.168.2.60", username="toor4nsn", password="oZPS0POrRieRtu"
)

_EIF1_connection_Asik2 = SshServiceDetails(
    addr="192.168.2.63", username="toor4nsn", password="oZPS0POrRieRtu"
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


flavor_env_files = [os.path.join(_CFG_DIR, "5gbts_flavor.env")]
flavor_config = create_configuration_data(flavor_env_files)

net_env_files = [os.path.join(_CFG_DIR, "5gbts_ext_net.env")]
net_config = create_configuration_data(net_env_files)

vnf_env_files = [
    os.path.join(_CFG_DIR, "5gbts_heat.env"),
    os.path.join(_CFG_DIR, "5gbts_heat_QT.env"),
]
# vnf_config = create_configuration_data(vnf_env_files)


_cbts_flavor = DeploymentFlavorStack(
    name="flavor_" + TL_NPS_name,
    env_files=flavor_env_files,
    yaml_file=os.path.join(_CFG_DIR, "5gbts_flavor_aio.yaml"),
    configuration_data=flavor_config,
    default_vnf_prefix="5gbts",
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
    backhaul_site_oam_ip="192.168.255.100",
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.100", username="robot", password="rastre1"
    ),
    oam_http_connection_details=HttpConnectionDetails(addr="192.168.255.100"),
)


_cbts = CloudBts(cu=_cu, cloud_deployment=_cloud_deployment, vnf_name=TL_NPS_name)

_epcsim = EPCSim(
    mme_ip="10.5.112.41",
    mcc=-1,
    mnc=-1,
    tac=-1,
    default_ssh_connection_details=SshServiceDetails(
        addr="10.5.112.41", username="ute", password="ute"
    ),
    dir_path="/opt/lteemu_SEP18_3GPP_32bits",
    cfg_filename="TL13_NSA-Step1_basic_cfg_LteEmu_309.cfg",
)


tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    # airphone=[_airphone],
    cloud_hostings=[_ncir],
    core=_epcsim,
    ues=[_airphone],
    tl_cloud_topology="CLOUD_5G_TYPE",
)
# print ( tl.gnbs[0].cloud_deployment.vnfs[0].name  )
# print ( tl.gnbs[0].cloud_deployment.vnfs[0].env_files  )
# print ( tl.gnbs[0].cloud_deployment.vnfs[0].configuration_data  )

tl = TestlineWrapper(tl)

# __all__ = ['tl']

IPV = "IPV4"
WEBUI_USER_NAME = "Nemuadmin"
WEBUI_PASSWORD = "nemuuser"
if IPV == "IPV4":
    WEBUI_URL = "https://" + tl.gnbs[0].cu.oam_ssh_connection_details.addr

if IPV == "IPV6":
    WEBUI_URL = "https://[" + tl.gnbs[0].cu.oam_ssh_connection_details.addr + "]"


Config_with_airphone = "False"


# For test compatibility
cfg_dir = _CFG_DIR
lmp_connection = _lmp_connection
lmp_connection2 = _lmp_connection2
EIF1_connection_Asik1 = _EIF1_connection_Asik1
EIF1_connection_Asik2 = _EIF1_connection_Asik2

# TODO need to clean useless variables
# __all__ = [
#     'tl',
#     'lmp_connection',
#     'lmp_connection2',
#     'EIF1_connection_Asik1',
#     'EIF1_connection_Asik2']
__all__ = ["tl"]
