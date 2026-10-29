__maintainer__ = "Liu Jie"
__team__ = ""
__email__ = ""
__owner_email__ = "jie.8.liu@nokia-sbell.com"

import os

from taf.config.testline.cloud_hosting import (
    ControlNode,
    NCIR,
    CloudDeployment,
    DeploymentFlavorStack,
    DeploymentNetworkStack,
    DeploymentVnfStack,
    OSP,
)
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
)

from taf.config.testline.testpc import TestPc
from taf.config.testline.core import RealCore
from taf.config.testline.lab_infrastructure import PxeServer
from taf.config.testline.pdu import FACOM
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU
from taf.config.testline import RealEnb
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.cbam import Cbam
from taf.config.testline.nms import NMS
from taf.config.testline.nom import NOM
from taf.config.testline.attenuator import HBTE
from taf.config.testline.ue import Android
from taf.config.testline.connection_details import IperfDataTransferDetails
from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.config.testline.gnb.networkaddress import RoutingInformation
from taf.config.testline.connection_details import K8SConnectionDetails
from taf.config.testline.gnb.du import FHGW
from taf.config.testline.gnb.du import VDU
from taf.config.testline.cloud_hosting import MasterNode, K8S
from taf.config.testline.radio import RU


_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# Testpc

# UTE IP address and User Name, Password
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.108.229.68", username="ute", password="ute"
    )
)

# VCU related NCIR controlNode
_control = ControlNode(
    # Configuration for SSH access
    default_ssh_connection_details=SshServiceDetails(
        addr="10.110.9.116", username="cranuser23", password="systeM!23"
    ),
    # Configuration for openstack connection
    open_stack_connection_details=OpenStackConnectionDetails(
        username="cranuser23",
        password="systeM!23",
        ip_addr="10.110.9.116",
        tenant="cran23",
    ),
    bmc_connection_details=BmcConnectionDetails(addr="", username="", password=""),
)

# configuration of VCU related NCIR/OSP
_ncir = NCIR(compute_nodes=[], control_nodes=[_control], version="ncir_19")


######################################## eNB start ######################################################
_common_unit_pdu = FACOM(addr="10.57.242.12", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_lmp_connection_0 = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_0 = CapacityUnit(addr="ip")

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection_0,
    capacity_units=[_capacity_unit_0],
    pdu_port=_common_unit_pdu.pdu_ports[2],
)


# airscale
_airscale_0 = Airscale(common_units=[_common_unit_0])


# enb
_hbte_params_4G_1 = {
    "ip_addr": "10.97.123.8",
    "port": 5000,
    "attenuation_port_numbers": [7, 10],
    "model": "PA-16-16-6-127-0.5-B-S",
    "version": None,
}
_attenuator_4G_1 = HBTE(**_hbte_params_4G_1)

_hbte_params_4G_2 = {
    "ip_addr": "10.97.123.8",
    "port": 5000,
    "attenuation_port_numbers": [8, 11],
    "model": "PA-16-16-6-127-0.5-B-S",
    "version": None,
}
_attenuator_4G_2 = HBTE(**_hbte_params_4G_2)

_ru_4G_1 = RU(
    ru_hw_group="hw_group",
    attenuation_ports=[
        _attenuator_4G_1.attenuator_ports[7],
        _attenuator_4G_1.attenuator_ports[10],
    ],
)

_ru_4G_2 = RU(
    ru_hw_group="hw_group",
    attenuation_ports=[
        _attenuator_4G_2.attenuator_ports[8],
        _attenuator_4G_2.attenuator_ports[11],
    ],
)

_real_enb = RealEnb(
    airscale=_airscale_0, oam_ip="10.97.122.214", rms=[_ru_4G_1, _ru_4G_2]
)

# test pc information of enb
_enb_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.108.229.61", username="ute", password="ute"
    ),
    connections=[_real_enb],
)

############################# eNB END ############################################################

# flavor of VCU
flavor_env_files = [os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/5gbts_flavor.env")]

# ext_net of VCU
net_env_files = [os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/5gbts_ext_net.env")]

# heat parameters
vnf_env_files = [os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/5gbts_heat.env")]

_cbts_flavor = DeploymentFlavorStack(
    name="hgz-5211",
    env_files=flavor_env_files,
    yaml_file=os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/5gbts_flavor.yaml"),
    default_vnf_prefix="hgz-5211",
)

_cbts_net = DeploymentNetworkStack(
    name="hgz-5211",
    env_files=net_env_files,
    yaml_file=os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/5gbts_ext_net.yaml"),
)

_cbts_vnf = DeploymentVnfStack(
    name="hgz-5211",
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
    name="aic-vdu",
    yaml_file=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/aic_vdu_values_override_0.yaml"
    ),
)

# VDU internal network configuration for deployment
_vdu_intnet_1 = DeploymentNetworkStack(
    name="aic-intnet",
    yaml_file=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/aic_intnet_values_override_0.yaml"
    ),
)

# ssh connection information of OE, for tenant user
_ssh_connection_details = SshServiceDetails(
    addr="10.71.177.194", username="cranuser1", password="systeM!23"
)

# ssh connection information of OE, for cloudadmin user
_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.71.177.194", username="cloudadmin", password="system123", port="22"
)

