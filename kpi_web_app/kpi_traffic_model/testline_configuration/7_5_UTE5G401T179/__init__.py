__maintainer__ = "jiangrong wang"
__team__ = "VRF_HAZ3_T02"
__email__ = "jiangrong.wang@nokia-sbell.com"

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
from taf.config.testline import RU, RadioTypes
from taf.config.testline import CloudBts, CU
from taf.config.testline import VDU, FHGW
from taf.config.testline import PxeServer
from taf.config.testline import TestLine
from taf.config.testline import TestPc
from taf.config.testline.nms import NetAct
from taf.config.testline.ue import MediaTek, TafUeFastmile
from taf.config.testline.pdn import PDN, PDPTypes
from taf.config.testline.connection_details import (
    SshServiceDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.appserver import AppServer, TafUeAppServer
from taf.config.testline.taf_ue_data_transfer_protocol import TafUeDataTransferProtocol

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# Testpc
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.159.89", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# CU
_cu = CU(
    instance_id=37314,
    global_bts_id=37314,
    backhaul_site_oam_ip=NetworkAddress(v4="10.57.158.144"),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.158.2", username="cranuser179", password="systeM!23"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.158.144", username="Nemuadmin", password="Nokia@123", port=443
    ),
    f1c=NetworkAddress(
        v4="110.57.168.28",
        vlan_id=109,
        routing=RoutingInformation(gateway="10.57.168.1", ip_prefix_length=26),
    ),
    f1u=NetworkAddress(
        v4="10.57.168.29",
        vlan_id=109,
        routing=RoutingInformation(gateway="10.57.168.1", ip_prefix_length=26),
    ),
    ngc=NetworkAddress(
        v4="10.57.168.156",
        vlan_id=111,
        routing=RoutingInformation(gateway="10.57.168.129", ip_prefix_length=26),
    ),
    ngu=NetworkAddress(
        v4="10.57.168.157",
        vlan_id=111,
        routing=RoutingInformation(gateway="10.57.168.129", ip_prefix_length=26),
    ),
    x2c=NetworkAddress(
        v4="10.57.168.92",
        vlan_id=110,
        routing_v4=RoutingInformation(gateway="10.57.168.64/26"),
    ),
    x2u=NetworkAddress(
        v4="10.57.168.93",
        vlan_id=110,
        routing_v4=RoutingInformation(gateway=" 10.57.168.64/26"),
    ),
    s1u=NetworkAddress(
        v4="10.57.158.48",
        vlan_id=102,
        routing_v4=RoutingInformation(gateway="10.57.158.32/27"),
    ),
    tracing=None,
)

# cloud_deployment for vCU
_vcu_cnf_1 = DeploymentVnfStack(
    name="vcu179",
    yaml_file=os.path.join(_cfg_dir, "DEP/gnbs_0/vCU/CU_cnf_values-override.yaml"),
)
_vcu_intnet_1 = DeploymentNetworkStack(
    name=_vcu_cnf_1.name + "-prerequisite",
    yaml_file=os.path.join(_cfg_dir, "DEP/gnbs_0/vCU/CU_pvc_values-override.yaml"),
)

# ssh connection information of OE, for tenant user
_vcu_ssh_connection_details = SshServiceDetails(
    addr="10.57.158.2", username="cranuser179", password="systeM!23", port=22
)
# ssh connection information of OE, for root user
_vcu_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.57.158.2", username="cranuser179", password="systeM!23", port=22
)

_vcu_master_node = MasterNode(
    k8s_connection_details=_vcu_k8s_connection_details,
    ssh_connection_details=_vcu_ssh_connection_details,
)

_vcu_k8s = K8S(namespace="tl179", master_node=_vcu_master_node)

_vcu_k8s_cloud_deployment = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    networks=[_vcu_intnet_1],
    vnfs=[_vcu_cnf_1],
    cloud_hosting=_vcu_k8s,
)


