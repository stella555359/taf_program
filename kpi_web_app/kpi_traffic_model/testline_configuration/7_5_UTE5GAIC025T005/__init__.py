__maintainer__ = "Guo Qianqian"
__team__ = "I_NSB_MN_RAN_RD_VRF_HAZ1_2_GMS"
__email__ = "I_NSB_MN_RAN_RD_VRF_HAZ1_2@internal.nsn.com"
__owner_email__ = "qianqian.guo@nokia-sbell.com"

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
from taf.config.testline.appserver import AppServer
from taf.config.testline.ue import Android
from taf.config.testline.pdu import HBTE as PBHBTE
from taf.config.testline.attenuator import HBTE
from taf.config.testline.attenuator import AttenuationPort, TopYoung
from taf.config.testline.nms import NMS
from taf.config.testline.nom import NOM

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# vCU_0
_cu_0 = CU(
    # CU web UI ip address
    backhaul_site_oam_ip=NetworkAddress(v4="10.107.160.13"),
    # VCU OAM ssh connection, oam interface ip of oam vm
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.107.160.13", username="serviceuser", password="Pl(FzaYj5~c5;q"
    ),
    # VCU OAM http connection
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.107.160.13", username="Nemuadmin", password="nemuuser", port="443"
    ),
    tracing=None,
)

# ssh connection information of CU tenant user
_vcu_0_ssh_connection_details = SshServiceDetails(
    addr="10.107.123.162", username="cranuser13", password="systeM!23"
)
# ssh connection information of OE, for root user
_vcu_0_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.107.123.162", username="core", password="system123", port="22"
)

_vcu_0_master_node = MasterNode(
    k8s_connection_details=_vcu_0_k8s_connection_details,
    ssh_connection_details=_vcu_0_ssh_connection_details,
)
# CU namespace
_vcu_0_k8s = K8S(namespace="cran13", master_node=_vcu_0_master_node)

# _cluster_preparation_cu_0 = HelmChart(
#     name="aic-vcu-cluster-preparation",
#     yaml_file=os.path.join(_cfg_dir, 'vcu-cluster-preparation.yaml'),
# )
#
# _prerequisite_cu_0 = HelmChart(
#     name="aic-vcu-prerequisite",
#     yaml_file=os.path.join(_cfg_dir, 'vcu-prerequisite.yaml'),
# )
#
# _cnf_cu_0 = HelmChart(
#     name="aic-vcu",
#     yaml_file=os.path.join(_cfg_dir, 'vcu-cnf.yaml'),
# )

_vcu_0_k8s_cloud_deployment = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    cloud_hosting=_vcu_0_k8s,
    # cluster_preparation=_cluster_preparation_cu_0,
    # prerequisite=_prerequisite_cu_0,
    # cnf=_cnf_cu_0,
)



# vDU_0
# ssh connection information of DU
_vdu_0_ssh_connection_details = SshServiceDetails(
    addr="10.70.85.82", username="core", password="system123"
)

# ssh connection information of DU
_vdu_0_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.70.85.82", username="core", password="system123", port="22"
)

# master node information of DU
_vdu_0_master_node = MasterNode(
    k8s_connection_details=_vdu_0_k8s_connection_details,
    ssh_connection_details=_vdu_0_ssh_connection_details,
)

# DU namespace
_vdu_0_k8s = K8S(namespace="cran1", master_node=_vdu_0_master_node)

# _cluster_preparation_du_0 = HelmChart(
#     name="aic-vdu-cluster-preparation",
#     yaml_file=os.path.join(_cfg_dir, 'vdu-cluster-preparation.yaml'),
# )
#
# _prerequisite_du_0 = HelmChart(
#     name="aic-vdu-prerequisite",
#     yaml_file=os.path.join(_cfg_dir, 'vdu-prerequisite.yaml'),
# )
#
# _cnf_du_0 = HelmChart(
#     name="aic-vdu",
#     yaml_file=os.path.join(_cfg_dir, 'vdu-cnf.yaml'),
# )

# VDU deployment configuration
_vdu_0_k8s_cloud_deployment = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    cloud_hosting=_vdu_0_k8s,
    # cluster_preparation=_cluster_preparation_du_0,
    # prerequisite=_prerequisite_du_0,
    # cnf=_cnf_du_0,
)

# VDU oam http connection
_vdu_0_oam_http_connection_details = HttpConnectionDetails(
    addr="10.70.85.114", port="443", username="Nemuadmin", password="nemuuser"
)




# RU PDU, all TL could use the same info
_ru_pdu = PBHBTE(addr="10.97.122.137", port_numbers=[7, 8, 4, 6, 5, 9, 10])

# PA configuration
_attenuator_5G = TopYoung(
    ip_addr="10.97.83.37",
    port=5000,
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32],
    model="TAS32T8-0.4G6- 120-1N-DES",
    version=None,
)

_ru_1 = RU(
    ru_hw_group="RU_INT_ECPRI",
    radio_type="AEQP",
    serial_number="1M211225078",
    attenuation_ports=[
        _attenuator_5G.attenuator_ports[3],
        _attenuator_5G.attenuator_ports[9],
		_attenuator_5G.attenuator_ports[10],
		_attenuator_5G.attenuator_ports[11],
    ],
    pdu_port=_ru_pdu.pdu_ports[7],
)

