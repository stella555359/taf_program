#This is using 10788 jenkins testline ,but using 11135CU and 11133DU info
__maintainer__ = "xxx"
__team__ = "OO_NSB_MN_RAN_RD_VRF_HAZ2_1_52491171_GMS"
__email__ = "oo_nsb_mn_ran_rd_vrf_haz2_1_52491171@internal.nsn.com"
__owner_email__ = "jane.wang@nokia_sbell.com"

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
from taf.config.testline import (
    RealEnb,
    NetworkAddress,
    RoutingInformation,
    Airscale,
    CommonUnit,
    CapacityUnit,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline import RealEnb, NetworkAddress, RoutingInformation
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU
from taf.config.testline import DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC
from taf.config.testline.pdu import TopYoung as TP
from taf.config.testline.lab_infrastructure import PxeServer
from taf.config.testline.core import RealCore
from taf.config.testline.connection_details import K8SConnectionDetails
from taf.config.testline.gnb.du import FHGW
from taf.config.testline.gnb.du import VDU
from taf.config.testline.cloud_hosting import MasterNode, K8S
from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.config.testline.radio import RU
from taf.config.testline.nms import NMS
from taf.config.testline.nom import NOM
from taf.config.testline.attenuator import HBTE, TopYoung
from taf.config.testline.ue import Android, Qualcomm
from taf.config.testline.radio import RU
from taf.config.testline.nms import Netact
from taf.config.testline.cloud_hosting import MasterNode, K8S, HelmChart

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

# this is test PC for AIC, including UTE IP address, User Name and Password.
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.108.229.125", username="ute", password="QAZqaz123!@#"
    )
)

# ######## start of vCU ##########################################################
# NCIR
_control = ControlNode(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.107.123.134", username="core", password="system123"
    ),
    open_stack_connection_details=OpenStackConnectionDetails(
        username="core",
        password="system123",
        ip_addr="10.107.123.134",
        tenant="cran3",
    ),
    bmc_connection_details=BmcConnectionDetails(addr="", username="", password=""),
)

_ncir = NCIR(compute_nodes=[], control_nodes=[_control], version="ncir_19")

_cu = CU(
    # CU web UI ip address, oam interface ip of oam vm
    # backhaul_site_oam_ip=NetworkAddress(v4="10.107.138.103"),
    backhaul_site_oam_ip=NetworkAddress(v4="10.110.179.200"),
    # VCU OAM ssh connection, oam interface ip of oam vm
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.107.105.182",
        username="cranuser3",
        password="systeM!23",
    ),
    # VCU OAM http connection, oam interface ip of oam vm
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.107.105.182",
        username="Nemuadmin",
        password="nemuuser",
        port="443",
    ),
    # route configuration for x2 link to ENB, v4 is network address of ENB x2 link
    x2c=NetworkAddress(
        v4="10.110.179.134",
        routing=RoutingInformation(gateway="10.110.179.129", ip_prefix_length=26),
     ),
    # route configuration for f1c link to VDU on VCU, v4 is network address of VDU f1c link
    f1c=NetworkAddress(
        v4="10.107.105.232",
        routing=RoutingInformation(gateway="10.110.74.1", ip_prefix_length=29),
    ),
    # route configuration for f1u link to VDU on VCU, v4 is network address of VDU f1u link
    f1u=NetworkAddress(
        v4="10.107.152.8",
        routing=RoutingInformation(gateway="10.110.74.129", ip_prefix_length=25),
    ),
    s1u=NetworkAddress(
        v4="10.110.179.8",
        routing=RoutingInformation(gateway="10.110.179.1", ip_prefix_length=25),
    ),
    tracing=None,
    global_bts_id=11135,
)

# ######## start of vDU ######################################################
# VDU deployment

_vdu_vnf_1 = DeploymentVnfStack(
    name="aic-vdu",
    yaml_file=os.path.join(
        _cfg_dir,
        "DEP_SCF_FILES/CU_0/vDU_0/cnf_parameters.yaml",
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
    addr="10.69.13.210", username="cranuser1", password="systeM!23"
)
_k8s_connection_details_0 = K8SConnectionDetails(
    ip_addr="10.69.13.210",
    username="core",
    password="system123",
    port="22",
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
    addr="10.69.33.82",
    port="443",
    username="Nemuadmin",
    password="nemuuser",
)

# PA configuration
_hbte_params_1 = {
    "ip_addr": "10.97.126.236",
    "port": 5000,
    "attenuation_port_numbers": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    "model": "PA-16-8-4-127-0.5-B-S",
    "version": None,
}


_attenuator_5G_1 = HBTE(**_hbte_params_1)


# RU configuration
_ru_1 = RU(
    ru_hw_group="RU_INT_ECPRI",
    serial_number="K9220312566",
    attenuation_ports=[
        _attenuator_5G_1.attenuator_ports[5],
        _attenuator_5G_1.attenuator_ports[6],
        _attenuator_5G_1.attenuator_ports[7],
        _attenuator_5G_1.attenuator_ports[8],
    ],
#    pdu_port=_ru_pdu_1.pdu_ports[1]
)

# PXE server info for FHGW deployment
_pxe_server_ssh_info = SshServiceDetails(
    addr="10.69.38.28", username="root", password="pxe@systeM!23"
)
_pxe_server = PxeServer(
    nfs_ip="10.69.38.28", ssh_connection_details=_pxe_server_ssh_info
)

# FHGW information
_fhgw_0 = FHGW(
    user_config_path=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/FHGW_0/fhgw_user_config_3.yaml"
    ),
    rus=[_ru_1],
    pxe_server=_pxe_server,
)
_fhgw_0.ssh_username = "root"
_fhgw_0.ssh_password = "root"

