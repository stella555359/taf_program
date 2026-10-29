__maintainer__ = "Dong Tingting"
__team__ = "MN_RAN_RD_VRF_HAZ3_02"
__email__ = "tingting.dong@nokia-sbell.com"

import os
from taf.config.testline.appserver import AppServer
from taf.config.testline import (
    CloudDeployment,
    DeploymentNetworkStack,
    DeploymentVnfStack,
    MasterNode,
    K8S,
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
from taf.config.testline.pdu import FPFH
from taf.config.testline import RU, RadioTypes
from taf.config.testline import CloudBts, CU
from taf.config.testline import VDU, FHGW
from taf.config.testline import PxeServer
from taf.config.testline import TestLine
from taf.config.testline import TestPc
from taf.config.testline.nms import NetAct

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# Testpc
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.159.86", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# CU
_cu = CU(
    instance_id=37200,
    global_bts_id=37200,
    backhaul_site_oam_ip=NetworkAddress(v4="10.57.173.16"),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.171.130", username="tl177", password="systeM!23"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.173.16", username="Nemuadmin", password="Nokia@123", port=443
    ),
    f1c=NetworkAddress(
        v4="10.57.174.28",
        vlan_id=2559,
        routing_v4=RoutingInformation(gateway="10.57.174.1", ip_prefix_length=26),
    ),
    f1u=NetworkAddress(
        v4="10.57.174.29",
        vlan_id=2559,
        routing_v4=RoutingInformation(gateway="10.57.174.1", ip_prefix_length=26),
    ),
    ngc=NetworkAddress(
        v4="10.57.174.156",
        vlan_id=2561,
        routing_v4=RoutingInformation(gateway="10.57.174.129", ip_prefix_length=26),
    ),
    ngu=NetworkAddress(
        v4="10.57.174.157",
        vlan_id=2561,
        routing_v4=RoutingInformation(gateway="10.57.174.129", ip_prefix_length=26),
    ),
    x2c=NetworkAddress(
        v4="10.57.174.92",
        vlan_id=2560,
        routing_v4=RoutingInformation(gateway="10.57.174.65", ip_prefix_length=26),
    ),
    x2u=NetworkAddress(
        v4="10.57.174.93",
        vlan_id=2560,
        routing_v4=RoutingInformation(gateway="10.57.174.65", ip_prefix_length=26),
    ),
    s1u=NetworkAddress(
        v4="10.57.173.49",
        vlan_id=2552,
        routing_v4=RoutingInformation(gateway="10.57.173.33", ip_prefix_length=27),
    ),
    tracing=None,
)

# cloud_deployment for vCU
_vcu_cnf_1 = DeploymentVnfStack(
    name="vcutest",
    yaml_file=os.path.join(_cfg_dir, "DEP/gnbs_0/vCU/CU_cnf_values-override.yaml"),
)
_vcu_intnet_1 = DeploymentNetworkStack(
    name=_vcu_cnf_1.name + "-prerequisite",
    yaml_file=os.path.join(_cfg_dir, "DEP/gnbs_0/vCU/CU_pvc_values-override.yaml"),
)

# ssh connection information of OE, for tenant user
_vcu_ssh_connection_details = SshServiceDetails(
    addr="10.57.171.130", username="tl177", password="systeM!23", port=22
)
# ssh connection information of OE, for root user
_vcu_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.57.171.130", username="tl177", password="systeM!23", port=22
)

_vcu_master_node = MasterNode(
    k8s_connection_details=_vcu_k8s_connection_details,
    ssh_connection_details=_vcu_ssh_connection_details,
)

_vcu_k8s = K8S(namespace="tl177", master_node=_vcu_master_node)

_vcu_k8s_cloud_deployment = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    networks=[_vcu_intnet_1],
    vnfs=[_vcu_cnf_1],
    cloud_hosting=_vcu_k8s,
)


# 5G RU
_ru_pdu1 = FPFH(addr="10.71.196.76", port_numbers=[5])

