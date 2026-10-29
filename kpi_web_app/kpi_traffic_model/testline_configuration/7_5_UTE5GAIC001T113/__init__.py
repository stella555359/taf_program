__maintainer__ = "Lin Yujia"
__team__ = "I_NSB_MN_5GSC_5GSW_ENG_AIC_SI_CN_2SISO_GMS <I_NSB_MN_5GSC_5GSW_ENG_AIC_SI_CN_2SISO@internal.nsn.com>"
__email__ = "I_NSB_MN_5GSC_5GSW_ENG_AIC_SI_CN_2SISO@internal.nsn.com"
__owner_email__ = "lionel.lin@nokia-sbell.com"

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
from taf.config.testline.cloud_hosting import MasterNode, K8S
from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.config.testline.radio import RU
from taf.config.testline.attenuator import HBTE
from taf.config.testline.ue import Android
from taf.config.testline.nom import NOM

##################  No USE  #################
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC
from taf.config.testline.cbam import Cbam
from taf.config.testline.nms import NMS
from taf.config.testline.attenuator import Attenuator
from taf.config.testline.attenuator import AttenuationPort

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# Testpc

# UTE IP address and User Name, Password
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.108.229.109", username="ute", password="ute"
    )
)

# VCU related NCIR controlNode
_control = ControlNode(
    # Configuration for SSH access
    default_ssh_connection_details=SshServiceDetails(
        addr="10.110.9.116", username="cranuser4", password="systeMi!2345"
    ),
    # Configuration for openstack connection
    open_stack_connection_details=OpenStackConnectionDetails(
        username="cranuser4",
        password="systeMi!2345",
        ip_addr="10.110.9.116",
        tenant="cran4",
    ),
    bmc_connection_details=BmcConnectionDetails(addr="", username="", password=""),
)

# configuration of VCU related NCIR/OSP
_ncir = NCIR(compute_nodes=[], control_nodes=[_control], version="ncir_19")


# CU0 configuration
_cu0 = CU(
    # CU web UI ip address, oam interface ip of oam vm
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.110.99.7", username="serviceuser", password="Pl(FzaYj5~c5;q"
    ),
    # VCU OAM ssh connection, oam interface ip of oam vm
    backhaul_site_oam_ip=NetworkAddress(v4="10.110.99.7"),
    # VCU OAM http connection, oam interface ip of oam vm
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.110.99.7", username="Nemuadmin", password="nemuuser", port="443"
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
        routing=RoutingInformation(gateway="10.110.101.129", ip_prefix_length=29),
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
# CU1 configuration
_cu1 = CU(
    # CU web UI ip address, oam interface ip of oam vm
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.110.99.26", username="serviceuser", password="Pl(FzaYj5~c5;q"
    ),
    # VCU OAM ssh connection, oam interface ip of oam vm
    backhaul_site_oam_ip=NetworkAddress(v4="10.110.123.11"),
    # VCU OAM http connection, oam interface ip of oam vm
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.110.99.26", username="Nemuadmin", password="nemuuser", port="443"
    ),
    # route configuration for x2c link to ENB, v4 is network address of ENB x2c link
    x2c=NetworkAddress(
        v4="10.0.0.0",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.110.124.1", ip_prefix_length=8),
    ),
    # route configuration for x2u link to ENB, v4 is network address of ENB x2u link
    x2u=NetworkAddress(
        v4="10.0.0.0",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.110.124.65", ip_prefix_length=8),
    ),
    # route configuration for f1c link to VDU on VCU, v4 is network address of VDU f1c link
    f1c=NetworkAddress(
        v4="10.71.162.0",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.110.124.97", ip_prefix_length=24),
    ),
    # route configuration for f1u link to VDU on VCU, v4 is network address of VDU f1u link
    f1u=NetworkAddress(
        v4="10.71.162.0",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.110.124.97", ip_prefix_length=24),
    ),
    tracing=None,
)
######################################## eNB start ######################################################
_common_unit_pdu = FACOM(addr="10.57.242.12", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_lmp_connection_0 = SshServiceDetails(
    addr="10.97.122.215", username="toor4nsn", password="oZPS0POrRieRtu"
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
    "ip_addr": "10.97.123.57",
    "port": 5000,
    "attenuation_port_numbers": [1, 4],
    "model": "PA-16-16-6-127-0.5-B-S",
    "version": None,
}
_attenuator_4G_1 = HBTE(**_hbte_params_4G_1)

_ru_4G_1 = RU(
    ru_hw_group="hw_group",
    attenuation_ports=[
        _attenuator_4G_1.attenuator_ports[1],
        _attenuator_4G_1.attenuator_ports[4],
    ],
)

_real_enb = RealEnb(airscale=_airscale_0, oam_ip="10.97.122.215", rms=[_ru_4G_1])

# test pc information of enb
_enb_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.108.229.109", username="ute", password="ute"
    ),
    connections=[_real_enb],
)

