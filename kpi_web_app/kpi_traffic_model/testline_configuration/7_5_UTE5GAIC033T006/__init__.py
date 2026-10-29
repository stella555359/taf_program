__maintainer__ = "Chen Xiaowei"
__team__ = "I_NSB_MN_RAN_PZ_1_HAZ_2_GMS "
__email__ = "I_NSB_MN_RAN_PZ_1_HAZ_2@internal.nsn.com"
__owner_email__ = "xiaowei.1.chen@nokia-sbell.com"

import os
import yaml

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
from taf.config.testline import RealEnb, NetworkAddress, RoutingInformation
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU
from taf.config.testline import DU
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC
from taf.config.testline.lab_infrastructure import PxeServer
from taf.config.testline.appserver import AppServer
from taf.config.testline.attenuator import HBTE
from taf.config.testline.attenuator import AttenuationPort, TopYoung
from taf.config.testline.pdu import TopYoung as TP
from taf.config.testline.core import RealCore
from taf.config.testline.ue import Android, Qualcomm
from taf.config.testline.nms import NMS
# from taf.config.testline.nom import NOM
from taf.config.testline.nms import NOM

######################VDU###########################
## following are VDU related class which defined
## in taf.config.testline
## you can uncomment them when new version of
## taf.config.testline merged
#######################VDU##########################
from taf.config.testline.connection_details import K8SConnectionDetails
from taf.config.testline.gnb.du import FHGW
from taf.config.testline.gnb.du import VDU
from taf.config.testline.cloud_hosting import MasterNode, K8S, HelmChart
from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.config.testline.radio import RU


_cfg_dir = os.path.dirname(os.path.abspath(__file__))



# VDU related NCIR controlNode
_control = ControlNode(
    # configuration for ssh connecting to OE
    default_ssh_connection_details=SshServiceDetails(
        addr="10.70.25.82", username="core", password="system123"
    ),
    # configuration for connection of open stack UI, default port is 5000
    open_stack_connection_details=OpenStackConnectionDetails(
        username="core",
        password="system123",
        ip_addr="10.70.25.82",
        tenant="core",
    ),
    # BMC configuration of OE
    bmc_connection_details=BmcConnectionDetails(
        addr="10.97.65.26", username="admin", password="CNnokia_123nokia"
    ),
)

_control2 = ControlNode(
    # configuration for ssh connecting to OE
    default_ssh_connection_details=SshServiceDetails(
        addr="10.69.108.18", username="core", password="system123"
    ),
    # configuration for connection of open stack UI, default port is 5000
    open_stack_connection_details=OpenStackConnectionDetails(
        username="core",
        password="system123",
        ip_addr="10.69.108.18",
        tenant="core",
    ),
    # BMC configuration of OE
    bmc_connection_details=BmcConnectionDetails(
        addr="10.69.104.54", username="admin", password="CNnokia123_nokia"
    ),
)

# configuration of VCU related NCIR/OSP
_ncir = NCIR(compute_nodes=[], control_nodes=[_control], version="OE20")

# CU configuration
_cu = CU(
    # CU web UI ip address, oam interface ip of oam vm
    backhaul_site_oam_ip=NetworkAddress(
		v4="10.107.160.15"
		),
    # VCU OAM ssh connection, oam interface ip of oam vm
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.107.160.15", username="serviceuser", password="Pl(FzaYj5~c5;q"
    ),
    # VCU OAM http connection, oam interface ip of oam vm
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.107.160.15", username="Nemuadmin", password="Nokia@123", port="443"
    ),
    # route configuration for x2 link to ENB on VCU, v4 is network address of ENB x2 link
	
    # route configuration for f1c link to VDU on VCU, v4 is network address of VDU f1c link
    f1c=NetworkAddress(
        v4="10.107.160.79",
        vlan_id=101,
        routing=RoutingInformation(gateway="10.57.173.65/26"),
    ),

    # route configuration for f1u link to VDU on VCU, v4 is network address of VDU f1u link
    f1u=NetworkAddress(
        v4="110.107.160.179",
        vlan_id=102,
        routing=RoutingInformation(gateway="10.57.173.65/26"),
    ),

    xnc=NetworkAddress(
        v4="10.107.161.15",
        vlan_id=103,
        routing_v4=RoutingInformation(gateway="10.107.110.113/29"),
    ),
    xnu=NetworkAddress(
        v4="10.107.161.169",
        vlan_id=104,
        routing_v4=RoutingInformation(gateway="10.107.110.33/27"),
    ),

    ngc=NetworkAddress(
        v4="10.107.161.79",
        vlan_id=105,
        routing_v4=RoutingInformation(gateway="10.107.110.65/27"),
    ),
    ngu=NetworkAddress(
        v4="10.107.162.41",
        vlan_id=106,
        routing_v4=RoutingInformation(gateway="10.107.110.65/27"),
    ),
    tracing=NetworkAddress(
        v4="10.107.163.169",
        vlan_id=110,
        routing_v4=RoutingInformation(gateway="10.110.27.0/23"),
    ),
)

