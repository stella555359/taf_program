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
from taf.config.testline.ue import AirphoneCloud, Airphone
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.compatibility.configuration import TestlineWrapper
from taf.config.cbts import create_configuration_data


##################################################################
# NPS add on
# update  for TL739
##################################################################

TL_NPS_name = "ib739"
TL_name = "7_20_QTIB739"
# TL_name = '7_20_QT'+TL_NPS_name
# MODEM_BOARD='ABIL'  #ABIL   ABIK

##################################################################

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.14.33.96", username="ute", password="ute"
    )
)

_control = ControlNode(
    open_stack_connection_details=OpenStackConnectionDetails(
        ip_addr="10.14.33.102", username="wrsroot", tenant="admin", password="uteadmin"
    ),
    default_ssh_connection_details=SshServiceDetails(
        addr="10.14.33.102", username="admin", password="uteadmin"
    ),
    bmc_connection_details=BmcConnectionDetails(addr="", username="", password=""),
)

_ncir = NCIR(compute_nodes=[], control_nodes=[_control], version="ncir_17A")


flavor_env_files = [os.path.join(_CFG_DIR, "5gbts_flavor.env")]
flavor_config = create_configuration_data(flavor_env_files)

net_env_files = [os.path.join(_CFG_DIR, "5gbts_ext_net.env")]
net_config = create_configuration_data(net_env_files)

vnf_env_files = [os.path.join(_CFG_DIR, "5gbts_heat.env")]
vnf_config = create_configuration_data(vnf_env_files)

_cbts_flavor = DeploymentFlavorStack(
    name="flavor_" + TL_NPS_name,
    env_files=flavor_env_files,
    yaml_file=os.path.join(_CFG_DIR, "5gbts_flavor_aio.yaml"),
    configuration_data=flavor_config,
    default_vnf_prefix="5gbts",
)


_cbts_vnf = DeploymentVnfStack(
    #   name='deploy_'+TL_NPS_name,
    name="heat_" + TL_NPS_name,
    env_files=vnf_env_files,
    yaml_file=os.path.join(_CFG_DIR, "5gbts_heat.yaml"),
    configuration_data=vnf_config,
)

_cbts_net = DeploymentNetworkStack(
    #   name='net_'+TL_NPS_name,
    name="ext_net_" + TL_NPS_name,
    env_files=net_env_files,
    yaml_file=os.path.join(_CFG_DIR, "5gbts_ext_net.yaml"),
    configuration_data=net_config,
)


_cloud_deployment = CloudDeployment(
    default_cfg_dir=_CFG_DIR,
    flavors=[_cbts_flavor],
    networks=[_cbts_net],
    vnfs=[_cbts_vnf],
    cloud_hosting=_ncir,
)

_cu = CU(
    backhaul_site_oam_ip="10.14.48.217",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.14.33.103", username="robot", password="rastre1"
    ),
    oam_http_connection_details=HttpConnectionDetails(addr="10.14.48.217"),
)


_cbts = CloudBts(cu=_cu, cloud_deployment=_cloud_deployment, vnf_name="5gbts")

_epcsim = EPCSim(
    mme_ip="135.120.10.17",
    mcc=-1,
    mnc=-1,
    tac=-1,
    default_ssh_connection_details=SshServiceDetails(
        addr="135.120.10.17", username="ute", password="ute"
    ),
    dir_path="/home/ute/lteemu_June18",
    cfg_filename="TL10_basic_wts_step1.cfg",
)
_airphone_cloud = AirphoneCloud(
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.14.48.217", username="_rcpadmin", password="RCP_owner"
    ),
    oam_http_connection_details=HttpConnectionDetails(addr="10.14.48.217"),
)

_egate = SshServiceDetails(addr="0.0.0.0", username="user2", password="password2")

_l3 = SshServiceDetails(addr="10.14.48.217", username="_rcpadmin", password="RCP_owner")

_l2 = SshServiceDetails(addr="10.14.48.217", username="_rcpadmin", password="RCP_owner")

_lmp_connection = SshServiceDetails(
    addr="10.14.32.103", username="toor4nsn", password="oZPS0POrRieRtu"
)


tl = TestLine(
    test_pc=_test_pc,
    core=_epcsim,
    # ues=[_airphone],
    gnbs=[_cbts],
    cloud_hostings=[_ncir],
    #    tl_cloud_topology='CLOUD_5G_TYPE')
    tl_cloud_topology="CLOUD_5G_BB3_18A",
)


# for  Wrapper
tl = TestlineWrapper(tl)
# NPS Addons
cfg_dir = _CFG_DIR
lmp_connection = _lmp_connection


IPV = "IPV4"
WEBUI_USER_NAME = "Nemuadmin"
WEBUI_PASSWORD = "nemuuser"

# to be modified    to used   new  variable instead of  tl.cbts.oam.addr
# and  tl.cbts.oam.addr

if IPV == "IPV4":
    #    WEBUI_URL = 'https://' + tl.cbts.oam.addr
    WEBUI_URL = "https://" + tl.gnbs[0].cu.oam_ssh_connection_details.addr
if IPV == "IPV6":
    #    WEBUI_URL = 'https://['+tl.cbts.oam.addr + ']'
    WEBUI_URL = "https://[" + tl.gnbs[0].cu.oam_ssh_connection_details.addr + "]"

Config_with_airphone = "True"


# For test compatibility
# __all__ = [
#     'tl',
#     'cfg_dir',
#     'WEBUI_USER_NAME',
#     'TL_NPS_name',
#     'TL_name',
#     'Config_with_airphone',
#     'vnf_env_files',
#     'vnf_config',
#     'IPV',
#     'lmp_connection']
__all__ = ["tl"]