# master node information of OE
_master_node = MasterNode(
    k8s_connection_details=_k8s_connection_details,
    ssh_connection_details=_ssh_connection_details,
)

_k8s = K8S(namespace="cran1", master_node=_master_node)

# VDU deployment configuration
_k8s_cloud_deployment = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    networks=[_vdu_intnet_1],
    vnfs=[_vdu_vnf_1],
    cloud_hosting=_k8s,
)

# VDU oam http connection
_vdu_oam_http_connection_details = HttpConnectionDetails(
    addr="10.71.177.210", port="443", username="Nemuadmin", password="nemuuser"
)

# attenuator info
_hbte_params_5G_1 = {
    "ip_addr": "10.97.123.8",
    "port": 5000,
    "attenuation_port_numbers": [1, 4],
    "model": "PA-16-16-6-127-0.5-B-S",
    "version": None,
}
_attenuator_5G_1 = HBTE(**_hbte_params_5G_1)

# RU configuration
_ru_1 = RU(
    ru_hw_group="hw_group",
    serial_number="AS195112278",
    attenuation_ports=[
        _attenuator_5G_1.attenuator_ports[1],
        _attenuator_5G_1.attenuator_ports[4],
    ],
)

# PXE server info for FHGW deployment
_pxe_server_ssh_info = SshServiceDetails(
    addr="10.97.122.231", username="root", password="nokia123"
)
_pxe_server = PxeServer(
    nfs_ip="10.97.122.231", ssh_connection_details=_pxe_server_ssh_info
)

# FHGW information
_fhgw_1 = FHGW(
    user_config_path=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/FHGW_0/fhgw_user_config_0.yaml"
    ),
    rus=[_ru_1],
    pxe_server=_pxe_server,
)

# VDU global configuration
_vdu_1 = VDU(
    cloud_deployment=_k8s_cloud_deployment,
    oam_http_connection_details=_vdu_oam_http_connection_details,
    fhgws=[_fhgw_1],
    # route configuration of f1c link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_c_ip_addr=NetworkAddress(
        v4="10.71.177.200",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.177.201", ip_prefix_length=24),
    ),
    # route configuration of f1u link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_u_ip_addr=NetworkAddress(
        v4="10.71.177.200",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.177.201", ip_prefix_length=24),
    ),
    # route configuration of f1/ link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_m_ip_addr=NetworkAddress(
        v4="10.71.177.208",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.177.209", ip_prefix_length=24),
    ),
)

######################### VDU-2 configuration for deployment##########################################
_vdu_vnf_2 = DeploymentVnfStack(
    name="aic-vdu",
    yaml_file=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/vDU_1/aic_vdu_values_override_1.yaml"
    ),
)

# VDU internal network configuration for deployment
_vdu_intnet_2 = DeploymentNetworkStack(
    name="aic-intnet",
    yaml_file=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/vDU_1/aic_intnet_values_override_1.yaml"
    ),
)

# ssh connection information of OE, for tenant user
_ssh_connection_details_vdu2 = SshServiceDetails(
    addr="10.71.168.130", username="cranuser1", password="systeM!23"
)

# ssh connection information of OE, for cloudadmin user
_k8s_connection_details_vdu2 = K8SConnectionDetails(
    ip_addr="10.71.168.130", username="cloudadmin", password="system123", port="22"
)

# master node information of OE
_master_node_vdu2 = MasterNode(
    k8s_connection_details=_k8s_connection_details_vdu2,
    ssh_connection_details=_ssh_connection_details_vdu2,
)

_k8s_vdu2 = K8S(namespace="cran1", master_node=_master_node_vdu2)

# VDU deployment configuration
_k8s_cloud_deployment_vdu2 = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    networks=[_vdu_intnet_2],
    vnfs=[_vdu_vnf_2],
    cloud_hosting=_k8s_vdu2,
)

# VDU oam http connection
_vdu_oam_http_connection_details_vdu2 = HttpConnectionDetails(
    addr="10.71.168.146", port="443", username="Nemuadmin", password="nemuuser"
)

