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
from taf.config.testline import (
    RealEnb,
    NetworkAddress,
    RoutingInformation,
    Airscale,
    CommonUnit,
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
from taf.config.testline.appserver import TafUeAppServer
from taf.config.testline import TafUeDataTransferProtocol
from taf.config.testline.pdn import PDNTafUeAndroidDetails
from taf.config.testline.ue import TafUeAndroid
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
        addr="10.108.229.64", username="ute", password="QAZqaz123!@#"
    )
)

# VCU related OCP controlNode
_control = ControlNode(
    # Configuration for SSH access
    default_ssh_connection_details=SshServiceDetails(
        addr="10.110.10.98", username="cranuser15", password="systeM!23"
    ),
    # Configuration for openstack connection
    open_stack_connection_details=OpenStackConnectionDetails(
        username="cranuser15",
        password="systeM!23",
        ip_addr="10.110.10.98",
        tenant="cran15",
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
        addr="10.110.10.98", username="cranuser15", password="systeM!23"
    ),
    # VCU OAM ssh connection, oam interface ip of oam vm
    backhaul_site_oam_ip=NetworkAddress(v4="10.110.177.210"),
    # VCU OAM http connection, oam interface ip of oam vm
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.110.177.210", username="Nemuadmin", password="nemuuser", port="443"
    ),
    # route INFO not need
    # # route configuration for x2c link to ENB, v4 is network address of ENB x2c link
    # x2c=NetworkAddress(
    #     v4="10.0.0.0",
    #     vlan_id=None,
    #     routing=RoutingInformation(gateway="10.107.86.113", ip_prefix_length=8),
    # ),
    # # route configuration for x2u link to ENB, v4 is network address of ENB x2u link
    # x2u=NetworkAddress(
    #     v4="10.0.0.0",
    #     vlan_id=None,
    #     routing=RoutingInformation(gateway="10.107.86.113", ip_prefix_length=8),
    # ),
    # # route configuration for f1c link to VDU on VCU, v4 is network address of VDU f1c link
    # f1c=NetworkAddress(
    #     v4="10.71.163.0",
    #     vlan_id=None,
    #     routing=RoutingInformation(gateway="10.107.86.97", ip_prefix_length=24),
    # ),
    # # route configuration for f1u link to VDU on VCU, v4 is network address of VDU f1u link
    # f1u=NetworkAddress(
    #     v4="10.71.163.0",
    #     vlan_id=None,
    #     routing=RoutingInformation(gateway="10.107.86.1", ip_prefix_length=24),
    # ),
    # tracing=None,
)

_cu1 = CU(
    # CU web UI ip address, oam interface ip of oam vm
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.110.10.98", username="cranuser2", password="systeM!23"
    ),
    # VCU OAM ssh connection, oam interface ip of oam vm
    backhaul_site_oam_ip=NetworkAddress(v4="10.110.113.135"),
    # VCU OAM http connection, oam interface ip of oam vm
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.110.113.135", username="Nemuadmin", password="nemuuser", port="443"
    ),
    # route INFO not need
    # # route configuration for x2c link to ENB, v4 is network address of ENB x2c link
    # x2c=NetworkAddress(
    #     v4="10.0.0.0",
    #     vlan_id=None,
    #     routing=RoutingInformation(gateway="10.107.86.113", ip_prefix_length=8),
    # ),
    # # route configuration for x2u link to ENB, v4 is network address of ENB x2u link
    # x2u=NetworkAddress(
    #     v4="10.0.0.0",
    #     vlan_id=None,
    #     routing=RoutingInformation(gateway="10.107.86.113", ip_prefix_length=8),
    # ),
    # # route configuration for f1c link to VDU on VCU, v4 is network address of VDU f1c link
    # f1c=NetworkAddress(
    #     v4="10.71.163.0",
    #     vlan_id=None,
    #     routing=RoutingInformation(gateway="10.107.86.97", ip_prefix_length=24),
    # ),
    # # route configuration for f1u link to VDU on VCU, v4 is network address of VDU f1u link
    # f1u=NetworkAddress(
    #     v4="10.71.163.0",
    #     vlan_id=None,
    #     routing=RoutingInformation(gateway="10.107.86.1", ip_prefix_length=24),
    # ),
    # tracing=None,
)
######################################## eNB start ######################################################
# _common_unit_pdu = FACOM(addr="10.57.242.12", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

