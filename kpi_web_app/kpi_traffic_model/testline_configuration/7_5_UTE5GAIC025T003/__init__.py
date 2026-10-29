__maintainer__ = "gao zhuo"
__team__ = "I_NSB_MN_RAN_PZ_1_HAZ_3_GMS "
__email__ = "I_NSB_MN_RAN_PZ_1_HAZ_3@internal.nsn.com"
__owner_email__ = "zhuo1.1.gao@nokia-sbell.com"

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
        addr="10.108.197.178", username="core", password="system123"
    ),
    # configuration for connection of open stack UI, default port is 5000
    open_stack_connection_details=OpenStackConnectionDetails(
        username="core",
        password="system123",
        ip_addr="10.108.197.178",
        tenant="cran1",
    ),
    # BMC configuration of OE
    bmc_connection_details=BmcConnectionDetails(
        addr="10.108.194.18", username="admin", password="Nokia*1234567890"
    ),
)


# configuration of VCU related NCIR/OSP
_ncir = NCIR(compute_nodes=[], control_nodes=[_control], version="OE20")

# CU configuration
_cu = CU(
    # CU web UI ip address, oam interface ip of oam vm
    backhaul_site_oam_ip=NetworkAddress(
		v4="10.107.205.77"
		),
    # VCU OAM ssh connection, oam interface ip of oam vm
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.107.205.77", username="serviceuser", password="Pl(FzaYj5~c5;q"
    ),
    # VCU OAM http connection, oam interface ip of oam vm
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.107.205.77", username="Nemuadmin", password="Nokia@123", port="443"
    ),
    # route configuration for x2 link to ENB on VCU, v4 is network address of ENB x2 link

    # route configuration for f1c link to VDU on VCU, v4 is network address of VDU f1c link
    f1c=NetworkAddress(
        v4="10.107.90.144",
        vlan_id=1341,
        routing=RoutingInformation(gateway="10.57.173.65/26"),
    ),

    # route configuration for f1u link to VDU on VCU, v4 is network address of VDU f1u link
    f1u=NetworkAddress(
        v4="10.110.40.172",
        vlan_id=1342,
        routing=RoutingInformation(gateway="10.107.90.128/26"),
    ),

    xnc=NetworkAddress(
        v4="10.107.90.209",
        vlan_id=1343,
        routing_v4=RoutingInformation(gateway="10.107.90.192/26"),
    ),
    xnu=NetworkAddress(
        v4="10.107.91.102",
        vlan_id=1344,
        routing_v4=RoutingInformation(gateway="10.107.91.0/25"),
    ),

    ngc=NetworkAddress(
        v4="10.107.92.80",
        vlan_id=1347,
        routing_v4=RoutingInformation(gateway="10.107.92.64/26"),
    ),
    ngu=NetworkAddress(
        v4="10.107.91.230",
        vlan_id=1345,
        routing_v4=RoutingInformation(gateway="10.107.91.128/25"),
    ),
    tracing=NetworkAddress(
        v4="10.107.89.1",
        vlan_id=1340,
        routing_v4=RoutingInformation(gateway="10.107.88.0/23"),
    ),
)


# test pc information of enb
_enb_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.0.81.65", username="noklab\five-tester", password="Nokia123!"
    ),
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
    addr="10.107.99.210", username="core", password="system123", port="22"
)

# ssh connection information of OE, for root user
_vcu_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.107.99.210", username="core", password="system123", port="22"
)

_vcu_master_node = MasterNode(
    k8s_connection_details=_vcu_k8s_connection_details,
    ssh_connection_details=_vcu_ssh_connection_details,
)

_vcu_k8s = K8S(namespace="cran10", master_node=_vcu_master_node)
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
    addr="10.108.197.178", username="core", password="system123", port="22"
)

# ssh connection information of OE, for cloudadmin user
_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.108.197.178", username="core", password="system123", port="22"
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
    addr="10.108.197.210", port="443", username="Nemuadmin", password="Nokia@123"
)


_ru_pdu = TP(addr="10.97.83.3", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16])


