__maintainer__ = "Barbier Jean-Michel"
__team__ = "MN 5G RAN I&V 1 Pz 4 SG"
__email__ = "I_UTE_NPS_5G@internal.nsn.com"

import os
import shutil

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
from taf.config.testline.testpc import TestPc
from taf.config.testline.gnb.du import RU, DU
from taf.config.testline.pdu import ATEN
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit


from taf.config.testline.ue import Prisma
from taf.config.testline.enb import PrismaEnb
from taf.config.testline.core import PrismaCore

from collections import OrderedDict

__all__ = ["tl"]


# ################################################################################ #
#                                                                                  #
#                          TL standard definition                                  #
#                                                                                  #
# ################################################################################ #

cfg_dir = os.path.dirname(os.path.abspath(__file__))

control = ControlNode(
    open_stack_connection_details=OpenStackConnectionDetails(
        ip_addr="10.14.49.26", username="admin", tenant="admin", password="uteadmin"
    ),
    default_ssh_connection_details=SshServiceDetails(
        addr="10.14.49.26", username="wrsroot", password="uteadmin"
    ),
    bmc_connection_details=BmcConnectionDetails(addr="", username="", password=""),
)

ncir = NCIR(compute_nodes=[], control_nodes=[control], version="ncir_17a")

# Test VM
host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.14.38.83", username="localuser", password="10c@1user"
    )
)

# VM UTE
# host = VM_UTE(
#    default_ssh_connection_details=SshServiceDetails(
#        addr='10.14.34.30',
#        username='ute',
#        password='ute'))

ru_pdu = ATEN(addr="", port_numbers=[4])

ru = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="umniedziola"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="root", password="umniedziola"
    ),
    pdu_port=ru_pdu.pdu_ports[4],
)

common_unit = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.1", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
)

airscale = Airscale(common_units=[common_unit])

du = DU(airscale=airscale, rus=[ru])

cbts_flavor = DeploymentFlavorStack(
    name="cbtsflavor",
    env_files=[os.path.join(cfg_dir, "config_flavor.env")],
    yaml_file=os.path.join(cfg_dir, "config_flavor.yaml"),
    default_vnf_prefix="cbts_prefix",
)

cbts_net = DeploymentNetworkStack(
    name="ext_net",
    env_files=[os.path.join(cfg_dir, "config_ext_net.env")],
    yaml_file=os.path.join(cfg_dir, "config_ext_net.yaml"),
)

cbts_vnf = DeploymentVnfStack(
    name="cbts_deploy",
    env_files=[os.path.join(cfg_dir, "config_bts.env")],
    yaml_file=os.path.join(cfg_dir, "config_bts.yaml"),
)

cu = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        # addr='10.14.49.35',
        # username='toor4nsn',
        # password='oZPS0POrRieRtu'),
        addr="10.14.49.32",
        username="robot",
        password="rastre1",
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.14.49.32", username="Nemuadmin", password="nemuuser"
    ),
)

cloud_deployment = CloudDeployment(
    default_cfg_dir=cfg_dir,
    flavors=[cbts_flavor],
    networks=[cbts_net],
    vnfs=[cbts_vnf],
    cloud_hosting=ncir,
)

cbts = CloudBts(dus=[du], cu=cu, cloud_deployment=cloud_deployment, vnf_name="5gbts")

tl_cloud_topology = "CLOUD_5G_PRISMAPX2_ASIKX42L_ABILX21B1_AEUA_18A"


# In case of airmosaic running on testVM:
_airmosaic_ssh = SshServiceDetails(
    addr="10.14.38.91", username="localuser", password="10c@1user"
)
_airmosaic_harness = HttpConnectionDetails(addr="10.14.38.91", port=8090)

_lsu_uu_ssh = SshServiceDetails(addr="10.14.54.184", username="user", password="user")
_tstm_uu_ssh = SshServiceDetails(addr="10.14.54.184", username="user", password="user")
_prisma_ue = Prisma(
    airmosaic_ssh_connection_details=_airmosaic_ssh,
    airmosaic_harness_connection_details=_airmosaic_harness,
    lsu_uu_ssh_connection_details=_lsu_uu_ssh,
    tstm_uu_ssh_connection_details=_tstm_uu_ssh,
)

_tstm_x2_ssh = SshServiceDetails(addr="10.14.54.184", username="user", password="user")
_prisma_enb = PrismaEnb(tstm_x2_ssh_connection_details=_tstm_x2_ssh)

_lsu_s1_ssh = SshServiceDetails(addr="10.14.54.183", username="user", password="user")
_tstm_s1_ssh = SshServiceDetails(addr="10.14.54.183", username="user", password="user")
_prisma_core = PrismaCore(
    lsu_s1_ssh_connection_details=_lsu_s1_ssh,
    tstm_s1_ssh_connection_details=_tstm_s1_ssh,
)

