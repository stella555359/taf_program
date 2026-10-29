__maintainer__ = "Wang Xiaocui"
__team__ = ""
__email__ = ""
__owner_email__ = "xiaocui.wang@nokia-sbell.com"

import os

from taf.config.testline.cloud_hosting import (
    ControlNode,
    NCIR,
    CloudDeployment,
    DeploymentFlavorStack,
    DeploymentNetworkStack,
    DeploymentVnfStack,
)
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    UltraCallerConnectionDetails,
)
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline import RealEnb, NetworkAddress, RoutingInformation
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU
from taf.config.testline.lab_infrastructure import PxeServer
from taf.config.testline.core import RealCore
from taf.config.testline.connection_details import K8SConnectionDetails
from taf.config.testline.gnb.du import FHGW
from taf.config.testline.gnb.du import VDU
from taf.config.testline.cloud_hosting import MasterNode, K8S
from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.config.testline.radio import RU
from taf.config.testline.nms import NMS
from taf.config.testline.nom import NOM
from taf.config.testline.ue import UltraCaller
from taf.config.testline.ue import Qualcomm, QualcommUeType, Android
from taf.config.testline.appserver import AppServer

# Following mandatory files and parameters should be configured
# Please don't ignore any parameters, you can add, but don't ingore
# Any problem, please check with CI team

#################################################################

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# UTE IP address and User Name, Password,
# this is test PC (UTE VM) for AIC
# NOTE! WE ARE USING 5718 UTE VM SINCE DEDICATED UTE VM IS NOT YET AVAILABLE FOR 5725 TL
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.111", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# VCU related NCIR controlNode:
_control = ControlNode(
    # Configuration for SSH access
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.138.34", username="core", password="system123"
    ),
    # Configuration for openstack connection
    open_stack_connection_details=OpenStackConnectionDetails(
        username="core",
        password="system123",
        ip_addr="10.57.138.34",
        tenant="core",
    ),
    # Configuration of BMC connection, if you need use it in test case, plase config it
    # currently, it's not used in agent
    bmc_connection_details=BmcConnectionDetails(addr="", username="", password=""),
)

# configuration of VCU related NCIR/OSP
_ncir = NCIR(compute_nodes=[], control_nodes=[_control], version="ncir_18")

# CU configuration (vCU-5725):
_cu = CU(
    # CU web UI ip address, oam interface ip of oam vm
    backhaul_site_oam_ip=NetworkAddress(v4="10.57.179.59"),
    # VCU OAM ssh connection, oam interface ip of oam vm
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.138.34", username="core", password="system123"
    ),
    # VCU OAM http connection, oam interface ip of oam vm
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.179.59", username="Nemuadmin", password="nemuuser", port="443"
    ),
    # route vCU -> SGW, currently placeholder IP
    s1u=NetworkAddress(
        v4="10.57.179.250",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.57.179.193", ip_prefix_length=26),
    ),
    # route vCU -> 4G/SBTS X2 interface, currently placeholder IP
    x2c=NetworkAddress(
        v4="10.57.179.184",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.57.179.129", ip_prefix_length=26),
    ),
    # route vCU -> vDU F1-C interface, currently placeholder IP
    f1c=NetworkAddress(
        v4="10.57.179.120",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.57.179.65", ip_prefix_length=26),
    ),
    # route vCU -> vDU F1-U interface, currently placeholder IP
    f1u=NetworkAddress(
        v4="10.57.179.119",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.57.179.65", ip_prefix_length=26),
    ),
    tracing=None,
)

# enb for NSA (not used, 5725 is SA)
_real_enb = RealEnb(oam_ip="10.71.209.98", instance_id="")

# test pc information of enb
# you can configure it as AIC UTE environment
_enb_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.111", username="ute", password="CsvUTE2021!"
    ),
    connections=[_real_enb],
)

