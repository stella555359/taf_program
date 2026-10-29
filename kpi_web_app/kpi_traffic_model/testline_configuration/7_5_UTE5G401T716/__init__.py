import os

from taf.config.testline import (
    CloudDeployment,
    DeploymentNetworkStack,
    DeploymentVnfStack,
    MasterNode,
    K8S,
    HelmChart,
    RANNIC,
)
from taf.config.testline import (
    SshServiceDetails,
    HttpConnectionDetails,
    K8SConnectionDetails,
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
    TopYoung,
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
from taf.config.testline.pdu import HBTE as hbte
from taf.config.testline.attenuator import HBTE
from taf.config.testline import LicenseKeeper
from taf.config.testline.airscale import CapacityUnit

from taf.config.testline.appserver import TafUeAppServer
from taf.config.testline import TafUeDataTransferProtocol
from taf.config.testline.pdn import PDNTafUeAndroidDetails

from taf.config.testline.ue import TafUeAndroid, MediaTek

_licensekeeper = LicenseKeeper(username="HAZ3_SG4", password="HAZ3_SG4")

__maintainer__ = "Pengliang Wu"
__team__ = (
    "I_NSB_MN_RAN_RD_VRF_HAZ3_04_GMS <I_NSB_MN_RAN_RD_VRF_HAZ3_04@internal.nsn.com>"
)
__email__ = "pengliang.wu@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))


# Testpc --confirm
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.203", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# CU

# CU0
_cu_0 = CU(
    instance_id=37441,
    global_bts_id=37441,
    backhaul_site_oam_ip=NetworkAddress(v4="10.57.165.9"),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.165.130", username="cranuser716", password="systeM!23"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.165.9", username="Nemuadmin", password="Nokia@123", port=443
    ),
    x2c=NetworkAddress(
        v4="10.57.166.78",
        vlan_id=2690,
        routing=RoutingInformation(gateway="10.57.166.65", ip_prefix_length=26),
    ),
    x2u=NetworkAddress(
        v4="10.57.166.79",
        vlan_id=2690,
        routing=RoutingInformation(gateway="10.57.166.65", ip_prefix_length=26),
    ),
    f1c=NetworkAddress(
        v4="10.57.166.14",
        vlan_id=2689,
        routing=RoutingInformation(gateway="10.57.166.1", ip_prefix_length=26),
    ),
    f1u=NetworkAddress(
        v4="10.57.166.15",
        vlan_id=2689,
        routing=RoutingInformation(gateway="10.57.166.1", ip_prefix_length=26),
    ),
    s1u=NetworkAddress(
        v4="10.57.165.41",
        vlan_id=2682,
        routing=RoutingInformation(gateway="10.57.165.33", ip_prefix_length=27),
    ),
    tracing=None,
)

# ssh connection information of OE, for tenant user, tester used
_vcu_ssh_connection_details_0 = SshServiceDetails(
    addr="10.57.165.130", username="cranuser716", password="systeM!23", port=22
)
# ssh connection information of OE, for root user
_vcu_k8s_connection_details_0 = K8SConnectionDetails(
    ip_addr="10.57.165.130", username="core", password="system123", port=22
)

_vcu_master_node_0 = MasterNode(
    k8s_connection_details=_vcu_k8s_connection_details_0,
    ssh_connection_details=_vcu_ssh_connection_details_0,
)

_vcu_k8s_0 = K8S(namespace="cran716", master_node=_vcu_master_node_0)

_cnf_cu_1 = HelmChart(
    name="vcu716",
    yaml_file=os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/cnf.yaml"),
)

_cluster_preparation_cu_1 = HelmChart(
    name=_cnf_cu_1.name + "-cluster-preparation",
    yaml_file=os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/preparation.yaml"),
)

_prerequisite_cu_1 = HelmChart(
    name=_cnf_cu_1.name + "-prerequisite",
    yaml_file=os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/prerequisite.yaml"),
)
_vcu_k8s_cloud_deployment = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    cloud_hosting=_vcu_k8s_0,
    cluster_preparation=_cluster_preparation_cu_1,
    prerequisite=_prerequisite_cu_1,
    cnf=_cnf_cu_1,
)


