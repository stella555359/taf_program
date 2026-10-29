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
from taf.config.testline import Airscale, CommonUnit
from taf.config.testline import HBTE_PDU as HBTE
from taf.config.testline import RadioTypes
from taf.config.testline import RealEnb, RoutingInformation
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
from taf.config.testline.attenuator import HBTE




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
        addr="10.57.167.48", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# VCU related NCIR controlNode:
_control = ControlNode(
    # Configuration for SSH access
    default_ssh_connection_details=SshServiceDetails(
        addr="10.70.222.214", username="tl2078", password="systeM!23"
    ),
    # Configuration for openstack connection
    open_stack_connection_details=OpenStackConnectionDetails(
        username="tl2078",
        password="systeM!23",
        ip_addr="10.70.222.214",
        tenant="tl2078",
    ),
    # Configuration of BMC connection, if you need use it in test case, plase config it
    # currently, it's not used in agent
    bmc_connection_details=BmcConnectionDetails(addr="", username="", password=""),
)

# configuration of VCU related NCIR/OSP
_ncir = NCIR(compute_nodes=[], control_nodes=[_control], version="ncir_18")

# CU configuration (vCU-5725):
_cu = CU(
    instance_id=2078,
    global_bts_id=2078,
    # CU web UI ip address, oam interface ip of oam vm
    backhaul_site_oam_ip=NetworkAddress(v4="10.57.181.4"),
    # VCU OAM ssh connection, oam interface ip of oam vm
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.70.222.214", username="tl2078", password="systeM!23"
    ),
    # VCU OAM http connection, oam interface ip of oam vm
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.181.4", username="Nemuadmin", password="Nokia@123", port="443"
    ),
    # route vCU -> SGW, currently placeholder IP
    s1u=NetworkAddress(
        v4="10.57.181.36",
        vlan_id=102,
        routing=RoutingInformation(gateway="10.57.181.33", ip_prefix_length=27),
    ),
    # route vCU -> 4G/SBTS X2 interface, currently placeholder IP
    x2c=NetworkAddress(
        v4="10.57.182.68",
        vlan_id=110,
        routing=RoutingInformation(gateway="10.57.182.65", ip_prefix_length=26),
    ),
    # route vCU -> vDU F1-C interface, currently placeholder IP
    f1c=NetworkAddress(
        v4="10.57.182.4",
        vlan_id=109,
        routing=RoutingInformation(gateway="10.57.182.1", ip_prefix_length=26),
    ),
    # route vCU -> vDU F1-U interface, currently placeholder IP
    f1u=NetworkAddress(
        v4="10.57.182.5",
        vlan_id=109,
        routing=RoutingInformation(gateway="10.57.182.1", ip_prefix_length=26),
    ),
    x2u=NetworkAddress(
        v4="10.57.182.69",
        vlan_id=110,
        routing=RoutingInformation(gateway="10.57.182.65", ip_prefix_length=26),
    ),
    ngc=NetworkAddress(
        v4="10.57.182.132",
        vlan_id=111,
        routing=RoutingInformation(gateway="10.57.182.129", ip_prefix_length=26),
    ),
    ngu=NetworkAddress(
        v4="10.57.182.133",
        vlan_id=111,
        routing=RoutingInformation(gateway="10.57.182.129", ip_prefix_length=26),
    ),
    tracing=None,
)

# enb for NSA (not used, 5725 is SA)
_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.71.209.99", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
)

_real_enb = Airscale(common_units=[_common_unit_2])
_lte_real_enb = RealEnb(
    airscale=_real_enb,
    oam_ip="10.71.209.99",
    global_bts_id="10583",
)

# test pc information of enb
# you can configure it as AIC UTE environment
_enb_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.48", username="ute", password="CsvUTE2021!"
    ),
    connections=[_lte_real_enb],
)

# cloud_deployment for vCU
_vcu_cnf_1 = DeploymentVnfStack(
    name="vcu2078",  # chart_name under [VCU_CONFIG_INFO] in kuafu-vcu_config.ini
    yaml_file=os.path.join(_cfg_dir, "DEP/gnbs_0/vCU/CU_cnf_values-override.yaml"),
)
_vcu_intnet_1 = DeploymentNetworkStack(
    name=_vcu_cnf_1.name + "-prerequisite",
    yaml_file=os.path.join(_cfg_dir, "DEP/gnbs_0/vCU/CU_pvc_values-override.yaml"),
)

# ssh connection information of OE, for tenant user
_vcu_ssh_connection_details = SshServiceDetails(
    addr="10.70.222.214", username="tl2078", password="systeM!23", port=22
)
# ssh connection information of OE, for root user
_vcu_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.70.222.214", username="tl2078", password="systeM!23", port=22
)

_vcu_master_node = MasterNode(
    k8s_connection_details=_vcu_k8s_connection_details,
    ssh_connection_details=_vcu_ssh_connection_details,
)

_vcu_k8s = K8S(
    namespace="tl2078", master_node=_vcu_master_node
)  # namespace under [VCU_NAMESPACE] in kuafu-vcu_config.ini

# cloud deployment configuration fo VCU
_vcu_k8s_cloud_deployment = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    networks=[_vcu_intnet_1],
    vnfs=[_vcu_cnf_1],
    cloud_hosting=_vcu_k8s,
)

# VDU configuration for deployment, currently not used
_vdu_cnf_0 = DeploymentVnfStack(
    name="vdu2078",  # chart_name under [VDU_CONFIG_INFO] in kuafu-vdu_config.ini
    yaml_file=os.path.join(_cfg_dir, "DEP/gnbs_0/vDU_0/DU_cnf_values-override.yaml"),
)

