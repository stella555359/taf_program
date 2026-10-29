__maintainer__ = "Li Zhiguo"
__team__ = "NSB MN RAN RD VRF HAZ3 7"
__email__ = "zhiguo.li@nokia-sbell.com"

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
from taf.config.testline.attenuator import (
    AttenuationPort,
    # TopYoung,
    JFW,
    HBTE,
    Hytem,
    RadioRack,
)
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    BmcConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.ue import (
    AirphoneCloud,
    Airphone,
    Prisma,
    TM500,
    Qualcomm,
    QualcommUeType,
    Android,
    MediaTek,
    TafUeFastmile,
)
from taf.config.testline import NetworkAddress, RoutingInformation
from taf.config.testline import RealEnb, Airscale, CommonUnit
# from taf.config.testline import HBTE_PDU as HBTE
from taf.config.testline.pdu import HBTE as pdu_HBTE
from taf.config.testline.pdu import FPFH
from taf.config.testline import RU, RadioTypes
from taf.config.testline import CloudBts, CU
from taf.config.testline import VDU, FHGW, RANNIC
from taf.config.testline import PxeServer
from taf.config.testline import TestLine
from taf.config.testline import TestPc
from taf.config.testline.taf_ue_data_transfer_protocol import TafUeDataTransferProtocol
from taf.config.testline.appserver import TafUeAppServer, AppServer
from taf.config.testline.lmi import LMI, Local
from taf.config.testline import LicenseKeeper

# common
__all__ = ["tl"]
_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# Testpc
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.159.110", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
# UTF
_utf_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.171.40", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# CU
_cu = CU(
    instance_id=37730,
    global_bts_id=37730,
    backhaul_site_oam_ip=NetworkAddress(v4="10.57.191.151"),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.191.2", username="core", password="system123"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.191.151", username="Nemuadmin", password="Nokia@123", port=443
    ),
    f1c=NetworkAddress(
        v4="10.57.192.42",
        vlan_id=109,
        routing=RoutingInformation(gateway="10.57.192.1/26"),
    ),
    f1u=NetworkAddress(
        v4="10.57.192.52",
        vlan_id=109,
        routing=RoutingInformation(gateway="10.57.192.1/26"),
    ),
    ngc=NetworkAddress(
        v4="10.57.192.170",
        vlan_id=111,
        routing=RoutingInformation(gateway="10.57.192.129/26"),
    ),
    ngu=NetworkAddress(
        v4="10.57.192.180",
        vlan_id=111,
        routing=RoutingInformation(gateway="10.57.192.129/26"),
    ),
    x2c=NetworkAddress(
        v4="10.57.192.106",
        vlan_id=110,
        routing_v4=RoutingInformation(gateway="10.57.192.65/26"),
    ),
    x2u=NetworkAddress(
        v4="10.57.192.116",
        vlan_id=110,
        routing_v4=RoutingInformation(gateway="10.57.192.65/26"),
    ),
    xnc=NetworkAddress(
        v4="10.57.192.234",
        vlan_id=112,
        routing_v4=RoutingInformation(gateway="10.57.192.193/26"),
    ),
    xnu=NetworkAddress(
        v4="10.57.192.244",
        vlan_id=112,
        routing_v4=RoutingInformation(gateway="10.57.192.193/26"),
    ),
    s1u=NetworkAddress(
        v4="10.57.191.60",
        vlan_id=102,
        routing_v4=RoutingInformation(gateway="10.57.191.33/27"),
    ),
)

# ssh connection information of OE, for tenant user
_vcu_ssh_connection_details = SshServiceDetails(
    addr="10.57.191.2", username="cranuser2408", password="systeM!23", port=22
)

# ssh connection information of OE, for root user
_vcu_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.57.191.2", username="core", password="system123", port=22
)

_vcu_master_node = MasterNode(
    k8s_connection_details=_vcu_k8s_connection_details,
    ssh_connection_details=_vcu_ssh_connection_details,
)

_vcu_k8s = K8S(namespace="cran2408", master_node=_vcu_master_node)

