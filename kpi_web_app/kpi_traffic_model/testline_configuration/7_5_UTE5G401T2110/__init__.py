__maintainer__ = "Ding Binmei"
__team__ = "RAN_PZ_HAZ3_SG01"
__email__ = "binmei.ding@nokia-sbell.com"

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
from taf.config.testline import NetworkAddress, RoutingInformation
from taf.config.testline import RealEnb, Airscale, CommonUnit
from taf.config.testline import HBTE_PDU as HBTE
from taf.config.testline import RU, RadioTypes
from taf.config.testline import CloudBts, CU
from taf.config.testline import VDU, FHGW
from taf.config.testline import PxeServer
from taf.config.testline import TestLine
from taf.config.testline import RealEnb
from taf.config.testline import TestPc

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# Testpc
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="XXX", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# CU
_cu = CU(
    instance_id=37241,
    global_bts_id=37241,
    backhaul_site_oam_ip=NetworkAddress(v4="10.57.181.4"),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.70.222.214", username="tl2110", password="systeM!23"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.181.4", username="Nemuadmin", password="Nokia@123", port=443
    ),
    x2c=NetworkAddress(
        v4="10.57.182.68",
        vlan_id=110,
        routing_v4=RoutingInformation(gateway="10.57.182.64/26"),
    ),
    x2u=NetworkAddress(
        v4="10.57.182.69",
        vlan_id=110,
        routing_v4=RoutingInformation(gateway="10.57.182.64/26"),
    ),
    f1c=NetworkAddress(
        v4="10.57.182.4",
        vlan_id=109,
        routing_v4=RoutingInformation(gateway="10.57.182.0/26"),
    ),
    f1u=NetworkAddress(
        v4="10.57.182.5",
        vlan_id=109,
        routing_v4=RoutingInformation(gateway="10.57.182.0/26"),
    ),
    s1u=NetworkAddress(
        v4="10.57.181.36",
        vlan_id=102,
        routing_v4=RoutingInformation(gateway="10.57.181.32/27"),
    ),
    tracing=NetworkAddress(
        v4="10.57.181.68",
        vlan_id=103,
        routing_v4=RoutingInformation(gateway="10.57.181.64/27"),
    ),
)

# cloud_deployment for vCU
_vcu_cnf_1 = DeploymentVnfStack(
    name="vcutest",
    yaml_file=os.path.join(_cfg_dir, "DEP/gnbs_0/vCU/cu_cnf_values-override.yaml"),
)
_vcu_intnet_1 = DeploymentNetworkStack(
    name=_vcu_cnf_1.name + "-prerequisite",
    yaml_file=os.path.join(_cfg_dir, "DEP/gnbs_0/vCU/cu_pvc_values-override.yaml"),
)

# ssh connection information of OE, for tenant user
_vcu_ssh_connection_details = SshServiceDetails(
    addr="10.70.222.214", username="tl2110", password="systeM!23", port=22
)
# ssh connection information of OE, for root user
_vcu_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.70.222.214", username="tl2110", password="systeM!23", port=22
)

_vcu_master_node = MasterNode(
    k8s_connection_details=_vcu_k8s_connection_details,
    ssh_connection_details=_vcu_ssh_connection_details,
)

_vcu_k8s = K8S(namespace="tl2110", master_node=_vcu_master_node)

_vcu_k8s_cloud_deployment = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    networks=[_vcu_intnet_1],
    vnfs=[_vcu_cnf_1],
    cloud_hosting=_vcu_k8s,
)


# 5G RU
_ru_pdu = HBTE(addr="XX", port_numbers=[2])

_ru = RU(
    ru_hw_group="hw_group",
    pdu_port=_ru_pdu.pdu_ports[2],
    radio_type=RadioTypes.AEQY,
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.35",
        username="rfsw",
        password="5rfS2qmWC0AiFYvir7k8JekCN8/NklqDK5E6OWXuUVQ=",
    ),
)

# vDU
# _pxe_server_ssh_info = SshServiceDetails(
#     addr="10.71.223.254", username="ute", password="!Q2w3e4r5t6y7u"
# )
# _pxe_server = PxeServer(
#     nfs_ip="10.71.223.254", ssh_connection_details=_pxe_server_ssh_info
# )