_ru_2 = RU(
    ru_hw_group="RU_INT_ECPRI",
    radio_type="AEQP",
    serial_number="1M213504194",
    attenuation_ports=[
        _attenuator_5G.attenuator_ports[2],
        _attenuator_5G.attenuator_ports[5],
    ],
    pdu_port=_ru_pdu.pdu_ports[8],
)

_ru_3 = RU(
    ru_hw_group="RU_INT_ECPRI",
    radio_type="AKQJ",
    serial_number="1M222600268",
    attenuation_ports=[
        _attenuator_5G.attenuator_ports[12],
        _attenuator_5G.attenuator_ports[29],
		_attenuator_5G.attenuator_ports[30],
		_attenuator_5G.attenuator_ports[31],
		_attenuator_5G.attenuator_ports[32],
    ],
    pdu_port=_ru_pdu.pdu_ports[4],
)

_ru_4 = RU(
    ru_hw_group="RU_INT_ECPRI",
    radio_type="AEQY",
    serial_number="1M220829952",
    attenuation_ports=[
        _attenuator_5G.attenuator_ports[15],
		_attenuator_5G.attenuator_ports[21],
		_attenuator_5G.attenuator_ports[22],
    ],
    pdu_port=_ru_pdu.pdu_ports[6],
)

_ru_5 = RU(
    ru_hw_group="RU_INT_ECPRI",
    radio_type="AEQP",
    serial_number="1M213504200",
    attenuation_ports=[
        _attenuator_5G.attenuator_ports[4],
        _attenuator_5G.attenuator_ports[7],
    ],
    pdu_port=_ru_pdu.pdu_ports[5],
)

_ru_6 = RU(
    ru_hw_group="RU_INT_ECPRI",
    radio_type="AHFIB",
    serial_number="BL2236V082T",
    attenuation_ports=[
        _attenuator_5G.attenuator_ports[23],
		_attenuator_5G.attenuator_ports[24],
    ],
    pdu_port=_ru_pdu.pdu_ports[9],
)

_ru_7 = RU(
    ru_hw_group="RU_INT_ECPRI",
    radio_type="AHFIB",
    serial_number="BL2236V082U",
    attenuation_ports=[
        _attenuator_5G.attenuator_ports[13],
        _attenuator_5G.attenuator_ports[14],
    ],
    pdu_port=_ru_pdu.pdu_ports[10],
)


# PXE server info for FHGW deployment
_pxe_server_ssh_info = SshServiceDetails(
    addr="10.56.103.30", username="ute", password="Cdslabadmin@"
)
_pxe_server = PxeServer(
    nfs_ip="10.56.103.30", ssh_connection_details=_pxe_server_ssh_info
)
# FHGW information
_fhgw_0 = FHGW(
    user_config_path=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/FHGW_0/fhgw_user_config_0.yaml"
    ),
    rus=[_ru_6, _ru_7],
    pxe_server=_pxe_server,
)



# VDU global configuration
_vdu_0 = VDU(
    cloud_deployment=_vdu_0_k8s_cloud_deployment,
    oam_http_connection_details=_vdu_0_oam_http_connection_details,
    fhgws=[_fhgw_0],
)



# mcc, mnc configuration
_realcore = RealCore(five_g=None, mcc="262", mnc="03", pdns=None)

#  iperf server info
_appserver_ssh = SshServiceDetails(
    addr="10.108.229.121", username="ute", password="ute"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.106.243.149",
    iperf_path="/data/data/com.nokia.syve.uemanager.mobile/",
    port="54015",
)

_appserver = AppServer(_iperf)

# UE configuration
_Samsung_S24 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.97.83.19", username="Pz1", password="Nokia@2w3e4r5t6y7u"
    ),
    serial_number="RFCX10868TH",
    # 26203,Samsung S24 (PN:SM-S921U)
    server_dir="/cygdrive/c/pyro_server",
    python_path="/cygdrive/c/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["Commercial", "samsung"],
)

_RedMi_K50 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.97.83.19", username="Pz1", password="Nokia@2w3e4r5t6y7u"
    ),
    serial_number="RKZDLBKR6XGIO7EQ",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["Commercial", "xiaomi"],
)

_Xiaomi11 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.97.83.19", username="Pz1", password="Nokia@2w3e4r5t6y7u"
    ),
    serial_number="c9057d71",
    server_dir="/cygdrive/c/pyro_server",
    python_path="/cygdrive/c/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["Commercial", "xiaomi"],
)



_cbts_0 = CloudBts(
    dus=[_vdu_0],
    cu=_cu_0,
    cloud_deployment=_vcu_0_k8s_cloud_deployment,
    instance_id="10765",
    global_bts_id="10765",
)

#_cbts_1 = CloudBts(
#    dus=[_vdu_1],
#    cu=_cu_1,
#    cloud_deployment=_vcu_1_k8s_cloud_deployment,
#    instance_id="10870",
#    global_bts_id="10870",
#)

# UTE info
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.56.198.45", username="ute", password="UTE.debian12 "
    ),
    connections=[_cbts_0],
)

tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts_0],
    tl_cloud_topology="CLOUD_5G_AIC_SA_1XAndroid_1XvCU_1XvDU_DELL_1XAKQJ_2XAEQY",
    ues=[_Samsung_S24, _RedMi_K50, _Xiaomi11],
    attenuator=_attenuator_5G,
    appserver=_appserver,
    core=_realcore,
)


__all__ = ["tl"]