# attenuator info
_hbte_params_5G_2 = {
    "ip_addr": "10.97.123.8",
    "port": 5000,
    "attenuation_port_numbers": [2, 5],
    "model": "PA-16-16-6-127-0.5-B-S",
    "version": None,
}
_attenuator_5G_2 = HBTE(**_hbte_params_5G_2)

# RU configuration

_ru_2 = RU(
    ru_hw_group="hw_group",
    serial_number="AS195112264",
    attenuation_ports=[
        _attenuator_5G_2.attenuator_ports[2],
        _attenuator_5G_2.attenuator_ports[5],
    ],
)

# FHGW information
_fhgw_2 = FHGW(
    user_config_path=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/vDU_1/FHGW_1/fhgw_user_config_1.yaml"
    ),
    rus=[_ru_2],
    pxe_server=_pxe_server,
)

# VDU global configuration
_vdu_2 = VDU(
    cloud_deployment=_k8s_cloud_deployment_vdu2,
    oam_http_connection_details=_vdu_oam_http_connection_details_vdu2,
    fhgws=[_fhgw_2],
    # route configuration of f1c link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_c_ip_addr=NetworkAddress(
        v4="10.110.100.0",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.168.137", ip_prefix_length=24),
    ),
    # route configuration of f1u link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_u_ip_addr=NetworkAddress(
        v4="10.110.100.0",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.168.137", ip_prefix_length=24),
    ),
)


# mcc, mnc configuration
_realcore = RealCore(five_g=None, mcc="262", mnc="03", pdns=None)

# cloud osp
_osp_control_0 = ControlNode(
    open_stack_connection_details=OpenStackConnectionDetails(
        ip_addr="10.107.8.117",
        username="5gBTS5user",
        tenant="5gBTS5",
        password="system123",
        port=13000,
        protocol="https",
    ),
    default_ssh_connection_details=SshServiceDetails(
        addr="10.107.8.117", username="stack", password="system123"
    ),
    bmc_connection_details=BmcConnectionDetails(
        addr="", username="admin", password="admin"
    ),
)


_osp_control_1 = ControlNode(
    open_stack_connection_details=OpenStackConnectionDetails(
        ip_addr="10.107.8.117",
        username="5gBTS4user",
        tenant="5gBTS4",
        password="system123",
        port=13000,
        protocol="https",
    ),
    default_ssh_connection_details=SshServiceDetails(
        addr="10.107.8.117", username="stack", password="system123"
    ),
    bmc_connection_details=BmcConnectionDetails(
        addr="", username="admin", password="admin"
    ),
)

_osp_0 = OSP(
    control_nodes=[_osp_control_0],
    version="19A",
    cloud_deployments=None,
    compute_nodes=[],
)

_osp_1 = OSP(
    control_nodes=[_osp_control_1],
    version="19A",
    cloud_deployments=None,
    compute_nodes=[],
)

# CloudBts
_flavor_env_files = [os.path.join(_cfg_dir, "5gbts_flavor_cit.env")]

_net_env_files = [os.path.join(_cfg_dir, "5gbts_ext_net.env")]

_vnf_env_files = [
    os.path.join(_cfg_dir, "5gbts_heat.env"),
    os.path.join(_cfg_dir, "5gbts_heat_cit.env"),
]
_cbts_flavor = DeploymentFlavorStack(
    name="flavor_3220-5gbts",
    env_files=_flavor_env_files,
    yaml_file=os.path.join(_cfg_dir, "5gbts_flavor.yaml"),
    default_vnf_prefix="flavor-3220",
)

_cbts_net = DeploymentNetworkStack(
    name="EXT_NET",
    env_files=_net_env_files,
    yaml_file=os.path.join(_cfg_dir, "5gbts_ext_net.yaml"),
)

_cbts_vnf = DeploymentVnfStack(
    name="vnf_3220-5gbts",
    env_files=_vnf_env_files,
    yaml_file=os.path.join(_cfg_dir, "5gbts_heat.yaml"),
)

_cloud_deployment_0 = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    flavors=[_cbts_flavor],
    networks=[_cbts_net],
    vnfs=[_cbts_vnf],
    cloud_hosting=_osp_0,
)

_cloud_deployment_1 = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    flavors=[_cbts_flavor],
    networks=[_cbts_net],
    vnfs=[_cbts_vnf],
    cloud_hosting=_osp_1,
)