_attenuator_5G = TopYoung(
    ip_addr="10.97.83.3",
    port=1000,
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    model="TAS16T16-51-120-1S-DES",
)

# RU configuration
_ru_1 = RU(
    ru_hw_group="RU_INT_ECPRI",
    radio_type="AZQJ",
    serial_number="1M222701738",
    attenuation_ports=[
        _attenuator_5G.attenuator_ports[1],
        _attenuator_5G.attenuator_ports[2],
        _attenuator_5G.attenuator_ports[3],
        _attenuator_5G.attenuator_ports[4],
        _attenuator_5G.attenuator_ports[5],
        _attenuator_5G.attenuator_ports[6],
        _attenuator_5G.attenuator_ports[7],
        _attenuator_5G.attenuator_ports[8],
    ],
    pdu_port=_ru_pdu.pdu_ports[2]
)
_ru_2 = RU(
    ru_hw_group="RU_INT_ECPRI",
    radio_type="AHEGB",
    serial_number="EA203761454",
    attenuation_ports=[
        _attenuator_5G.attenuator_ports[1],
        _attenuator_5G.attenuator_ports[2],
        _attenuator_5G.attenuator_ports[3],
        _attenuator_5G.attenuator_ports[4],
    ],
    pdu_port=_ru_pdu.pdu_ports[1]
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


# VDU global configuration
_vdu_1 = VDU(
    cloud_deployment=_k8s_cloud_deployment,
    oam_http_connection_details=_vdu_oam_http_connection_details,
    fhgws=[_fhgw_1],
    # route configuration of f1m link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_m_ip_addr=NetworkAddress(
        v4="10.108.197.210",
        vlan_id=1816,
        routing_v4=RoutingInformation(gateway="10.108.197.208/29"),
    ),
    # route configuration of f1c link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_c_ip_addr=NetworkAddress(
        v4="10.108.197.202",
        vlan_id=1815,
        routing_v4=RoutingInformation(gateway="10.108.197.200/29"),
    ),
    # route configuration of f1u link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_u_ip_addr=NetworkAddress(
        v4="10.108.197.202",
        vlan_id=1815,
        routing_v4=RoutingInformation(gateway="10.108.197.200/29"),
    ),
    instance_id=11184,
)

# mcc, mnc configuration
_realcore = RealCore(five_g=None, mcc="262", mnc="03", pdns=None)

_cbts = CloudBts(
    dus=[_vdu_1],  # vdu related parameter
    cu=_cu,
    cloud_deployment=_vcu_k8s_cloud_deployment,
    vnf_name="hgz-11184",
    instance_id="11184",
    global_bts_id="11184",
)


#  iperf server info
_appserver_ssh = SshServiceDetails(
    addr="10.56.198.156", username="ute", password="UTE.debian12",port="50002",
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.56.198.156",
    iperf_path="/user/bin/",
    port="50002",
)

_appserver = AppServer(_iperf)

huawei = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.97.65.138", username="T03-tester", password="Nokia123!"
    ),
    serial_number="f82c7eee",

    server_dir="/cygdrive/c/pyro_server",
    python_path="/cygdrive/c/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["Commercial", "huawei_mate40"],
)
ue_config_path = os.path.join(_cfg_dir, "TestData/inseego2.yml")
if os.path.isfile(ue_config_path):
    with open(ue_config_path) as f:
        ue_config = yaml.load(stream=f, Loader=yaml.FullLoader)
else:
    ue_config = ""

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
        addr="10.0.81.65", username="ute", password="UTE.debian12"
    ),
    connections=[_cbts]
)

# Testline configuration
tl = TestLine(
    test_pc=_test_pc,
    ues=[ue_config, huawei],
    gnbs=[_cbts],
    # enbs=[_real_enb],
    tl_cloud_topology="CLOUD_5G_AIC_SA_1xAndroid_1xHPE_1xAZQJ",
    cloud_hostings=[_ncir],
    test_pcs=[_test_pc],
    attenuator=_attenuator_5G,
    core=_realcore,
    appserver=_appserver,
)

# only tl variable can be accessed by user

__all__ = ["tl"]
