__maintainer__ = "Xiao Tingting"
__team__ = "I_NSB_MN_5GSC_5GSW_ENG_AIC_SI_CN_2SISO_GMS <I_NSB_MN_5GSC_5GSW_ENG_AIC_SI_CN_2SISO@internal.nsn.com>"
__email__ = "I_NSB_MN_5GSC_5GSW_ENG_AIC_SI_CN_2SISO@internal.nsn.com"
__owner_email__ = "tingting.xiao@nokia-sbell.com"

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
)
from taf.config.testline.testpc import TestPc
from taf.config.testline import RealEnb, NetworkAddress, RoutingInformation
from taf.config.testline.core import RealCore
from taf.config.testline.lab_infrastructure import PxeServer
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU
from taf.config.testline import DU
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC
from taf.config.testline.cbam import Cbam
from taf.config.testline.nms import NMS
from taf.config.testline.nom import NOM
from taf.config.testline.attenuator import Attenuator
from taf.config.testline.attenuator import AttenuationPort
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
from taf.config.testline.nms import Netact


_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# Testpc

# UTE IP address and User Name, Password
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.108.229.164", username="ute", password="QAZqaz123!@#"
    )
)

# flavor of VCU
flavor_env_files = [os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/5gbts_flavor.env")]

# ext_net of VCU
net_env_files = [os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/5gbts_ext_net.env")]

# heat parameters
vnf_env_files = [os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/5gbts_heat.env")]

_cbts_net = DeploymentNetworkStack(
    name="hgz-10727",
    env_files=net_env_files,
    yaml_file=os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/5gbts_ext_net.yaml"),
)

_cbts_vnf = DeploymentVnfStack(
    name="hgz-10727",
    env_files=vnf_env_files,
    yaml_file=os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/5gbts_heat.yaml"),
)

# ssh connection information of OE, for tenant user
_vcu_ssh_connection_details = SshServiceDetails(
    addr="10.107.123.66", username="cranuser3", password="systeM!23"
)
# ssh connection information of OE, for root user
_vcu_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.107.123.66", username="cranuser3", password="systeM!23", port="22"
)

_vcu_master_node = MasterNode(
    k8s_connection_details=_vcu_k8s_connection_details,
    ssh_connection_details=_vcu_ssh_connection_details,
)

# cloud deployment configuration fo VCU
_vcu_k8s = K8S(namespace="cran3", master_node=_vcu_master_node)
_cloud_deployment = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    networks=[_cbts_net],
    vnfs=[_cbts_vnf],
    cloud_hosting=_vcu_k8s,
)


# CU configuration
_cu = CU(
    # CU web UI ip address, oam interface ip of oam vm
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.107.123.66", username="cranuser3", password="systeM!23"
    ),
    # VCU OAM ssh connection, oam interface ip of oam vm
    backhaul_site_oam_ip=NetworkAddress(v4="10.107.115.106"),
    # VCU OAM http connection, oam interface ip of oam vm
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.107.118.133", username="Nemuadmin", password="nemuuser", port="443"
    ),
    # route configuration for x2c link to ENB, v4 is network address of ENB x2c link
    x2c=NetworkAddress(
        v4="10.107.79.69",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.107.79.64", ip_prefix_length=27),
    ),
    # route configuration for x2u link to ENB, v4 is network address of ENB x2u link
    x2u=NetworkAddress(
        v4="10.107.116.6",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.107.116.0", ip_prefix_length=25),
    ),
    s1u=NetworkAddress(
        v4="10.107.116.134",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.107.116.128", ip_prefix_length=25),
    ),
    # route configuration for f1c link to VDU on VCU, v4 is network address of VDU f1c link
    f1c=NetworkAddress(
        v4="10.107.115.37",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.107.115.32", ip_prefix_length=27),
    ),
    # route configuration for f1u link to VDU on VCU, v4 is network address of VDU f1u link
    f1u=NetworkAddress(
        v4="10.107.115.134",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.107.115.128", ip_prefix_length=25),
    ),
    tracing=None,
)
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
        addr="10.108.229.164", username="ute", password="QAZqaz123!@#"
    ),
    connections=[_real_enb],
)

############################# eNB END ############################################################


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
    addr="10.71.169.50", username="cranuser1", password="systeM!23"
)

# ssh connection information of OE, for cloudadmin user
_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.71.169.50", username="core", password="system123", port="22"
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
    addr="10.71.169.18", port="443", username="Nemuadmin", password="nemuuser"
)

# attenuator info
_hbte_params_5G_1 = {
    "ip_addr": "10.97.123.5",
    "port": 5000,
    "attenuation_port_numbers": [3, 7],
    "model": "PA-16-16-6-127-0.5-B-S",
    "version": None,
}
_attenuator_5G_1 = HBTE(**_hbte_params_5G_1)

# RU configuration
_ru_1 = RU(
    ru_hw_group="hw_group",
    serial_number="AS195112278",
    attenuation_ports=[
        _attenuator_5G_1.attenuator_ports[3],
        _attenuator_5G_1.attenuator_ports[7],
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
    f1_m_ip_addr=NetworkAddress(
        v4="10.110.100.0",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.168.9", ip_prefix_length=24),
    ),
    # route configuration of f1c link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_c_ip_addr=NetworkAddress(
        v4="10.110.100.0",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.168.9", ip_prefix_length=24),
    ),
    # route configuration of f1u link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_u_ip_addr=NetworkAddress(
        v4="10.110.100.0",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.168.9", ip_prefix_length=24),
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
_ssh_connection_details_2 = SshServiceDetails(
    addr="10.69.54.114", username="cranuser1", password="systeM!23"
)

# ssh connection information of OE, for cloudadmin user
_k8s_connection_details_2 = K8SConnectionDetails(
    ip_addr="10.69.54.114", username="core", password="system123", port="22"
)

# master node information of OE
_master_node_2 = MasterNode(
    k8s_connection_details=_k8s_connection_details_2,
    ssh_connection_details=_ssh_connection_details_2,
)

_k8s_2 = K8S(namespace="cran1", master_node=_master_node_2)

# VDU deployment configuration
_k8s_cloud_deployment_2 = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    networks=[_vdu_intnet_2],
    vnfs=[_vdu_vnf_2],
    cloud_hosting=_k8s_2,
)

