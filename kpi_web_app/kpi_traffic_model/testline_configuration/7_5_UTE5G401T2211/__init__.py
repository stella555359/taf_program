__maintainer__ = "Wang Bin"
__team__ = "RAN_PZ_HAZ4_SG01"
__email__ = "bin.3.wang@nokia-sbell.com"

import os

from taf.config.testline import (
    CloudDeployment,
    MasterNode,
    K8S,
)
from taf.config.testline import (
    SshServiceDetails,
    HttpConnectionDetails,
    K8SConnectionDetails,
    HelmChart,
)
from taf.config.testline.cloud_hosting import (
    DeploymentNetworkStack,
    DeploymentVnfStack,
    CloudDeployment,
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
from taf.config.testline import VDU, RANNIC
#from taf.config.testline.attenuator import HBTE 
#from taf.config.testline.pdu import HBTE as PBHBTE
from taf.config.testline.pdu import TopYoung, FACOM, HBTE
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
        addr="10.57.189.36", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# CU
_cu = CU(
    instance_id=2211,
    global_bts_id=36962,
    backhaul_site_oam_ip=NetworkAddress(v4="10.57.209.144"),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.209.2", username="cranuser2211", password="systeM!23"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.209.144", username="Nemuadmin", password="nemuuser", port="443"
    ),
	x2c=NetworkAddress(
        v4="10.57.210.92",
        vlan_id=110,
        routing=RoutingInformation(gateway="10.57.166.65", ip_prefix_length=26),
    ),
    f1c=NetworkAddress(
        v4="10.57.210.27",
        vlan_id=109,
        routing=RoutingInformation(gateway="10.57.210.1", ip_prefix_length=26),
    ),
    f1u=NetworkAddress(
        v4="10.57.210.28",
        vlan_id=109,
        routing=RoutingInformation(gateway="10.57.210.1", ip_prefix_length=26),
    ),
    s1u=NetworkAddress(
        v4="10.57.209.48",
        vlan_id=102,
        routing=RoutingInformation(gateway="10.57.209.33", ip_prefix_length=27),
    ),
    x2u=NetworkAddress(
        v4="10.57.210.93",
        vlan_id=110,
        routing=RoutingInformation(gateway="10.57.210.65", ip_prefix_length=26),
    ),
    tracing=NetworkAddress(
        v4="10.57.209.80",
        vlan_id=103,
        routing_v4=RoutingInformation(gateway="10.57.209.65/27"),
    ),
)

# ssh connection information of OE, for tenant user
_vcu_ssh_connection_details = SshServiceDetails(
    addr="10.57.209.2", username="cranuser2211", password="systeM!23", port=22
)
# ssh connection information of OE, for root user
_vcu_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.57.209.2", username="core", password="system123", port=22
)

_vcu_master_node = MasterNode(
    k8s_connection_details=_vcu_k8s_connection_details,
    ssh_connection_details=_vcu_ssh_connection_details,
)

_vcu_k8s = K8S(namespace="cran2211", master_node=_vcu_master_node)

_cnf_cu_1 = HelmChart(
    name="vcu2211",
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
_vcu_k8s_cloud_deployment = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    cloud_hosting=_vcu_k8s,
    cluster_preparation=_cluster_preparation_cu_1,
    prerequisite=_prerequisite_cu_1,
    cnf=_cnf_cu_1,
)


# 5G RU

_ru1_pdu = HBTE(addr="10.71.197.46", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_ru2_pdu = HBTE(addr="10.71.197.46", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_ru3_pdu = HBTE(addr="10.71.197.47", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_ru4_pdu = TopYoung(addr="10.71.197.52", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru1 = RU(
    ru_hw_group="hw_group",
    pdu_port=_ru1_pdu.pdu_ports[4],
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.3",
        username="serviceuser",
        password="bobuWrUHk7Xq7WPpY9ZcjEi8zNdX3plZ+/y420RZ7W4=",
    ),
)

_ru2 = RU(
    ru_hw_group="hw_group",
    pdu_port=_ru2_pdu.pdu_ports[2],
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.1",
        username="serviceuser",
        password="bobuWrUHk7Xq7WPpY9ZcjEi8zNdX3plZ+/y420RZ7W4=",
    ),
)

_ru3 = RU(
    ru_hw_group="hw_group",
    pdu_port=_ru3_pdu.pdu_ports[3],
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.2",
        username="serviceuser",
        password="bobuWrUHk7Xq7WPpY9ZcjEi8zNdX3plZ+/y420RZ7W4=",
    ),
)

_ru4 = RU(
    ru_hw_group="hw_group",
    pdu_port=_ru4_pdu.pdu_ports[5],
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.2",
        username="serviceuser",
        password="bobuWrUHk7Xq7WPpY9ZcjEi8zNdX3plZ+/y420RZ7W4=",
    ),
)


