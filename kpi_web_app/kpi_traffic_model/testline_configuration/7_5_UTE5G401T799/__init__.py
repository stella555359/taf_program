__maintainer__ = "yulu"
__team__ = "NSB MN RAN RD VRF HAZ4 2"
__email__ = "lu.1.yu@nokia-sbell.com"

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
from taf.config.testline import HBTE_PDU as HBTE
from taf.config.testline import RU, RadioTypes
from taf.config.testline import CloudBts, CU
from taf.config.testline import VDU, FHGW, RANNIC
from taf.config.testline import PxeServer
from taf.config.testline import TestLine
from taf.config.testline import RealEnb
from taf.config.testline import TestPc

from taf.config.testline.taf_ue_data_transfer_protocol import TafUeDataTransferProtocol
from taf.config.testline.ue import TafUeFastmile
from taf.config.testline.appserver import TafUeAppServer

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# Testpc
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.199", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# CU
_cu = CU(
    instance_id=799,
    global_bts_id=799,
    backhaul_site_oam_ip=NetworkAddress(v4="10.57.173.10"),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.160.2", username="cranuser799", password="systeM!23"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.160.138", username="Nemuadmin", password="nemuuser", port=443
    ),
    x2c=NetworkAddress(
        v4="10.57.190.80",
        vlan_id=110,
        routing_v4=RoutingInformation(gateway="10.57.174.64/26"),
    ),
    f1c=NetworkAddress(
        v4="10.57.190.16",
        vlan_id=109,
        routing_v4=RoutingInformation(gateway="10.57.174.0/26"),
    ),
    f1u=NetworkAddress(
        v4="10.57.190.17",
        vlan_id=109,
        routing_v4=RoutingInformation(gateway="10.57.174.0/26"),
    ),
    s1u=NetworkAddress(
        v4="10.57.160.42",
        vlan_id=102,
        routing_v4=RoutingInformation(gateway="10.57.173.32/27"),
    ),
    x2u=NetworkAddress(
        v4="10.57.190.81",
        vlan_id=110,
        routing_v4=RoutingInformation(gateway="10.57.174.64/26"),
    ),
    tracing=NetworkAddress(
        v4="10.57.160.74",
        vlan_id=103,
        routing_v4=RoutingInformation(gateway="10.57.173.64/27"),
    ),
)

# ssh connection information of OE, for tenant user
_vcu_ssh_connection_details = SshServiceDetails(
    addr="10.57.160.2", username="cranuser799", password="systeM!23", port=22
)
# ssh connection information of OE, for root user
_vcu_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.57.160.2", username="core", password="system123", port=22
)

_vcu_master_node = MasterNode(
    k8s_connection_details=_vcu_k8s_connection_details,
    ssh_connection_details=_vcu_ssh_connection_details,
)

_vcu_k8s = K8S(namespace="cran799", master_node=_vcu_master_node)

_cnf_cu_1 = HelmChart(
    name="vcu799",
    yaml_file=os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/vcu_cnf.yaml"),
)

_cluster_preparation_cu_1 = HelmChart(
    name=_cnf_cu_1.name + "-cluster-preparation",
    yaml_file=os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/vcu_preparation.yaml"),
)

_prerequisite_cu_1 = HelmChart(
    name=_cnf_cu_1.name + "-prerequisite",
    yaml_file=os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/vcu_prerequisite.yaml"),
)
_vcu_k8s_cloud_deployment = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    vnfs=[],
    cloud_hosting=_vcu_k8s,
    cluster_preparation=_cluster_preparation_cu_1,
    prerequisite=_prerequisite_cu_1,
    cnf=_cnf_cu_1,
)


# 5G RU
_ru_pdu = HBTE(addr="10.57.176.200", port_numbers=[6])

_ru = RU(
    ru_hw_group="hw_group",
    pdu_port=_ru_pdu.pdu_ports[6],
    radio_type=RadioTypes.AEQP,
    default_ssh_connection_details=SshServiceDetails(
        addr="169.254.1.2",
        username="rfsw",
        password="5rfS2qmWC0AiFYvir7k8JekCN8/NklqDK5E6OWXuUVQ=",
    ),
)

