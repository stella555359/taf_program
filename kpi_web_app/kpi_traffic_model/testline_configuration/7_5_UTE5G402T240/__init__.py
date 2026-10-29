__maintainer__ = "Jack Zeng"
__team__ = "RAN_PZ_HAZ4_SG03"
__email__ = "jack.zeng@nokia-sbell.com"

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
from taf.config.testline import HBTE_PDU as HBTE
from taf.config.testline import RU, RadioTypes
from taf.config.testline import CloudBts, CU
from taf.config.testline import VDU, FHGW
from taf.config.testline import PxeServer
from taf.config.testline import TestLine
from taf.config.testline import RealEnb
from taf.config.testline import TestPc

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# Testpc
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.121", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# CU
_cu = CU(
    instance_id=240,
    global_bts_id=240,
    backhaul_site_oam_ip=NetworkAddress(v4="10.57.173.4"),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.171.130", username="tl240", password="systeM!23"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.173.4", username="Nemuadmin", password="nemuuser", port=443
    ),
    x2c=NetworkAddress(
        v4="10.57.174.68",
        vlan_id=2560,
        routing_v4=RoutingInformation(gateway="10.57.174.64", ip_prefix_length=26),
    ),
    f1c=NetworkAddress(
        v4="10.57.174.4",
        vlan_id=2559,
        routing_v4=RoutingInformation(gateway="10.57.174.0", ip_prefix_length=26),
    ),
    f1u=NetworkAddress(
        v4="10.57.174.5",
        vlan_id=2559,
        routing_v4=RoutingInformation(gateway="10.57.174.0", ip_prefix_length=26),
    ),
    s1u=NetworkAddress(
        v4="10.57.173.36",
        vlan_id=2552,
        routing_v4=RoutingInformation(gateway="10.57.173.32", ip_prefix_length=27),
    ),
    x2u=NetworkAddress(
        v4="10.57.174.69",
        vlan_id=2560,
        routing_v4=RoutingInformation(gateway="10.57.174.64", ip_prefix_length=26),
    ),
    tracing=NetworkAddress(
        v4="10.57.173.68",
        vlan_id=2553,
        routing_v4=RoutingInformation(gateway="10.57.173.64", ip_prefix_length=27),
    ),
)

# cloud_deployment for vCU
_vcu_cnf_1 = DeploymentVnfStack(
    name="vcu240",
    yaml_file=os.path.join(_cfg_dir, "DEP/gnbs_0/vCU/CU_cnf_values-override.yaml"),
)
_vcu_intnet_1 = DeploymentNetworkStack(
    name=_vcu_cnf_1.name + "-prerequisite",
    yaml_file=os.path.join(_cfg_dir, "DEP/gnbs_0/vCU/CU_pvc_values-override.yaml"),
)

# ssh connection information of OE, for tenant user
_vcu_ssh_connection_details = SshServiceDetails(
    addr="10.57.171.130", username="core", password="system123", port=22
)
# ssh connection information of OE, for root user
_vcu_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.57.171.130", username="tl240", password="systeM!23", port=22
)

_vcu_master_node = MasterNode(
    k8s_connection_details=_vcu_k8s_connection_details,
    ssh_connection_details=_vcu_ssh_connection_details,
)

_vcu_k8s = K8S(namespace="tl240", master_node=_vcu_master_node)

_vcu_k8s_cloud_deployment = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    networks=[_vcu_intnet_1],
    vnfs=[_vcu_cnf_1],
    cloud_hosting=_vcu_k8s,
)


# 5G RU
_ru_pdu = HBTE(addr="10.71.196.240", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru = RU(
    ru_hw_group="hw_group",
    pdu_port=_ru_pdu.pdu_ports[5],
    radio_type=RadioTypes.AZQP,
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.35",
        username="rfsw",
        password="5rfS2qmWC0AiFYvir7k8JekCN8/NklqDK5E6OWXuUVQ=",
    ),
)

