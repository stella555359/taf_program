__maintainer__ = "Xu Huilin"
__team__ = "I_NSB_MN_5GSC_5GSW_ENG_AIC_SI_CN_2SISO_GMS <I_NSB_MN_5GSC_5GSW_ENG_AIC_SI_CN_2SISO@internal.nsn.com>"
__email__ = "I_NSB_MN_5GSC_5GSW_ENG_AIC_SI_CN_2SISO@internal.nsn.com"
__owner_email__ = "huilin.xu@nokia-sbell.com"

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
from taf.config.testline.cloud_hosting import MasterNode, K8S, ComputeNode
from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.config.testline.gnb.networkaddress import RoutingInformation
from taf.config.testline.radio import RU
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.nms import NMS
from taf.config.testline.nom import NOM
from taf.config.testline.nms import Netact
from taf.config.testline.attenuator import HBTE, TopYoung
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit

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
        addr="10.108.229.71", username="ute", password="QAZqaz123!@#"
    )
)

# enb
_hbte_params_4 = {
    "ip_addr": "10.97.120.131",
    "port": 5000,
    "attenuation_port_numbers": [4],
    "model": "PA-8-8-4-127-0.5-B-S",
    "version": None,
}
_attenuator_4G = HBTE(**_hbte_params_4)
_ru_4 = RU(
    ru_hw_group="hw_group",
    attenuation_ports=[
        _attenuator_4G.attenuator_ports[4],
    ],
)
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
    addr="2a00:8a00:8000:5002:0:17:0:902", username="cranuser4", password="systeM!23"
)
# ssh connection information of OE, for root user
_vcu_k8s_connection_details = K8SConnectionDetails(
    ip_addr="2a00:8a00:8000:5002:0:17:0:902",
    username="core",
    password="system123",
    port="22",
)

_vcu_master_node = MasterNode(
    k8s_connection_details=_vcu_k8s_connection_details,
    ssh_connection_details=_vcu_ssh_connection_details,
)

_vcu_k8s = K8S(namespace="cran4", master_node=_vcu_master_node)

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
    backhaul_site_oam_ip=NetworkAddress(v6="2a00:8a00:8000:5002:0:17:0000:0707"),
    # VCU OAM ssh connection, oam interface ip of oam vm
    oam_ssh_connection_details=SshServiceDetails(
        addr="2a00:8a00:8000:5002:0:17:0000:0707",
        username="serviceuser",
        password="Pl(FzaYj5~c5;q",
    ),
    # VCU OAM http connection, oam interface ip of oam vm
    oam_http_connection_details=HttpConnectionDetails(
        addr="2a00:8a00:8000:5002:0:17:0000:0707",
        username="Nemuadmin",
        password="nemuuser",
        port="443",
    ),
    s1u=NetworkAddress(
        v6="::",
        vlan_id=None,
        routing=RoutingInformation(
            gateway="2a00:8a00:8000:5002:0:17:0000:0601", ip_prefix_length=120
        ),
    ),
    # route configuration for x2 link to ENB, v4 is network address of ENB x2 link
    x2c=NetworkAddress(
        v6="::",
        vlan_id=None,
        routing=RoutingInformation(
            gateway="2a00:8a00:8000:5002:0:17:0000:0401", ip_prefix_length=120
        ),
    ),
    # route configuration for x2 link to ENB on VCU, v4 is network address of ENB x2 link
    f1c=NetworkAddress(
        v6="2a00:8a00:8000:5002:0:17:0000:0207",
        vlan_id=None,
        routing=RoutingInformation(
            gateway="2a00:8a00:8000:5002:0:17:0000:0201", ip_prefix_length=120
        ),
    ),
    # route configuration for f1u link to VDU on VCU, v4 is network address of VDU f1u link
    f1u=NetworkAddress(
        v6="2a00:8a00:8000:5002:0:17:0000:0307",
        vlan_id=None,
        routing=RoutingInformation(
            gateway="2a00:8a00:8000:5002:0:17:0000:0301", ip_prefix_length=120
        ),
    ),
    ngc=NetworkAddress(
        v6="2a00:8a00:8000:5002:0:17:0000:0807",
        routing=RoutingInformation(
            gateway="2a00:8a00:8000:5002:0:17:0000:0801", ip_prefix_length=120
        ),
    ),
    ngu=NetworkAddress(
        v6="2a00:8a00:8000:5002:0:17:0000:0c07",
        routing=RoutingInformation(
            gateway="2a00:8a00:8000:5002:0:17:0000:0c01", ip_prefix_length=120
        ),
    ),
    tracing=None,
    global_bts_id=5228,
)

# mcc, mnc configuration
_realcore = RealCore(five_g=None, mcc="262", mnc="03", pdns=None)