tl = TestLine(
    test_pc=host,
    gnbs=[cbts],
    cloud_hostings=[ncir],
    tl_cloud_topology=tl_cloud_topology,
    core=_prisma_core,
    enbs=[_prisma_enb],
    ues=[_prisma_ue],
)


# ################################################################################ #
#                                                                                  #
#                           Customization of TL                                    #
#                                                                                  #
# ################################################################################ #

tl_name = "IV_PS_310"

# Values usefull with specific Prisma library outside of taff
prismaIV = {
    "lsu_uu": "10.14.54.184",
    "lsu_s1": "10.14.54.183",
    "tstm_uu": "10.14.54.184",
    "tstm_s1": "10.14.54.183",
    "lsu_uu_username": "user",
    "lsu_uu_passwd": "user",
    "lsu_s1_username": "user",
    "lsu_s1_passwd": "user",
    "tstm_uu_username": "user",
    "tstm_uu_passwd": "user",
    "tstm_s1_username": "user",
    "tstm_s1_passwd": "user",
    "airmosaic_host": "127.0.0.1",
    "airmosaic_port": "8090",
    "airmosaic_path": "/opt/Prisma/airmosaic_lteuu/bin/airmosaic_lteuu",
    "airmosaic_cfg_path": "/opt/Prisma/CV046_Prisma_Config/config files",
    "sid_filename": "NSA_real_eNB_amm_01.sid",
    "Ul_gain": "0.0",
    "Dl_gain": "21.0",
}

# Variables from eCLAT
eclat = None
if "WORKSPACE" in os.environ:
    eclat = {
        "launcher": "eCLAT",
        "storage": os.environ["ECLAT_STORAGE"],
        "tools": os.environ["ECLAT_TOOLS"],
        "exec_path": os.environ["WORKSPACE"],
        "robotws5g": os.environ["ROBOTWS5G_DIRECTORY"],
        "robotws5g_branch": os.environ["ROBOTWS5G_BRANCH"],
        "logCollector_TLcfg": os.environ["TLConfig"],
        "logCollector_CMDcfg": os.environ["TLCommandsAndFiles"],
        "LOGS_STORAGE": os.environ["LOGS_STORAGE"],
        "PM_STORAGE": os.environ["PM_STORAGE"],
        "TESTCASE_PATH": os.path.join(
            os.environ["WORKSPACE"], "test-cases", os.environ["testCaseId"]
        ),
    }
    PATH_Storage = os.environ["ECLAT_STORAGE"]
    PATH_Tools = os.environ["ECLAT_TOOLS"]
else:
    PATH_Storage = "%s/robot_temporary" % (os.environ["HOME"])
    PATH_RESOURCES = "%s/resources" % (os.environ["HOME"])
    PATH_Tools = "%s/resources/tools" % (os.environ["HOME"])
    # Creation of path in local on the VM
    for ipath in [PATH_Storage, PATH_RESOURCES, PATH_Tools]:
        if not os.path.isdir(ipath):
            if os.path.exists(ipath):
                shutil.rmtree(ipath)
            os.makedirs(ipath)
    eclat = {
        "launcher": "unknown",
        "storage": PATH_Storage,
        "tools": PATH_Tools,
        "exec_path": "",
        "robotws5g": "",
        "robotws5g_branch": "",
        "logCollector_TLcfg": "",
        "logCollector_CMDcfg": "",
        "LOGS_STORAGE": PATH_Storage,
        "PM_STORAGE": PATH_Storage,
        "TESTCASE_PATH": "",
    }

