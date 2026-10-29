# description INFO
__maintainer__ = "xianbiao.cheng"
__team__ = "OO_NSB_MN_RAN_PZ_2_HAZ_5_SG_10025988_GMS"
__email__ = "OO_NSB_MN_RAN_PZ_2_HAZ_5_SG_10025988_GMS@internal.nsn.com"
__owner_email__ = "xianbiao.cheng@nokia-sbell.com"


# import libraryA
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
from taf.config.testline.cloud_hosting import MasterNode, K8S, ComputeNode, HelmChart
from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.config.testline.radio import RU
from taf.config.testline.attenuator import HBTE
from taf.config.testline.ue import Android
from taf.config.testline.nom import NOM
from taf.config.testline.nms import Netact
from taf.config.testline.nms import NMS
from taf.config.testline.appserver import TafUeAppServer
from taf.config.testline import TafUeDataTransferProtocol
from taf.config.testline.pdn import PDNTafUeAndroidDetails
from taf.config.testline.ue import TafUeAndroid
from taf.config.testline.connection_details import IperfDataTransferDetails
from taf.config.testline.gnb.networkaddress import NetworkAddress

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
        addr="10.108.229.162", username="ute", password="QAZqaz123!@#"
    )
)

# VCU related OCP controlNode
_control = ControlNode(
    # Configuration for SSH access
    default_ssh_connection_details=SshServiceDetails(
        addr="10.110.10.98", username="cranuser5", password="systeM!23"
    ),
    # Configuration for openstack connection
    open_stack_connection_details=OpenStackConnectionDetails(
        username="cranuser5",
        password="systeM!23",
        ip_addr="10.110.10.98",
        tenant="cran5",
    ),
    bmc_connection_details=BmcConnectionDetails(addr="", username="", password=""),
)

workerbm_0 = ComputeNode(
    bmc_connection_details=BmcConnectionDetails(
        addr="10.107.97.162", username="cdslabuser", password="HZnokia123!"
    )
)

workerbm_1 = ComputeNode(
    bmc_connection_details=BmcConnectionDetails(
        addr="10.107.97.37", username="cdslabuser", password="HZnokia123!"
    )
)

workerbm_2 = ComputeNode(
    bmc_connection_details=BmcConnectionDetails(
        addr="10.107.97.43", username="cdslabuser", password="HZnokia123!"
    )
)

workerbm_3 = ComputeNode(
    bmc_connection_details=BmcConnectionDetails(
        addr="10.107.97.41", username="cdslabuser", password="HZnokia123!"
    )
)
workerbm_4 = ComputeNode(
    bmc_connection_details=BmcConnectionDetails(
        addr="10.107.97.52", username="cdslabuser", password="HZnokia123!"
    )
)

workerbm_5 = ComputeNode(
    bmc_connection_details=BmcConnectionDetails(
        addr="10.107.97.53", username="cdslabuser", password="HZnokia123!"
    )
)

workerbm_6 = ComputeNode(
    bmc_connection_details=BmcConnectionDetails(
        addr="10.107.97.54", username="cdslabuser", password="HZnokia123!"
    )
)

workerbm_7 = ComputeNode(
    bmc_connection_details=BmcConnectionDetails(
        addr="10.107.97.55", username="cdslabuser", password="HZnokia123!"
    )
)
workerbm_8 = ComputeNode(
    bmc_connection_details=BmcConnectionDetails(
        addr="10.107.97.56", username="cdslabuser", password="HZnokia123!"
    )
)

workerbm_9 = ComputeNode(
    bmc_connection_details=BmcConnectionDetails(
        addr="10.107.97.57", username="cdslabuser", password="HZnokia123!"
    )
)

workerbm_10 = ComputeNode(
    bmc_connection_details=BmcConnectionDetails(
        addr="10.107.97.58", username="cdslabuser", password="HZnokia123!"
    )
)

workerbm_11 = ComputeNode(
    bmc_connection_details=BmcConnectionDetails(
        addr="10.107.97.60", username="cdslabuser", password="HZnokia123!"
    )
)

