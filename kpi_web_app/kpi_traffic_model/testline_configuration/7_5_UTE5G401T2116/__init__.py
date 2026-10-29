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

from taf.config.testline.pdu import HBTE, PduPort, Pdu, EPC, ATEN, RRB, APC, Gude
from taf.config.testline.core import RealCore, RealCore5GDetails, AMF
from taf.config.testline import NetworkAddress, RoutingInformation
from taf.config.testline import RealEnb, Airscale, CommonUnit
from taf.config.testline import RU, RadioTypes
from taf.config.testline import CloudBts, CU
from taf.config.testline import VDU, FHGW
from taf.config.testline import PxeServer
from taf.config.testline import TestLine
from taf.config.testline import TestPc
from taf.config.testline.ue import Android
from taf.config.testline.appserver import AppServer
from taf.config.testline.attenuator import HBTE as ATTEN_HBTE


__maintainer__ = "Lingxue Cui"
__team__ = "I_NSB_MN_RAN_RD_VRF_HAZ3_01@internal.nsn.com"
__email__ = "lingxue.cui@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))


# Testpc --confirm
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.179", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# CU
_cu_0 = CU(
    instance_id=37241,
    global_bts_id=37241,
    # CU OAM IP
    backhaul_site_oam_ip=NetworkAddress(v4="10.57.209.132"),
    # CU OCP ssh IP
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.209.2", username="cranuser2116", password="systeM!23"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.209.132", username="Nemuadmin", password="nemuuser", port=443
    ),
    x2c=NetworkAddress(
        v4="10.57.210.68",
        vlan_id=110,
        routing=RoutingInformation(gateway="10.57.182.65", ip_prefix_length=26),
    ),
    x2u=NetworkAddress(
        v4="10.57.210.69",
        vlan_id=110,
        routing=RoutingInformation(gateway="10.57.182.65", ip_prefix_length=26),
    ),
    f1c=NetworkAddress(
        v4="10.57.210.4",
        vlan_id=109,
        routing=RoutingInformation(gateway="10.57.182.1", ip_prefix_length=26),
    ),
    f1u=NetworkAddress(
        v4="10.57.210.5",
        vlan_id=109,
        routing=RoutingInformation(gateway="10.57.182.1", ip_prefix_length=26),
    ),
    s1u=NetworkAddress(
        v4="10.57.209.36",
        vlan_id=102,
        routing=RoutingInformation(gateway="10.57.181.33", ip_prefix_length=27),
    ),
    tracing=None,
)

# cloud_deployment for vCU0
_vcu_cnf_0 = DeploymentVnfStack(
    name="vcu2116",
    yaml_file=os.path.join(_cfg_dir, "DEP/gnbs_0/vCU/CU_cnf_values-override.yaml"),
)
_vcu_intnet_0 = DeploymentNetworkStack(
    name=_vcu_cnf_0.name + "-prerequisite",
    yaml_file=os.path.join(_cfg_dir, "DEP/gnbs_0/vCU/CU_pvc_values-override.yaml"),
)

# ssh connection information of OE, for tenant user, tester used
_vcu_ssh_connection_details_0 = SshServiceDetails(
    addr="10.57.209.2", username="cranuser2116", password="systeM!23", port=22
)
# ssh connection information of OE, for root user
_vcu_k8s_connection_details_0 = K8SConnectionDetails(
    ip_addr="10.57.209.2", username="core", password="system123", port=22
)

_vcu_master_node_0 = MasterNode(
    k8s_connection_details=_vcu_k8s_connection_details_0,
    ssh_connection_details=_vcu_ssh_connection_details_0,
)

_vcu_k8s_0 = K8S(namespace="cran2116", master_node=_vcu_master_node_0)

_cnf_cu_0 = HelmChart(
    name="vcutest",
    yaml_file=os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/cnf.yaml"),
)

_cluster_preparation_cu_0 = HelmChart(
    name=_cnf_cu_0.name  + "-cluster-preparation",
    yaml_file=os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/preparation.yaml"),
)

_prerequisite_cu_0 = HelmChart(
    name=_cnf_cu_0.name + "-prerequisite",
    yaml_file=os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/prerequisite.yaml"),
)

_vcu_k8s_cloud_deployment_0 = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    networks=[_vcu_intnet_0],
    vnfs=[_vcu_cnf_0],
    cloud_hosting=_vcu_k8s_0,
    cluster_preparation=_cluster_preparation_cu_0,
    prerequisite=_prerequisite_cu_0,
    cnf=_cnf_cu_0,
)

