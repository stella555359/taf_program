# description INFO
__maintainer__ = "Yang Mengli"
__team__ = "I_NSB_MN_RAN_PZ_1_HAZ_3_GMS "
__email__ = "I_NSB_MN_RAN_PZ_1_HAZ_3@internal.nsn.com"
__owner_email__ = "mengli.yang@nokia-sbell.com"


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
from taf.config.testline.attenuator import HBTE,AttenuationPort,TopYoung 
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
        addr="10.69.53.184", username="ute", password="ute"
    )
)

# VCU related OCP controlNode
_control = ControlNode(
    # Configuration for SSH access
    default_ssh_connection_details=SshServiceDetails(
        addr="10.107.123.2", username="cranuser8", password="systeM!23"
    ),
    # Configuration for openstack connection
    open_stack_connection_details=OpenStackConnectionDetails(
        username="cranuser8",
        password="systeM!23",
        ip_addr="10.107.123.2",
        tenant="cran7",
    ),
    bmc_connection_details=BmcConnectionDetails(addr="", username="", password=""),
)

# VDU related NCIR controlNode
_control = ControlNode(
    # configuration for ssh connecting to OE
    default_ssh_connection_details=SshServiceDetails(
        addr="10.70.24.21", username="core", password="system123"
    ),
    # configuration for connection of open stack UI, default port is 5000
    open_stack_connection_details=OpenStackConnectionDetails(
        username="core",
        password="system123",
        ip_addr="10.70.24.21",
        tenant="cran1",
    ),
    # BMC configuration of OE
    bmc_connection_details=BmcConnectionDetails(
        addr="10.56.105.36", username="admin", password="CNnokia_123nokia"
    ),
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
        addr="10.107.123.2", username="cranuser8", password="systeM!23"
    ),
    # VCU OAM ssh connection, oam interface ip of oam vm
    backhaul_site_oam_ip=NetworkAddress(v4="10.107.160.6"),
    # VCU OAM http connection, oam interface ip of oam vm
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.107.160.6", username="Nemuadmin", password="Nokia@123", port="443"
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
        addr="10.107.123.2", username="cranuser9", password="systeM!23"
    ),
    # VCU OAM ssh connection, oam interface ip of oam vm
    backhaul_site_oam_ip=NetworkAddress(v4="10.107.160.8"),
    # VCU OAM http connection, oam interface ip of oam vm
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.107.160.8", username="Nemuadmin", password="Nokia@123", port="443"
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
    "ip_addr": "10.97.83.199",
    "port": 5000,
    "attenuation_port_numbers": [5, 6, 7, 8, 21, 22],
    "model": "PA-16-16-6-127-0.5-B-S",
    "version": None,
}
_attenuator_4G_1 = HBTE(**_hbte_params_4G_1)


_ru_4G_1 = RU(
    ru_hw_group="hw_group",
    attenuation_ports=[
        _attenuator_4G_1.attenuator_ports[5],
        _attenuator_4G_1.attenuator_ports[6],
        _attenuator_4G_1.attenuator_ports[7],
        _attenuator_4G_1.attenuator_ports[8],
        _attenuator_4G_1.attenuator_ports[21],
        _attenuator_4G_1.attenuator_ports[22],
    ],
)

# enb local IP
_real_enb = RealEnb(airscale=_airscale_0, oam_ip="10.97.122.215", rms=[_ru_4G_1])

# test pc information of enb UTE
_enb_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.108.229.66", username="ute", password="ute"
    ),
    connections=[_real_enb],
)

############################# eNB END ############################################################


######################### VDU-1 configuration for deployment##########################################

# ssh connection information of OE, for tenant user
_ssh_connection_details = SshServiceDetails(
    addr="10.56.10.146", username="core", password="system123"
)

# ssh connection information of OE, for cloudadmin user
_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.56.10.146", username="core", password="system123", port="22"
)


# master node information of OE
_master_node = MasterNode(
    k8s_connection_details=_k8s_connection_details,
    ssh_connection_details=_ssh_connection_details,
)

_vdu_k8s = K8S(namespace="cran1", master_node=_master_node)


# VDU internal network configuration for deployment
_vdu_intnet_1 = DeploymentNetworkStack(
    name="aic-intnet",
    yaml_file=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/aic_intnet_values_override_0.yaml"
    ),
)

# VDU configuration for deployment

