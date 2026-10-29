__maintainer__ = "Xian Xue"
__team__ = ""
__email__ = ""
__owner_email__ = "xue.xian@nokia-sbell.com"

import os

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
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline import RealEnb, NetworkAddress, RoutingInformation
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU
from taf.config.testline import DU
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC
from taf.config.testline.lab_infrastructure import PxeServer
from taf.config.testline.attenuator import HBTE
from taf.config.testline.core import RealCore
from taf.config.testline.ue import Android, Qualcomm

######################VDU###########################
## following are VDU related class which defined
## in taf.config.testline
## you can uncomment them when new version of
## taf.config.testline merged
#######################VDU##########################
from taf.config.testline.connection_details import K8SConnectionDetails
from taf.config.testline.gnb.du import FHGW
from taf.config.testline.gnb.du import VDU
from taf.config.testline.cloud_hosting import MasterNode, K8S
from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.config.testline.gnb.networkaddress import RoutingInformation
from taf.config.testline.radio import RU
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.nms import NMS
from taf.config.testline.nom import NOM

# Following all parameters should be configured for one testline
# please don't ignore any parameters, you can add, but don't ingore
# any problem, please check with CI team

#####  FOLLOWING ARE CHECKLIST OF TESTLINE CONFIGURATION #######

#  1. 5gbts_ext_net.env have been configured as following
#  2. 5gbts_flavor.env have been configured as following
#  3. 5gbts_heat.env have been configured as following
#  4. aic-intnet-values-override_x.yaml have been configured as following
#  5. aic-vdu-values-override_x.yaml have been configured as following
#  6. user_config_x.yaml have been configured as following (currently, it's not used)
#  7. "vnf_prefix" in 5gbts_flavor.env should be re-configued, don't use common flavor name
#  8. vnf_prefix naming rule should be flavor-<testline name>, e.g: flavor-7_5_UTE5GAIC001T001
#  9. "flavors" in 5gbts_heat.env should be configured and prefix should equal to vnf_prefix value configured on 5gbts_flavor.env
#  10. please make sure 5gbts_ext_net.env, 5gbts_flavor.env, 5gbts_heat.env are new enough for next build
#  11. please make sure aic-intnet-values-override_x.yaml and aic-vdu-values-override_x.yaml are new enough for next build
#  12. please make sure files in step 1,2,3,4,5 have valid configuration
#  13. please make sure ip address of NCIR and test pc can be accessible by network
#  14. please make sure VDU on OE have been cleared or VDU helm release name is equal to name of DeploymentVnfStack before start agent_5g_aic
#  15. please make sure VCU on NCIR have been cleared or VCU stack name is TL_<testline name>_BTS before start agent_5g_aic
#################################################################


_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# this is test PC for AIC, including UTE IP address, User Name and Password.
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.108.229.147", username="ute", password="QAZqaz123!@#"
    )
)

# ######## start of vCU ##########################################################
# NCIR
_control = ControlNode(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.110.9.116", username="cranuser27", password="systeM!23"
    ),
    open_stack_connection_details=OpenStackConnectionDetails(
        username="cranuser27",
        password="systeM!23",
        ip_addr="10.110.9.116",
        tenant="cran27",
    ),
    bmc_connection_details=BmcConnectionDetails(addr="", username="", password=""),
)

