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

_licensekeeper = LicenseKeeper(username="HAZ3_SG4", password="HAZ3_SG4")


__maintainer__ = "changsheng chen"
__team__ = (
    "I_NSB_MN_RAN_RD_VRF_HAZ3_04_GMS <I_NSB_MN_RAN_RD_VRF_HAZ3_04@internal.nsn.com>"
)
__email__ = "changsheng.chen@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))


# Testpc --confirm
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.29", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# CU

# CU0
_cu_0 = CU(
    instance_id=37519,
    global_bts_id=37519,
    backhaul_site_oam_ip=NetworkAddress(v4="10.57.179.11"),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.138.34", username="tl37519", password="systeM!23"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.179.11", username="Nemuadmin", password="Nokia@123", port=443
    ),
    x2c=NetworkAddress(
        v4="10.57.180.82",
        vlan_id=2670,
        routing=RoutingInformation(gateway="10.57.180.65", ip_prefix_length=26),
    ),
    x2u=NetworkAddress(
        v4="10.57.180.83",
        vlan_id=2670,
        routing=RoutingInformation(gateway="10.57.180.65", ip_prefix_length=26),
    ),
    f1c=NetworkAddress(
        v4="10.57.180.18",
        vlan_id=2669,
        routing=RoutingInformation(gateway="10.57.180.1", ip_prefix_length=26),
    ),
    f1u=NetworkAddress(
        v4="10.57.180.19",
        vlan_id=2669,
        routing=RoutingInformation(gateway="10.57.180.1", ip_prefix_length=26),
    ),
    s1u=NetworkAddress(
        v4="10.57.179.43",
        vlan_id=2662,
        routing=RoutingInformation(gateway="10.57.179.33", ip_prefix_length=27),
    ),
    tracing=None,
)

# cloud_deployment for vCU0
_vcu_cnf_0 = DeploymentVnfStack(
    name="vcu722",
    yaml_file=os.path.join(_cfg_dir, "DEP/gnbs_0/vCU/CU_cnf_values-override.yaml"),
)
_vcu_intnet_0 = DeploymentNetworkStack(
    name=_vcu_cnf_0.name + "-prerequisite",
    yaml_file=os.path.join(_cfg_dir, "DEP/gnbs_0/vCU/CU_pvc_values-override.yaml"),
)

# ssh connection information of OE, for tenant user, tester used
_vcu_ssh_connection_details_0 = SshServiceDetails(
    addr="10.57.179.11", username="tl37519", password="systeM!23", port=22
)
# ssh connection information of OE, for root user
_vcu_k8s_connection_details_0 = K8SConnectionDetails(
    ip_addr="10.57.179.11", username="core", password="system123", port=22
)

_vcu_master_node_0 = MasterNode(
    k8s_connection_details=_vcu_k8s_connection_details_0,
    ssh_connection_details=_vcu_ssh_connection_details_0,
)

_vcu_k8s_0 = K8S(namespace="tl37519", master_node=_vcu_master_node_0)

_vcu_k8s_cloud_deployment_0 = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    networks=[_vcu_intnet_0],
    vnfs=[_vcu_cnf_0],
    cloud_hosting=_vcu_k8s_0,
)

# no check
_attenuator = HBTE(
    ip_addr="10.64.56.226",
    port="5000",
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    model="PA-16-16-6-127-0.5-B-S",
)

_ru_pdu_0 = hbte(addr="10.64.49.14", port_numbers=[1, 2, 4, 5])
_ru_pdu_1 = hbte(addr="10.71.195.132", port_numbers=[6])
# ru account need to be changed
_ru_1 = RU(
    ru_hw_group="hw_group",
    pdu_port=_ru_pdu_0.pdu_ports[1],
    # radio_type=RadioTypes.AHFIB,
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.35",
        username="rfsw",
        password="5rfS2qmWC0AiFYvir7k8JekCN8/NklqDK5E6OWXuUVQ=",
    ),
    attenuation_ports=[
        _attenuator.attenuator_ports[5],
    ],
)

_ru_2 = RU(
    ru_hw_group="hw_group",
    pdu_port=_ru_pdu_0.pdu_ports[4],
    # radio_type=RadioTypes.AHLOA,
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.35",
        username="rfsw",
        password="5rfS2qmWC0AiFYvir7k8JekCN8/NklqDK5E6OWXuUVQ=",
    ),
    attenuation_ports=[
        _attenuator.attenuator_ports[2],
    ],
)