workerbm_12 = ComputeNode(
    bmc_connection_details=BmcConnectionDetails(
        addr="10.107.97.61", username="cdslabuser", password="HZnokia123!"
    )
)
# configuration of VCU related NCIR/OSP
_ncir = NCIR(
    compute_nodes=[
        workerbm_0,
        workerbm_1,
        workerbm_2,
        workerbm_3,
        workerbm_4,
        workerbm_5,
        workerbm_6,
        workerbm_7,
        workerbm_8,
        workerbm_9,
        workerbm_10,
        workerbm_11,
        workerbm_12,
    ],
    # master_node="",
    control_nodes=[_control],
    version="OSP_19",
)
# CU configuration
_cu = CU(
    # CU web UI ip address, oam interface ip of oam vm
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.110.10.98", username="cranuser5", password="systeM!23"
    ),
    # VCU OAM ssh connection, oam interface ip of oam vm
    backhaul_site_oam_ip=NetworkAddress(v4="10.110.177.200"),
    # VCU OAM http connection, oam interface ip of oam vm
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.110.177.200", username="Nemuadmin", password="nemuuser", port="443"
    ),
)
######################################## eNB start ###########################################                                       ###########
# _common_unit_pdu = FACOM(addr="10.57.242.12", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

# enb LMP ip
_lmp_connection_0 = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_0 = CapacityUnit(addr="ip")

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection_0, capacity_units=[_capacity_unit_0]
)


# airscale
_airscale_0 = Airscale(common_units=[_common_unit_0])


# enb related PA
_hbte_params_4G_1 = {
    "ip_addr": "10.97.122.162",
    "port": 5000,
    "attenuation_port_numbers": [1, 5],
    "model": "PA-16-16-6-127-0.5-B-S",
    "version": None,
}
_attenuator_4G_1 = HBTE(**_hbte_params_4G_1)

_hbte_params_4G_2 = {
    "ip_addr": "10.97.122.162",
    "port": 5000,
    "attenuation_port_numbers": [8, 11],
    "model": "PA-16-16-6-127-0.5-B-S",
    "version": None,
}
_attenuator_4G_2 = HBTE(**_hbte_params_4G_2)

_ru_4G_1 = RU(
    ru_hw_group="hw_group",
    attenuation_ports=[
        _attenuator_4G_1.attenuator_ports[1],
        _attenuator_4G_1.attenuator_ports[5],
    ],
)

_ru_4G_2 = RU(
    ru_hw_group="hw_group",
    attenuation_ports=[
        _attenuator_4G_2.attenuator_ports[8],
        _attenuator_4G_2.attenuator_ports[11],
    ],
)

# enb local IP
_real_enb = RealEnb(
    airscale=_airscale_0, oam_ip="10.97.122.163", rms=[_ru_4G_1, _ru_4G_2]
)

# test pc information of enb UTE
_enb_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.108.229.162", username="ute", password="QAZqaz123!@#"
    ),
    connections=[_real_enb],
)

############################# eNB END ########################################################                                       ####

# flavor of VCU
flavor_env_files = [os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/5gbts_flavor.env")]

# ext_net of VCU
net_env_files = [os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/5gbts_ext_net.env")]

# heat parameters
vnf_env_files = [os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/5gbts_heat.env")]

_cbts_flavor = DeploymentFlavorStack(
    name="hgz-5031",
    env_files=flavor_env_files,
    yaml_file=os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/5gbts_flavor.yaml"),
    default_vnf_prefix="hgz-5031",
)

_cbts_net = DeploymentNetworkStack(
    name="hgz-5031",
    env_files=net_env_files,
    yaml_file=os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/5gbts_ext_net.yaml"),
)

_cbts_vnf = DeploymentVnfStack(
    name="hgz-5031",
    env_files=vnf_env_files,
    yaml_file=os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/5gbts_heat.yaml"),
)

# cloud deployment configuration fo VCU vRAN2.0
_cloud_deployment = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    flavors=[_cbts_flavor],
    networks=[_cbts_net],
    vnfs=[_cbts_vnf],
    cloud_hosting=_ncir,
)

######################### VDU-1 configuration for deployment##################################                                       ########
_vdu_vnf_1 = DeploymentVnfStack(
    name="aic-vdu-mvp",
    yaml_file=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/vDU_1/aic_vdu_values_override_0.yaml"
    ),
)

_vdu_vnf_0 = DeploymentVnfStack(
    name="aic-vdu-mvp",
    yaml_file=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/aic_vdu_values_override_0.yaml"
    ),
)

