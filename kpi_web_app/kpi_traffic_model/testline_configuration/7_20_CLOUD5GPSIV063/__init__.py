__maintainer__ = "Jourdain Remi"
__team__ = "MN 5G&SC Pz 5G I&V 2 2 SG"
__email__ = "remi.jourdain@nokia.com"
__owner_email__ = "remi.jourdain@nokia.com"

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
from taf.config.testline import RU, DU
from taf.config.testline.pdu import ATEN
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit

__all__ = ["tl"]

# ################################################################################ #
#                                                                                  #
#                          TL standard definition                                  #
#                                                                                  #
# ################################################################################ #

cfg_dir = os.path.dirname(os.path.abspath(__file__))

control = ControlNode(
    open_stack_connection_details=OpenStackConnectionDetails(
        ip_addr="10.14.55.209", username="admin", tenant="admin", password="uteadmin"
    ),
    default_ssh_connection_details=SshServiceDetails(
        addr="10.14.55.211", username="wrsroot", password="uteadmin"
    ),
    bmc_connection_details=BmcConnectionDetails(
        addr="10.14.55.208", username="admin", password="admin"
    ),
)

ncir = NCIR(compute_nodes=[], control_nodes=[control], version="ncir_17a")

host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.14.39.12", username="localuser", password="10c@1user"
    )
)

ru_pdu = ATEN(addr="TO_UPDATE", port_numbers=[1])

ru = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziela"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.255.1", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=ru_pdu.pdu_ports[1],
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
    backhaul_site_oam_ip="10.14.48.63",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.14.48.63", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(addr="10.14.48.63"),
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

tl = TestLine(
    test_pc=host,
    gnbs=[cbts],
    cloud_hostings=[ncir],
    tl_cloud_topology=tl_cloud_topology,
)


# ################################################################################ #
#                                                                                  #
#                           Customization of TL                                    #
#                                                                                  #
# ################################################################################ #

tl_name = "IV_PS_063"

# Values useful with specific Prisma library outside of taf
prismaIV = {
    "lsu_uu": "10.14.56.17",
    "tstm_uu": "10.14.56.17",
    "tstm_s1": "None",
    "lsu_s1": "None",
    "lsu_uu_username": "user",
    "lsu_uu_passwd": "user",
    "tstm_uu_username": "user",
    "tstm_uu_passwd": "user",
    "airmosaic_host": "127.0.0.1",
    "airmosaic_port": "8090",
    "airmosaic_path": "/opt/Prisma/airmosaic_fiveguu/bin/airmosaic_fiveguu",
    "airmosaic_cfg_path": "/opt/Prisma/CV63_Prisma_Config/config_files",
    "sid_filename": "CV63.sid",
    "scenario_prisma": "CV63.sce",
    "Ul_gain": "20.0",
    "Dl_gain": "41.0",
}

# Variables for iPerf

