__maintainer__ = "Chen Jian"
__team__ = "NSB MN RAN RD VRF HAZ3 5"
__email__ = "jian.1.chen@nokia-sbell.com"

import os
from taf.config.testline.cloud_hosting import (
    MasterNode,
    K8S,
    ComputeNode,
    CloudDeployment,
    HelmChart,
)

from taf.config.testline.connection_details import (
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    K8SConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)

from taf.config.testline.testpc import TestPc
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU
from taf.config.testline.gnb.du import VDU, RANNIC
from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.config.testline import Airphone
from taf.config.testline.ue import PreferredVlan

from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit, SlotId

from taf.config.testline.pdu import FPFH
from taf.config.testline.pdu import TopYoung
from taf.config.testline.radio import RU
from taf.config.testline.ue import Android
from taf.config.testline.radio import RadioTypes
from taf.config.testline import FHGW
from taf.config.testline import PxeServer
from taf.config.testline.dcap import DcapBasic

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

__all__ = ["tl"]

_vdu0_k8s_ssh_connection_details = SshServiceDetails(
    addr="10.57.202.58", username="core", password="system123"
)

_vdu0_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.57.202.58", username="core", password="system123", port=22
)

_vdu0_master_node = MasterNode(
    k8s_connection_details=_vdu0_k8s_connection_details,
    ssh_connection_details=_vdu0_k8s_ssh_connection_details,
)

_vdu0_k8s = K8S(namespace="tl2043", master_node=_vdu0_master_node)
#
#
# _prerequisite_du_1 = HelmChart(
#     name="aic-vdu-prerequisite",
#     yaml_file=os.path.join(_cfg_dir, 'vdu-prerequisite-1.yaml'),
# )
#
# _prerequisite_du_2 = HelmChart(
#     name="aic-vdu-prerequisite",
#     yaml_file=os.path.join(_cfg_dir, 'vdu-prerequisite-2.yaml'),
# )
#
# _cnf_du_1 = HelmChart(
#     name="aic-vdu",
#     yaml_file=os.path.join(_cfg_dir, 'vdu-cnf-1.yaml'),
# )
#
# _cnf_du_2 = HelmChart(
#     name="aic-vdu",
#     yaml_file=os.path.join(_cfg_dir, 'vdu-cnf-2.yaml'),
# )

_k8s_cloud_deployment_0 = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    cloud_hosting=_vdu0_k8s,
    # prerequisite=_prerequisite_du_1,
    # cnf=_cnf_du_1,
)

_vdu0_oam_http_connection_details = HttpConnectionDetails(
    addr="10.57.202.194", port=443, username="Nemuadmin", password="Nokia@123"
)

_vdu_0_rannic1 = RANNIC(serial_number="L1243107653", product_code="AF1791.102")


_vdu_0 = VDU(
    cloud_deployment=_k8s_cloud_deployment_0,
    oam_http_connection_details=_vdu0_oam_http_connection_details,
    instance_id=1,
    fhuc_vlans=[301],
    rannics=[_vdu_0_rannic1],
)

_vdu1_k8s_ssh_connection_details = SshServiceDetails(
    addr="10.57.202.210", username="core", password="system123"
)

_vdu1_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.57.202.210", username="core", password="system123", port=22
)

_vdu1_master_node = MasterNode(
    k8s_connection_details=_vdu1_k8s_connection_details,
    ssh_connection_details=_vdu1_k8s_ssh_connection_details,
)

_vdu1_k8s = K8S(namespace="tl2043", master_node=_vdu1_master_node)
#
#
# _prerequisite_du_1 = HelmChart(
#     name="aic-vdu-prerequisite",
#     yaml_file=os.path.join(_cfg_dir, 'vdu-prerequisite-1.yaml'),
# )
#
# _prerequisite_du_2 = HelmChart(
#     name="aic-vdu-prerequisite",
#     yaml_file=os.path.join(_cfg_dir, 'vdu-prerequisite-2.yaml'),
# )
#
# _cnf_du_1 = HelmChart(
#     name="aic-vdu",
#     yaml_file=os.path.join(_cfg_dir, 'vdu-cnf-1.yaml'),
# )
#
# _cnf_du_2 = HelmChart(
#     name="aic-vdu",
#     yaml_file=os.path.join(_cfg_dir, 'vdu-cnf-2.yaml'),
# )

_k8s_cloud_deployment_1 = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    cloud_hosting=_vdu1_k8s,
    # prerequisite=_prerequisite_du_1,
    # cnf=_cnf_du_1,
)

_vdu1_oam_http_connection_details = HttpConnectionDetails(
    addr="10.57.202.242", port=443, username="Nemuadmin", password="Nokia@123"
)

_vdu_1_rannic1 = RANNIC(serial_number="L1243107654", product_code="AF1791.102")

_vdu_1 = VDU(
    cloud_deployment=_k8s_cloud_deployment_1,
    oam_http_connection_details=_vdu1_oam_http_connection_details,
    instance_id=1,
    fhuc_vlans=[301],
    rannics=[_vdu_1_rannic1],
)

_cu = CU(
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.158.149", username="Nemuadmin", password="Nokia@123"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.158.149", port=443, username="Nemuadmin", password="Nokia@123"
    ),
    backhaul_site_oam_ip="None",
)