# ######## start of ENB #############################
_capacity_unit = CapacityUnit(addr="6.6.6.6")

_common_unit = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.97.122.172", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_capacity_unit],
)

_airscale = Airscale(common_units=[_common_unit])

_real_enb = RealEnb(airscale=_airscale, oam_ip="10.97.122.172", rms=[_ru_4])

# test pc information of enb
_enb_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.108.229.51", username="ute", password="QAZqaz123!@#"
    ),
    connections=[_real_enb],
)
# ######## start of vDU ######################################################
# VDU deployment
_vdu_vnf_1 = DeploymentVnfStack(
    # this is vdu release name, the name should only be lower case and only can include alphabet, number,
    name="aic-vdu",
    yaml_file=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/one_click_ne_deploy.yaml"
    ),
)

_vdu_intnet_1 = DeploymentNetworkStack(
    # this is intnet release name, the name should only be lower case and only can include alphabet, number,
    name="aic-intnet",
    yaml_file=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/aic_intnet_values_override_0.yaml"
    ),
)

_ssh_connection_details_1 = SshServiceDetails(
    addr="2a00:8a00:8000:117:1:2:a47:b822", username="cranuser1", password="systeM!23"
)
# ssh connection information of OE, for cloudadmin user
_k8s_connection_details_1 = K8SConnectionDetails(
    ip_addr="2a00:8a00:8000:117:1:2:a47:b822",
    username="core",
    password="system123",
    port="22",
)

_master_node_1 = MasterNode(
    k8s_connection_details=_k8s_connection_details_1,
    ssh_connection_details=_ssh_connection_details_1,
)
_k8s_1 = K8S(namespace="cran1", master_node=_master_node_1)
_k8s_cloud_deployment_1 = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    networks=[_vdu_intnet_1],
    vnfs=[_vdu_vnf_1],
    cloud_hosting=_k8s_1,
)

# VDU oam http connection
_vdu_oam_http_connection_details = HttpConnectionDetails(
    addr="2a00:8a00:8000:117:1:2:a47:b812",
    port="443",
    username="Nemuadmin",
    password="nemuuser",
)
# RU configuration
_hbte_params_1 = {
    "ip_addr": "10.97.120.131",
    "port": 5000,
    "attenuation_port_numbers": [1, 2, 3],
    "model": "PA-8-8-4-127-0.5-B-S",
    "version": None,
}
_attenuator_5G_1 = HBTE(**_hbte_params_1)

# RU configuration
_ru_1 = RU(
    ru_hw_group="RU_INT_ECPRI",
    serial_number="1M213303651",
    attenuation_ports=[
        _attenuator_5G_1.attenuator_ports[1],
        _attenuator_5G_1.attenuator_ports[2],
        _attenuator_5G_1.attenuator_ports[3],
    ],
)

_hbte_params_2 = {
    "ip_addr": "10.97.120.183",
    "port": 5000,
    "attenuation_port_numbers": [1, 2],
    "model": "PA-8-8-4-127-0.5-B-S",
    "version": None,
}
_attenuator_5G_2 = HBTE(**_hbte_params_2)

_ru_2 = RU(
    ru_hw_group="RU_INT_CPRI",
    serial_number="1M231011386",
    attenuation_ports=[
        _attenuator_5G_2.attenuator_ports[1],
        _attenuator_5G_2.attenuator_ports[2],
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
_fhgw_1 = FHGW(
    user_config_path=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/FHGW_0/fhgw_user_config_0.yaml"
    ),
    rus=[_ru_1, _ru_2],
    pxe_server=_pxe_server,
    fhgw_id=5228,
)

# VDU global configuration
_vdu_1 = VDU(
    cloud_deployment=_k8s_cloud_deployment_1,
    oam_http_connection_details=_vdu_oam_http_connection_details,
    fhgws=[_fhgw_1],
    # route configuration of f1m link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_m_ip_addr=NetworkAddress(
        v6="2a00:8a00:8000:117:1:2:a47:b80a",
        vlan_id=None,
        routing=RoutingInformation(
            gateway="2a00:8a00:8000:117:1:2:a47:b809", ip_prefix_length=125
        ),
    ),
    # route configuration of f1c link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_c_ip_addr=NetworkAddress(
        v6="2a00:8a00:8000:117:1:2:a47:b80a",
        vlan_id=None,
        routing=RoutingInformation(
            gateway="2a00:8a00:8000:117:1:2:a47:b809", ip_prefix_length=125
        ),
    ),
    # route configuration of f1u link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_u_ip_addr=NetworkAddress(
        v6="2a00:8a00:8000:117:1:2:a47:b80b",
        vlan_id=None,
        routing=RoutingInformation(
            gateway="2a00:8a00:8000:117:1:2:a47:b809", ip_prefix_length=125
        ),
    ),
    instance_id=5228,
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
        password="Qwer_123456",
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