_ncir = NCIR(compute_nodes=[], control_nodes=[_control], version="ncir_19")
# enb
_hbte_params_1 = {
    "ip_addr": "10.97.122.133",
    "port": 5000,
    "attenuation_port_numbers": [4, 8],
    "model": "PA-8-8-4-127-0.5-B-S",
    "version": None,
}
_attenuator_4G = HBTE(**_hbte_params_1)
_ru_4 = RU(
    ru_hw_group="hw_group",
    attenuation_ports=[
        _attenuator_4G.attenuator_ports[4],
        _attenuator_4G.attenuator_ports[8],
    ],
)
# CloudBts deployment
flavor_env_files = [os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/5gbts_flavor.env")]
net_env_files = [os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/5gbts_ext_net.env")]
vnf_env_files = [os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/5gbts_heat.env")]

_cbts_flavor = DeploymentFlavorStack(
    name="name is not used", env_files=flavor_env_files, default_vnf_prefix="hgz-tl5555"
)

_cbts_net = DeploymentNetworkStack(
    name="name is not used",
    env_files=net_env_files,
    yaml_file=os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/5gbts_ext_net.yaml"),
)

_cbts_vnf = DeploymentVnfStack(
    name="name is not used",
    env_files=vnf_env_files,
    yaml_file=os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/5gbts_heat.yaml"),
)

_cloud_deployment = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    flavors=[_cbts_flavor],
    networks=[_cbts_net],
    vnfs=[_cbts_vnf],
    cloud_hosting=_ncir,
)


_cu = CU(
    # CU web UI ip address, oam interface ip of oam vm
    backhaul_site_oam_ip=NetworkAddress(v6="2a00:8a00:8000:5801:0:4:0:30"),
    # VCU OAM ssh connection, oam interface ip of oam vm
    oam_ssh_connection_details=SshServiceDetails(
        addr="2a00:8a00:8000:5801:0:4:0:30",
        username="serviceuser",
        password="Pl(FzaYj5~c5;q",
    ),
    # VCU OAM http connection, oam interface ip of oam vm
    oam_http_connection_details=HttpConnectionDetails(
        addr="2a00:8a00:8000:5801:0:4:0:30",
        username="Nemuadmin",
        password="nemuuser",
        port="443",
    ),
    # route configuration for x2 link to ENB, v4 is network address of ENB x2 link
    x2c=NetworkAddress(
        v6="2a00:8a00:8000:5801:0:6:0:30",
        vlan_id=None,
        routing=RoutingInformation(
            gateway="2a00:8a00:8000:5801:0:6:0:1", ip_prefix_length=120
        ),
    ),
    # route configuration for f1c link to VDU on VCU, v4 is network address of VDU f1c link
    f1c=NetworkAddress(
        v6="2a00:8a00:8000:5801:0:5:0:30",
        vlan_id=None,
        routing=RoutingInformation(
            gateway="2a00:8a00:8000:5801:0:5:0:1", ip_prefix_length=120
        ),
    ),
    # route configuration for f1u link to VDU on VCU, v4 is network address of VDU f1u link
    f1u=NetworkAddress(
        v6="2a00:8a00:8000:5801:0:5:0:30",
        vlan_id=None,
        routing=RoutingInformation(
            gateway="2a00:8a00:8000:5801:0:9:0:1", ip_prefix_length=120
        ),
    ),
    tracing=None,
    global_bts_id=5472,
)

# mcc, mnc configuration
_realcore = RealCore(five_g=None, mcc="262", mnc="03", pdns=None)


# ######## start of ENB #############################
_capacity_unit = CapacityUnit(addr="6.6.6.6")

_common_unit = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.97.122.234", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_capacity_unit],
)

_airscale = Airscale(common_units=[_common_unit])

_real_enb = RealEnb(
    airscale=_airscale,
    oam_ip="10.97.122.234",
    global_bts_id="5147",
    rms=[_ru_4],
)

# you can configure it as AIC UTE environment
_enb_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.108.229.147", username="ute", password="QAZqaz123!@#"
    ),
    connections=[_real_enb],
)


# ######## start of vDU ######################################################
# VDU deployment
_vdu_vnf_1 = DeploymentVnfStack(
    # this is vdu release name, the name should only be lower case and only can include alphabet, number,
    name="vducran1",
    yaml_file=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/one_click_ne_deploy.yaml"
    ),
)

_vdu_intnet_0 = DeploymentNetworkStack(
    # this is intnet release name, the name should only be lower case and only can include alphabet, number,
    name="aic-intnet",
    yaml_file=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/aic_intnet_values_override_0.yaml"
    ),
)

_ssh_connection_details_0 = SshServiceDetails(
    addr="10.71.172.62", username="cranuser1", password="systeM!23"
)
_k8s_connection_details_0 = K8SConnectionDetails(
    ip_addr="10.71.172.62", username="core", password="system123", port="22"
)

_master_node_0 = MasterNode(
    k8s_connection_details=_k8s_connection_details_0,
    ssh_connection_details=_ssh_connection_details_0,
)
_k8s_0 = K8S(namespace="cran1", master_node=_master_node_0)
_k8s_cloud_deployment_0 = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    networks=[_vdu_intnet_0],
    vnfs=[_vdu_vnf_1],
    cloud_hosting=_k8s_0,
)

_vdu_oam_http_connection_details = HttpConnectionDetails(
    addr="2a00:8a00:8000:117:1:2:a47:ac12",
    port="443",
    username="Nemuadmin",
    password="nemuuser",
)
# RU configuration
_hbte_params = {
    "ip_addr": "10.97.122.133",
    "port": 5000,
    "attenuation_port_numbers": [1, 2, 3, 4, 5, 6, 7, 8],
    "model": "PA-8-8-4-127-0.5-B-S",
    "version": None,
}
_attenuator_5G = HBTE(**_hbte_params)

