import os

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
    HelmChart,
)
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.attenuator import (
    AttenuationPort,
    TopYoung
)  # added in taf.meta 5.4
from taf.config.testline.pdu import HBTE, PduPort, Pdu, EPC, ATEN, RRB, APC, Gude
from taf.config.testline.core import RealCore, RealCore5GDetails, AMF
from taf.config.testline import NetworkAddress, RoutingInformation
from taf.config.testline import RealEnb, Airscale, CommonUnit
from taf.config.testline import RU, RadioTypes
from taf.config.testline import CloudBts, CU
from taf.config.testline import VDU, FHGW
from taf.config.testline import PxeServer
from taf.config.testline import TestLine
from taf.config.testline import RealEnb
from taf.config.testline import TestPc
from taf.config.testline.ue import Android
from taf.config.testline.appserver import AppServer


__maintainer__ = "Dandan Fang"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_4_GMS <I_MN_5G_RAN_IV4_LINE_HZG_4@internal.nsn.com>"
)
__email__ = "dandan.fang@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))


# Testpc --confirm
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.49", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# CU

# CU0
_cu_0 = CU(
    instance_id=37180,
    global_bts_id=37180,
    backhaul_site_oam_ip=NetworkAddress(v4="10.57.209.142"),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.209.2", username="cranuser2112", password="systeM!23"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.209.142", username="Nemuadmin", password="nemuuser", port=443
    ),
    x2c=NetworkAddress(
        v4="10.57.210.88",
        vlan_id=110,
        routing=RoutingInformation(gateway="10.57.210.64", ip_prefix_length=26),
    ),
    x2u=NetworkAddress(
        v4="10.57.210.89",
        vlan_id=110,
        routing=RoutingInformation(gateway="10.57.210.64", ip_prefix_length=26),
    ),
    f1c=NetworkAddress(
        v4="10.57.210.24",
        vlan_id=109,
        routing=RoutingInformation(gateway="10.57.210.0", ip_prefix_length=26),
    ),
    f1u=NetworkAddress(
        v4="10.57.210.25",
        vlan_id=109,
        routing=RoutingInformation(gateway="10.57.210.0", ip_prefix_length=26),
    ),
    s1u=NetworkAddress(
        v4="10.57.209.46",
        vlan_id=102,
        routing=RoutingInformation(gateway="10.57.209.32", ip_prefix_length=27),
    ),
    tracing=None,
)

# ssh connection information of OE, for tenant user, tester used
_vcu_ssh_connection_details_0 = SshServiceDetails(
    addr="10.57.209.2", username="cranuser2112", password="systeM!23", port=22
)
# ssh connection information of OE, for root user
_vcu_k8s_connection_details_0 = K8SConnectionDetails(
    ip_addr="10.57.209.2", username="core", password="system123", port=22
)

_vcu_master_node_0 = MasterNode(
    k8s_connection_details=_vcu_k8s_connection_details_0,
    ssh_connection_details=_vcu_ssh_connection_details_0,
)

_vcu_k8s_0 = K8S(namespace="cran2112", master_node=_vcu_master_node_0)

_cnf_cu_0 = HelmChart(
    name="vcu2112",
    yaml_file=os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/cnf.yaml"),
)

_cluster_preparation_cu_0 = HelmChart(
    name=_cnf_cu_0.name + "-cluster-preparation",
    yaml_file=os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/preparation.yaml"),
)

_prerequisite_cu_0 = HelmChart(
    name=_cnf_cu_0.name + "-prerequisite",
    yaml_file=os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/prerequisite.yaml"),
)

_vcu_k8s_cloud_deployment_0 = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    cloud_hosting=_vcu_k8s_0,
    cluster_preparation=_cluster_preparation_cu_0,
    prerequisite=_prerequisite_cu_0,
    cnf=_cnf_cu_0,
)


_topyoung_params_1 = {
    "ip_addr": "10.71.204.27",
    "port": "23",
    "attenuation_port_numbers": [1, 18, 21, 35, 37, 52, 66, 83, 97, 115, 129, 130, 133,
                                 148, 163, 165, 178, 182, 193, 210, 227, 244],
    "model": "TAS16B16-51-90-0.5B-DES"
}

_attenuator_0 = TopYoung(**_topyoung_params_1)

_ru_pdu_0 = HBTE(addr="10.71.195.174", port_numbers=[1, 2, 4])
_ru_pdu_1 = HBTE(addr="10.71.195.176", port_numbers=[4])
_ru_pdu_2 = HBTE(addr="10.71.195.178", port_numbers=[4])
# ru account need to be changed
_ru_0 = RU(
    ru_hw_group="hw_group",
    pdu_port=_ru_pdu_0.pdu_ports[2],
    radio_type=RadioTypes.AHFII,
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.35",
        username="rfsw",
        password="5rfS2qmWC0AiFYvir7k8JekCN8/NklqDK5E6OWXuUVQ=",
    ),
    attenuation_ports=[
        _attenuator_0.attenuator_ports[193],
        _attenuator_0.attenuator_ports[210],
        _attenuator_0.attenuator_ports[227],
        _attenuator_0.attenuator_ports[244],
    ],
)

