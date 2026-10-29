__maintainer__ = "Zhong Tingting"
__team__ = "RAN_RD_VRF_HAZ4_04"
__email__ = "tingting.zhong@nokia-sbell.com"

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
from taf.config.testline.lmi import LMI, Local


# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# Testpc
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.159.23", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# CU
_cu = CU(
    instance_id=37302,
    global_bts_id=37302,
    backhaul_site_oam_ip=NetworkAddress(v4="10.57.160.134"),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.160.2", username="cranuser37302", password="systeM!23"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.160.134", username="Nemuadmin", password="nemuuser", port=443
    ),
)

# ssh connection information of OE, for tenant user
_vcu_ssh_connection_details = SshServiceDetails(
    addr="10.57.160.2", username="cranuser37302", password="systeM!23", port=22
)
# ssh connection information of OE, for root user
_vcu_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.57.160.2", username="core", password="system123", port=22
)

_vcu_master_node = MasterNode(
    k8s_connection_details=_vcu_k8s_connection_details,
    ssh_connection_details=_vcu_ssh_connection_details,
)

_vcu_k8s = K8S(namespace="cran37302", master_node=_vcu_master_node)

_cnf_cu_1 = HelmChart(
    name="vcu37302",
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
    cloud_hosting=_vcu_k8s,
    cluster_preparation=_cluster_preparation_cu_1,
    prerequisite=_prerequisite_cu_1,
    cnf=_cnf_cu_1,
    vnfs=[],
)


# 5G RU
_ru_lmi_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.0.176.61", username="mn5gran", password="nokia123@"
    )
)
_ru_lmi = LMI(
    product_code="476401A.101",
    host=_ru_lmi_pc,
    uart_mapping=[Local(port="COM6"), Local(port="COM5")],
)

_ru_pdu = HBTE(addr="10.71.196.114", port_numbers=[5])

_ru = RU(
    ru_hw_group="AVQC",
    pdu_port=_ru_pdu.pdu_ports[5],
    radio_type=RadioTypes.AVQC,
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2",
        username="rfsw",
        password="f6gh0K2nXq0O8XqVFkUuMtJnzuKm0U3box0QcYgugn0=",
    ),
    lmp_connection=SshServiceDetails(
        addr="10.0.176.61", username="mn5gran", password="nokia123@"
    ),
    serial_number="1M235231310",
    lmi=_ru_lmi,
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
_fhgw_0.ip = "10.64.161.53"
_fhgw_0.username = "toor4nsn"
_fhgw_0.password = "Fhgw@nokia123"
_fhgw_0.version = "22R2"

# RANNIC information
_rannic_0 = RANNIC(serial_number="L1240608156", product_code="AF1791.101", rus=[_ru])

# ssh connection information of OE, for tenant user
_ssh_connection_details_0 = SshServiceDetails(
    addr="10.64.173.162", username="cranuser37302", password="systeM!23"
)
# ssh connection information of OE, for root user
_k8s_connection_details_0 = K8SConnectionDetails(
    ip_addr="10.64.173.162", username="core", password="system123", port="22"
)

_master_node_0 = MasterNode(
    k8s_connection_details=_k8s_connection_details_0,
    ssh_connection_details=_ssh_connection_details_0,
)

_k8s_0 = K8S(namespace="cran37302", master_node=_master_node_0)

_cnf_du_0 = HelmChart(
    name="vdu37302",
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

_vdu_cnf_0 = DeploymentVnfStack(
    name="vdu37302",
    yaml_file=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/du_cnf_values-override.yaml"
    ),
)

_vdu_k8s_cloud_deployment_0 = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    cloud_hosting=_k8s_0,
    cluster_preparation=_cluster_preparation_du_0,
    prerequisite=_prerequisite_du_0,
    cnf=_cnf_du_0,
    vnfs=[_vdu_cnf_0],
)

_du_0 = VDU(
    cloud_deployment=_vdu_k8s_cloud_deployment_0,
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.64.173.90", username="Nemuadmin", password="nemuuser", port="443"
    ),
    fhgws=[_fhgw_0],
    rannics=[_rannic_0],
    instance_id=37302,
    global_bts_id=37302,
    rus=[_ru],
    f1_m_ip_addr="10.64.173.90",
)

# BTS
_cbts = CloudBts(
    dus=[_du_0],
    cu=_cu,
    cloud_deployment=_vcu_k8s_cloud_deployment,
)

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.71.212.162", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(
    airscale=_real_enb,
    oam_ip="10.71.212.162",
    global_bts_id="607",
)

# CI_Detail_UE_Type='Nokia FastMile 5G Receiver 5G19-A'
_fastmile_appserver_1 = TafUeAppServer(
    app_server_name="APP_SERVER_1",
    address="10.71.207.151",
    user="vrf4_sg4",
    password="vrf4@sg4",
    bind_interface_ip="10.71.207.151",
    expected_prompt="[vrf4_sg4@appserver ~]$",
    binary_path="/home/vrf4_sg4/taf_debug/iperf",
    ports=[53302, 54302],
)

_fastmile_data_transfer_1 = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_fastmile_appserver_1,
    interval=1,
    binary_path="iperf",
    version=2,
)

_fastmile_1 = TafUeFastmile(
    ue_pc_address="10.57.159.23",
    root_password="LP=2T6RfZNgh4d5=",
    default_user_password="EuaAd6yNQbyZX9+m",
    ue_manage_ip="10.71.205.86",
    serial_number="KLT230800008",
    version="receiver 5g19a",
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
    tl_cloud_topology="CLOUD_5G_AIC_OE22_DC_AVQC",
    enbs=[_lte_real_enb],
)
