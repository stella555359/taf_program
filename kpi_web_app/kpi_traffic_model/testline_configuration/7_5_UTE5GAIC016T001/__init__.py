__maintainer__ = "Yang Mengli"
__team__ = "I_NSB_MN_RAN_PZ_1_HAZ_3_GMS "
__email__ = "I_NSB_MN_RAN_PZ_1_HAZ_3@internal.nsn.com"
__owner_email__ = "mengli.yang@nokia-sbell.com"

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
from taf.config.testline import DU
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC
from taf.config.testline.lab_infrastructure import PxeServer
from taf.config.testline.appserver import AppServer
from taf.config.testline.pdu import HBTE as PBHBTE
from taf.config.testline.attenuator import HBTE
from taf.config.testline.attenuator import AttenuationPort, TopYoung
from taf.config.testline.core import RealCore
from taf.config.testline.ue import Android, Qualcomm
from taf.config.testline.nms import NMS
from taf.config.testline.nom import NOM

######################VDU###########################
## following are VDU related class which defined
## in taf.config.testline
## you can uncomment them when new version of
## taf.config.testline merged
#######################VDU##########################
from taf.config.testline.connection_details import K8SConnectionDetails
from taf.config.testline.gnb.du import FHGW
from taf.config.testline.gnb.du import VDU
from taf.config.testline.cloud_hosting import MasterNode, K8S
from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.config.testline.radio import RU

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# VDU related NCIR controlNode
_control = ControlNode(
    # configuration for ssh connecting to OE
    default_ssh_connection_details=SshServiceDetails(
        addr="10.108.194.34", username="core", password="system123"
    ),
    # configuration for connection of open stack UI, default port is 5000
    open_stack_connection_details=OpenStackConnectionDetails(
        username="core",
        password="system123",
        ip_addr="10.108.194.34",
        tenant="cran1",
    ),
    # BMC configuration of OE
    bmc_connection_details=BmcConnectionDetails(
        addr="10.108.194.2", username="admin", password="cmb9.admin"
    ),
)

# configuration of VCU related NCIR/OSP
_ncir = NCIR(compute_nodes=[], control_nodes=[_control], version="OE20")

# CU configuration
_cu = CU(
    # CU web UI ip address, oam interface ip of oam vm
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.107.92.12"
        # v6='2a00:8a00:8000:136:10:57:159:1111'
    ),
    # VCU OAM ssh connection, oam interface ip of oam vm
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.107.92.12", username="Nemuadmin", password="nemuuser"
    ),
    # VCU OAM http connection, oam interface ip of oam vm
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.107.92.12", username="Nemuadmin", password="nemuuser", port="443"
    ),
    # route configuration for x2 link to ENB on VCU, v4 is network address of ENB x2 link
    x2c=NetworkAddress(
        v4="10.107.138.56",
        vlan_id=1004,
        routing=RoutingInformation(gateway="10.110.64.1", ip_prefix_length=25),
    ),
    x2u=NetworkAddress(
        v4="10.107.135.65",
        vlan_id=1005,
        routing=RoutingInformation(gateway="10.110.64.129", ip_prefix_length=25),
    ),
    # route configuration for f1c link to VDU on VCU, v4 is network address of VDU f1c link
    f1c=NetworkAddress(
        v4="10.107.110.101",
        vlan_id=1246,
        routing=RoutingInformation(gateway="10.107.110.97", ip_prefix_length=25),
    ),
    # route configuration for f1u link to VDU on VCU, v4 is network address of VDU f1u link
    f1u=NetworkAddress(
        v4="10.107.110.7",
        vlan_id=1242,
        routing=RoutingInformation(gateway="10.107.110.1", ip_prefix_length=25),
    ),
    s1u=NetworkAddress(
        v4="10.107.110.71",
        vlan_id=1241,
        routing=RoutingInformation(gateway="10.107.110.65", ip_prefix_length=25),
    ),
    tracing=None,
)

# RU PDU
_ru_pdu = PBHBTE(addr="10.97.65.5", port_numbers=[1, 2, 9, 10])

