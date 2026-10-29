__maintainer__ = "Cheng Jiajing"
__team__ = "RAN_PZ_HAZ4_SG01"
__email__ = "jiajing.1.cheng@nokia-sbell.com"

import os

from taf.config.testline import (
    CloudDeployment,
    DeploymentNetworkStack,
    DeploymentVnfStack,
    MasterNode,
    K8S,
)
from taf.config.testline import (
    SshServiceDetails,
    HttpConnectionDetails,
    K8SConnectionDetails,
    HelmChart,
)
from taf.config.testline import NetworkAddress, RoutingInformation
from taf.config.testline import RealEnb, Airscale, CommonUnit
from taf.config.testline import RU, RadioTypes
from taf.config.testline import CloudBts, CU
from taf.config.testline import VDU, FHGW
from taf.config.testline import PxeServer
from taf.config.testline import TestLine
from taf.config.testline import RealEnb
from taf.config.testline import TestPc
from taf.config.testline.attenuator import HBTE
from taf.config.testline.pdu import HBTE as PBHBTE

# from taf.config.testline.pdu import TopYoung as pdu_TopYoung
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.ue import Airphone, Qualcomm, QualcommUeType, Android, MediaTek
from taf.config.testline.appserver import AppServer
from taf.config.testline import LicenseKeeper

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# Testpc
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.5", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# CU
_cu = CU(
    instance_id=1124,
    global_bts_id=10548,
    backhaul_site_oam_ip=NetworkAddress(v4="10.57.179.15"),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.187.2", username="cranuser1124", password="systeM!23"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.187.147", username="Nemuadmin", password="nemuuser", port=443
    ),
    x2c=NetworkAddress(
        v4="10.57.250.98",
        vlan_id=110,
        routing=RoutingInformation(gateway="10.57.250.65", ip_prefix_length=26),
    ),
    f1c=NetworkAddress(
        v4="10.57.250.34",
        vlan_id=109,
        routing=RoutingInformation(gateway="10.57.250.1", ip_prefix_length=26),
    ),
    f1u=NetworkAddress(
        v4="10.57.250.36",
        vlan_id=109,
        routing=RoutingInformation(gateway="10.57.250.1", ip_prefix_length=26),
    ),
    s1u=NetworkAddress(
        v4="10.57.187.51",
        vlan_id=102,
        routing=RoutingInformation(gateway="10.57.187.33", ip_prefix_length=27),
    ),
    x2u=NetworkAddress(
        v4="10.57.250.100",
        vlan_id=110,
        routing=RoutingInformation(gateway="10.57.250.65", ip_prefix_length=26),
    ),
    tracing=None,
)

# cloud_deployment for vCU
_vcu_cnf_1 = DeploymentVnfStack(
    name="vcu1124",
    yaml_file=os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/cnf.yaml"),
)
_vcu_intnet_1 = DeploymentNetworkStack(
    name=_vcu_cnf_1.name + "-prerequisite",
    yaml_file=os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/cnf.yaml"),
)

_cnf_cu_1 = HelmChart(
    name="vcu1124",
    yaml_file=os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/cnf.yaml"),
)

_cluster_preparation_cu_1 = HelmChart(
    name=_cnf_cu_1.name + "-cluster-preparation",
    yaml_file=os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/preparation.yaml"),
)

_prerequisite_cu_1 = HelmChart(
    name=_cnf_cu_1.name + "-prerequisite",
    yaml_file=os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/prerequisite.yaml"),
)

# ssh connection information of OE, for tenant user
_vcu_ssh_connection_details = SshServiceDetails(
    addr="10.57.187.2", username="cranuser1124", password="systeM!23", port=22
)
# ssh connection information of OE, for root user
_vcu_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.57.187.2", username="core", password="system123", port=22
)

_vcu_master_node = MasterNode(
    k8s_connection_details=_vcu_k8s_connection_details,
    ssh_connection_details=_vcu_ssh_connection_details,
)

_vcu_k8s = K8S(namespace="cran1124", master_node=_vcu_master_node)

_vcu_k8s_cloud_deployment = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    networks=[_vcu_intnet_1],
    vnfs=[_vcu_cnf_1],
    cloud_hosting=_vcu_k8s,
    cluster_preparation=_cluster_preparation_cu_1,
    prerequisite=_prerequisite_cu_1,
    cnf=_cnf_cu_1,
)