# VDU internal network configuration for deployment
_vdu_intnet_1 = DeploymentNetworkStack(
    name="aic-intnet-mvp",
    yaml_file=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/vDU_1/aic_intnet_values_override_0.yaml"
    ),
)

_vdu_intnet_0 = DeploymentNetworkStack(
    name="aic-intnet-mvp",
    yaml_file=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/aic_intnet_values_override_0.yaml"
    ),
)

# ssh connection information of OE, for tenant user
_ssh_connection_details_10950 = SshServiceDetails(
    addr="10.57.137.2", username="cranuser1", password="systeM!23"
)

# ssh connection information of OE, for cloudadmin user
_k8s_connection_details_10950 = K8SConnectionDetails(
    ip_addr="10.57.137.2", username="core", password="system123", port="22"
)

_ssh_connection_details = SshServiceDetails(
    addr="10.71.178.242", username="cranuser1", password="systeM!23"
)

# ssh connection information of OE, for cloudadmin user
_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.71.178.242", username="core", password="system123", port="22"
)

# master node information of OE
_master_node = MasterNode(
    k8s_connection_details=_k8s_connection_details,
    ssh_connection_details=_ssh_connection_details,
)

_master_node_10950 = MasterNode(
    k8s_connection_details=_k8s_connection_details_10950,
    ssh_connection_details=_ssh_connection_details_10950,
)

_vdu_k8s = K8S(namespace="cran1", master_node=_master_node)


_vdu_k8s_10950 = K8S(namespace="cran1", master_node=_master_node_10950)

_cluster_preparation_du_1 = HelmChart(
    name="preparation-vdu",
    yaml_file=os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/vdu_preparation_10950.yaml"),
)

_prerequisite_du_1 = HelmChart(
    name="prerequisite-vdu",
    yaml_file=os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/vdu_prerequisite_10950.yaml"),
)

_cnf_du_1 = HelmChart(
    name="cnf-vdu",
    yaml_file=os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/vdu_cnf_10950.yaml"),
)

# VDU deployment configuration
_k8s_cloud_deployment = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    networks=[_vdu_intnet_1],
    vnfs=[_vdu_vnf_1],
    cloud_hosting=_vdu_k8s,
)

_k8s_cloud_deployment_10950 = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    cluster_preparation=_cluster_preparation_du_1,
    prerequisite=_prerequisite_du_1,
    cnf=_cnf_du_1,
    cloud_hosting=_vdu_k8s_10950,    
)

# VDU oam http connection
_vdu_oam_http_connection_details = HttpConnectionDetails(
    addr="10.71.178.210", port="443", username="Nemuadmin", password="nemuuser"
)

_vdu_oam_http_connection_details_10950 = HttpConnectionDetails(
    addr="10.57.213.178", port="443", username="Nemuadmin", password="nemuuser"
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
_ru_1 = RU(
    ru_hw_group="hw_group",
    serial_number="1M194808590",
    attenuation_ports=[
        _attenuator_5G_1.attenuator_ports[2],
        _attenuator_5G_1.attenuator_ports[6],
    ],
)

_ru_0 = RU(
    ru_hw_group="hw_group",
    serial_number="1M211917778",
    attenuation_ports=[
        _attenuator_5G_1.attenuator_ports[2],
        _attenuator_5G_1.attenuator_ports[6],
    ],
)

# PXE server info for FHGW deployment
_pxe_server_ssh_info_1 = SshServiceDetails(
    addr="10.71.160.156", username="root", password="nokia123"
)
_pxe_server_ssh_info_0 = SshServiceDetails(
    addr="10.71.160.156", username="ute", password="Cdslabadmin@"
)
_pxe_server_1 = PxeServer(
    nfs_ip="110.71.160.156", ssh_connection_details=_pxe_server_ssh_info_1
)

_pxe_server_0 = PxeServer(
    nfs_ip="10.108.204.30", ssh_connection_details=_pxe_server_ssh_info_0
)

# FHGW information
_fhgw_1 = FHGW(
    user_config_path=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/vDU_1/FHGW_1/user_config_0.yaml"
    ),
    rus=[_ru_1],
    pxe_server=_pxe_server_1,
)

