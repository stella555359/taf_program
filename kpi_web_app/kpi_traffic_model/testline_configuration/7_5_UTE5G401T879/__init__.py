__maintainer__ = "lihong"
__team__ = "RAN_PZ_HAZ4_SG07"
__email__ = "liping.hong@nokia-sbell.com"

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
    HBTE,
)
from taf.config.testline import NetworkAddress, RoutingInformation
from taf.config.testline import RealEnb, Airscale, CommonUnit
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC
from taf.config.testline.ue import Qualcomm, QualcommUeType, Android
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
        addr="10.57.167.86", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_tce_pc_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.195.83",
        username="utfuser",
        password="utfadmin!",
        port=49148,
    )
)

_tce_pc_1 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.195.83",
        username="utfuser",
        password="utfadmin!",
        port=49148,
    )
)

# CU
_cu = CU(
    instance_id=879,
    global_bts_id=879,
    backhaul_site_oam_ip=NetworkAddress(v4="10.70.216.141"),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.70.216.2", username="cranuser879", password="systeM!23", port=22
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.70.216.141", username="Nemuadmin", password="Nokia@123", port=443
    ),
    ngc=NetworkAddress(
        v4="10.57.201.150",
        vlan_id=111,
        routing_v4=RoutingInformation(gateway="10.57.201.129/26"),
    ),
    f1c=NetworkAddress(
        v4="10.57.201.22",
        vlan_id=109,
        routing_v4=RoutingInformation(gateway="10.57.201.1/26"),
    ),
    f1u=NetworkAddress(
        v4="10.57.201.23",
        vlan_id=109,
        routing_v4=RoutingInformation(gateway="10.57.201.1/26"),
    ),
    s1u=NetworkAddress(
        v4="10.70.216.25",
        vlan_id=102,
        routing_v4=RoutingInformation(gateway="10.57.188.33/27"),
    ),
    ngu=NetworkAddress(
        v4="10.57.201.151",
        vlan_id=111,
        routing_v4=RoutingInformation(gateway="10.57.201.129/26"),
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
    addr="10.70.216.2", username="cranuser879", password="systeM!23", port=22
)
# ssh connection information of OE, for root user
_vcu_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.70.216.2", username="cranuser879", password="systeM!23", port=22
)

_vcu_master_node = MasterNode(
    k8s_connection_details=_vcu_k8s_connection_details,
    ssh_connection_details=_vcu_ssh_connection_details,
)

_vcu_k8s = K8S(namespace="cran879", master_node=_vcu_master_node)

_vcu_k8s_cloud_deployment = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    networks=[_vcu_intnet_1],
    vnfs=[_vcu_cnf_1],
    cloud_hosting=_vcu_k8s,
)

_attenuator = HBTE(
    ip_addr="10.71.204.214",
    port="5000",
    model="PA-16-16-6-127-0.5-B-S",
    attenuation_port_numbers=[r for r in range(1, 17)],
)

# 5G RU
_ru_pdu_1 = FACOM(addr="10.71.196.34", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_ru_pdu_2 = FACOM(addr="10.71.196.36", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

# 4G RU
_ru_pdu_3 = FACOM(addr="10.71.196.37", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_ru_0 = RU(
    ru_hw_group="pa_initinial",
    pdu_port=_ru_pdu_1.pdu_ports[5],
    radio_type=RadioTypes.AZQJ,
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.35",
        username="rfsw",
        password="5rfS2qmWC0AiFYvir7k8JekCN8/NklqDK5E6OWXuUVQ=",
    ),
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[6],
        _attenuator.attenuator_ports[7],
        _attenuator.attenuator_ports[8],
        _attenuator.attenuator_ports[9],
        _attenuator.attenuator_ports[10],
        _attenuator.attenuator_ports[11],
        _attenuator.attenuator_ports[12],
        _attenuator.attenuator_ports[13],
        _attenuator.attenuator_ports[14],
        _attenuator.attenuator_ports[15],
        _attenuator.attenuator_ports[16],
    ],
)

_ru_1 = RU(
    ru_hw_group="hw_group",
    pdu_port=_ru_pdu_1.pdu_ports[5],
    radio_type=RadioTypes.AZQJ,
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.35",
        username="rfsw",
        password="5rfS2qmWC0AiFYvir7k8JekCN8/NklqDK5E6OWXuUVQ=",
    ),
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
    ],
)

