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
from taf.config.testline.attenuator import (
    AttenuationPort,
    TopYoung,
    HBTE,
)  # added in taf.meta 5.4
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, ATEN, RRB, APC, Gude
from taf.config.testline.core import RealCore, RealCore5GDetails, AMF
from taf.config.testline import NetworkAddress, RoutingInformation
from taf.config.testline import RealEnb, Airscale, CommonUnit
from taf.config.testline import RU, RadioTypes
from taf.config.testline import CloudBts, CU
from taf.config.testline import VDU, FHGW
from taf.config.testline import PxeServer
from taf.config.testline import TestLine
from taf.config.testline import RealEnb
from taf.config.testline import TestPc
from taf.config.testline.ue import Android
from taf.config.testline.appserver import AppServer


__maintainer__ = "Liu Jia"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_3_GMS <I_MN_5G_RAN_IV4_LINE_HZG_3@internal.nsn.com>"
)
__email__ = "jia-rebecca.liu@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))


# Testpc
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.159.19", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# CU

## CU0
_cu_0 = CU(
    instance_id=239,
    global_bts_id=239,
    backhaul_site_oam_ip=NetworkAddress(v4="10.57.180.132"),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.160.2", username="core", password="system123"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.160.132", username="Nemuadmin", password="Nokia@123", port=443
    ),
    x2c=NetworkAddress(
        v4="10.57.190.68",
        vlan_id=110,
        routing=RoutingInformation(gateway="10.57.190.65", ip_prefix_length=26),
    ),
    f1c=NetworkAddress(
        v4="10.57.190.4",
        vlan_id=109,
        routing=RoutingInformation(gateway="10.57.190.1", ip_prefix_length=26),
    ),
    f1u=NetworkAddress(
        v4="10.57.190.5",
        vlan_id=109,
        routing=RoutingInformation(gateway="10.57.190.1", ip_prefix_length=26),
    ),
    s1u=NetworkAddress(
        v4="10.57.160.36",
        vlan_id=102,
        routing=RoutingInformation(gateway="10.57.160.33", ip_prefix_length=27),
    ),
    x2u=NetworkAddress(
        v4="10.57.190.69",
        vlan_id=110,
        routing=RoutingInformation(gateway="10.57.190.65", ip_prefix_length=26),
    ),
    tracing=None,
)

## CU0
_cu_1 = CU(
    instance_id=2392,
    global_bts_id=2392,
    backhaul_site_oam_ip=NetworkAddress(v4="10.57.201.148"),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.70.216.2", username="cranuser239", password="systeM!23"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.70.216.140", username="Nemuadmin", password="Nokia@123", port=443
    ),
    x2c=NetworkAddress(
        v4="10.70.217.84",
        vlan_id=110,
        routing=RoutingInformation(gateway="10.57.201.64", ip_prefix_length=26),
    ),
    f1c=NetworkAddress(
        v4="10.70.217.20",
        vlan_id=109,
        routing=RoutingInformation(gateway="10.57.201.1", ip_prefix_length=26),
    ),
    f1u=NetworkAddress(
        v4="10.70.217.21",
        vlan_id=109,
        routing=RoutingInformation(gateway="10.57.201.1", ip_prefix_length=26),
    ),
    s1u=NetworkAddress(
        v4="10.70.216.44",
        vlan_id=102,
        routing=RoutingInformation(gateway="10.57.188.33", ip_prefix_length=27),
    ),
    x2u=NetworkAddress(
        v4="10.70.217.85",
        vlan_id=110,
        routing=RoutingInformation(gateway="10.57.201.65", ip_prefix_length=26),
    ),
    tracing=None,
)

# cloud_deployment for vCU0
_vcu_cnf_0 = DeploymentVnfStack(
    name="vcu239",
    yaml_file=os.path.join(_cfg_dir, "DEP/gnbs_0/vCU/CU_cnf_values-override.yaml"),
)
_vcu_intnet_0 = DeploymentNetworkStack(
    name=_vcu_cnf_0.name + "-prerequisite",
    yaml_file=os.path.join(_cfg_dir, "DEP/gnbs_0/vCU/CU_pvc_values-override.yaml"),
)