_vdu_vnf_1 = DeploymentVnfStack(
    name="aic-vdu",
    yaml_file=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/aic_vdu_values_override_0.yaml"
    ),
)

# VDU deployment configuration
_k8s_cloud_deployment = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    networks=[_vdu_intnet_1],
    vnfs=[_vdu_vnf_1],
    cloud_hosting=_vdu_k8s,
)

# VDU oam http connection
_vdu_0_oam_http_connection_details = HttpConnectionDetails(
    addr="10.56.10.178", port="443", username="Nemuadmin", password="Nokia@123"
)

_vdu_1_oam_http_connection_details = HttpConnectionDetails(
    addr="10.56.10.226", port="443", username="Nemuadmin", password="Nokia@123"
)

_vdu_2_oam_http_connection_details = HttpConnectionDetails(
    addr="10.70.24.21", port="443", username="Nemuadmin", password="Nokia@123"
)

# attenuator info

_topyoung = TopYoung(ip_addr="10.97.83.199", port=3000, attenuation_port_numbers=list(range(1,33)), model="TAS16T16-51-120-1S-DES")

_attenuator_5G_1 = _topyoung

# RU configuration
_ru_1 = RU(
    ru_hw_group="hw_group",
    serial_number="1M220200001",
    attenuation_ports=[
        _attenuator_5G_1.attenuator_ports[1],
        _attenuator_5G_1.attenuator_ports[2],
        _attenuator_5G_1.attenuator_ports[3],
        _attenuator_5G_1.attenuator_ports[4],
        _attenuator_5G_1.attenuator_ports[5],
        _attenuator_5G_1.attenuator_ports[6],
        _attenuator_5G_1.attenuator_ports[7],
        _attenuator_5G_1.attenuator_ports[8],
        _attenuator_5G_1.attenuator_ports[9],
        _attenuator_5G_1.attenuator_ports[10],
        _attenuator_5G_1.attenuator_ports[11],
        _attenuator_5G_1.attenuator_ports[12],
        _attenuator_5G_1.attenuator_ports[13],
        _attenuator_5G_1.attenuator_ports[14],
        _attenuator_5G_1.attenuator_ports[15],
        _attenuator_5G_1.attenuator_ports[16],
        _attenuator_5G_1.attenuator_ports[17],
        _attenuator_5G_1.attenuator_ports[18],
        _attenuator_5G_1.attenuator_ports[19],
        _attenuator_5G_1.attenuator_ports[20],
        _attenuator_5G_1.attenuator_ports[21],
        _attenuator_5G_1.attenuator_ports[22],
        _attenuator_5G_1.attenuator_ports[23],
        _attenuator_5G_1.attenuator_ports[24],
        _attenuator_5G_1.attenuator_ports[25],
        _attenuator_5G_1.attenuator_ports[26],
        _attenuator_5G_1.attenuator_ports[27],
        _attenuator_5G_1.attenuator_ports[28],
        _attenuator_5G_1.attenuator_ports[29],
        _attenuator_5G_1.attenuator_ports[30],
        _attenuator_5G_1.attenuator_ports[31],
        _attenuator_5G_1.attenuator_ports[32],
    ],
)

_topyoung2 = TopYoung(ip_addr="10.97.83.200", port=3000, attenuation_port_numbers=list(range(1,33)), model="TAS16T16-51-120-1S-DES")

_attenuator_5G_2 = _topyoung2


# RU configuration
_ru_2 = RU(
    ru_hw_group="hw_group",
    serial_number="1M220200001",
    attenuation_ports=[
        _attenuator_5G_1.attenuator_ports[1],
        _attenuator_5G_1.attenuator_ports[2],
        _attenuator_5G_1.attenuator_ports[3],
        _attenuator_5G_1.attenuator_ports[4],
        _attenuator_5G_1.attenuator_ports[5],
        _attenuator_5G_1.attenuator_ports[6],
        _attenuator_5G_1.attenuator_ports[7],
        _attenuator_5G_1.attenuator_ports[8],
        _attenuator_5G_1.attenuator_ports[9],
        _attenuator_5G_1.attenuator_ports[10],
        _attenuator_5G_1.attenuator_ports[11],
        _attenuator_5G_1.attenuator_ports[12],
        _attenuator_5G_1.attenuator_ports[13],
        _attenuator_5G_1.attenuator_ports[14],
        _attenuator_5G_1.attenuator_ports[15],
        _attenuator_5G_1.attenuator_ports[16],
        _attenuator_5G_1.attenuator_ports[17],
        _attenuator_5G_1.attenuator_ports[18],
        _attenuator_5G_1.attenuator_ports[19],
        _attenuator_5G_1.attenuator_ports[20],
        _attenuator_5G_1.attenuator_ports[21],
        _attenuator_5G_1.attenuator_ports[22],
        _attenuator_5G_1.attenuator_ports[23],
        _attenuator_5G_1.attenuator_ports[24],
        _attenuator_5G_1.attenuator_ports[25],
        _attenuator_5G_1.attenuator_ports[26],
        _attenuator_5G_1.attenuator_ports[27],
        _attenuator_5G_1.attenuator_ports[28],
        _attenuator_5G_1.attenuator_ports[29],
        _attenuator_5G_1.attenuator_ports[30],
        _attenuator_5G_1.attenuator_ports[31],
        _attenuator_5G_1.attenuator_ports[32],
    ],
)