_fhgw_0 = FHGW(
    user_config_path=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/FHGW_0/user_config_0.yaml"
    ),
    rus=[_ru_0],
    pxe_server=_pxe_server_0,
)


# VDU global configuration
_vdu_1 = VDU(
    cloud_deployment=_k8s_cloud_deployment_10950,
    oam_http_connection_details=_vdu_oam_http_connection_details_10950,
    fhgws=[_fhgw_0],
    # route configuration of f1m link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_m_ip_addr=NetworkAddress(
        v4="10.108.207.24",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.108.207.25", ip_prefix_length=29),
    ),
    # route configuration of f1c link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_c_ip_addr=NetworkAddress(
        v4="10.108.207.24",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.108.207.25", ip_prefix_length=29),
    ),
    # route configuration of f1u link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_u_ip_addr=NetworkAddress(
        v4="10.108.207.24",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.108.207.25", ip_prefix_length=29),
    ),
)

# VDU global configuration
_vdu_2 = VDU(
    cloud_deployment=_k8s_cloud_deployment,
    oam_http_connection_details=_vdu_oam_http_connection_details,
    fhgws=[_fhgw_1],
    # route configuration of f1m link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_m_ip_addr=NetworkAddress(
        v4="10.71.178.200",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.178.201", ip_prefix_length=29),
    ),
    # route configuration of f1c link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_c_ip_addr=NetworkAddress(
        v4="10.71.178.200",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.178.201", ip_prefix_length=29),
    ),
    # route configuration of f1u link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_u_ip_addr=NetworkAddress(
        v4="10.71.178.200",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.178.201", ip_prefix_length=29),
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
    addr="10.110.10.98", username="cranuser5", password="systeM!23"
)
# ssh connection information of OE, for root user
_vcu_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.110.10.98", username="core", password="system123", port="22"
)

_vcu_master_node = MasterNode(
    k8s_connection_details=_vcu_k8s_connection_details,
    ssh_connection_details=_vcu_ssh_connection_details,
)

_vcu_k8s = K8S(namespace="cran5", master_node=_vcu_master_node)

_cluster_preparation_cu_1 = HelmChart(
    name="preparation-cu",
    yaml_file=os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/vcu_preparation_2003.yaml"),
)

_prerequisite_cu_1 = HelmChart(
    name="prerequisite-cu",
    yaml_file=os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/vcu_prerequisite_2003.yaml"),
)

_cnf_cu_1 = HelmChart(
    name="cnf-cu",
    yaml_file=os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/vcu_cnf_2003.yaml"),
)

_vcu_k8s_cloud_deployment = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    cluster_preparation=_cluster_preparation_cu_1,
    prerequisite=_prerequisite_cu_1,
    cnf=_cnf_cu_1,
    cloud_hosting=_vcu_k8s,
)


_cbts = CloudBts(
    dus=[_vdu_1],  # vdu related parameter
    cu=_cu,
    cloud_deployment=_vcu_k8s_cloud_deployment,
    vnf_name="vnf_2003",
    instance_id="2003",
    global_bts_id="2003",
)


# AppServer info iperf used
_app_server_1 = TafUeAppServer(app_server_name="APP_1",
                               address="10.108.229.162",
                               user="ute",
                               password="QAZqaz123!@#",
                               )

_data_transfer_iperf = TafUeDataTransferProtocol(protocol_name='iperf',
                                                 app_server=_app_server_1,
                                                 interval=1,
                                                 # binary_path='/data/data/com.nokia.android.application/',
                                                 interface_name='rmnet_data0',
                                                 server_close_delay=50,
                                                 version=2)

_pdn1 = PDNTafUeAndroidDetails(entryName='stdata1',
                               apnName='stdata1',
                               apnType=['DEFAULT'])

# _app_server = SshServiceDetails(
#     addr="10.108.229.162", username="ute", password="QAZqaz123!@#"
# )
#
# _iperf = IperfDataTransferDetails(
#     ssh_connection_details=_app_server,
#     network_interface_address="10.108.229.162",
# )

