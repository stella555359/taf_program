__maintainer__ = "Liu Shasha"
__team__ = "shasha.liu"
__email__ = "shasha.liu@nokia-sbell.com"
__owner_email__ = "shasha.liu@nokia-sbell.com"

import os

from taf.config.testline.cloud_hosting import (
    ControlNode,
    NCIR,
    CloudDeployment,
    DeploymentFlavorStack,
    DeploymentNetworkStack,
    DeploymentVnfStack,
)
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.core import RealCore
from taf.config.testline.gnb.du import DU, VDU, FHGW
from taf.config.testline.pdu import HBTE, TopYoung
from taf.config.testline.lab_infrastructure import PxeServer
from taf.config.testline.connection_details import K8SConnectionDetails
from taf.config.testline.cloud_hosting import MasterNode, K8S
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb.gnb import CloudBts, CU
from taf.config.testline.enb import RealEnb
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import Qualcomm, QualcommUeType, Android
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.config.testline.attenuator import AttenuationPort, HBTE
from taf.config.testline.gnb.networkaddress import NetworkAddress, RoutingInformation
from taf.config.testline.radio import RU, RadioModule, RadioTypes
from taf.config.testline.appserver import AppServer
from taf.config.testline.core import EPCSim

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# Testpc
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.101.60.26", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# CU
_cu = CU(
    instance_id=2369,
    global_bts_id=2369,
    backhaul_site_oam_ip=NetworkAddress(v4="10.57.173.12"),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.171.130", username="core", password="system123"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.173.12", username="Nemuadmin", password="nemuuser", port=443
    ),
    x2c=NetworkAddress(
        v4="10.57.173.148",
        vlan_id=2551,
        routing_v4=RoutingInformation(
            gateway="10.57.173.128", destIpAddr="10.57.173.148/26"
        ),
    ),
    f1c=NetworkAddress(
        v4="10.57.173.84",
        vlan_id=2550,
        routing_v4=RoutingInformation(
            gateway="10.57.173.64", destIpAddr="10.57.173.84/26"
        ),
    ),
    f1u=NetworkAddress(
        v4="10.57.173.85",
        vlan_id=2550,
        routing_v4=RoutingInformation(
            gateway="10.57.173.64", destIpAddr="10.57.173.85/26"
        ),
    ),
    s1u=NetworkAddress(
        v4="10.57.173.213",
        vlan_id=2552,
        routing_v4=RoutingInformation(
            gateway="10.57.173.192", destIpAddr="10.57.173.213/26"
        ),
    ),
    x2u=NetworkAddress(
        v4="10.57.173.149",
        vlan_id=2551,
        routing_v4=RoutingInformation(
            gateway="10.57.173.128", destIpAddr="10.57.173.149/26"
        ),
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
    addr="10.57.171.130", username="core", password="system123", port=22
)
# ssh connection information of OE, for root user
_vcu_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.57.171.130", username="core", password="system123", port=22
)

_vcu_master_node = MasterNode(
    k8s_connection_details=_vcu_k8s_connection_details,
    ssh_connection_details=_vcu_ssh_connection_details,
)

_vcu_k8s = K8S(namespace="tl469", master_node=_vcu_master_node)

_vcu_k8s_cloud_deployment = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    networks=[_vcu_intnet_1],
    vnfs=[_vcu_cnf_1],
    cloud_hosting=_vcu_k8s,
)


# 5G RU
_ru1_pdu = TopYoung(addr="10.71.196.199", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru1 = RU(
    ru_hw_group="below6GHz",
    pdu_port=_ru1_pdu.pdu_ports[2],
    radio_type=RadioTypes.AZQI,
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.35",
        username="rfsw",
        password="5rfS2qmWC0AiFYvir7k8JekCN8/NklqDK5E6OWXuUVQ=",
    ),
)

_ru2_pdu = TopYoung(addr="10.71.196.199", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru2 = RU(
    ru_hw_group="below6GHz",
    pdu_port=_ru2_pdu.pdu_ports[1],
    radio_type=RadioTypes.AZQJ,
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.33",
        username="rfsw",
        password="5rfS2qmWC0AiFYvir7k8JekCN8/NklqDK5E6OWXuUVQ=",
    ),
)

# _cloud_deployment = CloudDeployment()

# vDU
_pxe_server_ssh_info = SshServiceDetails(
    addr="10.71.223.254", username="ute", password="!Q2w3e4r5t6y7u"
)
_pxe_server = PxeServer(
    nfs_ip="10.71.223.254", ssh_connection_details=_pxe_server_ssh_info
)

# FHGW information
_fhgw_0 = FHGW(user_config_path=_cfg_dir, rus=[_ru1, _ru2], pxe_server=_pxe_server)
_fhgw_0.ip = "10.64.161.57"
_fhgw_0.username = "toor4nsn"
_fhgw_0.password = "Fhgw@nokia123"
_fhgw_0.version = "22R3"

_ssh_connection_details_0 = SshServiceDetails(
    addr="10.64.161.18", username="core", password="system123"
)
_k8s_connection_details_0 = K8SConnectionDetails(
    ip_addr="10.64.161.18", username="core", password="system123", port="22"
)

_master_node_0 = MasterNode(
    k8s_connection_details=_k8s_connection_details_0,
    ssh_connection_details=_ssh_connection_details_0,
)
_k8s_0 = K8S(namespace="tl469", master_node=_master_node_0)

_vdu_cnf_0 = DeploymentVnfStack(
    name="vdutest",
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
        addr="10.64.161.210", username="Nemuadmin", password="nemuuser"
    ),
    fhgws=[_fhgw_0],
    instance_id=2369,
    global_bts_id=2369,
)

# BTS
_cbts = CloudBts(
    dus=[_du_0],
    cu=_cu,
    cloud_deployment=_vcu_k8s_cloud_deployment,
    #    vnf_name="hgz-tl469",
)

# _ncir = NCIR(compute_nodes=[], control_nodes=[""], version="ncir_19")

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.71.213.234", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(
    airscale=_real_enb,
    oam_ip="10.71.213.234",
    global_bts_id=2370,
)

# TestLine
tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    tl_cloud_topology="CLOUD_5G_AIC_RM17_OCP_FHGW_AZQI",
    enbs=[_lte_real_enb],
)

__all__ = ["tl"]