netact_id = {
    "clab3766": {
        "node_ip": "10.32.217.23",
        "user": "omc",
        "password": "omc",
        "url": "https://clab3766lbwas.netact.nsn-rdnet.net",
        "url_user": "omc",
        "url_password": "omc",
        "mr": "MRC-5G22R1VDU/MR-5228",
        "ca_file": "nom/clab3766ca.pem",
        "ca_sn": "0x45BFB1864E379F8CA2FC4184ADC55AF31DA5857C",
        "ca_id": "CACERT_R1",
    },
    "clab3386": {
        "node_ip": "10.32.217.141",
        "user": "omc",
        "password": "omc",
        "url": "https://clab3386lbwas.netact.nsn-rdnet.net",
        "url_user": "omc",
        "url_password": "omc",
        "mr": "MRC-5G22R1VDU/MR-5228",
    },
}
_netact = Netact(netact_id)

_cbts = CloudBts(
    dus=[_vdu_1],  # vdu related parameter
    cu=_cu,
    cloud_deployment=_vcu_k8s_cloud_deployment,
    instance_id="5228",
    global_bts_id="5228",
)
_tools_repository = {
    "ip": "10.108.229.152",
    "username": "ute",
    "password": "QAZqaz123!@#",
    "repo_tool_folder": "/opt/tools/trans_test/",
    "repo_data_folder": "/opt/tools/trans_data/",
    "testline_extra_config": "/opt/testline_config/",
}

_switch_1 = {
    "du_switch_ip": "10.108.212.106",
    "username": "chriscd",
    "password": "12345678",
    "en_password": "",
    "port": "23",
    "switch_interface": "1/1/1",
    "simu4DU_interface": "",
    "acl_number": "188",
    "du_vlan_id": "20",
    "du_vlan_masklen": "27",
    "du_vlan_gateway": "10.108.227.129",
    "du_vlan_mtu": "1500",
    "du_2nd_vlan_id": "100",
    "du_2nd_vlan_masklen": "27",
    "du_2nd_vlan_gateway": "10.108.227.192",
    "du_2nd_vlan_mtu": "1500",
    "du_2nd_vlan_ip": "10.108.227.220",
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

# AppServer info
_app_server_1 = TafUeAppServer(
    app_server_name="APP_1",
    address="10.108.229.71",
    user="ute",
    password="QAZqaz123!@#",
)

_data_transfer_iperf = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_app_server_1,
    interval=1,
    # binary_path="/data/data/com.nokia.android.application/",
    interface_name="rmnet_data0",
    # bind_ue_ip=False,
    server_close_delay=50,
    version=3,
)

_pdn1 = PDNTafUeAndroidDetails(
    entryName="stdata2", apnName="stdata2", apnType=["DEFAULT"]
)

# UE info
_android_1 = TafUeAndroid(
    serial_number="R3CW10X08QJ",
    capabilities=["REAL_UE"],
    ue_pc_address="10.97.120.130",
    data_transfer=[_data_transfer_iperf],
    ssh_connection_details=SshServiceDetails(
        addr="10.97.120.130", username="aic", password="Nokia123!"
    ),
    # phone_number="+358480500013",
    ue_pc_port="8080",
    # imei="12345678912345",
    # imsi="260123456789",
    pdns=[_pdn1],
    # qualcomm_prototype=True,
    service_call_attach="17",
    service_call_detach="17",
    # network_mode_switch_method="ADB",
    # airplane_mode_switcher_text="Airplane",
    # airplane_mode_confirm_button_text="OK",
    # path_to_network_mode_type="Mobile networks/Preferred network type",
    # secret_code="*#0808#*",
    # is_rooted="no",
)


# Testline configuration
tl = TestLine(
    test_pc=_test_pc,
    ues=[_android_1],
    attenuators=[_attenuator_5G_1, _attenuator_5G_2, _attenuator_4G],
    gnbs=[_cbts],
    enbs=[_real_enb],
    tl_cloud_topology="DRAN_SNO_3xRU_SA_TDD_Android",
    test_pcs=[_enb_test_pc],
    core=_realcore,
    nms=_netact,
)

_misc = {
    # 1-Use Netact config in __init__.py, 0-Use Netact config in global_variable.py.
    # If this key is not given, default value is 1
    "netact_config_source_from_init_py": "0",
 
    # 1-knife image will be made, knife files are given in _tools_repository.testline_extra_config folder 
    # 0-knife image will not be made
    # If this key is not given, default value is 0
    "knife": "1",
}

tl._misc = _misc

# only tl variable can be accessed by user
tl._trans_para = _trans_para
__all__ = ["tl"]
