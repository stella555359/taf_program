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
TL_NPS_name = "TL10"
TL_name = "7_20_QT" + TL_NPS_name
# MODEM_BOARD='ABIL'  #ABIL   ABIK

##################################################################

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="135.238.24.241", username="ute", password="ute"
    )
)

_control = ControlNode(
    open_stack_connection_details=OpenStackConnectionDetails(
        ip_addr="135.238.24.236",
        username="wrsroot",
        tenant="admin",
        password="uteadmin5G!",
    ),
    default_ssh_connection_details=SshServiceDetails(
        addr="135.238.24.236", username="admin", password="uteadmin5G!"
    ),
    bmc_connection_details=BmcConnectionDetails(addr="", username="", password=""),
)

_ncir = NCIR(compute_nodes=[], control_nodes=[_control], version="ncir_17A")

flavor_env_files = [os.path.join(_CFG_DIR, "5gbts_flavor.env")]
flavor_config = create_configuration_data(flavor_env_files)

net_env_files = [os.path.join(_CFG_DIR, "5gbts_ext_net.env")]
net_config = create_configuration_data(net_env_files)

# STATIC
vnf_env_files = [os.path.join(_CFG_DIR, "5gbts_heat.env")]
vnf_config = create_configuration_data(vnf_env_files)

# DEBUG
vnf_env_files = [
    os.path.join(_CFG_DIR, "5gbts_heat.env"),
    os.path.join(_CFG_DIR, "5gbts_heat_QT.env"),
]
# vnf_config = create_configuration_data(vnf_env_files)


_cbts_flavor = DeploymentFlavorStack(
    name="flavor_" + TL_NPS_name,
    env_files=flavor_env_files,
    #    yaml_file=os.path.join(_CFG_DIR, '5gbts_flavor_aio.yaml'),
    yaml_file=os.path.join(_CFG_DIR, "5gbts_flavor.yaml"),
    configuration_data=flavor_config,
    default_vnf_prefix="5gbts",
)


_cbts_vnf = DeploymentVnfStack(
    name="deploy" + TL_NPS_name,
    env_files=vnf_env_files,
    yaml_file=os.path.join(_CFG_DIR, "5gbts_heat.yaml"),
)

# STATIC
#    yaml_file=os.path.join(_CFG_DIR, '5gbts_heat.yaml'),
#    configuration_data=vnf_config)

_cbts_net = DeploymentNetworkStack(
    name="net_" + TL_NPS_name,
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
    backhaul_site_oam_ip="192.168.255.100",
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.100", username="robot", password="rastre1"
    ),
    oam_http_connection_details=HttpConnectionDetails(addr="192.168.255.100"),
)


_cbts = CloudBts(cu=_cu, cloud_deployment=_cloud_deployment, vnf_name=TL_NPS_name)
#    vnf_name='5gbts')

_epcsim = EPCSim(
    mme_ip="135.120.10.17",
    mcc=-1,
    mnc=-1,
    tac=-1,
    default_ssh_connection_details=SshServiceDetails(
        addr="135.120.10.17", username="ute", password="ute"
    ),
    dir_path="/home/ute/lteemu_Dec18",
    cfg_filename="TL10_basic_wts_step1.cfg",
)
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
    # addr='10.14.32.65',
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
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

tl = TestLine(
    test_pc=_test_pc,
    core=_epcsim,
    ues=[_airphone],
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

# __all__ = [ 'tl' ]
__all__ = ["tl"]
