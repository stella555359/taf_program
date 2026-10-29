# description INFO
__maintainer__ = "luofei.tu"
__team__ = "OO_NSB_MN_RAN_PZ_2_HAZ_3_SG_10025988_GMS"
__email__ = "OO_NSB_MN_RAN_PZ_2_HAZ_3_SG_10025988_GMS@internal.nsn.com"
__owner_email__ = "luofei.tu@nokia-sbell.com"


# import library
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
from taf.config.testline.cloud_hosting import MasterNode, K8S, ComputeNode
from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.config.testline.radio import RU
from taf.config.testline.attenuator import HBTE
from taf.config.testline.ue import Android
from taf.config.testline.nom import NOM
from taf.config.testline.nms import Netact
from taf.config.testline.nms import NMS

##################  No USE  #################
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC
from taf.config.testline.cbam import Cbam
from taf.config.testline.nms import NMS
from taf.config.testline.attenuator import Attenuator
from taf.config.testline.attenuator import AttenuationPort

# get init file path
_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# Testpc  UTE

# UTE IP address and User Name, Password
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.108.229.67", username="ute", password="QAZqaz123!@#"
    )
)

# VCU related OCP controlNode
_control = ControlNode(
    # Configuration for SSH access
    default_ssh_connection_details=SshServiceDetails(
        addr="10.107.99.130", username="cranuser9", password="systeM!23"
    ),
    # Configuration for openstack connection
    open_stack_connection_details=OpenStackConnectionDetails(
        username="cranuser9",
        password="systeM!23",
        ip_addr="10.107.99.130",
        tenant="cran9",
    ),
    bmc_connection_details=BmcConnectionDetails(addr="", username="", password=""),
)


# configuration of VCU related NCIR/OSP
_ncir = NCIR(
    compute_nodes=[],
    # master_node="",
    control_nodes=[_control],
    version="OSP_19",
)

# CU configuration
_cu = CU(
    # CU web UI ip address, oam interface ip of oam vm
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.107.99.130", username="cranuser9", password="systeM!23"
    ),
    # VCU OAM ssh connection, oam interface ip of oam vm
    backhaul_site_oam_ip=NetworkAddress(v4="10.107.119.76"),
    # VCU OAM http connection, oam interface ip of oam vm
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.107.119.76", username="Nemuadmin", password="nemuuser", port="443"
    ),
)
_cu1 = CU(
    # CU web UI ip address, oam interface ip of oam vm
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.107.99.130", username="cranuser10", password="systeM!23"
    ),
    # VCU OAM ssh connection, oam interface ip of oam vm
    backhaul_site_oam_ip=NetworkAddress(v4="10.107.119.77"),
    # VCU OAM http connection, oam interface ip of oam vm
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.107.119.77", username="Nemuadmin", password="nemuuser", port="443"
    ),
)

# flavor of VCU
flavor_env_files = [os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/5gbts_flavor.env")]

# ext_net of VCU
net_env_files = [os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/5gbts_ext_net.env")]

# heat parameters
vnf_env_files = [os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/5gbts_heat.env")]

_cbts_flavor = DeploymentFlavorStack(
    name="hgz-5309",
    env_files=flavor_env_files,
    yaml_file=os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/5gbts_flavor.yaml"),
    default_vnf_prefix="hgz-5309",
)

_cbts_net = DeploymentNetworkStack(
    name="hgz-5309",
    env_files=net_env_files,
    yaml_file=os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/5gbts_ext_net.yaml"),
)

_cbts_vnf = DeploymentVnfStack(
    name="hgz-5309",
    env_files=vnf_env_files,
    yaml_file=os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/5gbts_heat.yaml"),
)

# cloud deployment configuration fo VCU
_cloud_deployment = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    flavors=[_cbts_flavor],
    networks=[_cbts_net],
    vnfs=[_cbts_vnf],
    cloud_hosting=_ncir,
)

######################### VDU-1 configuration for deployment##########################################
_vdu_vnf_1 = DeploymentVnfStack(
    name="aic-vdu-mvp",
    yaml_file=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/aic_vdu_values_override_0.yaml"
    ),
)

# VDU internal network configuration for deployment
_vdu_intnet_1 = DeploymentNetworkStack(
    name="aic-intnet-mvp",
    yaml_file=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/aic_intnet_values_override_0.yaml"
    ),
)