# 5G RU

_ru_pdu = PBHBTE(addr="10.71.197.48", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_ru1 = RU(
    ru_hw_group="hw_group",
    pdu_port=_ru_pdu.pdu_ports[1],
    radio_type=RadioTypes.AZQI,
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.35",
        username="rfsw",
        password="5rfS2qmWC0AiFYvir7k8JekCN8/NklqDK5E6OWXuUVQ=",
    ),
)

_ru2_pdu = PBHBTE(addr="10.71.197.45", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru2 = RU(
    ru_hw_group="hw_group",
    pdu_port=_ru2_pdu.pdu_ports[7],
    radio_type=RadioTypes.AZQI,
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.37",
        username="serviceuser",
        password="bobuWrUHk7Xq7WPpY9ZcjEi8zNdX3plZ+/y420RZ7W4=",
    ),
)

_ru3_pdu = PBHBTE(addr="10.71.197.48", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru3 = RU(
    ru_hw_group="hw_group",
    pdu_port=_ru3_pdu.pdu_ports[1],
    radio_type=RadioTypes.AZQI,
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.37",
        username="serviceuser",
        password="bobuWrUHk7Xq7WPpY9ZcjEi8zNdX3plZ+/y420RZ7W4=",
    ),
)

_ru4_pdu = PBHBTE(addr="10.71.197.48", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru4 = RU(
    ru_hw_group="hw_group",
    pdu_port=_ru4_pdu.pdu_ports[3],
    radio_type=RadioTypes.AZQI,
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.37",
        username="serviceuser",
        password="bobuWrUHk7Xq7WPpY9ZcjEi8zNdX3plZ+/y420RZ7W4=",
    ),
)

_ru5_pdu = PBHBTE(addr="10.71.197.52", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru5 = RU(
    ru_hw_group="hw_group",
    pdu_port=_ru5_pdu.pdu_ports[6],
    radio_type=RadioTypes.AZQI,
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.37",
        username="serviceuser",
        password="bobuWrUHk7Xq7WPpY9ZcjEi8zNdX3plZ+/y420RZ7W4=",
    ),
)

# FHGW information
_pxe_server_ssh_info = SshServiceDetails(
    addr="0.0.0.0", username="root", password="centos"
)
_pxe_server = PxeServer(nfs_ip="0.0.0.0", ssh_connection_details=_pxe_server_ssh_info)

_fhgw_0 = FHGW(user_config_path=_cfg_dir, rus=[_ru1, _ru2], pxe_server=_pxe_server)
_fhgw_0.ip = "10.71.222.149"
_fhgw_0.username = "toor4nsn"
_fhgw_0.password = "Fhgw@nokia123"
_fhgw_0.version = "22R3"

_fhgw_1 = FHGW(user_config_path=_cfg_dir, rus=[_ru3], pxe_server=_pxe_server)
_fhgw_1.ip = "10.71.220.75"
_fhgw_1.username = "toor4nsn"
_fhgw_1.password = "Fhgw@nokia123"
_fhgw_1.version = "22R3"

_fhgw_2 = FHGW(user_config_path=_cfg_dir, rus=[_ru4], pxe_server=_pxe_server)
_fhgw_2.ip = "10.71.221.233"
_fhgw_2.username = "toor4nsn"
_fhgw_2.password = "Fhgw@nokia123"
_fhgw_2.version = "22R3"

_fhgw_3 = FHGW(user_config_path=_cfg_dir, rus=[_ru5], pxe_server=_pxe_server)
_fhgw_3.ip = "10.71.220.73"
_fhgw_3.username = "toor4nsn"
_fhgw_3.password = "Fhgw@nokia123"
_fhgw_3.version = "22R3"

# vDU_1
_ssh_connection_details_0 = SshServiceDetails(
    addr="10.71.222.178", username="cranuser1124", password="systeM!23", port=22
)
_k8s_connection_details_0 = K8SConnectionDetails(
    ip_addr="10.71.222.178", username="core", password="system123", port=22
)