############################# eNB END ############################################################

# flavor of VCU
flavor_env_files = [os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/5gbts_flavor.env")]

# flavor of VCU
flavor_env_files_vdu2 = [os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_1/5gbts_flavor.env")]

# ext_net of VCU
net_env_files = [os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/5gbts_ext_net.env")]

# ext_net of VCU
net_env_files_vdu2 = [os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_1/5gbts_ext_net.env")]

# heat parameters
vnf_env_files = [os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/5gbts_heat.env")]

# heat parameters
vnf_env_files_vdu2 = [os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_1/5gbts_heat.env")]

_cbts_flavor = DeploymentFlavorStack(
    name="hgz-5223",
    env_files=flavor_env_files,
    yaml_file=os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/5gbts_flavor.yaml"),
    default_vnf_prefix="hgz-5223",
)

_cbts_flavor_vdu2 = DeploymentFlavorStack(
    name="hgz-5224",
    env_files=flavor_env_files_vdu2,
    yaml_file=os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_1/5gbts_flavor.yaml"),
    default_vnf_prefix="hgz-5224",
)

_cbts_net = DeploymentNetworkStack(
    name="hgz-5223",
    env_files=net_env_files,
    yaml_file=os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/5gbts_ext_net.yaml"),
)

_cbts_net_vdu2 = DeploymentNetworkStack(
    name="hgz-5224",
    env_files=net_env_files_vdu2,
    yaml_file=os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_1/5gbts_ext_net.yaml"),
)

_cbts_vnf = DeploymentVnfStack(
    name="hgz-5223",
    env_files=vnf_env_files,
    yaml_file=os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/5gbts_heat.yaml"),
)

_cbts_vnf_vdu2 = DeploymentVnfStack(
    name="hgz-5224",
    env_files=vnf_env_files_vdu2,
    yaml_file=os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_1/5gbts_heat.yaml"),
)

# cloud deployment configuration fo VCU
_cloud_deployment = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    flavors=[_cbts_flavor],
    networks=[_cbts_net],
    vnfs=[_cbts_vnf],
    cloud_hosting=_ncir,
)

# cloud deployment configuration fo VCU
_cloud_deployment_vdu2 = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    flavors=[_cbts_flavor_vdu2],
    networks=[_cbts_net_vdu2],
    vnfs=[_cbts_vnf_vdu2],
    cloud_hosting=_ncir,
)
######################### VDU-1 configuration for deployment##########################################
_vdu_vnf = DeploymentVnfStack(
    name="aic-vdu",
    yaml_file=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/aic_vdu_values_override_0.yaml"
    ),
)

# VDU internal network configuration for deployment
_vdu_intnet = DeploymentNetworkStack(
    name="aic-intnet",
    yaml_file=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/aic_intnet_values_override_0.yaml"
    ),
)

# ssh connection information of OE, for tenant user
_ssh_connection_details = SshServiceDetails(
    addr="10.71.162.66", username="cranuser1", password="systeM!23"
)

# ssh connection information of OE, for cloudadmin user
_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.71.162.66", username="cbis-admin", password="systeM!23", port="22"
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
    networks=[_vdu_intnet],
    vnfs=[_vdu_vnf],
    cloud_hosting=_k8s,
)

# VDU oam http connection
_vdu_oam_http_connection_details = HttpConnectionDetails(
    addr="10.71.162.82", port="443", username="Nemuadmin", password="nemuuser"
)

# attenuator info
_hbte_params_5G_1 = {
    "ip_addr": "10.97.123.57",
    "port": 5000,
    "attenuation_port_numbers": [2, 5, 8, 11],
    "model": "PA-16-16-6-127-0.5-B-S",
    "version": None,
}
_attenuator_5G_1 = HBTE(**_hbte_params_5G_1)

# RU configuration
_ru_1 = RU(
    ru_hw_group="hw_group",
    serial_number="1M211225074",
    attenuation_ports=[
        _attenuator_5G_1.attenuator_ports[2],
        _attenuator_5G_1.attenuator_ports[5],
        _attenuator_5G_1.attenuator_ports[8],
        _attenuator_5G_1.attenuator_ports[11],
    ],
)

# PXE server info for FHGW deployment
_pxe_server_ssh_info = SshServiceDetails(
    addr="10.97.120.175", username="root", password="nokia123"
)
_pxe_server = PxeServer(
    nfs_ip="10.97.120.175", ssh_connection_details=_pxe_server_ssh_info
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
    # route configuration of f1m link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_m_ip_addr=NetworkAddress(
        v4="10.110.100.0",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.162.9", ip_prefix_length=24),
    ),
    # route configuration of f1c link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_c_ip_addr=NetworkAddress(
        v4="10.110.100.0",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.162.9", ip_prefix_length=24),
    ),
    # route configuration of f1u link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_u_ip_addr=NetworkAddress(
        v4="10.110.100.0",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.162.9", ip_prefix_length=24),
    ),
)

