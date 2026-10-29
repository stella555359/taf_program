__maintainer__ = "Yu Mengtian"
__team__ = "I_SG1_ATOM_SQUAD@internal.nsn.com"
__email__ = "I_SG1_ATOM_SQUAD@internal.nsn.com"
__owner_email__ = "mengtian.yu@nokia-sbell.com"

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
from taf.config.testline.pdu import HBTE as PBHBTE
from taf.config.testline.pdu import TopYoung as TP
from taf.config.testline.attenuator import HBTE
from taf.config.testline.nms import NMS
from taf.config.testline.nom import NOM
from taf.config.testline.nms import Netact
from taf.config.testline.pdu import PduPort, FPFH

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# CU configuration
_cu = CU(
    # CU web UI ip address, oam interface ip of oam vm
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.110.179.206"
        # v6=''
    ),
    # VCU OAM ssh connection, oam interface ip of oam vm
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.110.179.206", username="Nemuadmin", password="nemuuser"
    ),
    # VCU OAM http connection, oam interface ip of oam vm
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.110.179.206", username="Nemuadmin", password="nemuuser", port="443"
    ),
    tracing=None,
)

# enb for NSA
_real_enb = RealEnb(oam_ip="10.97.122.241", instance_id="", rms=[])

# test pc information of enb
# you can configure it as AIC UTE environment
_enb_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.108.229.68", username="ute", password="QAZqaz123!@#"
    ),
    connections=[_real_enb],
)

# VDU configuration for deployment
_vdu_vnf_0 = DeploymentVnfStack(
    name="aic-vdu",
    # this is vdu release name, the name should only be lower case and only can include alphabet, number, _
    yaml_file=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/aic_vdu_values_override_0.yaml"
    ),
)

# VDU internal network configuration for deployment
_vdu_intnet_0 = DeploymentNetworkStack(
    name="aic-intnet",
    # this is intnet release name, the name should only be lower case and only can include alphabet, number, _
    yaml_file=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/aic_intnet_values_override_0.yaml"
    ),
)

# ssh connection information of OE, for tenant user
_ssh_connection_details = SshServiceDetails(
    addr="10.97.127.149", username="cranuser1", password="systeM!23"
)

# ssh connection information of OE, for cloudadmin user
_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.97.127.149", username="core", password="system123", port="22"
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
    addr="10.97.127.170", port="443", username="Nemuadmin", password="nemuuser"
)

# RU PDU
_ru_pdu_7 = PBHBTE(addr="10.108.213.15", port_numbers=[4])

_ru_pdu_8 = PBHBTE(addr="10.108.213.15", port_numbers=[5])

_ru_pdu_9 = FPFH(
    port_numbers=[3],
    addr="10.108.213.7",
    login="admin",
    password="admin",
)


_hbte_params_7 = {
    "ip_addr": "10.108.213.37",
    "port": 5000,
    "attenuation_port_numbers": [3, 4],
    "model": "PA-16-8-4-127-0.5-B-S",
    "version": None,
}

_hbte_params_8 = {
    "ip_addr": "10.108.213.37",
    "port": 5000,
    "attenuation_port_numbers": [1, 2],
    "model": "PA-16-8-4-127-0.5-B-S",
    "version": None,
}

_hbte_params_9 = {
    "ip_addr": "10.108.213.34",
    "port": 5000,
    "attenuation_port_numbers": [15, 16],
    "model": "PA-16-16-6-127-0.5-B-S",
    "version": None,
}

_attenuator_5G_7 = HBTE(**_hbte_params_7)
_attenuator_5G_8 = HBTE(**_hbte_params_8)
_attenuator_5G_9 = HBTE(**_hbte_params_9)

# simulator RU configuration
_ru_1 = RU(
    ru_hw_group="FRMr5.1_1_4T4R",
    radio_type="AHCA",
    serial_number="6Q182502974",
    attenuation_ports=[
        _attenuator_5G_7.attenuator_ports[3],
        _attenuator_5G_7.attenuator_ports[4],
    ],
    pdu_port=_ru_pdu_7.pdu_ports[4]
)

_ru_2 = RU(
    ru_hw_group="FRMr5.1_1_4T4R",
    radio_type="AHCA",
    serial_number="6Q182502973",
    attenuation_ports=[
        _attenuator_5G_7.attenuator_ports[3],
        _attenuator_5G_7.attenuator_ports[4],
    ],
    pdu_port=_ru_pdu_7.pdu_ports[4]
)

_ru_3 = RU(
    ru_hw_group="FRMr5.1_1_4T4R",
    radio_type="AHCA",
    serial_number="6Q182502975",
    attenuation_ports=[
        _attenuator_5G_7.attenuator_ports[3],
        _attenuator_5G_7.attenuator_ports[4],
    ],
    pdu_port=_ru_pdu_7.pdu_ports[4]
)