_cnf_cu_1 = HelmChart(
    name="vcu2408",
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
    cloud_hosting=_vcu_k8s,
    cluster_preparation=_cluster_preparation_cu_1,
    prerequisite=_prerequisite_cu_1,
    cnf=_cnf_cu_1,
)

# Attenuator
_attenuator0 = HBTE(
    ip_addr="10.64.56.27",
    port=5000,
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32],
    model="PA-32-32-6-127-0.5",
)

# PB
_pdu_0 = FPFH(addr="10.64.49.66", port_numbers=[1, 2, 3, 4, 5, 6])

_pdu_1 = FPFH(addr="10.64.49.68", port_numbers=[1, 2, 3, 4, 5, 6])

# LMI
_ru_lmi_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.64.57.28", username="mn5gran", password="nokia123@"
    )
)

_ru_lmi_pc2 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.64.57.36", username="mn5gran", password="nokia123@"
    )
)

_ru_lmi_0 = LMI(product_code="",
              host=_ru_lmi_pc,
              uart_mapping=[Local(port="COM10")])

_ru_lmi_1 = LMI(product_code="",
              host=_ru_lmi_pc,
              uart_mapping=[Local(port="COM11")])

_ru_lmi_2 = LMI(product_code="",
              host=_ru_lmi_pc,
              uart_mapping=[Local(port="COM16")])

_ru_lmi_3 = LMI(product_code="",
              host=_ru_lmi_pc2,
              uart_mapping=[Local(port="COM21")])

# 5G RU
_ru_0 = RU(
    ru_hw_group="AHLOA",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.34", username="root", password=""
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_pdu_0.pdu_ports[3],
    radio_type=RadioTypes.AHLOA.value,
    serial_number="BL2003G10Y5",
    attenuation_ports=[
        _attenuator0.attenuator_ports[17],
        _attenuator0.attenuator_ports[18],
        _attenuator0.attenuator_ports[19],
        _attenuator0.attenuator_ports[20],
    ],
    lmi=_ru_lmi_0
)

_ru_1 = RU(
    ru_hw_group="AZQS",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.35", username="serviceuser", password="wcdjLlTpqEY3cAmOe11u6aELwGI3rDvpGJQvCkcyHZc="
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_pdu_0.pdu_ports[1],
    radio_type=RadioTypes.AZQS.value,
    serial_number="1M223737750",
    attenuation_ports=[
        _attenuator0.attenuator_ports[9],
        _attenuator0.attenuator_ports[10],
        _attenuator0.attenuator_ports[11],
        _attenuator0.attenuator_ports[12],
    ],
    lmi=_ru_lmi_1
)

_ru_2 = RU(
    ru_hw_group="AZQO",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.36", username="serviceuser", password="wcdjLlTpqEY3cAmOe11u6aELwGI3rDvpGJQvCkcyHZc="
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_pdu_0.pdu_ports[2],
    radio_type=RadioTypes.AZQO.value,
    serial_number="1M202116551",
    attenuation_ports=[
        _attenuator0.attenuator_ports[1],
        _attenuator0.attenuator_ports[2],
        _attenuator0.attenuator_ports[5],
        _attenuator0.attenuator_ports[6],
        _attenuator0.attenuator_ports[3],
        _attenuator0.attenuator_ports[4],
        _attenuator0.attenuator_ports[7],
        _attenuator0.attenuator_ports[8],
    ],
    lmi=_ru_lmi_2
)

_ru_3 = RU(
    ru_hw_group="AVQC",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.37", username="serviceuser", password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og="
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_pdu_1.pdu_ports[4],
    radio_type=RadioTypes.AVQC.value,
    serial_number="1M234304784",
    attenuation_ports=[
        _attenuator0.attenuator_ports[13],
        _attenuator0.attenuator_ports[14],
        _attenuator0.attenuator_ports[15],
        _attenuator0.attenuator_ports[16],
    ],
    lmi=_ru_lmi_3
)

