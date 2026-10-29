__maintainer__ = "zhang yu2"
__team__ = "RAN_PZ_HAZ3_SG02"
__email__ = "yu.2.zhang@nokia-sbell.com"

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
from taf.config.testline import NetworkAddress, RoutingInformation
from taf.config.testline import RealEnb, Airscale, CommonUnit
from taf.config.testline import HBTE_PDU as HBTE
from taf.config.testline.pdu import TopYoung
from taf.config.testline import RU, RadioTypes
from taf.config.testline import CloudBts, CU
from taf.config.testline import VDU, FHGW
from taf.config.testline import PxeServer
from taf.config.testline import TestLine
from taf.config.testline import RealEnb
from taf.config.testline import TestPc
from taf.config.testline.nms import NetAct

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# Testpc
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.195.50", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# CU
_cu = CU(
    instance_id=11272,
    global_bts_id=175,
    backhaul_site_oam_ip=NetworkAddress(v4="10.70.216.135"),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.70.216.2", username="cranuser175", password="systeM!23"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.70.216.135", username="Nemuadmin", password="Nokia@123", port=443
    ),
    f1c=NetworkAddress(
        v4="10.57.251.26",
        vlan_id=2459,
        routing=RoutingInformation(gateway="10.57.251.0", ip_prefix_length=26),
    ),
    f1u=NetworkAddress(
        v4="10.57.251.27",
        vlan_id=2459,
        routing=RoutingInformation(gateway="10.57.251.0", ip_prefix_length=26),
    ),
    ngc=NetworkAddress(
        v4="10.57.234.218",
        vlan_id=2461,
        routing=RoutingInformation(gateway="10.57.234.192", ip_prefix_length=26),
    ),
    ngu=NetworkAddress(
        v4="10.57.234.219",
        vlan_id=2461,
        routing=RoutingInformation(gateway="10.57.234.192", ip_prefix_length=26),
    ),
    x2c=NetworkAddress(
        v4="10.57.251.90",
        vlan_id=2460,
        routing_v4=RoutingInformation(gateway="10.57.251.64/26"),
    ),
    x2u=NetworkAddress(
        v4="10.57.251.91",
        vlan_id=2460,
        routing_v4=RoutingInformation(gateway="10.57.251.64/26"),
    ),
    s1u=NetworkAddress(
        v4="10.57.250.47",
        vlan_id=2452,
        routing_v4=RoutingInformation(gateway="10.57.250.32/27"),
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
    addr="10.70.216.2", username="cranuser175", password="systeM!23", port=22
)
# ssh connection information of OE, for root user
_vcu_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.70.216.2", username="cranuser175", password="systeM!23", port=22
)

_vcu_master_node = MasterNode(
    k8s_connection_details=_vcu_k8s_connection_details,
    ssh_connection_details=_vcu_ssh_connection_details,
)

_vcu_k8s = K8S(namespace="tl175", master_node=_vcu_master_node)

_vcu_k8s_cloud_deployment = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    networks=[_vcu_intnet_1],
    vnfs=[_vcu_cnf_1],
    cloud_hosting=_vcu_k8s,
)


# 5G RU
_ru_pdu1 = HBTE(addr="10.71.196.15", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru1 = RU(
    ru_hw_group="hw_group",
    pdu_port=_ru_pdu1.pdu_ports[5],
    radio_type=RadioTypes.AQQS,
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.40",
        username="serviceuser",
        password="bobuWrUHk7Xq7WPpY9ZcjEi8zNdX3plZ+/y420RZ7W4=",
    ),
)

_ru_pdu2 = HBTE(addr="10.71.196.10", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru1 = RU(
    ru_hw_group="hw_group",
    pdu_port=_ru_pdu2.pdu_ports[3],
    radio_type=RadioTypes.AEQC,
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.50",
        username="serviceuser",
        password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og=",
    ),
)
_ru2 = RU(
    ru_hw_group="hw_group",
    pdu_port=_ru_pdu2.pdu_ports[3],
    radio_type=RadioTypes.AVQQA,
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.50",
        username="serviceuser",
        password="bobuWrUHk7Xq7WPpY9ZcjEi8zNdX3plZ+/y420RZ7W4=",
    ),
)
_ru3 = RU(
    ru_hw_group="hw_group",
    pdu_port=_ru_pdu2.pdu_ports[3],
    radio_type=RadioTypes.AQNA,
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.50",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
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
_fhgw_0 = FHGW(user_config_path=_cfg_dir, rus=[_ru1, _ru2], pxe_server=_pxe_server)
_fhgw_0.ip = "10.71.223.195"
_fhgw_0.username = "toor4nsn"
_fhgw_0.password = "Fhgw@nokia123"
_fhgw_0.version = "22R2"

_ssh_connection_details_0 = SshServiceDetails(
    addr="10.64.167.210", username="core", password="system123"
)
_k8s_connection_details_0 = K8SConnectionDetails(
    ip_addr="10.64.167.210", username="core", password="system123", port="22"
)

_master_node_0 = MasterNode(
    k8s_connection_details=_k8s_connection_details_0,
    ssh_connection_details=_ssh_connection_details_0,
)
_k8s_0 = K8S(namespace="cran1", master_node=_master_node_0)
_vdu_cnf_0 = DeploymentVnfStack(
    name="vdu175",
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
        addr="10.64.167.234", username="Nemuadmin", password="Nokia@123"
    ),
    fhgws=[_fhgw_0],
    instance_id=11272,
    global_bts_id=175,
)

# BTS
_cbts = CloudBts(
    dus=[_du_0],
    cu=_cu,
    cloud_deployment=_vcu_k8s_cloud_deployment,
)

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.71.211.140", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(
    airscale=_real_enb,
    oam_ip="10.71.211.140",
    global_bts_id="175",
)

# #######Iperf########
_appserver_ssh_1 = SshServiceDetails(
    addr="10.57.162.2", username="mmw_sg2", password="mm@2", port="431731"
)

_iperf_1 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh_1,
    network_interface_address="10.57.162.2",
    iperf_path="/system/bin",
    port=421731,
)

# _android_1 for SA, _android_2 for NSA#
# Qualcomm
# CI_Detail_UE_Type='Qualcomm'
_android_1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.218.26", username="nokia5G", password="noki@123"
    ),
    serial_number="94acd6f9",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf_1,
    #capabilities=['REAL_ANDORID_UE', 'QUALCOMM_UE'],
    capabilities=["REAL_ANDROID_UE", "sdx60", "qct_dx50"],
)

_iperf_details = _iperf_1
_appserver = AppServer(_iperf_details)

# Netact
_netact = NetAct(
    https_main_info=HttpConnectionDetails(
        addr="10.82.44.57", username="omc", password="Medsql!_1893"
    ),
)

# TestLine
tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    tl_cloud_topology="CLOUD_5G_AIC_RM17_OCP_FHGW_AEQY",
    enbs=[_lte_real_enb],
    ues=[_android_1],
    nms=_netact,
    appserver=_appserver,
)

__all__ = ["tl"]