# enb LMP ip
_lmp_connection_0 = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_0 = CapacityUnit(addr="ip")

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection_0,
    capacity_units=[_capacity_unit_0],
)


# airscale
_airscale_0 = Airscale(common_units=[_common_unit_0])


# enb related PA
_hbte_params_4G_1 = {
    "ip_addr": "10.97.123.102",
    "port": 5000,
    "attenuation_port_numbers": [1, 5],
    "model": "PA-16-16-6-127-0.5-B-S",
    "version": None,
}
_attenuator_4G_1 = HBTE(**_hbte_params_4G_1)


_ru_4G_1 = RU(
    ru_hw_group="hw_group",
    attenuation_ports=[
        _attenuator_4G_1.attenuator_ports[1],
        _attenuator_4G_1.attenuator_ports[5],
    ],
)

# enb local IP
_real_enb = RealEnb(airscale=_airscale_0, oam_ip="10.97.123.106", rms=[_ru_4G_1])

# test pc information of enb UTE
_enb_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.108.229.64", username="ute", password="QAZqaz123!@#"
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
    addr="10.71.163.61", username="cranuser1", password="systeM!23"
)

# ssh connection information of OE, for cloudadmin user
_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.71.163.61", username="core", password="system123", port="22"
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
    addr="10.71.163.18", port="443", username="Nemuadmin", password="nemuuser"
)

# attenuator info
_hbte_params_5G_1 = {
    "ip_addr": "10.97.123.119",
    "port": 5000,
    "attenuation_port_numbers": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    "model": "HBTE-PA-12-4-6-127-0.5",
    "version": None,
}
_attenuator_5G_1 = HBTE(**_hbte_params_5G_1)



# RU configuration
_ru_1 = RU(
    ru_hw_group="RU_INT_CPRI",
    serial_number="1M212901964",
    attenuation_ports=[
        _attenuator_5G_1.attenuator_ports[2],
        _attenuator_5G_1.attenuator_ports[5],
        _attenuator_5G_1.attenuator_ports[8],
        _attenuator_5G_1.attenuator_ports[11],
    ],
)

_ru_2 = RU(
    ru_hw_group="RU_INT_CPRI",
    serial_number="1M212901965",
    attenuation_ports=[
        _attenuator_5G_1.attenuator_ports[1],
        _attenuator_5G_1.attenuator_ports[4],
        _attenuator_5G_1.attenuator_ports[7],
        _attenuator_5G_1.attenuator_ports[10],
    ],
)

_ru_3 = RU(
    ru_hw_group="RU_INT_CPRI",
    serial_number="1M220614451",
    attenuation_ports=[
        _attenuator_5G_1.attenuator_ports[3],
        _attenuator_5G_1.attenuator_ports[6],
        _attenuator_5G_1.attenuator_ports[9],
        _attenuator_5G_1.attenuator_ports[12],
    ],
)

# PXE server info for FHGW deployment
_pxe_server_ssh_info = SshServiceDetails(
    addr="110.71.160.35", username="root", password="root"
)
_pxe_server = PxeServer(
    nfs_ip="10.71.160.35", ssh_connection_details=_pxe_server_ssh_info
)

# FHGW information
_fhgw_1 = FHGW(
    user_config_path=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/FHGW_0/user_config_0.yaml"
    ),
    rus=[_ru_1, _ru_2, _ru_3],
    pxe_server=_pxe_server,
)

_tools_repository = {
    "ip": "10.108.229.152",
    "username": "ute",
    "password": "QAZqaz123!@#",
    "repo_tool_folder": "/opt/tools/trans_test/",
    "repo_data_folder": "/opt/tools/trans_data/",
    "repo_simu4trs_folder": "/opt/tools/trans_simu4trs/",
}

