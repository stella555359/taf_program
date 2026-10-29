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
    HBTE,
)  # added in taf.meta 5.4
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, ATEN, RRB, APC, Gude
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
        addr="10.57.167.180", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# CU

## CU0
_cu_0 = CU(
    instance_id=37159,
    global_bts_id=37159,
    backhaul_site_oam_ip=NetworkAddress(v4="10.57.209.143"),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.209.2", username="cranuser2115", password="systeM!23"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.209.143", username="Nemuadmin", password="Nokia@123", port=443
    ),
    x2c=NetworkAddress(
        v4="10.57.210.90",
        vlan_id=110,
        routing=RoutingInformation(gateway="10.57.210.65", ip_prefix_length=26),
    ),
    x2u=NetworkAddress(
        v4="10.57.210.91",
        vlan_id=110,
        routing=RoutingInformation(gateway="10.57.210.65", ip_prefix_length=26),
    ),
    f1c=NetworkAddress(
        v4="10.57.210.30",
        vlan_id=109,
        routing=RoutingInformation(gateway="10.57.210.1", ip_prefix_length=26),
    ),
    f1u=NetworkAddress(
        v4="10.57.210.26",
        vlan_id=109,
        routing=RoutingInformation(gateway="10.57.210.1", ip_prefix_length=26),
    ),
    s1u=NetworkAddress(
        v4="10.57.209.47",
        vlan_id=102,
        routing=RoutingInformation(gateway="10.57.209.33", ip_prefix_length=27),
    ),
    tracing=None,
)

# cloud_deployment for vCU0
_vcu_cnf_0 = DeploymentVnfStack(
    name="cran2115",
    yaml_file=os.path.join(_cfg_dir, "DEP/gnbs_0/vCU/CU_cnf_values-override.yaml"),
)
_vcu_intnet_0 = DeploymentNetworkStack(
    name=_vcu_cnf_0.name + "-prerequisite",
    yaml_file=os.path.join(_cfg_dir, "DEP/gnbs_0/vCU/CU_pvc_values-override.yaml"),
)

# ssh connection information of OE, for tenant user, tester used
_vcu_ssh_connection_details_0 = SshServiceDetails(
    addr="10.57.209.2", username="cranuser2115", password="systeM!23", port=22
)
# ssh connection information of OE, for root user
_vcu_k8s_connection_details_0 = K8SConnectionDetails(
    ip_addr="10.57.209.2", username="core", password="system123", port=22
)

_vcu_master_node_0 = MasterNode(
    k8s_connection_details=_vcu_k8s_connection_details_0,
    ssh_connection_details=_vcu_ssh_connection_details_0,
)

_vcu_k8s_0 = K8S(namespace="cran2115", master_node=_vcu_master_node_0)

_vcu_k8s_cloud_deployment_0 = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    networks=[_vcu_intnet_0],
    vnfs=[_vcu_cnf_0],
    cloud_hosting=_vcu_k8s_0,
)

# 5G RU
_hbte_params_0 = {
    "ip_addr": "10.57.230.22",
    "port": 5000,
    "attenuation_port_numbers": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    "model": "PA-16-16-6-127-0.5-B-S",
    "version": None,
}

_attenuator_0 = HBTE(**_hbte_params_0)


_hbte_params_1 = {
    "ip_addr": "10.57.230.21",
    "port": 5000,
    "attenuation_port_numbers": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    "model": "PA-16-16-6-127-0.5-B-S",
    "version": None,
}

_attenuator_1 = HBTE(**_hbte_params_1)

_ru_pdu_0 = FACOM(addr="10.57.246.201", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru_0 = RU(
    ru_hw_group="hw_group",
    pdu_port=_ru_pdu_0.pdu_ports[6],
    radio_type=RadioTypes.AEQY,
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.35",
        username="rfsw",
        password="5rfS2qmWC0AiFYvir7k8JekCN8/NklqDK5E6OWXuUVQ=",
    ),
    attenuation_ports=[
        _attenuator_0.attenuator_ports[1],
        _attenuator_0.attenuator_ports[2],
        _attenuator_0.attenuator_ports[3],
        _attenuator_0.attenuator_ports[4],
    ],
)

# vDU
_pxe_server_ssh_info = SshServiceDetails(
    addr="10.64.171.54", username="ute", password="!Q2w3e4r5t6y7u"
)
_pxe_server = PxeServer(
    nfs_ip="10.64.171.54", ssh_connection_details=_pxe_server_ssh_info
)

## vDU0
# FHGW information
_fhgw_0 = FHGW(
    user_config_path=_cfg_dir,
    rus=[_ru_0],
    pxe_server=_pxe_server,
)

_fhgw_0.ip = "10.64.169.181"
_fhgw_0.username = "toor4nsn"
_fhgw_0.password = "Fhgw@nokia123"
_fhgw_0.version = "25R2"

_ssh_connection_details_0 = SshServiceDetails(
    addr="10.0.181.178", username="core", password="system123"
)
_k8s_connection_details_0 = K8SConnectionDetails(
    ip_addr="10.0.181.178", username="core", password="system123", port="22"
)

_master_node_0 = MasterNode(
    k8s_connection_details=_k8s_connection_details_0,
    ssh_connection_details=_ssh_connection_details_0,
)
_k8s_0 = K8S(namespace="cran1", master_node=_master_node_0)
_vdu_cnf_0 = DeploymentVnfStack(
    name="vdu2115",
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
        addr="10.0.181.202", username="Nemuadmin", password="Nokia@123"
    ),
    instance_id=37159,
    global_bts_id=37159,
)

# BTS
_cbts_0 = CloudBts(
    dus=[_du_0],
    cu=_cu_0,
    cloud_deployment=_vcu_k8s_cloud_deployment_0,
)

## ENB ##
_common_unit_0 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.71.199.19", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
)

_real_enb_0 = Airscale(common_units=[_common_unit_0])

_lte_real_enb_0 = RealEnb(
    airscale=_real_enb_0,
    oam_ip="10.71.199.19",
    instance_id=10504,
    global_bts_id="10504",
)

_appserver_ssh = SshServiceDetails(
    addr="10.70.222.54", username="mmw_sg1", password="mm@1", port="41630"
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.70.222.54",
    iperf_path="/usr/bin/iperf",
    port="41631",
)
_appserver = AppServer(_iperf)

#UE Info
_android_0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.217.206", username="nokia5G", password="noki@123"
    ),
    serial_number="9a41506a",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python38/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="/cygdrive/c/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "sdx65", "qct_dx50"],
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
    # attenuator=[_attenuator_0, _attenuator_1],
    appserver=_appserver,
)
