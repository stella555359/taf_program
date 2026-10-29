__maintainer__ = "Yang Di"
__team__ = "MN_RAN_RD_VRF_HAZ3_05"
__email__ = "di.yang@nokia-sbell.com"

import os
from taf.config.testline.airscale import CapacityUnit
from taf.config.testline.appserver import AppServer, TafUeAppServer
from taf.config.testline.attenuator import HBTE as AHBTE
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
)
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
        addr="10.57.159.10", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# CU
_cu = CU(
    instance_id=1928,
    global_bts_id=37403,
    backhaul_site_oam_ip=NetworkAddress(v4="10.57.158.142"),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.158.2", username="cranuser1928", password="systeM!23"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.158.142", username="Nemuadmin", password="Nokia@123", port=443
    ),
    f1c=NetworkAddress(
        v4="10.57.221.12",
        vlan_id=109,
        routing_v4=RoutingInformation(gateway="10.57.221.1", ip_prefix_length=26),
    ),
    f1u=NetworkAddress(
        v4="10.57.221.13",
        vlan_id=109,
        routing_v4=RoutingInformation(gateway="10.57.221.1", ip_prefix_length=26),
    ),
    ngc=NetworkAddress(
        v4="10.57.221.140",
        vlan_id=111,
        routing_v4=RoutingInformation(gateway="10.57.221.129", ip_prefix_length=26),
    ),
    ngu=NetworkAddress(
        v4="10.57.221.141",
        vlan_id=111,
        routing_v4=RoutingInformation(gateway="10.57.221.129", ip_prefix_length=26),
    ),
    x2c=NetworkAddress(
        v4="10.57.221.76",
        vlan_id=110,
        routing_v4=RoutingInformation(gateway="10.57.221.65", ip_prefix_length=26),
    ),
    x2u=NetworkAddress(
        v4="10.57.221.77",
        vlan_id=110,
        routing_v4=RoutingInformation(gateway="10.57.221.65", ip_prefix_length=26),
    ),
    s1u=NetworkAddress(
        v4="10.57.222.40",
        vlan_id=102,
        routing_v4=RoutingInformation(gateway="10.57.222.33", ip_prefix_length=27),
    ),
    tracing=None,
)

# cloud_deployment for vCU
_vcu_cnf_1 = DeploymentVnfStack(
    name="aic-vcu",
    yaml_file=os.path.join(_cfg_dir, "DEP/gnbs_0/vCU/CU_cnf_values-override.yaml"),
)
_vcu_intnet_1 = DeploymentNetworkStack(
    name=_vcu_cnf_1.name + "-prerequisite",
    yaml_file=os.path.join(_cfg_dir, "DEP/gnbs_0/vCU/CU_pvc_values-override.yaml"),
)

# ssh connection information of OE, for tenant user
_vcu_ssh_connection_details = SshServiceDetails(
    addr="10.57.158.2", username="cranuser1928", password="systeM!23", port=22
)
# ssh connection information of OE, for root user
_vcu_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.57.158.2", username="cranuser1928", password="systeM!23", port=22
)

_vcu_master_node = MasterNode(
    k8s_connection_details=_vcu_k8s_connection_details,
    ssh_connection_details=_vcu_ssh_connection_details,
)

_vcu_k8s = K8S(namespace="tl1928", master_node=_vcu_master_node)

_vcu_k8s_cloud_deployment = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    networks=[_vcu_intnet_1],
    vnfs=[_vcu_cnf_1],
    cloud_hosting=_vcu_k8s,
)