###################### VCU global configuration ##########
# CU configuration
_cu1 = CU(
    # CU web UI ip address, oam interface ip of oam vm
    # oam_ssh_connection_details=SshServiceDetails(
    #     addr="2a00:8a00:8000:5002:0:f:11:17", username="serviceuser", password="Pl(FzaYj5~c5;q"
    # ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.107.169.80", username="serviceuser", password="Pl(FzaYj5~c5;q"
    ),
    # VCU OAM ssh connection, oam interface ip of oam vm
    backhaul_site_oam_ip=NetworkAddress(v4="10.110.99.27"),
    # VCU OAM http connection, oam interface ip of oam vm
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.107.169.82", username="Nemuadmin", password="nemuuser", port="443"
    ),
    # route configuration for x2c link to ENB, v4 is network address of ENB x2c link
    x2c=NetworkAddress(
        v4="10.0.0.0",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.110.101.1", ip_prefix_length=8),
    ),
    # route configuration for x2u link to ENB, v4 is network address of ENB x2u link
    x2u=NetworkAddress(
        v4="10.0.0.0",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.110.101.129", ip_prefix_length=8),
    ),
    # route configuration for f1c link to VDU on VCU, v4 is network address of VDU f1c link
    f1c=NetworkAddress(
        v4="10.71.0.0",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.110.100.1", ip_prefix_length=16),
    ),
    # route configuration for f1u link to VDU on VCU, v4 is network address of VDU f1u link
    f1u=NetworkAddress(
        v4="10.71.0.0",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.110.100.1", ip_prefix_length=16),
    ),
    tracing=None,
)

# CU configuration
_cu2 = CU(
    # CU web UI ip address, oam interface ip of oam vm
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.107.169.77", username="serviceuser", password="Pl(FzaYj5~c5;q"
    ),
    # VCU OAM ssh connection, oam interface ip of oam vm
    backhaul_site_oam_ip=NetworkAddress(v4="2a00:8a00:8000:5002:0:f:11:14"),
    # VCU OAM http connection, oam interface ip of oam vm
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.107.169.79", username="Nemuadmin", password="nemuuser", port="443"
    ),
    # route configuration for x2c link to ENB, v4 is network address of ENB x2c link
    x2c=NetworkAddress(
        v4="10.0.0.0",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.110.101.1", ip_prefix_length=8),
    ),
    # route configuration for x2u link to ENB, v4 is network address of ENB x2u link
    x2u=NetworkAddress(
        v4="10.0.0.0",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.110.101.129", ip_prefix_length=8),
    ),
    # route configuration for f1c link to VDU on VCU, v4 is network address of VDU f1c link
    f1c=NetworkAddress(
        v4="10.71.0.0",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.110.100.1", ip_prefix_length=16),
    ),
    # route configuration for f1u link to VDU on VCU, v4 is network address of VDU f1u link
    f1u=NetworkAddress(
        v4="10.71.0.0",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.110.100.1", ip_prefix_length=16),
    ),
    tracing=None,
)

_cbts1 = CloudBts(
    dus=[_vdu_1],
    cu=_cu1,
    cloud_deployment=_cloud_deployment_0,
    vnf_name="52131-5gbts",
    instance_id="52131",
)

_cbts2 = CloudBts(
    dus=[_vdu_1],
    cu=_cu2,
    cloud_deployment=_cloud_deployment_1,
    vnf_name="52131-5gbts",
    instance_id="52131",
)


# AppServer info
_app_server = SshServiceDetails(addr="10.108.229.61", username="ute", password="ute")

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_app_server,
    network_interface_address="10.108.229.61",
    iperf_path="/usr/bin/iperf",
)

# UE info
_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.97.123.40", username="miller.liu", password="nokiaE2E@"
    ),
    serial_number="90b918c0",
    iperf_details=_iperf,
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    capabilities=["REAL_UE", "REAL_ANDROID_UE"],
)

_nom_ssh_connection_edge0 = SshServiceDetails(
    addr="10.39.156.122", username="cloud-user"
)

_nom1 = NOM(
    ssh_connections_info=[_nom_ssh_connection_edge0],
    https_main_info=HttpConnectionDetails(
        addr="https://neo-hosting-page.srncnms04.srnblr.nsn-rdnet.net/",
        username="cnms01",
        password="Qwer_1234",
    ),
    neo_endpoints_ip="10.39.156.88",
)

_cnms = NMS(addr="10.39.156.122", nom=_nom1)

_cbam = Cbam(
    addr="10.110.95.10",
    client_id="rest_api",
    client_secret="17f1ecea-2d29-4663-b534-c22d94c6251f",
)

# Testline configuration
tl = TestLine(
    test_pc=_test_pc,
    nms=_cnms,
    cbam=_cbam,
    ues=[_android],
    gnbs=[_cbts1, _cbts2],
    enbs=[_real_enb],
    attenuators=[_attenuator_5G_1, _attenuator_5G_2],
    tl_cloud_topology="CLOUD_5G_AIC_NCIR_NCIR_FHGW_AHCA_Android",
    cloud_hostings=[_ncir],
    test_pcs=[_enb_test_pc],
    core=_realcore,
)

# only tl variable can be accessed by user
__all__ = ["tl"]
