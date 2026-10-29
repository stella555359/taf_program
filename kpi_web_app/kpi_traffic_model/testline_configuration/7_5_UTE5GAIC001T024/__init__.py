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
    CapacityUnit,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline import RealEnb, NetworkAddress, RoutingInformation
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU
from taf.config.testline import DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC
# from taf.config.testline.pdu import HBTE as PBHBTE
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
# _test_pc = TestPc(
#     default_ssh_connection_details=SshServiceDetails(
#         addr="10.108.229.144", username="ute", password="ute"
#     )
# )

# VCU related OCP controlNode
_control = ControlNode(
    # Configuration for SSH access
    default_ssh_connection_details=SshServiceDetails(
        addr="10.110.8.130", username="cranuser3", password="systeM!23"
    ),
    # Configuration for openstack connection
    open_stack_connection_details=OpenStackConnectionDetails(
        username="cranuser3",
        password="systeM!23",
        ip_addr="10.110.8.130",
        tenant="cran3",
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
        v4="10.107.87.11"
        # v6='2a00:8a00:8000:5002:0:5:0000:070b'
    ),
    # VCU OAM ssh connection, oam interface ip of oam vm
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.110.8.130", username="cranuser3", password="systeM!23"
    ),
    # VCU OAM http connection, oam interface ip of oam vm
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.110.113.136", username="Nemuadmin", password="nemuuser", port="443"
    ),
    # route configuration for x2 link to ENB, v4 is network address of ENB x2 link
    x2c=NetworkAddress(
        v4="10.107.85.75",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.107.85.65", ip_prefix_length=26),
    ),
    # route configuration for f1c link to VDU on VCU, v4 is network address of VDU f1c link
    f1c=NetworkAddress(
        v4="10.107.85.11",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.107.85.1", ip_prefix_length=26),
    ),
    # route configuration for f1u link to VDU on VCU, v4 is network address of VDU f1u link
    f1u=NetworkAddress(
        v4="10.107.85.143",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.107.85.129", ip_prefix_length=25),
    ),
    s1u=NetworkAddress(
        v4="10.107.86.143",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.107.86.129", ip_prefix_length=25),
    ),
    x2u=NetworkAddress(
        v4="10.107.86.15",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.107.86.1", ip_prefix_length=25),
    ),
    tracing=None,
)

# enb for NSA
_real_enb = RealEnb(oam_ip="10.97.122.232", instance_id="")

# test pc information of enb
# you can configure it as AIC UTE environment
_enb_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.108.229.144", username="ute", password="ute"
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
    addr="10.108.205.94", username="cranuser1", password="systeM!23"
)

# ssh connection information of OE, for cloudadmin user
_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.108.205.94", username="core", password="system123", port="22"
)

# master node information of OE
_master_node = MasterNode(
    k8s_connection_details=_k8s_connection_details,
    ssh_connection_details=_ssh_connection_details,
)

_k8s = K8S(namespace="cran1", master_node=_master_node)

_cluster_preparation_du = HelmChart(
    name="aic-vdu-cluster-preparation",
    yaml_file=os.path.join(_cfg_dir, 'vdu-cluster-preparation.yaml'),
)

_prerequisite_du = HelmChart(
    name="aic-vdu-prerequisite",
    yaml_file=os.path.join(_cfg_dir, 'vdu-prerequisite.yaml'),
)
 
_cnf_du = HelmChart(
    name="aic-vdu",
    yaml_file=os.path.join(_cfg_dir, 'vdu-cnf.yaml'),
)

# VDU deployment configuration
_k8s_cloud_deployment = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    networks=[_vdu_intnet_0],
    vnfs=[_vdu_vnf_0],
    cloud_hosting=_k8s,
    cluster_preparation=_cluster_preparation_du,
    prerequisite=_prerequisite_du,
    cnf=_cnf_du,
)