_ru1 = RU(
    ru_hw_group="Below6GHz",
    pdu_port=_ru_pdu1.pdu_ports[5],
    radio_type=RadioTypes.AVQE,
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.37",
        username="rfsw",
        password="f6gh0K2nXq0O8XqVFkUuMtJnzuKm0U3box0QcYgugn0=",
    ),
)

_ru_pdu2 = FPFH(addr="10.71.196.76", port_numbers=[4])

_ru2 = RU(
    ru_hw_group="Below6GHz",
    pdu_port=_ru_pdu2.pdu_ports[4],
    radio_type=RadioTypes.AQQC,
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.36",
        username="rfsw",
        password="3Is6ezFJ7dFlB29cgs0yp3RCM3fUF1zNO1+6Z08tlAc=",
    ),
)
# vDU information
_IP_pxe="10.71.220.62"
_pxe_server_ssh_info = SshServiceDetails(
    addr=_IP_pxe, username="root", password="uteadmin"
)
_pxe_server = PxeServer(
    nfs_ip=_IP_pxe, ssh_connection_details=_pxe_server_ssh_info
)

# FHGW information
_fhgw_0 = FHGW(user_config_path=_cfg_dir, rus=[_ru1], pxe_server=_pxe_server)
_fhgw_0.ip = "10.71.222.147"
_fhgw_0.username = "toor4nsn"
_fhgw_0.password = "Fhgw@nokia123"
_fhgw_0.version = "FHGW24R2"

# OE information
_IP_OCP="10.64.170.226"
_ssh_connection_details_0 = SshServiceDetails(
    addr=_IP_OCP, username="core", password="system123"
)
_k8s_connection_details_0 = K8SConnectionDetails(
    ip_addr=_IP_OCP, username="core", password="system123", port="22"
)

_master_node_0 = MasterNode(
    k8s_connection_details=_k8s_connection_details_0,
    ssh_connection_details=_ssh_connection_details_0,
)
_k8s_0 = K8S(namespace="tl177", master_node=_master_node_0)
_vdu_cnf_0 = DeploymentVnfStack(
    name="vdutest",
    yaml_file=os.path.join(_cfg_dir, "DEP/gnbs_0/vDU_0/DU_cnf_values-override.yaml"),
)
_vdu_intnet_0 = DeploymentNetworkStack(
    name=_vdu_cnf_0.name + "-prerequisite",
    yaml_file=os.path.join(_cfg_dir, "DEP/gnbs_0/vDU_0/DU_pvc_values-override.yaml"),
)

_vdu_k8s_cloud_deployment_0 = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    cloud_hosting=_k8s_0,
    networks=[_vdu_intnet_0],
    vnfs=[_vdu_cnf_0],
)


_du_0 = VDU(
    cloud_deployment=_vdu_k8s_cloud_deployment_0,
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.64.170.250", username="Nemuadmin", password="Nokia@123"
    ),
    fhgws=[_fhgw_0],
    instance_id=37200,
    global_bts_id=37200,
)

# BTS
_cbts = CloudBts(
    dus=[_du_0],
    cu=_cu,
    cloud_deployment=_vcu_k8s_cloud_deployment,
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
    port=43177,
)

_appserver = AppServer(_iperf_details_on_appserver1)

_ue_host_ssh = SshServiceDetails(addr="10.71.218.253", username="nokia5G", password="noki@123")

_licensekeeper = LicenseKeeper(username="HAZ3_SG2", password="HAZ3_SG2")



_IMSI_1="262033100001080"
# C:\Program Files (x86)\Spark1.1.2008.3\Bin\Spark.exe
_spark_server_dir="C:/Program Files (x86)/Spark1.1.2009.11/Bin/Spark.exe"
# _spark_server_dir="/cygdrive/c/Program Files (x86)/Spark1.1.2008.3/Bin/Spark.exe"

_sigspark_1 = Android(
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
    tl_cloud_topology="CLOUD_5G_AIC_RM17_OCP_FHGW_AVQE_AQQC",
    ues=[_sigspark_1],
    appserver=_appserver,
)

__all__ = ["tl"]