_ru_4 = RU(
    ru_hw_group="AHFII",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.38", username="serviceuser", password="WAH26M0DHuXSxpqpUSLmklXrKUfF4iPrXQ+8YULFNuM="
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_pdu_0.pdu_ports[5],
    radio_type=RadioTypes.AHFII.value,
    serial_number="BL2341N4ANV",
    attenuation_ports=[
        _attenuator0.attenuator_ports[21],
        _attenuator0.attenuator_ports[22],
        _attenuator0.attenuator_ports[23],
        _attenuator0.attenuator_ports[24],
    ],
)

# vDU
_pxe_server_ssh_info = SshServiceDetails(
    addr="10.64.161.14", username="ute", password="!Q2w3e4r5t6y7u"
)
_pxe_server = PxeServer(
    nfs_ip="10.64.161.14", ssh_connection_details=_pxe_server_ssh_info
)

# FHGW information,need update
# _fhgw_0 = FHGW(user_config_path=_cfg_dir, rus=[_ru], pxe_server=_pxe_server)
# _fhgw_0.ip = "x.x.x.x"
# _fhgw_0.username = "toor4nsn"
# _fhgw_0.password = "Fhgw@nokia123"
# _fhgw_0.version = "FHGW24R2"

# RANNIC information
_rannic_0 = RANNIC(serial_number="L1241303881", product_code="AF1791.101", rus=[_ru_0, _ru_1, _ru_2])
_rannic_1 = RANNIC(serial_number="L1241205628", product_code="AF1791.101", rus=[_ru_4])
_rannic_2 = RANNIC(serial_number="L1243107679", product_code="AF1791.102", rus=[_ru_3])

# ssh connection information of OE, for tenant user
_ssh_connection_details_0 = SshServiceDetails(
    addr="10.64.52.106", username="cranuser2408", password="systeM!23"
)
_ssh_connection_details_1 = SshServiceDetails(
    addr="10.64.52.154", username="cranuser2408", password="systeM!23"
)

# ssh connection information of OE, for root user
_k8s_connection_details_0 = K8SConnectionDetails(
    ip_addr="10.64.52.106", username="core", password="system123", port="22"
)
_k8s_connection_details_1 = K8SConnectionDetails(
    ip_addr="10.64.52.154", username="core", password="system123", port="22"
)

_master_node_0 = MasterNode(
    k8s_connection_details=_k8s_connection_details_0,
    ssh_connection_details=_ssh_connection_details_0,
)
_master_node_1 = MasterNode(
    k8s_connection_details=_k8s_connection_details_1,
    ssh_connection_details=_ssh_connection_details_1,
)

_k8s_0 = K8S(namespace="cran2408", master_node=_master_node_0)
_k8s_1 = K8S(namespace="cran2408", master_node=_master_node_1)

_vdu_cnf_0 = DeploymentVnfStack(
    name="vdu2408",
    yaml_file=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/du_cnf_values-override.yaml"
    ),
)
_vdu_cnf_1 = DeploymentVnfStack(
    name="vdu2408",
    yaml_file=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/vDU_1/du_cnf_values-override.yaml"
    ),
)

_vdu_intnet_0 = DeploymentNetworkStack(
    name=_vdu_cnf_0.name + "-prerequisite",
    yaml_file=os.path.join(_cfg_dir, "DEP/gnbs_0/vDU_0/DU_pvc_values-override.yaml"),
)
_vdu_intnet_1 = DeploymentNetworkStack(
    name=_vdu_cnf_1.name + "-prerequisite",
    yaml_file=os.path.join(_cfg_dir, "DEP/gnbs_0/vDU_1/DU_pvc_values-override.yaml"),
)

_cnf_du_0 = HelmChart(
    name="vdu24081",
    yaml_file=os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/cnf.yaml"),
)
_cnf_du_1 = HelmChart(
    name="vdu24082",
    yaml_file=os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/vDU_1/cnf.yaml"),
)

_cluster_preparation_du_0 = HelmChart(
    name=_cnf_du_0.name + "-cluster-preparation",
    yaml_file=os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/preparation.yaml"),
)
_cluster_preparation_du_1 = HelmChart(
    name=_cnf_du_1.name + "-cluster-preparation",
    yaml_file=os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/vDU_1/preparation.yaml"),
)