# PXE server info for FHGW deployment
_pxe_server_ssh_info = SshServiceDetails(
    addr="10.56.103.30", username="root", password="root"
)
_pxe_server = PxeServer(
    nfs_ip="10.56.103.30", ssh_connection_details=_pxe_server_ssh_info
)

# FHGW information
_fhgw_1 = FHGW(
    user_config_path=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/FHGW_0/user_config_0.yaml"
    ),
    rus=[_ru_1, _ru_2],
    pxe_server=_pxe_server,
)



# VDU global configuration
_vdu_0 = VDU(
    cloud_deployment=_k8s_cloud_deployment,
    oam_http_connection_details=_vdu_0_oam_http_connection_details,
    fhgws=[_fhgw_1],
    # route configuration of f1m link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_m_ip_addr=NetworkAddress(
        v4="10.56.10.170",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.56.10.169", ip_prefix_length=24),
    ),
    # route configuration of f1c link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_c_ip_addr=NetworkAddress(
        v4="10.56.10.170",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.56.10.169", ip_prefix_length=27),
    ),
    # route configuration of f1u link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_u_ip_addr=NetworkAddress(
        v4="10.56.10.171",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.56.10.169", ip_prefix_length=25),
    ),
)

_vdu_1 = VDU(
    cloud_deployment=_k8s_cloud_deployment,
    oam_http_connection_details=_vdu_1_oam_http_connection_details,
    fhgws=[_fhgw_1],
    # route configuration of f1m link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_m_ip_addr=NetworkAddress(
        v4="10.56.10.218",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.56.10.217", ip_prefix_length=24),
    ),
    # route configuration of f1c link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_c_ip_addr=NetworkAddress(
        v4="10.56.10.218",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.56.10.217", ip_prefix_length=27),
    ),
    # route configuration of f1u link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_u_ip_addr=NetworkAddress(
        v4="10.56.10.219",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.56.10.217", ip_prefix_length=25),
    ),
)


_vdu_2 = VDU(
    cloud_deployment=_k8s_cloud_deployment,
    oam_http_connection_details=_vdu_2_oam_http_connection_details,
    fhgws=[_fhgw_1],
    # route configuration of f1m link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_m_ip_addr=NetworkAddress(
        v4="10.70.24.10",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.70.24.9", ip_prefix_length=24),
    ),
    # route configuration of f1c link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_c_ip_addr=NetworkAddress(
        v4="10.70.24.10",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.70.24.9", ip_prefix_length=27),
    ),
    # route configuration of f1u link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_u_ip_addr=NetworkAddress(
        v4="10.70.24.11",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.70.24.9", ip_prefix_length=25),
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
    addr="10.107.123.2", username="cranuser8", password="systeM!23"
)
# ssh connection information of OE, for root user
_vcu_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.107.123.2", username="cranuser8", password="systeM!23", port="22"
)

_vcu_master_node = MasterNode(
    k8s_connection_details=_vcu_k8s_connection_details,
    ssh_connection_details=_vcu_ssh_connection_details,
)

_vcu_k8s = K8S(namespace="cran5", master_node=_vcu_master_node)


_vcu_k8s_cloud_deployment = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    networks=[_vcu_intnet_1],
    vnfs=[_vcu_vnf_1],
    cloud_hosting=_vcu_k8s,
)


_cbts = CloudBts(
    dus=[_vdu_0, _vdu_1],  # vdu related parameter
    cu=_cu,
    cloud_deployment=_vcu_k8s_cloud_deployment,
    vnf_name="vnf_11077",
    instance_id="11077",
    global_bts_id="11077",
)