_cu2 = CU(
    # CU web UI ip address, oam interface ip of oam vm
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.107.92.19"
    ),
    # VCU OAM ssh connection, oam interface ip of oam vm
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.107.92.19", username="serviceuser", password="Pl(FzaYj5~c5;q"
    ),
    # VCU OAM http connection, oam interface ip of oam vm
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.107.92.19", username="Nemuadmin", password="Nokia@123", port="443"
    ),
    # route configuration for x2 link to ENB on VCU, v4 is network address of ENB x2 link
    x2c=NetworkAddress(
        v4="10.107.92.147",
        vlan_id=1400,
        routing_v4=RoutingInformation(gateway="10.107.92.128/26"),
    ),
    x2u=NetworkAddress(
        v4="10.107.92.211",
        vlan_id=1401,
        routing_v4=RoutingInformation(gateway="10.107.92.192/26"),
    ),
    xnc=NetworkAddress(
        v4="10.107.90.212",
        vlan_id=1343,
        routing_v4=RoutingInformation(gateway="10.107.90.192/26"),
    ),
    xnu=NetworkAddress(
        v4="10.107.91.111",
        vlan_id=1344,
        routing_v4=RoutingInformation(gateway="10.107.91.0/25"),
    ),
    # route configuration for f1c link to VDU on VCU, v4 is network address of VDU f1c link
    f1c=NetworkAddress(
        v4="10.107.90.147",
        vlan_id=1341,
        routing_v4=RoutingInformation(gateway="10.107.90.128/26"),
    ),
    # route configuration for f1u link to VDU on VCU, v4 is network address of VDU f1u link
    f1u=NetworkAddress(
        v4="10.107.90.111",
        vlan_id=1342,
        routing_v4=RoutingInformation(gateway="10.107.90.0/25"),
    ),
    s1u=NetworkAddress(
        v4="10.107.94.147",
        vlan_id=1402,
        routing_v4=RoutingInformation(gateway="10.107.94.128/26"),
    ),
    ngc=NetworkAddress(
        v4="10.107.92.83",
        vlan_id=1347,
        routing_v4=RoutingInformation(gateway="10.107.92.64/26"),
    ),
    ngu=NetworkAddress(
        v4="10.107.91.240",
        vlan_id=1345,
        routing_v4=RoutingInformation(gateway="10.107.91.128/25"),
    ),
    tracing=NetworkAddress(
        v4="10.107.89.64",
        vlan_id=1340,
        routing_v4=RoutingInformation(gateway="10.107.88.0/23"),
    )
)

# test pc information of enb
_enb_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.56.198.86", username="ute", password="UTE.debian12"
    ),
)


_vcu_intnet_1 = DeploymentNetworkStack(
    name="aic-vcu-intnet",
    yaml_file=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/aic_intnet_values_override_0.yaml"
    ),
)
_vcu_intnet_2 = DeploymentNetworkStack(
    name="aic-vcu-intnet",
    yaml_file=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/aic_intnet_values_override_0.yaml"
    ),
)
_vcu_vnf_1 = DeploymentVnfStack(
    name="aic-vcu",
    yaml_file=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/aic_vdu_values_override_0.yaml"
    ),
)
_vcu_vnf_2 = DeploymentVnfStack(
    name="aic-vcu",
    yaml_file=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/aic_vdu_values_override_0.yaml"
    ),
)

# ssh connection information of OE, for tenant user
_vcu_ssh_connection_details = SshServiceDetails(
    addr="10.107.123.162", username="cranuser15", password="systeM!23", port="22"
)
_vcu_ssh_connection_details2 = SshServiceDetails(
    addr="10.107.14.66", username="cranuser15", password="systeM!23", port="22"
)
# ssh connection information of OE, for root user
_vcu_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.107.123.162", username="core", password="system123", port="22"
)
_vcu_k8s_connection_details2 = K8SConnectionDetails(
    ip_addr="10.107.14.66", username="core", password="system123", port="22"
)
_vcu_master_node = MasterNode(
    k8s_connection_details=_vcu_k8s_connection_details,
    ssh_connection_details=_vcu_ssh_connection_details,
)
_vcu_master_node2 = MasterNode(
    k8s_connection_details=_vcu_k8s_connection_details2,
    ssh_connection_details=_vcu_ssh_connection_details2,
)
_vcu_k8s = K8S(namespace="cran3", master_node=_vcu_master_node)
_cluster_preparation_cu_1 = HelmChart(
  name = "aic-vcu-cluster-preparation",
  yaml_file = os.path.join(_cfg_dir, 'vcu-cluster-preparation.yaml'),
)