# Custom Values
custom = {
    "TL_Number": "310",
    "PATH_Tools": PATH_Tools,
    "PATH_Storage": PATH_Storage,
    "eclat": eclat,
    #'PDU_IP': '10.28.1.103',
    "PDU_IP": "10.14.58.216",
    "PDU_5G_PORT": "5",
    "PDU_4G_PORT": "4",
    "PATH_Tools_titan": "/mnt/titan/tools",
    # Values linked to the gNB
    "GNB_Friendly_TL_Name": "CV310",
    "GNB_Architecture": "CLASSICAL",
    "GNB_First_CellID": "1",
    "GNB_First_Cell_nrArfcn": "2071591",
    # Prisa TAF - YAML File generation
    "yaml_prisma_filename_path": "/opt/Prisma/CV046_Prisma_Config",
    "yaml_prisma_filename": "generated_CV46_prisma_nps.yaml",
    # Prisma TAF (yaml parameters)
    # LSU S1
    "prisma_S1_present": True,
    "prisma_S1_start_script": "start_epc",
    "prisma_S1_init_script": "init_epc",
    # LSU UU
    "prisma_UU_create_5G_cell": "start_nr5g",
    "prisma_ppu_cell_5G": ["p0-2"],
    "prisma_ppu_cell_4G": "p0-18",
    "prisma_ppu_rach": "p0-5",
    "Ul_gain": "0.0",
    "Dl_gain": "21.0",
    # TSTM X2
    "prisma_tstm_X2_present": True,
    "prisma_tstm_X2_start_script": "start_nr5g_X2",
    # TSTM UU
    "prisma_UU_start_script": "start_nr5g_Uu_ms_gui",
    # AIRMOSAIC
    "prisma_cli_path": "/opt/Prisma/airmosaic_lteuu/bin/airmosaic_lteuu",
    "airmosaic_cfg_path": "/opt/Prisma/CV046_Prisma_Config/config files",
    "sid_filename": "NSA_real_eNB_amm_01.sid",
    "prisma_enable_amm": "true",
    "prisma_clock_timer": "900",
    # ----------------
    # iPerf configuration on DL side: VM @10.14.60.72
    "iPerf_VM_DL_ipaddress": "10.14.60.72",
    "iPerf_VM_DL_login": "ftp",
    "iPerf_VM_DL_passwd": "ftp",
    "iPerf_VM_DL_launch_command": "iperf -c 41.0.0.1 -u -i 1 -l 350 -p 5100 -b 26M -t 100000000",
    "iPerf_VM_DL_Check_on_UL_Side": "iperf -s -u -i 1 -p 5100",
    # iPerf configuration on UL side: VM @10.14.60.73
    "iPerf_VM_UL_ipaddress": "10.14.60.73",
    "iPerf_VM_UL_login": "ftp",
    "iPerf_VM_UL_passwd": "ftp",
    "iPerf_VM_UL_launch_command": "iperf -c 192.168.4.3 -u -i 1 -l 350 -p 4100 -b 5M -t 3600",
    "iPerf_VM_UL_Check_on_DL_Side": "iperf -s -u -i 1 -p 4100",
    "BTS_USERNAME_FIELD": "xpath:*//input[@id='applicationLoginUsername']",
    "BTS_PASSWORD_FIELD": "xpath://input[@id='applicationLoginPassword']",
    "BTS_LOGIN_BTN": "xpath://button[@id='applicationLoginButton']",
    "MAIN_CONTAINER": "xpath:/html/body/main/div",
    "SOFTWARE_SECTION": "xpath://*[@id='softwareupdate']/div[1]",
    "Logout": "xpath://*[@id='n-banner-collapse']/div[1]/ul/li[5]",
    "RU_VIEW": "xpath://div[@id='rap-module-1']",
    "RU_LED_COLOR": "xpath://div[@id='frm-1']/div[1]/div[1]/div[2]",
    "RU_LOCK": "xpath://*[@id='frm-1-lock-container']/div/div/div[1]/label",
    "RU_LOCK_CONFIRM": "xpath:/html/body/div/div/div/div[3]/div/button[1]",
    "RU_RESET_BTN": "xpath://button[@id='frm-1-reset']",
    "RU_RESET_RADIO_INPUT_SERVICE_CONTINUE": "xpath://input[@id='force-reset-false']",
    "RU_RESET_FORCE_RESET": "xpath://input[@id='force-reset-true']",
    "RU_RESET_CONFIRMATION_BTN": "xpath://button[@id='confirmation-modal-confirm']",
    "LOCK_CONFIRM": "xpath://*[@id='react-modal']/div/div[3]/div/button",
    "unlock_confirm": "xpath://*[@id='react-modal']/div/div[3]/div/button",
    "CELL_VIEW": "xpath://*[@id='site-rack-cells-1']",
    "CELL_LOCK": "xpath://*[@id='subcellgroup-0']/div/div[2]/button[1]",
    "CELL_UNLOCK": "xpath://*[@id='subcellgroup-0']/div/div[2]/button[2]",
    "CELL_LOCK_CONFIRM": "xpath:/html/body/div/div/div/div[3]/div/button[1]",
    "SNAPSHOT_COLLECTION_TAB": "xpath://*[@id='snapshot-navigation']/a",
    "SNAPSHOT_SERVER_IP": "xpath://*[@id='snapshot-server-ip-address']",
    "SNAPSHOT_PORT": "xpath://*[@id='snapshot-server-port']",
    "SNAPSHOT_PASSWORD": "xpath://*[@id='snapshot-server-password']",
    "SNAPSHOT_TARGET_FOLDER": "xpath://*[@id='snapshot-server-target-folder']",
    "SNAPSHOT_SAVE_BTN": "xpath://*[@id='snapshot-save-button']",
    "SNAPSHOT_SAVE_SERVER": "xpath://*[@id='snapshot-save-button']",
    "software_section": "xpath://*[@id='softwareupdate']/div[1]",
    "Rollback_button": "xpath://*[@id='site-rollback-button']",
    "parameters_tab": "xpath://*[@id='cmeditor-navigation']",
    "commisionning_parameters_holder": "xpath://*[@id='composer-app']",
    "parameters_filter": "xpath://*[@id='cm-editor']/header/div[3]/div/input",
    "parameters_filter_value": "xpath://*[@id='cm-editor']/section/table/tbody/tr[5]/td[4]/div/div/input",
    "parameters_error_table": "xpath://*[@id='pe-errors-data-table']",
}
