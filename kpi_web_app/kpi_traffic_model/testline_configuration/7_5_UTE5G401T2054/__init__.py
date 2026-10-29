__maintainer__ = "LiYing"
__team__ = "RAN_PZ_HAZ3_SG03"
__email__ = "ying.15.li@nokia-sbell.com"

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
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.core import RealCore, PCF
from taf.config.testline import NetworkAddress, RoutingInformation
from taf.config.testline import RealEnb, Airscale, CommonUnit
from taf.config.testline import HBTE_PDU as HBTE
from taf.config.testline import RU, RadioTypes
from taf.config.testline import CloudBts, CU
from taf.config.testline import VDU, FHGW
from taf.config.testline import PxeServer
from taf.config.testline import TestLine
from taf.config.testline import RealEnb
from taf.config.testline import TestPc
from taf.config.testline.ue import Android
from taf.config.testline.nms import Netact
from taf.config.testline.appserver import AppServer

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# Testpc
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.107", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# CU
_cu = CU(
    instance_id=2054,
    global_bts_id=2054,
    backhaul_site_oam_ip=NetworkAddress(v4="10.57.173.15"),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.171.130", username="tl2054", password="systeM!23"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.173.15", username="Nemuadmin", password="Nokia@123", port=443
    ),
    x2c=NetworkAddress(
        v4="10.57.174.90",
        vlan_id=2560,
        routing=RoutingInformation(gateway="10.57.174.65", ip_prefix_length=26),
    ),
    f1c=NetworkAddress(
        v4="10.57.174.26",
        vlan_id=2559,
        routing=RoutingInformation(gateway="10.57.174.1", ip_prefix_length=26),
    ),
    f1u=NetworkAddress(
        v4="10.57.174.27",
        vlan_id=2559,
        routing=RoutingInformation(gateway="10.57.174.1", ip_prefix_length=26),
    ),
    s1u=NetworkAddress(
        v4="10.57.173.47",
        vlan_id=2552,
        routing=RoutingInformation(gateway="10.57.173.33", ip_prefix_length=26),
    ),
    x2u=NetworkAddress(
        v4="10.57.174.91",
        vlan_id=2560,
        routing=RoutingInformation(gateway="10.57.174.65", ip_prefix_length=26),
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
    addr="10.57.171.130", username="tl2054", password="systeM!23", port=22
)
# ssh connection information of OE, for root user
_vcu_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.57.171.130", username="tl2054", password="systeM!23", port=22
)

_vcu_master_node = MasterNode(
    k8s_connection_details=_vcu_k8s_connection_details,
    ssh_connection_details=_vcu_ssh_connection_details,
)

_vcu_k8s = K8S(namespace="tl2054", master_node=_vcu_master_node)

_vcu_k8s_cloud_deployment = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    networks=[_vcu_intnet_1],
    vnfs=[_vcu_cnf_1],
    cloud_hosting=_vcu_k8s,
)


# 5G RU
_ru_pdu = HBTE(addr="10.71.195.120", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru = RU(
    ru_hw_group="hw_group",
    pdu_port=_ru_pdu.pdu_ports[1],
    radio_type=RadioTypes.AEQY,
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.35",
        username="rfsw",
        password="5rfS2qmWC0AiFYvir7k8JekCN8/NklqDK5E6OWXuUVQ=",
    ),
)

# vDU
_pxe_server_ssh_info = SshServiceDetails(
    addr="10.71.223.254", username="ute", password="!Q2w3e4r5t6y7u"
)
_pxe_server = PxeServer(
    nfs_ip="10.71.223.254", ssh_connection_details=_pxe_server_ssh_info
)

# FHGW information
_fhgw_0 = FHGW(user_config_path=_cfg_dir, rus=[_ru], pxe_server=_pxe_server)
_fhgw_0.ip = "10.71.222.155"
_fhgw_0.username = "toor4nsn"
_fhgw_0.password = "Fhgw@nokia123"
_fhgw_0.version = "22R2"

_ssh_connection_details_0 = SshServiceDetails(
    addr="10.64.163.162", username="core", password="system123"
)
_k8s_connection_details_0 = K8SConnectionDetails(
    ip_addr="10.64.163.162", username="core", password="system123", port="22"
)

_master_node_0 = MasterNode(
    k8s_connection_details=_k8s_connection_details_0,
    ssh_connection_details=_ssh_connection_details_0,
)
_k8s_0 = K8S(namespace="tl2054", master_node=_master_node_0)
_vdu_cnf_0 = DeploymentVnfStack(
    name="vdu2054",
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
        addr="10.64.163.194", username="Nemuadmin", password="Nokia@123"
    ),
    fhgws=[_fhgw_0],
    instance_id=2054,
    global_bts_id=2054,
)

# BTS
_cbts = CloudBts(
    dus=[_du_0],
    cu=_cu,
    cloud_deployment=_vcu_k8s_cloud_deployment,
    instance_id=2054,
    global_bts_id=2054,
)

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.71.209.99", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(
    airscale=_real_enb,
    oam_ip="10.71.209.99",
    global_bts_id="10583",
)

_appserver_ssh = SshServiceDetails(
    addr="10.71.219.23", username="mmw_sg3", password="mm@3", port="43088"
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.219.23",
    iperf_path="/usr/bin/iperf",
    port="43088",
)
_appserver = AppServer(_iperf)

_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.217.13", username="nokia5G", password="noki@123"
    ),
    serial_number="R5CR92XYFSZ",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="/cygdrive/c/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "samsung_vran20"],
)

_android1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.217.13", username="nokia5G", password="noki@123"
    ),
    serial_number="RFCR11CL9DH",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="/cygdrive/c/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "samsung_vran20"],
)
# RealCore
_pcf = PCF(
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.60.20", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_realcore = RealCore(pcf=_pcf)

# DCAP server
DCAP_server = {
    "ip": "10.57.150.41",
    "user": "dcapuser",
    "password": "Nokia@123",
    "port": "443",
}
Emil_Host = {
    "ip": "10.68.86.137",
    "user": "nokia5G",
    "password": "noki@123",
    "port": "443",
}
_Emil_host = Netact(Emil_Host)

_DCAP = Netact(DCAP_server)

# TestLine
tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    core=_realcore,
    ues=[_android, _android1],
    tl_cloud_topology="CLOUD_5G_AIC_RM17_OCP_AZQJ",
    enbs=[_lte_real_enb],
    appserver=_appserver,
    nms=[_DCAP,_Emil_host],
)

__all__ = ["tl"]
