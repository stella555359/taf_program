__maintainer__ = "Yu Mengtian"
__team__ = "I_SG1_ATOM_SQUAD@internal.nsn.com"
__email__ = "I_SG1_ATOM_SQUAD@internal.nsn.com"
__owner_email__ = "mengtian.yu@nokia-sbell.com"

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
from taf.config.testline.cloud_hosting import MasterNode, K8S
from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.config.testline.radio import RU
from taf.config.testline.nms import NMS
from taf.config.testline.nom import NOM
from taf.config.testline.attenuator import HBTE
from taf.config.testline.ue import Android
from taf.config.testline.radio import RU
from taf.config.testline.nms import Netact

# Following mandatory files and parameters should be configured
# Please don't ignore any parameters, you can add, but don't ingore
# Any problem, please check with CI team

#####  FOLLOWING ARE CHECKLIST OF TESTLINE CONFIGURATION #######

#  1. 5gbts_ext_net.env have been configured as following
#  2. 5gbts_flavor.env have been configured as following
#  3. 5gbts_heat.env have been configured as following
#  4. aic-intnet-values-override_${vdu_index}.yaml (vdu_index should start from 0) have been configured as following
#  5. aic-vdu-values-override_${vdu_index}.yaml (vdu_index should start from 0) have been configured as following
#  6. user_config_${fhgw_index}.yaml (fhgw_index should start from 0) have been configured as following (currently, it's not used)
#  7. "vnf_prefix" in 5gbts_flavor.env should be re-configued, don't use common flavor name
#  8. vnf_prefix naming rule should be flavor-<testline name>, e.g: flavor-7_5_UTE5GAIC001T037
#  9. "flavors" in 5gbts_heat.env should be configured and prefix should equal to vnf_prefix value configured on 5gbts_flavor.env
#  10. please make sure 5gbts_ext_net.env, 5gbts_flavor.env, 5gbts_heat.env are new enough for next build
#  11. please make sure aic-intnet-values-override_x.yaml and aic-vdu-values-override_x.yaml are new enough for next build
#  12. please make sure files in step 1,2,3,4,5 have valid configuration
#  13. please make sure ip address of NCIR and test pc can be accessible by network
#  14. please make sure VDU on OE have been cleared or VDU helm release name is equal to name of DeploymentVnfStack before start agent_5g_aic
#  15. please make sure VCU on NCIR have been cleared or VCU stack name is TL_<testline name>_BTS before start agent_5g_aic
#  16. please check nom mo configured
#################################################################


_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# UTE IP address and User Name, Password,
# this is test PC for AIC
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.108.229.74", username="ute", password="QAZqaz123!@#"
    )
)

# VCU related OCP controlNode
_control = ControlNode(
    # Configuration for SSH access
    default_ssh_connection_details=SshServiceDetails(
        addr="10.110.18.226", username="cranuser4", password="systeM!23"
    ),
    # Configuration for openstack connection
    open_stack_connection_details=OpenStackConnectionDetails(
        username="cranuser4",
        password="systeM!23",
        ip_addr="10.110.18.226",
        tenant="cran4",
    ),
    # Configuration of BMC connection, if you need use it in test case, plase config it
    # currently, it's not used in agent
    bmc_connection_details=BmcConnectionDetails(addr="", username="", password=""),
)

# configuration of VCU related NCIR/OCP
_ncir = NCIR(compute_nodes=[], control_nodes=[_control], version="ncir_19")