_ru2 = RU(
    ru_hw_group="hw_group",
    pdu_port=_ru_pdu.pdu_ports[6],
    radio_type=RadioTypes.AZQP,
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.35",
        username="rfsw",
        password="5rfS2qmWC0AiFYvir7k8JekCN8/NklqDK5E6OWXuUVQ=",
    ),
)

# vDU
_pxe_server_ssh_info = SshServiceDetails(
    addr="100.71.160.156", username="root", password="centos"
)
_pxe_server = PxeServer(
    nfs_ip="100.71.160.156", ssh_connection_details=_pxe_server_ssh_info
)

# FHGW information
_fhgw_0 = FHGW(user_config_path=_cfg_dir, rus=[_ru], pxe_server=_pxe_server)
_fhgw_0.ip = "10.71.220.71"
_fhgw_0.username = "toor4nsn"
_fhgw_0.password = "Fhgw@nokia123"
_fhgw_0.version = "22R1"

_fhgw_1 = FHGW(user_config_path=_cfg_dir, rus=[_ru2], pxe_server=_pxe_server)
_fhgw_1.ip = "10.71.220.71"
_fhgw_1.username = "toor4nsn"
_fhgw_1.password = "Fhgw@nokia123"
_fhgw_1.version = "22R1"

_ssh_connection_details_0 = SshServiceDetails(
    addr="10.64.165.98", username="core", password="system123"
)
_k8s_connection_details_0 = K8SConnectionDetails(
    ip_addr="10.64.165.98", username="core", password="system123", port="22"
)

_master_node_0 = MasterNode(
    k8s_connection_details=_k8s_connection_details_0,
    ssh_connection_details=_ssh_connection_details_0,
)
_k8s_0 = K8S(namespace="tl240", master_node=_master_node_0)
_vdu_cnf_0 = DeploymentVnfStack(
    name="vdu2401",
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


_ssh_connection_details_1 = SshServiceDetails(
    addr="10.64.165.99", username="core", password="system123"
)
_k8s_connection_details_1 = K8SConnectionDetails(
    ip_addr="10.64.165.99", username="core", password="system123", port="22"
)

_master_node_1 = MasterNode(
    k8s_connection_details=_k8s_connection_details_1,
    ssh_connection_details=_ssh_connection_details_1,
)
_k8s_1 = K8S(namespace="tl240", master_node=_master_node_1)
_vdu_cnf_1 = DeploymentVnfStack(
    name="vdu2402",
    yaml_file=os.path.join(_cfg_dir, "DEP/gnbs_0/vDU_1/DU_cnf_values-override.yaml"),
)
_vdu_intnet_1 = DeploymentNetworkStack(
    name=_vdu_cnf_1.name + "-prerequisite",
    yaml_file=os.path.join(_cfg_dir, "DEP/gnbs_0/vDU_1/DU_pvc_values-override.yaml"),
)

_vdu_k8s_cloud_deployment_1 = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    cloud_hosting=_k8s_1,
    networks=[_vdu_intnet_1],
    vnfs=[_vdu_cnf_1],
)

_du_0 = VDU(
    cloud_deployment=_vdu_k8s_cloud_deployment_0,
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.64.165.134", username="Nemuadmin", password="nemuuser"
    ),
    fhgws=[_fhgw_0],
    instance_id=240,
    global_bts_id=240,
)

_du_1 = VDU(
    cloud_deployment=_vdu_k8s_cloud_deployment_1,
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.64.165.166", username="Nemuadmin", password="nemuuser"
    ),
    fhgws=[_fhgw_1],
    instance_id=240,
    global_bts_id=240,
)

# BTS
_cbts = CloudBts(
    dus=[_du_0, _du_1],
    cu=_cu,
    cloud_deployment=_vcu_k8s_cloud_deployment,
)

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.71.214.107", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(
    airscale=_real_enb,
    oam_ip="10.71.214.107",
    global_bts_id="24021",
)

# TestLine
tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    tl_cloud_topology="CLOUD_5G_AIC_RM17_OCP_FHGW_AZQP",
    enbs=[_lte_real_enb],
)

__all__ = ["tl"]