# RU configuration
_ru_0 = RU(
    ru_hw_group="RU_INT_CPRI",
    serial_number="K9190632462",
    attenuation_ports=[
        _attenuator_5G.attenuator_ports[1],
        _attenuator_5G.attenuator_ports[5],
    ],
)
_ru_1 = RU(
    ru_hw_group="RU_INT_CPRI",
    serial_number="K9190632533",
    attenuation_ports=[
        _attenuator_5G.attenuator_ports[2],
        _attenuator_5G.attenuator_ports[6],
    ],
)
_ru_2 = RU(
    ru_hw_group="RU_INT_CPRI",
    serial_number="K9190632302",
    attenuation_ports=[
        _attenuator_5G.attenuator_ports[3],
        _attenuator_5G.attenuator_ports[7],
    ],
)
# PXE server info for FHGW deployment
_pxe_server_ssh_info = SshServiceDetails(
    addr="10.68.179.27", username="root", password="centos"
)
_pxe_server = PxeServer(
    nfs_ip="10.68.179.27", ssh_connection_details=_pxe_server_ssh_info
)

# FHGW information
_fhgw_0 = FHGW(
    user_config_path=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/FHGW_0/fhgw_user_config_0.yaml"
    ),
    rus=[_ru_0, _ru_1, _ru_2],
    pxe_server=_pxe_server,
)
_vdu_0 = VDU(
    cloud_deployment=_k8s_cloud_deployment_0,
    oam_http_connection_details=_vdu_oam_http_connection_details,
    fhgws=[_fhgw_0],
    # route configuration of f1m link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_m_ip_addr=NetworkAddress(
        v6="2a00:8a00:8000:5002:0:3:0:100",
        vlan_id=None,
        routing=RoutingInformation(
            gateway="2a00:8a00:8000:117:1:2:a47:ac09", ip_prefix_length=120
        ),
    ),
    # route configuration of f1c link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_c_ip_addr=NetworkAddress(
        v6="2a00:8a00:8000:5801:0:5:0:0",
        vlan_id=None,
        routing=RoutingInformation(
            gateway="2a00:8a00:8000:117:1:2:a47:ac09", ip_prefix_length=120
        ),
    ),
    # route configuration of f1u link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_u_ip_addr=NetworkAddress(
        v6="2a00:8a00:8000:5801:0:5:0:0",
        vlan_id=None,
        routing=RoutingInformation(
            gateway="2a00:8a00:8000:117:1:2:a47:ac09", ip_prefix_length=120
        ),
    ),
    instance_id=5472,
)

_appserver_ssh = SshServiceDetails(
    addr="10.108.229.140", username="ute", password="QAZqaz123!@#"
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.108.229.140",
)
_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.97.122.172", username="aic", password="Nokia123!"
    ),
    serial_number="R5CN20TXGBP",  # R5CN20LYP5R R5CN20HRWLM R5CN212N3RX
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "samsung"],
)

# ######## start of NOM ######################################################
_nom_ssh_connection_edge0 = SshServiceDetails(
    addr="2a00:8a00:8000:5801:0:e:0:428", username="cloud-user"
)

_nom1 = NOM(
    ssh_connections_info=[_nom_ssh_connection_edge0],
    https_main_info=HttpConnectionDetails(
        addr="https://neo-hosting-page.srncnms10.srnblr.nsn-rdnet.net/",
        username="neonetics",
        password="Nokia_150",
    ),
    https_user_mgmt_info=HttpConnectionDetails(
        addr="https://user-mgmt.srncnms10.srnblr.nsn-rdnet.net",
    ),
    https_rest_info=HttpConnectionDetails(
        addr="https://apigw.srncnms10.srnblr.nsn-rdnet.net",
    ),
    neo_endpoints_ip="[2a00:8a00:8000:5801:0:e:0:42b]",
)

_cnms = NMS(addr="2a00:8a00:8000:5801:0:e:0:428", nom=_nom1)

_cbts = CloudBts(
    dus=[_vdu_0],
    cu=_cu,
    cloud_deployment=_cloud_deployment,
    vnf_name="5472-5gbts",
    instance_id="5472",
)


_tools_repository = {
    "ip": "10.108.229.152",
    "username": "ute",
    "password": "ute",
    "repo_tool_folder": "/opt/tools/trans_test/",
    "repo_data_folder": "/opt/tools/trans_data/",
    "repo_simu4trs_folder": "/opt/tools/trans_simu4trs/",
}

# Testline configuration, tl is only variable which can be accessed by agent and test case
# you can access all parameters configured upper by tl parameter
tl = TestLine(
    test_pc=_test_pc,
    nms=_cnms,
    attenuators=[_attenuator_5G, _attenuator_4G],
    gnbs=[_cbts],
    enbs=[_real_enb],
    tl_cloud_topology="CLOUD_5G_AIC_NCIR_NCIR_FHGW_3xAHBCC",
    cloud_hostings=[_ncir],
    test_pcs=[_enb_test_pc],
    ues=[_android],
    core=_realcore,
)

# it's a WA, please see https://jira3.int.net.nokia.com/browse/TALIB-846,
# this jira has blocked a few transport TA cases design and debug
# one of other WA is declare a global python variable, 'TRANS_PARA = _trans_para'
# i don't know which WA is better, please give me suggestion if you like to change WA.


__all__ = ["tl"]
