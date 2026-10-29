__maintainer__ = "Cao Zhaojun"
__team__ = "I_MN_SRAN_ENG2_HZ_AIC_EXPLORER@internal.nsn.com"
__email__ = "I_MN_SRAN_ENG2_HZ_AIC_EXPLORER@internal.nsn.com"
__owner_email__ = "zhaojun.cao@nokia-sbell.com"

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
from taf.config.testline.lab_infrastructure import PxeServer
from taf.config.testline.core import RealCore
from taf.config.testline.connection_details import K8SConnectionDetails
from taf.config.testline.gnb.du import FHGW
from taf.config.testline.gnb.du import VDU
from taf.config.testline.cloud_hosting import MasterNode, K8S, HelmChart
from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.config.testline.radio import RU
from taf.config.testline.nms import NMS
from taf.config.testline.nom import NOM
from taf.config.testline.nms import Netact
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import Android, Qualcomm
from taf.config.testline.pdu import FPFH
from taf.config.testline.attenuator import TopYoung, HBTE
from taf.config.testline.pdu import HBTE as PBHBTE
from taf.config.testline.appserver import TafUeAppServer
from taf.config.testline import TafUeDataTransferProtocol
from taf.config.testline.pdn import PDNTafUeAndroidDetails
from taf.config.testline.ue import TafUeAndroid

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

_ru_pdu_1 = PBHBTE(addr="10.56.99.7", port_numbers=[4])

# this is test PC for AIC, including UTE IP address, User Name and Password.


# ######## start of vCU ##########################################################
# VCU related NCIR controlNode
_control = ControlNode(
    # Configuration for SSH access
    default_ssh_connection_details=SshServiceDetails(
        addr="10.110.37.2", username="cranuser12", password="systeM!23"
    ),
    # Configuration for openstack connection
    open_stack_connection_details=OpenStackConnectionDetails(
        username="cranuser12",
        password="systeM!23",
        ip_addr="10.110.37.2",
        tenant="cran12",
    ),
    # Configuration for BMC access if you need use it in test case, plase config it
    # currently, it's not used in agent
    bmc_connection_details=BmcConnectionDetails(addr="", username="", password=""),
)

# configuration of VCU related NCIR/OSP
_ncir = NCIR(compute_nodes=[], control_nodes=[_control], version="ncir_19")

# CloudBts deployment
flavor_env_files = [os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/5gbts_flavor.env")]
net_env_files = [os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/5gbts_ext_net.env")]
vnf_env_files = [os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/5gbts_heat.env")]


# #################### START of VCU CNF platform ##########################
_vcu_intnet_1 = DeploymentNetworkStack(
    name="aic-vcu-intnet",
    yaml_file=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/aic_intnet_values_override_0.yaml"
    ),
)

_vcu_vnf_1 = DeploymentVnfStack(
    name="aic-vcu-cnf",
    yaml_file=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/aic_vdu_values_override_0.yaml"
    ),
)


# ssh connection information of OE, for tenant user
_vcu_ssh_connection_details = SshServiceDetails(
    addr="10.110.10.98", username="cranuser10", password="systeM!23"
)
# ssh connection information of OE, for root user
_vcu_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.110.10.98", username="core", password="system123", port="22"
)

_vcu_master_node = MasterNode(
    k8s_connection_details=_vcu_k8s_connection_details,
    ssh_connection_details=_vcu_ssh_connection_details,
)

_vcu_k8s = K8S(namespace="cran10", master_node=_vcu_master_node)

_cluster_preparation_cu_1 = HelmChart(
    name="preparation-cu",
    yaml_file=os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/vcu_preparation_11132.yaml"),
)

_prerequisite_cu_1 = HelmChart(
    name="prerequisite-cu",
    yaml_file=os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/vcu_prerequisite_11132.yaml"),
)

_cnf_cu_1 = HelmChart(
    name="cnf-cu",
    yaml_file=os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/vcu_cnf_11132.yaml"),
)