_attenuator_0 = ATTEN_HBTE(
    ip_addr="10.71.204.117",
    port=5000,
    model="PA-16-16-6-127-0.5-B-S",
    attenuation_port_numbers=[
        1,
        34,
        67,
        100,
        5,
        38,
        71,
        104,
        9,
        42,
        75,
        108,
        13,
        46,
        79,
        112,
        17,
        50,
        83,
        116,
        21,
        54,
        87,
        120,
        31,
        64,
        25,
        58,
        91,
        124
    ],
)

# RU info
_ru_pdu = HBTE(addr="10.71.195.231", port_numbers=[1, 2, 3, 4, 5, 8])

_ru_0 = RU(
    ru_hw_group="hw_group",
    pdu_port=_ru_pdu.pdu_ports[1],
    radio_type=RadioTypes.AWHQX,
    serial_number="EB2232R0705",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.40",
        username="rfsw",
        password="KRG3dFggxxHw+s0z64U0AR22VyjfnXdHrAVdSv5jpc4=",
    ),
    attenuation_ports=[
        _attenuator_0.attenuator_ports[1],
        _attenuator_0.attenuator_ports[34],
        _attenuator_0.attenuator_ports[67],
        _attenuator_0.attenuator_ports[100],
    ],
)

_ru_1 = RU(
    ru_hw_group="hw_group",
    pdu_port=_ru_pdu.pdu_ports[2],
    radio_type=RadioTypes.AWHQX,
    serial_number="EB2232R0701",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.41",
        username="rfsw",
        password="KRG3dFggxxHw+s0z64U0AR22VyjfnXdHrAVdSv5jpc4=",
    ),
    attenuation_ports=[
        _attenuator_0.attenuator_ports[5],
        _attenuator_0.attenuator_ports[38],
        _attenuator_0.attenuator_ports[71],
        _attenuator_0.attenuator_ports[104],
    ],
)

_ru_2 = RU(
    ru_hw_group="hw_group",
    pdu_port=_ru_pdu.pdu_ports[3],
    radio_type=RadioTypes.AWHQX,
    serial_number="EB2232R0698",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.42",
        username="rfsw",
        password="KRG3dFggxxHw+s0z64U0AR22VyjfnXdHrAVdSv5jpc4=",
    ),
    attenuation_ports=[
        _attenuator_0.attenuator_ports[9],
        _attenuator_0.attenuator_ports[42],
        _attenuator_0.attenuator_ports[75],
        _attenuator_0.attenuator_ports[108],
    ],
)

_ru_3 = RU(
    ru_hw_group="hw_group",
    pdu_port=_ru_pdu.pdu_ports[4],
    radio_type=RadioTypes.AWHQX,
    serial_number="EB2232R0677",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.43",
        username="rfsw",
        password="KRG3dFggxxHw+s0z64U0AR22VyjfnXdHrAVdSv5jpc4=",
    ),
    attenuation_ports=[
        _attenuator_0.attenuator_ports[13],
        _attenuator_0.attenuator_ports[46],
        _attenuator_0.attenuator_ports[79],
        _attenuator_0.attenuator_ports[112],
    ],
)

_ru_4 = RU(
    ru_hw_group="hw_group",
    pdu_port=_ru_pdu.pdu_ports[5],
    radio_type=RadioTypes.AWHQX,
    serial_number="EB2232R0678",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.44",
        username="rfsw",
        password="KRG3dFggxxHw+s0z64U0AR22VyjfnXdHrAVdSv5jpc4=",
    ),
    attenuation_ports=[
        _attenuator_0.attenuator_ports[17],
        _attenuator_0.attenuator_ports[50],
        _attenuator_0.attenuator_ports[83],
        _attenuator_0.attenuator_ports[116],
    ],
)

_ru_5 = RU(
    ru_hw_group="hw_group",
    pdu_port=_ru_pdu.pdu_ports[8],
    radio_type=RadioTypes.AWHQX,
    serial_number="EB2232R0680",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.45",
        username="rfsw",
        password="KRG3dFggxxHw+s0z64U0AR22VyjfnXdHrAVdSv5jpc4=",
    ),
    attenuation_ports=[
        _attenuator_0.attenuator_ports[21],
        _attenuator_0.attenuator_ports[54],
        _attenuator_0.attenuator_ports[87],
        _attenuator_0.attenuator_ports[120],
    ],
)

