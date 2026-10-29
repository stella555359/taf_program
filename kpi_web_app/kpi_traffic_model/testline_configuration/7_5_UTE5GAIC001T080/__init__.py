__maintainer__ = "Cao Liting"
__team__ = "I_MN_SRAN_ENG2_HZ_AIC_EXPLORER"
__email__ = "I_MN_SRAN_ENG2_HZ_AIC_EXPLORER@internal.nsn.com"
__owner_email__ = "liting.cao@nokia_sbell.com"

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
from taf.config.testline.attenuator import HBTE
from taf.config.testline.core import RealCore
from taf.config.testline.ue import Android, Qualcomm
from taf.config.testline.nms import Netact

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

# Testpc
# UTE IP address and User Name, Password
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.108.229.129", username="ute", password="ute"
    )
)

# VDU related NCIR controlNode
_control = ControlNode(
    # configuration for ssh connecting to OE
    default_ssh_connection_details=SshServiceDetails(
        addr="10.110.9.4", username="nruser3", password="Nokia@1234"
    ),
    # configuration for connection of open stack UI, default port is 5000
    open_stack_connection_details=OpenStackConnectionDetails(
        username="nruser3",
        password="Nokia@1234",
        ip_addr="10.110.9.4",
        tenant="cran3",
    ),
    # BMC configuration of OE
    bmc_connection_details=BmcConnectionDetails(
        addr="10.71.160.198", username="admin", password="Nokia*1234567890"
    ),
)
# configuration of VDU related NCIR
_ncir = NCIR(compute_nodes=[], control_nodes=[_control], version="ncir_19")

# CU configuration
_cu = CU(
    # CU web UI ip address, oam interface ip of oam vm
    backhaul_site_oam_ip=NetworkAddress(
        # v4="10.110.63.50"
        v6="2a00:8a00:8000:5801:0:19:0:b84"
    ),
    # VCU OAM ssh connection, oam interface ip of oam vm
    oam_ssh_connection_details=SshServiceDetails(
        addr="2a00:8a00:8000:5801:0:19:0:b84",
        username="serviceuser",
        password="Pl(FzaYj5~c5;q",
    ),
    # VCU OAM http connection, oam interface ip of oam vm
    oam_http_connection_details=HttpConnectionDetails(
        addr="2a00:8a00:8000:5801:0:19:0:b84",
        username="Nemuadmin",
        password="nemuuser",
        port="443",
    ),
    # route configuration for x2 link to ENB on VCU, v4 is network address of ENB x2 link
    x2c=NetworkAddress(
        v4="10.110.64.0",
        vlan_id=3116,
        routing=RoutingInformation(gateway="10.110.64.1", ip_prefix_length=27),
    ),
    # route configuration for x2 link to ENB on VCU, v4 is network address of ENB x2 link
    f1c=NetworkAddress(
        v4="10.110.64.128",
        vlan_id=3117,
        routing=RoutingInformation(gateway="10.110.64.129", ip_prefix_length=29),
    ),
    # route configuration for f1u link to VDU on VCU, v4 is network address of VDU f1u link
    f1u=NetworkAddress(
        v4="10.110.64.128",
        vlan_id=3117,
        routing=RoutingInformation(gateway="10.110.64.129", ip_prefix_length=29),
    ),
    # f1m=NetworkAddress(v6='2A00:6666:6000:607c::2222', vlan_id=None,
    #                    routing=RoutingInformation(gateway='2A00:6666:6000:607c::1111', ip_prefix_length=120)),
    # x2c=NetworkAddress(v6='2A00:7777:6000:607c::2222', vlan_id=None,
    #                    routing=RoutingInformation(gateway='2A00:7777:6000:607c::1111', ip_prefix_length=120)),
    # f1c=NetworkAddress(v6='2A00:8888:6000:607c::2222', vlan_id=None,
    #                    routing=RoutingInformation(gateway='2A00:8888:6000:607c::1111', ip_prefix_length=120)),
    # f1u=NetworkAddress(v6='2A00:9999:6000:607c::2222', vlan_id=None,
    #                    routing=RoutingInformation(gateway='2A00:9999:6000:607c::1111', ip_prefix_length=120)),
    tracing=None,
)

# enb
_hbte_params_1 = {
    "ip_addr": "10.97.122.45",
    "port": 5000,
    "attenuation_port_numbers": [7, 8],
    "model": "PA-16-2-4-127-0.5-B-S",
    "version": None,
}
_attenuator_4G = HBTE(**_hbte_params_1)

_ru_2 = RU(
    ru_hw_group="hw_group",
    attenuation_ports=[
        _attenuator_4G.attenuator_ports[7],
        _attenuator_4G.attenuator_ports[8],
    ],
)

