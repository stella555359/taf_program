__maintainer__ = "I_HAZ1_RRM7_CODER_TEAM@internal.nsn.com"
__team__ = "NSB MN SRAN PROD IWK HZ GMS "
__email__ = "I_HAZ1_RRM7_CODER_TEAM@internal.nsn.com"
__owner_email__ = "I_HAZ1_RRM7_CODER_TEAM@internal.nsn.com"

import os
import yaml
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
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU
from taf.config.testline.gnb.du import VDU, RANNIC
from taf.config.testline.gnb.networkaddress import NetworkAddress,RoutingInformation
from taf.config.testline import Airphone
from taf.config.testline.ue import PreferredVlan
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit, SlotId
from taf.config.testline.pdu import FPFH
from taf.config.testline.radio import RU
from taf.config.testline.attenuator import HBTE, TopYoung


_cfg_dir = os.path.dirname(os.path.abspath(__file__))


_pdu = FPFH(
    addr="10.108.190.166",
    port_numbers=[1, 2],
    login="admin",
    password="admin",
)

_pdus = [_pdu]
## for MRBTS-37256-TDD-DC
_vdu_k8s_ssh_connection_details = SshServiceDetails(
    addr="10.68.164.82", username="core", password="system123"
)

_vdu_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.68.164.82", username="core", password="system123", port=22
)

_vdu_master_node = MasterNode(
    k8s_connection_details=_vdu_k8s_connection_details,
    ssh_connection_details=_vdu_k8s_ssh_connection_details,
)
_vdu_k8s = K8S(namespace="cran6", master_node=_vdu_master_node)

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

_vdu_k8s_cloud_deployment = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    cloud_hosting=_vdu_k8s,
    cluster_preparation=_cluster_preparation_du,
    prerequisite=_prerequisite_du,
    cnf=_cnf_du,
)

_vdu_oam_http_connection_details = HttpConnectionDetails(
    addr="10.68.164.114", port=443, username="Nemuadmin", password="Nokia@123"
)
_attenuator = TopYoung(
    ip_addr="10.97.65.75",
    port=3000,
    attenuation_port_numbers=[i for i in range(1, 256)],
    model="TAS16T16-51-120-1S-DES",
)
_ru_1 = RU(
    serial_number="1M234905259",
    radio_type="AZQJ",
    pdu_port=_pdu.pdu_ports[1],
    ru_hw_group="RU_INT_ECPRI",
    attenuation_ports=[
        _attenuator.attenuator_ports[i] for i in [1, 34]  # port 20
    ],

)
_vdu_rannic1 = RANNIC(serial_number="L1240804847", product_code="1791B.101")
_vdu = VDU(
    cloud_deployment=_vdu_k8s_cloud_deployment,
    oam_http_connection_details=_vdu_oam_http_connection_details,
    rus=[_ru_1],
    instance_id=37256,
    fhuc_vlans=[301, 301],
    rannics=[_vdu_rannic1],
    f1_m_ip_addr=NetworkAddress(
        v4="192.168.254.33",
        vlan_id=295,
        routing=RoutingInformation(gateway="192.168.254.0", ip_prefix_length=26),
    ),
    # route configuration of f1c link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_c_ip_addr=NetworkAddress(
        v4="10.68.164.106",
        vlan_id=715,
        routing=RoutingInformation(gateway="10.68.164.105", ip_prefix_length=28),
    ),
    # route configuration of f1u link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_u_ip_addr=NetworkAddress(
        v4="10.68.164.104",
        vlan_id=715,
        routing=RoutingInformation(gateway="10.68.164.105", ip_prefix_length=28),
    ),

)
## for MRBTS-37020-FDD-DC
_vdu_k8s_ssh_connection_details_2 = SshServiceDetails(
    addr="10.68.163.178", username="core", password="system123"
)

_vdu_k8s_connection_details_2 = K8SConnectionDetails(
    ip_addr="10.68.163.178", username="core", password="system123", port=22
)

_vdu_master_node_2 = MasterNode(
    k8s_connection_details=_vdu_k8s_connection_details_2,
    ssh_connection_details=_vdu_k8s_ssh_connection_details_2,
)

_vdu_k8s_2 = K8S(namespace="cran1", master_node=_vdu_master_node_2)

_cluster_preparation_du_2 = HelmChart(
    name="aic-vdu-cluster-preparation-2",
    yaml_file=os.path.join(_cfg_dir, 'vdu-cluster-preparation-2.yaml'),
)

_prerequisite_du_2 = HelmChart(
    name="aic-vdu-prerequisite-2",
    yaml_file=os.path.join(_cfg_dir, 'vdu-prerequisite-2.yaml'),
)

_cnf_du_2 = HelmChart(
    name="aic-vdu",
    yaml_file=os.path.join(_cfg_dir, 'vdu-cnf-2.yaml'),
)

_vdu_k8s_cloud_deployment_2 = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    cloud_hosting=_vdu_k8s_2,
    cluster_preparation=_cluster_preparation_du_2,
    prerequisite=_prerequisite_du_2,
    cnf=_cnf_du_2,
)

