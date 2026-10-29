######################################
#  TestLine Cloud TL3 HZ                   #
######################################
__maintainer__ = "Mao, Cathy"
__team__ = "NSB MN ECE RD 2 CN 06 SG"
__email__ = "cathy.mao@nokia-sbell.com"
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
from taf.config.testline.core import LTEEmuCore
from taf.config.testline.ue import Airphone
from taf.config.testline.pdu import FACOM
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.compatibility.configuration import TestlineWrapper
from taf.config.cbts import create_configuration_data

# from taf.config.testline.legacy import (CONFIG_5G, AirPhone, Control, Host, Lteemu, SCF, EPCSim, RF, Pdu)
from taf.config.testline.legacy import SCF

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.183.68.67", username="root", password="5gr00t"
    )
)

_control_0 = ControlNode(
    open_stack_connection_details=OpenStackConnectionDetails(
        ip_addr="10.57.137.244",
        username="tl3user",
        tenant="CI-TestLine3",
        password="ece5Gci",
    ),
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.137.244", username="tl3user", password="ece5Gci!"
    ),
    bmc_connection_details=BmcConnectionDetails(addr="", username="", password=""),
)

_ncir = NCIR(compute_nodes=[], control_nodes=[_control_0], version="ncir_17A")

flavor_env_files = [os.path.join(_CFG_DIR, "config_flavor.env")]
flavor_config = create_configuration_data(flavor_env_files)

net_env_files = [os.path.join(_CFG_DIR, "config_ext_net.env")]
net_config = create_configuration_data(net_env_files)

vnf_env_files = [os.path.join(_CFG_DIR, "config_bts.env")]
vnf_config = create_configuration_data(vnf_env_files)

_cbts_flavor = DeploymentFlavorStack(
    name="TL3-Flavors",
    env_files=flavor_env_files,
    #                                        yaml_file=os.path.join(_CFG_DIR, '5gbts_flavor_aio.yaml'),
    yaml_file="bla",
    configuration_data=flavor_config,
    default_vnf_prefix="ci-tl3",
)

_cbts_net = DeploymentNetworkStack(
    name="TL3-Ext-Networks",
    env_files=net_env_files,
    #                                        yaml_file=os.path.join(_CFG_DIR, '5gbts_ext_net.yaml'),
    yaml_file="bla",
    configuration_data=net_config,
)

_cbts_vnf = DeploymentVnfStack(
    name="CI-TL3-Stack",
    env_files=vnf_env_files,
    # yaml_file=os.path.join(_CFG_DIR, '5gbts_heat.yaml'),
    yaml_file="bla",
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
    backhaul_site_oam_ip="10.57.212.53",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.212.53", username="robot", password="rastre1"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.212.53", username="Nemuadmin", password="nemuuser"
    ),
)

# PDU  port3= DU  port4= Airphone
_pdu = FACOM(addr="10.57.247.202", port_numbers=[1, 2])


# ABIL
_capacity_unit = CapacityUnit(addr="192.168.253.22")

# ASIK
_common_unit = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.146.130", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_capacity_unit],
    pdu_port=_pdu.pdu_ports[1],
)

_airscale = Airscale(common_units=[_common_unit])

_du = DU(airscale=_airscale)

_cbts = CloudBts(
    cu=_cu, dus=[_du], cloud_deployment=_cloud_deployment, vnf_name="ci-tl3"
)

#########LTEemuSim##########
_lteemu = LTEEmuCore(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.212.83", username="nokia", password="nokia123"
    ),
    dir_path="/home/nokia/Binary64bits_RrcWithNrRrc_new",
    cfg_filename="basic_wts_step2.cfg",
    mme_ip="",
    edaemon_port="22222",
    egate_port="20000",
)

# TODO move SCF away from TL config
## additional parameters for FRT tests
#
# TL specific values to be used for gNB configuration after SW update
_PARAMS_TO_MODIFY_SCF = [
    dict(value="Nokia 5G_HZ_ECE_TL3", dist_name="MRBTS-1900", p_name="btsName"),
    dict(value="192.168.2.61", dist_name="DU_f1Cplane", p_name="localIpAddr"),
    dict(value="192.168.2.60", dist_name="DU_f1Mplane", p_name="localIpAddr"),
    dict(value="192.168.2.62", dist_name="DU_f1Uplane", p_name="localIpAddr"),
    dict(
        value="38",
        dist_name="MRBTS-1900/NRBTS-1/NRCELL-1",
        p_name="prachConfigurationIndex",
    ),
]