_real_enb = RealEnb(oam_ip="10.97.122.4", instance_id="5461", rms=[_ru_2])

# test pc information of enb
_enb_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.108.229.129", username="ute", password="ute"
    ),
    connections=[_real_enb],
)

# flavor
flavor_env_files = [os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/5gbts_flavor.env")]

# ext_net
net_env_files = [os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/5gbts_ext_net.env")]

# heat parameters
vnf_env_files = [os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/5gbts_heat.env")]

_cbts_flavor = DeploymentFlavorStack(
    name="hgz-tl003_flavor",
    env_files=flavor_env_files,
    yaml_file=os.path.join(_cfg_dir, "5gbts_flavor.yaml"),
    default_vnf_prefix="hgz-tl003",
)

_cbts_net = DeploymentNetworkStack(
    name="EXT_NET",
    env_files=net_env_files,
    yaml_file=os.path.join(_cfg_dir, "5gbts_ext_net.yaml"),
)

_cbts_vnf = DeploymentVnfStack(
    name="HGZ-TL003-STACK",
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
    name="aic-vdu",
    yaml_file=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/one_click_ne_deploy.yaml"
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
    addr="10.71.173.190", username="cranuser1", password="systeM!23"
)
# ssh connection information of OE, for cloudadmin user
_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.71.173.190", username="core", password="system123", port="22"
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
    addr="2a00:8a00:8000:117:1:2:a47:ad92",
    port="443",
    username="Nemuadmin",
    password="nemuuser",
)


_hbte_params = {
    "ip_addr": "10.97.122.45",
    "port": 5000,
    "attenuation_port_numbers": [9, 10, 11, 12],
    "model": "PA-16-2-4-127-0.5-B-S",
    "version": None,
}
_attenuator_5G = HBTE(**_hbte_params)

# RU configuration
_ru_1 = RU(
    ru_hw_group="RU_INT_ECPRI",
    serial_number="AS202701778",
    attenuation_ports=[
        _attenuator_5G.attenuator_ports[9],
        _attenuator_5G.attenuator_ports[10],
        _attenuator_5G.attenuator_ports[11],
        _attenuator_5G.attenuator_ports[12],
    ],
)

# PXE server info for FHGW deployment
_pxe_server_ssh_info = SshServiceDetails(
    addr="10.71.160.199", username="root", password="root"
)
_pxe_server = PxeServer(
    nfs_ip="10.71.160.199", ssh_connection_details=_pxe_server_ssh_info
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
        v4="10.71.173.136",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.173.137", ip_prefix_length=24),
    ),
    # route configuration of f1c link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_c_ip_addr=NetworkAddress(
        v4="10.71.173.136",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.173.137", ip_prefix_length=24),
    ),
    # route configuration of f1u link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_u_ip_addr=NetworkAddress(
        v4="10.71.173.136",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.173.137", ip_prefix_length=24),
    ),
)

# mcc, mnc configuration
_realcore = RealCore(five_g=None, mcc="262", mnc="03", pdns=None)

_cbts = CloudBts(
    dus=[_vdu_1],  # vdu related parameter
    cu=_cu,
    cloud_deployment=_cloud_deployment,
    vnf_name="hgz-tl001",
    instance_id="5461",
    global_bts_id="5461",
)

#  iperf server info
_appserver_ssh = SshServiceDetails(
    addr="10.108.229.129", username="ute", password="QAZqaz123!@#"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.108.229.129",
)

_android1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.97.122.32", username="leiming", password="Nokia123!"
    ),
    serial_number="R3CR50K9TZP",  # Iris R5CN219G6VJ Liting R5CN3009D9L Xiuxiu R5CN301C1PL  R3CR50K9TZP
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "samsung"],
)

_android2 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.97.122.32", username="leiming", password="Nokia123!"
    ),
    serial_number="R3CR50K9TZP",  # Iris R5CN219G6VJ Liting R5CN3009D9L Xiuxiu R5CN301C1PL  R5CR411T8ED
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_UE", "REAL_ANDROID_UE_2", "samsung"],
)

_netact = Netact("10.97.122.45")
# Testline configuration
tl = TestLine(
    test_pc=_test_pc,
    ues=[_android1, _android2],
    gnbs=[_cbts],
    enbs=[_real_enb],
    tl_cloud_topology="CLOUD_5G_AIC_NCIR_NoneUE_NSA_1xvDU__OE19_FHGW_1xAHCA",
    cloud_hostings=[_ncir],
    test_pcs=[_enb_test_pc],
    attenuators=[_attenuator_5G, _attenuator_4G],
    core=_realcore,
    nms=_netact,
)

# only tl variable can be accessed by user
__all__ = ["tl"]