# vDU
# RANNIC information
_rannic_0 = RANNIC(serial_number="L1240808929", product_code="AF1791.101")

# ssh connection information of OE, for tenant user
_ssh_connection_details_0 = SshServiceDetails(
    addr="10.64.168.58", username="cranuser2211", password="systeM!23"
)
# ssh connection information of OE, for root user
_k8s_connection_details_0 = K8SConnectionDetails(
    ip_addr="10.64.168.58", username="core", password="system123", port="22"
)

_master_node_0 = MasterNode(
    k8s_connection_details=_k8s_connection_details_0,
    ssh_connection_details=_ssh_connection_details_0,
)
_k8s_0 = K8S(namespace="cran2211", master_node=_master_node_0)


_cnf_du_0 = HelmChart(
    name="vdu2211",
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

_vdu_vnf_0 = DeploymentVnfStack(
    # this is vdu release name, the name should only be lower case and only can include alphabet number,
    name="ocp-vdu"
)

_vdu_k8s_cloud_deployment_0 = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    cloud_hosting=_k8s_0,
    cluster_preparation=_cluster_preparation_du_0,
    prerequisite=_prerequisite_du_0,
    vnfs=[_vdu_vnf_0],
    cnf=_cnf_du_0,
)

_du_0 = VDU(
    cloud_deployment=_vdu_k8s_cloud_deployment_0,
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.64.168.82", username="Nemuadmin", password="nemuuser", port="443"
    ),
    rus=[_ru1, _ru2, _ru3, _ru4],
    rannics=[_rannic_0],
    instance_id=2211,
    global_bts_id=36962,
)

# BTS
_cbts = CloudBts(
    dus=[_du_0],
    cu=_cu,
    cloud_deployment=_vcu_k8s_cloud_deployment,
)


# UL traffic: ${tl.appserver.iperf_details.port}

_appserver1_ssh = SshServiceDetails(
    addr="10.0.176.27", username="MN5GRAN", password="nokia123@"
)

_appserver2_ssh = SshServiceDetails(
    addr="10.0.176.18", username="MN5GRAN", password="nokia123@"
)

# ${EPC_IP}=${tl.appserver.iperf_details.network_interface_address}
_iperf_details_on_appserver1 = IperfDataTransferDetails(
    ssh_connection_details=_appserver1_ssh,
    network_interface_address="10.71.207.142",
    iperf_path="/usr/bin/iperf",
    port=51001,
)

_iperf_details_on_appserver2 = IperfDataTransferDetails(
    ssh_connection_details=_appserver2_ssh,
    network_interface_address="10.71.207.142",
    iperf_path="/usr/bin/iperf",
    port=51001,
)

_appserver1 = AppServer(_iperf_details_on_appserver1)
_appserver2 = AppServer(_iperf_details_on_appserver2)

# DL traffic:  ${tl.ues[${ue_index}].iperf_details.port}
_appserver_ssh1 = SshServiceDetails(
    addr="10.71.207.142",
    username="vrf4_sg1",
    password="vrf4@sg1",
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh1,
    network_interface_address="10.71.207.142",
    iperf_path="iperf",
    port=51001,
)

_appserver_ssh2 = SshServiceDetails(
    addr="10.71.207.142",
    username="vrf4_sg1",
    password="vrf4@sg1",
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh2,
    network_interface_address="10.71.207.142",
    iperf_path="iperf",
    port=51001,
)

# spark license
_licensekeeper = LicenseKeeper(username="HAZ4_SG1", password="HAZ4_SG1")


# SA   CI_Detail_UE_Type='Huawei Mate 30 Pro 5G'
_sigspark1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.0.176.27", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="9YS0220217010002",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.48/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="460023032997011",
    capabilities=["huawei_sigspark"],
    licensekeeper=_licensekeeper,
)

_sigspark2 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.0.176.18", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="9YS0220103005660",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.45/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="460023100010180",
    capabilities=["huawei_sigspark"],
    licensekeeper=_licensekeeper,
)

# TestLine
tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    tl_cloud_topology="CLOUD_5G_AIC_OCP",
    ues=[_sigspark1,_sigspark2],
    appserver=[_appserver1,_appserver2]
)

__all__ = ["tl"]
