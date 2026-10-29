__maintainer__ = "Lusha Zhang"
__team__ = "VRF_HAZ3_T02"
__email__ = "lusha.zhang@nokia-sbell.com"

import os
from taf.config.testline.appserver import AppServer
from taf.config.testline import (
    CloudDeployment,
    DeploymentNetworkStack,
    DeploymentVnfStack,
    MasterNode,
    K8S,
    HelmChart,
)
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
    K8SConnectionDetails,
)
from taf.config.testline.ue import (
    AirphoneCloud,
    Airphone,
    Prisma,
    TM500,
    Qualcomm,
    QualcommUeType,
    Android,
)  # added in taf.meta.5.4
from taf.config.testline import NetworkAddress, RoutingInformation, LicenseKeeper
from taf.config.testline import RealEnb, Airscale, CommonUnit
from taf.config.testline import HBTE_PDU as HBTE
from taf.config.testline import RU, RadioTypes
from taf.config.testline import CloudBts, CU
from taf.config.testline import VDU, FHGW, RANNIC
from taf.config.testline import PxeServer
from taf.config.testline import TestLine
from taf.config.testline import TestPc
from taf.config.testline.nms import NetAct

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# Testpc
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.159.144", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# CU
_cu = CU(
    instance_id=37361,
    global_bts_id=37361,
    backhaul_site_oam_ip=NetworkAddress(v4="10.57.165.7"),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.165.130", username="cranuser190", password="systeM!23"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.165.7", username="Nemuadmin", password="nemuuser", port=443
    ),
    f1c=NetworkAddress(
        v4="10.57.166.10",
        vlan_id=2689,
        routing_v4=RoutingInformation(gateway="10.57.166.0/26"),
    ),
    f1u=NetworkAddress(
        v4="110.57.166.11",
        vlan_id=2689,
        routing_v4=RoutingInformation(gateway="10.57.166.0/26"),
    ),
    ngc=NetworkAddress(
        v4="10.57.166.138",
        vlan_id=2691,
        routing_v4=RoutingInformation(gateway="10.57.166.128/26"),
    ),
    ngu=NetworkAddress(
        v4="10.57.166.139",
        vlan_id=2691,
        routing_v4=RoutingInformation(gateway="10.57.166.128/26"),
    ),
    x2c=NetworkAddress(
        v4="10.57.166.74",
        vlan_id=2690,
        routing_v4=RoutingInformation(gateway="10.57.182.64/26"),
    ),
    x2u=NetworkAddress(
        v4="10.57.166.75",
        vlan_id=2690,
        routing_v4=RoutingInformation(gateway="10.57.182.64/26"),
    ),
    s1u=NetworkAddress(
        v4="10.57.165.39",
        vlan_id=2682,
        routing_v4=RoutingInformation(gateway="10.57.165.32/27"),
    ),
    tracing=NetworkAddress(
        v4="10.57.165.71",
        vlan_id=2683,
        routing_v4=RoutingInformation(gateway="10.57.165.64/27"),
    ),
)

# cloud_deployment for vCU

# ssh connection information of OE, for tenant user
_vcu_ssh_connection_details = SshServiceDetails(
    addr="10.57.165.130", username="cranuser190", password="systeM!23", port=22
)
# ssh connection information of OE, for root user
_vcu_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.57.165.130", username="core", password="system123", port=22
)

_vcu_master_node = MasterNode(
    k8s_connection_details=_vcu_k8s_connection_details,
    ssh_connection_details=_vcu_ssh_connection_details,
)

_vcu_k8s = K8S(namespace="cran190", master_node=_vcu_master_node)