# ssh connection information of OE, for tenant user
_vcu_ssh_connection_details_0 = SshServiceDetails(
    addr="10.57.160.2", username="cranuser239", password="systeM!23", port=22
)
# ssh connection information of OE, for root user
_vcu_k8s_connection_details_0 = K8SConnectionDetails(
    ip_addr="10.57.160.2", username="core", password="system123", port=22
)

_vcu_master_node_0 = MasterNode(
    k8s_connection_details=_vcu_k8s_connection_details_0,
    ssh_connection_details=_vcu_ssh_connection_details_0,
)

_vcu_k8s_0 = K8S(namespace="cran239", master_node=_vcu_master_node_0)

_vcu_k8s_cloud_deployment_0 = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    networks=[_vcu_intnet_0],
    vnfs=[_vcu_cnf_0],
    cloud_hosting=_vcu_k8s_0,
)


# cloud_deployment for vCU1
_vcu_cnf_1 = DeploymentVnfStack(
    name="vcu240",
    yaml_file=os.path.join(_cfg_dir, "DEP/gnbs_1/vCU/CU_cnf_values-override.yaml"),
)
_vcu_intnet_1 = DeploymentNetworkStack(
    name=_vcu_cnf_1.name + "-prerequisite",
    yaml_file=os.path.join(_cfg_dir, "DEP/gnbs_1/vCU/CU_pvc_values-override.yaml"),
)

# ssh connection information of OE, for tenant user
_vcu_ssh_connection_details_1 = SshServiceDetails(
    addr="10.70.216.2", username="cranuser239", password="systeM!23", port=22
)
# ssh connection information of OE, for root user
_vcu_k8s_connection_details_1 = K8SConnectionDetails(
    ip_addr="10.70.216.2", username="core", password="system123", port=22
)

_vcu_master_node_1 = MasterNode(
    k8s_connection_details=_vcu_k8s_connection_details_1,
    ssh_connection_details=_vcu_ssh_connection_details_1,
)

_vcu_k8s_1 = K8S(namespace="cran239", master_node=_vcu_master_node_1)

_vcu_k8s_cloud_deployment_1 = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    networks=[_vcu_intnet_1],
    vnfs=[_vcu_cnf_1],
    cloud_hosting=_vcu_k8s_1,
)

# 5G RU

_hbte_params_0 = {
    "ip_addr": "10.57.230.22",
    "port": 5000,
    "attenuation_port_numbers": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    "model": "PA-16-16-6-127-0.5-B-S",
    "version": None,
}

_attenuator_0 = HBTE(**_hbte_params_0)


_hbte_params_1 = {
    "ip_addr": "10.57.230.21",
    "port": 5000,
    "attenuation_port_numbers": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    "model": "PA-16-16-6-127-0.5-B-S",
    "version": None,
}

_attenuator_1 = HBTE(**_hbte_params_1)

_ru_pdu_0 = FACOM(addr="10.57.246.201", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru_0 = RU(
    ru_hw_group="hw_group",
    pdu_port=_ru_pdu_0.pdu_ports[6],
    radio_type=RadioTypes.AEQP,
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.35",
        username="rfsw",
        password="5rfS2qmWC0AiFYvir7k8JekCN8/NklqDK5E6OWXuUVQ=",
    ),
    attenuation_ports=[
        _attenuator_0.attenuator_ports[1],
        _attenuator_0.attenuator_ports[2],
        _attenuator_0.attenuator_ports[3],
        _attenuator_0.attenuator_ports[4],
    ],
)

_ru_pdu_1 = FACOM(addr="10.57.246.199", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru_1 = RU(
    ru_hw_group="hw_group",
    pdu_port=_ru_pdu_1.pdu_ports[3],
    radio_type=RadioTypes.AEQP,
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.35",
        username="rfsw",
        password="5rfS2qmWC0AiFYvir7k8JekCN8/NklqDK5E6OWXuUVQ=",
    ),
    attenuation_ports=[
        _attenuator_0.attenuator_ports[5],
        _attenuator_0.attenuator_ports[6],
        _attenuator_0.attenuator_ports[7],
        _attenuator_0.attenuator_ports[8],
    ],
)

