# -*- coding:UTF-8 -*-
__maintainer__ = "Nie Rong"
__team__ = "I_NSB_MN_RAN_PZ_1_HAZ_2_GMS "
__email__ = "I_NSB_MN_RAN_PZ_1_HAZ_2@internal.nsn.com"
__owner_email__ = "rong.nie@nokia-sbell.com"

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
#from taf.config.testline.nms import NMS
# from taf.config.testline.nom import NOM
#from taf.config.testline.nms import NOM

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
        addr="10.70.83.66", username="core", password="system123"
    ),
    # configuration for connection of open stack UI, default port is 5000
    open_stack_connection_details=OpenStackConnectionDetails(
        username="core",
        password="system123",
        ip_addr="10.70.83.66",
        tenant="core",
    ),
    # BMC configuration of OE
    bmc_connection_details=BmcConnectionDetails(
        addr="10.97.82.134", username="root", password="Nokia@123"
    ),
)

# configuration of VCU related NCIR/OSP
_ncir = NCIR(compute_nodes=[], control_nodes=[_control], version="OE19")

# CU configuration
_cu = CU(
    # CU web UI ip address, oam interface ip of oam vm
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.107.160.17"
    ),
    # VCU OAM ssh connection, oam interface ip of oam vm
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.107.160.17", username="serviceuser", password="Pl(FzaYj5~c5;q"
    ),
    # VCU OAM http connection, oam interface ip of oam vm
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.107.160.17", username="Nemuadmin", password="nemuuser", port="443"
    ),
    # route configuration for x2 link to ENB on VCU, v4 is network address of ENB x2 link
    x2c=NetworkAddress(
        v4="10.107.162.145",
        vlan_id=107,
        routing=RoutingInformation(gateway="10.107.92.128/26"),
    ),
    x2u=NetworkAddress(
        v4="10.107.163.47",
        vlan_id=108,
        routing=RoutingInformation(gateway="10.107.92.192/26"),
    ),
    xnc=NetworkAddress(
        v4="10.107.161.17",
        vlan_id=103,
        routing_v4=RoutingInformation(gateway="10.107.90.192/26"),
    ),
    xnu=NetworkAddress(
        v4="10.107.161.175",
        vlan_id=104,
        routing_v4=RoutingInformation(gateway="10.107.91.0/25"),
    ),
    # route configuration for f1c link to VDU on VCU, v4 is network address of VDU f1c link
    f1c=NetworkAddress(
        v4="10.107.160.81",
        vlan_id=101,
        routing=RoutingInformation(gateway="10.107.90.128/26"),
    ),
    # route configuration for f1u link to VDU on VCU, v4 is network address of VDU f1u link
    f1u=NetworkAddress(
        v4="10.107.160.185",
        vlan_id=102,
        routing=RoutingInformation(gateway="10.107.90.0/25"),
    ),
    s1u=NetworkAddress(
        v4="10.107.162.209",
        vlan_id=109,
        routing=RoutingInformation(gateway="10.107.94.128/26"),
    ),
    ngc=NetworkAddress(
        v4="10.107.161.81",
        vlan_id=105,
        routing_v4=RoutingInformation(gateway="10.107.92.64/26"),
    ),
    ngu=NetworkAddress(
        v4="10.107.162.47",
        vlan_id=106,
        routing_v4=RoutingInformation(gateway="10.107.91.128/25"),
    ),
    tracing=NetworkAddress(
        v4="10.107.163.175",
        vlan_id=110,
        routing_v4=RoutingInformation(gateway="10.107.88.0/23"),
    )
)

# test pc information of enb
_enb_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.97.65.246", username="ute", password="ute"
    ),
    # connections=[_real_enb],    #暂时没填
)


_vcu_intnet_1 = DeploymentNetworkStack(
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
# ssh connection information of OE, for tenant user
_vcu_ssh_connection_details = SshServiceDetails(
    addr="10.107.123.162", username="cranuser17", password="systeM!23", port="22"
)
# ssh connection information of OE, for root user
_vcu_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.107.123.162", username="core", password="system123", port="22"
)

_vcu_master_node = MasterNode(
    k8s_connection_details=_vcu_k8s_connection_details,
    ssh_connection_details=_vcu_ssh_connection_details,
)
_vcu_k8s = K8S(namespace="cran17", master_node=_vcu_master_node)

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

# VDU configuration for deployment