# VDU internal network configuration for deployment, currently not used
_vdu_intnet_0 = DeploymentNetworkStack(
    name=_vdu_cnf_0.name + "-prerequisite",
    yaml_file=os.path.join(_cfg_dir, "DEP/gnbs_0/vDU_0/DU_pvc_values-override.yaml"),
)

# ssh connection information of OE
_ssh_connection_details = SshServiceDetails(
    addr="10.64.165.242", username="core", password="system123"
)

# ssh connection information of OE, for cloudadmin user
_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.64.165.242", username="core", password="system123", port="22"
)

# master node information of OE
_master_node = MasterNode(
    k8s_connection_details=_k8s_connection_details,
    ssh_connection_details=_ssh_connection_details,
)

_k8s = K8S(namespace="tl2078", master_node=_master_node)

# VDU deployment configuration
_k8s_cloud_deployment = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    networks=[_vdu_intnet_0],
    vnfs=[_vdu_cnf_0],
    cloud_hosting=_k8s,
)

# VDU oam http connection
_vdu_oam_http_connection_details = HttpConnectionDetails(
    addr="10.64.166.18", port="443", username="Nemuadmin", password="Nokia@123"
)


_hbte_params = {
    "ip_addr": "10.71.209.38",
    "port": 5000,
    "attenuation_port_numbers": [1, 2, 3, 4, 5, 6, 7, 8],
    "model": "HBTE-PA-8-8-4-127-0.5",
    "version": None,
}

_attenuator_5G = HBTE(**_hbte_params)


# RU configuration
_ru_1 = RU(
    ru_hw_group="RU_INT_ECPRI",
    serial_number="1M204202984",
    attenuation_ports=[
        _attenuator_5G.attenuator_ports[1],
        _attenuator_5G.attenuator_ports[2],
        _attenuator_5G.attenuator_ports[3],
        _attenuator_5G.attenuator_ports[4],
    ],
)

# PXE server info for FHGW deployment, currently not used
_pxe_server_ssh_info = SshServiceDetails(
    addr="10.71.223.254", username="ute", password="!Q2w3e4r5t6y7u"
)
_pxe_server = PxeServer(
    nfs_ip="10.71.223.254", ssh_connection_details=_pxe_server_ssh_info
)

# FHGW information
_fhgw_0 = FHGW(
    user_config_path=_cfg_dir,
    rus=[_ru_1],
    pxe_server=_pxe_server,
)

_fhgw_0.ip = "10.71.223.201"
_fhgw_0.username = "toor4nsn"
_fhgw_0.password = "Fhgw@nokia123"
_fhgw_0.version = "22R4"

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
_du_0 = VDU(
    cloud_deployment=_k8s_cloud_deployment,
    oam_http_connection_details=_vdu_oam_http_connection_details,
    fhgws=[_fhgw_0],
    instance_id=2078,
    global_bts_id=2078,
    # route vDU -> vCU F1-M interface, currently not used
    f1_m_ip_addr=NetworkAddress(
        v4="10.10.10.10",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.10.10.10", ip_prefix_length=28),
    ),
    # route vDU -> vCU F1-C interface, currently not used
    f1_c_ip_addr=NetworkAddress(
        v4="10.64.166.10",
        vlan_id=135,
        routing=RoutingInformation(gateway="10.64.166.9", ip_prefix_length=29),
    ),
    # route vDU -> vCU F1-U interface, currently not used
    f1_u_ip_addr=NetworkAddress(
        v4="10.64.166.11",
        vlan_id=135,
        routing=RoutingInformation(gateway="10.64.166.9", ip_prefix_length=29),
    ),
)

# mcc, mnc configuration
_realcore = RealCore(five_g=None, mcc="001", mnc="01", pdns=None)

# VCU global configuration
_cbts = CloudBts(
    dus=[_du_0],  # vdu related parameter
    cu=_cu,
    cloud_deployment=_vcu_k8s_cloud_deployment,
    instance_id="2078",
    global_bts_id="2078",
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
#_appserver_ssh = SshServiceDetails(
#   addr="10.57.162.3", username="mmw_sg3", password="test@123!", port="43055"
#)

_appserver_ssh = SshServiceDetails(
    addr="10.70.222.51", username="mmw_sg3", password="mm@3", port="43602"
)
#_appserver_ssh = SshServiceDetails(
#    addr="10.57.157.135", username="ute", password="iW_K#8.ute%A10h0m0ra", port="43055"
#)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.162.3",
    iperf_path="/usr/bin/iperf",
    port="43455",
)
_iperf_details_on_appserver2 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.70.222.51",
    iperf_path="/usr/bin/iperf",
    port="44055",
)
_appserver = AppServer(_iperf_details_on_appserver2)


_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.217.178", username="nokia5G", password="noki@123"
    ),
    serial_number="RFCT32AJNYX",
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
    gnbs=[_cbts],
    enbs=[_lte_real_enb],
    ues=[_android],
    tl_cloud_topology="CLOUD_5G_AIC_NCIR_NCIR_FHGW_AHCA",
    cloud_hostings=[_ncir],
    test_pcs=[_enb_test_pc],
    core=_realcore,
    appserver=_appserver,
    attenuators=[_attenuator_5G],
)
tl._trans_para = _trans_para
# only tl variable can be accessed by user
__all__ = ["tl"]
