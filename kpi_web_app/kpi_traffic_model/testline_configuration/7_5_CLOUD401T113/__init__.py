__maintainer__ = "Fan Kongshuai"
__team__ = "I_MN_5G_RAN_IV4_QT_HZG_GMS <I_MN_5G_RAN_IV4_QT_HZG@internal.nsn.com>"
__email__ = "I_MN_5G_RAN_IV4_QT_HZG@internal.nsn.com"
__owner_email__ = "kongshuai.fan@nokia-sbell.com"

import os

from taf.config.testline.cloud_hosting import (
    ControlNode,
    CloudDeployment,
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
from taf.config.testline.pdu import FACOM
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU
from taf.config.testline.enb import RealEnb
from taf.config.testline.ue import TM500
from taf.config.testline import DU, RU
from taf.config.testline.cloud_hosting import MasterNode, K8S
from taf.config.testline.connection_details import K8SConnectionDetails
from taf.config.testline.gnb.du import VDU
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.radio import RadioModule
from taf.config.testline.appserver import AppServer

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# Testpc
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.108.183.58", username="root", password="nokia123"
    )
)

# CU
_cu = CU(
    backhaul_site_oam_ip="10.107.169.147",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.107.169.147", username="robot", password="rastre1"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.107.169.147", username="Nemuadmin", password="nemuuser"
    ),
)

# DU
_common_unit_pdu = FACOM(addr="10.57.241.140", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_lmp_connection_0 = SshServiceDetails(
    addr="10.57.235.108", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_0 = CapacityUnit(addr="192.168.253.20")

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection_0,
    capacity_units=[_capacity_unit_0],
    pdu_port=_common_unit_pdu.pdu_ports[5],
)
# vCU
# VCU internal network configuration for deployment
_vcu_intnet_1 = DeploymentNetworkStack(
    name="qt-net",
    yaml_file=os.path.join(_cfg_dir, "values-override.yaml"),
)

# ssh connection information of OE, for tenant user
_ssh_connection_details = SshServiceDetails(
    addr="10.57.137.74", username="root", password="root"
)

# ssh connection information of OE, for cloudadmin user
_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.57.137.74", username="root", password="root", port="22"
)

# master node information of OE
_master_node = MasterNode(
    k8s_connection_details=_k8s_connection_details,
    ssh_connection_details=_ssh_connection_details,
)

_k8s = K8S(namespace="cran1", master_node=_master_node)

# VCU configuration for deployment
_vcu_cnf_1 = DeploymentVnfStack(
    name="vcutest", yaml_file=os.path.join(_cfg_dir, "values-override.yaml")
)

_vcu_pvc_1 = DeploymentVnfStack(
    name="pvc-vcutest", yaml_file=os.path.join(_cfg_dir, "values-override.yaml")
)

# VCU deployment configuration
_k8s_cloud_deployment = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    networks=[_vcu_intnet_1],
    vnfs=[_vcu_cnf_1, _vcu_pvc_1],
    cloud_hosting=_k8s,
)

# VCU oam http connection
_vdu_oam_http_connection_details = HttpConnectionDetails(
    addr="10.57.170.84",
    port="443",
    username="Nemuadmin",
    password="nemuuser",
)


# airscale
_airscale_0 = Airscale(common_units=[_common_unit_0])

# 5G RU
_ru_pdu = FACOM(addr="10.57.246.238", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.52", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu.pdu_ports[5],
)

_du_0 = DU(airscale=_airscale_0, rus=[_ru], f1_m_ip_addr="10.57.227.78")
_du_1 = VDU(
    cloud_deployment=_k8s_cloud_deployment,
    oam_http_connection_details=_vdu_oam_http_connection_details,
)

# 4G RU
_4g_ru_pdu = FACOM(addr="10.57.249.22", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_RadioModule = RadioModule(
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="umniedziala"
    ),
    pdu_port=_4g_ru_pdu.pdu_ports[1],
)


# Real ENB
_real_enb_pdu = FACOM(addr="10.57.241.141", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_common_unit_enb = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.235.103", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[1],
    hardware_type="ASIA",
    hardware_version="A.103",
)

_real_enb = Airscale(common_units=[_common_unit_enb])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=[_RadioModule])
#

# CloudBts
_cbts = CloudBts(
    dus=[_du_0, _du_1],
    cu=_cu,
    cloud_deployment=_k8s_cloud_deployment,
    vnf_name="hgz-tl113",
    instance_id="1",
    global_bts_id="1",
)
#########UE##########
_iperf_data_transfer = IperfDataTransferDetails(
    ssh_connection_details=SshServiceDetails(
        addr="10.108.183.58", username="root", password="nokia123"
    ),
    network_interface_address="10.108.183.58",
    iperf_path="/usr/bin/iperf",
    port=59995,
)

_cobham = TM500(
    tma_host=SshServiceDetails(
        addr="10.57.130.60", username="CNHZ5GRAN1024+tester", password="tester123"
    ),
    tma_command_port=5004,
    tma_path=(
        r"C:\\Program Files (x86)\\Aeroflex\\TM500\\5G NR - NLA 4.33.2"
        r"\\Test Mobile Application\\TmaApplication.exe"
    ),
    iperf_details=_iperf_data_transfer,
)

_cobham.ue_type = "viavi"

#########app server#########
_appserver_ssh = SshServiceDetails(
    addr="10.108.183.58", username="ute", password="iW_K#8.ute%A10h0m0ra"
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.108.183.58",
    iperf_path="iperf",
    port=5023,
)

_appserver = AppServer(_iperf_details_on_appserver)

# TestLine
tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    enbs=[_lte_real_enb],
    ues=[_cobham],
    appserver=_appserver,
    tl_cloud_topology="hgz-tl113",
)

__all__ = ["tl"]
