__maintainer__ = "Yang Liqin"
__team__ = "MN_RAN_RD_VRF_HAZ3_05"
__email__ = "liqin.yang@nokia-sbell.com"

import os
from taf.config.testline.appserver import AppServer, TafUeAppServer
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
    MediaTek,
    TafUeFastmile,
)  # added in taf.meta.5.4
from taf.config.testline import NetworkAddress, RoutingInformation, LicenseKeeper
from taf.config.testline import RealEnb, Airscale, CommonUnit
from taf.config.testline import HBTE_PDU as HBTE
from taf.config.testline.pdu import FPFH
from taf.config.testline import RU, RadioTypes
from taf.config.testline import CloudBts, CU
from taf.config.testline import VDU, FHGW
from taf.config.testline import PxeServer
from taf.config.testline import TestLine
from taf.config.testline import TestPc
from taf.config.testline.nms import NetAct
from taf.config.testline.taf_ue_data_transfer_protocol import TafUeDataTransferProtocol


_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# Testpc
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.195.64", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# CU
_cu = CU(
    instance_id=1925,
    global_bts_id=11546,
    backhaul_site_oam_ip=NetworkAddress(v4="10.57.173.16"),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.165.130", username="cranuser1925", password="systeM!23"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.165.6", username="Nemuadmin", password="Nokia@123", port=443
    ),
    f1c=NetworkAddress(
        v4="10.57.166.8",
        vlan_id=2689,
        routing_v4=RoutingInformation(gateway="10.57.166.1", ip_prefix_length=26),
    ),
    f1u=NetworkAddress(
        v4="10.57.166.9",
        vlan_id=2689,
        routing_v4=RoutingInformation(gateway="10.57.166.1", ip_prefix_length=26),
    ),
    ngc=NetworkAddress(
        v4="10.57.166.134",
        vlan_id=2691,
        routing_v4=RoutingInformation(gateway="10.57.166.129", ip_prefix_length=26),
    ),
    ngu=NetworkAddress(
        v4="10.57.166.135",
        vlan_id=2691,
        routing_v4=RoutingInformation(gateway="10.57.166.129", ip_prefix_length=26),
    ),
    x2c=NetworkAddress(
        v4="10.57.166.70",
        vlan_id=2690,
        routing_v4=RoutingInformation(gateway="10.57.166.65", ip_prefix_length=26),
    ),
    x2u=NetworkAddress(
        v4="10.57.166.71",
        vlan_id=2690,
        routing_v4=RoutingInformation(gateway="10.57.166.65", ip_prefix_length=26),
    ),
    s1u=NetworkAddress(
        v4="10.57.165.37",
        vlan_id=2682,
        routing_v4=RoutingInformation(gateway="10.57.165.33", ip_prefix_length=27),
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
    addr="10.57.165.130", username="cranuser1925", password="systeM!23", port=22
)
# ssh connection information of OE, for root user
_vcu_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.57.165.130", username="cranuser1925", password="systeM!23", port=22
)

_vcu_master_node = MasterNode(
    k8s_connection_details=_vcu_k8s_connection_details,
    ssh_connection_details=_vcu_ssh_connection_details,
)

_vcu_k8s = K8S(namespace="cran1925", master_node=_vcu_master_node)

_vcu_k8s_cloud_deployment = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    networks=[_vcu_intnet_1],
    vnfs=[_vcu_cnf_1],
    cloud_hosting=_vcu_k8s,
)


# 5G RU
_ru_pdu1 = FPFH(addr="10.71.196.76", port_numbers=[5])

_ru1 = RU(
    ru_hw_group="Below6GHz",
    pdu_port=_ru_pdu1.pdu_ports[5],
    radio_type=RadioTypes.AEHC,
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.37",
        username="rfsw",
        password="f6gh0K2nXq0O8XqVFkUuMtJnzuKm0U3box0QcYgugn0=",
    ),
)


# OE information
_IP_OCP="10.64.173.218"
_ssh_connection_details_0 = SshServiceDetails(
    addr=_IP_OCP, username="core", password="system123"
)
_k8s_connection_details_0 = K8SConnectionDetails(
    ip_addr=_IP_OCP, username="core", password="system123", port="22"
)

_master_node_0 = MasterNode(
    k8s_connection_details=_k8s_connection_details_0,
    ssh_connection_details=_ssh_connection_details_0,
)
_k8s_0 = K8S(namespace="cran1925", master_node=_master_node_0)
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
        addr="10.64.173.242", username="Nemuadmin", password="Nokia@123"
    ),
    instance_id=1925,
    global_bts_id=11546,
)

# BTS
_cbts = CloudBts(
    dus=[_du_0],
    cu=_cu,
    cloud_deployment=_vcu_k8s_cloud_deployment,
)

_fastmile_appserver_1 = TafUeAppServer(
    app_server_name="APP_SERVER_1",
    address="10.71.207.139",
    user="vrf3_sg5",
    password="vrf3@sg5",
    bind_interface_ip="10.71.207.139",
    expected_prompt="[mmw_sg5@appserver ~]$ ",
    binary_path="/usr/bin/iperf",
    ports=[45825, 45925],
)

_fastmile_data_transfer_1 = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_fastmile_appserver_1,
    interval=1,
    binary_path="iperf",
    version=2,
)

_fastmile_1 = TafUeFastmile(
    ue_pc_address="10.57.195.64",
    root_password='CtiWVFUSj9uehtM6',
    default_user_password='7CdgDedA@tAKPAod',
    ue_manage_ip="10.71.208.130",
    data_transfer=[_fastmile_data_transfer_1],
    serial_number='KLT234301903',
    proxy_mngr_port=9955,
    ueproxy_force_release=True,
    version='receiver 5g19a',
    capabilities=["REAL_FASTMILE_UE1", "nokia_fastmile"],
)


# TestLine
tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    tl_cloud_topology="TL1925",
    ues=[_fastmile_1],
)

__all__ = ["tl"]