_switch_1 = {
    "du_switch_ip": "10.108.215.13",
    "username": "cisco",
    "password": "cisco",
    "en_password": "",
    "port": "22",
    "prompt": "#",
}

_fhgw_misc = {
    "ruproxy_create_tool": "create_ruproxy_new.py",
    "ruproxy_delete_tool": "remove_ruproxy_new.py",
}

_trans_para = {
    "tools_repository": _tools_repository,
    "du_switch": [_switch_1],
    "fhgw_misc": _fhgw_misc,
}

# VDU global configuration
_vdu_1 = VDU(
    cloud_deployment=_k8s_cloud_deployment,
    oam_http_connection_details=_vdu_oam_http_connection_details,
    fhgws=[_fhgw_1],
    # route configuration of f1m link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_m_ip_addr=NetworkAddress(
        v4="10.110.100.0",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.163.73", ip_prefix_length=24),
    ),
    # route configuration of f1c link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_c_ip_addr=NetworkAddress(
        v4="10.110.100.0",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.163.73", ip_prefix_length=24),
    ),
    # route configuration of f1u link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_u_ip_addr=NetworkAddress(
        v4="10.110.100.0",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.163.73", ip_prefix_length=24),
    ),
    instance_id=50312,
    global_bts_id=50312,
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

_vcu_intnet = DeploymentNetworkStack(
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

_vcu_vnf = DeploymentVnfStack(
    name="aic-vcu-cnf",
    yaml_file=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/aic_vcu_values_override_0.yaml"
    ),
)

# ssh connection information of OE, for tenant user
_vcu_ssh_connection_details = SshServiceDetails(
    addr="10.110.10.98", username="cranuser15", password="systeM!23"
)

_vcu_ssh_connection_details1 = SshServiceDetails(
    addr="10.110.10.98", username="cranuser2", password="systeM!23"
)

# ssh connection information of OE, for root user
_vcu_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.110.10.98", username="cranuser15", password="systeM!23", port="22"
)

_vcu_k8s_connection_details1 = K8SConnectionDetails(
    ip_addr="10.110.10.98", username="cranuser2", password="systeM!23", port="22"
)

_vcu_master_node = MasterNode(
    k8s_connection_details=_vcu_k8s_connection_details,
    ssh_connection_details=_vcu_ssh_connection_details,
)

_vcu_master_node1 = MasterNode(
    k8s_connection_details=_vcu_k8s_connection_details1,
    ssh_connection_details=_vcu_ssh_connection_details1,
)

_vcu_k8s = K8S(namespace="cran15", master_node=_vcu_master_node)

_vcu_k8s1 = K8S(namespace="cran2", master_node=_vcu_master_node1)


_vcu_k8s_cloud_deployment = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    networks=[_vcu_intnet],
    vnfs=[_vcu_vnf],
    cloud_hosting=_vcu_k8s,
)

_vcu1_k8s_cloud_deployment = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    networks=[_vcu_intnet_1],
    vnfs=[_vcu_vnf_1],
    cloud_hosting=_vcu_k8s1,
)

_cbts1 = CloudBts(
    dus=[],  # vdu related parameter
    cu=_cu1,
    cloud_deployment=_vcu1_k8s_cloud_deployment,
    vnf_name="vnf_50311",
    instance_id="50311",
    global_bts_id="50311",
)

_cbts = CloudBts(
    dus=[_vdu_1],  # vdu related parameter
    cu=_cu,
    cloud_deployment=_vcu_k8s_cloud_deployment,
    vnf_name="vnf_5031",
    instance_id="5031",
    global_bts_id="5031",
)