# flavor of VCU, currently not used
flavor_env_files = [os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/5gbts_flavor.env")]

# ext_net of VCU, currently not used
net_env_files = [os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/5gbts_ext_net.env")]

# heat parameters, currently not used
vnf_env_files = [os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/5gbts_heat.env")]

_cbts_flavor = DeploymentFlavorStack(
    name="name is not used",  # this name is not used, you need NOT configure it, let it be
    env_files=flavor_env_files,
    default_vnf_prefix="esp-tl5725",
)

_cbts_net = DeploymentNetworkStack(
    name="name is not used",  # this name is not used, you need NOT configure it, let it be
    env_files=net_env_files,
    yaml_file=os.path.join(_cfg_dir, "5gbts_ext_net.yaml"),
)

_cbts_vnf = DeploymentVnfStack(
    name="name is not used",  # this name is not used, you need NOT configure it, let it be
    env_files=vnf_env_files,
    yaml_file=os.path.join(_cfg_dir, "5gbts_heat.yaml"),
)

# cloud deployment configuration fo VCU
_cloud_deployment = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    flavors=[_cbts_flavor],
    networks=[_cbts_net],
    vnfs=[_cbts_vnf],
    cloud_hosting=_ncir,
)

# VDU configuration for deployment, currently not used
_vdu_vnf_0 = DeploymentVnfStack(
    name="aic-vdu-mvp",  # this is vdu release name, the name should only be lower case and only can include alphabet, number, _
    yaml_file=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/aic_vdu_values_override_0.yaml"
    ),
)

# VDU internal network configuration for deployment, currently not used
_vdu_intnet_0 = DeploymentNetworkStack(
    name="aic-intnet-mvp",  # this is intnet release name
    yaml_file=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/aic_intnet_values_override_0.yaml"
    ),
)

# ssh connection information of OE
_ssh_connection_details = SshServiceDetails(
    addr="10.71.221.62", username="core", password="system123"
)

# ssh connection information of OE, for cloudadmin user
_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.71.221.62", username="core", password="system123", port="22"
)

# master node information of OE
_master_node = MasterNode(
    k8s_connection_details=_k8s_connection_details,
    ssh_connection_details=_ssh_connection_details,
)

_k8s = K8S(namespace="tl2072", master_node=_master_node)

# VDU deployment configuration
_k8s_cloud_deployment = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    networks=[_vdu_intnet_0],
    vnfs=[_vdu_vnf_0],
    cloud_hosting=_k8s,
)

# VDU oam http connection
_vdu_oam_http_connection_details = HttpConnectionDetails(
    addr="10.71.221.18", port="443", username="Nemuadmin", password="nemuuser"
)

# RU configuration
_ru_1 = RU(ru_hw_group="RU_INT_CPRI", serial_number="1M204202984")

# PXE server info for FHGW deployment, currently not used
_pxe_server_ssh_info = SshServiceDetails(
    addr="10.10.10.10", username="labuser", password="system123"
)
_pxe_server = PxeServer(
    nfs_ip="10.10.10.10", ssh_connection_details=_pxe_server_ssh_info
)

# FHGW information
_fhgw_0 = FHGW(
    user_config_path=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/FHGW_0/user_config_0.yaml"
    ),
    rus=[_ru_1],
    pxe_server=_pxe_server,
)

_switch_1 = {
    "du_switch_ip": "10.10.10.10",
    "username": "chriscd",
    "password": "12345678",
    "en_password": "",
    "port": "23",
    "switch_interface": "1/1/1",
    "simu4DU_interface": "",
    "acl_number": "188",
    "du_vlan_id": "20",
    "du_vlan_masklen": "27",
    "du_vlan_gateway": "10.10.10.10",
    "du_vlan_mtu": "1500",
    "du_2nd_vlan_id": "100",
    "du_2nd_vlan_masklen": "27",
    "du_2nd_vlan_gateway": "10.10.10.10",
    "du_2nd_vlan_mtu": "1500",
    "du_2nd_vlan_ip": "10.10.10.10",
}
_fhgw_misc = {
    "ruproxy_create_tool": "create_ruproxy_new.py",
    "ruproxy_delete_tool": "removePod_new.py",
}
_tools_repository = {
    "ip": "10.10.10.10",
    "username": "ute",
    "password": "ute",
    "repo_tool_folder": "/opt/tools/trans_test/",
    "repo_data_folder": "/opt/tools/trans_data/",
    "repo_simu4trs_folder": "/opt/tools/trans_simu4trs/",
}

