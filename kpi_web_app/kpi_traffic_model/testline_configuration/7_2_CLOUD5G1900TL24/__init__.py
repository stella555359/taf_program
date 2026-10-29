######################################
#  TestLine 24 BGL                   #
######################################
__maintainer__ = "I MN ECE BLR RD UP SQD LAKSHYA"
__team__ = "I MN ECE BLR RD UP SQD LAKSHYA"
__email__ = "I_MN_ECE_BLR_RD_UP_SQD_LAKSHYA@internal.nsn.com"
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
)
from taf.config.testline.gnb import CloudBts, CU, DU
from taf.config.testline.core import EPCSim
from taf.config.testline.ue import Airphone, AirphoneCloud
from taf.config.testline.pdu import RRB
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.compatibility.configuration import TestlineWrapper
from taf.config.cbts import create_configuration_data

# from taf.config.testline.legacy import (CONFIG_5G, AirPhone, Control, Host, Lteemu, SCF, EPCSim, RF, Pdu)
from taf.config.testline.legacy import SCF


_CFG_DIR = os.path.dirname(os.path.abspath(__file__))


_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.41.170.145", username="ute", password="ute"
    )
)

_control_0 = ControlNode(
    open_stack_connection_details=OpenStackConnectionDetails(
        ip_addr="10.41.170.140", username="admin", tenant="admin", password="test123"
    ),
    default_ssh_connection_details=SshServiceDetails(
        addr="10.41.170.140", username="admin", password="test123"
    ),
    bmc_connection_details=BmcConnectionDetails(addr="", username="", password=""),
)

_ncir = NCIR(compute_nodes=[], control_nodes=[_control_0], version="ncir_17A")

# PDU  port3= DU  port4= Airphone
_pdu = RRB(addr="10.41.170.126", port_numbers=[1, 2])

# GNB

flavor_env_files = [os.path.join(_CFG_DIR, "config_flavor_aio.env")]
flavor_config = create_configuration_data(flavor_env_files)

net_env_files = [os.path.join(_CFG_DIR, "config_ext_net.env")]
net_config = create_configuration_data(net_env_files)

vnf_env_files = [os.path.join(_CFG_DIR, "config_bts.env")]
vnf_config = create_configuration_data(vnf_env_files)

_cbts_flavor = DeploymentFlavorStack(
    name="TL24_5gbts_flavors",
    env_files=flavor_env_files,
    # only name on yaml file -> path will be set in frt_script
    yaml_file="5gbts_flavor_aio.yaml",
    configuration_data=flavor_config,
    default_vnf_prefix="tl24-5gbts",
)

_cbts_net = DeploymentNetworkStack(
    name="TL24_5gbts_ext",
    env_files=net_env_files,
    # only name on yaml file -> path will be set in frt_script
    yaml_file="5gbts_ext_net.yaml",
    configuration_data=net_config,
)

_cbts_vnf = DeploymentVnfStack(
    name="TL24_5gbts_rac",
    env_files=vnf_env_files,
    # only name on yaml file -> path will be set in frt_script
    yaml_file="5gbts_heat.yaml",
    configuration_data=vnf_config,
)

_cloud_deployment = CloudDeployment(
    default_cfg_dir=_CFG_DIR,
    flavors=[_cbts_flavor],
    networks=[_cbts_net],
    vnfs=[_cbts_vnf],
    cloud_hosting=_ncir,
)

_cu = CU(
    backhaul_site_oam_ip="10.41.170.147",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.41.170.147", username="robot", password="rastre1"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.41.170.147", username="Nemuadmin", password="nemuuser"
    ),
)

# ABIL
_capacity_unit_1 = CapacityUnit(addr="192.168.253.20")

# ASIK
_common_unit_1 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.2", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_capacity_unit_1],
    pdu_port=_pdu.pdu_ports[2],
)

_airscale_1 = Airscale(common_units=[_common_unit_1])

_du_1 = DU(airscale=_airscale_1)

_cbts = CloudBts(
    cu=_cu, dus=[_du_1], cloud_deployment=_cloud_deployment, vnf_name="tl24-5gbts"
)

_epcsim = EPCSim(
    mme_ip="192.168.4.120",
    mcc=311,
    mnc=489,
    tac=333,
    default_ssh_connection_details=SshServiceDetails(
        addr="10.41.170.145", username="ute", password="ute"
    ),
    dir_path="/home/ute/WTS",
    cfg_filename="basic_wts_step2.cfg",
    edaemon_port=22222,
    egate_port=20000,
)