# _ru2_pdu = HBTE(addr="10.57.246.56", port_numbers=[5])

# _ru2 = RU(
#     ru_hw_group="hw_group",
#     pdu_port=_ru_pdu.pdu_ports[5],
#     radio_type=RadioTypes.AQQY,
#     default_ssh_connection_details=SshServiceDetails(
#         addr="169.254.1.2",
#         username="rfsw",
#         password="3Is6ezFJ7dFlB29cgs0yp3RCM3fUF1zNO1+6Z08tlAc=",
#     ),
# )

# vDU
# RANNIC information
_rannic_0 = RANNIC(serial_number="L1241302485", product_code="AF1791.101", rus=[_ru])

# ssh connection information of OE, for tenant user
_ssh_connection_details_0 = SshServiceDetails(
    addr="10.57.170.18", username="cranuser799", password="systeM!23"
)
# ssh connection information of OE, for root user
_k8s_connection_details_0 = K8SConnectionDetails(
    ip_addr="10.57.170.18", username="core", password="system123", port="22"
)

_master_node_0 = MasterNode(
    k8s_connection_details=_k8s_connection_details_0,
    ssh_connection_details=_ssh_connection_details_0,
)
_k8s_0 = K8S(namespace="cran799", master_node=_master_node_0)
_vdu_cnf_0 = DeploymentVnfStack(
    name="vdu799",
    yaml_file=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/du_cnf_values-override.yaml"
    ),
)

_cnf_du_0 = HelmChart(
    name="vdu799",
    yaml_file=os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/vdu_cnf.yaml"),
)
_cluster_preparation_du_0 = HelmChart(
    name=_cnf_du_0.name + "-cluster-preparation",
    yaml_file=os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/vdu_preparation.yaml"),
)

_prerequisite_du_0 = HelmChart(
    name=_cnf_du_0.name + "-prerequisite",
    yaml_file=os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/vdu_prerequisite.yaml"),
)

_vdu_k8s_cloud_deployment_0 = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    cloud_hosting=_k8s_0,
    vnfs=[_vdu_cnf_0],
    cluster_preparation=_cluster_preparation_du_0,
    prerequisite=_prerequisite_du_0,
    cnf=_cnf_du_0,
)

_du_0 = VDU(
    cloud_deployment=_vdu_k8s_cloud_deployment_0,
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.170.50", username="Nemuadmin", password="nemuuser", port="443"
    ),
    rannics=[_rannic_0],
    instance_id=799,
    global_bts_id=799,
    f1_m_ip_addr="10.57.170.50",
)

# BTS
_cbts = CloudBts(
    dus=[_du_0],
    cu=_cu,
    cloud_deployment=_vcu_k8s_cloud_deployment,
)

# CI_Detail_UE_Type='Nokia FastMile 5G Gateway 3.2'
_fastmile_appserver_1 = TafUeAppServer(
    app_server_name="APP_SERVER_1",
    address="10.57.223.206",
    user="ute",
    password="ute",
    bind_interface_ip="10.57.223.206",
    expected_prompt="[ute@localhost ~]$ ",
    binary_path="/usr/bin/iperf",
    ports=[52799, 52800],
)

_fastmile_data_transfer_1 = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_fastmile_appserver_1,
    interval=1,
    binary_path="/usr/bin/iperf",
    version=2,
)

_fastmile_1 = TafUeFastmile(
    ue_pc_address="10.57.155.199",
    root_password="b6fa933276bd",
    ue_manage_ip="10.57.230.103",
    serial_number="LPL221400695",
    version="3.2",
    data_transfer=[_fastmile_data_transfer_1],
    proxy_mngr_port=9955,
    ueproxy_force_release=True,
    capabilities=["REAL_FASTMILE_UE1", "nokia_fastmile"],
)

# TestLine
tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    ues=[_fastmile_1],
    tl_cloud_topology="CLOUD_5G_AIC_AEQP",
    # enbs=[_lte_real_enb],
)