# mcc, mnc configuration
_realcore = RealCore(five_g=None, mcc="262", mnc="03", pdns=None)

######################### VDU-2 configuration for deployment##########################################
_vdu_vnf_vdu2 = DeploymentVnfStack(
    name="aic-vdu2",
    yaml_file=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_1/vDU_1/aic_vdu_values_override_1.yaml"
    ),
)

# VDU internal network configuration for deployment
_vdu_intnet_vdu2 = DeploymentNetworkStack(
    name="aic-intnet2",
    yaml_file=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_1/vDU_1/aic_intnet_values_override_1.yaml"
    ),
)
# ssh connection information of OE, for tenant user
_ssh_connection_details_vdu2 = SshServiceDetails(
    addr="10.71.168.2", username="cranuser1", password="systeM!23"
)

# ssh connection information of OE, for cloudadmin user
_k8s_connection_details_vdu2 = K8SConnectionDetails(
    ip_addr="10.71.168.2", username="cloudadmin", password="system123", port="22"
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
    networks=[_vdu_intnet_vdu2],
    vnfs=[_vdu_vnf_vdu2],
    cloud_hosting=_k8s_vdu2,
)

# VDU oam http connection
_vdu_oam_http_connection_details_vdu2 = HttpConnectionDetails(
    addr="10.71.162.82", port="443", username="Nemuadmin", password="nemuuser"
)

# attenuator info
_hbte_params_5G_2 = {
    "ip_addr": "10.97.123.57",
    "port": 5000,
    "attenuation_port_numbers": [10, 11],
    "model": "PA-16-16-6-127-0.5-B-S",
    "version": None,
}
_attenuator_5G_2 = HBTE(**_hbte_params_5G_2)

# RU configuration

_ru_2 = RU(
    ru_hw_group="hw_group",
    serial_number="K9190632644",
    attenuation_ports=[
        _attenuator_5G_2.attenuator_ports[10],
        _attenuator_5G_2.attenuator_ports[11],
    ],
)


# FHGW information
_fhgw_2 = FHGW(
    user_config_path=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_1/vDU_1/FHGW_1/fhgw_user_config_1.yaml"
    ),
    rus=[_ru_2],
    pxe_server=_pxe_server,
)

# VDU global configuration
_vdu_2 = VDU(
    cloud_deployment=_k8s_cloud_deployment_vdu2,
    oam_http_connection_details=_vdu_oam_http_connection_details_vdu2,
    fhgws=[_fhgw_2],
    # route configuration of f1m link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_m_ip_addr=NetworkAddress(
        v4="10.110.124.0",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.162.73", ip_prefix_length=24),
    ),
    # route configuration of f1c link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_c_ip_addr=NetworkAddress(
        v4="10.110.124.0",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.162.73", ip_prefix_length=24),
    ),
    # route configuration of f1u link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_u_ip_addr=NetworkAddress(
        v4="10.110.124.0",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.162.73", ip_prefix_length=24),
    ),
)


# mcc, mnc configuration
_realcore = RealCore(five_g=None, mcc="262", mnc="03", pdns=None)

###################### VCU global configuration ##########
_cbts1 = CloudBts(
    dus=[_vdu_1],  # vdu related parameter
    cu=_cu0,
    cloud_deployment=_cloud_deployment,
    vnf_name="vnf_5223",
    instance_id="5223",
    global_bts_id="5223",
)
_cbts2 = CloudBts(
    dus=[_vdu_2],  # vdu related parameter
    cu=_cu1,
    cloud_deployment=_cloud_deployment_vdu2,
    vnf_name="vnf_5224",
    instance_id="5224",
    global_bts_id="5224",
)
# AppServer info
_app_server = SshServiceDetails(addr="10.108.229.109", username="ute", password="ute")

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_app_server,
    network_interface_address="10.108.229.109",
    iperf_path="/usr/bin/iperf",
)

# UE info
_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.97.123.13", username="aic", password="Nokia123!"
    ),
    serial_number="R3CR40TP9QF",
    iperf_details=_iperf,
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    capabilities=["REAL_UE", "REAL_ANDROID_UE"],
)

# Testline configuration
tl = TestLine(
    test_pc=_test_pc,
    ues=[_android],
    gnbs=[_cbts1],
    enbs=[_real_enb],
    attenuators=[_attenuator_5G_1],
    tl_cloud_topology="CLOUD_5G_AIC_NCIR_NCIR_FHGW_AHCA_Android",
    cloud_hostings=[_ncir],
    test_pcs=[_enb_test_pc],
    core=_realcore,
)

__all__ = ["tl"]