# 5G RU
_ru_pdu1 = HBTE(addr="10.71.196.10", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru1 = RU(
    ru_hw_group="hw_group",
    pdu_port=_ru_pdu1.pdu_ports[6],
    radio_type=RadioTypes.AEQY,
    default_ssh_connection_details=SshServiceDetails(
        addr="10.71.196.10",
        username="serviceuser",
        password="bobuWrUHk7Xq7WPpY9ZcjEi8zNdX3plZ+/y420RZ7W4=",
    ),
)

# vDU
_pxe_server_ssh_info = SshServiceDetails(
    addr="10.57.134.238", username="ute", password="Ut3pa5s#ff97"
)
_pxe_server = PxeServer(
    nfs_ip="10.57.134.238", ssh_connection_details=_pxe_server_ssh_info
)

# FHGW information
_fhgw_0 = FHGW(user_config_path=_cfg_dir, rus=[_ru1], pxe_server=_pxe_server)
_fhgw_0.ip = "10.57.134.246"
_fhgw_0.username = "toor4nsn"
_fhgw_0.password = "Fhgw@nokia123"
_fhgw_0.version = "24R2"

_ssh_connection_details_0 = SshServiceDetails(
    addr="10.57.137.186", username="core", password="system123"
)
_k8s_connection_details_0 = K8SConnectionDetails(
    ip_addr="10.57.137.186", username="core", password="system123", port="22"
)

_master_node_0 = MasterNode(
    k8s_connection_details=_k8s_connection_details_0,
    ssh_connection_details=_ssh_connection_details_0,
)
_k8s_0 = K8S(namespace="cran179", master_node=_master_node_0)
_vdu_cnf_0 = DeploymentVnfStack(
    name="vdu179",
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
        addr="10.57.197.18", username="Nemuadmin", password="Nokia@123"
    ),
    fhgws=[_fhgw_0],
    instance_id=37314,
    global_bts_id=37314,
)

# BTS
_cbts = CloudBts(
    dus=[_du_0],
    cu=_cu,
    cloud_deployment=_vcu_k8s_cloud_deployment,
)

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.71.211.99", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(
    airscale=_real_enb,
    oam_ip="10.71.211.99",
    global_bts_id="179",
)

# #######Iperf########
_appserver_ssh_1 = SshServiceDetails(
    addr="10.57.191.195", username="vrf3_sg2", password="vrf3@sg2", port="43172"
)

_iperf_1 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh_1,
    network_interface_address="10.57.191.195",
    iperf_path="iperf",
    port=42172,
)


# Qualcomm
# CI_Detail_UE_Type='Qualcomm'
_android_1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.217.113", username="nokia5G", password="noki@123"
    ),
    serial_number="R5CR111A94N",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf_1,
    capabilities=["samsung_vran20"],
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
_appserver_ip_addr1 = "10.71.207.155"

_spark_appserver_ssh1 = SshServiceDetails(
    addr=_appserver_ip_addr1, username="vrf3_sg2", password="vrf3@sg2"
)

_iperf_details_on_appserver1 = IperfDataTransferDetails(
    ssh_connection_details=_spark_appserver_ssh1,
    network_interface_address=_appserver_ip_addr1,
    iperf_path="iperf",
    port=42179,
)

_appserver = AppServer(_iperf_details_on_appserver1)

_ue_host_ssh = SshServiceDetails(
    addr="10.57.150.192", username="nokia5G", password="noki@123"
)

_licensekeeper = LicenseKeeper(username="HAZ3_SG2", password="HAZ3_SG2")


_IMSI_1 = "262033100010761"
# C:\Program Files (x86)\Spark1.1.2008.3\Bin\Spark.exe
_spark_server_dir = "C:/Program Files (x86)/Spark1.1.2009.15/Bin/Spark.exe"
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

# UE-2 cell-5 PCI-54 AQQJ CPE
_fastmile_appserver_1 = TafUeAppServer(
    app_server_name="APP_SERVER_1",
    address="10.57.191.234",
    user="vrf3_sg2",
    password="vrf3@sg2",
    bind_interface_ip="10.57.191.234",
    expected_prompt="[vrf3_sg2@appserver ~]$",
    binary_path="/usr/bin/iperf",
    ports=[42179, 43179],
)


_fastmile_data_transfer_1 = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_fastmile_appserver_1,
    interval=1,
    binary_path="iperf",
    version=1,
)

_fastmile_1 = TafUeFastmile(
    com_port="4",
    ue_pc_address="10.57.150.221",
    root_password="76ea79a242d4",
    ue_manage_ip="192.168.1.1",
    serial_number="LPL221400489",
    data_transfer=[_fastmile_data_transfer_1],
    ue_pc_port=6179,
    version="3.2",
    capabilities=["REAL_FASTMILE_UE1", "nokia_fastmile"],
)

# TestLine
tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    tl_cloud_topology="CLOUD_5G_AIC_RM17_OCP_FHGW_AEQP_AHPE",
    # enbs=[_lte_real_enb],
    ues=[_sigspark_1, _fastmile_1],
    nms=_netact,
    appserver=_appserver,
)

__all__ = ["tl"]
