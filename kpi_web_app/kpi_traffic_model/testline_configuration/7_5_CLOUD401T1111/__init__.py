__maintainer__ = "lisa.yang"
__team__ = "I_NSB_MN_5GSC_5GSW_ENG_AIC_SI_CN_PCI_GMS <I_NSB_MN_5GSC_5GSW_ENG_AIC_SI_CN_PCI@internal.nsn.com>"
__email__ = "I_NSB_MN_5GSC_5GSW_ENG_AIC_SI_CN_PCI@internal.nsn.com"
__owner_email__ = "lisa.yang@nokia-sbell.com"

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
from taf.config.testline.nms import Netact
from taf.config.testline.ue import Android
from taf.config.testline.appserver import AppServer
from taf.config.testline.attenuator import HBTE

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# Testpc
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.108.229.58", username="ute", password="A8CuY#6Vc^a0m4MmiT_2"
    )
)

# CU related OSP controlNode
_control = ControlNode(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.70.222.86", username="core", password="system123"
    ),
    open_stack_connection_details=OpenStackConnectionDetails(
        username="core",
        password="system123",
        ip_addr="10.70.222.86",
        tenant="cran2",
    ),
    bmc_connection_details=BmcConnectionDetails(addr="", username="", password=""),
)

# configuration of VDU related NCIR
_ncir = NCIR(compute_nodes=[], control_nodes=[_control], version="ncir_19")

# CU
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.57.170.85"
        # v6=''
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.170.85", username="robot", password="rastre1"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.170.85",
        username="Nemuadmin",
        password="nemuuser",
        port="443",
    ),
    # route configuration for x2 link to ENB on VCU, v4 is network address of ENB x2 link
    x2c=NetworkAddress(
        v4="10.57.170.67",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.57.170.65", ip_prefix_length=28),
    ),
    # route configuration for f1c link to VDU on VCU, v4 is network address of VDU f1c link
    f1c=NetworkAddress(
        v4="10.57.170.6",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.57.170.1", ip_prefix_length=27),
    ),
    # route configuration for f1u link to VDU on VCU, v4 is network address of VDU f1u link
    f1u=NetworkAddress(
        v4="10.57.170.5",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.57.170.1", ip_prefix_length=27),
    ),
    tracing=None,
)

# enb
_hbte_params_1 = {
    "ip_addr": "",
    "port": 5000,
    "attenuation_port_numbers": [1, 5],
    "model": "PA-16-16-6-127-0.5-B-S",
    "version": None,
}
_attenuator_4G = HBTE(**_hbte_params_1)

_ru_2 = RU(
    ru_hw_group="hw_group",
    attenuation_ports=[
        _attenuator_4G.attenuator_ports[1],
        _attenuator_4G.attenuator_ports[5],
    ],
)


_real_enb = RealEnb(oam_ip="10.97.122.238", instance_id="", rms=[_ru_2])

# test pc information of enb
_enb_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.108.229.58", username="ute", password="A8CuY#6Vc^a0m4MmiT_2"
    ),
    connections=[_real_enb],
)

# CloudBts
flavor_env_files = [os.path.join(_cfg_dir, "5gbts_flavor.env")]

net_env_files = [os.path.join(_cfg_dir, "5gbts_ext_net.env")]

vnf_env_files = [os.path.join(_cfg_dir, "5gbts_heat.env")]

_cbts_flavor = DeploymentFlavorStack(
    name="hgz-tl1111_flavor",
    env_files=flavor_env_files,
    yaml_file=os.path.join(_cfg_dir, "5gbts_flavor.yaml"),
    default_vnf_prefix="hgz-tl1111",
)

_cbts_net = DeploymentNetworkStack(
    name="EXT_NET",
    env_files=net_env_files,
    yaml_file=os.path.join(_cfg_dir, "5gbts_ext_net.yaml"),
)

_cbts_vnf = DeploymentVnfStack(
    name="HGZ-tl1111-STACK",
    env_files=vnf_env_files,
    yaml_file=os.path.join(_cfg_dir, "5gbts_heat.yaml"),
)