_vcu_k8s_cloud_deployment = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    networks=[_vcu_intnet_1],
    cluster_preparation=_cluster_preparation_cu_1,
    prerequisite=_prerequisite_cu_1,
    cnf=_cnf_cu_1,
    vnfs=[_vcu_vnf_1],
    cloud_hosting=_vcu_k8s,
)
# #################### End of VCU CNF platform ##########################

# CU configuration
_cu = CU(
    # CU web UI ip address, oam interface ip of oam vm
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.110.177.205"
        # v6='2a00:8a00:8000:136:10:57:159:1111'
    ),
    # VCU OAM ssh connection, oam interface ip of oam vm
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.110.10.98",
        # username="serviceuser",
        username="cranuser10",
        password="systeM!23",
        # password="Pl(FzaYj5~c5;q"
    ),
    # VCU OAM http connection, oam interface ip of oam vm
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.110.177.205", username="Nemuadmin", password="nemuuser", port="443"
    ),
    # route configuration for x2 link to ENB, v4 is network address of ENB x2 link
    # route configuration for f1c link to VDU on VCU, v4 is network address of VDU f1c link
    f1c=NetworkAddress(
        v4="10.108.207.218", routing_v4=RoutingInformation(gateway="10.108.207.217")
    ),
    # route configuration for f1u link to VDU on VCU, v4 is network address of VDU f1u link
    f1u=NetworkAddress(
        v4="10.108.207.219", routing_v4=RoutingInformation(gateway="10.108.207.217")
    ),
    tracing=None,
    global_bts_id=11132,
)

# mcc, mnc configuration
_realcore = RealCore(five_g=None, mcc="262", mnc="03", pdns=None)


# ######## start of ENB #############################
_capacity_unit = CapacityUnit(addr="6.6.6.6")

_common_unit = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.97.120.141", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_capacity_unit],
)

_airscale = Airscale(common_units=[_common_unit])

_real_enb = RealEnb(airscale=_airscale, oam_ip="10.97.122.4")

# you can configure it as AIC UTE environment
_enb_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.108.229.250", username="ute", password="ute"
    ),
    connections=[_real_enb],
)


# ######## start of vDU ######################################################
# VDU deployment
_vdu_vnf_0 = DeploymentVnfStack(
    # this is vdu release name, the name should only be lower case and only can include alphabet, number,
    name="aic-vdu",
    yaml_file=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/aic_vdu_values_override_0.yaml"
    ),
)

_vdu_intnet_0 = DeploymentNetworkStack(
    # this is intnet release name, the name should only be lower case and only can include alphabet, number,
    name="aic-intnet",
    yaml_file=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/aic_intnet_values_override_0.yaml"
    ),
)

# ssh connection information of OE, for tenant user
_ssh_connection_details_0 = SshServiceDetails(
    addr="10.69.13.34", username="cranuser1", password="systeM!23"
)
# ssh connection information of OE, for cloudadmin user
# ip_addr="10.97.119.62", username="core", password="system123", port="22"
_k8s_connection_details_0 = K8SConnectionDetails(
    ip_addr="10.69.13.34", username="core", password="system123", port="22"
)

_master_node_0 = MasterNode(
    k8s_connection_details=_k8s_connection_details_0,
    ssh_connection_details=_ssh_connection_details_0,
)
_k8s_0 = K8S(namespace="cran1", master_node=_master_node_0)

_cluster_preparation_du_1 = HelmChart(
    name="preparation-vdu",
    yaml_file=os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/vdu_preparation_11131.yaml"),
)

_prerequisite_du_1 = HelmChart(
    name="prerequisite-vdu",
    yaml_file=os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/vdu_prerequisite_11131.yaml"),
)

_cnf_du_1 = HelmChart(
    name="cnf-vdu",
    yaml_file=os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/vdu_cnf_11131.yaml"),
)

