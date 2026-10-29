__maintainer__ = "li yajie"
__team__ = "RAN_PZ_HAZ4_SG01"
__email__ = "yajie.li@nokia-sbell.com"

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
from taf.config.testline import RU, RadioTypes
from taf.config.testline import CloudBts, CU
from taf.config.testline import VDU, FHGW
from taf.config.testline import PxeServer
from taf.config.testline import TestLine
from taf.config.testline import RealEnb
from taf.config.testline import TestPc
from taf.config.testline import VDU, RANNIC
from taf.config.testline.attenuator import HBTE
from taf.config.testline.pdu import HBTE as PBHBTE
from taf.config.testline.pdu import TopYoung, FACOM
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.ue import Airphone, Qualcomm, QualcommUeType, Android, MediaTek
from taf.config.testline.appserver import AppServer
from taf.config.testline import LicenseKeeper

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# Testpc
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.195.118", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# CU
_cu = CU(
    instance_id=2238,
    global_bts_id=36971,
    backhaul_site_oam_ip=NetworkAddress(v4="10.57.191.154"),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.191.2", username="cranuser2238", password="systeM!23"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.191.154", username="Nemuadmin", password="nemuuser", port=443
    ),
    x2c=NetworkAddress(
        v4="10.57.192.112",
        vlan_id=110,
        routing=RoutingInformation(gateway="10.57.192.65", ip_prefix_length=26),
    ),
    f1c=NetworkAddress(
        v4="10.57.192.48",
        vlan_id=109,
        routing=RoutingInformation(gateway="10.57.192.1", ip_prefix_length=26),
    ),
    f1u=NetworkAddress(
        v4="10.57.192.49",
        vlan_id=109,
        routing=RoutingInformation(gateway="10.57.192.1", ip_prefix_length=26),
    ),
    s1u=NetworkAddress(
        v4="10.57.191.58",
        vlan_id=102,
        routing=RoutingInformation(gateway="10.57.191.33", ip_prefix_length=27),
    ),
    x2u=NetworkAddress(
        v4="10.57.192.113",
        vlan_id=110,
        routing=RoutingInformation(gateway="10.57.192.65", ip_prefix_length=26),
    ),
    tracing=NetworkAddress(
        v4="10.57.191.90",
        vlan_id=103,
        routing_v4=RoutingInformation(gateway="10.57.191.65/27"),
    ),
)

# cloud_deployment for vCU
# _vcu_cnf_1 = DeploymentVnfStack(
#     name="tl2221",
#     yaml_file=os.path.join(_cfg_dir, "DEP/gnbs_0/vCU/CU_cnf_values-override.yaml"),
# )
# _vcu_intnet_1 = DeploymentNetworkStack(
#     name=_vcu_cnf_1.name + "-prerequisite",
#     yaml_file=os.path.join(_cfg_dir, "DEP/gnbs_0/vCU/CU_pvc_values-override.yaml"),
# )

# ssh connection information of OE, for tenant user
_vcu_ssh_connection_details = SshServiceDetails(
    addr="10.57.191.2", username="cranuser2238", password="systeM!23", port=22
)

# ssh connection information of OE, for root user
_vcu_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.57.191.2", username="core", password="system123", port=22
)

_vcu_master_node = MasterNode(
    k8s_connection_details=_vcu_k8s_connection_details,
    ssh_connection_details=_vcu_ssh_connection_details,
)

_vcu_k8s = K8S(namespace="cran2238", master_node=_vcu_master_node)

_cnf_cu_1 = HelmChart(
    name="vcu2238",
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
_ru1_pdu = TopYoung(addr="10.71.196.178", port_numbers=[5])
_ru2_pdu = TopYoung(addr="10.71.196.178", port_numbers=[1])
_ru3_pdu = PBHBTE(addr="10.71.196.177", port_numbers=[1])
_ru4_pdu = TopYoung(addr="10.71.196.176", port_numbers=[3])
_ru5_pdu = PBHBTE(addr="10.71.196.185", port_numbers=[3])
_ru6_pdu = PBHBTE(addr="10.71.196.185", port_numbers=[5])
_ru7_pdu = PBHBTE(addr="10.71.196.185", port_numbers=[6])
_ru8_pdu = PBHBTE(addr="10.71.196.185", port_numbers=[7])
_ru9_pdu = FACOM(addr="10.71.196.179", port_numbers=[8])
#_ru10_pdu = PBHBTE(addr="10.71.196.185", port_numbers=[6])
#_ru11_pdu = PBHBTE(addr="10.71.196.185", port_numbers=[7])
#_ru12_pdu = FACOM(addr="10.71.196.179", port_numbers=[8])
#_ru13_pdu = PBHBTE(addr="10.71.196.185", port_numbers=[2])
# _ru14_pdu = PBHBTE(addr="10.71.196.185", port_numbers=[4])

_ru1 = RU(
    ru_hw_group="hw_group",
    pdu_port=_ru1_pdu.pdu_ports[5],
    radio_type=RadioTypes.AVQE,
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.35",
        username="serviceuser",
        password="bobuWrUHk7Xq7WPpY9ZcjEi8zNdX3plZ+/y420RZ7W4=",
    ),
)

