__maintainer__ = "Lou Shuhui"
__team__ = "RAN_PZ_HAZ4_SG01"
__email__ = "shuhui.lou@nokia-sbell.com"

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
from taf.config.testline.pdu import FPFH, HBTE as PBHBTE
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
from taf.config.testline.cloud_hosting import MasterNode, K8S, HelmChart

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# Testpc
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.159.99", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# CU
_cu = CU(
    instance_id=3,
    global_bts_id=369777,
    backhaul_site_oam_ip=NetworkAddress(v4="10.57.158.137"),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.158.2", username="cranuser3", password="systeM!23"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.158.137", username="Nemuadmin", password="nemuuser", port=443
    ),
    x2c=NetworkAddress(
        v4="10.57.168.123",
        vlan_id=112,
        routing=RoutingInformation(gateway="10.57.168.65", ip_prefix_length=26),
    ),
    f1c=NetworkAddress(
        v4="10.57.168.61",
        vlan_id=109,
        routing=RoutingInformation(gateway="10.57.168.1", ip_prefix_length=26),
    ),
    f1u=NetworkAddress(
        v4="10.57.168.57",
        vlan_id=109,
        routing=RoutingInformation(gateway="10.57.168.1", ip_prefix_length=26),
    ),
    s1u=NetworkAddress(
        v4="10.57.158.61",
        vlan_id=102,
        routing=RoutingInformation(gateway="10.57.158.33", ip_prefix_length=27),
    ),
    x2u=NetworkAddress(
        v4="10.57.168.125",
        vlan_id=110,
        routing=RoutingInformation(gateway="10.57.168.65", ip_prefix_length=26),
    ),
    tracing=None,
)

# cloud_deployment for vCU
_vcu_cnf_1 = DeploymentVnfStack(
    name="vcu3",
    yaml_file=os.path.join(_cfg_dir, "DEP/gnbs_0/vCU/CU_cnf_values-override.yaml"),
)
_vcu_intnet_1 = DeploymentNetworkStack(
    name=_vcu_cnf_1.name + "-prerequisite",
    yaml_file=os.path.join(_cfg_dir, "DEP/gnbs_0/vCU/CU_pvc_values-override.yaml"),
)

# ssh connection information of OE, for tenant user
_vcu_ssh_connection_details = SshServiceDetails(
    addr="10.57.158.2", username="cranuser3", password="systeM!23", port=22
)

# ssh connection information of OE, for root user
_vcu_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.57.158.2", username="core", password="system123", port=22
)

_vcu_master_node = MasterNode(
    k8s_connection_details=_vcu_k8s_connection_details,
    ssh_connection_details=_vcu_ssh_connection_details,
)

_vcu_k8s = K8S(namespace="cran3", master_node=_vcu_master_node)

_cnf_cu_1 = HelmChart(
    name="vcu3",
    yaml_file=os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/cnf.yaml"),
)

_cluster_preparation_cu_1 = HelmChart(
    name=_cnf_cu_1.name  + "-cluster-preparation",
    yaml_file=os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/preparation.yaml"),
)

_prerequisite_cu_1 = HelmChart(
    name=_cnf_cu_1.name + "-prerequisite",
    yaml_file=os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/prerequisite.yaml"),
)


_vcu_k8s_cloud_deployment = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    networks=[_vcu_intnet_1],
    vnfs=[_vcu_cnf_1],
    cluster_preparation=_cluster_preparation_cu_1,
    prerequisite=_prerequisite_cu_1,
    cnf=_cnf_cu_1,
    cloud_hosting=_vcu_k8s,
)


# 5G RU
_ru1_pdu = PBHBTE(addr="10.71.197.40", port_numbers=[1, 2, 3, 4, 5, 6])
_ru2_pdu = FPFH(addr="10.71.197.36", port_numbers=[1, 2, 3, 4, 5, 6])
_ru3_pdu = PBHBTE(addr="10.71.197.38", port_numbers=[1, 2, 3, 4, 5, 6])
_ru4_pdu = PBHBTE(addr="10.71.197.42", port_numbers=[1, 2, 3, 4, 5, 6])
_ru5_pdu = PBHBTE(addr="10.71.197.38", port_numbers=[1, 2, 3, 4, 5, 6])
_ru6_pdu = FPFH(addr="10.71.197.36", port_numbers=[1, 2, 3, 4, 5, 6])

#AS220200107
_ru1 = RU(
    ru_hw_group="hw_group",
    pdu_port=_ru1_pdu.pdu_ports[2],
    radio_type=RadioTypes.AHCA,
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.35",
        username="serviceuser",
        password="bobuWrUHk7Xq7WPpY9ZcjEi8zNdX3plZ+/y420RZ7W4=",
    ),
)

#L1181705792
_ru2 = RU(
    ru_hw_group="hw_group",
    pdu_port=_ru2_pdu.pdu_ports[5],
    radio_type=RadioTypes.AHCA,
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.36",
        username="serviceuser",
        password="bobuWrUHk7Xq7WPpY9ZcjEi8zNdX3plZ+/y420RZ7W4=",
    ),
)

#1M190429307
_ru3 = RU(
    ru_hw_group="hw_group",
    pdu_port=_ru3_pdu.pdu_ports[1],
    radio_type=RadioTypes.AHCA,
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.36",
        username="serviceuser",
        password="bobuWrUHk7Xq7WPpY9ZcjEi8zNdX3plZ+/y420RZ7W4=",
    ),
)