_ru_pdu_2 = FACOM(addr="10.57.246.201", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru_2 = RU(
    ru_hw_group="hw_group",
    pdu_port=_ru_pdu_1.pdu_ports[4],
    radio_type=RadioTypes.AEQP,
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.35",
        username="rfsw",
        password="5rfS2qmWC0AiFYvir7k8JekCN8/NklqDK5E6OWXuUVQ=",
    ),
    attenuation_ports=[
        _attenuator_0.attenuator_ports[9],
        _attenuator_0.attenuator_ports[10],
        _attenuator_0.attenuator_ports[11],
        _attenuator_0.attenuator_ports[12],
    ],
)

_ru_pdu_3 = FACOM(addr="10.57.246.199", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru_3 = RU(
    ru_hw_group="hw_group",
    pdu_port=_ru_pdu_0.pdu_ports[2],
    radio_type=RadioTypes.AEQP,
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.35",
        username="rfsw",
        password="5rfS2qmWC0AiFYvir7k8JekCN8/NklqDK5E6OWXuUVQ=",
    ),
    attenuation_ports=[
        _attenuator_0.attenuator_ports[13],
        _attenuator_0.attenuator_ports[14],
        _attenuator_0.attenuator_ports[15],
        _attenuator_0.attenuator_ports[16],
    ],
)


_ru_pdu_4 = FACOM(addr="10.57.246.201", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru_4 = RU(
    ru_hw_group="hw_group",
    pdu_port=_ru_pdu_4.pdu_ports[3],
    radio_type=RadioTypes.FXEB,
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.35",
        username="rfsw",
        password="5rfS2qmWC0AiFYvir7k8JekCN8/NklqDK5E6OWXuUVQ=",
    ),
    attenuation_ports=[
        _attenuator_1.attenuator_ports[3],
        _attenuator_1.attenuator_ports[4],
    ],
)

_ru_pdu_5 = FACOM(addr="10.57.246.199", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru_5 = RU(
    ru_hw_group="hw_group",
    pdu_port=_ru_pdu_5.pdu_ports[5],
    radio_type=RadioTypes.FXEB,
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.35",
        username="rfsw",
        password="5rfS2qmWC0AiFYvir7k8JekCN8/NklqDK5E6OWXuUVQ=",
    ),
    attenuation_ports=[
        _attenuator_1.attenuator_ports[1],
        _attenuator_1.attenuator_ports[2],
    ],
)

_ru_pdu_6 = FACOM(addr="10.57.246.201", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru_6 = RU(
    ru_hw_group="hw_group",
    pdu_port=_ru_pdu_6.pdu_ports[1],
    radio_type=RadioTypes.FXEB,
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.35",
        username="rfsw",
        password="5rfS2qmWC0AiFYvir7k8JekCN8/NklqDK5E6OWXuUVQ=",
    ),
    attenuation_ports=[
        _attenuator_1.attenuator_ports[5],
        _attenuator_1.attenuator_ports[6],
    ],
)

_ru_pdu_7 = FACOM(addr="10.57.176.142", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_ru_7 = RU(
    ru_hw_group="hw_group",
    pdu_port=_ru_pdu_7.pdu_ports[6],
    radio_type=RadioTypes.AHFIB,
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.35",
        username="rfsw",
        password="5rfS2qmWC0AiFYvir7k8JekCN8/NklqDK5E6OWXuUVQ=",
    ),
    attenuation_ports=[
        _attenuator_1.attenuator_ports[7],
        _attenuator_1.attenuator_ports[8],
    ],
)

# vDU
_pxe_server_ssh_info = SshServiceDetails(
    addr="10.71.223.254", username="ute", password="!Q2w3e4r5t6y7u"
)
_pxe_server = PxeServer(
    nfs_ip="10.71.223.254", ssh_connection_details=_pxe_server_ssh_info
)

## vDU0
# FHGW information
_fhgw_0 = FHGW(
    user_config_path=_cfg_dir,
    rus=[_ru_0, _ru_1, _ru_4, _ru_5, _ru_6],
    pxe_server=_pxe_server,
)

_fhgw_0.ip = "10.71.222.155"
_fhgw_0.username = "toor4nsn"
_fhgw_0.password = "Fhgw@nokia123"
_fhgw_0.version = "23R2"

_ssh_connection_details_0 = SshServiceDetails(
    addr="10.57.184.18", username="core", password="system123"
)
_k8s_connection_details_0 = K8SConnectionDetails(
    ip_addr="10.57.184.18", username="core", password="system123", port="22"
)