# no check
_attenuator = HBTE(
    ip_addr="10.71.203.196",
    port="5000",
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    model="PA-16-16-6-127-0.5-B-S",
)

_ru_pdu_0 = hbte(addr="10.71.195.132", port_numbers=[5])
_ru_pdu_1 = hbte(addr="10.71.195.130", port_numbers=[8])
_ru_pdu_2 = hbte(addr="10.71.195.131", port_numbers=[4])
# ru account need to be changed
_ru_1 = RU(
    ru_hw_group="AHFII",
    serial_number="K9244701858",
    pdu_port=_ru_pdu_0.pdu_ports[5],
    radio_type=RadioTypes.AHFII,
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1",
        username="root",
        password="root",
    ),
    lmp_connection=SshServiceDetails(
        addr="10.71.217.196", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[6],
        _attenuator.attenuator_ports[7],
        _attenuator.attenuator_ports[8],
        _attenuator.attenuator_ports[9],
        _attenuator.attenuator_ports[10],
        _attenuator.attenuator_ports[11],
        _attenuator.attenuator_ports[12],
        _attenuator.attenuator_ports[13],
        _attenuator.attenuator_ports[14],
        _attenuator.attenuator_ports[15],
        _attenuator.attenuator_ports[16],
    ],
)

_ru_2 = RU(
    ru_hw_group="AWHQN",
    serial_number="K9244701858",
    pdu_port=_ru_pdu_1.pdu_ports[8],
    radio_type=RadioTypes.AWHQN,
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1",
        username="rfsw",
        password="KRG3dFggxxHw+s0z64U0AR22VyjfnXdHrAVdSv5jpc4=",
    ),
    lmp_connection=SshServiceDetails(
        addr="10.71.217.196", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    attenuation_ports=[
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[6],
        _attenuator.attenuator_ports[7],
        _attenuator.attenuator_ports[8],
    ],
)

_ru_3 = RU(
    ru_hw_group="AWHQN",
    serial_number="K9244701858",
    pdu_port=_ru_pdu_2.pdu_ports[4],
    radio_type=RadioTypes.AWHQN,
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1",
        username="rfsw",
        password="KRG3dFggxxHw+s0z64U0AR22VyjfnXdHrAVdSv5jpc4=",
    ),
    lmp_connection=SshServiceDetails(
        addr="10.71.217.196", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
)

# RANNIC information
_rannic_0 = RANNIC(
    serial_number="L1241303089", product_code="AF1791.101", rus=[_ru_1, _ru_2, _ru_3]
)

# ssh connection information of OE, for tenant user
_ssh_connection_details_0 = SshServiceDetails(
    addr="10.0.178.42", username="cranuser716", password="systeM!23"
)
# ssh connection information of OE, for root user
_k8s_connection_details_0 = K8SConnectionDetails(
    ip_addr="10.0.178.42", username="core", password="system123", port="22"
)

_master_node_0 = MasterNode(
    k8s_connection_details=_k8s_connection_details_0,
    ssh_connection_details=_ssh_connection_details_0,
)
_k8s_0 = K8S(namespace="cran716", master_node=_master_node_0)
_vdu_cnf_0 = DeploymentVnfStack(
    name="vdu716",
    yaml_file=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/du_cnf_values-override.yaml"
    ),
)
_vdu_intnet_0 = DeploymentNetworkStack(
    name=_vdu_cnf_0.name + "-prerequisite",
    yaml_file=os.path.join(_cfg_dir, "DEP/gnbs_0/vDU_0/DU_pvc_values-override.yaml"),
)

_cnf_du_0 = HelmChart(
    name="vdu716",
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
        addr="10.0.178.66", username="Nemuadmin", password="Nokia@123", port=443
    ),
    rannics=[_rannic_0],
    fhgws=[],
    instance_id=37441,
    global_bts_id=37441,
)