_k8s_cloud_deployment_0 = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    networks=[_vdu_intnet_0],
    vnfs=[_vdu_vnf_0],
    cloud_hosting=_k8s_0,
    cluster_preparation=_cluster_preparation_du_1,
    prerequisite=_prerequisite_du_1,
    cnf=_cnf_du_1,
)

_vdu_oam_http_connection_details = HttpConnectionDetails(
    addr="10.69.13.66", port="443", username="Nemuadmin", password="nemuuser"
)

# RU PDU
# _ru_pdu = PBHBTE(addr="10.97.122.137", port_numbers=[3])
_ru_pdu = FPFH(
    addr="10.56.99.7",
    port_numbers=[1, 2, 3, 4, 5, 6],
    login="admin",
    password="admin",
)

_attenuator_5G = TopYoung(
    ip_addr="10.56.99.19",
    port=3000,
    attenuation_port_numbers=[i for i in range(257)],
    model="32X8",
)

# RU configuration

_ru_1 = RU(
    ru_hw_group="RU_INT_ECPRI",
    radio_type="AEQY",
    serial_number="1M223231024",
    attenuation_ports=[
        _attenuator_5G.attenuator_ports[13],
        _attenuator_5G.attenuator_ports[14],
        _attenuator_5G.attenuator_ports[15],
        _attenuator_5G.attenuator_ports[16],
    ],
    # pdu_port=_ru_pdu.pdu_ports[3]
    pdu_port=_ru_pdu.pdu_ports[4],
)


_pxe_server_ssh_info = SshServiceDetails(
    addr="10.108.204.30", username="root", password="pxe@systeM!23"
)
_pxe_server = PxeServer(
    nfs_ip="10.108.204.30", ssh_connection_details=_pxe_server_ssh_info
)

# FHGW information
_fhgw_0 = FHGW(
    user_config_path=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/FHGW_0/user_config_0.yaml"
    ),
    rus=[_ru_1],
    pxe_server=_pxe_server,
    fhgw_id=11131,

)
_fhgw_0.ru_ports = ["16", "17", "18"]
_fhgw_0.ssh_username = "toor4nsn"
_fhgw_0.ssh_password = "Fhgw@nokia123"

_vdu_0 = VDU(
    cloud_deployment=_k8s_cloud_deployment_0,
    oam_http_connection_details=_vdu_oam_http_connection_details,
    fhgws=[_fhgw_0],
    # route configuration of f1m link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_m_ip_addr=NetworkAddress(
        v4="10.107.92.15/25",
        vlan_id=None,
        routing_v4=RoutingInformation(gateway="10.108.207.81"),
    ),
    # route configuration of f1c link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_c_ip_addr=NetworkAddress(
        v4="10.20.146.98/29",
        vlan_id=None,
        routing_v4=RoutingInformation(gateway="10.108.207.73"),
    ),
    # route configuration of f1u link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_u_ip_addr=NetworkAddress(
        v4="10.20.146.74/29",
        vlan_id=None,
        routing_v4=RoutingInformation(gateway="10.108.207.73"),
    ),
    instance_id=11131,
    global_bts_id=11131,
)


# ######## start of NOM ######################################################
_nom_ssh_connection_edge0 = SshServiceDetails(
    addr="10.27.137.179", username="cloud-user"
)
_nom22 = NOM(
    ssh_connections_info=[_nom_ssh_connection_edge0],
    https_main_info=HttpConnectionDetails(
        addr="https://neo8256.dyn.nesc.nokia.net/",
        username="neonetics",
        password="Nokia123_",
    ),
    https_user_mgmt_info=HttpConnectionDetails(
        addr="https://neo8256.dyn.nesc.nokia.net/"
    ),
    https_rest_info=HttpConnectionDetails(addr="https://neo8256.dyn.nesc.nokia.net/"),
    neo_endpoints_ip="100.74.46.141",
)