# CU configuration
_cu = CU(
    # CU web UI ip address, oam interface ip of oam vm
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.110.179.199"
        # v6='2a00:8a00:8000:136:10:57:159:1111'
    ),
    # VCU OAM ssh connection, oam interface ip of oam vm
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.110.179.199", username="Nemuadmin", password="nemuuser"
    ),
    # VCU OAM http connection, oam interface ip of oam vm
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.110.179.199", username="Nemuadmin", password="nemuuser", port="443"
    ),
    # route configuration for x2 link to ENB, v4 is network address of ENB x2 link
    x2c=NetworkAddress(
        v4="10.110.179.128",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.110.179.129", ip_prefix_length=26),
    ),
    # route configuration for f1c link to VDU on VCU, v4 is network address of VDU f1c link
    f1c=NetworkAddress(
        v4="10.110.189.128",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.110.189.129", ip_prefix_length=26),
    ),
    # route configuration for f1u link to VDU on VCU, v4 is network address of VDU f1u link
    f1u=NetworkAddress(
        v4="10.110.178.0",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.110.178.1", ip_prefix_length=25),
    ),
    s1u=NetworkAddress(
        v4="10.110.179.0",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.110.179.1", ip_prefix_length=25),
    ),
    x2u=NetworkAddress(
        v4="10.110.178.128",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.110.178.129", ip_prefix_length=25),
    ),
    tracing=None,
)

# enb for NSA

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.108.213.4", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    # pdu_port=_real_enb_pdu.pdu_ports[2],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(
    airscale=_real_enb,
    oam_ip="10.108.213.4",
    instance_id="",
    global_bts_id="5254",
)

# test pc information of enb
# you can configure it as AIC UTE environment
_enb_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.108.229.74", username="ute", password="QAZqaz123!@#"
    ),
    connections=[_real_enb],
)

# VDU configuration for deployment
_vdu_vnf_0 = DeploymentVnfStack(
    name="vdu",  # this is vdu release name, the name should only be lower case and only can include alphabet, number, _
    yaml_file=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/aic_vdu_values_override_0.yaml"
    ),
)

# VDU internal network configuration for deployment
_vdu_intnet_0 = DeploymentNetworkStack(
    name="aic-intnet-mvp",  # this is intnet release name, the name should only be lower case and only can include alphabet, number, _
    yaml_file=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/aic_intnet_values_override_0.yaml"
    ),
)

# ssh connection information of OE, for tenant user
_ssh_connection_details = SshServiceDetails(
    addr="10.108.205.178", username="cranuser1", password="systeM!23"
)

# ssh connection information of OE, for cloudadmin user
_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.108.205.178", username="core", password="system123", port="22"
)

# master node information of OE
_master_node = MasterNode(
    k8s_connection_details=_k8s_connection_details,
    ssh_connection_details=_ssh_connection_details,
)

_k8s = K8S(namespace="cran1", master_node=_master_node)

# VDU deployment configuration
_k8s_cloud_deployment = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    networks=[_vdu_intnet_0],
    vnfs=[_vdu_vnf_0],
    cloud_hosting=_k8s,
)

# VDU oam http connection
_vdu_oam_http_connection_details = HttpConnectionDetails(
    addr="10.108.205.162", port="443", username="Nemuadmin", password="nemuuser"
)

# RU configuration

_hbte_params_1 = {
    "ip_addr": "10.97.126.232",
    "port": 5000,
    "attenuation_port_numbers": [1, 2, 3, 4, 5, 6, 7, 8],
    "model": "PA-16-8-4-127-0.5-B-S",
    "version": None,
}

_attenuator_5G_1 = HBTE(**_hbte_params_1)

# AHCA
_ru_1 = RU(
    ru_hw_group="RU_INT_ECPRI",
    serial_number="AS195112288",
    attenuation_ports=[
        _attenuator_5G_1.attenuator_ports[5],
        _attenuator_5G_1.attenuator_ports[6],
        _attenuator_5G_1.attenuator_ports[7],
        _attenuator_5G_1.attenuator_ports[8],
    ],
)

# PXE server info for FHGW deployment
_pxe_server_ssh_info = SshServiceDetails(
    addr="10.108.204.30", username="ute", password="Cdslabadmin@"
)
_pxe_server = PxeServer(
    nfs_ip="10.68.179.27", ssh_connection_details=_pxe_server_ssh_info
)

# FHGW information
_fhgw_0 = FHGW(
    user_config_path=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/FHGW_0/fhgw_user_config_0.yaml"
    ),
    rus=[_ru_1],
    pxe_server=_pxe_server,
)
_fhgw_0.ssh_username = "root"
_fhgw_0.ssh_password = "root"