_trans_para = {
    "tools_repository": _tools_repository,
    "du_switch": [_switch_1],
    "fhgw_misc": _fhgw_misc,
}

# VDU global configuration
_vdu_0 = VDU(
    cloud_deployment=_k8s_cloud_deployment,
    oam_http_connection_details=_vdu_oam_http_connection_details,
    fhgws=[_fhgw_0],
    # route vDU -> vCU F1-M interface, currently not used
    f1_m_ip_addr=NetworkAddress(
        v4="10.10.10.10",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.10.10.10", ip_prefix_length=28),
    ),
    # route vDU -> vCU F1-C interface, currently not used
    f1_c_ip_addr=NetworkAddress(
        v4="10.71.221.10",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.221.9", ip_prefix_length=29),
    ),
    # route vDU -> vCU F1-U interface, currently not used
    f1_u_ip_addr=NetworkAddress(
        v4="10.71.221.11",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.221.9", ip_prefix_length=29),
    ),
)

# mcc, mnc configuration
_realcore = RealCore(five_g=None, mcc="001", mnc="01", pdns=None)

# VCU global configuration
_cbts_0 = CloudBts(
    dus=[_vdu_0],  # vdu related parameter
    cu=_cu,
    cloud_deployment=_cloud_deployment,
    instance_id="2072",
    global_bts_id="2072",
)

_nom_ssh_connection_edge0 = SshServiceDetails(addr="10.10.10.10", username="cloud-user")

_nom1 = NOM(
    ssh_connections_info=[_nom_ssh_connection_edge0],
    https_main_info=HttpConnectionDetails(
        addr="https://neo-hosting-page.srncnms04.srnblr.nsn-rdnet.net/",
        username="cnms01",
        password="Qwer1234",
    ),
    neo_endpoints_ip="10.10.10.10",
)

_cnms = NMS(addr="10.10.10.10", nom=_nom1)

_uc_server_details = HttpConnectionDetails(addr="10.16.34.213", port=443)
_uc_details = UltraCallerConnectionDetails(
    ultracaller_server_details=_uc_server_details,
    api_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IjVHX0FJQyIsImFkbWluIjp0cnVlfQ.VgxWJeHFL--49Zlw1v9jlj9pV2tk34N8HskQYtmQoRc",
)

_uc_ue1 = UltraCaller(
    ultracaller_connection_details=_uc_details,
    head_group="5725",
    sub_group="5725",
    imei="353137110421297",
)
_appserver_ssh = SshServiceDetails(
    addr="10.57.162.3", username="mmw_sg3", password="test@123!", port="43055"
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.162.3",
    iperf_path="/usr/bin/iperf",
    port="43455",
)
_iperf_details_on_appserver2 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.162.3",
    iperf_path="iperf",
    port="44055",
)
_appserver = AppServer(_iperf_details_on_appserver2)


_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.217.68", username="nokia5G", password="noki@123"
    ),
    serial_number="R3CR40S2CMM",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="/cygdrive/c/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "samsung_vran20"],
)
# Testline configuration, tl is only variable which can be accessed by agent and test case
# you can access all parameters configured upper by tl parameter
tl = TestLine(
    test_pc=_test_pc,
    nms=_cnms,
    gnbs=[_cbts_0],
    enbs=[_real_enb],
    ues=[_android],
    tl_cloud_topology="CLOUD_5G_AIC_NCIR_NCIR_FHGW_AHCA",
    cloud_hostings=[_ncir],
    test_pcs=[_enb_test_pc],
    core=_realcore,
    appserver=_appserver,
)
tl._trans_para = _trans_para
# only tl variable can be accessed by user
__all__ = ["tl"]