# AppServer info iperf used
# AppServer info
_app_server_1 = TafUeAppServer(app_server_name="APP_1",
                               address="10.108.229.64",
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

_pdn1 = PDNTafUeAndroidDetails(entryName='stdata2',
                               apnName='stdata2',
                               apnType=['DEFAULT'])

# UE info
_android = TafUeAndroid(serial_number='R3CRA0GCLYX',
                          capabilities=['REAL_UE'],
                          ue_pc_address='10.97.123.99',
                          data_transfer=[_data_transfer_iperf],
                          ssh_connection_details=SshServiceDetails(addr='10.97.123.99',
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

_nom_ssh_connection_edge0 = SshServiceDetails(
    addr="10.39.156.122", username="cloud-user"
)


netact_id = {
    "clab2002" : {
        "netact_id": "clab2002",
        "node_ip": "10.82.47.15",
        "user": "omc",
        "password": "Medsql!_1893",
        "url": "https://srnclab2002lbwas.srnblr.nsn-rdnet.net",
        "url_user": "omc",
        "url_password": "Medsql!_1893",
        "mr": "netact_clab2003_mr_dict",
        "ca_file": "nom/clab33ca.pem",
        "ca_sn": "0x9B",
        "ca_id": "CACERT_R1",
        "configured_status": "available",
    },
    "clab1016": {
        "netact_id": "clab1016",
        "node_ip": "10.41.146.167",
        "user": "omc",
        "password": "Medsql!_1893",
        "url": "https://srnclab1016lbwas.srnblr.nsn-rdnet.net",
        "url_user": "omc",
        "url_password": "Medsql!_1893",
        "mr": "MRC-23R3VCU/MR-23R3VCU",
        "ca_file": "nom/clab33ca.pem",
        "ca_sn": "0x9B",
        "ca_id": "",
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
    "clabZheng3": {
        "node_ip": "10.110.188.146",
        "user": "omc",
        "password": "Nokia123!",
        "url": "https://zheng3lbwas.zheng3.srnhz.nsn-rdnet.net/",
        "url_user": "omc",
        "url_password": "Nokia123!",
        "mr": "MRC-5G22R1VDU/MR-MRBTS-5326",
    },
    "clab1060" : {
        "netact_id": "clab1060",
        "node_ip": "10.58.215.21",
        "user": "omc",
        "password": "Medsql!_1893",
        "url": "https://srnclab1060lbwas.srnblr.nsn-rdnet.net",
        "url_user": "omc",
        "url_password": "Medsql!_1893",
        "mr": "netact_clab2003_mr_dict",
        "ca_file": "nom/clab33ca.pem",
        "ca_sn": "0x9B",
        "ca_id": "CACERT_R1",
        "configured_status": "available",
    }
}

_netact = Netact(netact_id)

_nom1 = NOM(
    ssh_connections_info=[_nom_ssh_connection_edge0],
    https_main_info=HttpConnectionDetails(
        addr="https://neo-hosting-page.srncnms04.srnblr.nsn-rdnet.net/",
        username="cnms04",
        password="Qwer_1234",
    ),
    https_user_mgmt_info=HttpConnectionDetails(
        addr="https://user-mgmt.srncnms04.srnblr.nsn-rdnet.net"
    ),
    https_rest_info=HttpConnectionDetails(
        addr="https://apigw.srncnms04.srnblr.nsn-rdnet.net"
    ),
    neo_endpoints_ip="10.39.156.88",
)
_cnms = NMS(addr="10.39.156.122", nom=_nom1)
# Testline configuration, tl is only variable which can be accessed by agent and test case
# you can access all parameters configured upper by tl parameter
tl = TestLine(
    test_pc=_test_pc,
    nms=_cnms,
    attenuators=[_attenuator_5G_1],
    ues=[_android],
    gnbs=[_cbts],
    enbs=[_real_enb],
    tl_cloud_topology="CLOUD_5G_AIC_OCP_UE_SA_1xvDU__OE20_FHGW_AEQP",
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


# it's a WA, please see https://jira3.int.net.nokia.com/browse/TALIB-846,
# this jira has blocked a few transport TA cases design and debug
# one of other WA is declare a global python variable, 'TRANS_PARA = _trans_para'
# i don't know which WA is better, please give me suggestion if you like to change WA.
tl._trans_para = _trans_para



__all__ = ["tl"]