# ssh connection information of OE, for tenant user
_ssh_connection_details = SshServiceDetails(
    addr="10.71.162.126", username="cranuser1", password="systeM!23"
)

# ssh connection information of OE, for cloudadmin user
_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.71.162.126", username="core", password="system123", port="22"
)

# master node information of OE
_master_node = MasterNode(
    k8s_connection_details=_k8s_connection_details,
    ssh_connection_details=_ssh_connection_details,
)

_vdu_k8s = K8S(namespace="cran1", master_node=_master_node)

# VDU deployment configuration
_k8s_cloud_deployment = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    networks=[_vdu_intnet_1],
    vnfs=[_vdu_vnf_1],
    cloud_hosting=_vdu_k8s,
)

# VDU oam http connection
_vdu_oam_http_connection_details = HttpConnectionDetails(
    addr="10.71.162.82", port="443", username="Nemuadmin", password="nemuuser"
)

# attenuator info
_hbte_params_5G_1 = {
    "ip_addr": "10.97.123.102",
    "port": 5000,
    "attenuation_port_numbers": [2, 6],
    "model": "PA-16-16-6-127-0.5-B-S",
    "version": None,
}
_attenuator_5G_1 = HBTE(**_hbte_params_5G_1)

# RU configuration
_ru_1 = RU(
    ru_hw_group="hw_group",
    serial_number="1M212810185",
    attenuation_ports=[
        _attenuator_5G_1.attenuator_ports[2],
        _attenuator_5G_1.attenuator_ports[6],
    ],
)

# PXE server info for FHGW deployment
_pxe_server_ssh_info = SshServiceDetails(
    addr="10.71.160.28", username="root", password="root"
)
_pxe_server = PxeServer(
    nfs_ip="10.71.160.28", ssh_connection_details=_pxe_server_ssh_info
)

# FHGW information
_fhgw_1 = FHGW(
    user_config_path=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/FHGW_0/user_config_0.yaml"
    ),
    rus=[_ru_1],
    pxe_server=_pxe_server,
)


# VDU global configuration
_vdu_1 = VDU(
    cloud_deployment=_k8s_cloud_deployment,
    oam_http_connection_details=_vdu_oam_http_connection_details,
    fhgws=[_fhgw_1],
    # route configuration of f1m link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_m_ip_addr=NetworkAddress(
        v4="10.107.119.0",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.162.73", ip_prefix_length=24),
    ),
    # route configuration of f1c link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_c_ip_addr=NetworkAddress(
        v4="10.107.119.0",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.162.73", ip_prefix_length=27),
    ),
    # route configuration of f1u link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_u_ip_addr=NetworkAddress(
        v4="	10.107.90.0",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.162.73", ip_prefix_length=25),
    ),
)


# mcc, mnc configuration
_realcore = RealCore(five_g=None, mcc="262", mnc="03", pdns=None)

###################### VCU global configuration ##########
_vcu_intnet_1 = DeploymentNetworkStack(
    name="aic-vcu-network",
    yaml_file=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/aic_network_values_override_0.yaml"
    ),
)

_vcu_vnf_1 = DeploymentVnfStack(
    name="aic-vcu-cnf",
    yaml_file=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/aic_vcu_values_override_0.yaml"
    ),
)

# ssh connection information of OE, for tenant user
_vcu_ssh_connection_details = SshServiceDetails(
    addr="10.107.99.130", username="cranuser9", password="systeM!23"
)
# ssh connection information of OE, for root user
_vcu_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.107.99.130", username="cranuser9", password="systeM!23", port="22"
)

