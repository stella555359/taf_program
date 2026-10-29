__maintainer__ = "li yajie"
__team__ = "RAN_PZ_HAZ4_SG01"
__email__ = "yajie.li@nokia-sbell.com"

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
from taf.config.testline.pdu import HBTE as PBHBTE
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
        addr="10.57.155.48", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# CU
_cu = CU(
    instance_id=1126,
    global_bts_id=10550,
    backhaul_site_oam_ip=NetworkAddress(v4="10.57.179.8"),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.138.34", username="core", password="system123"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.179.8", username="Nemuadmin", password="Nokia@123", port=443
    ),
    x2c=NetworkAddress(
        v4="10.57.180.76",
        vlan_id=2670,
        routing=RoutingInformation(gateway="10.57.180.65", ip_prefix_length=26),
    ),
    f1c=NetworkAddress(
        v4="10.57.180.12",
        vlan_id=2669,
        routing=RoutingInformation(gateway="10.57.180.1", ip_prefix_length=26),
    ),
    f1u=NetworkAddress(
        v4="10.57.180.13",
        vlan_id=2669,
        routing=RoutingInformation(gateway="10.57.180.1", ip_prefix_length=26),
    ),
    s1u=NetworkAddress(
        v4="10.57.179.40",
        vlan_id=2662,
        routing=RoutingInformation(gateway="10.57.179.33", ip_prefix_length=27),
    ),
    x2u=NetworkAddress(
        v4="10.57.173.161",
        vlan_id=2670,
        routing=RoutingInformation(gateway="10.57.180.65", ip_prefix_length=26),
    ),
    tracing=None,
)

# cloud_deployment for vCU
_vcu_cnf_1 = DeploymentVnfStack(
    name="vcu1126",
    yaml_file=os.path.join(_cfg_dir, "DEP/gnbs_0/vCU/CU_cnf_values-override.yaml"),
)
_vcu_intnet_1 = DeploymentNetworkStack(
    name=_vcu_cnf_1.name + "-prerequisite",
    yaml_file=os.path.join(_cfg_dir, "DEP/gnbs_0/vCU/CU_pvc_values-override.yaml"),
)

# ssh connection information of OE, for tenant user
_vcu_ssh_connection_details = SshServiceDetails(
    addr="10.57.138.34", username="core", password="system123", port=22
)

# ssh connection information of OE, for root user
_vcu_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.57.138.34", username="core", password="system123", port=22
)

_vcu_master_node = MasterNode(
    k8s_connection_details=_vcu_k8s_connection_details,
    ssh_connection_details=_vcu_ssh_connection_details,
)

_vcu_k8s = K8S(namespace="tl1126", master_node=_vcu_master_node)

_vcu_k8s_cloud_deployment = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    networks=[_vcu_intnet_1],
    vnfs=[_vcu_cnf_1],
    cloud_hosting=_vcu_k8s,
)


# 5G RU
_ru_pdu = PBHBTE(addr="10.71.197.38", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_ru2_pdu = PBHBTE(addr="10.71.197.40", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru = RU(
    ru_hw_group="hw_group",
    pdu_port=_ru_pdu.pdu_ports[4],
    radio_type=RadioTypes.AEQE,
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.35",
        username="serviceuser",
        password="bobuWrUHk7Xq7WPpY9ZcjEi8zNdX3plZ+/y420RZ7W4=",
    ),
)

_ru2 = RU(
    ru_hw_group="hw_group",
    pdu_port=_ru2_pdu.pdu_ports[2],
    radio_type=RadioTypes.AEQE,
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.36",
        username="serviceuser",
        password="bobuWrUHk7Xq7WPpY9ZcjEi8zNdX3plZ+/y420RZ7W4=",
    ),
)


# FHGW information
_pxe_server_ssh_info = SshServiceDetails(
    addr="0.0.0.0", username="root", password="centos"
)
_pxe_server = PxeServer(nfs_ip="0.0.0.0", ssh_connection_details=_pxe_server_ssh_info)