# TODO move SCF away from TL config
## additional parameters for FRT tests
#
# TL specific values to be used for gNB configuration after SW update
_PARAMS_TO_MODIFY_SCF = [
    dict(value="Nokia BGL Testline 24", dist_name="MRBTS-1900", p_name="btsName"),
    dict(
        value="38",
        dist_name="MRBTS-1900/NRBTS-1/NRCELL-1",
        p_name="prachConfigurationIndex",
    ),
    dict(
        value="192.168.4.2",
        dist_name="MRBTS-1900/NRBTS-1/SERVEDAMF-1",
        p_name="amfIPAddress",
    ),
    dict(
        value="false",
        dist_name="MRBTS-1900/MNL-1/MNLENT-1/FEATCADM-1",
        p_name="systemAcctPermEnable",
    ),  # enable login via too4nsn to DU
    dict(
        value="false",
        dist_name="MRBTS-1900/MNL-1/MNLENT-2/FEATCADM-1",
        p_name="systemAcctPermEnable",
    ),  # enable login via too4nsn to DU
    dict(
        value="true",
        dist_name="MRBTS-1900/MNL-1/MNLENT-2/SECADM-1",
        p_name="actServiceAccountSsh",
    ),
    dict(
        value="15min",
        dist_name="MRBTS-1900/MNL-1/PMCADM-1",
        p_name="reportingIntervalPm",
    ),
    dict(
        value="3gppFlowControl",
        dist_name="MRBTS-1900/NRBTS-1",
        p_name="dlFlowControlAlgo",
        index="0",
    ),
    dict(
        value="3gppFlowControl",
        dist_name="MRBTS-1900/NRBTS-1",
        p_name="dlFlowControlAlgo",
        index="1",
    ),
    dict(
        value="3gppFlowControl",
        dist_name="MRBTS-1900/NRBTS-1",
        p_name="dlFlowControlAlgo",
        index="2",
    ),
    dict(
        value="3gppFlowControl",
        dist_name="MRBTS-1900/NRBTS-1",
        p_name="dlFlowControlAlgo",
        index="3",
    ),
    dict(
        value="3gppFlowControl",
        dist_name="MRBTS-1900/NRBTS-1",
        p_name="dlFlowControlAlgo",
        index="4",
    ),
    dict(
        value="3gppFlowControl",
        dist_name="MRBTS-1900/NRBTS-1",
        p_name="dlFlowControlAlgo",
        index="5",
    ),
    dict(
        value="3gppFlowControl",
        dist_name="MRBTS-1900/NRBTS-1",
        p_name="dlFlowControlAlgo",
        index="6",
    ),
    dict(
        value="3gppFlowControl",
        dist_name="MRBTS-1900/NRBTS-1",
        p_name="dlFlowControlAlgo",
        index="7",
    ),
    dict(
        value="3gppFlowControl",
        dist_name="MRBTS-1900/NRBTS-1",
        p_name="dlFlowControlAlgo",
        index="8",
    ),
    dict(
        value="3gppFlowControl",
        dist_name="MRBTS-1900/NRBTS-1",
        p_name="dlFlowControlAlgo",
        index="9",
    ),
    dict(
        value="3gppFlowControl",
        dist_name="MRBTS-1900/NRBTS-1",
        p_name="dlFlowControlAlgo",
        index="10",
    ),
    dict(
        value="3gppFlowControl",
        dist_name="MRBTS-1900/NRBTS-1",
        p_name="dlFlowControlAlgo",
        index="11",
    ),
    dict(
        value="3gppFlowControl",
        dist_name="MRBTS-1900/NRBTS-1",
        p_name="dlFlowControlAlgo",
        index="12",
    ),
]

_scf = SCF(
    project="5G18A",
    name="SBTS5G18A_5g_pid11_abil_l2rt.xml",
    scf_params=_PARAMS_TO_MODIFY_SCF,
)


# TODO convert to new TL config
Baseband = "ABIL"
airscaleNodeID = ["0x10", "0x12"]


# AirPhone
_airphone_flavor = DeploymentFlavorStack(
    name="TL24_5gap_flavors",
    env_files=[os.path.join(_CFG_DIR, "airphone_flavor.env")],
    yaml_file=os.path.join(_CFG_DIR, "airphone_flavor.yaml"),
    configuration_data=create_configuration_data(
        [os.path.join(_CFG_DIR, "airphone_flavor.env")]
    ),
    default_vnf_prefix="tl24-5gap",
)

