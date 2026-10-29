__maintainer__ = "xu hongli"
__team__ = "RAN_PZ_HAZ4_SG08"
__email__ = "hongli.xu@nokia-sbell.com"

import os
import re
import yaml
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
from taf.config.testline import NetworkAddress, RoutingInformation
from taf.config.testline import RealEnb, Airscale, CommonUnit
from taf.config.testline import RU, RadioTypes
from taf.config.testline import CloudBts, CU
from taf.config.testline import VDU, FHGW
from taf.config.testline import PxeServer
from taf.config.testline import TestLine
from taf.config.testline import RealEnb
from taf.config.testline import TestPc
from taf.config.testline.core import EPCSim, LTEEmuCore, PrismaCore
from taf.config.testline.attenuator import HBTE
from taf.config.testline.pdu import HBTE, TopYoung
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
host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.177.24", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_appserver_ssh = SshServiceDetails(
    addr="10.57.191.239", username="vrf3_sg8", password="Nokia@1234567", port="48999"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.239",
    iperf_path="/usr/bin/iperf",
    port="48998",
)
_appserver = AppServer(_iperf)
_appserver.iperf_details.port = 48998

# epcsim
_epc_sim = EPCSim(
    mme_ip="10.107.245.164",
    mcc="262",
    mnc="3",
    tac="201",
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.191.239", username="vrf3_sg8", password="vrf3@sg8"
    ),
    edaemon_port=10000,
    egate_port=20000,
    dir_path="/opt/iphy/latest",
    cfg_filename="LRC.cfg",
)

# askey
_ue_config_path = os.path.join(_cfg_dir, "TestData/askey.yml")
if os.path.isfile(_ue_config_path):
    with open(_ue_config_path) as f:
        _ue_inseego = f.read()
        # qci_port = re.findall("(_iperf.*?port)", _ue_inseego)
        # for item in qci_port:
        # _ue_inseego = _ue_inseego.replace(item, str(eval(item)))
        _ue_config = yaml.safe_load(_ue_inseego)
else:
    _ue_config = ""
# askey

# CU
_cu = CU(
    instance_id=1903,
    global_bts_id=1105,
    backhaul_site_oam_ip=NetworkAddress(v4="10.57.181.9"),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.158.2", username="cranuser1903", password="systeM!23"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.158.135", username="Nemuadmin", password="Nokia@123", port=443
    ),
    x2c=NetworkAddress(
        v4="10.57.168.74",
        vlan_id=110,
        routing=RoutingInformation(gateway="10.57.168.65", ip_prefix_length=26),
    ),
    f1c=NetworkAddress(
        v4="10.57.168.10",
        vlan_id=109,
        routing=RoutingInformation(gateway="10.57.168.1", ip_prefix_length=26),
    ),
    f1u=NetworkAddress(
        v4="10.57.168.11",
        vlan_id=109,
        routing=RoutingInformation(gateway="10.57.168.1", ip_prefix_length=26),
    ),
    s1u=NetworkAddress(
        v4="10.57.158.39",
        vlan_id=102,
        routing=RoutingInformation(gateway="10.57.158.33", ip_prefix_length=27),
    ),
    x2u=NetworkAddress(
        v4="10.57.168.75",
        vlan_id=110,
        routing=RoutingInformation(gateway="10.57.168.65", ip_prefix_length=26),
    ),
    tracing=None,
)

# cloud_deployment for vCU
_vcu_cnf_1 = DeploymentVnfStack(
    name="vcu1903",
    yaml_file=os.path.join(_cfg_dir, "DEP/gnbs_0/vCU/CU_cnf_values-override.yaml"),
)
_vcu_intnet_1 = DeploymentNetworkStack(
    name=_vcu_cnf_1.name + "-prerequisite",
    yaml_file=os.path.join(_cfg_dir, "DEP/gnbs_0/vCU/CU_pvc_values-override.yaml"),
)

# ssh connection information of OE, for tenant user
_vcu_ssh_connection_details = SshServiceDetails(
    addr="10.57.158.2", username="cranuser1903", password="systeM!23", port=22
)

# ssh connection information of OE, for root user
_vcu_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.57.158.2", username="cranuser1903", password="systeM!23", port=22
)

_vcu_master_node = MasterNode(
    k8s_connection_details=_vcu_k8s_connection_details,
    ssh_connection_details=_vcu_ssh_connection_details,
)

_vcu_k8s = K8S(namespace="cran1903", master_node=_vcu_master_node)

_vcu_k8s_cloud_deployment = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    networks=[_vcu_intnet_1],
    vnfs=[_vcu_cnf_1],
    cloud_hosting=_vcu_k8s,
)


# 5G RU
_ru_pdu = TopYoung(addr="10.71.195.198", port_numbers=[5])

_ru = RU(
    ru_hw_group="hw_group",
    pdu_port=_ru_pdu.pdu_ports[5],
    radio_type=RadioTypes.AEQQ,
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.35",
        username="serviceuser",
        password="bobuWrUHk7Xq7WPpY9ZcjEi8zNdX3plZ+/y420RZ7W4=",
    ),
)

# FHGW information
_pxe_server_ssh_info = SshServiceDetails(
    addr="0.0.0.0", username="root", password="centos"
)
_pxe_server = PxeServer(nfs_ip="0.0.0.0", ssh_connection_details=_pxe_server_ssh_info)

_fhgw_0 = FHGW(user_config_path=_cfg_dir, rus=[_ru], pxe_server=_pxe_server)
_fhgw_0.ip = "10.71.222.147"
_fhgw_0.username = "toor4nsn"
_fhgw_0.password = "Fhgw@nokia123"
_fhgw_0.version = "22R3"


# vDU
_ssh_connection_details_0 = SshServiceDetails(
    addr="10.64.166.146", username="core", password="system123"
)
_k8s_connection_details_0 = K8SConnectionDetails(
    ip_addr="10.64.166.146", username="core", password="system123", port="22"
)

_master_node_0 = MasterNode(
    k8s_connection_details=_k8s_connection_details_0,
    ssh_connection_details=_ssh_connection_details_0,
)

_k8s_0 = K8S(namespace="cran1903", master_node=_master_node_0)
_vdu_cnf_0 = DeploymentVnfStack(
    name="vdu1903",
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
        addr="10.64.166.186", username="Nemuadmin", password="Nokia@123"
    ),
    fhgws=[_fhgw_0],
    instance_id=1903,
    global_bts_id=1105,
)

# BTS
_cbts = CloudBts(
    dus=[_du_0],
    cu=_cu,
    cloud_deployment=_vcu_k8s_cloud_deployment,
)


# TestLine
tl = TestLine(
    test_pc=host,
    gnbs=[_cbts],
    tl_cloud_topology="CLOUD_5G_AIC_RM17_OCP_FHGW_AEQE",
    ues=[_ue_config],
    core=_epc_sim,
    appserver=_appserver,
)

__all__ = ["tl"]