_prerequisite_cu_1 = HelmChart(
  name = "aic-vcu-prerequisite",
  yaml_file = os.path.join(_cfg_dir, 'vcu-prerequisite.yaml'),
)

_cnf_cu_1 = HelmChart(
  name = "aic-vcu",
  yaml_file = os.path.join(_cfg_dir, 'vcu-cnf.yaml'),
)

_vcu_k8s_cloud_deployment = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    networks=[_vcu_intnet_1],
    cluster_preparation=_cluster_preparation_cu_1,
    prerequisite=_prerequisite_cu_1,
    cnf=_cnf_cu_1,
    vnfs=[_vcu_vnf_1],
    cloud_hosting=_vcu_k8s,
)
_vcu_k8s2 = K8S(namespace="cran15", master_node=_vcu_master_node2)

_cluster_preparation_cu_2 = HelmChart(
  name = "aic-vcu-cluster-preparation",
  yaml_file = os.path.join(_cfg_dir, 'vcu-cluster-preparation.yaml'),
)

_prerequisite_cu_2 = HelmChart(
  name = "aic-vcu-prerequisite",
  yaml_file = os.path.join(_cfg_dir, 'vcu-prerequisite.yaml'),
)

_cnf_cu_2 = HelmChart(
  name = "aic-vcu",
  yaml_file = os.path.join(_cfg_dir, 'vcu-cnf.yaml'),
)

_vcu_k8s_cloud_deployment2 = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    networks=[_vcu_intnet_2],
	cluster_preparation=_cluster_preparation_cu_2,
    prerequisite=_prerequisite_cu_2,
    cnf=_cnf_cu_2,
    vnfs=[_vcu_vnf_2],
    cloud_hosting=_vcu_k8s2,
)
# VDU configuration for deployment

_vdu_vnf_1 = DeploymentVnfStack(
    name="aic-vdu",
    yaml_file=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/aic_vdu_values_override_0.yaml"
    ),
)
_vdu_vnf_2 = DeploymentVnfStack(
    name="aic-vdu",
    yaml_file=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/aic_vdu_values_override_0.yaml"
    ),
)
# VDU internal network configuration for deployment
_vdu_intnet_1 = DeploymentNetworkStack(
    name="aic-intnet",
    yaml_file=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/aic_intnet_values_override_0.yaml"
    ),
)
_vdu_intnet_2 = DeploymentNetworkStack(
    name="aic-intnet",
    yaml_file=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/aic_intnet_values_override_0.yaml"
    ),
)
# ssh connection information of OE, for tenant user
_ssh_connection_details = SshServiceDetails(
    addr="10.70.25.82", username="core", password="system123"
)
_ssh_connection_details2 = SshServiceDetails(
    addr="10.69.108.18", username="core", password="system123"
)
# ssh connection information of OE, for cloudadmin user
_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.70.25.82", username="core", password="system123", port="22"
)
_k8s_connection_details2 = K8SConnectionDetails(
    ip_addr="10.69.108.18", username="core", password="system123", port="22"
)
# master node information of OE
_master_node = MasterNode(
    k8s_connection_details=_k8s_connection_details,
    ssh_connection_details=_ssh_connection_details,
)

_k8s = K8S(namespace="cran1", master_node=_master_node)

_cluster_preparation_du = HelmChart(
    name="aic-vdu-cluster-preparation",
    yaml_file=os.path.join(_cfg_dir, 'vdu-cluster-preparation.yaml'),
)

_prerequisite_du = HelmChart(
    name="aic-vdu-prerequisite",
    yaml_file=os.path.join(_cfg_dir, 'vdu-prerequisite.yaml'),
)

_cnf_du = HelmChart(
    name="aic-vdu",
    yaml_file=os.path.join(_cfg_dir, 'vdu-cnf.yaml'),
)

_master_node2 = MasterNode(
    k8s_connection_details=_k8s_connection_details2,
    ssh_connection_details=_ssh_connection_details2,
)

_k8s2 = K8S(namespace="cran1", master_node=_master_node2)

_cluster_preparation_du_2 = HelmChart(
    name="aic-vdu-cluster-preparation",
    yaml_file=os.path.join(_cfg_dir, 'vdu-cluster-preparation.yaml'),
)