_ru_4 = RU(
    ru_hw_group="FRMr5.1_1_4T4R",
    radio_type="AHCA",
    serial_number="6Q182502976",
    attenuation_ports=[
        _attenuator_5G_7.attenuator_ports[3],
        _attenuator_5G_7.attenuator_ports[4],
    ],
    pdu_port=_ru_pdu_7.pdu_ports[4]
)

_ru_5 = RU(
    ru_hw_group="FRMr5.1_1_4T4R",
    radio_type="AHCA",
    serial_number="6Q182502977",
    attenuation_ports=[
        _attenuator_5G_7.attenuator_ports[3],
        _attenuator_5G_7.attenuator_ports[4],
    ],
    pdu_port=_ru_pdu_7.pdu_ports[4]
)

_ru_6 = RU(
    ru_hw_group="FRMr5.1_1_4T4R",
    radio_type="AHCA",
    serial_number="6Q182502978",
    attenuation_ports=[
        _attenuator_5G_7.attenuator_ports[3],
        _attenuator_5G_7.attenuator_ports[4],
    ],
    pdu_port=_ru_pdu_7.pdu_ports[4]
)

# Real RU configuration
_ru_7 = RU(
    ru_hw_group="FRMr5.1_1_4T4R",
    radio_type="AHCA",
    serial_number="AS202612676",
    attenuation_ports=[
        _attenuator_5G_7.attenuator_ports[3],
        _attenuator_5G_7.attenuator_ports[4],
    ],
    pdu_port=_ru_pdu_7.pdu_ports[4]
)

_ru_8 = RU(
    ru_hw_group="FRMr5.1_1_4T4R",
    radio_type="AHCA",
    serial_number="AS202612684",
    attenuation_ports=[
        _attenuator_5G_8.attenuator_ports[1],
        _attenuator_5G_8.attenuator_ports[2],
    ],
    pdu_port=_ru_pdu_8.pdu_ports[5]
)

_ru_9 = RU(
    ru_hw_group="FRMr5.1_1_4T4R",
    radio_type="AHCA",
    serial_number="AS202612675",
    attenuation_ports=[
        _attenuator_5G_9.attenuator_ports[15],
        _attenuator_5G_9.attenuator_ports[16],
    ],
    pdu_port=_ru_pdu_9.pdu_ports[3]
)


# PXE server info for FHGW deployment
_pxe_server_ssh_info = SshServiceDetails(
    addr="10.108.213.25", username="ute", password="Cdslabadmin@"
)
_pxe_server = PxeServer(
    nfs_ip="10.108.213.25", ssh_connection_details=_pxe_server_ssh_info
)

# FHGW information
_fhgw_0 = FHGW(
    user_config_path=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/FHGW_0/user_config_0.yaml"
    ),
    rus=[_ru_1, _ru_2, _ru_3, _ru_4, _ru_5, _ru_6, _ru_7, _ru_8, _ru_9],
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
    addr="10.108.229.42", username="ute", password="Cdslabadmin@"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_name="rmnet_data0",
)

# _android = Android(
#     ssh_connection_details=SshServiceDetails(
#         addr="10.97.122.248", username="aic", password="Nokia123!"
#     ),
#     serial_number="R5CN21F5R6P",  # R5CN20LYP5R R5CN20HRWLM R5CN212N3RX
#     server_dir="/cygdrive/c/pyro_server",
#     python_path="C:/Python27/python.exe",
#     qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
#     diag_cfg_path="C:/pyro_server/DIAG.cfg",
#     # iperf_details=_iperf,
#     capabilities=["REAL_UE", "REAL_ANDROID_UE", "samsung"],
# )

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
    addr="10.110.18.226", username="cranuser11", password="systeM!23"
)
# ssh connection information of OE, for root user
_vcu_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.110.18.226", username="core", password="system123", port="22"
)

_vcu_master_node = MasterNode(
    k8s_connection_details=_vcu_k8s_connection_details,
    ssh_connection_details=_vcu_ssh_connection_details,
)

_vcu_k8s = K8S(namespace="cran11", master_node=_vcu_master_node)

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
    instance_id="10777",
    global_bts_id="10777",
)

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.108.229.68", username="ute", password="QAZqaz123!@#"
    ),
    connections=[_cbts_0]
)

tl = TestLine(
    test_pc=_test_pc,
    nms=_cnms,
    gnbs=[_cbts_0],
    #   enbs=[_real_enb],
    tl_cloud_topology="CLOUD_5G_CR_DRAN_SNO_3xRU_SA_FDD_Android",
    cloud_hostings=[_vcu_k8s],
    test_pcs=[_test_pc],
    #   attenuators=[_attenuator_5G, _attenuator_4G],
    #   ues=[_android],
    core=_realcore,
)

# only tl variable can be accessed by user
__all__ = ["tl"]