iPerf_Config = {
    "PublicIPTrafficServerDL": "10.14.42.87",
    "CoreIPTrafficServerDL": "10.11.70.172",
    "userDL": "ran5g",
    "pwDL": "nokia2018",
    "userUL": "ftp",
    "pwUL": "ftp",
    "TrafficServerUL": "10.14.57.193",
    "UEList": [
        {
            "UL_addr": "192.168.63.61",
            "UL_port": "5161",
            "DL_addr": "172.10.1.61",
            "DL_port": "5261",
        },
        {
            "UL_addr": "192.168.63.62",
            "UL_port": "5162",
            "DL_addr": "172.10.1.62",
            "DL_port": "5262",
        },
        {
            "UL_addr": "192.168.63.63",
            "UL_port": "5163",
            "DL_addr": "172.10.1.63",
            "DL_port": "5263",
        },
        {
            "UL_addr": "192.168.63.64",
            "UL_port": "5164",
            "DL_addr": "172.10.1.64",
            "DL_port": "5264",
        },
        {
            "UL_addr": "192.168.63.65",
            "UL_port": "5165",
            "DL_addr": "172.10.1.65",
            "DL_port": "5265",
        },
        {
            "UL_addr": "192.168.63.66",
            "UL_port": "5166",
            "DL_addr": "172.10.1.66",
            "DL_port": "5266",
        },
        {
            "UL_addr": "192.168.63.67",
            "UL_port": "5167",
            "DL_addr": "172.10.1.67",
            "DL_port": "5267",
        },
        {
            "UL_addr": "192.168.63.68",
            "UL_port": "5168",
            "DL_addr": "172.10.1.68",
            "DL_port": "5268",
        },
        {
            "UL_addr": "192.168.63.69",
            "UL_port": "5169",
            "DL_addr": "172.10.1.69",
            "DL_port": "5269",
        },
        {
            "UL_addr": "192.168.63.70",
            "UL_port": "5170",
            "DL_addr": "172.10.1.70",
            "DL_port": "5270",
        },
        {
            "UL_addr": "192.168.63.71",
            "UL_port": "5171",
            "DL_addr": "172.10.1.71",
            "DL_port": "5271",
        },
        {
            "UL_addr": "192.168.63.72",
            "UL_port": "5172",
            "DL_addr": "172.10.1.72",
            "DL_port": "5272",
        },
        {
            "UL_addr": "192.168.63.73",
            "UL_port": "5173",
            "DL_addr": "172.10.1.73",
            "DL_port": "5273",
        },
        {
            "UL_addr": "192.168.63.74",
            "UL_port": "5174",
            "DL_addr": "172.10.1.74",
            "DL_port": "5274",
        },
        {
            "UL_addr": "192.168.63.75",
            "UL_port": "5175",
            "DL_addr": "172.10.1.75",
            "DL_port": "5275",
        },
        {
            "UL_addr": "192.168.63.76",
            "UL_port": "5176",
            "DL_addr": "172.10.1.76",
            "DL_port": "5276",
        },
        {
            "UL_addr": "192.168.63.77",
            "UL_port": "5177",
            "DL_addr": "172.10.1.77",
            "DL_port": "5277",
        },
        {
            "UL_addr": "192.168.63.78",
            "UL_port": "5178",
            "DL_addr": "172.10.1.78",
            "DL_port": "5278",
        },
        {
            "UL_addr": "192.168.63.79",
            "UL_port": "5179",
            "DL_addr": "172.10.1.79",
            "DL_port": "5279",
        },
        {
            "UL_addr": "192.168.63.80",
            "UL_port": "5180",
            "DL_addr": "172.10.1.80",
            "DL_port": "5280",
        },
        {
            "UL_addr": "192.168.63.81",
            "UL_port": "5181",
            "DL_addr": "172.10.1.81",
            "DL_port": "5281",
        },
        {
            "UL_addr": "192.168.63.82",
            "UL_port": "5182",
            "DL_addr": "172.10.1.82",
            "DL_port": "5282",
        },
        {
            "UL_addr": "192.168.63.83",
            "UL_port": "5183",
            "DL_addr": "172.10.1.83",
            "DL_port": "5283",
        },
        {
            "UL_addr": "192.168.63.84",
            "UL_port": "5184",
            "DL_addr": "172.10.1.84",
            "DL_port": "5284",
        },
        {
            "UL_addr": "192.168.63.85",
            "UL_port": "5185",
            "DL_addr": "172.10.1.85",
            "DL_port": "5285",
        },
        {
            "UL_addr": "192.168.63.86",
            "UL_port": "5186",
            "DL_addr": "172.10.1.86",
            "DL_port": "5286",
        },
        {
            "UL_addr": "192.168.63.87",
            "UL_port": "5187",
            "DL_addr": "172.10.1.87",
            "DL_port": "5287",
        },
        {
            "UL_addr": "192.168.63.88",
            "UL_port": "5188",
            "DL_addr": "172.10.1.88",
            "DL_port": "5288",
        },
        {
            "UL_addr": "192.168.63.89",
            "UL_port": "5189",
            "DL_addr": "172.10.1.89",
            "DL_port": "5289",
        },
        {
            "UL_addr": "192.168.63.90",
            "UL_port": "5190",
            "DL_addr": "172.10.1.90",
            "DL_port": "5290",
        },
    ],
}


# Variables from eCLAT
eclat = None
if "WORKSPACE" in os.environ:
    eclat = {
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
    if not os.path.isdir(PATH_Storage):
        if os.path.exists(PATH_Storage):
            shutil.rmtree(PATH_Storage)
        os.makedirs(PATH_Storage)
    PATH_RESOURCES = "%s/resources" % (os.environ["HOME"])
    if not os.path.isdir(PATH_RESOURCES):
        if os.path.exists(PATH_RESOURCES):
            shutil.rmtree(PATH_RESOURCES)
        os.makedirs(PATH_RESOURCES)
    PATH_Tools = "%s/resources/tools" % (os.environ["HOME"])
    if not os.path.isdir(PATH_Tools):
        if os.path.exists(PATH_Tools):
            shutil.rmtree(PATH_Tools)
        os.makedirs(PATH_Tools)

# Custom Values
custom = {
    "TL_Number": "063",
    "PATH_Tools": PATH_Tools,
    "PATH_Storage": PATH_Storage,
    "eclat": eclat,
    # Values linked to the gNB
    "BTS_ID": "1900",
    "GNB_Friendly_TL_Name": "CV063",
    "GNB_Architecture": "CLASSICAL",
    "GNB_First_CellID": "1",
    "GNB_First_Cell_nrArfcn": "2071592",
}