# VDU global configuration
_vdu_0 = VDU(
    cloud_deployment=_k8s_cloud_deployment,
    oam_http_connection_details=_vdu_oam_http_connection_details,
    fhgws=[_fhgw_0],
    # route configuration of f1m link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_m_ip_addr=NetworkAddress(
        v4="192.168.252.0",
        vlan_id=None,
        routing=RoutingInformation(gateway="192.168.252.1", ip_prefix_length=30),
    ),
    # route configuration of f1c link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_c_ip_addr=NetworkAddress(
        v4="10.108.205.152",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.108.205.153", ip_prefix_length=29),
    ),
    # route configuration of f1u link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_u_ip_addr=NetworkAddress(
        v4="10.108.205.152",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.108.205.153", ip_prefix_length=29),
    ),
)

# mcc, mnc configuration
_realcore = RealCore(five_g=None, mcc="262", mnc="03", pdns=None)

# _appserver_ssh = SshServiceDetails(
#     addr="10.108.229.43", username="ute", password="Cdslabadmin@"
# )

_appserver_ssh = SshServiceDetails(
    addr="10.108.229.42", username="ute", password="Cdslabadmin@"
)

_iperf = IperfDataTransferDetails(
#    iperf_path="/usr/bin/iperf",
    ssh_connection_details=_appserver_ssh,
    network_interface_name="rmnet_data0",
)


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
    addr="10.110.18.226", username="cranuser4", password="systeM!23"
)
# ssh connection information of OE, for root user
_vcu_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.110.18.226", username="core", password="system123", port="22"
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


# VCU global configuration
_cbts_0 = CloudBts(
    dus=[_vdu_0],  # vdu related parameter
    cu=_cu,
    cloud_deployment=_vcu_k8s_cloud_deployment,
    instance_id="11485",
    global_bts_id="11485",
)

netact_id = {
    "clab3766": {
        "node_ip": "10.32.217.23",
        "user": "omc",
        "password": "omc",
        "url": "https://clab3766lbwas.netact.nsn-rdnet.net",
        "url_user": "omc",
        "url_password": "omc",
        "mr": "MRC-vDU-10776/MR-MRBTS-10776",
    },
    "clab152": {
        "node_ip": "10.92.135.231",
        "user": "omc",
        "password": "omc",
        "url": "https://clab152lbwas.netact.nsn-rdnet.net",
        "url_user": "omc",
        "url_password": "omc",
        "mr": "MRC-vDU-10776/MR-MRBTS-10776",
    },
}

_ue_host_ssh = SshServiceDetails(addr="10.97.126.200", username="spark", password="spark")

_sigspark_1 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="6d08bd6d",
    server_dir="C:\Program Files (x86)\Spark1.1.2008.13\Bin\Spark.exe",
    python_path="C:/Python38",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="262033031381559",
)

_sigspark_2 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="6d08bd6d",
    server_dir="C:\Program Files (x86)\Spark1.1.2008.13\Bin\Spark.exe",
    python_path="C:/Python38",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="262033031393753",
)

_netact = Netact(netact_id)
# Testline configuration, tl is only variable which can be accessed by agent and test case
# you can access all parameters configured upper by tl parameter
tl = TestLine(
    test_pc=_test_pc,
    nms=_netact,
    attenuators=[_attenuator_5G_1],
    gnbs=[_cbts_0],
    enbs=[_lte_real_enb],
    tl_cloud_topology="CLOUD_5G_CR_DRAN_SNO_3xRU_SA_FDD_Spark",
    cloud_hostings=[_ncir],
    test_pcs=[_enb_test_pc],
    core=_realcore,
    ues=[_sigspark_1, _sigspark_2],
)

_misc = {
    # 1-Use NOM config in __init__.py, 0-Use NOM config in global_variable.py.
    # If this key is not given, default value is 1
    "nom_config_source_from_init_py": "0",
    # 1-Use Netact config in __init__.py, 0-Use Netact config in global_variable.py.
    # If this key is not given, default value is 1
    "netact_config_source_from_init_py": "1",
}
tl._misc = _misc


# only tl variable can be accessed by user
__all__ = ["tl"]
