__maintainer__ = "Chen Tingting"
__team__ = "I_NSB_MN_5GSC_5GSW_ENG_AIC_SI_CN_PCI_GMS <I_NSB_MN_5GSC_5GSW_ENG_AIC_SI_CN_PCI@internal.nsn.com>"
__email__ = "I_NSB_MN_5GSC_5GSW_ENG_AIC_SI_CN_PCI@internal.nsn.com"
__owner_email__ = "tingting.chen@nokia-sbell.com"

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
from taf.config.testline import RealEnb, NetworkAddress, RoutingInformation
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU
from taf.config.testline.lab_infrastructure import PxeServer
from taf.config.testline.core import RealCore
from taf.config.testline.connection_details import K8SConnectionDetails
from taf.config.testline.gnb.du import FHGW
from taf.config.testline.gnb.du import VDU
from taf.config.testline.cloud_hosting import MasterNode, K8S, HelmChart
from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.config.testline.radio import RU
from taf.config.testline.nms import Netact
from taf.config.testline.ue import Android
# from taf.config.testline.pdu import HBTE as PBHBTE
from taf.config.testline.pdu import FPFH
from taf.config.testline.attenuator import TopYoung, HBTE
from taf.config.testline.nms import NMS
from taf.config.testline.nom import NOM
from taf.config.testline.nms import Netact

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# VCU related NCIR controlNode
_control = ControlNode(
    # configuration for ssh connecting to OE
    default_ssh_connection_details=SshServiceDetails(
        addr="10.110.9.4", username="nruser9", password="Nokia$12345"
    ),
    # configuration for connection of open stack UI, default port is 5000
    open_stack_connection_details=OpenStackConnectionDetails(
        username="nruser9",
        password="Nokia$12345",
        ip_addr="10.110.9.4",
        tenant="nr9",
    ),
    # BMC configuration of OE
    bmc_connection_details=BmcConnectionDetails(
        addr="10.71.160.212", username="admin", password="Nokia*1234567890"
    ),
)
# configuration of VDU related NCIR
_ncir = NCIR(compute_nodes=[], control_nodes=[_control], version="ncir_19")

# CU configuration
_cu = CU(
    # CU web UI ip address, oam interface ip of oam vm
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.107.115.108"
        # v6=''
    ),
    # VCU OAM ssh connection, oam interface ip of oam vm
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.110.10.98", username="cranuser1", password="systeM!23"
    ),
    # VCU OAM http connection, oam interface ip of oam vm
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.110.177.196", username="Nemuadmin", password="nemuuser", port="443"
    ),
    # route configuration for x2 link to ENB on VCU, v4 is network address of ENB x2 link
    x2c=NetworkAddress(
        v4="10.110.64.0",
        vlan_id=3116,
        routing=RoutingInformation(gateway="10.110.64.1", ip_prefix_length=25),
    ),
    # route configuration,  for x2 link to ENB on VCUv4 is network address of ENB x2 link
    f1c=NetworkAddress(
        v4="10.110.64.128",
        vlan_id=3117,
        routing=RoutingInformation(gateway="10.110.64.129", ip_prefix_length=25),
    ),
    tracing=None,
)

# VDU configuration for deployment
_vdu_vnf_0 = DeploymentVnfStack(
    name="aic-vdu",  # this is vdu release name, the name should only be lower case and only can include alphabet, number, _
    yaml_file=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/aic_vdu_values_override_0.yaml"
    ),
)

# VDU internal network configuration for deployment
_vdu_intnet_0 = DeploymentNetworkStack(
    name="aic-intnet",  # this is intnet release name, the name should only be lower case and only can include alphabet, number, _
    yaml_file=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/aic_intnet_values_override_0.yaml"
    ),
)

# ssh connection information of OE, for tenant user
_ssh_connection_details = SshServiceDetails(
    addr="10.69.54.210", username="cranuser1", password="systeM!23"
)

# ssh connection information of OE, for cloudadmin user
_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.69.54.210", username="core", password="system123", port="22"
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
    networks=[_vdu_intnet_0],
    vnfs=[_vdu_vnf_0],
    cloud_hosting=_k8s,
    cluster_preparation=_cluster_preparation_du,
    prerequisite=_prerequisite_du,
    cnf=_cnf_du,
)

# VDU oam http connection
_vdu_oam_http_connection_details = HttpConnectionDetails(
    addr="10.69.54.242", port="443", username="Nemuadmin", password="nemuuser"
)

# RU PDU
# _ru_pdu = PBHBTE(addr="10.97.122.137", port_numbers=[3])
_ru_pdu = FPFH(addr="10.97.122.49",
               port_numbers=[1,2,3,4,5,6],
               login="admin",
               password="admin",
               )
_attenuator_5G = TopYoung(
    ip_addr="10.97.122.6",
    port=3000,
    attenuation_port_numbers=[i for i in range(257)],
    model="32X8",
)
# RU configuration
_ru_1 = RU(
    ru_hw_group="RU_INT_ECPRI",
    radio_type="AEQP",
    serial_number="1M213504204",
	attenuation_ports=[
        _attenuator_5G.attenuator_ports[13],
        _attenuator_5G.attenuator_ports[14],
        _attenuator_5G.attenuator_ports[15],
        _attenuator_5G.attenuator_ports[16],
    ],
	# pdu_port=_ru_pdu.pdu_ports[3]
    pdu_port=_ru_pdu.pdu_ports[4]
)