_vdu_vnf_1 = DeploymentVnfStack(
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
# ssh connection information of OE, for tenant user
_ssh_connection_details = SshServiceDetails(
    addr="10.70.83.66", username="core", password="system123"
)
# ssh connection information of OE, for cloudadmin user
_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.70.83.66", username="core", password="system123", port="22"
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

# VDU oam http connection
_vdu_oam_http_connection_details = HttpConnectionDetails(
    addr="10.70.83.98", port="443", username="Nemuadmin", password="nemuuser"
)

_ru_pdu = TP(addr="10.97.65.16", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16])

_attenuator_5G = TopYoung(
    ip_addr="10.97.83.3",
    port=1000,
    attenuation_port_numbers=[9, 10, 11, 12],
    model="PA-8-2-4-127-0.5-B-S",
)

# RU configuration
_ru_1 = RU(
    ru_hw_group="RU_INT_ECPRI",
    radio_type="AEQP",
    serial_number="1M210320625",
    attenuation_ports=[
        _attenuator_5G.attenuator_ports[9],
        _attenuator_5G.attenuator_ports[10],
        _attenuator_5G.attenuator_ports[11],
        _attenuator_5G.attenuator_ports[12]
    ],
    pdu_port=_ru_pdu.pdu_ports[2]
)

# PXE server info for FHGW deployment
_pxe_server_ssh_info = SshServiceDetails(
    addr="10.56.103.30", username="root", password="nokia123"
)
_pxe_server = PxeServer(
    nfs_ip="10.56.103.30", ssh_connection_details=_pxe_server_ssh_info
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

# VDU global configuration
_vdu_1 = VDU(
    cloud_deployment=_k8s_cloud_deployment,
    oam_http_connection_details=_vdu_oam_http_connection_details,
    fhgws=[_fhgw_1],
    # route configuration of f1m link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_m_ip_addr=NetworkAddress(
        v4="10.70.83.84",
        vlan_id=2115,
        routing_v4=RoutingInformation(gateway="10.70.83.81/29"),
    ),
    # route configuration of f1c link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_c_ip_addr=NetworkAddress(
        v4="10.70.83.82",
        vlan_id=2115,
        routing_v4=RoutingInformation(gateway="10.70.83.81/29"),
    ),
    # route configuration of f1u link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_u_ip_addr=NetworkAddress(
        v4="10.70.83.82",
        vlan_id=2115,
        routing_v4=RoutingInformation(gateway="10.70.83.81/29"),
    ),

    instance_id=4294967294,
)

# mcc, mnc configuration
_realcore = RealCore(five_g=None, mcc="262", mnc="03", pdns=None)

_cbts = CloudBts(
    dus=[_vdu_1],  # vdu related parameter
    cu=_cu,
    cloud_deployment=_vcu_k8s_cloud_deployment,
    vnf_name="hgz-4294967294",
    instance_id="4294967294",
    global_bts_id="4294967294",
)

#  iperf server info
_appserver_ssh = SshServiceDetails(
    addr="10.97.97.18", username="ute", password="Ut3pa5s#ff97"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.106.164.168",
    iperf_path="/data/data/com.nokia.syve.uemanager.mobile/",
    port="5013",
)

_appserver = AppServer(_iperf)

# # Mifi
# ue_config_path = os.path.join(_cfg_dir, "TestData/mifi.yml")
# if os.path.isfile(ue_config_path):
#     with open(ue_config_path) as f:
#         ue_config = yaml.load(f, Loader=yaml.FullLoader)
# else:
#     ue_config = ""
dingli = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.97.83.29", username="root", password="123456"
    ),
    serial_number="9YS0220624012499",
    server_dir="/cygdrive/c/pyro_server",
    python_path="/cygdrive/c/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["pioneer", "huawei1"],
)




# Testpc
# UTE IP address and User Name, Password
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.97.65.246", username="ute", password="ute"
    ),
    connections=[_cbts]
)

# Testline configuration
tl = TestLine(
    test_pc=_test_pc,
    # ues=[huawei1],
    ues=[dingli],
    gnbs=[_cbts],
    # enbs=[_real_enb],
    tl_cloud_topology="CLOUD_5G_AIC_SA_1XAndroid_1XvDU_OE20_1XFHGW_1XAEQP_1XAEQE",
    cloud_hostings=[_ncir],
    test_pcs=[_test_pc],
    attenuator = _attenuator_5G,
    core=_realcore,
    appserver=_appserver,
)

# only tl variable can be accessed by user

__all__ = ["tl"]