_master_node_0 = MasterNode(
    k8s_connection_details=_k8s_connection_details_0,
    ssh_connection_details=_ssh_connection_details_0,
)
_k8s_0 = K8S(namespace="cran1", master_node=_master_node_0)
_vdu_cnf_0 = DeploymentVnfStack(
    name="vdu2391",
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
        addr="10.57.184.58", username="Nemuadmin", password="Nokia@123"
    ),
    fhgws=[_fhgw_0],
    instance_id=239,
    global_bts_id=239,
)

## vDU1
# FHGW information
_fhgw_1 = FHGW(user_config_path=_cfg_dir, rus=[_ru_2], pxe_server=_pxe_server)
_fhgw_1.ip = "10.71.222.155"
_fhgw_1.username = "toor4nsn"
_fhgw_1.password = "Fhgw@nokia123"
_fhgw_1.version = "23R2"

_ssh_connection_details_1 = SshServiceDetails(
    addr="10.57.184.98", username="core", password="system123"
)
_k8s_connection_details_1 = K8SConnectionDetails(
    ip_addr="10.57.184.98", username="core", password="system123", port="22"
)

_master_node_1 = MasterNode(
    k8s_connection_details=_k8s_connection_details_1,
    ssh_connection_details=_ssh_connection_details_1,
)
_k8s_1 = K8S(namespace="cran1", master_node=_master_node_1)
_vdu_cnf_1 = DeploymentVnfStack(
    name="vdu2392",
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

_du_1 = VDU(
    cloud_deployment=_vdu_k8s_cloud_deployment_1,
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.184.90", username="Nemuadmin", password="Nokia@123"
    ),
    fhgws=[_fhgw_1],
    instance_id=239,
    global_bts_id=239,
)

## vDU2
# FHGW information
_fhgw_2 = FHGW(user_config_path=_cfg_dir, rus=[_ru_3, _ru_7], pxe_server=_pxe_server)
_fhgw_2.ip = "10.71.222.155"
_fhgw_2.username = "toor4nsn"
_fhgw_2.password = "Fhgw@nokia123"
_fhgw_2.version = "23R2"

_ssh_connection_details_2 = SshServiceDetails(
    addr="10.57.170.66", username="core", password="system123"
)
_k8s_connection_details_2 = K8SConnectionDetails(
    ip_addr="10.57.170.66", username="core", password="system123", port="22"
)

_master_node_2 = MasterNode(
    k8s_connection_details=_k8s_connection_details_2,
    ssh_connection_details=_ssh_connection_details_2,
)
_k8s_2 = K8S(namespace="cran1", master_node=_master_node_2)
_vdu_cnf_2 = DeploymentVnfStack(
    name="vdu2393",
    yaml_file=os.path.join(_cfg_dir, "DEP/gnbs_1/vDU_0/DU_cnf_values-override.yaml"),
)
_vdu_intnet_2 = DeploymentNetworkStack(
    name=_vdu_cnf_2.name + "-prerequisite",
    yaml_file=os.path.join(_cfg_dir, "DEP/gnbs_1/vDU_0/DU_pvc_values-override.yaml"),
)

_vdu_k8s_cloud_deployment_2 = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    cloud_hosting=_k8s_2,
    networks=[_vdu_intnet_2],
    vnfs=[_vdu_cnf_2],
)

_du_2 = VDU(
    cloud_deployment=_vdu_k8s_cloud_deployment_2,
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.170.90", username="Nemuadmin", password="Nokia@123"
    ),
    fhgws=[_fhgw_2],
    instance_id=2392,
    global_bts_id=2392,
)

# BTS
_cbts_0 = CloudBts(
    dus=[_du_0, _du_1],
    cu=_cu_0,
    cloud_deployment=_vcu_k8s_cloud_deployment_0,
)

_cbts_1 = CloudBts(
    dus=[_du_2],
    cu=_cu_1,
    cloud_deployment=_vcu_k8s_cloud_deployment_1,
)

## ENB ##
_common_unit_0 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.227.40", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
)

_real_enb_0 = Airscale(common_units=[_common_unit_0])

