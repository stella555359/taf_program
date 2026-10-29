__maintainer__ = "Barbier Jean-Michel"
__team__ = "MN 5G RAN I&V 1 Pz 1 SG"
__email__ = "I_UTE_NPS_5G@internal.nsn.com"

import os

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
from taf.config.testline.testpc import TestPc
from taf.config.testline.gnb.du import RU, DU
from taf.config.testline.pdu import ATEN, PduPort
from taf.config.testline.testline import TestLine
from taf.config.testline.ue import Airphone
from taf.config.testline.gnb.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import CapacityUnit, CommonUnit, Airscale
from taf.compatibility.configuration import TestlineWrapper
from taf.config.cbts import create_configuration_data
from taf.config.testline.enb import LTEEmuEnb
from taf.config.testline.core import LTEEmuCore

__all__ = ["tl"]

# Variable to define the path to record files used during test execution
if "ECLAT_STORAGE" in os.environ:
    PATH_Storage = os.environ["ECLAT_STORAGE"]
else:
    PATH_Storage = "%s/robot_temporary" % (os.environ["HOME"])

# Custom Values
tl_name = "IV_PS_136"
testLine = "IV_PS_136"

custom = {
    "TL_Number": "136",
    "PATH_Tools": "%s/resources/tools" % (os.environ["HOME"]),
    "PATH_Storage": PATH_Storage,
    "temporary_path": "/tmp",
    "LOG_PATH": "/tmp",
    "GNB_Friendly_TL_Name": "CV136",
    "GNB_Architecture": "CLOUD",
    "GNB_First_CellID": "50",
    "GNB_First_Cell_nrArfcn": "2071592",
    "f1MPlane_localAddr": "192.168.136.111",
    "f1CPlane_localAddr": "192.168.136.112",
    "X2CPlane_localAddr": "192.168.4.110",
    "interface_fronthaul": "fronthaul",
    "interface_oam": "oam",
    "cpif_fronthaul": "fronthaul",
    "cpif_backhaul": "backhaul",
    "pcap_cleanup": "True",
    "scf_file_name": "scf_cv136.xml",
    "scf_version_mnl": "MNL5G19A_1904_200",
    "scf_version_tnl": "TNL5G19A_1904_200",
    # ------------- Airphone / LTEEmu / ePCSim -------------
    # LTEEmu - ePCSim
    "LTEEmu_addr": "10.14.55.7",
    "LTEemu_alias": "lteemu",
    "LTEemu_sudo_pwd": "lteemu",
    "LTEemu_user": "lteemu",
    "LTEemu_password": "lteemu",
    "LTEEmu_edaemon_port": "22224",
    "LTEEmu_egate_port": "20111",
    "LTEEmu_cfg_filename": "cv136_wts_step1.cfg",
    "LTEEmu_dir_path": "/home/lteemu/Airphone_December_2018"
    # ------------------------------------------------------
}

# Setting of switch
switchdict = {
    "TorSwitch_type": "quanta",
    "TorSwitch_addr": "10.5.116.136",
    "TorSwitch_login": "5GCV",
    "TorSwitch_passwd": "Tl5Gcv2017$",
    "TorSwitch_Fronthaul_interface": "0/5",
    "TorSwitch_alias": "oam",
}

# Setting of Airphone / LteEmu
lteemu_gen1 = {
    "tl_lteemu_addr": "10.14.55.7",
    "tl_lteemu_username": "lteemu",
    "tl_lteemu_password": "lteemu",
    "tl_lteemu_dir_path": "/home/lteemu/Airphone_December_2018",
    "tl_lteemu_cfg_filename": "cv136_wts_step1.cfg",
    "egate_port": 20111,
    "edaemon_port": 22224,
}

netact = {
    "vm_was1_address": "10.5.119.36",
    "vm_was2_address": "10.5.119.37",
    "vm_ne3s_address": "10.5.119.34",
    "omc_user": "omc",
    "omc_password": "Alcatel_1",
    "root_password": "Alcatel_1",
    "gui_url": "https://ivrrmlab.ivrrm.noklab.net",
    "gui_user": "omc",
    "gui_password": "Alcatel_1",
}

# tl

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

# Test VM
_test_vm = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="localuser", password="10c@1user"
    )
)

# VM UTE
_vm_ute = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.14.58.44", username="ute", password="ute"
    )
)