# VDU oam http connection
_vdu_oam_http_connection_details_2 = HttpConnectionDetails(
    addr="10.69.54.146", port="443", username="Nemuadmin", password="nemuuser"
)

# attenuator info
_hbte_params_5G_2 = {
    "ip_addr": "10.97.123.9",
    "port": 5000,
    "attenuation_port_numbers": [13, 14],
    "model": "PA-16-16-6-127-0.5-B-S",
    "version": None,
}
_attenuator_5G_2 = HBTE(**_hbte_params_5G_2)

# RU configuration

_ru_2 = RU(
    ru_hw_group="hw_group",
    serial_number="AS195112264",
    attenuation_ports=[
        _attenuator_5G_2.attenuator_ports[13],
        _attenuator_5G_2.attenuator_ports[14],
    ],
)

# FHGW information
_fhgw_2 = FHGW(
    user_config_path=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/vDU_1/FHGW_0/fhgw_user_config_0.yaml"
    ),
    rus=[_ru_2],
    pxe_server=_pxe_server,
)

# VDU global configuration
_vdu_2 = VDU(
    cloud_deployment=_k8s_cloud_deployment_2,
    oam_http_connection_details=_vdu_oam_http_connection_details_2,
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

###################### VCU global configuration ##########
_cbts = CloudBts(
    dus=[_vdu_1,_vdu_2],  # vdu related parameter[_vdu_1, _vdu_2]
    cu=_cu,
    cloud_deployment=_cloud_deployment,
    vnf_name="vnf_10727",
    instance_id="10727",
    global_bts_id="10727",
)

# AppServer info
_app_server = SshServiceDetails(
    addr="10.108.229.164", username="ute", password="QAZqaz123!@#"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_app_server,
    network_interface_address="10.108.229.164",
)

# UE info

_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.97.123.21", username="aic", password="Nokia123!"
    ),
    serial_number="R5CR11WMNPY",
    iperf_details=_iperf,
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    capabilities=["REAL_SUMSANG_1", "REAL_ANDROID_UE1"],
    #service_call_attach=17,      #Android11 no need these two parameters
    #service_call_detach=17,
)

_android_1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.97.123.4", username="miller.liu", password="nokiaE2E@"
    ),
    serial_number="R5CN20F65JM",
    iperf_details=_iperf,
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    capabilities=["REAL_SUMSANG_2", "REAL_ANDROID_UE2"],
)

_tools_repository = {
    "ip": "10.108.229.152",
    "username": "ute",
    "password": "ute",
    "repo_tool_folder": "/opt/tools/trans_test/",
    "repo_data_folder": "/opt/tools/trans_data/",
    "repo_simu4trs_folder": "/opt/tools/trans_simu4trs/",
}

_switch_1 = {
    "du_switch_ip": "10.108.212.106",
    "username": "chriscd",
    "password": "12345678",
    "en_password": "",
    "port": "23",
    "switch_interface": "1/1/1",
    "simu4DU_interface": "",
    "acl_number": "188",
    "du_vlan_id": "20",
    "du_vlan_masklen": "27",
    "du_vlan_gateway": "10.108.227.129",
    "du_vlan_mtu": "1500",
    "du_2nd_vlan_id": "100",
    "du_2nd_vlan_masklen": "27",
    "du_2nd_vlan_gateway": "10.108.227.192",
    "du_2nd_vlan_mtu": "1500",
    "du_2nd_vlan_ip": "10.108.227.220",
}

_fhgw_misc = {
    "ruproxy_create_tool": "create_ruproxy_new.py",
    "ruproxy_delete_tool": "removePod_new.py",
}

_trans_para = {
    "tools_repository": _tools_repository,
    "du_switch": [_switch_1],
    "fhgw_misc": _fhgw_misc,
}
netact_id = {
   "clab1016": {
       "netact_id": "clab1016",
       "node_ip": "10.41.146.167",
       "user": "omc",
       "password": "Medsql!_1893",
       "url": "https://srnclab1016lbwas.srnblr.nsn-rdnet.net",
       "url_user": "omc",
       "url_password": "Medsql!_1893",
       "mr": "MRC-AICTAFHGW/MR-10727",
       "ca_file": "nom/clab33ca.pem",
       "ca_sn": "0x9B",
       "ca_id": "",
   },
}

_netact = Netact(netact_id)

# Testline configuration
tl = TestLine(
    test_pc=_test_pc,
    # nms=_cnms,
    nms=_netact,
    ues=[_android],
    gnbs=[_cbts],
    enbs=[_real_enb],
    attenuators=[_attenuator_5G_1, _attenuator_5G_2],
    tl_cloud_topology="CLOUD_5G_AIC_OCP_OCP_FHGW_AHCA_Android",
    test_pcs=[_enb_test_pc],
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

tl._trans_para = _trans_para


__all__ = ["tl"]