_vcu_master_node = MasterNode(
    k8s_connection_details=_vcu_k8s_connection_details,
    ssh_connection_details=_vcu_ssh_connection_details,
)

_vcu_k8s = K8S(namespace="cran9", master_node=_vcu_master_node)


_vcu_k8s_cloud_deployment = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    networks=[_vcu_intnet_1],
    vnfs=[_vcu_vnf_1],
    cloud_hosting=_vcu_k8s,
)

_cbts = CloudBts(
    dus=[_vdu_1],  # vdu related parameter
    cu=_cu,
    cloud_deployment=_vcu_k8s_cloud_deployment,
    vnf_name="vnf_5309",
    instance_id="5309",
    global_bts_id="5309",
)

# VCU1 ssh connection information of OE, for tenant user
_vcu1_ssh_connection_details = SshServiceDetails(
    addr="10.107.99.130", username="cranuser10", password="systeM!23"
)
# VCU1 ssh connection information of OE, for root user
_vcu1_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.107.99.130", username="cranuser10", password="systeM!23", port="22"
)

_vcu1_master_node = MasterNode(
    k8s_connection_details=_vcu1_k8s_connection_details,
    ssh_connection_details=_vcu1_ssh_connection_details,
)

_vcu1_k8s = K8S(namespace="cran10", master_node=_vcu1_master_node)

_vcu1_k8s_cloud_deployment = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    networks=[_vcu_intnet_1],
    vnfs=[_vcu_vnf_1],
    cloud_hosting=_vcu1_k8s,
)

_cbts1 = CloudBts(
    dus=[],  # vdu related parameter
    cu=_cu1,
    cloud_deployment=_vcu1_k8s_cloud_deployment,
    vnf_name="vnf_53091",
    instance_id="53091",
    global_bts_id="53091",
)

# AppServer info iperf used
_app_server = SshServiceDetails(addr="10.108.229.67", username="ute", password="ute")

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_app_server,
    network_interface_address="10.108.229.67",
    iperf_path="/usr/bin/iperf",
)

# UE info
_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.97.123.49", username="aic", password="Nokia123!"
    ),
    serial_number="R3CR40N8M9L",
    iperf_details=_iperf,
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    capabilities=["REAL_SUMSANG_0", "REAL_ANDROID_UE"],
    service_call_attach=17,
    service_call_detach=17,
)

_nom_ssh_connection_edge0 = SshServiceDetails(
    addr="10.39.156.122", username="cloud-user"
)


netact_id = {
    "clab3766": {
        "node_ip": "10.32.217.23",
        "user": "omc",
        "password": "omc",
        "url": "https://clab3766lbwas.netact.nsn-rdnet.net",
        "url_user": "omc",
        "url_password": "omc",
        "mr": "MRC-5G22R1VDU/MR-MRBTS-5326",
    },
    "clab3386": {
        "node_ip": "10.32.217.141",
        "user": "omc",
        "password": "omc",
        "url": "https://clab3386lbwas.netact.nsn-rdnet.net",
        "url_user": "omc",
        "url_password": "omc",
        "mr": "MRC-5G22R1VDU/MR-MRBTS-5326",
    },
}

_netact = Netact(netact_id)

# Testline configuration, tl is only variable which can be accessed by agent and test case
# you can access all parameters configured upper by tl parameter
tl = TestLine(
    test_pc=_test_pc,
    nms=_netact,
    ues=[_android],
    gnbs=[_cbts, _cbts1],
    tl_cloud_topology="CLOUD_5G_AIC_OCP_ocp_AEQP",
    core=_realcore,
)

_misc = {
    # 1-Use NOM config in __init__.py, 0-Use NOM config in global_variable.py.
    # If this key is not given, default value is 1
    "nom_config_source_from_init_py": "0",
    # 1-Use Netact config in __init__.py, 0-Use Netact config in global_variable.py.
    # If this key is not given, default value is 1
    "netact_config_source_from_init_py": "1",
}
tl._misc = _misc

# only tl variable can be accessed by user
__all__ = ["tl"]
