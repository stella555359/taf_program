__maintainer__ = "I_HAZ1_RRM7_CODER_TEAM@internal.nsn.com"
__team__ = "NSB MN SRAN PROD IWK HZ GMS "
__email__ = "I_HAZ1_RRM7_CODER_TEAM@internal.nsn.com"

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
)
from taf.config.testline.testpc import TestPc
from taf.config.testline import RealEnb, NetworkAddress, RoutingInformation
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU
from taf.config.testline import DU
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, HBTE
from taf.config.testline.lab_infrastructure import PxeServer
from taf.config.testline.appserver import AppServer
from taf.config.testline.attenuator import AttenuationPort, TopYoung
from taf.config.testline.attenuator import HBTE as HB
from taf.config.testline.core import RealCore
from taf.config.testline.nms import NMS
from taf.config.testline.nom import NOM
#for proxy ue
from taf.config.testline.appserver import TafUeAppServer
from taf.config.testline import TafUeDataTransferProtocol
from taf.config.testline.pdn import PDNTafUeAndroidDetails
from taf.config.testline.connection_details import IperfDataTransferDetails
from taf.config.testline.ue import TafUeAndroid,Android
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




########### Part 2: cloud_hostings ########################
# VDU related NCIR controlNode
_control = ControlNode(
    # configuration for ssh connecting to OE
    default_ssh_connection_details=SshServiceDetails(
        addr="10.110.10.66", username="cranuser4", password="systeM!23"
    ),
    # configuration for connection of open stack UI, default port is 5000
    open_stack_connection_details=OpenStackConnectionDetails(
        username="cranuser4",
        password="systeM!23",
        ip_addr="10.110.10.66",
        tenant="cran4",
    ),
    # BMC configuration of OE
    bmc_connection_details=BmcConnectionDetails(
        addr="10.56.10.18", username="admin", password="CNnokia_123nokia"
    ),
)

# configuration of VCU related NCIR/OSP
_ncir = NCIR(compute_nodes=[], control_nodes=[_control], version="OE20")

########### Part 6: attenuator ############################
_attenuator = HB(
    ip_addr="10.56.107.5",
    port=5000,
    attenuation_port_numbers=[i for i in range(1, 127)],
    model="PAM-16X16-6-63-0.5-S",
)

########### Part 3: gnbs ##################################
# RU configuration
_pdu = HBTE(addr="10.97.65.194", port_numbers=[3])
_pdu = HBTE(addr="10.97.65.194", port_numbers=[3])
_ru_1 = RU(
    ru_hw_group="RU_INT_ECPRI",
    serial_number="1M202405022",
    radio_type="AEQE",
    pdu_port=_pdu.pdu_ports[3],
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[18],
    ],
)

# PXE server info for FHGW deployment
_pxe_server_ssh_info = SshServiceDetails(
    addr="10.56.10.35", username="robot", password="robot"
)
_pxe_server = PxeServer(
    nfs_ip="10.97.120.170", ssh_connection_details=_pxe_server_ssh_info
)

_vdu_vnf_0 = DeploymentVnfStack(
    name="aic-vdu",
    yaml_file=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/aic_vdu_values_override_0.yaml"
    ),
)

# VDU internal network configuration for deployment
_vdu_intnet_0 = DeploymentNetworkStack(
    name="aic-intnet",
    yaml_file=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/aic_intnet_values_override_0.yaml"
    ),
)

# ssh connection information of OE, for tenant user
# _ssh_connection_details = SshServiceDetails(
#     addr="10.56.10.50", username="cranuser1", password="systeM!23"
# )
_ssh_connection_details = SshServiceDetails(
    addr="10.56.10.50", username="core", password="system123"
)
# ssh connection information of OE, for cloudadmin user
_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.56.10.50", username="core", password="system123", port="22"
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
    networks=[_vdu_intnet_0],
    vnfs=[_vdu_vnf_0],
    cloud_hosting=_k8s,
    cluster_preparation=_cluster_preparation_du,
    prerequisite=_prerequisite_du,
    cnf=_cnf_du,
)

# VDU oam http connection
_vdu_oam_http_connection_details = HttpConnectionDetails(
    addr="10.56.10.82", port="443", username="Nemuadmin", password="Nokia@123"
)

# FHGW information
_fhgw_0 = FHGW(
    user_config_path=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/FHGW_0/fhgw_user_config_0.yaml"
    ),
    rus=[_ru_1],
    pxe_server=_pxe_server,
)

# fhgw extra parameter configuration
_fhgw_0.ssh_username = "toor4nsn"
_fhgw_0.ssh_password = "Fhgw@nokia123!"

# VDU global configuration
_vdu_0 = VDU(
    cloud_deployment=_k8s_cloud_deployment,
    oam_http_connection_details=_vdu_oam_http_connection_details,
    fhgws=[_fhgw_0],
    # route configuration of f1m link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_m_ip_addr=NetworkAddress(
        v4="192.168.254.33",
        vlan_id=295,
        routing=RoutingInformation(gateway="192.168.254.34", ip_prefix_length=26),
    ),
    # route configuration of f1c link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_c_ip_addr=NetworkAddress(
        v4="10.56.10.74",
        vlan_id=615,
        routing=RoutingInformation(gateway="10.56.10.73", ip_prefix_length=29),
    ),
    # route configuration of f1u link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_u_ip_addr=NetworkAddress(
        v4="10.56.104.75",
        vlan_id=615,
        routing=RoutingInformation(gateway="10.56.104.73", ip_prefix_length=29),
    ),
    instance_id=11074,
)

