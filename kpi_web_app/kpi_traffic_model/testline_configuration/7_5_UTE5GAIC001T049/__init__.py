__maintainer__ = "Zhao ling"
__team__ = "I_NSB_MN_5GSC_5GSW_ENG_AIC_SI_CN_2SISO_GMS <I_NSB_MN_5GSC_5GSW_ENG_AIC_SI_CN_2SISO@internal.nsn.com>"
__email__ = "I_NSB_MN_5GSC_5GSW_ENG_AIC_SI_CN_2SISO@internal.nsn.com"
__owner_email__ = "ling.2.zhao@nokia-sbell.com"

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
    IperfDataTransferDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline import RealEnb, NetworkAddress, RoutingInformation
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU
from taf.config.testline.lab_infrastructure import PxeServer
from taf.config.testline.core import RealCore
from taf.config.testline.ue import Android, Qualcomm
from taf.config.testline.connection_details import K8SConnectionDetails
from taf.config.testline.gnb.du import FHGW
from taf.config.testline.gnb.du import VDU
from taf.config.testline.cloud_hosting import MasterNode, K8S, ComputeNode, HelmChart
from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.config.testline.radio import RU
from taf.config.testline.pdu import TopYoung as TP
from taf.config.testline.nms import NMS
from taf.config.testline.nom import NOM
from taf.config.testline.nms import Netact
from taf.config.testline.attenuator import HBTE, TopYoung
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit

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
        addr="10.108.229.98", username="ute", password="QAZqaz123!@#"
    )
)

# ######## start of vCU ##########################################################
# VCU related NCIR controlNode
_control = ControlNode(
    # Configuration for SSH access
    default_ssh_connection_details=SshServiceDetails(
        addr="10.70.32.50", username="cranuser6", password="systeM!23"
    ),
    # Configuration for openstack connection
    open_stack_connection_details=OpenStackConnectionDetails(
        username="cranuser6",
        password="systeM!23",
        ip_addr="10.70.32.50",
        tenant="cran6",
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
    name="aic-vcu",
    yaml_file=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/aic_vdu_values_override_0.yaml"
    ),
)


# ssh connection information of OE, for tenant user
_vcu_ssh_connection_details = SshServiceDetails(
    addr="10.70.32.50", username="cranuser6", password="systeM!23"
)
# ssh connection information of OE, for root user
_vcu_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.70.32.50", username="core", password="system123", port="22"
)

_vcu_master_node = MasterNode(
    k8s_connection_details=_vcu_k8s_connection_details,
    ssh_connection_details=_vcu_ssh_connection_details,
)

_vcu_k8s = K8S(namespace="cran6", master_node=_vcu_master_node)


_vcu_k8s_cloud_deployment = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    networks=[_vcu_intnet_1],
    vnfs=[_vcu_vnf_1],
    cloud_hosting=_vcu_k8s,
)
# #################### End of VCU CNF platform ##########################

# CU configuration
_cu = CU(
    # CU web UI ip address, oam interface ip of oam vm
    backhaul_site_oam_ip=NetworkAddress(
        #v4="10.110.93.31"
         v6='2a00:8a00:8000:117:1:29:a47:e1a9'
    ),
    # VCU OAM ssh connection, oam interface ip of oam vm
    oam_ssh_connection_details=SshServiceDetails(
        addr="2a00:8a00:8000:117:1:29:a47:e1a9",
        username="serviceuser",
        password="Pl(FzaYj5~c5;q",
    ),
    # VCU OAM http connection, oam interface ip of oam vm
    oam_http_connection_details=HttpConnectionDetails(
        addr="2a00:8a00:8000:117:1:29:a47:e1a9",
        username="Nemuadmin",
        password="nemuuser",
        port="443",
    ),
    # route configuration for x2 link to ENB, v4 is network address of ENB x2 link
    # route configuration for f1c link to VDU on VCU, v4 is network address of VDU f1c link
    f1c=NetworkAddress(
        v6="2a00:8a00:8000:117:1:29:a47:e220",
        routing=RoutingInformation(gateway="2a00:8a00:8000:117:1:29:a47:e221", ip_prefix_length=123),
    ),
    # route configuration for f1u link to VDU on VCU, v4 is network address of VDU f1u link
    f1u=NetworkAddress(
        v6="2a00:8a00:8000:117:1:29:a47:bdc0",
        routing=RoutingInformation(
            gateway="2a00:8a00:8000:117:1:29:a47:bdc1", ip_prefix_length=122
        ),
    ),
    # route configuration for x2 link to ENB on VCU, v4 is network address of ENB x2 link
    ngc=NetworkAddress(
        v6="2a00:8a00:8000:117:1:29:a47:e1e0",
        routing=RoutingInformation(gateway="2a00:8a00:8000:117:1:29:a47:e1e1", ip_prefix_length=123),
    ),
    ngu=NetworkAddress(
        v6="2a00:8a00:8000:117:1:29:a47:e140",
        routing=RoutingInformation(gateway="2a00:8a00:8000:117:1:29:a47:e141", ip_prefix_length=122),
    ),
    tracing=None,
    global_bts_id=108852,
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

_real_enb = RealEnb(airscale=_airscale, oam_ip="10.97.120.141")

# you can configure it as AIC UTE environment
_enb_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.108.229.98", username="ute", password="QAZqaz123!@#"
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

_ssh_connection_details_0 = SshServiceDetails(
    addr="2a00:8a00:8000:117:1:2:a47:b132", username="cranuser1", password="systeM!23"
)

# ip_addr="10.97.119.62", username="core", password="system123", port="22"
_k8s_connection_details_0 = K8SConnectionDetails(
    ip_addr="2a00:8a00:8000:117:1:2:a47:b132", username="core", password="system123", port="22"
)

_master_node_0 = MasterNode(
    k8s_connection_details=_k8s_connection_details_0,
    ssh_connection_details=_ssh_connection_details_0,
)
_k8s_0 = K8S(namespace="cran1", master_node=_master_node_0)


_vdu_oam_http_connection_details = HttpConnectionDetails(
    addr="2a00:8a00:8000:117:1:2:a47:b112",
    port="443",
    username="Nemuadmin",
    password="nemuuser",
)

_k8s_cloud_deployment_0 = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    networks=[_vdu_intnet_0],
    vnfs=[_vdu_vnf_0],
    cloud_hosting=_k8s_0,
)