# VDU global configuration
_vdu_0 = VDU(
    cloud_deployment=_k8s_cloud_deployment_0,
    oam_http_connection_details=_vdu_oam_http_connection_details,
    fhgws=[_fhgw_0],
    # route configuration of f1c link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_c_ip_addr=NetworkAddress(
        v4="10.69.13.234",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.69.13.233", ip_prefix_length=29),
    ),
    # route configuration of f1u link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_u_ip_addr=NetworkAddress(
        v4="10.69.13.235",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.69.13.233", ip_prefix_length=29),
    ),
    instance_id=11136,
    global_bts_id=11135,
)

#####################################


# AppServer info iperf used
_app_server_1 = TafUeAppServer(app_server_name="APP_1",
                               address="10.108.229.125",
                               user="ute",
                               password="QAZqaz123!@#",
                               )

_data_transfer_iperf = TafUeDataTransferProtocol(protocol_name='iperf',
                                                 app_server=_app_server_1,
                                                 interval=1,
                                                 interface_name='rmnet_data0',
                                                 server_close_delay=50,
                                                 version=2)

_pdn1 = PDNTafUeAndroidDetails(entryName='stdata2',
                               apnName='stdata2',
                               apnType=['DEFAULT'])


# UE info
_android_1 = TafUeAndroid(serial_number='R5CR41CVSPB',
                          capabilities=['REAL_UE'],
                          ue_pc_address='10.56.99.23',
                          data_transfer=[_data_transfer_iperf],
                          ssh_connection_details=SshServiceDetails(addr='10.56.99.23',
                                                                   username='aic',
                                                                   password='Nokia123!'),
                          ue_pc_port='8080',
                          pdns=[_pdn1],
#                          service_call_attach='17',
#                          service_call_detach='17',
                          )




#####################################


# ######## start of NOM ######################################################
_nom_ssh_connection_edge0 = SshServiceDetails(
    addr="10.27.137.179", username="cloud-user"
)

_nom1 = NOM(
    ssh_connections_info=[_nom_ssh_connection_edge0],
    https_main_info=HttpConnectionDetails(
        addr="https://neo-hosting-page.srncnms13.srnblr.nsn-rdnet.net/",
        username="neonetics",
        password="Nokia123@",
    ),
    https_user_mgmt_info=HttpConnectionDetails(
        addr="https://user-mgmt.srncnms13.srnblr.nsn-rdnet.net",
    ),
    https_rest_info=HttpConnectionDetails(
        addr="https://apigw.srncnms13.srnblr.nsn-rdnet.net",
    ),
    neo_endpoints_ip="10.27.137.181",
)

_cnms = NMS(addr="10.27.137.179", nom=_nom1)

_vcu_intnet_1 = DeploymentNetworkStack(
    name="aic-vcu-pre",
    yaml_file=os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/values-override-pre.yaml"),
)

_vcu_vnf_1 = DeploymentVnfStack(
    name="aic-vcu-cnf",
    yaml_file=os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/values-override-vcu.yaml"),
)


# ssh connection information of OE, for tenant user
_vcu_ssh_connection_details = SshServiceDetails(
    addr="10.107.123.134",
    username="cranuser3",
    password="systeM!23",
)
# ssh connection information of OE, for root user
_vcu_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.107.123.134",
    username="core",
    password="system123",
    port="22",
)

_vcu_master_node = MasterNode(
    k8s_connection_details=_vcu_k8s_connection_details,
    ssh_connection_details=_vcu_ssh_connection_details,
)

_vcu_k8s = K8S(namespace="cran3", master_node=_vcu_master_node)
_vcu_k8s_cloud_deployment = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    networks=[_vcu_intnet_1],
    vnfs=[_vcu_vnf_1],
    cloud_hosting=_vcu_k8s,
)


# VCU global configuration
_cbts = CloudBts(
    dus=[_vdu_0],
    cu=_cu,
    cloud_deployment=_vcu_k8s_cloud_deployment,
    instance_id="11133",
    global_bts_id="11133",
)

_tools_repository = {
    "ip": "10.108.229.101",
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
    attenuators=[_attenuator_5G_1],
    gnbs=[_cbts],
    enbs=[],
    tl_cloud_topology="CLOUD_5G_CR_TL_3_DRAN_SNO_AEHC_3xCell_SA_TDD_Android",
    cloud_hostings=[_ncir],
    ues=[_android_1],

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


__all__ = ["tl"]