_cnms = NMS(addr="100.74.46.147", nom=_nom22)


# ######## start of NOM ######################################################
# _nom_ssh_connection_edge0 = SshServiceDetails(
# addr="10.110.73.148", username="cloud-user"
# )
# _nom1 = NOM(
# ssh_connections_info=[_nom_ssh_connection_edge0],
# https_main_info=HttpConnectionDetails(
# addr="https://neo-hosting-page.srncnms07.srnblr.nsn-rdnet.net/",
# username="cnms01",
# password="Qwer_1234",
# ),
# https_user_mgmt_info=HttpConnectionDetails(
# addr="https://user-mgmt.srncnms07.srnblr.nsn-rdnet.net"
# ),
# https_rest_info=HttpConnectionDetails(
# addr="https://apigw.srncnms07.srnblr.nsn-rdnet.net"
# ),
# neo_endpoints_ip="10.110.73.149",
# )

# _cnms = NMS(addr="10.110.73.148", nom=_nom1)


# ######## start of Netact ######################################################
# _netact_info = {
#     "netact_info1": {
#         "netact_id": "clab3766",
#         "node_ip": "10.32.217.23",
#         "user": "omc",
#         "password": "omc",
#         "url": "https://clab3766lbwas.netact.nsn-rdnet.net",
#         "url_user": "omc",
#         "url_password": "omc",
#         "mr": "MRC-VRAN2.0/MR-10820",
#     },
#     "netact_info2": {
#         "netact_id": "clab3386",
#         "node_ip": "10.32.217.141",
#         "user": "omc",
#         "password": "omc",
#         "url": "https://clab3386lbwas.netact.nsn-rdnet.net",
#         "url_user": "omc",
#         "url_password": "omc",
#         "mr": "MRC-1/MR-1",
#     },
# }
#
# _netact = [_netact_info]

netact_id = {
    "clab3766": {
        "node_ip": "10.32.217.23",
        "user": "omc",
        "password": "omc",
        "url": "https://clab3766lbwas.netact.nsn-rdnet.net",
        "url_user": "omc",
        "url_password": "omc",
        "mr": "MRC-5GAIC/MR-Explorer",
    },
    "clab152": {
        "node_ip": "10.92.135.231",
        "user": "omc",
        "password": "omc",
        "url": "https://clab152lbwas.netact.nsn-rdnet.net",
        "url_user": "omc",
        "url_password": "omc",
        "mr": "MRC-1/MR-1",
    },
}


_netact = Netact(netact_id)

# vcu CNF: _vcu_k8s_cloud_deployment
_cbts_0 = CloudBts(
    dus=[_vdu_0],  # vdu related parameter
    cu=_cu,
    cloud_deployment=_vcu_k8s_cloud_deployment,
    vnf_name="cran10",
    instance_id="11131",
    global_bts_id="11131",
)


_tools_repository = {
    "ip": "10.108.229.152",
    "username": "ute",
    "password": "QAZqaz123@#",
    "repo_tool_folder": "/opt/tools/trans_test/",
    "repo_data_folder": "/opt/tools/trans_data/",
    "repo_simu4trs_folder": "/opt/tools/trans_simu4trs/",
}

_switch_1 = {
    "du_switch_ip": "10.108.215.13",
    "username": "cisco",
    "password": "cisco",
    "en_password": "",
    "port": "22",
    "prompt": "#",
}

_fhgw_misc = {
    "ruproxy_create_tool": "create_ruproxy_new.py",
    "ruproxy_delete_tool": "remove_ruproxy_new.py",
}

_trans_para = {
    "tools_repository": _tools_repository,
    "du_switch": [_switch_1],
    "fhgw_misc": _fhgw_misc,
}