# RU PDU
# _ru_pdu = PBHBTE(addr="10.97.122.137", port_numbers=[3])
# _ru_pdu = TP(addr="10.56.99.8", port_numbers=[1, 2, 3])
#_ru_pdu = TP(addr="10.97.126.240", port_numbers=[5])

# RU configuration
# for cell 1,2,3 (PC 10.56.99.16)
_hbte_params = {
    "ip_addr": "10.97.120.231",
    "port": 23,
    "attenuation_port_numbers": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    "model": "PA-16-8-4-127-0.5-B-S",
    "version": None,
}

_attenuator_5G = TopYoung(**_hbte_params)


# RU configuration

_ru_1 = RU(
    ru_hw_group="RU_INT_CPRI",
    radio_type="AEQP",
    serial_number="1M213504197",
    attenuation_ports=[
        _attenuator_5G.attenuator_ports[5],
        _attenuator_5G.attenuator_ports[6],
        _attenuator_5G.attenuator_ports[7],
        _attenuator_5G.attenuator_ports[8],
    ],
    #    pdu_port=_ru_pdu.pdu_ports[2],
    #pdu_port=_ru_pdu.pdu_ports[5],
)
_ru_2 = RU(
    ru_hw_group="RU_INT_CPRI",
    radio_type="AEQY",
    serial_number="1M212037559",
    attenuation_ports=[
        _attenuator_5G.attenuator_ports[13],
        _attenuator_5G.attenuator_ports[14],
        _attenuator_5G.attenuator_ports[15],
        _attenuator_5G.attenuator_ports[16],
    ],
    #    pdu_port=_ru_pdu.pdu_ports[1],
    # pdu_port=_ru_pdu.pdu_ports[5],
)


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
    rus=[_ru_1, _ru_2],
    pxe_server=_pxe_server,
    fhgw_id=11235,
)
_fhgw_0.ssh_username = "root"
_fhgw_0.ssh_password = "Fhgw@nokia123!"

_vdu_0 = VDU(
    cloud_deployment=_k8s_cloud_deployment_0,
    oam_http_connection_details=_vdu_oam_http_connection_details,
    fhgws=[_fhgw_0],
    # route configuration of f1m link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_m_ip_addr=NetworkAddress(
        v4="10.97.79.0",
        vlan_id=None,
        routing=RoutingInformation(
            gateway="10.71.177.9", ip_prefix_length=24
        ),
    ),
    # route configuration of f1c link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_c_ip_addr=NetworkAddress(
        v6="2a00:8a00:8000:117:1:2:a47:b108",
        vlan_id=None,
        routing=RoutingInformation(
            gateway="2a00:8a00:8000:117:1:2:a47:b109", ip_prefix_length=125
        ),
    ),
    # route configuration of f1u link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_u_ip_addr=NetworkAddress(
        v6="2a00:8a00:8000:117:1:2:a47:b108",
        vlan_id=None,
        routing=RoutingInformation(
            gateway="2a00:8a00:8000:117:1:2:a47:b109", ip_prefix_length=125
        ),
    ),
    instance_id=108851,
)