_ru2 = RU(
    ru_hw_group="hw_group",
    pdu_port=_ru2_pdu.pdu_ports[1],
    radio_type=RadioTypes.AVQQA,
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.36",
        username="serviceuser",
        password="bobuWrUHk7Xq7WPpY9ZcjEi8zNdX3plZ+/y420RZ7W4=",
    ),
)

_ru3 = RU(
    ru_hw_group="hw_group",
    pdu_port=_ru3_pdu.pdu_ports[1],
    radio_type=RadioTypes.AVQE,
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.37",
        username="serviceuser",
        password="bobuWrUHk7Xq7WPpY9ZcjEi8zNdX3plZ+/y420RZ7W4=",
    ),
)

_ru4 = RU(
    ru_hw_group="hw_group",
    pdu_port=_ru4_pdu.pdu_ports[3],
    radio_type=RadioTypes.AVQL,
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.38",
        username="serviceuser",
        password="bobuWrUHk7Xq7WPpY9ZcjEi8zNdX3plZ+/y420RZ7W4=",
    ),
)

_ru5 = RU(
    ru_hw_group="hw_group",
    pdu_port=_ru5_pdu.pdu_ports[3],
    radio_type=RadioTypes.AWHQX,
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.39",
        username="serviceuser",
        password="bobuWrUHk7Xq7WPpY9ZcjEi8zNdX3plZ+/y420RZ7W4=",
    ),
)

_ru6 = RU(
    ru_hw_group="hw_group",
    pdu_port=_ru6_pdu.pdu_ports[5],
    radio_type=RadioTypes.AWHQX,
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.40",
        username="serviceuser",
        password="bobuWrUHk7Xq7WPpY9ZcjEi8zNdX3plZ+/y420RZ7W4=",
    ),
 )

_ru7 = RU(
    ru_hw_group="hw_group",
    pdu_port=_ru7_pdu.pdu_ports[6],
    radio_type=RadioTypes.AWHQX,
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.41",
        username="serviceuser",
        password="bobuWrUHk7Xq7WPpY9ZcjEi8zNdX3plZ+/y420RZ7W4=",
    ),
)

_ru8 = RU(
    ru_hw_group="hw_group",
    pdu_port=_ru8_pdu.pdu_ports[7],
    radio_type=RadioTypes.AWHQX,
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.42",
        username="serviceuser",
        password="bobuWrUHk7Xq7WPpY9ZcjEi8zNdX3plZ+/y420RZ7W4=",
    ),
)

_ru9 = RU(
    ru_hw_group="hw_group",
    pdu_port=_ru9_pdu.pdu_ports[8],
    radio_type=RadioTypes.AWHQX,
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.43",
        username="serviceuser",
        password="bobuWrUHk7Xq7WPpY9ZcjEi8zNdX3plZ+/y420RZ7W4=",
    ),
)

#_ru10 = RU(
#    ru_hw_group="hw_group",
#    pdu_port=_ru10_pdu.pdu_ports[6],
#    radio_type=RadioTypes.AWHQX,
#    default_ssh_connection_details=SshServiceDetails(
#        addr="192.168.254.44",
#        username="serviceuser",
#        password="bobuWrUHk7Xq7WPpY9ZcjEi8zNdX3plZ+/y420RZ7W4=",
#    ),
#)

#_ru11 = RU(
#    ru_hw_group="hw_group",
#    pdu_port=_ru11_pdu.pdu_ports[7],
#    radio_type=RadioTypes.AWHQX,
#    default_ssh_connection_details=SshServiceDetails(
#        addr="192.168.254.45",
#        username="serviceuser",
#        password="bobuWrUHk7Xq7WPpY9ZcjEi8zNdX3plZ+/y420RZ7W4=",
#    ),
#)

#_ru12 = RU(
#    ru_hw_group="hw_group",
#    pdu_port=_ru12_pdu.pdu_ports[8],
#    radio_type=RadioTypes.AWHQX,
#    default_ssh_connection_details=SshServiceDetails(
#        addr="192.168.254.46",
#        username="serviceuser",
#        password="bobuWrUHk7Xq7WPpY9ZcjEi8zNdX3plZ+/y420RZ7W4=",
#    ),
#)

#_ru13 = RU(
#    ru_hw_group="hw_group",
#    pdu_port=_ru13_pdu.pdu_ports[2],
#    radio_type=RadioTypes.AWHQX,
#    default_ssh_connection_details=SshServiceDetails(
#        addr="192.168.254.47",
#        username="serviceuser",
#        password="bobuWrUHk7Xq7WPpY9ZcjEi8zNdX3plZ+/y420RZ7W4=",
#    ),
#)