_cnf_cu_1 = HelmChart(
    name="vcu190",
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
_ru_pdu1 = HBTE(addr="10.57.243.14", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru1 = RU(
    ru_hw_group="hw_group",
    pdu_port=_ru_pdu1.pdu_ports[4],
    radio_type=RadioTypes.AEQY,
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.43",
        username="serviceuser",
        password="bobuWrUHk7Xq7WPpY9ZcjEi8zNdX3plZ+/y420RZ7W4=",
    ),
)

_ru_pdu2 = HBTE(addr="10.57.243.14", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru2 = RU(
    ru_hw_group="hw_group",
    pdu_port=_ru_pdu1.pdu_ports[5],
    radio_type=RadioTypes.AQQJ,
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.42",
        username="rfsw",
        password="3Is6ezFJ7dFlB29cgs0yp3RCM3fUF1zNO1+6Z08tlAc=",
    ),
)

_ru_pdu3 = HBTE(addr="10.57.243.14", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru3 = RU(
    ru_hw_group="hw_group",
    pdu_port=_ru_pdu1.pdu_ports[3],
    radio_type=RadioTypes.AVQE,
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.49",
        username="rfsw",
        password="f6gh0K2nXq0O8XqVFkUuMtJnzuKm0U3box0QcYgugn0=",
    ),
)

_ru_pdu4 = HBTE(addr="10.57.243.150", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru4 = RU(
    ru_hw_group="hw_group",
    pdu_port=_ru_pdu1.pdu_ports[5],
    radio_type=RadioTypes.AVQL,
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.46",
        username="rfsw",
        password="f6gh0K2nXq0O8XqVFkUuMtJnzuKm0U3box0QcYgugn0=",
    ),
)

_ru_pdu5 = HBTE(addr="10.57.243.150", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru5 = RU(
    ru_hw_group="hw_group",
    pdu_port=_ru_pdu1.pdu_ports[6],
    radio_type=RadioTypes.AQQC,
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.35",
        username="rfsw",
        password="3Is6ezFJ7dFlB29cgs0yp3RCM3fUF1zNO1+6Z08tlAc=",
    ),
)

_ru_pdu6 = HBTE(addr="10.57.172.70", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru6 = RU(
    ru_hw_group="hw_group",
    pdu_port=_ru_pdu1.pdu_ports[1],
    radio_type=RadioTypes.AEQY,
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.36",
        username="serviceuser",
        password="bobuWrUHk7Xq7WPpY9ZcjEi8zNdX3plZ+/y420RZ7W4=",
    ),
)

# RANNIC information
_rannic_0 = RANNIC(
    serial_number="L1240913780",
    product_code="AF1791.A101",
    rus=[_ru1, _ru2, _ru3, _ru4, _ru5, _ru6],
)

# vDU
_ssh_connection_details_0 = SshServiceDetails(
    addr="10.57.246.74", username="cranuser190", password="systeM!23"
)
_k8s_connection_details_0 = K8SConnectionDetails(
    ip_addr="10.57.246.74", username="core", password="system123", port="22"
)

_master_node_0 = MasterNode(
    k8s_connection_details=_k8s_connection_details_0,
    ssh_connection_details=_ssh_connection_details_0,
)
_k8s_0 = K8S(namespace="cran190", master_node=_master_node_0)
_vdu_cnf_0 = DeploymentVnfStack(
    name="vdu190",
    yaml_file=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/du_cnf_values-override.yaml"
    ),
)
_vdu_intnet_0 = DeploymentNetworkStack(
    name=_vdu_cnf_0.name + "-prerequisite",
    yaml_file=os.path.join(_cfg_dir, "DEP/gnbs_0/vDU_0/DU_pvc_values-override.yaml"),
)

_cnf_du_0 = HelmChart(
    name="vdu190",
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
        addr="10.57.197.178", username="Nemuadmin", password="nemuuser", port="443"
    ),
    rannics=[_rannic_0],
    instance_id=37361,
    global_bts_id=37361,
)

# BTS
_cbts = CloudBts(
    dus=[_du_0],
    cu=_cu,
    cloud_deployment=_vcu_k8s_cloud_deployment,
)

# #######Iperf########
_appserver_ssh_1 = SshServiceDetails(
    addr="10.57.162.2", username="mmw_sg2", password="mm@2", port="43190"
)

_iperf_1 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh_1,
    network_interface_address="10.57.162.2",
    iperf_path="/system/bin",
    port=42191,
)

_iperf_details = _iperf_1
_appserver = AppServer(_iperf_details)

# Netact
_netact = NetAct(
    https_main_info=HttpConnectionDetails(
        addr="10.82.47.15", username="omc", password="Medsql!_1893"
    ),
)

# SIGSPARK
_appserver_ip_addr1 = "10.71.219.22"

_spark_appserver_ssh1 = SshServiceDetails(
    addr=_appserver_ip_addr1, username="mmw_sg2", password="mm@2"
)

_iperf_details_on_appserver1 = IperfDataTransferDetails(
    ssh_connection_details=_spark_appserver_ssh1,
    network_interface_address=_appserver_ip_addr1,
    iperf_path="iperf",
    port=42179,
)

_appserver = AppServer(_iperf_details_on_appserver1)

_ue_host_ssh = SshServiceDetails(addr="10.57.147.2", username="spark", password="spark")

_licensekeeper = LicenseKeeper(username="HAZ3_SG2", password="HAZ3_SG2")

##need update
_IMSI_1 = "262033100010761"
# C:\Program Files (x86)\Spark1.1.2008.3\Bin\Spark.exe
_spark_server_dir = "C:/Program Files (x86)/Spark1.1.2009.15/Bin/Spark.exe"
# _spark_server_dir="/cygdrive/c/Program Files (x86)/Spark1.1.2008.3/Bin/Spark.exe"

_sigspark1 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="072010332336005",
    server_dir=_spark_server_dir,
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver1,
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "huawei_sigspark"],
    imsi=_IMSI_1,
    licensekeeper=_licensekeeper,
)

# TestLine
tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    tl_cloud_topology="CLOUD_5G_AIC_RM17_OCP_FHGW_AEQP_AHPE",
    ues=[_sigspark1],
    nms=_netact,
    appserver=_appserver,
)

__all__ = ["tl"]
