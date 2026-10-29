__maintainer__ = "zhao nana"
__team__ = "RAN_PZ_HAZ3_SG02"
__email__ = "nana.zhao@nokia-sbell.com"

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
        addr="10.101.60.61", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# CU
_cu = CU(
    instance_id=11164,
    global_bts_id=11164,
    backhaul_site_oam_ip=NetworkAddress(v4="10.57.179.18"),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.171.130", username="tl173", password="systeM!23"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.173.19", username="Nemuadmin", password="Nokia@123", port=443
    ),
    f1c=NetworkAddress(
        v4="10.57.174.34",
        vlan_id=2559,
        routing=RoutingInformation(gateway="10.57.174.1", ip_prefix_length=26),
    ),
    f1u=NetworkAddress(
        v4="10.57.174.35",
        vlan_id=2559,
        routing=RoutingInformation(gateway="10.57.174.1", ip_prefix_length=26),
    ),
    ngc=NetworkAddress(
        v4="10.57.174.162",
        vlan_id=2561,
        routing=RoutingInformation(gateway="10.57.174.129", ip_prefix_length=26),
    ),
    ngu=NetworkAddress(
        v4="10.57.174.163",
        vlan_id=2561,
        routing=RoutingInformation(gateway="10.57.174.129", ip_prefix_length=26),
    ),
    x2c=NetworkAddress(
        v4="10.57.174.98",
        vlan_id=2560,
        routing_v4=RoutingInformation(gateway="10.57.174.64/26"),
    ),
    x2u=NetworkAddress(
        v4="10.57.174.99",
        vlan_id=2560,
        routing_v4=RoutingInformation(gateway="10.57.174.64/26"),
    ),
    s1u=NetworkAddress(
        v4="10.57.173.52",
        vlan_id=2552,
        routing_v4=RoutingInformation(gateway="10.57.173.32/27"),
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
    addr="10.57.171.130", username="tl173", password="systeM!23", port=22
)
# ssh connection information of OE, for root user
_vcu_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.57.171.130", username="tl173", password="systeM!23", port=22
)

_vcu_master_node = MasterNode(
    k8s_connection_details=_vcu_k8s_connection_details,
    ssh_connection_details=_vcu_ssh_connection_details,
)

_vcu_k8s = K8S(namespace="tl173", master_node=_vcu_master_node)

_vcu_k8s_cloud_deployment = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    networks=[_vcu_intnet_1],
    vnfs=[_vcu_cnf_1],
    cloud_hosting=_vcu_k8s,
)


# 5G RU
_ru_pdu1 = TopYoung(addr="10.71.196.15", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru1 = RU(
    ru_hw_group="hw_group",
    pdu_port=_ru_pdu1.pdu_ports[3],
    radio_type=RadioTypes.AQQQA,
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.40",
        username="rfsw",
        password="3Is6ezFJ7dFlB29cgs0yp3RCM3fUF1zNO1+6Z08tlAc=",
    ),
)

_ru_pdu2 = TopYoung(addr="10.71.196.15", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru2 = RU(
    ru_hw_group="hw_group",
    pdu_port=_ru_pdu2.pdu_ports[2],
    radio_type=RadioTypes.AQQQA,
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.50",
        username="rfsw",
        password="3Is6ezFJ7dFlB29cgs0yp3RCM3fUF1zNO1+6Z08tlAc=",
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
_fhgw_0.username = "robot"
_fhgw_0.password = "robot"
_fhgw_0.version = "23R3"

_ssh_connection_details_0 = SshServiceDetails(
    addr="10.71.223.210", username="core", password="system123"
)
_k8s_connection_details_0 = K8SConnectionDetails(
    ip_addr="10.71.223.210", username="core", password="system123", port="22"
)

_master_node_0 = MasterNode(
    k8s_connection_details=_k8s_connection_details_0,
    ssh_connection_details=_ssh_connection_details_0,
)
_k8s_0 = K8S(namespace="vducran", master_node=_master_node_0)
_vdu_cnf_0 = DeploymentVnfStack(
    name="vdu173",
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
        addr="10.64.160.66", username="Nemuadmin", password="Nokia@123"
    ),
    fhgws=[_fhgw_0],
    instance_id=11164,
    global_bts_id=11164,
)

# BTS
_cbts = CloudBts(
    dus=[_du_0],
    cu=_cu,
    cloud_deployment=_vcu_k8s_cloud_deployment,
)

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.71.211.98", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(
    airscale=_real_enb,
    oam_ip="10.71.211.98",
    global_bts_id="170",
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
        addr="10.71.217.214", username="nokia5G", password="noki@123"
    ),
    serial_number="R5CRB2HTAZT",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf_1,
    capabilities=["samsungS21", "samsung_vran20"],
)

_appserver_ssh_2 = SshServiceDetails(
    addr="10.57.162.2", username="mmw_sg2", password="mm@2", port="431732"
)

_iperf_2 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh_2,
    network_interface_address="10.57.162.2",
    iperf_path="/system/bin",
    port=421732,
)

# Qualcomm
# CI_Detail_UE_Type='Qualcomm'
_android_2 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.217.214", username="nokia5G", password="noki@123"
    ),
    serial_number="R5CR92YZH5D",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf_2,
    capabilities=["qct_dx50", "samsung_vran20"],
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
    ues=[_android_1, _android_2],
    nms=_netact,
    appserver=_appserver,
)

__all__ = ["tl"]