# VDU oam http connection
_vdu_oam_http_connection_details = HttpConnectionDetails(
    addr="10.108.205.66", port="443", username="Nemuadmin", password="nemuuser"
)
_hbte_params_139 = {
    "ip_addr": "10.97.122.139",
    "port": 23,
    "attenuation_port_numbers": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    "model": "PA-16-8-4-127-0.5-B-S",
    "version": None,
}

_hbte_params_234 = {
    "ip_addr": "10.97.126.234",
    "port": 5000,
    "attenuation_port_numbers": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    "model": "PA-16-8-4-127-0.5-B-S",
    "version": None,
}

_hbte_params_236 = {
    "ip_addr": "10.97.126.236",
    "port": 5000,
    "attenuation_port_numbers": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    "model": "PA-16-8-4-127-0.5-B-S",
    "version": None,
}

# RU PDU
# _ru_pdu = PBHBTE(addr="10.97.122.137", port_numbers=[3])
#_ru_pdu_1 = TP(addr="10.97.126.241", port_numbers=[1,2,3,4,5])
#_ru_pdu_2 = TP(addr="10.97.122.183", port_numbers=[1,2,3,4,5])

_attenuator_5G_234 = HBTE(**_hbte_params_234)
_attenuator_5G_139 = TopYoung(**_hbte_params_139)
_attenuator_5G_236 = HBTE(**_hbte_params_236)

# RU configuration
_ru_1 = RU(
    ru_hw_group="RU_INT_ECPRI",
    serial_number="L1221806960",
    attenuation_ports=[
        _attenuator_5G_234.attenuator_ports[1],
        _attenuator_5G_234.attenuator_ports[3],
        _attenuator_5G_234.attenuator_ports[5],
        _attenuator_5G_234.attenuator_ports[7],
    ],
#    pdu_port=_ru_pdu_1.pdu_ports[1]
)

_ru_2 = RU(
    ru_hw_group="RU_INT_ECPRI",
    serial_number="1M212230325",
    attenuation_ports=[
        _attenuator_5G_139.attenuator_ports[2],
        _attenuator_5G_139.attenuator_ports[4],
        _attenuator_5G_139.attenuator_ports[6],
        _attenuator_5G_139.attenuator_ports[8],
    ],
#    pdu_port=_ru_pdu_2.pdu_ports[2]
)

_ru_3 = RU(
    ru_hw_group="RU_INT_ECPRI",
    serial_number="1M213303650",
    attenuation_ports=[
        _attenuator_5G_236.attenuator_ports[9],
        _attenuator_5G_236.attenuator_ports[10],
        _attenuator_5G_236.attenuator_ports[11],
        _attenuator_5G_236.attenuator_ports[12],
    ],
#    pdu_port=_ru_pdu_1.pdu_ports[2]
)

# PXE server info for FHGW deployment
_pxe_server_ssh_info = SshServiceDetails(
    addr="10.69.38.28", username="root", password="pxe@systeM!23"
)
_pxe_server = PxeServer(
    nfs_ip="10.68.179.27", ssh_connection_details=_pxe_server_ssh_info
)

# FHGW information
_fhgw_0 = FHGW(
    user_config_path=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/FHGW_0/fhgw_user_config_0.yaml"
    ),
    rus=[_ru_1, _ru_2, _ru_3],
    pxe_server=_pxe_server,
)
_fhgw_0.ssh_username = "root"
_fhgw_0.ssh_password = "Fhgw@systeM!23"

# VDU global configuration
_vdu_0 = VDU(
    cloud_deployment=_k8s_cloud_deployment,
    oam_http_connection_details=_vdu_oam_http_connection_details,
    fhgws=[_fhgw_0],
    # route configuration of f1m link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_m_ip_addr=NetworkAddress(
        v4="10.108.205.0",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.69.55.25", ip_prefix_length=24),
    ),
    # route configuration of f1c link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_c_ip_addr=NetworkAddress(
        v4="10.108.205.0",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.69.55.25", ip_prefix_length=24),
    ),
    # route configuration of f1u link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_u_ip_addr=NetworkAddress(
        v4="10.108.205.0",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.69.55.25", ip_prefix_length=24),
    ),
)

