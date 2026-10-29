__maintainer__ = "Yang Qiming"
__team__ = "MN_RAN_RD_VRF_HAZ4_06"
__email__ = "qiming.yang@nokia-sbell.com"

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
    MediaTek,
)  # added in taf.meta.5.4

# added in taf.meta 5.4
from taf.config.testline.attenuator import (
    AttenuationPort,
    TopYoung,
    JFW,
    HBTE,
    Hytem,
    RadioRack,
)
from taf.config.testline import NetworkAddress, RoutingInformation, LicenseKeeper
from taf.config.testline import RealEnb, Airscale, CommonUnit
#from taf.config.testline import HBTE_PDU as HBTE
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
        addr="10.57.167.140", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# #RealEnb
_attenuator_0 = HBTE(
    ip_addr="10.71.205.174",
    port=5000,
    attenuation_port_numbers=[13, 14, 15, 16],
    model="PA-16-16-6-127-0.5-B-S",
)

# CU
_cu = CU(
    instance_id=275,
    global_bts_id=275,
    backhaul_site_oam_ip=NetworkAddress(v4="10.57.173.16"),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.187.2", username="tl275", password="systeM!23"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.187.138", username="Nemuadmin", password="Nokia@123", port=443
    ),
    f1c=NetworkAddress(
        v4="10.57.250.16",
        vlan_id=109,
        routing_v4=RoutingInformation(gateway="10.57.180.1", ip_prefix_length=29),
    ),
    f1u=NetworkAddress(
        v4="10.57.250.17",
        vlan_id=109,
        routing_v4=RoutingInformation(gateway="10.57.180.1", ip_prefix_length=29),
    ),
    ngc=NetworkAddress(
        v4="10.57.250.144",
        vlan_id=111,
        routing_v4=RoutingInformation(gateway="10.57.180.129", ip_prefix_length=32),
    ),
    ngu=NetworkAddress(
        v4="10.57.250.145",
        vlan_id=111,
        routing_v4=RoutingInformation(gateway="10.57.180.129", ip_prefix_length=32),
    ),
    x2c=NetworkAddress(
        v4="10.57.250.80",
        vlan_id=110,
        routing_v4=RoutingInformation(gateway="10.57.180.65", ip_prefix_length=8),
    ),
    x2u=NetworkAddress(
        v4="10.57.250.81",
        vlan_id=110,
        routing_v4=RoutingInformation(gateway="10.57.180.65", ip_prefix_length=8),
    ),
    s1u=NetworkAddress(
        v4="10.57.187.42",
        vlan_id=102,
        routing_v4=RoutingInformation(gateway="10.57.180.193", ip_prefix_length=8),
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
    addr="10.57.138.34", username="tl275", password="systeM!23", port=22
)
# ssh connection information of OE, for root user
_vcu_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.57.138.34", username="tl275", password="systeM!23", port=22
)

_vcu_master_node = MasterNode(
    k8s_connection_details=_vcu_k8s_connection_details,
    ssh_connection_details=_vcu_ssh_connection_details,
)

_vcu_k8s = K8S(namespace="tl275", master_node=_vcu_master_node)

_vcu_k8s_cloud_deployment = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    networks=[_vcu_intnet_1],
    vnfs=[_vcu_cnf_1],
    cloud_hosting=_vcu_k8s,
)


# 5G RU
_ru_pdu1 = FPFH(addr="10.71.196.76", port_numbers=[5])  ##PB infor error,need update

_ru1 = RU(
    ru_hw_group="Below6GHz",
    pdu_port=_ru_pdu1.pdu_ports[5],
    radio_type=RadioTypes.AEHC,
    attenuation_ports=[
        _attenuator_0.attenuator_ports[13],
        _attenuator_0.attenuator_ports[14],
        _attenuator_0.attenuator_ports[15],
        _attenuator_0.attenuator_ports[16],
    ],
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.37",
        username="rfsw",
        password="f6gh0K2nXq0O8XqVFkUuMtJnzuKm0U3box0QcYgugn0=",
    ),
)

# vDU information need update
_IP_pxe = "10.71.220.62"
_pxe_server_ssh_info = SshServiceDetails(
    addr=_IP_pxe, username="root", password="uteadmin"
)
_pxe_server = PxeServer(nfs_ip=_IP_pxe, ssh_connection_details=_pxe_server_ssh_info)

# FHGW information,need update
_fhgw_0 = FHGW(user_config_path=_cfg_dir, rus=[_ru1], pxe_server=_pxe_server)
_fhgw_0.ip = "10.71.160.181"
_fhgw_0.username = "toor4nsn"
_fhgw_0.password = "Fhgw@nokia123"
_fhgw_0.version = "FHGW24R2"

# OE information
_IP_OCP = "10.64.174.138"
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
_k8s_0 = K8S(namespace="crantl275", master_node=_master_node_0)
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
        addr="10.64.174.162", username="Nemuadmin", password="Nokia@123"
    ),
    fhgws=[_fhgw_0],
    instance_id=275,
    global_bts_id=275,
    rus=[_ru1],
)

# BTS
_cbts = CloudBts(
    dus=[_du_0],
    cu=_cu,
    cloud_deployment=_vcu_k8s_cloud_deployment,
)

# Iperf
_appserver_ssh = SshServiceDetails(
    addr="10.57.191.240", username="vrf4_sg6", password="Nokia@1234567", port="56275"
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.240",
    iperf_path="/usr/bin/iperf",
    port="563275",
)

_appserver = AppServer(_iperf)

# CI_Detail_UE_Type='MTK'
_ue_host_ssh = SshServiceDetails(
    addr="10.71.218.14", username="mn5gran", password="nokia123@"
)

_mtk = MediaTek(
    ssh_connection_details=_ue_host_ssh,
    server_dir="c:/pyro_server",
    server_port=8080,
    edb_file_path="auto",
    imei="0123456789ABCDEF",
    imsi="460023100013239",
    apn_url="dxdata2",
    iperf_details=_iperf,
    capabilities=["REAL_MEDIATEK_UE", "mtk"],
    serial_number="0123456789ABCDEF",
)


# TestLine
tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    tl_cloud_topology="TL275",
    ues=[_mtk],
    appserver=_appserver,
    attenuators=[_attenuator_0],
)

__all__ = ["tl"]