# VCU configuration ************************TBD Lance
_cu = CU(
    # CU web UI ip address, oam interface ip of oam vm
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.110.29.132"
        # v6='2a00:8a00:8000:136:10:57:159:1111'
    ),
    # VCU OAM ssh connection, oam interface ip of oam vm
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.110.29.132", username="Nemuadmin", password="Nokia@123"
    ),
    # VCU OAM http connection, oam interface ip of oam vm
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.110.29.132", username="Nemuadmin", password="Nokia@123", port="443"
    ),
    # route configuration for x2 link to ENB on VCU, v4 is network address of ENB x2 link
    x2c=NetworkAddress(
        v4="10.70.179.4",
        vlan_id=2010,
        routing=RoutingInformation(gateway="10.70.179.161", ip_prefix_length=27),
    ),
    x2u=NetworkAddress(
        v4="10.70.179.68",
        vlan_id=2011,
        routing=RoutingInformation(gateway="10.70.179.193", ip_prefix_length=27),
    ),
    # route configuration for f1c link to VDU on VCU, v4 is network address of VDU f1c link
    f1c=NetworkAddress(
        v4="10.70.179.4",
        vlan_id=2001,
        routing=RoutingInformation(gateway="10.70.179.193", ip_prefix_length=28),
    ),
    # route configuration for f1u link to VDU on VCU, v4 is network address of VDU f1u link
    f1u=NetworkAddress(
        v4="10.70.179.136",
        vlan_id=2002,
        routing=RoutingInformation(gateway="10.110.40.1", ip_prefix_length=25),
    ),
    s1u=NetworkAddress(
        v4="10.70.179.242",
        vlan_id=2012,
        routing=RoutingInformation(gateway="10.107.109.225", ip_prefix_length=27),
    ),
    tracing=None,
)

# k8s information
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
    addr="10.110.10.66", username="cranuser4", password="systeM!23"
)
# ssh connection information of OE, for root user
_vcu_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.110.10.66", username="core", password="system123", port="22"
)

_vcu_master_node = MasterNode(
    k8s_connection_details=_vcu_k8s_connection_details,
    ssh_connection_details=_vcu_ssh_connection_details,
)
_vcu_k8s = K8S(namespace="cran4", master_node=_vcu_master_node)

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

_cbts = CloudBts(
    dus=[_vdu_0],  # vdu related parameter
    cu=_cu,
    cloud_deployment=_vcu_k8s_cloud_deployment,
    vnf_name="hgz-11074",
    instance_id="11074",
    global_bts_id="11074",
)

########### Part 4: UE ####################################
#  iperf server info
_iperf2 = IperfDataTransferDetails(
    ssh_connection_details=SshServiceDetails(
        addr="10.56.198.156", username="ute", password="UTE.debian12"
    ),
    network_interface_address="10.56.198.156",
    iperf_path="iperf",
    port="5001",
)

_appserver = AppServer(_iperf2)

qualcomm8350 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.56.107.6", username="PzHZ2", password="Nokia123!"
    ),
    serial_number="3ef50d3c",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python39/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf2,
    serial_com=11,
    capabilities=["Commercial","qualcomm8350"],
)
ue_config_path = os.path.join(_cfg_dir, "TestData/inseego2.yml")
if os.path.isfile(ue_config_path):
    with open(ue_config_path) as f:
        ue_config = yaml.load(stream=f, Loader=yaml.FullLoader)
else:
    ue_config = ""
########### Part 7: CoreNetwork TBD Lance #################
# mcc, mnc configuration
_realcore = RealCore(five_g=None, mcc="262", mnc="03", pdns=None)

########### Part 8: NMS TBD Lance #########################
# _nom_ssh_connection_edge0 = SshServiceDetails(
#     addr="10.39.156.122", username="cloud-user"
# )

# _nom1 = NOM(
#     ssh_connections_info=[_nom_ssh_connection_edge0],
#     https_main_info=HttpConnectionDetails(
#         addr="https://neo-hosting-page.srncnms04.srnblr.nsn-rdnet.net/",
#         username="cnms04",
#         password="Qwer_1234",
#     ),
#     https_user_mgmt_info=HttpConnectionDetails(
#         addr="https://user-mgmt.srncnms04.srnblr.nsn-rdnet.net",
#     ),
#     https_rest_info=HttpConnectionDetails(
#         addr="https://apigw.srncnms04.srnblr.nsn-rdnet.net",
#     ),
#     neo_endpoints_ip="10.39.156.88",
# )

# _cnms = NMS(addr="10.39.156.122", nom=_nom1)

########### Part 9: Appserver #############################
# _appserver = AppServer(_iperf)
########### Part 1: Testpc ################################
# UTE IP address and User Name, Password
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.0.81.61", username="ute", password="ute"
    ),
    connections=[_cbts]
)
########### Main: Testline configuration ##################
tl = TestLine(
    test_pc=_test_pc,
    cloud_hostings=[_ncir],
    gnbs=[_cbts],
    ues=[ue_config, qualcomm8350],
    tl_cloud_topology="CLOUD_5G_AIC_SA_1xAndriod_1xvDU_OE20_1xFHGW_1xAEQE",
    attenuator=_attenuator,
    core=_realcore,
    # nms=_cnms,
    appserver=_appserver,
    appservers=[_appserver],
)

# only tl variable can be accessed by user

__all__ = ["tl"]