_lte_real_enb_0 = RealEnb(
    airscale=_real_enb_0,
    oam_ip="10.57.227.40",
    instance_id=10902,
    global_bts_id="10902",
)

_common_unit_1 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.227.41", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
)

_real_enb_1 = Airscale(common_units=[_common_unit_1])

_lte_real_enb_1 = RealEnb(
    airscale=_real_enb_0,
    oam_ip="10.57.227.41",
    instance_id=10903,
    global_bts_id="10903",
)

_appserver_ssh = SshServiceDetails(
    addr="10.57.191.245",
    username="vrf4_sg3",
    password="Haz4_vrf_sg3",
    port="53139",
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.245",
    iperf_path="/usr/bin/iperf",
    port="53239",
)
_appserver = AppServer(_iperf)

## UE
_android_0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.109", username="mn5gran", password="nokia123@"
    ),
    serial_number="R3CW10X29EJ",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="/cygdrive/c/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "samsung_vran20"],
)

_android_1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.109", username="mn5gran", password="nokia123@"
    ),
    serial_number="R5CT310BSKF",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="/cygdrive/c/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "samsung_vran20"],
)

_android_2 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.109", username="mn5gran", password="nokia123@"
    ),
    serial_number="R5CT34DPQMF",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="/cygdrive/c/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "samsung_vran20"],
)

_android_3 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.109", username="mn5gran", password="nokia123@"
    ),
    serial_number="R5CT34E5FJR",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="/cygdrive/c/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "samsung_vran20"],
)

_android_4 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.109", username="mn5gran", password="nokia123@"
    ),
    serial_number="RFCW211X0JD",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="/cygdrive/c/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "samsung_vran20"],
)

_android_5 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.109", username="mn5gran", password="nokia123@"
    ),
    serial_number="347d5507",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="/cygdrive/c/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "Xiaomi"],
)

_android_6 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.109", username="mn5gran", password="nokia123@"
    ),
    serial_number="7d12fa93",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="/cygdrive/c/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "Xiaomi"],
)

_android_7 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.109", username="mn5gran", password="nokia123@"
    ),
    serial_number="RFCW314PJGP",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="/cygdrive/c/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "Redmi"],
)

_android_8 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.109", username="mn5gran", password="nokia123@"
    ),
    serial_number="R5CR10CBRKR",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="/cygdrive/c/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "samsung_vran20"],
)

_android_9 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.109", username="mn5gran", password="nokia123@"
    ),
    serial_number="RFCR40JH7RF",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="/cygdrive/c/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "samsung_vran20"],
)

_android_10 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.109", username="mn5gran", password="nokia123@"
    ),
    serial_number="RFCT30TT7SK",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="/cygdrive/c/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "samsung_vran20"],
)

_android_11 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.109", username="mn5gran", password="nokia123@"
    ),
    serial_number="R5CT413KT3A",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="/cygdrive/c/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "samsung_vran20"],
)

_android_12 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.109", username="mn5gran", password="nokia123@"
    ),
    serial_number="RFCW20HK02H",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="/cygdrive/c/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "samsung_vran20"],
)

_android_13 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.109", username="mn5gran", password="nokia123@"
    ),
    serial_number="RFCW20HNPSF",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="/cygdrive/c/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "samsung_vran20"],
)

# RealCore
_amf_ssh = SshServiceDetails(
    addr="to_be_updated", username="to_be_updated", password="to_be_updated"
)

_amf_n2_addr = NetworkAddress(v4="10.110.66.198", v6="to_be_updated", vlan_id=None)

_amf = AMF(oam_ssh_connection_details=_amf_ssh, n2=_amf_n2_addr)

_core = RealCore(five_g=RealCore5GDetails(amf=_amf), mcc="460", mnc="02")


# TestLine
tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts_0, _cbts_1],
    core=_core,
    ues=[
        _android_0,
        _android_1,
        _android_2,
        _android_3,
        _android_4,
        _android_5,
        _android_6,
        _android_7,
        _android_8,
        _android_9,
        _android_10,
        _android_11,
        _android_12,
        _android_13
    ],
    tl_cloud_topology="CLOUD_5G_AIC_RM17_OCP_AZQJ",
    enbs=[_lte_real_enb_0, _lte_real_enb_1],
    attenuator=[_attenuator_0, _attenuator_1],
    appserver=_appserver,
)