#1M212137298
_ru4 = RU(
    ru_hw_group="hw_group",
    pdu_port=_ru4_pdu.pdu_ports[3],
    radio_type=RadioTypes.AEQE,
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.36",
        username="serviceuser",
        password="bobuWrUHk7Xq7WPpY9ZcjEi8zNdX3plZ+/y420RZ7W4=",
    ),
)

#DH223803757
_ru5 = RU(
    ru_hw_group="hw_group",
    pdu_port=_ru5_pdu.pdu_ports[2],
    radio_type=RadioTypes.AEQE,
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.36",
        username="serviceuser",
        password="bobuWrUHk7Xq7WPpY9ZcjEi8zNdX3plZ+/y420RZ7W4=",
    ),
)

#1M224419781
_ru6 = RU(
    ru_hw_group="hw_group",
    pdu_port=_ru6_pdu.pdu_ports[1],
    radio_type=RadioTypes.AEQY,
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.36",
        username="serviceuser",
        password="bobuWrUHk7Xq7WPpY9ZcjEi8zNdX3plZ+/y420RZ7W4=",
    ),
)

_pxe_server_ssh_info = SshServiceDetails(
    addr="10.71.220.62", username="root", password="uteadmin"
)
_pxe_server = PxeServer(
    nfs_ip="10.71.220.62", ssh_connection_details=_pxe_server_ssh_info
)
 
# FHGW information
_fhgw_0 = FHGW(user_config_path=_cfg_dir, rus=[_ru1, _ru2], pxe_server=_pxe_server)
_fhgw_0.ip = "10.64.173.109"
_fhgw_0.username = "toor4nsn"
_fhgw_0.password = "Fhgw@nokia123"
_fhgw_0.version = "24R1"


# vDU
# ssh connection information of OE, for tenant user
_ssh_connection_details_0 = SshServiceDetails(
    addr="10.64.174.186", username="cranuser3", password="systeM!23"
)
# ssh connection information of OE, for root user
_k8s_connection_details_0 = K8SConnectionDetails(
    ip_addr="10.64.174.186", username="core", password="system123", port="22"
)

_master_node_0 = MasterNode(
    k8s_connection_details=_k8s_connection_details_0,
    ssh_connection_details=_ssh_connection_details_0,
)

_k8s_0 = K8S(namespace="cran3", master_node=_master_node_0)
_vdu_cnf_0 = DeploymentVnfStack(
    name="vdu3",
    yaml_file=os.path.join(_cfg_dir, "DEP/gnbs_0/vDU_0/DU_cnf_values-override.yaml"),
)

_vdu_intnet_0 = DeploymentNetworkStack(
    name=_vdu_cnf_0.name + "-prerequisite",
    yaml_file=os.path.join(_cfg_dir, "DEP/gnbs_0/vDU_0/DU_pvc_values-override.yaml"),
)

_cnf_du_0 = HelmChart(
    name="vdu3",
    yaml_file=os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/cnf.yaml"),
)

_cluster_preparation_du_0 = HelmChart(
    name=_cnf_du_0.name  + "-cluster-preparation",
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
    cluster_preparation=_cluster_preparation_du_0,
    prerequisite=_prerequisite_du_0,
    cnf=_cnf_du_0,
)


_du_0 = VDU(
    cloud_deployment=_vdu_k8s_cloud_deployment_0,
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.64.174.210", username="Nemuadmin", password="nemuuser", port=443
    ),
    fhgws=[_fhgw_0],
    rus=[_ru1, _ru2, _ru3, _ru4, _ru5, _ru6],
    instance_id=1,
    global_bts_id=369777,
)

# BTS
_cbts = CloudBts(
    dus=[_du_0],
    cu=_cu,
    cloud_deployment=_vcu_k8s_cloud_deployment,
)


# UL traffic: ${tl.appserver.iperf_details.port}

_appserver2_ssh = SshServiceDetails(
    addr="10.71.218.215", username="MN5GRAN", password="nokia123@"
)

# ${EPC_IP}=${tl.appserver.iperf_details.network_interface_address}
_iperf_details_on_appserver2 = IperfDataTransferDetails(
    ssh_connection_details=_appserver2_ssh,
    network_interface_address="10.71.219.233",
    iperf_path="/data/local/tmp/iperf",
    port=51001,
)

_appserver = AppServer(_iperf_details_on_appserver2)


# DL traffic:  ${tl.ues[${ue_index}].iperf_details.port}
_appserver_ssh = SshServiceDetails(
    addr="10.71.207.142",
    username="vrf4_sg1",
    password="vrf4@sg1",
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.207.142",
    iperf_path="iperf",
    port=51001,
)
# spark license
_licensekeeper = LicenseKeeper(username="HAZ4_SG1", password="HAZ4_SG1")


# SA   CI_Detail_UE_Type='Huawei Mate 30 Pro 5G'
_sigspark = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.218.215", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="9YS0220721008832",
    server_dir="C:/Program Files (x86)/Spark/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="460023100013268",
    capabilities=["huawei_sigspark"],
    licensekeeper=_licensekeeper,
)


# TestLine
tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    tl_cloud_topology="CLOUD_5G_AIC_OCP",
    ues=[_sigspark],
    appserver=_appserver,
)

__all__ = ["tl"]
