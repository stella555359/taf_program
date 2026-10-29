__maintainer__ = "Yang Mengli"
__team__ = "I_NSB_MN_RAN_RD_VRF_HAZ1_2_GMS"
__email__ = "I_NSB_MN_RAN_RD_VRF_HAZ1_2_GMS@internal.nsn.com"
__owner_email__ = "mengli.yang@nokia-sbell.com"

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
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# vCU_0
_cu_0 = CU(
    # CU web UI ip address, oam interface ip of oam vm
    backhaul_site_oam_ip=NetworkAddress(v4="10.107.160.3"),
    # VCU OAM ssh connection, oam interface ip of oam vm
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.107.160.3", username="serviceuser", password="Pl(FzaYj5~c5;q"
    ),
    # VCU OAM http connection, oam interface ip of oam vm
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.107.160.3", username="Nemuadmin", password="nemuuser", port="443"
    ),
    tracing=None,
)

# ssh connection information of OE, for tenant user
_vcu_0_ssh_connection_details = SshServiceDetails(
    addr="10.107.123.162", username="cranuser3", password="systeM!23"
)
# ssh connection information of OE, for root user
_vcu_0_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.107.123.162", username="cranuser3", password="systeM!23", port="22"
)

_vcu_0_master_node = MasterNode(
    k8s_connection_details=_vcu_0_k8s_connection_details,
    ssh_connection_details=_vcu_0_ssh_connection_details,
)

_vcu_0_k8s = K8S(namespace="cran3", master_node=_vcu_0_master_node)

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
# ssh connection information of OE, for tenant user
_vdu_0_ssh_connection_details = SshServiceDetails(
    addr="10.108.195.146", username="core", password="system123"
)

# ssh connection information of OE, for cloudadmin user
_vdu_0_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.108.195.146", username="core", password="system123", port="22"
)

# master node information of OE
_vdu_0_master_node = MasterNode(
    k8s_connection_details=_vdu_0_k8s_connection_details,
    ssh_connection_details=_vdu_0_ssh_connection_details,
)

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
    addr="10.108.195.179", port="443", username="Nemuadmin", password="nemuuser"
)


# RU PDU
_ru_pdu = PBHBTE(addr="10.97.65.6", port_numbers=[1, 2, 5, 6])

_attenuator_5G = TopYoung(
    ip_addr="10.97.65.201",
    port=3000,
    attenuation_port_numbers=[
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        12,
        13,
        14,
        15,
        16,
        17,
        18,
        19,
        20,
        21,
        22,
        23,
        24,
        25,
        26,
        27,
        28,
        29,
        30,
        31,
        32,
    ],
    model="TAS16T16-51-120-1S-DES",
)

# RU configuration

_ru_1 = RU(
    ru_hw_group="RU_INT_ECPRI",
    radio_type="AHEGB",
    serial_number="K9191032028",
    attenuation_ports=[
        _attenuator_5G.attenuator_ports[9],
        _attenuator_5G.attenuator_ports[13],
    ],
    pdu_port=_ru_pdu.pdu_ports[5],
)

_ru_2 = RU(
    ru_hw_group="RU_INT_ECPRI",
    radio_type="AZQI",
    serial_number="1M212323141",
    attenuation_ports=[
        _attenuator_5G.attenuator_ports[17],
        _attenuator_5G.attenuator_ports[21],
        _attenuator_5G.attenuator_ports[25],
        _attenuator_5G.attenuator_ports[29],
    ],
    pdu_port=_ru_pdu.pdu_ports[1],
)

_ru_3 = RU(
    ru_hw_group="RU_INT_ECPRI",
    radio_type="AEQY",
    serial_number="1M220829960",
    attenuation_ports=[
        _attenuator_5G.attenuator_ports[5],
    ],
    pdu_port=_ru_pdu.pdu_ports[1],
)

_ru_4 = RU(
    ru_hw_group="RU_INT_ECPRI",
    radio_type="AEQE",
    serial_number="1M202413278",
    attenuation_ports=[
        _attenuator_5G.attenuator_ports[14],
        _attenuator_5G.attenuator_ports[18],
        _attenuator_5G.attenuator_ports[26],
    ],
    pdu_port=_ru_pdu.pdu_ports[1],
)