_ru_1 = RU(
    ru_hw_group="hw_group",
    pdu_port=_ru_pdu_1.pdu_ports[4],
    radio_type=RadioTypes.AHFIB,
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.35",
        username="rfsw",
        password="5rfS2qmWC0AiFYvir7k8JekCN8/NklqDK5E6OWXuUVQ=",
    ),
    attenuation_ports=[
        _attenuator_0.attenuator_ports[66],
        _attenuator_0.attenuator_ports[83],
    ],
)

_ru_2 = RU(
    ru_hw_group="hw_group",
    pdu_port=_ru_pdu_0.pdu_ports[4],
    radio_type=RadioTypes.AHLOA,
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.35",
        username="rfsw",
        password="5rfS2qmWC0AiFYvir7k8JekCN8/NklqDK5E6OWXuUVQ=",
    ),
    attenuation_ports=[
        _attenuator_0.attenuator_ports[97],
        _attenuator_0.attenuator_ports[115],
    ],
)

_ru_3 = RU(
    ru_hw_group="hw_group",
    pdu_port=_ru_pdu_2.pdu_ports[4],
    radio_type=RadioTypes.AEHC,
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.35",
        username="rfsw",
        password="5rfS2qmWC0AiFYvir7k8JekCN8/NklqDK5E6OWXuUVQ=",
    ),
    attenuation_ports=[
        _attenuator_0.attenuator_ports[1],
        _attenuator_0.attenuator_ports[18],
        _attenuator_0.attenuator_ports[21],
        _attenuator_0.attenuator_ports[35],
        _attenuator_0.attenuator_ports[52],
    ],
)

_ru_4 = RU(
    ru_hw_group="hw_group",
    pdu_port=_ru_pdu_0.pdu_ports[1],
    radio_type=RadioTypes.AWHQX,
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.35",
        username="rfsw",
        password="5rfS2qmWC0AiFYvir7k8JekCN8/NklqDK5E6OWXuUVQ=",
    ),
    attenuation_ports=[
        _attenuator_0.attenuator_ports[129],
        _attenuator_0.attenuator_ports[133],
        _attenuator_0.attenuator_ports[148],
        _attenuator_0.attenuator_ports[163],
        _attenuator_0.attenuator_ports[178],
        _attenuator_0.attenuator_ports[182],
    ],
)

_ssh_connection_details_0 = SshServiceDetails(
    addr="10.64.169.186", username="cranuser2112", password="systeM!23"
)
_k8s_connection_details_0 = K8SConnectionDetails(
    ip_addr="10.64.169.186", username="core", password="system123", port="22"
)

_master_node_0 = MasterNode(
    k8s_connection_details=_k8s_connection_details_0,
    ssh_connection_details=_ssh_connection_details_0,
)
_k8s_0 = K8S(namespace="cran2112", master_node=_master_node_0)

_cnf_du_0 = HelmChart(
    name="vdu2112",
    yaml_file=os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/cnf.yaml"),
)
_cluster_preparation_du_0 = HelmChart(
    name=_cnf_du_0.name + "-cluster-preparation",
    yaml_file=os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/preparation.yaml"),
)

_prerequisite_du_0 = HelmChart(
    name=_cnf_du_0.name + "-prerequisite",
    yaml_file=os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/prerequisite.yaml"),
)

_vdu_k8s_cloud_deployment_0 = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    cloud_hosting=_k8s_0,
    cluster_preparation=_cluster_preparation_du_0,
    prerequisite=_prerequisite_du_0,
    cnf=_cnf_du_0,
)

_du_0 = VDU(
    cloud_deployment=_vdu_k8s_cloud_deployment_0,
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.64.169.210", username="Nemuadmin", password="nemuuser", port="443"
    ),
    rus=[_ru_0, _ru_1, _ru_2, _ru_3, _ru_4],
    fhgws=[],
    instance_id=37180,
    global_bts_id=37180,
)

# BTS
_cbts_0 = CloudBts(
    dus=[_du_0],
    cu=_cu_0,
    cloud_deployment=_vcu_k8s_cloud_deployment_0,
)

#   10.70.222.54
_appserver_ssh = SshServiceDetails(
    addr="10.71.207.154", username="vrf3_sg1", password="vrf3@sg1", port="41624"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.207.154",
    iperf_path="/usr/bin/iperf",
    port="41625",
)
_appserver = AppServer(_iperf)

# UE Info
# replace to x70
_android_0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.217.2", username="mn5gran", password="nokia123@"
    ),
    serial_number="39a6a17f",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python38/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="/cygdrive/c/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "sdx80", "qct_dx50"],
)


# RealCore
_amf_ssh = SshServiceDetails(
    addr="to_be_updated", username="to_be_updated", password="to_be_updated"
)

_amf_n2_addr = NetworkAddress(v4="10.110.66.198", v6="to_be_updated", vlan_id=None)

_amf = AMF(oam_ssh_connection_details=_amf_ssh, n2=_amf_n2_addr)

_core = RealCore(five_g=RealCore5GDetails(amf=_amf), mcc="262", mnc="03")


# TestLine
tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts_0],
    core=_core,
    ues=[
        _android_0
    ],
    tl_cloud_topology="CLOUD_5G_AIC_RM17_OCP_AZQJ",
    # enbs=[_lte_real_enb_0],
    attenuator=[_attenuator_0],
    appserver=_appserver,
)