_ru_6 = RU(
    ru_hw_group="hw_group",
    pdu_port=_ru_pdu.pdu_ports[8],
    radio_type=RadioTypes.AVQC,
    serial_number="1M244205935",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.46",
        username="rfsw",
        password="f6gh0K2nXq0O8XqVFkUuMtJnzuKm0U3box0QcYgugn0=",
    ),
    attenuation_ports=[
        _attenuator_0.attenuator_ports[25],
        _attenuator_0.attenuator_ports[58],
        _attenuator_0.attenuator_ports[91],
        _attenuator_0.attenuator_ports[124],
    ],
)

# vDU info
# vDU OCP IP
_ssh_connection_details_0 = SshServiceDetails(
    addr="10.64.173.170", username="cranuser2116", password="systeM!23"
)
_k8s_connection_details_0 = K8SConnectionDetails(
    ip_addr="10.64.173.170", username="core", password="system123", port="22"
)

_master_node_0 = MasterNode(
    k8s_connection_details=_k8s_connection_details_0,
    ssh_connection_details=_ssh_connection_details_0,
)
_k8s_0 = K8S(namespace="cran2116", master_node=_master_node_0)
_vdu_cnf_0 = DeploymentVnfStack(
    name="vdu2116",
    yaml_file=os.path.join(_cfg_dir, "DEP/gnbs_0/vDU_0/DU_cnf_values-override.yaml"),
)
_vdu_intnet_0 = DeploymentNetworkStack(
    name=_vdu_cnf_0.name + "-prerequisite",
    yaml_file=os.path.join(_cfg_dir, "DEP/gnbs_0/vDU_0/DU_pvc_values-override.yaml"),
)

_cnf_du_0 = HelmChart(
    name="vdu2116", # same with chart_name in kuafu config.ini
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
    networks=[_vdu_intnet_0],
    vnfs=[_vdu_cnf_0],
    cluster_preparation=_cluster_preparation_du_0,
    prerequisite=_prerequisite_du_0,
    cnf=_cnf_du_0,
)

_du_0 = VDU(
    cloud_deployment=_vdu_k8s_cloud_deployment_0,
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.64.173.194", username="Nemuadmin", password="nemuuser", port="443"
    ),
    rus=[_ru_0, _ru_1, _ru_2, _ru_3, _ru_4, _ru_5, _ru_6],
    instance_id=37241,
    global_bts_id=37241,
)

# BTS
_cbts_0 = CloudBts(
    dus=[_du_0],
    cu=_cu_0,
    cloud_deployment=_vcu_k8s_cloud_deployment_0,
)

_appserver_ssh = SshServiceDetails(
    addr="10.57.191.194", username="vrf3_sg1", password="vrf3@sg1", port="41632"
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.194",
    iperf_path="/usr/bin/iperf",
    port="41633",
)
_appserver = AppServer(_iperf)

# RealEnb---------------------------------------------------------
_real_enb_pdu = HBTE(addr="10.71.195.228", port_numbers=[2])
_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.71.210.230", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[2],
)
_real_enb = Airscale(common_units=[_common_unit_2])
_lte_ru_0 = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=None,
    radio_type=RadioTypes.FXEB,
    serial_number="NK164601292",
    attenuation_ports=[
        _attenuator_0.attenuator_ports[31],
        _attenuator_0.attenuator_ports[64],
    ],
)
_lte_real_enb = RealEnb(
    airscale=_real_enb, rms=[_lte_ru_0], instance_id=45, global_bts_id=45
)

# UE Info
_android_0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.0.176.129", username="mn5gran", password="nokia123@"
    ),
    serial_number="291b5963",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Users/mn5gran/AppData/Local/Programs/Python/Python39/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="/cygdrive/c/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "sdx65", "qct_dx50"],
)

# RealCore
_amf_ssh = SshServiceDetails(
    addr="to_be_updated", username="to_be_updated", password="to_be_updated"
)

_amf_n2_addr = NetworkAddress(v4="10.110.133.68", v6="to_be_updated", vlan_id=None)

_amf = AMF(oam_ssh_connection_details=_amf_ssh, n2=_amf_n2_addr)

_core = RealCore(five_g=RealCore5GDetails(amf=_amf), mcc="262", mnc="03")


# TestLine
tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts_0],
    enbs=[_lte_real_enb],
    core=_core,
    ues=[_android_0],
    tl_cloud_topology="CLOUD_5G_AIC_RM17_OCP_AZQJ",
    attenuator=[_attenuator_0],
    appserver=_appserver,
)