# ######## start of NOM ######################################################
_nom_ssh_connection_edge0 = SshServiceDetails(
    addr="10.39.156.122", username="cloud-user"
)

_nom1 = NOM(
    ssh_connections_info=[_nom_ssh_connection_edge0],
    https_main_info=HttpConnectionDetails(
        addr="https://neo-hosting-page.srncnms04.srnblr.nsn-rdnet.net/",
        username="cnms04",
        password="Qwer_1234",
    ),
    https_user_mgmt_info=HttpConnectionDetails(
        addr="https://user-mgmt.srncnms04.srnblr.nsn-rdnet.net"
    ),
    https_rest_info=HttpConnectionDetails(
        addr="https://apigw.srncnms04.srnblr.nsn-rdnet.net"
    ),
    neo_endpoints_ip="10.39.156.88",
)
_cnms = NMS(addr="10.39.156.122", nom=_nom1)

# ######## start of Netact ######################################################
netact_id = {
    "clab3766": {
        "node_ip": "10.32.217.23",
        "user": "omc",
        "password": "omc",
        "url": "https://clab3766lbwas.netact.nsn-rdnet.net",
        "url_user": "omc",
        "url_password": "omc",
        "mr": "MRC-VRAN2.0/MR-10885",
    },
    "clab3386": {
        "node_ip": "10.32.217.141",
        "user": "omc",
        "password": "omc",
        "url": "https://clab3386lbwas.netact.nsn-rdnet.net",
        "url_user": "omc",
        "url_password": "omc",
        "mr": "MRC-1/MR-1",
    },
}

_netact = Netact(netact_id)

# vcu CNF: _vcu_k8s_cloud_deployment
_cbts = CloudBts(
    dus=[_vdu_0],
    cu=_cu,
    cloud_deployment=_vcu_k8s_cloud_deployment,
    vnf_name="hgz-108852",
    instance_id="108852",
    global_bts_id="108852",
)



#  UE
_appserver_ssh = SshServiceDetails(
    addr="10.108.229.98", username="ute", password="QAZqaz123!@#"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh, network_interface_name="rmnet_data0"
)

_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.97.120.234", username="aic", password="Nokia123!"
    ),
    serial_number="R5CRA0HMS4R",  # R5CR924FQRH RFCTB15HKAM
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "samsung"],
 #   service_call_attach=17,
 #   service_call_detach=17,
)


_tools_repository = {
    "ip": "10.108.229.152",
    "username": "ute",
    "password": "QAZqaz123@#",
    "repo_tool_folder": "/opt/tools/trans_test/",
    "repo_data_folder": "/opt/tools/trans_data/",
    "testline_extra_config": "/opt/testline_config/",
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


# Testline configuration, tl is only variable which can be accessed by agent and test case
# you can access all parameters configured upper by tl parameter
# CNUMS: nms=_cnms,
# Netact: nms=_netact
tl = TestLine(
    test_pc=_test_pc,
    attenuators=[_attenuator_5G],
    nms=_netact,
    ues=[_android],
    gnbs=[_cbts],
    enbs=[_real_enb],
    tl_cloud_topology="CLOUD_5G_AIC_OCP_UE_SA_1xvDU__OE22_FHGW_AZQJ",
    test_pcs=[_enb_test_pc],
    core=_realcore,
)
_misc = {
    # 1-Use Netact config in __init__.py, 0-Use Netact config in global_variable.py.
    # If this key is not given, default value is 1
    "netact_config_source_from_init_py": "0",
    
    #give netact group name, e.g, AIC_TRUNK_TEST, AIC_BRANCH_TEST, AIC_CDRT_TEST, or AIC_NETACT_FP_TEST
    #or give specific netact server name, e.g, clabChen4, clab2003, clab2002, clab1060, clab1013 or clab1057, etc.
    #if this value is not given, the candidates will be all netact server 
    "netact_server": "AIC_TRUNK_TEST",
    
    # 1-knife image will be made, knife files are given in _tools_repository.testline_extra_config folder 
    # 0-knife image will not be made
    # If this key is not given, default value is 0
    "knife": "1",    
}
tl._misc = _misc

_ru_direct_connection = {
    # 1- direct_connection(DC), 0-not direct_connection.
    # If this key is not given, default value is 0
    "ru_direct_connection": "0",
}
tl._ru_direct_connection = _ru_direct_connection


# it's a WA, please see https://jira3.int.net.nokia.com/browse/TALIB-846,
# this jira has blocked a few transport TA cases design and debug
# one of other WA is declare a global python variable, 'TRANS_PARA = _trans_para'
# i don't know which WA is better, please give me suggestion if you like to change WA.
tl._trans_para = _trans_para

__all__ = ["tl"]