# cloud deployment configuration fo VCU
_cloud_deployment = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    flavors=[_cbts_flavor],
    networks=[_cbts_net],
    vnfs=[_cbts_vnf],
    cloud_hosting=_ncir,
)

# VDU configuration for deployment
_vdu_vnf_1 = DeploymentVnfStack(
    name="vdu-pod-int", yaml_file=os.path.join(_cfg_dir, "values-pod_tl1111.yaml")
)

# VDU internal network configuration for deployment
_vdu_intnet_1 = DeploymentNetworkStack(
    name="prerequisite",
    yaml_file=os.path.join(_cfg_dir, "values-intnet_tl1111.yaml"),
)

# ssh connection information of OE, for tenant user
_ssh_connection_details = SshServiceDetails(
    addr="10.71.169.194", username="cranuser1", password="systeM!23"
)

# ssh connection information of OE, for cloudadmin user
_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.71.169.254", username="core", password="system123", port="22"
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
    addr="10.71.169.210", port="443", username="Nemuadmin", password="nemuuser"
)

# RU configuration
_hbte_params = {
    "ip_addr": "",
    "port": 5000,
    "attenuation_port_numbers": [3, 7],
    "model": "PA-16-16-6-127-0.5-B-S",
    "version": None,
}
_attenuator_5G = HBTE(**_hbte_params)

# RU configuration
_ru_1 = RU(
    ru_hw_group="RU_INT_ECPRI",
    serial_number="",
    attenuation_ports=[
        _attenuator_5G.attenuator_ports[3],
        _attenuator_5G.attenuator_ports[7],
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
    user_config_path=os.path.join(_cfg_dir, "user_config_4.yaml"),
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
        v4="10.71.169.202",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.169.201", ip_prefix_length=29),
    ),
    # route configuration of f1c link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_c_ip_addr=NetworkAddress(
        v4="10.71.169.202",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.169.201", ip_prefix_length=29),
    ),
    # route configuration of f1u link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_u_ip_addr=NetworkAddress(
        v4="10.71.169.202",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.169.201", ip_prefix_length=29),
    ),
)

# mcc, mnc configuration
_realcore = RealCore(five_g=None, mcc="262", mnc="03", pdns=None)

#########appserver##########
_appserver_ssh = SshServiceDetails(
    addr="10.108.229.58", username="ute", password="A8CuY#6Vc^a0m4MmiT_2"
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.108.229.58",
    iperf_path="/usr/bin/iperf",
)

_appserver = AppServer(_iperf_details_on_appserver)

#########UE##########

_iperf_data_transfer = IperfDataTransferDetails(
    ssh_connection_details=SshServiceDetails(
        addr="10.108.229.58", username="ute", password="A8CuY#6Vc^a0m4MmiT_2"
    ),
    network_interface_address="10.108.229.58",
    iperf_path="/usr/bin/iperf",
)

_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.97.122.176", username="aic.qt", password="Nokia123!"
    ),
    serial_number="R5CN20TDAWA",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf_data_transfer,
    capabilities=["REAL_UE", "REAL_ANDROID_UE"],
)
_android.ue_type = "samsung"

# VCU global configuration
_cbts = CloudBts(
    dus=[_vdu_1],  # vdu related parameter
    cu=_cu,
    cloud_deployment=_cloud_deployment,
    vnf_name="hgz-tl1111",
    instance_id="1",
    global_bts_id="1",
)

_netact = Netact("10.97.119.159")
# Testline configuration
tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    enbs=[_real_enb],
    tl_cloud_topology="hgz-tl1111",
    cloud_hostings=[_ncir],
    test_pcs=[_enb_test_pc],
    attenuators=[_attenuator_5G, _attenuator_4G],
    ues=[_android],
    appserver=_appserver,
    core=_realcore,
    nms=_netact,
)

# only tl variable can be accessed by user
__all__ = ["tl"]