_prerequisite_du_2 = HelmChart(
    name="aic-vdu-prerequisite",
    yaml_file=os.path.join(_cfg_dir, 'vdu-prerequisite.yaml'),
)

_cnf_du_2 = HelmChart(
    name="aic-vdu",
    yaml_file=os.path.join(_cfg_dir, 'vdu-cnf.yaml'),
)

# VDU deployment configuration
_k8s_cloud_deployment = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    networks=[_vdu_intnet_1],
    vnfs=[_vdu_vnf_1],
    cloud_hosting=_k8s,
	cluster_preparation=_cluster_preparation_du,
    prerequisite=_prerequisite_du,
    cnf=_cnf_du,
)
_k8s_cloud_deployment2 = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    networks=[_vdu_intnet_2],
    vnfs=[_vdu_vnf_2],
    cloud_hosting=_k8s,
	cluster_preparation=_cluster_preparation_du,
    prerequisite=_prerequisite_du,
    cnf=_cnf_du,
)
# VDU oam http connection
_vdu_oam_http_connection_details = HttpConnectionDetails(
    addr="10.70.25.114", port="443", username="Nemuadmin", password="Nokia@123"
)

_vdu_oam_http_connection_details2 = HttpConnectionDetails(
    addr="10.69.108.50", port="443", username="Nemuadmin", password="Nokia@123"
)

_ru_pdu = TP(addr="10.97.83.3", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16])
_ru_pdu1 = TP(addr="10.97.83.3", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16])

_attenuator_5G = TopYoung(
    ip_addr="10.97.83.3",
    port=1000,
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    model="TAS16T16-51-120-1S-DES",
)

# RU configuration
_ru_1 = RU(
    ru_hw_group="RU_INT_ECPRI",
    radio_type="AEQY",   
    serial_number="1M212900840",
    attenuation_ports=[
        _attenuator_5G.attenuator_ports[1],
        _attenuator_5G.attenuator_ports[2],
        _attenuator_5G.attenuator_ports[3],
        _attenuator_5G.attenuator_ports[4],
        _attenuator_5G.attenuator_ports[5],
        _attenuator_5G.attenuator_ports[6],
        _attenuator_5G.attenuator_ports[7],
        _attenuator_5G.attenuator_ports[8],
        _attenuator_5G.attenuator_ports[9],
        _attenuator_5G.attenuator_ports[10],
        _attenuator_5G.attenuator_ports[11],
        _attenuator_5G.attenuator_ports[12],
        _attenuator_5G.attenuator_ports[13],
        _attenuator_5G.attenuator_ports[14],
        _attenuator_5G.attenuator_ports[15],
        _attenuator_5G.attenuator_ports[16],
    ],
    pdu_port=_ru_pdu.pdu_ports[5]
)

_ru_2 = RU(
    ru_hw_group="RU_INT_ECPRI",
    radio_type="AEQY",   
    serial_number="1M212323229",
    attenuation_ports=[
        _attenuator_5G.attenuator_ports[1],
        _attenuator_5G.attenuator_ports[2],
        _attenuator_5G.attenuator_ports[3],
        _attenuator_5G.attenuator_ports[4],
        _attenuator_5G.attenuator_ports[5],
        _attenuator_5G.attenuator_ports[6],
        _attenuator_5G.attenuator_ports[7],
        _attenuator_5G.attenuator_ports[8],
        _attenuator_5G.attenuator_ports[9],
        _attenuator_5G.attenuator_ports[10],
        _attenuator_5G.attenuator_ports[11],
        _attenuator_5G.attenuator_ports[12],
        _attenuator_5G.attenuator_ports[13],
        _attenuator_5G.attenuator_ports[14],
        _attenuator_5G.attenuator_ports[15],
        _attenuator_5G.attenuator_ports[16],
    ],
    pdu_port=_ru_pdu1.pdu_ports[1]
)

# PXE server info for FHGW deployment
_pxe_server_ssh_info = SshServiceDetails(
    addr="10.56.104.30", username="root", password="nokia123"
)
_pxe_server = PxeServer(
    nfs_ip="10.56.104.30", ssh_connection_details=_pxe_server_ssh_info
)
# FHGW information
_fhgw_1 = FHGW(
    user_config_path=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/FHGW_0/fhgw_user_config_0.yaml"
    ),
    rus=[_ru_1],
    pxe_server=_pxe_server,
)

# fhgw extra parameter configuration
_fhgw_1.ssh_username = "toor4nsn"
_fhgw_1.ssh_password = "Fhgw@nokia123"

_fhgw_2 = FHGW(
    user_config_path=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/FHGW_0/fhgw_user_config_0.yaml"
    ),
    rus=[_ru_2],
    pxe_server=_pxe_server,
)