# # FHGW information
# _fhgw_0 = FHGW(user_config_path=_cfg_dir, rus=[_ru], pxe_server=_pxe_server)
# _fhgw_0.ip = "10.64.161.53"
# _fhgw_0.username = "toor4nsn"
# _fhgw_0.password = "Fhgw@nokia123"
# _fhgw_0.version = "22R2"

_ssh_connection_details_0 = SshServiceDetails(
    addr="10.64.165.242", username="core", password="system123"
)
_k8s_connection_details_0 = K8SConnectionDetails(
    ip_addr="10.64.165.242", username="core", password="system123", port="22"
)

_master_node_0 = MasterNode(
    k8s_connection_details=_k8s_connection_details_0,
    ssh_connection_details=_ssh_connection_details_0,
)
_k8s_0 = K8S(namespace="cran1", master_node=_master_node_0)
_vdu_cnf_0 = DeploymentVnfStack(
    name="vdutest",
    yaml_file=os.path.join(_cfg_dir, "DEP/gnbs_0/vDU_0/du_cnf_values-override.yaml"),
)
_vdu_intnet_0 = DeploymentNetworkStack(
    name=_vdu_cnf_0.name + "-prerequisite",
    yaml_file=os.path.join(_cfg_dir, "DEP/gnbs_0/vDU_0/du_pvc_values-override.yaml"),
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
        addr="10.64.166.18", username="Nemuadmin", password="Nokia@123"
    ),
    # fhgws=[_fhgw_0],
    instance_id=37241,
    global_bts_id=37241,
)

# BTS
_cbts = CloudBts(
    dus=[_du_0],
    cu=_cu,
    cloud_deployment=_vcu_k8s_cloud_deployment,
)

# _common_unit_2 = CommonUnit(
#     lmp_connection=SshServiceDetails(
#         addr="10.71.212.163", username="toor4nsn", password="oZPS0POrRieRtu"
#     ),
#     capacity_units=[],
# )

# _real_enb = Airscale(common_units=[_common_unit_2])

# _lte_real_enb = RealEnb(
#     airscale=_real_enb,
#     oam_ip="10.71.212.163",
#     global_bts_id="608",
# )
# _attenuator = ATTEN_HBTE(
#     ip_addr="10.101.51.210",
#     port=5000,
#     model="PA-16-16-6-127-0.5-B-S",
#     attenuation_port_numbers=[5, 70, 1, 34, 67, 100, 13, 78, 73, 106, 71, 104],
# )
# _appserver_ssh = SshServiceDetails(
#     addr="10.70.222.55", username="mmw_sg1", password="mm@1", port="41510"
# )
#
# _iperf_details_on_appserver = IperfDataTransferDetails(
#     ssh_connection_details=_appserver_ssh,
#     network_interface_address="10.70.222.55",
#     iperf_path="iperf",
#     port="41510",
# )
#
# _appserver = AppServer(_iperf_details_on_appserver)
#
# # #Qualcomm
# _iperf = IperfDataTransferDetails(
#     ssh_connection_details=_appserver_ssh,
#     network_interface_address="10.70.222.55",
#     iperf_path="/cygdrive/c/iperf",
#     port="41511",
# )
# _android_0 = Android(
#     ssh_connection_details=SshServiceDetails(
#         addr="10.101.47.109", username="mn5gran", password="nokia123@"
#     ),
#     serial_number="6ee8000c",
#     server_dir="/cygdrive/c/pyro_server",
#     python_path="C:/Users/MN5GRAN/AppData/Local/Programs/Python/Python36/python.exe",
#     qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
#     diag_cfg_path="C:/pyro_server/DIAG.cfg",
#     iperf_details=_iperf,
#     capabilities=["REAL_ANDROID_UE", "sdx70", "qct_dx50"],
#     clear_server_files="yes",
#     clear_logs="yes",
#     network_mode_switch_method="keyevents",
#     mobile_network_text="SIMs",
#     setting_network_mode_text="Preferred network type",
# )
############################################
# TestLine
tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    tl_cloud_topology="CLOUD_5G_AIC_RM17_OCP_OE22",
    # enbs=[_lte_real_enb],
    # attenuators=[_attenuator],
    # ues=[_android_0],
)