# _ru14 = RU(
#    ru_hw_group="hw_group",
#    pdu_port=_ru14_pdu.pdu_ports[4],
#    radio_type=RadioTypes.AWHQX,
#    default_ssh_connection_details=SshServiceDetails(
#        addr="192.168.254.48",
#        username="serviceuser",
#        password="bobuWrUHk7Xq7WPpY9ZcjEi8zNdX3plZ+/y420RZ7W4=",
#    ),
# )

# FHGW information
# _pxe_server_ssh_info = SshServiceDetails(
#     addr="0.0.0.0", username="root", password="centos"
# )
# _pxe_server = PxeServer(nfs_ip="0.0.0.0", ssh_connection_details=_pxe_server_ssh_info)
#
# _fhgw_0 = FHGW(user_config_path=_cfg_dir, rus=[_ru, _ru2], pxe_server=_pxe_server)
# _fhgw_0.ip = "10.71.222.147"
# _fhgw_0.username = "toor4nsn"
# _fhgw_0.password = "Fhgw@nokia123"
# _fhgw_0.version = "22R3"


# vDU
# RANNIC information
_rannic_0 = RANNIC(serial_number="L1240808935", product_code="AF1791.101")
_rannic_1 = RANNIC(serial_number="L1242707765", product_code="AF1791.102")

_ssh_connection_details_0 = SshServiceDetails(
    addr="10.0.181.130", username="cranuser2238", password="systeM!23"
)
_k8s_connection_details_0 = K8SConnectionDetails(
    ip_addr="10.0.181.130", username="core", password="system123", port="22"
)

_master_node_0 = MasterNode(
    k8s_connection_details=_k8s_connection_details_0,
    ssh_connection_details=_ssh_connection_details_0,
)

_k8s_0 = K8S(namespace="cran2238", master_node=_master_node_0)


# _vdu_cnf_0 = DeploymentVnfStack(
#     name="vdutest",
#     yaml_file=os.path.join(_cfg_dir, "DEP/gnbs_0/vDU_0/DU_cnf_values-override.yaml"),
# )
#
# _vdu_intnet_0 = DeploymentNetworkStack(
#     name=_vdu_cnf_0.name + "-prerequisite",
#     yaml_file=os.path.join(_cfg_dir, "DEP/gnbs_0/vDU_0/DU_pvc_values-override.yaml"),
# )
#
# _vdu_k8s_cloud_deployment_0 = CloudDeployment(
#     default_cfg_dir=_cfg_dir,
#     cloud_hosting=_k8s_0,
#     networks=[_vdu_intnet_0],
#     vnfs=[_vdu_cnf_0],
# )

_cnf_du_0 = HelmChart(
    name="cran2238",
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
        addr="10.0.181.154", username="Nemuadmin", password="nemuuser", port=443
    ),
    rus=[
        _ru1,
        _ru2,
        _ru3,
        _ru4,
        _ru5,
        _ru6,
        _ru7,
        _ru8,
        _ru9,
    #    _ru10,
    #    _ru11,
    #    _ru12,
        #       _ru13,
        #       _ru14,
    ],
    # fhgws=[_fhgw_0],
    instance_id=2238,
    global_bts_id=36971,
)

# BTS
_cbts = CloudBts(
    dus=[_du_0],
    cu=_cu,
    cloud_deployment=_vcu_k8s_cloud_deployment,
)


# UL traffic: ${tl.appserver.iperf_details.port}

_appserver2_ssh = SshServiceDetails(
    addr="10.71.217.200", username="MN5GRAN", password="nokia123@"
)

# ${EPC_IP}=${tl.appserver.iperf_details.network_interface_address}
_iperf_details_on_appserver2 = IperfDataTransferDetails(
    ssh_connection_details=_appserver2_ssh,
    network_interface_address="10.71.207.142",
    iperf_path="/usr/bin/iperf",
    port="51100",
)

_appserver = AppServer(_iperf_details_on_appserver2)


# DL traffic:  ${tl.ues[${ue_index}].iperf_details.port}
_appserver_ssh = SshServiceDetails(
    addr="10.71.207.142",
    username="vrf4_sg1",
    password="vrf4@sg1",
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.207.142",
    iperf_path="iperf",
    port=51001,
)
# spark license
_licensekeeper = LicenseKeeper(username="HAZ4_SG1", password="HAZ4_SG1")


# SA   CI_Detail_UE_Type='Huawei Mate 30 Pro 5G'
_sigspark = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.217.200", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="9YS0220108006550",
    server_dir="C:/Program Files (x86)/Spark/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="460028001006215",
    capabilities=["huawei_sigspark"],
    licensekeeper=_licensekeeper,
)


# TestLine
tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    tl_cloud_topology="CLOUD_5G_AIC_OCP",
    ues=[_sigspark],
    appserver=_appserver,
)

__all__ = ["tl"]
