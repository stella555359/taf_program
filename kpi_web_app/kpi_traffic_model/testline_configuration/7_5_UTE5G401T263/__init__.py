__maintainer__ = "Liu Shasha"
__team__ = "RAN_PZ_HAZ4_SG05"
__email__ = "shasha.liu@nokia-sbell.com"

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
from taf.config.testline.pdu import (
    FACOM,
    PduPort,
    Pdu,
    EPC,
    ATEN,
    RRB,
    APC,
    Gude,
    HBTE,
    FPFH,
    TopYoung,
)
from taf.config.testline import NetworkAddress, RoutingInformation
from taf.config.testline import RealEnb, Airscale, CommonUnit
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
        addr="10.101.60.26", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# CU
_cu = CU(
    instance_id=2163,
    global_bts_id=2163,
    backhaul_site_oam_ip=NetworkAddress(v4="10.57.188.138"),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.188.4", username="tl2163", password="systeM!23"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.188.138", username="Nemuadmin", password="Nokia@123", port=443
    ),
    f1c=NetworkAddress(
        v4="10.57.201.16",
        vlan_id=109,
        routing_v4=RoutingInformation(gateway="10.57.201.0/26"),
    ),
    f1u=NetworkAddress(
        v4="10.57.201.17",
        vlan_id=109,
        routing_v4=RoutingInformation(gateway="10.57.201.0/26"),
    ),
    ngc=NetworkAddress(
        v4="10.57.201.144",
        vlan_id=111,
        routing_v4=RoutingInformation(gateway="10.57.201.128/26"),
    ),
    ngu=NetworkAddress(
        v4="10.57.201.145",
        vlan_id=111,
        routing_v4=RoutingInformation(gateway="10.57.201.128/26"),
    ),
    x2c=NetworkAddress(
        v4="10.57.201.80",
        vlan_id=110,
        routing_v4=RoutingInformation(gateway="10.57.201.64/26"),
    ),
    x2u=NetworkAddress(
        v4="10.57.201.81",
        vlan_id=110,
        routing_v4=RoutingInformation(gateway="10.57.201.64/26"),
    ),
    s1u=NetworkAddress(
        v4="10.57.188.42",
        vlan_id=102,
        routing_v4=RoutingInformation(gateway="10.57.188.32/27"),
    ),
    tracing=None,
)

# cloud_deployment for vCU
_vcu_cnf_1 = DeploymentVnfStack(
    name="tl2163",  # vCU release name
    yaml_file=os.path.join(_cfg_dir, "DEP/gnbs_0/vCU/CU_cnf_values-override.yaml"),
)
_vcu_intnet_1 = DeploymentNetworkStack(
    name=_vcu_cnf_1.name + "-prerequisite",
    yaml_file=os.path.join(_cfg_dir, "DEP/gnbs_0/vCU/CU_pvc_values-override.yaml"),
)

# ssh connection information of OE, for tenant user
_vcu_ssh_connection_details = SshServiceDetails(
    addr="10.57.188.4", username="tl2163", password="systeM!23", port=22
)
# ssh connection information of OE, for root user
_vcu_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.57.188.4", username="tl2163", password="systeM!23", port=22
)

_vcu_master_node = MasterNode(
    k8s_connection_details=_vcu_k8s_connection_details,
    ssh_connection_details=_vcu_ssh_connection_details,
)

_vcu_k8s = K8S(namespace="tl2163", master_node=_vcu_master_node)  # vCU namespace

_vcu_k8s_cloud_deployment = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    networks=[_vcu_intnet_1],
    vnfs=[_vcu_cnf_1],
    cloud_hosting=_vcu_k8s,
)

# 5G RU
_ru1_pdu = TopYoung(addr="10.71.196.198", port_numbers=[5])

_ru1 = RU(
    ru_hw_group="hw_group",
    pdu_port=_ru1_pdu.pdu_ports[5],
    radio_type=RadioTypes.AZQJ,
    serial_number="1M214627093",
    product_code="475244A",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.169.4.3",
        username="serviceuser",
        password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og=",
    ),
)