# fhgw extra parameter configuration
_fhgw_2.ssh_username = "toor4nsn"
_fhgw_2.ssh_password = "Fhgw@nokia123"

# VDU global configuration
_vdu_1 = VDU(
    cloud_deployment=_k8s_cloud_deployment,
    oam_http_connection_details=_vdu_oam_http_connection_details,
    fhgws=[_fhgw_1],
    # route configuration of f1m link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_m_ip_addr=NetworkAddress(
        v4="10.56.104.2",
        vlan_id=516,
        routing_v4=RoutingInformation(gateway="10.56.104.1/29"),
    ),
    # route configuration of f1c link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_c_ip_addr=NetworkAddress(
        v4="10.70.25.106",
        vlan_id=515,
        routing_v4=RoutingInformation(gateway="10.56.103.249/29"),
    ),
    # route configuration of f1u link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_u_ip_addr=NetworkAddress(
        v4="10.70.25.106",
        vlan_id=515,
        routing_v4=RoutingInformation(gateway="10.56.103.249/29"),
    ),
    instance_id=10760,
)

_vdu_2 = VDU(
    cloud_deployment=_k8s_cloud_deployment2,
    oam_http_connection_details=_vdu_oam_http_connection_details2,
    fhgws=[_fhgw_2],
    # route configuration of f1m link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_m_ip_addr=NetworkAddress(
        v4="10.69.108.50",
        vlan_id=2016,
        routing_v4=RoutingInformation(gateway="10.69.108.48/29"),
    ),
    # route configuration of f1c link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_c_ip_addr=NetworkAddress(
        v4="10.69.108.42",
        vlan_id=1310,
        routing_v4=RoutingInformation(gateway="10.69.108.41/29"),
    ),
    # route configuration of f1u link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_u_ip_addr=NetworkAddress(
        v4="10.69.108.43",
        vlan_id=1310,
        routing_v4=RoutingInformation(gateway="10.69.108.41/29"),
    ),
    instance_id=11068,
)
# mcc, mnc configuration
_realcore = RealCore(five_g=None, mcc="262", mnc="03", pdns=None)

_cbts = CloudBts(
    dus=[_vdu_1],  # vdu related parameter
    cu=_cu,
    cloud_deployment=_vcu_k8s_cloud_deployment,
    vnf_name="hgz-10760",
    instance_id="10760",
    global_bts_id="10760",
)

_cbts2 = CloudBts(
    dus=[_vdu_2],  # vdu related parameter
    cu=_cu2,
    cloud_deployment=_vcu_k8s_cloud_deployment2,
    vnf_name="hgz-11068",
    instance_id="11068",
    global_bts_id="11068",
)

#  iperf server info
_appserver_ssh = SshServiceDetails(
    addr="10.56.198.86", username="ute", password="UTE.debian12"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.106.243.149",
    iperf_path="/data/data/com.nokia.syve.uemanager.mobile/",
    port="54015",
)

_appserver = AppServer(_iperf)

huawei = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.97.83.14", username="csv1-tester", password="Nokia123!"
    ),
    serial_number="RFCX10MEQBF",
    serial_com=34,
    server_dir="/cygdrive/c/pyro_server",
    python_path="/cygdrive/c/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["Commercial", "samsung23"],
)

#_android1 = Android(
#    ssh_connection_details=SshServiceDetails(
#         addr="10.97.83.14", username="rrm2-tester", password="Nokia123!"
#     ),
#     # serial_number="9YS0220730009229",
#     serial_number="H4K5T20C22016222",
#     server_dir="/cygdrive/c/pyro_server",
#     python_path="C:/Python27/python.exe",
#     qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
#     diag_cfg_path="C:/pyro_server/DIAG.cfg",
#     iperf_details=_iperf,
#     capabilities=["Commercial", "huawei_mate40"],
# )





# Testpc
# UTE IP address and User Name, Password
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.56.198.86", username="ute", password="UTE.debian12"
    ),
    connections=[_cbts]
)

# Testline configuration
tl = TestLine(
    test_pc=_test_pc,
    ues=[huawei],
    gnbs=[_cbts,_cbts2],
    # enbs=[_real_enb],
    tl_cloud_topology="CLOUD_5G_AIC_SA_1XAndroid_1XvDU_OE20_1XFHGW_1XAEQY_PB",
    cloud_hostings=[_ncir],
    test_pcs=[_test_pc],
    attenuator=_attenuator_5G,
    core=_realcore,
    appserver=_appserver,
)

# only tl variable can be accessed by user

__all__ = ["tl"]