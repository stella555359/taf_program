__maintainer__ = "Xu zhifu"
__team__ = "I_NSB_MN_RAN_PZ_1_HAZ_1_GMS "
__email__ = "I_NSB_MN_RAN_PZ_1_HAZ_1@internal.nsn.com"
__owner_email__ = "zhifu.xu@nokia-sbell.com"

import os
from taf.config.testline.cloud_hosting import (
    MasterNode,
    K8S,
    ComputeNode,
    CloudDeployment,
    HelmChart,
    ContainerRegistry,
)

from taf.config.testline.connection_details import (
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    K8SConnectionDetails,
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
from taf.config.testline.cloud_hosting import MasterNode, K8S
from taf.config.testline.pdu import FPFH
from taf.config.testline.ue import Android, Qualcomm


########### Part 4: UE ####################################
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

Qualcomm = Android(
ssh_connection_details=SshServiceDetails(
addr="10.97.65.197", username="pz1", password="Nokia@2w3e4r5t6y7u"
),
serial_number="bb957cac",
server_dir="/cygdrive/c/pyro_server",
python_path="C:/Python27/python.exe",
qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
diag_cfg_path="C:/pyro_server/DIAG.cfg",
iperf_details=_iperf,
capabilities=["Commercial", "REAL_ANDROID_UE"],
)

huawei1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.97.65.197", username="pz1", password="Nokia@2w3e4r5t6y7u"
    ),
    serial_number="H4K5T21105008665",
    # 460
    server_dir="/cygdrive/c/pyro_server",
    python_path="/cygdrive/c/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["Commercial", "huawei1"],
)

samsungs21 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.97.65.197", username="pz1", password="Nokia@2w3e4r5t6y7u"
    ),
    serial_number="R5CR30WLQXN",
    # 460
    server_dir="/cygdrive/c/pyro_server",
    python_path="/cygdrive/c/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["Commercial", "samsungs21"],
)

# PDU  port2= Airphone
_pdu = FPFH(addr="10.97.65.130", port_numbers=[1])

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

_pdus = [_pdu]

container_registry = ContainerRegistry(url="harbor-vrf1.ocp.hz.nsn-rdnet.net:443/vrf1", username="admin", password="HZnokia123!")

_vdu_k8s_ssh_connection_details = SshServiceDetails(
    addr="10.69.104.82", username="core", password="system123"
)

_vdu_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.69.104.82", username="core", password="system123", port=22
)

_vdu_master_node = MasterNode(
    k8s_connection_details=_vdu_k8s_connection_details,
    ssh_connection_details=_vdu_k8s_ssh_connection_details,
)

_vdu_k8s = K8S(namespace="cran1", master_node=_vdu_master_node)

_cluster_preparation_du = HelmChart(
    name="aic-vdu-cluster-preparation",
    yaml_file=os.path.join(_cfg_dir, "vdu-cluster-preparation.yaml"),
)

_prerequisite_du = HelmChart(
    name="aic-vdu-prerequisite",
    yaml_file=os.path.join(_cfg_dir, "vdu-prerequisite.yaml"),
)

_cnf_du = HelmChart(name="aic-vdu", yaml_file=os.path.join(_cfg_dir, "vdu-cnf.yaml"))

_vdu_k8s_cloud_deployment = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    cloud_hosting=_vdu_k8s,
    cluster_preparation=_cluster_preparation_du,
    prerequisite=_prerequisite_du,
    cnf=_cnf_du,
    container_registry=container_registry,
)

_vdu_oam_http_connection_details = HttpConnectionDetails(
    addr="10.69.104.114", port=443, username="Nemuadmin", password="nemuuser"
)

_vdu_0_rannic1 = RANNIC(serial_number="L1234509044", product_code="AF1791.M01")

_vdu = VDU(
    cloud_deployment=_vdu_k8s_cloud_deployment,
    oam_http_connection_details=_vdu_oam_http_connection_details,
    instance_id=10872,
    fhuc_vlans=[301],
    rannics=[_vdu_0_rannic1],
)

_cu = CU(
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.107.160.11", username="Nemuadmin", password="nemuuser"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.107.160.11", port=443, username="Nemuadmin", password="nemuuser"
    ),
    backhaul_site_oam_ip="None",
)

_vcu_k8s_ssh_connection_details = SshServiceDetails(
    addr="10.107.123.165", username="cranuser11", password="systeM!23"
)

_vcu_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.107.123.165", username="core", password="system123", port=22
)

_vcu_master_node = MasterNode(
    k8s_connection_details=_vcu_k8s_connection_details,
    ssh_connection_details=_vcu_k8s_ssh_connection_details,
)

_vcu_k8s = K8S(namespace="cran11", master_node=_vcu_master_node)
_cluster_preparation_cu = HelmChart(
  name = "aic-vcu-cluster-preparation",
  yaml_file = os.path.join(_cfg_dir, 'vcu-cluster-preparation.yaml'),
)

_prerequisite_cu = HelmChart(
    name="aic-vcu-prerequisite",
    yaml_file=os.path.join(_cfg_dir, "vcu-prerequisite.yaml"),
)

_cnf_cu = HelmChart(name="aic-vcu", yaml_file=os.path.join(_cfg_dir, "vcu-cnf.yaml"))

_vcu_k8s_cloud_deployment = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    cloud_hosting=_vcu_k8s,
    cluster_preparation=_cluster_preparation_cu,
    prerequisite=_prerequisite_cu,
    cnf=_cnf_cu,
)

_cbts = CloudBts(
    dus=[_vdu],
    cu=_cu,
    cloud_deployment=_vcu_k8s_cloud_deployment,
    instance_id="10872",
    global_bts_id="10872",
)

_preferred_vlan = PreferredVlan(slot_id=SlotId.B1, port_id=1, preferred_vlan_id=205)

_ue = Airphone(
    SshServiceDetails("", ""),
    SshServiceDetails("", ""),
    SshServiceDetails("", ""),
    Airscale(
        [
            CommonUnit(
                SshServiceDetails(
                    "192.168.200.1", "toor4nsn", password="oZPS0POrRieRtu"
                ),
                [CapacityUnit(addr="192.168.253.84", hardware_type="ABIO")],
                hardware_type="ASIL",
                pdu_port=_pdus[0].pdu_ports[1],
            )
        ]
    ),
    preferred_vlans=[_preferred_vlan],
)

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.97.65.249", username="ute", password="uteUTE!"
    ),
    connections=[_cbts, _ue],
)

tl = TestLine(
    test_pc=_test_pc,
    cloud_hostings=[_vcu_k8s, _vdu_k8s],
    gnbs=[_cbts],
    tl_cloud_topology="CLOUD_5G_AIC_SA_1xAndroid_mate1_1xvDU_OE20_1xFHGW_1xAEQY",
	ues=[huawei1,samsungs21, Qualcomm],
    pdus=_pdus,
)

__all__ = ["tl"]