_ru_5 = RU(
    ru_hw_group="RU_INT_ECPRI",
    radio_type="AHCA",
    serial_number="AS202612686",
    attenuation_ports=[
        _attenuator_5G.attenuator_ports[16],
    ],
    pdu_port=_ru_pdu.pdu_ports[1],
)

_ru_6 = RU(
    ru_hw_group="RU_INT_ECPRI",
    radio_type="AHFII",
    serial_number="BL2316N44XW",
    attenuation_ports=[
        _attenuator_5G.attenuator_ports[1],
        _attenuator_5G.attenuator_ports[3],
        _attenuator_5G.attenuator_ports[7],
        _attenuator_5G.attenuator_ports[8],
    ],
    pdu_port=_ru_pdu.pdu_ports[1],
)

_real_enb = RealEnb(oam_ip="10.108.195.179", instance_id="10847", rms=[_ru_2])

# test pc information of enb
_enb_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.69.53.183", username="ute", password="ute"
    ),
    connections=[_real_enb],
)

# PXE server info for FHGW deployment
_pxe_server_ssh_info = SshServiceDetails(
    addr="10.56.103.30", username="root", password="nokia123"
)
_pxe_server = PxeServer(
    nfs_ip="10.56.103.30", ssh_connection_details=_pxe_server_ssh_info
)
# FHGW information
_fhgw_0 = FHGW(
    user_config_path=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/FHGW_0/fhgw_user_config_0.yaml"
    ),
    rus=[_ru_1, _ru_2],
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
    addr="10.106.243.149", username="ute", password="PZ1RRM3!5t6y7u"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.106.243.149",
    iperf_path="/data/data/com.nokia.syve.uemanager.mobile/",
    port="54015",
)

_appserver = AppServer(_iperf)

# UE configuration
Samsung_s22 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.97.65.202", username="aic", password="Nokia123!"
    ),
    serial_number="R5CTA17R6QH",
    server_dir="/cygdrive/c/pyro_server",
    # python_path="C:/Python27/python.exe",
    python_path="/cygdrive/c/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["Commercial", "samsung"],
)

Samsung_s24 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.97.65.202", username="aic", password="Nokia123!"
    ),
    serial_number="RFCX10ME4QR",
    server_dir="/cygdrive/c/pyro_server",
    # python_path="C:/Python27/python.exe",
    python_path="/cygdrive/c/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["Commercial", "samsung"],
)

_M70 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.97.65.202", username="aic", password="Nokia123!"
    ),
    serial_number="0123456789ABCDEF",
    server_dir="/cygdrive/c/pyro_server",
    python_path="/cygdrive/c/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["Qualcomm", "REAL_ANDROID_UE"],
)

Qualcomm = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.97.65.202", username="aic", password="Nokia123!"
    ),
    serial_number="3e5229bd",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "REAL_QUALCOMM_UE"],
)

oppo = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.97.65.202", username="aic", password="Nokia123!"
    ),
    serial_number="YH49FMYX4PEUNNGQ",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["Commercial", "OPPO"],
)

huawei1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.97.65.202", username="aic", password="Nokia123!"
    ),
    serial_number="7TD5T21415000127",
    server_dir="/cygdrive/c/pyro_server",
    python_path="/cygdrive/c/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["Commercial", "huawei1"],
)

_cbts = CloudBts(
    dus=[_vdu_0],
    cu=_cu_0,
    cloud_deployment=_vcu_0_k8s_cloud_deployment,
    instance_id="10847",
    global_bts_id="10847",
)


_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.69.53.183", username="ute", password="uteUTE!"
    ),
    connections=[_cbts],
)

tl = TestLine(
    test_pc=_test_pc,
    ues=[Qualcomm, Samsung_s22, Samsung_s24, _M70],
    gnbs=[_cbts],
    enbs=[_real_enb],
    tl_cloud_topology="CLOUD_5G_AIC_SA_1xAndroid_vDU_OE20_DC_1xAEQY_1xAEQE_1xAHEGB",
    attenuator=_attenuator_5G,
    appserver=_appserver,
    core=_realcore,
)

__all__ = ["tl"]