# BTS
_cbts_0 = CloudBts(
    dus=[_du_0],
    cu=_cu_0,
    cloud_deployment=_vcu_k8s_cloud_deployment,
)

# AppServer info iperf used
_app_server_1 = TafUeAppServer(
    app_server_name="APP_1",
    address="10.71.207.148",
    user="vrf3_sg4",
    password="vrf3@sg4",
    ports=[44421, 44422, 44423, 44424],
    # bind_interface_ip='10.71.207.148',
    # expected_prompt='[vrf3_sg4@@appserver ~]$ ',
    # binary_path='/home/vrf3_sg4/taf_debug/iperf',
)

_data_transfer_iperf = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_app_server_1,
    interval=1,
    # binary_path='/data/data/com.nokia.android.application/',
    interface_name="rmnet_data0",
    server_close_delay=50,
    # binary_path='iperf',
    # version=2,)
)


_pdn1 = PDNTafUeAndroidDetails(
    entryName="dxdata1", apnName="dxdata1", apnType=["DEFAULT"]
)


_appserver_ssh = SshServiceDetails(
    addr="10.71.207.148", username="vrf3_sg4", password="vrf3@sg4", port="44421"
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.207.148",
    iperf_path="C:/Users/mn5gran/Desktop/Tool/iperf_tool_v3.10.3/iperf",
    port="44421",
    ports=[44421, 44422, 44423, 44424],
)

_iperf_details_on_mtk = IperfDataTransferDetails(
    ssh_connection_details=SshServiceDetails(
        addr="10.0.176.187", username="mn5gran", password="nokia123@"
    ),
    network_interface_address="",
    iperf_path="C:/Tool/iperf-2.0.9-win64/iperf",
    port="44252",
)

_appserver = AppServer(_iperf)

# UE Info
UE_0 = TafUeAndroid(
    serial_number="RFCR10K046N",
    capabilities=["REAL_UE", "samsung_ue"],
    ue_pc_address="10.0.176.187",
    data_transfer=[_data_transfer_iperf],
    ssh_connection_details=SshServiceDetails(
        addr="10.0.176.187", username="mn5gran", password="nokia123@"
    ),
    ue_pc_port="8080",
    pdns=[_pdn1],
)

# MTK_UE = MediaTek(
#     ssh_connection_details=SshServiceDetails(
#         addr="10.0.176.187", username="mn5gran", password="nokia123@"
#     ),
#     server_dir="c:/pyro_server",
#     server_port=8080,
#     edb_file_path=r"C:\Users\mn5gran\Desktop\Tool\MTK_M90\MDDB_MT6986D_S00_NR17_R2_MP_W25_02_P4.EDB",
#     # python_path='C:/Users/mn5gran/AppData/Local/Programs/Python/Python39/python.exe',
#     #log_filter="None",
#     imei="123123123123327",
#     imsi="262033100020882",
#     apn_url="dxdata1",
#     iperf_details=_iperf,
#     capabilities=["REAL_MEDIATEK_UE", "REAL_UE", "NSA"],
# )

MTK_UE = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.0.176.187", username="mn5gran", password="nokia123@"
    ),
    serial_number="0123456789ABCDEF",
    server_dir="C:/Program Files (x86)/Spark1.1.2008.30/Bin/Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "samsung"],
    imsi="262033100020882",
)

_eNB_capacity_unit = CapacityUnit(addr="192.168.253.36")
_real_enb_pdu = hbte(addr="10.57.241.158", port_numbers=[2])
_eNB_common_unit = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.71.209.220", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_real_enb_pdu.pdu_ports[2],
    capacity_units=[_eNB_capacity_unit],
)
_enb_airscale = Airscale(common_units=[_eNB_common_unit])
_enb = RealEnb(
    airscale=_enb_airscale,
    global_bts_id="11188",
    instance_id="11188",
    oam_ip=NetworkAddress(v4="10.71.209.220"),
    system_module=_enb_airscale,
)


# TestLine
tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts_0],
    enbs=[_enb],
    ues=[UE_0, MTK_UE],
    attenuator=_attenuator,
    appserver=_appserver,
)