# mcc, mnc configuration
_realcore = RealCore(five_g=None, mcc="262", mnc="03", pdns=None)

_appserver_ssh = SshServiceDetails(
    addr="10.108.229.44", username="ute", password="Cdslabadmin@"
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_name="rmnet_data0",
)
_android_1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.97.126.227", username="aic", password="Nokia123!"
    ),
    serial_number="R5CR414M8ZN",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_SUMSANG_1", "REAL_ANDROID_UE1"],
    service_call_attach=17,
    service_call_detach=17,
)

_android_2 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.97.122.150", username="aic", password="Nokia123!"
    ),
    serial_number="R5CR40W6NEF",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_SUMSANG_2", "REAL_ANDROID_UE2"],
    service_call_attach=17,
    service_call_detach=17,
)

_android_3 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.97.126.198", username="pz2", password="Nokia@2w3e4r5t6y7u"
    ),
    serial_number="R5CR312LXLW",
    iperf_details=_iperf,
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    capabilities=["REAL_SUMSANG_3", "REAL_ANDROID_UE3"],
    service_call_attach=17,
    service_call_detach=17,
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
    addr="10.110.8.130", username="cranuser3", password="systeM!23"
)
# ssh connection information of OE, for root user
_vcu_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.110.8.130", username="core", password="system123", port="22"
)

_vcu_master_node = MasterNode(
    k8s_connection_details=_vcu_k8s_connection_details,
    ssh_connection_details=_vcu_ssh_connection_details,
)

_vcu_k8s = K8S(namespace="cran3", master_node=_vcu_master_node)

_cluster_preparation_cu_1 = HelmChart(
    name="aic-vcu-cluster-preparation",
    yaml_file=os.path.join(_cfg_dir, 'vcu-cluster-preparation.yaml'),
)

_prerequisite_cu_1 = HelmChart(
    name="aic-vcu-prerequisite",
    yaml_file=os.path.join(_cfg_dir, 'vcu-prerequisite.yaml'),
)
 
_cnf_cu_1 = HelmChart(
    name="aic-vcu",
    yaml_file=os.path.join(_cfg_dir, 'vcu-cnf.yaml'),
)


_vcu_k8s_cloud_deployment = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    networks=[_vcu_intnet_1],
    vnfs=[_vcu_vnf_1],
    cloud_hosting=_vcu_k8s,
    cluster_preparation=_cluster_preparation_cu_1,
    prerequisite=_prerequisite_cu_1,
    cnf=_cnf_cu_1,
)


# VCU global configuration
_cbts_0 = CloudBts(
    dus=[_vdu_0],  # vdu related parameter
    cu=_cu,
    cloud_deployment=_vcu_k8s_cloud_deployment,
    instance_id="10778",
    global_bts_id="10778",
)

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.108.229.204", username="ute", password="QAZqaz123!@#"
    ),
    connections=[_cbts_0]
)

netact_id = {
    "clab33": {
        "node_ip": "10.53.80.134",
        "user": "omc",
        "password": "Medsql!_1893",
        "url": "https://srnclab33lbwas.srnblr.nsn-rdnet.net",
        "url_user": "omc",
        "url_password": "Medsql!_1893",
        "mr": "MRC-AICTAVDU/MR-10778",
    },
}

_netact = Netact(netact_id)
# Testline configuration, tl is only variable which can be accessed by agent and test case
# you can access all parameters configured upper by tl parameter
tl = TestLine(
    test_pc=_test_pc,
    nms=_netact,
    attenuators=[_attenuator_5G_234, _attenuator_5G_139, _attenuator_5G_236],
    gnbs=[_cbts_0],
    enbs=[_real_enb],
    tl_cloud_topology="CLOUD_5G_AIC_OCP_OCP_AEQY",
    cloud_hostings=[_ncir],
    test_pcs=[_test_pc],
    core=_realcore,
    ues=[_android_1, _android_2, _android_3],
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

# only tl variable can be accessed by user
__all__ = ["tl"]
