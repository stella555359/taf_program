__maintainer__ = "Rock 1. Wang"
__team__ = "NSB MN RAN RD VRF HAZ3 4"
__email__ = "rock.1.wang@nokia-sbell.com"

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
        addr="10.57.155.32", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# CU
_cu = CU(
    instance_id=746,
    global_bts_id=746,
    backhaul_site_oam_ip=NetworkAddress(v4="10.57.209.137"),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.209.2", username="core", password="system123"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.209.137", username="Nemuadmin", password="nemuuser", port=443
    ),
    x2c=NetworkAddress(
        v4="10.57.210.78",
        vlan_id=110,
        routing_v4=RoutingInformation(gateway="10.57.210.64/26"),
    ),
    f1c=NetworkAddress(
        v4="10.57.210.14",
        vlan_id=109,
        routing_v4=RoutingInformation(gateway="10.57.210.0/26"),
    ),
    f1u=NetworkAddress(
        v4="10.57.210.15",
        vlan_id=109,
        routing_v4=RoutingInformation(gateway="10.57.210.0/26"),
    ),
    s1u=NetworkAddress(
        v4="10.57.209.41",
        vlan_id=102,
        routing_v4=RoutingInformation(gateway="10.57.209.32/27"),
    ),
    x2u=NetworkAddress(
        v4="10.57.210.79",
        vlan_id=110,
        routing_v4=RoutingInformation(gateway="10.57.210.64/26"),
    ),
    tracing=NetworkAddress(
        v4="10.57.209.73",
        vlan_id=103,
        routing_v4=RoutingInformation(gateway="10.57.209.64/27"),
    ),
)

# ssh connection information of OE, for tenant user
_vcu_ssh_connection_details = SshServiceDetails(
    addr="10.57.209.2", username="cranuser746", password="systeM!23", port=22
)
# ssh connection information of OE, for root user
_vcu_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.57.209.2", username="core", password="system123", port=22
)

_vcu_master_node = MasterNode(
    k8s_connection_details=_vcu_k8s_connection_details,
    ssh_connection_details=_vcu_ssh_connection_details,
)

_vcu_k8s = K8S(namespace="cran746", master_node=_vcu_master_node)

_cnf_cu_1 = HelmChart(
    name="vcu746",
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
_ru_pdu = HBTE(addr="10.71.196.122", port_numbers=[1])

_ru = RU(
    ru_hw_group="hw_group",
    pdu_port=_ru_pdu.pdu_ports[1],
    radio_type=RadioTypes.AEQY,
    default_ssh_connection_details=SshServiceDetails(
        addr="169.254.1.2",
        username="rfsw",
        password="5rfS2qmWC0AiFYvir7k8JekCN8/NklqDK5E6OWXuUVQ=",
    ),
)

# vDU
_pxe_server_ssh_info = SshServiceDetails(
    addr="10.64.161.14", username="ute", password="!Q2w3e4r5t6y7u"
)

_pxe_server = PxeServer(
    nfs_ip="10.64.161.14", ssh_connection_details=_pxe_server_ssh_info
)

# FHGW information
_fhgw_0 = FHGW(user_config_path=_cfg_dir, rus=[_ru], pxe_server=_pxe_server)
_fhgw_0.ip = "10.57.135.236"
_fhgw_0.username = "root"
_fhgw_0.password = "root"
_fhgw_0.version = "25R2"

# RANNIC information
_rannic_0 = RANNIC(serial_number="L1241207382", product_code="AF1791.101", rus=[_ru])

# ssh connection information of OE, for tenant user
_ssh_connection_details_0 = SshServiceDetails(
    addr="10.57.137.250", username="cranuser746", password="systeM!23"
)
# ssh connection information of OE, for root user
_k8s_connection_details_0 = K8SConnectionDetails(
    ip_addr="10.57.137.250", username="core", password="system123", port="22"
)

_master_node_0 = MasterNode(
    k8s_connection_details=_k8s_connection_details_0,
    ssh_connection_details=_ssh_connection_details_0,
)
_k8s_0 = K8S(namespace="cran746", master_node=_master_node_0)
_vdu_cnf_0 = DeploymentVnfStack(
    name="vdu746",
    yaml_file=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/du_cnf_values-override.yaml"
    ),
)
_vdu_intnet_0 = DeploymentNetworkStack(
    name=_vdu_cnf_0.name + "-prerequisite",
    yaml_file=os.path.join(_cfg_dir, "DEP/gnbs_0/vDU_0/DU_pvc_values-override.yaml"),
)

_cnf_du_0 = HelmChart(
    name="vdu746",
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
        addr="10.57.213.146", username="Nemuadmin", password="nemuuser", port="443"
    ),
    rannics=[_rannic_0],
    instance_id=746,
    global_bts_id=746,
)

# BTS
_cbts = CloudBts(
    dus=[_du_0],
    cu=_cu,
    cloud_deployment=_vcu_k8s_cloud_deployment,
)

# _common_unit_2 = CommonUnit(
#    lmp_connection=SshServiceDetails(
#        addr="10.71.212.163", username="toor4nsn", password="oZPS0POrRieRtu"
#    ),
#    capacity_units=[],
# )

# _real_enb = Airscale(common_units=[_common_unit_2])

# _lte_real_enb = RealEnb(
#    airscale=_real_enb,
#    oam_ip="10.71.212.163",
#    global_bts_id="608",
# )

# CI_Detail_UE_Type='Nokia FastMile 5G Gateway 3.1'
_fastmile_appserver_1 = TafUeAppServer(
    app_server_name="APP_SERVER_1",
    address="10.71.207.151",
    user="vrf4_sg4",
    password="vrf4@sg4",
    bind_interface_ip="10.71.207.151",
    expected_prompt="[vrf4_sg4@appserver ~]$",
    binary_path="/home/vrf4_sg4/taf_debug/iperf",
    ports=[53608, 54608],
)

_fastmile_data_transfer_1 = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_fastmile_appserver_1,
    interval=1,
    binary_path="iperf",
    version=2,
)

_fastmile_1 = TafUeFastmile(
    ue_pc_address="10.57.195.13",
    root_password="c6fa6a92fea9",
    ue_manage_ip="10.71.212.221",
    serial_number="LPL2214005D4",
    version="3.2",
    data_transfer=[_fastmile_data_transfer_1],
    proxy_mngr_port=9955,
    ueproxy_force_release=True,
    capabilities=["REAL_FASTMILE_UE1", "nokia_fastmile"],
)

# TestLine topology
tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    ues=[_fastmile_1],
    tl_cloud_topology="CLOUD_5G_AIC_HPE_OCP_Switch7250_FHGW",
    # enbs=[_lte_real_enb],
)