_airphone_net = DeploymentNetworkStack(
    name="TL24_5gap_ext",
    env_files=[os.path.join(_CFG_DIR, "airphone_ext_net.env")],
    yaml_file=os.path.join(_CFG_DIR, "airphone_ext_net.yaml"),
    configuration_data=create_configuration_data(
        [os.path.join(_CFG_DIR, "airphone_ext_net.env")]
    ),
)

_airphone_vnf = DeploymentVnfStack(
    name="TL24_5gap_rac",
    env_files=[os.path.join(_CFG_DIR, "airphone_config_bts.env")],
    yaml_file=os.path.join(_CFG_DIR, "airphone_config_bts.yaml"),
    configuration_data=create_configuration_data(
        [os.path.join(_CFG_DIR, "airphone_config_bts.env")]
    ),
)

airphone_deployment = CloudDeployment(
    default_cfg_dir=_CFG_DIR,
    flavors=[_airphone_flavor],
    networks=[_airphone_net],
    vnfs=[_airphone_vnf],
    cloud_hosting=_ncir,
)

_airphone_cloud = AirphoneCloud(
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.41.170.152", username="robot", password="rastre1"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.41.170.152", username="Nemuadmin", password="nemuuser"
    ),
)

_airphone_capacity_unit_1 = CapacityUnit(addr="192.168.253.84")

_airphone_common_unit_1 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.3", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_airphone_capacity_unit_1],
    pdu_port=_pdu.pdu_ports[1],
)

_airphone_airscale = Airscale(common_units=[_airphone_common_unit_1])

_airphone = Airphone(
    egate=None,
    airphone_cloud=_airphone_cloud,
    l1=_airphone_airscale,
    l3_ssh_connection_details=None,
    l2_ssh_connection_details=None,
)

# TODO move SCF away from TL config
#
# TL specific values to be used for Airphone configuration after SW update
AIRPHONE_SCF_PARAMETERS = [
    dict(value="Nokia BGL TL24 AP", dist_name="MRBTS-1900", p_name="btsName"),
    dict(
        value="192.168.2.81",
        dist_name="MRBTS-1900/TNLSVC-1/TNL-4/IPNO-1/IPIF-1/IPADDRESSV4-1",
        p_name="localIpAddr",
    ),
    dict(
        value="192.168.2.82",
        dist_name="MRBTS-1900/TNLSVC-1/TNL-4/IPNO-1/IPIF-1/IPADDRESSV4-2",
        p_name="localIpAddr",
    ),
    dict(
        value="192.168.2.80",
        dist_name="MRBTS-1900/TNLSVC-1/TNL-4/IPNO-1/IPIF-1/IPADDRESSV4-3",
        p_name="localIpAddr",
    ),
    dict(
        value="5G18A/5g_pid11_airphone",
        dist_name="MRBTS-1900/EQM-1/APEQM-1",
        p_name="rapProfile",
    ),
    dict(
        value="false",
        dist_name="MRBTS-1900/MNL-1/MNLENT-1/FEATCADM-1",
        p_name="systemAcctPermEnable",
    ),
    dict(
        value="false",
        dist_name="MRBTS-1900/MNL-1/MNLENT-2/FEATCADM-1",
        p_name="systemAcctPermEnable",
    ),
    dict(
        value="true",
        dist_name="MRBTS-1900/MNL-1/MNLENT-1/SECADM-1",
        p_name="actServiceAccountSsh",
    ),
    dict(
        value="wts",
        dist_name="MRBTS-1900/TNLSVC-1/TNL-2/ETHSVC-1/ETHLK-1",
        p_name="underLyingInterface",
    ),
    dict(
        value="wts",
        dist_name="MRBTS-1900/TNLSVC-1/TNL-3/ETHSVC-1/ETHLK-1",
        p_name="underLyingInterface",
    ),
]

airphone_scf = SCF(
    project="5G18A", name="SBTS5G18A_5g_pid11.xml", scf_params=AIRPHONE_SCF_PARAMETERS
)

#
# Testline
tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    cloud_hostings=[_ncir],
    core=_epcsim,
    tl_cloud_topology="CLOUD_5G_BB3_18A",
    pdus=[_pdu],
    ues=[_airphone],
)
tl = TestlineWrapper(tl)

tl.scf = _scf  # still a WA

AIRPHONE_airscaleNodeID = ["0x50", "0x52"]
# L1bypass parameters for only for test, to be removed later

L1byPass_flag = "L1BYPASS"

__all__ = ["tl"]