# UE info
_android = TafUeAndroid(serial_number='R5CNC097LMD',
                          capabilities=['REAL_UE'],
                          ue_pc_address='10.97.122.167',
                          data_transfer=[_data_transfer_iperf],
                          ssh_connection_details=SshServiceDetails(addr='10.97.122.167',
                                                                   username='aic',
                                                                   password='Nokia123!'),
                          # phone_number='+358480500013',
                          ue_pc_port='8080',
                          # imei='12345678912345',
                          # imsi='260123456789',
                          pdns=[_pdn1],
                          # qualcomm_prototype=True,
                          service_call_attach='17',
                          service_call_detach='17',
                          # network_mode_switch_method='ADB',
                          # airplane_mode_switcher_text='Airplane',
                          # airplane_mode_confirm_button_text='OK',
                          # path_to_network_mode_type='Mobile networks/Preferred network type',
                          # secret_code='*#0808#*',
                          # is_rooted='no',
                          )

# _android = Android(
#     ssh_connection_details=SshServiceDetails(
#         addr="10.97.122.167", username="aic", password="Nokia123!"
#     ),
#     serial_number="R5CR40LWZQA",
#     iperf_details=_iperf,
#     server_dir="/cygdrive/c/pyro_server",
#     python_path="C:/Python27/python.exe",
#     qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
#     diag_cfg_path="C:/pyro_server/DIAG.cfg",
#     capabilities=["REAL_SUMSANG_0", "REAL_ANDROID_UE"],
#     service_call_detach=17,
#     service_call_attach=17,
# )

_android1 = TafUeAndroid(serial_number='R3CRA0GCLYX',
                          capabilities=['REAL_UE'],
                          ue_pc_address='10.97.122.144',
                          data_transfer=[_data_transfer_iperf],
                          ssh_connection_details=SshServiceDetails(addr='10.97.122.144',
                                                                   username='aic',
                                                                   password='Nokia123!'),
                          # phone_number='+358480500013',
                          ue_pc_port='8080',
                          # imei='12345678912345',
                          # imsi='260123456789',
                          pdns=[_pdn1],
                          # qualcomm_prototype=True,
                          # network_mode_switch_method='ADB',
                          # airplane_mode_switcher_text='Airplane',
                          # airplane_mode_confirm_button_text='OK',
                          # path_to_network_mode_type='Mobile networks/Preferred network type',
                          # secret_code='*#0808#*',
                          # is_rooted='no',
                          )

# _android1 = Android(
#     ssh_connection_details=SshServiceDetails(
#         addr="10.97.122.144", username="aic", password="Nokia123!"
#     ),
#     serial_number="R3CRA0GCLYX",
#     iperf_details=_iperf,
#     server_dir="/cygdrive/c/pyro_server",
#     python_path="C:/Python27/python.exe",
#     qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
#     diag_cfg_path="C:/pyro_server/DIAG.cfg",
#     capabilities=["REAL_SUMSANG_0", "REAL_ANDROID_UE"],
#     service_call_detach=17,
#     service_call_attach=17,
# )

_nom_ssh_connection_edge0 = SshServiceDetails(
    addr="10.39.156.122", username="cloud-user"
)


netact_id = {
    "clab152": {
        "node_ip": "10.92.135.231",
        "user": "omc",
        "password": "omc",
        "url": "https://clab152lbwas.netact.nsn-rdnet.net",
        "url_user": "omc",
        "url_password": "omc",
        "mr": "MRC-5G22R1VDU/MR-MRBTS-5326",
    },
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
    ues=[_android,_android1],
    gnbs=[_cbts],
    enbs=[_real_enb],
    tl_cloud_topology="CLOUD_5G_AIC_OCP_ocp_AEQP",
    attenuators=[_attenuator_5G_1],
    cloud_hostings=[_ncir],
    test_pcs=[_enb_test_pc],
    core=_realcore,
)

_misc = {
    # 1-Use NOM config in __init__.py, 0-Use NOM config in global_variable.py.
    # If this key is not given, default value is 1
    "nom_config_source_from_init_py": "0",
    # 1-Use Netact config in __init__.py, 0-Use Netact config in global_variable.py.
    # If this key is not given, default value is 1
    "netact_config_source_from_init_py": "0",
}
tl._misc = _misc

# only tl variable can be accessed by user
__all__ = ["tl"]
                                    