_ru_2 = RU(
    ru_hw_group="hw_group",
    pdu_port=_ru_pdu_1.pdu_ports[1],
    radio_type=RadioTypes.AZQJ,
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.35",
        username="rfsw",
        password="5rfS2qmWC0AiFYvir7k8JekCN8/NklqDK5E6OWXuUVQ=",
    ),
    attenuation_ports=[
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[6],
    ],
)

_pxe_server_ssh_info = SshServiceDetails(
    addr="0.0.0.0", username="ute", password="!Q2w3e4r5t6y7u"
)
_pxe_server = PxeServer(
    nfs_ip="10.71.223.254", ssh_connection_details=_pxe_server_ssh_info
)
# vDU
# FHGW information
_fhgw_0 = FHGW(
    user_config_path=_cfg_dir,
    rus=[_ru_0, _ru_1, _ru_2],
    pxe_server=_pxe_server,
)
_fhgw_0.ip = "0.0.0.0"
_fhgw_0.username = "toor4nsn"
_fhgw_0.password = "Fhgw@nokia123"
_fhgw_0.version = "22R1"


_ssh_connection_details_0 = SshServiceDetails(
    addr="10.64.163.34", username="core", password="system123"
)
_k8s_connection_details_0 = K8SConnectionDetails(
    ip_addr="10.64.163.34", username="core", password="system123", port="22"
)

_master_node_0 = MasterNode(
    k8s_connection_details=_k8s_connection_details_0,
    ssh_connection_details=_ssh_connection_details_0,
)
_k8s_0 = K8S(namespace="tl879", master_node=_master_node_0)
_vdu_cnf_0 = DeploymentVnfStack(
    name="vdu879",
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
    addr="10.64.167.2", username="core", password="system123"
)
_k8s_connection_details_1 = K8SConnectionDetails(
    ip_addr="10.64.167.2", username="core", password="system123", port="22"
)
_master_node_1 = MasterNode(
    k8s_connection_details=_k8s_connection_details_1,
    ssh_connection_details=_ssh_connection_details_1,
)

_k8s_1 = K8S(namespace="tl879du2", master_node=_master_node_1)
_vdu_cnf_1 = DeploymentVnfStack(
    name="vdu879",
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
        addr="10.64.163.66", username="Nemuadmin", password="Nokia@123"
    ),
    fhgws=[_fhgw_0],
    instance_id=879,
    global_bts_id=879,
)

_du_1 = VDU(
    cloud_deployment=_vdu_k8s_cloud_deployment_1,
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.64.167.42", username="Nemuadmin", password="Nokia@123"
    ),
    fhgws=[_fhgw_0],
    instance_id=879,
    global_bts_id=879,
)
# BTS
_cbts = CloudBts(
    dus=[_du_0, _du_1],
    cu=_cu,
    cloud_deployment=_vcu_k8s_cloud_deployment,
)

# BTS Target
# _cbts_1 = CloudBts(
#     dus=[_du_2],
# )


# ENB
_rmod_1 = RU(
    ru_hw_group="",
    pdu_port=_ru_pdu_3.pdu_ports[7],
    attenuation_ports=[
        _attenuator.attenuator_ports[9],
        _attenuator.attenuator_ports[10],
    ],
)

_enb_common_unit = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.71.211.165", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_ru_pdu_3.pdu_ports[7],
)
_lte_real_enb = RealEnb(
    airscale=Airscale(common_units=[_enb_common_unit]),
    rms=[_rmod_1],
    global_bts_id=10447,
    instance_id=10447,
)

# UE
_appserver_ssh = SshServiceDetails(
    addr="10.57.191.238", username="vrf3_sg6", password="vrf3@sg6"
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.238",
    iperf_path="/usr/bin/iperf",
    port=57879,
)

_android_1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.0.176.127", username="mn5gran", password="nokia123@"
    ),
    serial_number="L8K5T19923007058",
    # serial_number="L8K5T19916004089",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "huawei"],
)

_android_2 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.0.176.127", username="mn5gran", password="nokia123@"
    ),
    serial_number="L8K5T19910016408",
    # serial_number="L8K5T19916003909",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "huawei"],
)


# TestLine
tl = TestLine(
    test_pc=_test_pc,
    test_pcs=[_tce_pc_0, _tce_pc_1],
    gnbs=[_cbts],
    tl_cloud_topology="CLOUD_5G_AIC_RM17_OCP_AZQJ",
    enbs=[_lte_real_enb],
    ues=[_android_1, _android_2],
    attenuator=_attenuator,
)

__all__ = ["tl"]