_fhgw_0 = FHGW(user_config_path=_cfg_dir, rus=[_ru, _ru2], pxe_server=_pxe_server)
_fhgw_0.ip = "10.71.222.147"
_fhgw_0.username = "toor4nsn"
_fhgw_0.password = "Fhgw@nokia123"
_fhgw_0.version = "22R3"


# vDU
_ssh_connection_details_0 = SshServiceDetails(
    addr="10.71.222.162", username="core", password="system123"
)
_k8s_connection_details_0 = K8SConnectionDetails(
    ip_addr="10.71.222.162", username="core", password="system123", port="22"
)

_master_node_0 = MasterNode(
    k8s_connection_details=_k8s_connection_details_0,
    ssh_connection_details=_ssh_connection_details_0,
)

_k8s_0 = K8S(namespace="cran1", master_node=_master_node_0)
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
        addr="10.71.223.26", username="Nemuadmin", password="Nokia@123"
    ),
    fhgws=[_fhgw_0],
    instance_id=1126,
    global_bts_id=10550,
)

# BTS
_cbts = CloudBts(
    dus=[_du_0],
    cu=_cu,
    cloud_deployment=_vcu_k8s_cloud_deployment,
)

# ENB
_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.71.215.9", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(
    airscale=_real_enb,
    oam_ip="10.71.215.9",
    global_bts_id="1124",
)


_attenuator_RU1 = HBTE(
    ip_addr="10.71.206.130",
    port=5000,
    attenuation_port_numbers=[13, 14, 15, 16],
    model="PA-16-16-6-127-0.5-B-S",
)

_attenuator_RU2 = HBTE(
    ip_addr="10.71.206.131",
    port=5000,
    attenuation_port_numbers=[1, 2, 3, 4],
    model="PA-16-16-6-127-0.5-B-S",
)


# UE samsung
# UL traffic: ${tl.appserver.iperf_details.port}

_appserver2_ssh = SshServiceDetails(
    addr="10.71.217.132", username="nokia5G", password="noki@123"
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

## UE
_samsung = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.217.132", username="nokia5G", password="noki@123"
    ),
    serial_number="R5CR205EQ4P",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="310260100008781",
    capabilities=["REAL_ANDROID_UE", "samsung_vran20"],
    licensekeeper=_licensekeeper,
)


# SA   CI_Detail_UE_Type='Huawei Mate 30 Pro 5G'
# Lower priority UE
_sigspark = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.217.132", username="nokia5G", password="noki@123"
    ),
    serial_number="9YS0220114010320",
    server_dir="C:/Program Files (x86)/Spark/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="460023100010658",
    capabilities=["huawei_sigspark"],
    licensekeeper=_licensekeeper,
)


# SA   CI_Detail_UE_Type='Huawei Mate 30 Pro 5G'
# Higher priority UE
_2_sigspark = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.217.132", username="nokia5G", password="noki@123"
    ),
    serial_number="9YS0220103031558",
    server_dir="C:/Program Files (x86)/Spark/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="460023100010642",
    capabilities=["huawei_sigspark"],
    licensekeeper=_licensekeeper,
)


# NSA  CI_Detail_UE_Type='Huawei Mate 30PRO'
_3_sigspark = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.217.132", username="nokia5G", password="noki@123"
    ),
    serial_number="9YS0220721008832",
    server_dir="C:/Program Files (x86)/Spark/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="460023100010647",
    capabilities=["huawei_sigspark"],
    licensekeeper=_licensekeeper,
)

# TestLine
tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    tl_cloud_topology="CLOUD_5G_AIC_RM17_OCP_FHGW_AEQE",
    enbs=[_lte_real_enb],
    ues=[_sigspark, _2_sigspark, _3_sigspark],
    attenuators=[_attenuator_RU1, _attenuator_RU2],
    appserver=_appserver,
)

__all__ = ["tl"]