_control_0 = ControlNode(
    open_stack_connection_details=OpenStackConnectionDetails(
        ip_addr="10.14.55.11", username="admin", tenant="admin", password="uteadmin"
    ),
    default_ssh_connection_details=SshServiceDetails(
        addr="10.14.55.11", username="wrsroot", password="uteadmin"
    ),
    bmc_connection_details=BmcConnectionDetails(
        addr="10.14.55.1", username="admin", password="admin"
    ),
)

_ncir = NCIR(compute_nodes=[], control_nodes=[_control_0], version="ncir_17A")

_common_unit_lmp_connection = SshServiceDetails(
    addr="192.168.255.1", username="toor4nsn", password="oZPS0POrRieRtu"
)

_pdu = ATEN(addr="", port_numbers=list(range(1, 9)))

_common_unit_pdu_port = PduPort(pdu=_pdu, port_no=4)

_capacity_unit = CapacityUnit(addr="192.168.253.20")

_common_unit = CommonUnit(
    lmp_connection=_common_unit_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_common_unit_pdu_port,
)

_common_unit_lmp_connection = SshServiceDetails(
    addr="192.168.255.1", username="toor4nsn", password="oZPS0POrRieRtu"
)

_airscale = Airscale([_common_unit])

_du = DU(airscale=_airscale)

flavor_env_files = [os.path.join(_CFG_DIR, "config_flavor.env")]
flavor_config = create_configuration_data(flavor_env_files)

net_env_files = [os.path.join(_CFG_DIR, "config_ext_net.env")]
net_config = create_configuration_data(net_env_files)

vnf_env_files = [os.path.join(_CFG_DIR, "config_bts.env")]
vnf_config = create_configuration_data(vnf_env_files)

_cbts_flavor = DeploymentFlavorStack(
    name="7_20_CLOUD5GPSIV136_FLAVOR",
    env_files=[os.path.join(_CFG_DIR, "config_flavor.env")],
    yaml_file=os.path.join(_CFG_DIR, "config_flavor.yaml"),
    configuration_data=flavor_config,
    default_vnf_prefix="cbts_prefix",
)

_cbts_net = DeploymentNetworkStack(
    name="7_20_CLOUD5GPSIV136_EXT_NET",
    env_files=[os.path.join(_CFG_DIR, "config_ext_net.env")],
    configuration_data=net_config,
    yaml_file=os.path.join(_CFG_DIR, "config_ext_net.yaml"),
)

_cbts_vnf = DeploymentVnfStack(
    name="7_20_CLOUD5GPSIV136_BTS",
    env_files=[os.path.join(_CFG_DIR, "config_bts.env")],
    configuration_data=vnf_config,
    yaml_file=os.path.join(_CFG_DIR, "config_bts.yaml"),
)

_cu = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.14.48.136", username="robot", password="rastre1"
    ),
    oam_http_connection_details=HttpConnectionDetails(addr="10.14.48.136"),
)

_cloud_deployment = CloudDeployment(
    default_cfg_dir=_CFG_DIR,
    flavors=[_cbts_flavor],
    networks=[_cbts_net],
    vnfs=[_cbts_vnf],
    cloud_hosting=_ncir,
)

_cbts = CloudBts(
    dus=[_du], cu=_cu, cloud_deployment=_cloud_deployment, vnf_name="cv136gnb"
)

_tl_cloud_topology = "CLOUD_5G_PS_AP_ASIK_ABIL"

_airphone = Airphone(
    egate=None,  # type: SshServiceDetails
    l3_ssh_connection_details=None,  # type: SshServiceDetails
    l2_ssh_connection_details=None,  # type: SshServiceDetails
    l1=None,  # type: Airscale
)

# lteemu sim enb
_lte_sim_enb = LTEEmuEnb(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.14.55.7", username="lteemu", password="lteemu"
    ),
    dir_path="/home/lteemu/Airphone_December_2018",
    cfg_filename="cv136_wts_step1.cfg",
)

_epcsim = LTEEmuCore(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.14.55.7", username="lteemu", password="lteemu"
    ),
    dir_path="/home/lteemu/Airphone_December_2018",
    cfg_filename="cv136_wts_step1.cfg",
    mme_ip="1.1.1.1",
    mcc=-1,
    mnc=-1,
    tac=-1,
    edaemon_port=22224,
    egate_port=20111,
)

tl = TestLine(
    test_pc=_vm_ute,
    gnbs=[_cbts],
    cloud_hostings=[_ncir],
    tl_cloud_topology=_tl_cloud_topology,
    core=_epcsim,
)