# enb

_attenuator_4G = TopYoung(
    ip_addr="10.69.85.33",
    port=3000,
    attenuation_port_numbers=[
        1,
        2,
    ],
    model="TAS16T16-51-120-1SDES",
)

_ru_2 = RU(
    ru_hw_group="hw_group",
    serial_number="1M220829958",
    attenuation_ports=[
        _attenuator_4G.attenuator_ports[1],
    ],
    pdu_port=_ru_pdu.pdu_ports[1],
)

_real_enb = RealEnb(oam_ip="10.97.122.3", instance_id="10766", rms=[_ru_2])

_vcu_intnet_1 = DeploymentNetworkStack(
    name="aic-vcu-intnet",
    yaml_file=os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/cnf_parameters.yaml"),
)

_vcu_vnf_1 = DeploymentVnfStack(
    name="aic-vcu",
    yaml_file=os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/cnf_parameters.yaml"),
)

# ssh connection information of OE, for tenant user
_vcu_ssh_connection_details = SshServiceDetails(
    addr="10.107.14.66", username="cranuser8", password="systeM!23"
)
# ssh connection information of OE, for root user
_vcu_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.107.14.66", username="cranuser8", password="systeM!23", port="22"
)

_vcu_master_node = MasterNode(
    k8s_connection_details=_vcu_k8s_connection_details,
    ssh_connection_details=_vcu_ssh_connection_details,
)
_vcu_k8s = K8S(namespace="cran8", master_node=_vcu_master_node)

_vcu_k8s_cloud_deployment = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    networks=[_vcu_intnet_1],
    vnfs=[_vcu_vnf_1],
    cloud_hosting=_vcu_k8s,
)

# VDU configuration for deployment

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
    addr="10.108.194.34", username="cranuser1", password="systeM!23"
)
# ssh connection information of OE, for cloudadmin user
_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.108.194.34", username="core", password="system123", port="22"
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
    addr="10.108.194.66", port="443", username="Nemuadmin", password="nemuuser"
)

# _attenuator_5G = HBTE(
#     ip_addr="10.97.65.198",
#     port=5000,
#     attenuation_port_numbers=[1, 2, 3, 4],
#     model="PA-16-16-6-127-0.5-B-S",
# )

_attenuator_5G = TopYoung(
    ip_addr="10.97.65.198",
    port=3000,
    attenuation_port_numbers=[1, 2, 3, 4],
    model="TAS16T8-51-120-1N-DES",
)

# RU configuration
_ru_1 = RU(
    ru_hw_group="RU_INT_ECPRI",
    serial_number="BL2316N44UK",
    attenuation_ports=[
        _attenuator_5G.attenuator_ports[1],
        _attenuator_5G.attenuator_ports[2],
        _attenuator_5G.attenuator_ports[3],
        _attenuator_5G.attenuator_ports[4],
    ],
    pdu_port=_ru_pdu.pdu_ports[9],
)

# PXE server info for FHGW deployment
_pxe_server_ssh_info = SshServiceDetails(
    addr="10.108.194.30", username="ute", password="N0kia@dmin"
)
_pxe_server = PxeServer(
    nfs_ip="10.108.194.30", ssh_connection_details=_pxe_server_ssh_info
)
# FHGW information
_fhgw_0 = FHGW(
    user_config_path=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/FHGW_0/fhgw_user_config_0.yaml"
    ),
    rus=[_ru_1],
    pxe_server=_pxe_server,
)

# VDU global configuration
_vdu_0 = VDU(
    cloud_deployment=_k8s_cloud_deployment,
    oam_http_connection_details=_vdu_oam_http_connection_details,
    fhgws=[_fhgw_0],
    # route configuration of f1m link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_m_ip_addr=NetworkAddress(
        v4="10.108.194.59",
        vlan_id=295,
        routing=RoutingInformation(gateway="192.168.254.34", ip_prefix_length=26),
    ),
    # route configuration of f1c link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_c_ip_addr=NetworkAddress(
        v4="10.108.194.58",
        vlan_id=115,
        routing=RoutingInformation(gateway="10.108.194.57", ip_prefix_length=29),
    ),
    # route configuration of f1u link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_u_ip_addr=NetworkAddress(
        v4="10.108.194.59",
        vlan_id=115,
        routing=RoutingInformation(gateway="10.108.194.57", ip_prefix_length=29),
    ),
    instance_id=10846,
)