_ru2_pdu = TopYoung(addr="10.71.196.200", port_numbers=[5])

_ru2 = RU(
    ru_hw_group="hw_group",
    pdu_port=_ru2_pdu.pdu_ports[5],
    radio_type=RadioTypes.AHCA,
    serial_number="L1181705791",
    product_code="473966A",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.169.5.3",
        username="serviceuser",
        password="bobuWrUHk7Xq7WPpY9ZcjEi8zNdX3plZ+/y420RZ7W4=",
    ),
)

# vDU
_pxe_server_ssh_info = SshServiceDetails(
    addr="10.71.223.xxx", username="ute", password="!Q2w3e4r5t6y7u"
)
_pxe_server = PxeServer(
    nfs_ip="10.71.223.xxx", ssh_connection_details=_pxe_server_ssh_info
)

# FHGW information
# RU Direct Connetion
_fhgw_0 = FHGW(user_config_path=_cfg_dir, rus=[_ru1, _ru2], pxe_server=_pxe_server)
_fhgw_0.ip = "10.64.161.55"
_fhgw_0.username = "root"
_fhgw_0.password = "root"
_fhgw_0.version = "22R2"

_ssh_connection_details_0 = SshServiceDetails(
    addr="10.64.161.2", username="core", password="system123"
)
_k8s_connection_details_0 = K8SConnectionDetails(
    ip_addr="10.64.161.2", username="core", password="system123", port="22"
)

_master_node_0 = MasterNode(
    k8s_connection_details=_k8s_connection_details_0,  # non-tenant_credentials
    ssh_connection_details=_ssh_connection_details_0,  # tenant_credentials
)
_k8s_0 = K8S(namespace="cran1", master_node=_master_node_0)  # vDU namespace
_vdu_cnf_0 = DeploymentVnfStack(
    name="vdutest",  # vDU release name
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
        addr="10.64.161.170", username="Nemuadmin", password="Nokia@123"
    ),
    fhgws=[_fhgw_0],
    instance_id=2163,
    global_bts_id=2163,
)

# BTS
_cbts = CloudBts(
    dus=[_du_0],
    cu=_cu,
    cloud_deployment=_vcu_k8s_cloud_deployment,
)

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.71.211.xx", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(
    airscale=_real_enb,
    oam_ip="10.71.211.xx",
    global_bts_id="172",
)

"""
# for FastMile CPE 3.2
_fastmile_appserver_1 = TafUeAppServer(
    app_server_name="APP_SERVER_1",
    address="10.57.191.247",
    user="vrf4_sg5",
    password="vrf4@sg5",
    bind_interface_ip="10.57.191.247",
    expected_prompt="[vrf4_sg5@appserver ~]$ ",
    binary_path="/home/vrf4_sg5/taf_debug/iperf",
    ports=[55830, 55831],
)

_fastmile_data_transfer_1 = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_fastmile_appserver_1,
    interval=1,
    binary_path="iperf",
    version=2,
)

_fastmile_1 = TafUeFastmile(
    com_port="4",
    ue_pc_address="10.101.47.254",
    root_password="96ca38c29bd2",
    ue_manage_ip="192.168.1.1",
    serial_number="LPL221400517",
    data_transfer=[_fastmile_data_transfer_1],
    version="3.2",
    ue_pc_port=5555,
    capabilities=["REAL_FASTMILE_UE2", "nokia_fastmile"],
)
"""

# Netact
_netact = NetAct(
    https_main_info=HttpConnectionDetails(
        addr="10.82.47.15", username="omc", password="Medsql!_1893"
    ),
)

# TestLine
tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    tl_cloud_topology="CLOUD_5G_AIC_RM17_OCP_DC_AZQJ",
    enbs=[_lte_real_enb],
    # ues=[_android_1],
    # nms=_netact,
    # appserver=_appserver,
)

__all__ = ["tl"]