_vdu_oam_http_connection_details_2 = HttpConnectionDetails(
    addr="10.68.163.210", port=443, username="Nemuadmin", password="Nokia@123"
)
_ru_2 = RU(
    serial_number="L1173816784",
    radio_type="AHCA",
    pdu_port=_pdu.pdu_ports[2],
    ru_hw_group="RU_INT_ECPRI",
    attenuation_ports=[
        _attenuator.attenuator_ports[i] for i in [66,74,83,92]  # port 20
    ],

)
_vdu_rannic2 = RANNIC(serial_number="L1234509100", product_code="1791B.M01")
_vdu_2 = VDU(
    cloud_deployment=_vdu_k8s_cloud_deployment_2,
    oam_http_connection_details=_vdu_oam_http_connection_details_2,
    rus=[_ru_2],
    instance_id=37020,
    fhuc_vlans=[301, 301],
    rannics=[_vdu_rannic2],
    # route configuration of f1m link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_m_ip_addr=NetworkAddress(
        v4="192.168.254.33",
        vlan_id=295,
        routing=RoutingInformation(gateway="192.168.254.0", ip_prefix_length=26),
    ),
    # route configuration of f1c link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_c_ip_addr=NetworkAddress(
        v4="10.68.163.202",
        vlan_id=415,
        routing=RoutingInformation(gateway="10.68.163.201", ip_prefix_length=28),
    ),
    # route configuration of f1u link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_u_ip_addr=NetworkAddress(
        v4="10.68.163.204",
        vlan_id=415,
        routing=RoutingInformation(gateway="10.68.163.201", ip_prefix_length=29),
    ),

)
_cu = CU(
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.110.78.233", username="Nemuadmin", password="Nokia@123"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.110.78.233", port=443, username="Nemuadmin", password="Nokia@123"
    ),
    backhaul_site_oam_ip="10.110.78.233",
    # route configuration for x2 link to ENB on VCU, v4 is network address of ENB x2 link
    x2c=NetworkAddress(
        v4="10.110.110.105",
        vlan_id=1009,
        routing_v4=RoutingInformation(gateway="10.110.110.96/27"),
    ),
    x2u=NetworkAddress(
        v4="10.110.110.137",
        vlan_id=1010,
        routing_v4=RoutingInformation(gateway="10.110.110.128/27"),
    ),
    xnc=NetworkAddress(
        v4="10.110.78.142",
        vlan_id=1002,
        routing_v4=RoutingInformation(gateway="10.110.78.128/26"),
    ),
    xnu=NetworkAddress(
        v4="10.110.44.147",
        vlan_id=1003,
        routing_v4=RoutingInformation(gateway="10.110.44.128/25"),
    ),
    # route configuration for f1c link to VDU on VCU, v4 is network address of VDU f1c link
    f1c=NetworkAddress(
        v4="10.110.78.201",
        vlan_id=1000,
        routing_v4=RoutingInformation(gateway="10.110.78.192/27"),
    ),
    # route configuration for f1u link to VDU on VCU, v4 is network address of VDU f1u link
    f1u=NetworkAddress(
        v4="10.110.44.19",
        vlan_id=1001,
        routing_v4=RoutingInformation(gateway="10.110.44.0/25"),
    ),
    s1u=NetworkAddress(
        v4="10.110.110.169",
        vlan_id=1011,
        routing_v4=RoutingInformation(gateway="10.110.110.160/27"),
    ),
    ngc=NetworkAddress(
        v4="10.110.110.9",
        vlan_id=1006,
        routing_v4=RoutingInformation(gateway="10.110.110.0/27"),
    ),
    ngu=NetworkAddress(
        v4="10.110.78.19",
        vlan_id=1004,
        routing_v4=RoutingInformation(gateway="10.110.78.0/25"),
    ),
    tracing=NetworkAddress(
        v4="10.110.110.41",
        vlan_id=1007,
        routing_v4=RoutingInformation(gateway="10.110.110.32/27"),
    )

)

_vcu_k8s_ssh_connection_details = SshServiceDetails(
    addr="10.110.12.194", username="cranuser6", password="systeM!23"
)

_vcu_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.110.12.194", username="core", password="system123", port=22
)

_vcu_master_node = MasterNode(
    k8s_connection_details=_vcu_k8s_connection_details,
    ssh_connection_details=_vcu_k8s_ssh_connection_details,
)

_vcu_k8s = K8S(namespace="cran6", master_node=_vcu_master_node)

_cluster_preparation_cu = HelmChart(
    name="aic-vcu-cluster-preparation",
    yaml_file=os.path.join(_cfg_dir, 'vcu-cluster-preparation.yaml'),
)

_prerequisite_cu = HelmChart(
    name="aic-vcu-prerequisite",
    yaml_file=os.path.join(_cfg_dir, 'vcu-prerequisite.yaml'),
)

_cnf_cu = HelmChart(
    name="aic-vcu",
    yaml_file=os.path.join(_cfg_dir, 'vcu-cnf.yaml'),
)

_vcu_k8s_cloud_deployment = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    cloud_hosting=_vcu_k8s,
    cluster_preparation=_cluster_preparation_cu,
    prerequisite=_prerequisite_cu,
    cnf=_cnf_cu,
)

_cbts = CloudBts(
    dus=[_vdu, _vdu_2],
    cu=_cu,
    cloud_deployment=_vcu_k8s_cloud_deployment,
)
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.0.81.63",
        username="ute",
        password="ute",
    ),
    connections=[_cbts]
)

ue_config_path = os.path.join(_cfg_dir, "TestData/inseego2.yml")
if os.path.isfile(ue_config_path):
    with open(ue_config_path) as f:
        ue_config = yaml.load(stream=f, Loader=yaml.FullLoader)
else:
    ue_config = ""

tl = TestLine(
    test_pc=_test_pc,
    cloud_hostings=[_vcu_k8s, _vdu_k8s, _vdu_k8s_2],
    gnbs=[_cbts],
    tl_cloud_topology="CLOUD_5G_AIC_1xAndriod_2xvDU_OE22_1xAZQJ_1xAHCA_FDD_TDD_DC",
    test_pcs=[_test_pc],
    ues=[ue_config],
    attenuator=_attenuator,
    pdus=_pdus,
)

__all__ = ["tl"]