#  UE
# _appserver_ssh = SshServiceDetails(addr="10.108.229.127", username="ute", password="ute")
_appserver_ssh = SshServiceDetails(
    addr="10.108.229.250", username="ute", password="ute"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh, network_interface_address="10.108.229.250"
)
_pdn1 = PDNTafUeAndroidDetails(
    entryName="stdata2", apnName="stdata2", apnType=["DEFAULT"]
)

_app_server_1 = TafUeAppServer(
    app_server_name="APP_1",
    address="10.108.229.107",
    user="ute",
    password="QAZqaz123!@#",
)
_data_transfer_iperf = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_app_server_1,
    interval=1,  # binary_path='/data/data/com.nokia.android.application/',
    interface_name="rmnet_data0",
    server_close_delay=50,
    version=3,
)

_android = TafUeAndroid(
    ssh_connection_details=SshServiceDetails(
        addr="10.56.99.6", username="pz2", password="Nokia@2w3e4r5t6y7u"
    ),
    data_transfer=[_data_transfer_iperf],
    ue_pc_address="10.56.99.6",
    serial_number="R5CR31EZL3L",  # R5CN20LYP5R R5CN20HRWLM R5CN212N3RX R5CR31EZL3L R5CR41BNAWM
    # server_dir="/cygdrive/c/pyro_server",
    # python_path="C:/Python27/python.exe",
    # qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    # diag_cfg_path="C:/pyro_server/DIAG.cfg",
    pdns=[_pdn1],
    service_call_attach="17",
    service_call_detach="17",
    ue_pc_port="8080",
    # iperf_details=_iperf,
    capabilities=["REAL_UE"],
)

_hbte_params = {
    "ip_addr": "10.69.85.44",
    "port": 5000,
    "attenuation_port_numbers": [1, 2, 5, 6],
    "model": "PA-16-2-6-127-0.5",
    "version": None,
}
_attenuator_5G = HBTE(**_hbte_params)

# RU configuration
_ru_1 = RU(
    ru_hw_group="RU_INT_ECPRI",
    serial_number="K9190632303",
    attenuation_ports=[
        _attenuator_5G.attenuator_ports[1],
        _attenuator_5G.attenuator_ports[2],
        _attenuator_5G.attenuator_ports[5],
        _attenuator_5G.attenuator_ports[6],
    ],
    pdu_port=_ru_pdu_1.pdu_ports[4],
)

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.108.229.253", username="ute", password="ute"
    ),
    connections=[_cbts_0],
)

_real_enb = RealEnb(oam_ip="10.97.122.11", instance_id="10786", rms=[])
# Testline configuration, tl is only variable which can be accessed by agent and test case
# you can access all parameters configured upper by tl parameter
# CNUMS: nms=_cnms,
# Netact: nms=_netact
tl = TestLine(
    test_pc=_test_pc,
    nms=_netact,
    gnbs=[_cbts_0],
    enbs=[_real_enb],
    tl_cloud_topology="CLOUD_5G_CR__4__SA_TDD__CU_MNO_HA__VDU_OE22_DRAN_SNO__2xAEQY__FHGW",
    cloud_hostings=[_ncir],
    test_pcs=[_test_pc],
    core=_realcore,
    ues=[_android],
    attenuators=[_attenuator_5G],
)

_misc = {
    # 1-Use NOM config in __init__.py, 0-Use NOM config in global_variable.py.
    # If this key is not given, default value is 1
    "nom_config_source_from_init_py": "0",
    # 1-Use Netact config in __init__.py, 0-Use Netact config in global_variable.py.
    # If this key is not given, default value is 1
    "netact_config_source_from_init_py": "0",
}
tl._misc = _misc

# it's a WA, please see https://jira3.int.net.nokia.com/browse/TALIB-846,
# this jira has blocked a few transport TA cases design and debug
# one of other WA is declare a global python variable, 'TRANS_PARA = _trans_para'
# i don't know which WA is better, please give me suggestion if you like to change WA.
tl._trans_para = _trans_para

__all__ = ["tl"]