_master_node_0 = MasterNode(
    k8s_connection_details=_k8s_connection_details_0,
    ssh_connection_details=_ssh_connection_details_0,
)
_k8s_0 = K8S(namespace="cran1124", master_node=_master_node_0)
_vdu_cnf_0 = DeploymentVnfStack(
    name="vdu1124",
    yaml_file=os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/cnf.yaml"),
)
_vdu_intnet_0 = DeploymentNetworkStack(
    name=_vdu_cnf_0.name + "-prerequisite",
    yaml_file=os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/cnf.yaml"),
)
_cnf_du_0 = HelmChart(
    name="vdu1124",
    yaml_file=os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/cnf.yaml"),
)
_cluster_preparation_du_0 = HelmChart(
    name=_cnf_du_0.name + "-cluster-preparation",
    yaml_file=os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/preparation.yaml"),
)

_prerequisite_du_0 = HelmChart(
    name=_cnf_du_0.name + "-prerequisite",
    yaml_file=os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/prerequisite.yaml"),
)

_vdu_k8s_cloud_deployment_0 = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    cloud_hosting=_k8s_0,
    networks=[_vdu_intnet_0],
    vnfs=[_vdu_cnf_0],
    cluster_preparation=_cluster_preparation_du_0,
    prerequisite=_prerequisite_du_0,
    cnf=_cnf_du_0,
)


_du_0 = VDU(
    cloud_deployment=_vdu_k8s_cloud_deployment_0,
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.223.58", username="Nemuadmin", password="nemuuser", port=443
    ),
    rus=[_ru1, _ru2],
    fhgws=[],
    instance_id=1124,
    global_bts_id=10548,
)

# vDU_2
_ssh_connection_details_1 = SshServiceDetails(
    addr="10.71.220.242", username="core", password="system123"
)
_k8s_connection_details_1 = K8SConnectionDetails(
    ip_addr="10.71.220.242", username="core", password="system123", port="22"
)

_master_node_1 = MasterNode(
    k8s_connection_details=_k8s_connection_details_1,
    ssh_connection_details=_ssh_connection_details_1,
)
_k8s_1 = K8S(namespace="cran1", master_node=_master_node_1)
_vdu_cnf_1 = DeploymentVnfStack(
    name="vdutest",
    yaml_file=os.path.join(_cfg_dir, "DEP/gnbs_0/vDU_1/DU_cnf_values-override.yaml"),
)
_vdu_intnet_1 = DeploymentNetworkStack(
    name=_vdu_cnf_1.name + "-prerequisite",
    yaml_file=os.path.join(_cfg_dir, "DEP/gnbs_0/vDU_1/DU_pvc_values-override.yaml"),
)

_vdu_k8s_cloud_deployment_1 = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    cloud_hosting=_k8s_1,
    networks=[_vdu_intnet_1],
    vnfs=[_vdu_cnf_1],
)

_du_1 = VDU(
    cloud_deployment=_vdu_k8s_cloud_deployment_1,
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.221.90", username="Nemuadmin", password="Nokia@123", port=443
    ),
    fhgws=[_fhgw_1],
    instance_id=1124,
    global_bts_id=10548,
)

# vDU_3
_ssh_connection_details_2 = SshServiceDetails(
    addr="10.71.222.34", username="core", password="system123"
)
_k8s_connection_details_2 = K8SConnectionDetails(
    ip_addr="10.71.222.34", username="core", password="system123", port="22"
)

_master_node_2 = MasterNode(
    k8s_connection_details=_k8s_connection_details_2,
    ssh_connection_details=_ssh_connection_details_2,
)
_k8s_2 = K8S(namespace="cran1", master_node=_master_node_2)
_vdu_cnf_2 = DeploymentVnfStack(
    name="vdutest",
    yaml_file=os.path.join(_cfg_dir, "DEP/gnbs_0/vDU_2/DU_cnf_values-override.yaml"),
)
_vdu_intnet_2 = DeploymentNetworkStack(
    name=_vdu_cnf_2.name + "-prerequisite",
    yaml_file=os.path.join(_cfg_dir, "DEP/gnbs_0/vDU_2/DU_pvc_values-override.yaml"),
)

