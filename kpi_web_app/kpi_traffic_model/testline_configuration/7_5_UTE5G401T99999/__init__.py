__maintainer__ = "Li Jie"
__team__ = "NSB MN RAN RD VRF HAZ4 4"
__email__ = "jie.2.li@nokia-sbell.com"

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
from taf.config.testline import NetworkAddress, RoutingInformation

from taf.config.testline import HBTE_PDU as HBTE
from taf.config.testline import RU, RadioTypes
from taf.config.testline import CloudBts, CU
from taf.config.testline import VDU, RANNIC
from taf.config.testline import TestLine
from taf.config.testline import TestPc


# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# Testpc
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.101.60.125", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# CU
_cu = CU(
    instance_id=9999,
    global_bts_id=9999,
    backhaul_site_oam_ip=NetworkAddress(v4="10.57.173.7"),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.171.130", username="core", password="system123"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.173.7", username="Nemuadmin", password="nemuuser", port=443
    ),
    x2c=NetworkAddress(
        v4="10.57.174.74",
        vlan_id=2560,
        routing_v4=RoutingInformation(gateway="10.57.174.64/26"),
    ),
    f1c=NetworkAddress(
        v4="10.57.174.10",
        vlan_id=2559,
        routing_v4=RoutingInformation(gateway="10.57.174.0/26"),
    ),
    f1u=NetworkAddress(
        v4="10.57.174.11",
        vlan_id=2559,
        routing_v4=RoutingInformation(gateway="10.57.174.0/26"),
    ),
    s1u=NetworkAddress(
        v4="10.57.173.39",
        vlan_id=2552,
        routing_v4=RoutingInformation(gateway="10.57.173.32/27"),
    ),
    x2u=NetworkAddress(
        v4="10.57.174.75",
        vlan_id=2560,
        routing_v4=RoutingInformation(gateway="10.57.174.64/26"),
    ),
    tracing=NetworkAddress(
        v4="10.57.173.71",
        vlan_id=2553,
        routing_v4=RoutingInformation(gateway="10.57.173.64/27"),
    ),
)

# ssh connection information of OE, for tenant user
_vcu_ssh_connection_details = SshServiceDetails(
    addr="10.57.171.130", username="cranuser99999", password="systeM!23", port=22
)
# ssh connection information of OE, for root user
_vcu_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.57.171.130", username="core", password="system123", port=22
)

_vcu_master_node = MasterNode(
    k8s_connection_details=_vcu_k8s_connection_details,
    ssh_connection_details=_vcu_ssh_connection_details,
)

_vcu_k8s = K8S(namespace="cran99999", master_node=_vcu_master_node)

_cnf_cu_1 = HelmChart(
    name="vcu99999",
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
_ru_pdu = HBTE(addr="100.71.196.122", port_numbers=[10])

_ru = RU(
    ru_hw_group="hw_group",
    pdu_port=_ru_pdu.pdu_ports[10],
    radio_type=RadioTypes.AEQY,
    default_ssh_connection_details=SshServiceDetails(
        addr="169.254.1.2",
        username="rfsw",
        password="5rfS2qmWC0AiFYvir7k8JekCN8/NklqDK5E6OWXuUVQ=",
    ),
)

# vDU
# RANNIC information
_rannic_0 = RANNIC(serial_number="L1243107672", product_code="AF1791.102", rus=[_ru])

# ssh connection information of OE, for tenant user
_ssh_connection_details_0 = SshServiceDetails(
    addr="10.64.160.242", username="cranuser99999", password="systeM!23"
)
# ssh connection information of OE, for root user
_k8s_connection_details_0 = K8SConnectionDetails(
    ip_addr="10.64.160.242", username="core", password="system123", port="22"
)

_master_node_0 = MasterNode(
    k8s_connection_details=_k8s_connection_details_0,
    ssh_connection_details=_ssh_connection_details_0,
)
_k8s_0 = K8S(namespace="cran99999", master_node=_master_node_0)


_cnf_du_0 = HelmChart(
    name="vdu99999",
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
    cluster_preparation=_cluster_preparation_du_0,
    prerequisite=_prerequisite_du_0,
    cnf=_cnf_du_0,
)

_du_0 = VDU(
    cloud_deployment=_vdu_k8s_cloud_deployment_0,
    oam_http_connection_details=HttpConnectionDetails(
        addr="100.64.161.130", username="Nemuadmin", password="nemuuser", port="443"
    ),
    rannics=[_rannic_0],
    instance_id=99999,
    global_bts_id=99999,
)

# BTS
_cbts = CloudBts(
    dus=[_du_0],
    cu=_cu,
    cloud_deployment=_vcu_k8s_cloud_deployment,
)

# TestLine
tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    tl_cloud_topology="CLOUD_5G_AIC_RM17_OCP_FHGW_AEQY"
)