_vcu_k8s_ssh_connection_details = SshServiceDetails(
    addr="10.57.158.2", username="cranuser2043", password="systeM!23"
)

_vcu_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.57.158.2", username="cranuser2043", password="systeM!23", port=22
)

_vcu_master_node = MasterNode(
    k8s_connection_details=_vcu_k8s_connection_details,
    ssh_connection_details=_vcu_k8s_ssh_connection_details,
)

_vcu_k8s = K8S(namespace="cran2043", master_node=_vcu_master_node)

# _prerequisite_cu = HelmChart(
#     name="aic-vcu-prerequisite",
#     yaml_file=os.path.join(_cfg_dir, 'vcu-prerequisite.yaml'),
# )
#
# _cnf_cu = HelmChart(
#     name="aic-vcu",
#     yaml_file=os.path.join(_cfg_dir, 'vcu-cnf.yaml'),
# )
_vcu_k8s_cloud_deployment_1 = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    cloud_hosting=_vcu_k8s,
    # prerequisite=_prerequisite_cu,
    # cnf=_cnf_cu,
)

_dcap = DcapBasic(
    connection_details=HttpConnectionDetails(
        addr="10.101.60.55", port=443, username="utfuser", password="utfadmin!"
    )
)

_cbts = CloudBts(
    dus=[_vdu_0, _vdu_1],
    cu=_cu,
    cloud_deployment=_vcu_k8s_cloud_deployment_1,
    dcap=_dcap,
)

_vlan1 = PreferredVlan(slot_id=SlotId.B1, port_id=1, preferred_vlan_id=2914)

_vlan2 = PreferredVlan(slot_id=SlotId.B1, port_id=7, preferred_vlan_id=2915)

# SIGSPARK
_ue_host1_ssh = SshServiceDetails(
    addr="10.57.147.147", username="spark", password="spark"
)

_spark_appserver_ssh = SshServiceDetails(
    # addr="10.57.163.35",username="cmw_sg2",password="12345678"
    addr="10.57.162.19",
    username="vrf4_sg13",
    password="vrf4@13",
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_spark_appserver_ssh,
    network_interface_address="10.57.162.19",
    iperf_path="iperf",
    port="56578",
)

_sigspark1 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="36223656",
    server_dir="C:\Program Files (x86)\Spark1.1.2009.15\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033031397757",
    capabilities=["huawei_sigspark"],
)

_sigspark2 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="26901544",
    server_dir="C:\Program Files (x86)\Spark1.1.2009.15\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033031397661",
    capabilities=["huawei_sigspark"],
)

_sigspark3 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="40235955",
    server_dir="C:\Program Files (x86)\Spark1.1.2009.15\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033031397823",
    capabilities=["huawei_sigspark"],
)

_sigspark4 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="10835129",
    server_dir="C:\Program Files (x86)\Spark1.1.2009.15\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033031397826",
    capabilities=["huawei_sigspark"],
)

_sigspark5 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="13893854",
    server_dir="C:\Program Files (x86)\Spark1.1.2009.15\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033031397732",
    capabilities=["huawei_sigspark"],
)

_sigspark6 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="31851393",
    server_dir="C:\Program Files (x86)\Spark1.1.2009.15\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033031397852",
    capabilities=["huawei_sigspark"],
)

_sigspark7 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="14097099",
    server_dir="C:\Program Files (x86)\Spark1.1.2009.15\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033031397822",
    capabilities=["huawei_sigspark"],
)

_sigspark8 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="14220491",
    server_dir="C:\Program Files (x86)\Spark1.1.2009.15\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033030357429",
    capabilities=["huawei_sigspark"],
)

_ru_pdu = TopYoung(addr="10.57.247.218", port_numbers=[1])

_pdus = [_ru_pdu]

_ru = RU(
    ru_hw_group="hw_group",
    # default_ssh_connection_details=SshServiceDetails(
    # addr="172.22.0.154",
    # username="rfsw",
    # password="bdS%ztWG3v7%SjreCVA79wTPb"
    # ),
    pdu_port=_ru_pdu.pdu_ports[1],
    radio_type=RadioTypes.AEHC,
    # serial_number="L1211203222",
)
# vDU
_pxe_server_ssh_info = SshServiceDetails(
    addr="10.71.223.254", username="ute", password="!Q2w3e4r5t6y7u"
)

_pxe_server = PxeServer(
    nfs_ip="10.71.223.254", ssh_connection_details=_pxe_server_ssh_info
)
# FHGW information
_fhgw_0 = FHGW(user_config_path=_cfg_dir, rus=[_ru], pxe_server=_pxe_server)

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.195.104",
        username="ute",
        password="iW_K#8.ute%A10h0m0ra",
    ),
    connections=[_cbts],
)

tl = TestLine(
    test_pc=_test_pc,
    cloud_hostings=[_vcu_k8s, _vdu0_k8s, _vdu1_k8s],
    gnbs=[_cbts],
    # tl_cloud_topology="CLOUD_5GC_dRNIC_1vDU_TDD_AEHC_FDD_AHFIB",
    # ues=[
    #     _sigspark1,
    #     _sigspark2,
    #     _sigspark3,
    #     _sigspark4,
    #     _sigspark5,
    #     _sigspark6,
    #     _sigspark7,
    #     _sigspark8,
    # ],
    # pdus=_pdus,
)