_vdu_k8s_cloud_deployment_2 = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    cloud_hosting=_k8s_2,
    networks=[_vdu_intnet_2],
    vnfs=[_vdu_cnf_2],
)

_du_2 = VDU(
    cloud_deployment=_vdu_k8s_cloud_deployment_2,
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.222.74", username="Nemuadmin", password="Nokia@123", port=443
    ),
    fhgws=[_fhgw_2],
    instance_id=1124,
    global_bts_id=10548,
)

# vDU_4
_ssh_connection_details_3 = SshServiceDetails(
    addr="10.71.220.194", username="core", password="system123"
)
_k8s_connection_details_3 = K8SConnectionDetails(
    ip_addr="10.71.220.194", username="core", password="system123", port="22"
)

_master_node_3 = MasterNode(
    k8s_connection_details=_k8s_connection_details_3,
    ssh_connection_details=_ssh_connection_details_3,
)
_k8s_3 = K8S(namespace="cran1", master_node=_master_node_3)
_vdu_cnf_3 = DeploymentVnfStack(
    name="vdutest",
    yaml_file=os.path.join(_cfg_dir, "DEP/gnbs_0/vDU_3/DU_cnf_values-override.yaml"),
)
_vdu_intnet_3 = DeploymentNetworkStack(
    name=_vdu_cnf_3.name + "-prerequisite",
    yaml_file=os.path.join(_cfg_dir, "DEP/gnbs_0/vDU_3/DU_pvc_values-override.yaml"),
)

_vdu_k8s_cloud_deployment_3 = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    cloud_hosting=_k8s_3,
    networks=[_vdu_intnet_3],
    vnfs=[_vdu_cnf_3],
)

_du_3 = VDU(
    cloud_deployment=_vdu_k8s_cloud_deployment_3,
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.220.226", username="Nemuadmin", password="Nokia@123", port=443
    ),
    fhgws=[_fhgw_3],
    instance_id=1124,
    global_bts_id=10548,
)

# BTS
_cbts = CloudBts(
    dus=[_du_0],
    cu=_cu,
    cloud_deployment=_vcu_k8s_cloud_deployment,
)

# LTE
_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.71.215.41", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(
    airscale=_real_enb,
    oam_ip="10.71.215.41",
    global_bts_id="1124",
)

# PA info
_attenuator_PA1 = HBTE(
    ip_addr="10.71.206.135",
    port=5000,
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    model="PA-16-16-6-127-0.5-B-S",
)

_attenuator_PA2 = HBTE(
    ip_addr="10.71.206.136",
    port=5000,
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    model="PA-16-16-6-127-0.5-B-S",
)


# UE samsung
# UL traffic: ${tl.appserver.iperf_details.port}

_appserver2_ssh = SshServiceDetails(
    addr="10.71.217.18", username="noklab\mn5gran", password="nokia123@"
)

##${EPC_IP}=${tl.appserver.iperf_details.network_interface_address}
_iperf_details_on_appserver2 = IperfDataTransferDetails(
    ssh_connection_details=_appserver2_ssh,
    network_interface_address="10.71.219.233",
    iperf_path="/data/local/tmp/iperf",
    port=51001,
)

_appserver = AppServer(_iperf_details_on_appserver2)


# DL traffic:  ${tl.ues[${ue_index}].iperf_details.port}
_appserver_ssh = SshServiceDetails(
    addr="10.71.219.233",
    username="cmw_sg1",
    password="cm@1",
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.219.233",
    iperf_path="iperf",
    port=51001,
)

# spark license
_licensekeeper = LicenseKeeper(username="shuhui.lou@nokia-sbell.com", password="123456")

# UE_STU
_sigspark = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.217.18", username="mn5gran", password="nokia123@"
    ),
    serial_number="3df8a4f4",
    server_dir="C:/Program Files (x86)/Spark/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="460023100010655",
    capabilities=["huawei_sigspark"],
    licensekeeper=_licensekeeper,
)

# TestLine
tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    tl_cloud_topology="CLOUD_5G_AIC_RM17_OCP_FHGW_AZQI",
    enbs=[_lte_real_enb],
    ues=[_sigspark],
    attenuators=[_attenuator_PA1, _attenuator_PA2],
    appserver=_appserver,
)

__all__ = ["tl"]