# VCU1 ssh connection information of OE, for tenant user
_vcu1_ssh_connection_details = SshServiceDetails(
    addr="10.107.123.2", username="cranuser9", password="systeM!23"
)
# VCU1 ssh connection information of OE, for root user
_vcu1_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.107.123.2", username="cranuser9", password="systeM!23", port="22"
)

_vcu1_master_node = MasterNode(
    k8s_connection_details=_vcu1_k8s_connection_details,
    ssh_connection_details=_vcu1_ssh_connection_details,
)

_vcu1_k8s = K8S(namespace="cran11", master_node=_vcu1_master_node)

_vcu1_k8s_cloud_deployment = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    networks=[_vcu_intnet_1],
    vnfs=[_vcu_vnf_1],
    cloud_hosting=_vcu1_k8s,
)

_cbts1 = CloudBts(
    dus=[_vdu_2],  # vdu related parameter
    cu=_cu1,
    cloud_deployment=_vcu1_k8s_cloud_deployment,
    vnf_name="vnf_11078",
    instance_id="11078",
    global_bts_id="11078",
)

# AppServer info iperf used
_app_server = SshServiceDetails(addr="10.69.53.184", username="ute", password="ute")

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_app_server,
    network_interface_address="10.69.53.184",
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
)

huawei1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.97.83.195", username="PzHZ2", password="Nokia123!"
    ),
    serial_number="H4K5T20B26002536",
    server_dir="/cygdrive/c/pyro_server",
    python_path="/cygdrive/c/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["Commercial", "huawei1"],
)

_sigspark = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.97.83.204", username="spark", password="spark"
    ),
    serial_number="c802e804",
    server_dir="C:/Program Files (x86)/Spark1.1.2008.20/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="262033100009374",
    capabilities=["spark", "huawei1"],
)
_sigspark_1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.97.83.204", username="spark", password="spark"
    ),
    serial_number="928fd754",
    server_dir="C:/Program Files (x86)/Spark1.1.2008.20/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="262033100001254",
    capabilities=["spark", "huawei1"],
)
_sigspark_2 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.97.83.204", username="spark", password="spark"
    ),
    serial_number="d948fb75",
    server_dir="C:/Program Files (x86)/Spark1.1.2008.20/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="262033100010244",
    capabilities=["spark", "huawei1"],
)
_sigspark_3 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.97.83.204", username="spark", password="spark"
    ),
    serial_number="a744d188",
    server_dir="C:/Program Files (x86)/Spark1.1.2008.20/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="262033100009368",
    capabilities=["spark", "huawei1"],
)
_sigspark_4 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.97.83.204", username="spark", password="spark"
    ),
    serial_number="c77d2d92",
    server_dir="C:/Program Files (x86)/SSpark1.1.2008.20/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="460023100010282",
    capabilities=["spark", "huawei1"],
)
_sigspark_5 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.97.83.204", username="spark", password="spark"
    ),
    serial_number="2bac5719",
    server_dir="C:/Program Files (x86)/Spark1.1.2008.20/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="262033100001255",
    capabilities=["spark", "huawei1"],
)
_sigspark_6 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.97.83.204", username="spark", password="spark"
    ),
    serial_number="c09b9580",
    server_dir="C:/Program Files (x86)/Spark1.1.2008.20/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="262033100010269",
    capabilities=["spark", "huawei1"],
)
_sigspark_7 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.97.83.204", username="spark", password="spark"
    ),
    serial_number="65b5f02e",
    server_dir="C:/Program Files (x86)/Spark1.1.2008.20/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="262033100010275",
    capabilities=["spark", "huawei1"],
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
    ues=[huawei1,_sigspark,_sigspark_1,_sigspark_2,_sigspark_3,_sigspark_4,_sigspark_5,_sigspark_6,_sigspark_7],
    gnbs=[_cbts, _cbts1],
    enbs=[_real_enb],
    tl_cloud_topology="CLOUD_5G_AIC_SA_2XAndroid_2XvCU_3XvDU_OE20_2XFHGW_4XAEQY",
    cloud_hostings=[_ncir],
    test_pcs=[_enb_test_pc],
    attenuator=_attenuator_5G_1,
    attenuators=[_attenuator_5G_1, _attenuator_5G_2],
    core=_realcore,
)

# only tl variable can be accessed by user
__all__ = ["tl"]