_ru_3 = RU(
    ru_hw_group="hw_group",
    pdu_port=_ru_pdu_0.pdu_ports[5],
    # radio_type=RadioTypes.AEHC,
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.35",
        username="rfsw",
        password="5rfS2qmWC0AiFYvir7k8JekCN8/NklqDK5E6OWXuUVQ=",
    ),
    attenuation_ports=[
        _attenuator.attenuator_ports[3],
    ],
)

_ru_4 = RU(
    ru_hw_group="hw_group",
    pdu_port=_ru_pdu_1.pdu_ports[6],
    # radio_type=RadioTypes.AWHQX,
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.35",
        username="rfsw",
        password="5rfS2qmWC0AiFYvir7k8JekCN8/NklqDK5E6OWXuUVQ=",
    ),
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
    ],
)

_ssh_connection_details_0 = SshServiceDetails(
    addr="10.64.52.2", username="core", password="system123"
)
_k8s_connection_details_0 = K8SConnectionDetails(
    ip_addr="10.64.52.2", username="core", password="system123", port="22"
)

_master_node_0 = MasterNode(
    k8s_connection_details=_k8s_connection_details_0,
    ssh_connection_details=_ssh_connection_details_0,
)
_k8s_0 = K8S(namespace="tl37519", master_node=_master_node_0)
_vdu_cnf_0 = DeploymentVnfStack(
    name="vdu37519",
    yaml_file=os.path.join(_cfg_dir, "DEP/gnbs_0/vDU_0/DU_cnf_values-override.yaml"),
)
_vdu_intnet_0 = DeploymentNetworkStack(
    name=_vdu_cnf_0.name + "-prerequisite",
    yaml_file=os.path.join(_cfg_dir, "DEP/gnbs_0/vDU_0/DU_pvc_values-override.yaml"),
)

_vdu_k8s_cloud_deployment_0 = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    cloud_hosting=_k8s_0,
    networks=[_vdu_intnet_0],
    vnfs=[_vdu_cnf_0],
)

_du_0 = VDU(
    cloud_deployment=_vdu_k8s_cloud_deployment_0,
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.64.52.26", username="Nemuadmin", password="Nokia@123"
    ),
    # rus = [_ru_0, _ru_1, _ru_2, _ru_3, _ru_4],
    instance_id=37519,
    global_bts_id=37519,
)

# BTS
_cbts_0 = CloudBts(
    dus=[_du_0],
    cu=_cu_0,
    cloud_deployment=_vcu_k8s_cloud_deployment_0,
)

_appserver_ssh = SshServiceDetails(
    addr="10.71.219.24", username="mmw_sg4", password="mm@4", port="44321"
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.219.24",
    iperf_path="/usr/bin/iperf",
    port="44321",
    ports=[44321, 44322, 44323, 44324, 44325, 44326, 44327, 44328],
)
_appserver = AppServer(_iperf)

# UE Info
# old 75 2933e1ab  journey 75 bb9c8103
spark_UE_0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.218.12", username="nokia5g", password="noki@123"
    ),
    serial_number="921aba7f",
    server_dir="C:/Program Files (x86)/Spark1.1.2008.30/Bin/Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "sigspark_multiUE", "sigspark"],
    imsi="262030100010789",
    licensekeeper=_licensekeeper,
)

spark_UE_1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.64.57.9", username="nokia5g", password="noki@123"
    ),
    serial_number="921aba56",
    server_dir="C:/Program Files (x86)/Spark1.1.2008.30/Bin/Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "sigspark_multiUE", "sigspark"],
    imsi="262033100010067",
    licensekeeper=_licensekeeper,
)

spark_UE_2 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.217.115", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="921abab8",
    server_dir="C:/Program Files (x86)/Spark1.1.2008.30/Bin/Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "sigspark_multiUE", "sigspark"],
    imsi="262033032996900",
    licensekeeper=_licensekeeper,
)

spark_UE_3 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.217.115", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="921aba52",
    server_dir="C:/Program Files (x86)/Spark1.1.2008.30/Bin/Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "sigspark_multiUE", "sigspark"],
    imsi="262033100010083",
    licensekeeper=_licensekeeper,
)

# RealCore
# _amf_ssh = SshServiceDetails(
#     addr="to_be_updated", username="to_be_updated", password="to_be_updated"
# )
#
# _amf_n2_addr = NetworkAddress(v4="10.110.66.198", v6="to_be_updated", vlan_id=None)
#
# _amf = AMF(oam_ssh_connection_details=_amf_ssh, n2=_amf_n2_addr)
#
# _core = RealCore(five_g=RealCore5GDetails(amf=_amf), mcc="262", mnc="03")


# TestLine
tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts_0],
    # core=_core,
    ues=[spark_UE_0, spark_UE_1, spark_UE_2, spark_UE_3],
    attenuator=_attenuator,
    appserver=_appserver,
)