# PXE server info for FHGW deployment
_pxe_server_ssh_info = SshServiceDetails(
    addr="10.71.160.213", username="root", password="nokia123"
)
_pxe_server = PxeServer(
    nfs_ip="10.71.160.213", ssh_connection_details=_pxe_server_ssh_info
)

# FHGW information
_fhgw_0 = FHGW(
    user_config_path=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/FHGW_0/user_config_0.yaml"
    ),
    rus=[_ru_1],
    pxe_server=_pxe_server,
)

# VDU global configuration
_vdu_0 = VDU(
    cloud_deployment=_k8s_cloud_deployment,
    oam_http_connection_details=_vdu_oam_http_connection_details,
    fhgws=[_fhgw_0],
)

# mcc, mnc configuration
_realcore = RealCore(five_g=None, mcc="262", mnc="03", pdns=None)

_appserver_ssh = SshServiceDetails(
    addr="10.108.229.128", username="ute", password="ute"
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_name="rmnet_data0",
    network_interface_address="10.108.229.128",
)

_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.97.122.30", username="shwu", password="Nokia@123"
    ),
    serial_number="RFCT30V73CY",  # R5CN20LYP5R R5CN20HRWLM R5CN212N3RX R3CR50K9TZP R3CR40TPM5K
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "samsung"],
    service_call_attach=17,
    service_call_detach=17,
)
# ######## start of NOM ######################################################
_nom_ssh_connection_edge0 = SshServiceDetails(
    addr="10.39.156.122", username="cloud-user"
)

_nom1 = NOM(
    ssh_connections_info=[_nom_ssh_connection_edge0],
    https_main_info=HttpConnectionDetails(
        addr="https://neo-hosting-page.srncnms04.srnblr.nsn-rdnet.net/",
        username="cnms04",
        password="Qwer_1234",
    ),
    https_user_mgmt_info=HttpConnectionDetails(
        addr="https://user-mgmt.srncnms04.srnblr.nsn-rdnet.net",
    ),
    https_rest_info=HttpConnectionDetails(
        addr="https://apigw.srncnms04.srnblr.nsn-rdnet.net",
    ),
    neo_endpoints_ip="10.39.156.88",
)

_cnms = NMS(addr="10.39.156.122", nom=_nom1)

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
    addr="10.110.10.98", username="cranuser1", password="systeM!23"
)
# ssh connection information of OE, for root user
_vcu_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.110.10.98", username="core", password="system123", port="22"
)

_vcu_master_node = MasterNode(
    k8s_connection_details=_vcu_k8s_connection_details,
    ssh_connection_details=_vcu_ssh_connection_details,
)

_vcu_k8s = K8S(namespace="cran1", master_node=_vcu_master_node)

_cluster_preparation_cu_1 = HelmChart(
    name="aic-vcu-cluster-preparation",
    yaml_file=os.path.join(_cfg_dir, 'vcu-cluster-preparation.yaml'),
)

_prerequisite_cu_1 = HelmChart(
    name="aic-vcu-prerequisite",
    yaml_file=os.path.join(_cfg_dir, 'vcu-prerequisite.yaml'),
)

_cnf_cu_1 = HelmChart(
    name="aic-vcu",
    yaml_file=os.path.join(_cfg_dir, 'vcu-cnf.yaml'),
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


# VCU global configuration
_cbts_0 = CloudBts(
    dus=[_vdu_0],  # vdu related parameter
    cu=_cu,
    cloud_deployment=_vcu_k8s_cloud_deployment,
    vnf_name="cran1",
    instance_id="10790",
    global_bts_id="10790",
)

#  UE
# _appserver_ssh = SshServiceDetails(addr="10.108.229.127", username="ute", password="ute")
_appserver_ssh = SshServiceDetails(
    addr="10.108.229.128", username="ute", password="ute"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_name="rmnet_data0",
    network_interface_address="10.108.229.128",
)

_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.97.122.30", username="shwu", password="Nokia@123"
    ),
    serial_number="RFCT30V73CY",  # R5CN20LYP5R R5CN20HRWLM R5CN212N3RX R3CR50K9TZP R3CR40TPM5K
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "samsung"],
    service_call_attach=17,
    service_call_detach=17,
)

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.108.229.123", username="ute", password="ute"
    ),
     connections=[_cbts_0]
)

tl = TestLine(
    test_pc=_test_pc,
    nms=_cnms,
    gnbs=[_cbts_0],
#   enbs=[_real_enb],
    tl_cloud_topology="CLOUD_5G_CR_T0790_DRAN_SNO_AEQP_1xCell_SA_TDD_Android",
    cloud_hostings=[_vcu_k8s],
    test_pcs=[_test_pc],
    attenuators=[_attenuator_5G],
    ues=[_android],
    core=_realcore,
)

# only tl variable can be accessed by user
__all__ = ["tl"]