_prerequisite_du_0 = HelmChart(
    name=_cnf_du_0.name + "-prerequisite",
    yaml_file=os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/prerequisite.yaml"),
)
_prerequisite_du_1 = HelmChart(
    name=_cnf_du_1.name + "-prerequisite",
    yaml_file=os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/vDU_1/prerequisite.yaml"),
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
_vdu_k8s_cloud_deployment_1 = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    cloud_hosting=_k8s_1,
    networks=[_vdu_intnet_1],
    vnfs=[_vdu_cnf_1],
    cluster_preparation=_cluster_preparation_du_1,
    prerequisite=_prerequisite_du_1,
    cnf=_cnf_du_1,
)

_du_0 = VDU(
    cloud_deployment=_vdu_k8s_cloud_deployment_0,
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.64.52.130", username="Nemuadmin", password="Nokia@123", port="443"
    ),
    rannics=[_rannic_0, _rannic_1],
    instance_id=37730,
    global_bts_id=37730,
)
_du_1 = VDU(
    cloud_deployment=_vdu_k8s_cloud_deployment_1,
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.64.52.162", username="Nemuadmin", password="Nokia@123", port="443"
    ),
    rannics=[_rannic_2],
    instance_id=37730,
    global_bts_id=37730,
)

# BTS
_cbts = CloudBts(
    dus=[_du_0, _du_1],
    cu=_cu,
    cloud_deployment=_vcu_k8s_cloud_deployment,
)

# CI_Detail_UE_Type='Nokia FastMile 5G Gateway 3.1'
_fastmile_appserver_1 = TafUeAppServer(
    app_server_name="APP_SERVER_1",
    address="10.57.162.5",
    user="vrf3_sg8",
    password="vrf3@8",
    bind_interface_ip="10.57.162.5",
    expected_prompt="\[ute.*\$ ",
    binary_path="/home/vrf3_sg8/taf_debug/iperf",
    ports=[58000, 58999],
)

_fastmile_data_transfer_1 = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_fastmile_appserver_1,
    interval=1,
    binary_path="iperf",
    version=2,
)

_fastmile_1 = TafUeFastmile(
    ue_pc_address="10.64.57.51",
    root_password="Nokia123!",
    ue_manage_ip="10.71.212.221",
    serial_number="LPL2214005D4",
    version="3.2",
    data_transfer=[_fastmile_data_transfer_1],
    proxy_mngr_port=9955,
    ueproxy_force_release=True,
    capabilities=["REAL_FASTMILE_UE1", "nokia_fastmile"],
)

# UE
_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.179.233", username="vrf3_sg7", password="Haz4_vrf_sg3"
    ),
    network_interface_address="10.57.179.233",
    iperf_path="iperf",
    port="58000",
)

_appserver = AppServer(_iperf_details_on_appserver)

_licensekeeper = LicenseKeeper(username="huabao.jiang@nokia-sbell.com", password="nokia123")

_sigspark_0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.64.57.36", username="mn5gran", password="nokia123@"
    ),
    serial_number="921aba5a",
    server_dir="C:/Spark1.1.2012.3/Bin/Spark.exe",
    python_path="C:/Python39",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033100015425",
    licensekeeper=_licensekeeper,
    capabilities=["huawei_sigspark"],
)

_sigspark_1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.64.57.36", username="mn5gran", password="nokia123@"
    ),
    serial_number="921abaad",
    server_dir="C:/Spark1.1.2012.3/Bin/Spark.exe",
    python_path="C:/Python39",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033100015426",
    licensekeeper=_licensekeeper,
    capabilities=["huawei_sigspark"],
)

# TestLine
tl = TestLine(
    test_pc=_test_pc,
    test_pcs=[_test_pc, _utf_pc],
    gnbs=[_cbts],
    ues=[_sigspark_0, _sigspark_1],  # _fastmile_1
    tl_cloud_topology="CLOUD_5G_AIC_RM17_OCP_DC_FDD_TDD",
    appserver=_appserver,
    attenuators=[_attenuator0],
    # enbs=[_lte_real_enb],
)
