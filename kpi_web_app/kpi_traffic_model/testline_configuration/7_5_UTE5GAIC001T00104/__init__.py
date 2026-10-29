# description INFO
__maintainer__ = "ella.fang"
__team__ = "OO_NSB_MN_RAN_PZ_2_HAZ_3_SG_10025988_GMS"
__email__ = "OO_NSB_MN_RAN_PZ_2_HAZ_3_SG_10025988_GMS@internal.nsn.com"
__owner_email__ = "ella.fang@nokia-sbell.com"


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
        addr="10.108.229.104", username="ute", password="QAZqaz123!@#"
    )
)

# VCU related OCP controlNode
_control = ControlNode(
    # Configuration for SSH access
    default_ssh_connection_details=SshServiceDetails(
        addr="10.71.172.242", username="cranuser2", password="systeM!23"
    ),
    # Configuration for openstack connection
    open_stack_connection_details=OpenStackConnectionDetails(
        username="cranuser2",
        password="systeM!23",
        ip_addr="10.71.172.242",
        tenant="cran2",
    ),
    bmc_connection_details=BmcConnectionDetails(addr="", username="", password=""),
)

# configuration of VCU related NCIR/OSP
_ocp = NCIR(
    compute_nodes=[],
    control_nodes=[_control],
    version="OSP_19",
)
# CU configuration
_cu = CU(
    # CU web UI ip address, oam interface ip of oam vm
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.172.242", username="cranuser2", password="systeM!23"
    ),
    # VCU OAM ssh connection, oam interface ip of oam vm
    backhaul_site_oam_ip=NetworkAddress(v4="10.110.177.200"),
    # VCU OAM http connection, oam interface ip of oam vm
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.172.211", username="Nemuadmin", password="nemuuser", port="443"
    ),

)


# cloud deployment configuration fo VCU
_cloud_deployment = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    cloud_hosting=_ocp,
)


_ssh_connection_details = SshServiceDetails(
    addr="10.71.172.242", username="cranuser1", password="systeM!23"
)

# ssh connection information of OE, for cloudadmin user
_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.71.172.242", username="core", password="system123", port="22"
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
    cloud_hosting=_vdu_k8s,
)


# VDU oam http connection
_vdu_oam_http_connection_details = HttpConnectionDetails(
    addr="10.71.172.210", port="443", username="Nemuadmin", password="nemuuser"
)

# attenuator info
_hbte_params_5G_1 = {
    "ip_addr": "10.97.122.162",
    "port": 5000,
    "attenuation_port_numbers": [2, 6],
    "model": "PA-16-16-6-127-0.5-B-S",
    "version": None,
}
_attenuator_5G_1 = HBTE(**_hbte_params_5G_1)

# RU configuration

_ru_0 = RU(
    ru_hw_group="hw_group",
    serial_number="1M202730249",
    attenuation_ports=[
        _attenuator_5G_1.attenuator_ports[2],
        _attenuator_5G_1.attenuator_ports[6],
    ],
)

# PXE server info for FHGW deployment

_pxe_server_ssh_info_0 = SshServiceDetails(
    addr="10.71.160.156", username="ute", password="Cdslabadmin@"
)


_pxe_server_0 = PxeServer(
    nfs_ip="10.108.204.30", ssh_connection_details=_pxe_server_ssh_info_0
)

# FHGW information

_fhgw_0 = FHGW(
    user_config_path=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/FHGW_0/user_config_0.yaml"
    ),
    rus=[_ru_0],
    pxe_server=_pxe_server_0,
)


# VDU global configuration
_vdu_1 = VDU(
    cloud_deployment=_k8s_cloud_deployment,
    oam_http_connection_details=_vdu_oam_http_connection_details,
    fhgws=[_fhgw_0],
)

###################### VCU global configuration ##########


# ssh connection information of OE, for tenant user
_vcu_ssh_connection_details = SshServiceDetails(
    addr="10.71.172.242", username="cranuser2", password="systeM!23"
)
# ssh connection information of OE, for root user
_vcu_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.71.172.242", username="cranuser2", password="systeM!23", port="22"
)

_vcu_master_node = MasterNode(
    k8s_connection_details=_vcu_k8s_connection_details,
    ssh_connection_details=_vcu_ssh_connection_details,
)

_vcu_k8s = K8S(namespace="cran2", master_node=_vcu_master_node)


_vcu_k8s_cloud_deployment = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    cloud_hosting=_vcu_k8s,
)


_cbts = CloudBts(
    dus=[_vdu_1],  # vdu related parameter
    cu=_cu,
    cloud_deployment=_vcu_k8s_cloud_deployment,
    vnf_name="11251",
    instance_id="11251",
    global_bts_id="11251",
)


# AppServer info iperf used
_app_server = SshServiceDetails(
    addr="10.108.229.162", username="ute", password="Fhgw@systeM!23"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_app_server,
    network_interface_address="10.108.229.162",
    iperf_path="/usr/bin/iperf",
)

# UE info
_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.97.123.18", username="aic", password="Nokia123!"
    ),
    serial_number="R5CR40LWZQA",
    iperf_details=_iperf,
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    capabilities=["REAL_SUMSANG_0", "REAL_ANDROID_UE"],
    service_call_detach=17,
    service_call_attach=17,
)


_nom_ssh_connection_edge0 = SshServiceDetails(
    addr="10.39.156.122", username="cloud-user"
)


# Testline configuration, tl is only variable which can be accessed by agent and test case
# you can access all parameters configured upper by tl parameter
tl = TestLine(
    test_pc=_test_pc,
    ues=[_android],
    gnbs=[_cbts],
    tl_cloud_topology="CLOUD_5G_AIC_OCP_ocp_AEQP",
    cloud_hostings=[_ocp],
)

# only tl variable can be accessed by user
__all__ = ["tl"]
                                    