# OE information
_IP_OCP="10.0.179.98"
_IP_OCP_1="10.0.179.58"
_ssh_connection_details_0 = SshServiceDetails(
    addr=_IP_OCP, username="core", password="system123"
)
_ssh_connection_details_1 = SshServiceDetails(
    addr=_IP_OCP_1, username="core", password="system123"
)
_k8s_connection_details_0 = K8SConnectionDetails(
    ip_addr=_IP_OCP, username="core", password="system123", port="22"
)
_k8s_connection_details_1 = K8SConnectionDetails(
    ip_addr=_IP_OCP_1, username="core", password="system123", port="22"
)
_master_node_0 = MasterNode(
    k8s_connection_details=_k8s_connection_details_0,
    ssh_connection_details=_ssh_connection_details_0,
)
_master_node_1 = MasterNode(
    k8s_connection_details=_k8s_connection_details_1,
    ssh_connection_details=_ssh_connection_details_1,
)
_k8s_0 = K8S(namespace="tl1928", master_node=_master_node_0)
#_k8s_1 = K8S(namespace="tl1927", master_node=_master_node_1)
_vdu_cnf_0 = DeploymentVnfStack(
    name="aic-vdu",
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

#_vdu_k8s_cloud_deployment_1 = CloudDeployment(
#    default_cfg_dir=_cfg_dir,
#    cloud_hosting=_k8s_1,
#    networks=[_vdu_intnet_0],
#    vnfs=[_vdu_cnf_0],
#)

_attenuator = AHBTE(
    ip_addr="10.71.203.130",
    port=5000,
    attenuation_port_numbers=[11, 12, 1, 2],
    model="PA-16-16-6-127-0.5-B-S",
)

# RU configuration
_ru_1 = RU(ru_hw_group="cMAAr6.1_8T8R_eCPRI", radio_type="AZHL", serial_number="AH222603004",
    attenuation_ports=[
        _attenuator.attenuator_ports[11],
        _attenuator.attenuator_ports[12],
    ],
)
#_ru_2 = RU(ru_hw_group="RF6.2_4T4R_IDRU", radio_type="AWHQX", serial_number="EB2232R0696",
#    attenuation_ports=[
#        _attenuator.attenuator_ports[1],
#        _attenuator.attenuator_ports[2],
#    ],
#)

# FHGW information
_fhgw_0 = FHGW(
    user_config_path=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/FHGW_0/fhgw_user_config_0.yaml"
    ),
    rus=[_ru_1],
)

_du_0 = VDU(
    cloud_deployment=_vdu_k8s_cloud_deployment_0,
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.0.179.122", username="Nemuadmin", password="Nokia@123"
    ),
    fhgws=[_fhgw_0],
    instance_id=1928,
    global_bts_id=37403,
    fhuc_vlans=[337],
)

#_du_1 = VDU(
#    cloud_deployment=_vdu_k8s_cloud_deployment_1,
#    oam_http_connection_details=HttpConnectionDetails(
#        addr="10.0.179.82", username="Nemuadmin", password="Nokia@123"
#    ),
#    fhgws=[_fhgw_0],
#    instance_id=1927,
#    global_bts_id=37403,
#    fhuc_vlans=[337],
#)

# BTS
_cbts = CloudBts(
    dus=[_du_0],
    cu=_cu,
    cloud_deployment=_vcu_k8s_cloud_deployment,
)

# Iperf
_appserver_ssh = SshServiceDetails(
    addr="10.71.207.139", username="vrf3_sg5", password="vrf3@sg5", port="45027"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.207.139",
    iperf_path="iperf",
    port="45028",
)

_android1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.217.84", username="nokia5g", password="noki@123"
    ),
    serial_number="R3CR40S38RY",
    server_dir="/cygdrive/c/pyro_server",
    python_path="/cygdrive/c/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["Commercial", "samsung"],
)

_android2 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.217.84", username="nokia5g", password="noki@123"
    ),
    serial_number="R3CR50LEDHE",
    server_dir="/cygdrive/c/pyro_server",
    python_path="/cygdrive/c/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["Commercial", "samsung"],
)

_android3 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.217.84", username="nokia5g", password="noki@123"
    ),
    serial_number="RFCRA1HYDHV",
    server_dir="/cygdrive/c/pyro_server",
    python_path="/cygdrive/c/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["Commercial", "samsung"],
)

_appserver = AppServer(iperf_details=_iperf)

# TestLine
tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    cloud_hostings=[_vcu_k8s, _k8s_0],
    tl_cloud_topology="TL1928",
    ues=[_android1, _android2, _android3],
    attenuator=_attenuator,
    appserver=_appserver
)

__all__ = ["tl"]