# mcc, mnc configuration
_realcore = RealCore(five_g=None, mcc="262", mnc="03", pdns=None)

#  iperf server info
_appserver_ssh = SshServiceDetails(
    addr="10.108.229.191", username="ute", password="ute", port="54015"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.106.243.149",
    iperf_path="/data/data/com.nokia.android.application/",
    port="54015",
)

_appserver = AppServer(_iperf)

_android1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.97.65.199", username="Pz1", password="Nokia@2w3e4r5t6y7u"
    ),
    serial_number="R5CR20G4AVK",
    # 460
    server_dir="/cygdrive/c/pyro_server",
    python_path="/cygdrive/c/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["Commercial", "samsung"],
)

huawei1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.97.65.199", username="Pz1", password="Nokia@2w3e4r5t6y7u"
    ),
    serial_number="7TD0221525014906",
    server_dir="/cygdrive/c/pyro_server",
    python_path="/cygdrive/c/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["Commercial", "huawei1"],
)

huawei2 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.97.65.199", username="Pz1", password="Nokia@2w3e4r5t6y7u"
    ),
    serial_number="7TD5T21415000127",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["Commercial", "huawei2"],
)

oppo = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.97.65.199", username="Pz1", password="Nokia@2w3e4r5t6y7u"
    ),
    serial_number="DIJR4LLF6DBA7PSK",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["Commercial", "OPPO"],
)

Qualcomm = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.97.65.199", username="Pz1", password="Nokia@2w3e4r5t6y7u"
    ),
    serial_number="0123456789ABCDEF",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["Qualcomm", "REAL_ANDROID_UE"],
)

_nom_ssh_connection_edge0 = SshServiceDetails(
    addr="10.39.156.122", username="cloud-user"
)

_nom1 = NOM(
    ssh_connections_info=[_nom_ssh_connection_edge0],
    https_main_info=HttpConnectionDetails(
        addr="https://neo-hosting-page.srncnms04.srnblr.nsn-rdnet.net/",
        username="cnms04",
        password="Qwer_1234",
    ),
    https_user_mgmt_info=HttpConnectionDetails(
        addr="https://user-mgmt.srncnms04.srnblr.nsn-rdnet.net",
    ),
    https_rest_info=HttpConnectionDetails(
        addr="https://apigw.srncnms04.srnblr.nsn-rdnet.net",
    ),
    neo_endpoints_ip="10.39.156.88",
)

_cnms = NMS(addr="10.39.156.122", nom=_nom1)

_cbts_0 = CloudBts(
    dus=[_vdu_0],  # vdu related parameter
    cu=_cu,
    cloud_deployment=_vcu_k8s_cloud_deployment,
    instance_id="10846",
    global_bts_id="10846",
)

# test pc information of enb
_enb_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.108.229.121", username="ute", password="ute"
    ),
    connections=[_real_enb],
)

# Testpc
# UTE IP address and User Name, Password
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.97.65.243", username="ute", password="ute"
    ),
    connections=[_cbts_0]
)

# Testline configuration
tl = TestLine(
    test_pc=_test_pc,
    ues=[oppo, huawei1],
    gnbs=[_cbts_0],
    enbs=[_real_enb],
    tl_cloud_topology="CLOUD_5G_AIC_SA_2XAndroid_1XvCU_1XvDU_OE20_1XFHGW_2XAEQY_Common",
    cloud_hostings=[_ncir],
    test_pcs=[_enb_test_pc],
    # attenuators=[_attenuator_5G, _attenuator_4G],
    attenuator=_attenuator_5G,
    core=_realcore,
    nms=_cnms,
    appserver=_appserver,
)

# only tl variable can be accessed by user

__all__ = ["tl"]