_scf = SCF(
    project="5G18A",
    name="SBTS5G18A_5g_pid12_abil_l2rt.xml",
    scf_params=_PARAMS_TO_MODIFY_SCF,
)

# TODO  move away from TL config
delete_stack = "ALL"

# TODO convert to new TL config
Baseband = "ABIL"
airscaleNodeID = ["0x10", "0x12"]


#
# Testline
tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    cloud_hostings=[_ncir],
    core=_lteemu,
    tl_cloud_topology="CLOUD_5G_BB3_18A",
    pdus=[_pdu],
)
tl = TestlineWrapper(tl)

tl.scf = _scf  # still a WA

# Todo find place for this
tl.cbts.edaemon_port = "22222"
tl.cbts.egate_port = "10000"


pdu_ip = "10.57.247.202"
pdu_type = "FACOM"
pdu_port_num = [2]


# L1bypass parameters for only for test, to be removed later


# tl.uec_cfg_filename = 'basic_cfg_5guec.lua'
# tl.uec_dir_path = '/home/ute/L1R3_118/5guec'
# tl.ap_l3_dir_path = '/opt/AirPhone/L3'
# tl.uec_edaemon_path = '/opt/AirPhone/5guec'
SSH_OAM_AUTHENTICATION_TIMEOUT = "15 min"
L1byPass_flag = "L1BYPASS"
AIRPHONE_OAM_IP = "10.57.212.63"
AIRPHONE_DU_LMP_IP = "10.57.146.131"
AIRPHONE_DU_user = "toor4nsn"
AIRPHONE_DU_pwd = "oZPS0POrRieRtu"
# AIRPHONE_SCF_DEFAULT_PATH = ''
# AIRPHONE_SCF_PARAMETERS = ''
# AIRPHONE_STACK_NAME = 'TL24_5gap_rac'
# AIRPHONE_NET_NAME = 'TL24_5gap_ext'
# AIRPHONE_FLAVOR_NAME = 'TL24_5gap_flavors'
# AIRPHONE_VNF_NAME = 'tl24-5gap'
# AIRPHONE_VNF_PREFIX = 'tl24-5gap'
AIRPHONE_airscaleNodeID = ["0x50", "0x52"]
AIRPHONE_SCF_PARAMETERS = [
    dict(value="Nokia HZ TL3 AP", dist_name="MRBTS-1900", p_name="btsName"),
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
    # 	dict(value='192.168.2.121', dist_name='MRBTS-1900/TNLSVC-1/TNL-1/IPNO-1/IPIF-1/IPADDRESSV4-1', p_name='localIpAddr'),
    # 	dict(value='192.168.2.123', dist_name='MRBTS-1900/TNLSVC-1/TNL-3/IPNO-1/IPIF-2/IPADDRESSV4-1', p_name='localIpAddr'),
    # 	dict(value='192.168.2.122', dist_name='MRBTS-1900/TNLSVC-1/TNL-2/IPNO-1/IPIF-2/IPADDRESSV4-1', p_name='localIpAddr'),
    #    dict(value='192.168.6.129', dist_name='MRBTS-1900/TNLSVC-1/TNL-2/IPNO-1/IPIF-1/IPADDRESSV4-1', p_name='localIpAddr'),
    #    dict(value='192.168.6.130', dist_name='MRBTS-1900/TNLSVC-1/TNL-3/IPNO-1/IPIF-1/IPADDRESSV4-1', p_name='localIpAddr'),
    dict(
        value="5G18A/5g_pid12_airphone",
        dist_name="MRBTS-1900/EQM-1/APEQM-1",
        p_name="rapProfile",
    ),
    # dict(value='false', dist_name='MRBTS-1900/MNL-1/MNLENT-1/FEATCADM-1', p_name='systemAcctPermEnable'),
    dict(
        value="true",
        dist_name="MRBTS-1900/MNL-1/MNLENT-1/SECADM-1",
        p_name="actServiceAccountSsh",
    ),
]
AIRPHONE_SCF_DEFAULT_PATH = "/opt/nokia/SS_MzOam/cloud-siteoam/siteoam/site_conf/5G18A"
AIRPHONE_SCF_FILE_NAME = "SBTS5G18A_5g_pid11.xml"
airphone_pdu_ip = "10.57.247.202"
airphone_pdu_type = "FACOM"
airphone_pdu_port_num = [2]

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
__all__ = ["tl"]
