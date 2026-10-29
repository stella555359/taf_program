__maintainer__ = "Liu Chunxiu"
__team__ = "I_MN_SRAN_ENG2_HZ_AIC_EXPLORER"
__email__ = "I_MN_SRAN_ENG2_HZ_AIC_EXPLORER@internal.nsn.com"
__owner_email__ = "chunxiu.liu@nokia_sbell.com"

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
        addr="10.108.229.128", username="ute", password="ute"
    )
)

# VCU related NCIR controlNode
_control = ControlNode(
    # configuration for ssh connecting to OE
    default_ssh_connection_details=SshServiceDetails(
        addr="10.110.37.4", username="cranuser8", password="systeM!23"
    ),
    # configuration for connection of open stack UI, default port is 5000
    open_stack_connection_details=OpenStackConnectionDetails(
        username="cranuser8",
        password="systeM!23",
        ip_addr="10.110.37.4",
        tenant="cran9",
    ),
    # BMC configuration of OE
    bmc_connection_details=BmcConnectionDetails(
        addr="10.71.160.212", username="admin", password="Nokia*1234567890"
    ),
)
# configuration of VDU related NCIR
_ncir = NCIR(compute_nodes=[], control_nodes=[_control], version="ncir_19")

# CU configuration
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
_cu = CU(
    # CU web UI ip address, oam interface ip of oam vm
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.110.37.6"
        # v6=''
    ),
    # VCU OAM ssh connection, oam interface ip of oam vm
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.110.37.6", username="cranuser2", password="systeM!23"
    ),
    # VCU OAM http connection, oam interface ip of oam vm
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.110.74.102", username="Nemuadmin", password="nemuuser", port="443"
    ),
    # route configuration for x2 link to ENB on VCU, v4 is network address of ENB x2 link
    x2c=NetworkAddress(
        v4="10.110.64.0",
        vlan_id=3116,
        routing=RoutingInformation(gateway="10.110.64.1", ip_prefix_length=25),
    ),
    # route configuration,  for x2 link to ENB on VCUv4 is network address of ENB x2 link
    f1c=NetworkAddress(
        v4="10.110.64.128",
        vlan_id=3117,
        routing=RoutingInformation(gateway="10.110.64.129", ip_prefix_length=25),
    ),
    # route configuration for f1u link to VDU on VCU, v4 is network address of VDU f1u link
    f1u=NetworkAddress(
        v4="10.110.64.128",
        vlan_id=3117,
        routing=RoutingInformation(gateway="10.110.64.129", ip_prefix_length=25),
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
    "ip_addr": "10.97.122.41",
    "port": 5000,
    "attenuation_port_numbers": [5, 6],
    "model": "PA-16-2-6-127-0.5",
    "version": None,
}
_attenuator_4G = HBTE(**_hbte_params_1)

_ru_2 = RU(
    ru_hw_group="hw_group",
    attenuation_ports=[
        _attenuator_4G.attenuator_ports[5],
        _attenuator_4G.attenuator_ports[6],
    ],
)

_real_enb = RealEnb(oam_ip="10.97.122.11", instance_id="5465", rms=[_ru_2])

# test pc information of enb
_enb_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.108.229.128", username="ute", password="QAZqaz123!@#"
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
    yaml_file=os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/5gbts_flavor.yaml"),
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
    addr="10.71.174.114", username="cranuser1", password="systeM!23"
)

# ssh connection information of OE, for cloudadmin user
_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.71.174.114", username="core", password="system123", port="22"
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
    addr="10.71.174.82", port="443", username="Nemuadmin", password="nemuuser"
)


_hbte_params = {
    "ip_addr": "10.97.122.41",
    "port": 5000,
    "attenuation_port_numbers": [1, 2, 3, 4],
    "model": "PA-16-2-6-127-0.5",
    "version": None,
}
_attenuator_5G = HBTE(**_hbte_params)

# RU configuration
_ru_1 = RU(
    ru_hw_group="RU_INT_ECPRI",
    serial_number="K9190632303",
    attenuation_ports=[
        _attenuator_5G.attenuator_ports[1],
        _attenuator_5G.attenuator_ports[2],
        _attenuator_5G.attenuator_ports[3],
        _attenuator_5G.attenuator_ports[4],
    ],
)

# PXE server info for FHGW deployment
_pxe_server_ssh_info = SshServiceDetails(
    addr="10.71.160.213", username="root", password="nokia123"
)
_pxe_server = PxeServer(
    nfs_ip="10.71.160.213", ssh_connection_details=_pxe_server_ssh_info
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
        v4="10.110.63.0",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.174.73", ip_prefix_length=24),
    ),
    # route configuration of f1c link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_c_ip_addr=NetworkAddress(
        v4="10.110.63.0",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.174.73", ip_prefix_length=24),
    ),
    # route configuration of f1u link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_u_ip_addr=NetworkAddress(
        v4="10.110.63.0",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.174.73", ip_prefix_length=24),
    ),
    instance_id=5465,
)

# mcc, mnc configuration
_realcore = RealCore(five_g=None, mcc="262", mnc="03", pdns=None)

# ssh connection information of OE, for tenant user
_vcu_ssh_connection_details = SshServiceDetails(
    addr="10.110.37.6", username="cranuser2", password="systeM!23"
)
# ssh connection information of OE, for root user
_vcu_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.110.37.6", username="core", password="system123", port="22"
)

_vcu_master_node = MasterNode(
    k8s_connection_details=_vcu_k8s_connection_details,
    ssh_connection_details=_vcu_ssh_connection_details,
)

_vcu_k8s = K8S(namespace="cran2", master_node=_vcu_master_node)

_vcu_k8s_cloud_deployment = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    networks=[_vcu_intnet_1],
    vnfs=[_vcu_vnf_1],
    cloud_hosting=_vcu_k8s,
)

_cbts = CloudBts(
    dus=[_vdu_1],  # vdu related parameter
    cu=_cu,
    cloud_deployment=_vcu_k8s_cloud_deployment,
    vnf_name="cran1",
    instance_id="5465",
    global_bts_id="5465",
)

#  UE
# _appserver_ssh = SshServiceDetails(addr="10.108.229.127", username="ute", password="ute")
_appserver_ssh = SshServiceDetails(
    addr="10.108.229.128", username="ute", password="QAZqaz123!@#"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_name="rmnet_data0",
    network_interface_address="10.108.229.128",
)

_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.97.122.37", username="pci3", password="Nokia@123"
    ),
    serial_number="R3CR50K9TZP",  # R5CN20LYP5R R5CN20HRWLM R5CN212N3RX R3CR50K9TZP R3CR40TPM5K
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "samsung"],
    service_call_attach=17,
    service_call_detach=17,
)
_tools_repository = {
    "ip": "10.108.229.152",
    "username": "ute",
    "password": "QAZqaz123@#",
    "repo_tool_folder": "/opt/tools/trans_test/",
    "repo_data_folder": "/opt/tools/trans_data/",
    "repo_simu4trs_folder": "/opt/tools/trans_simu4trs/",
}

_switch_1 = {
    "du_switch_ip": "10.308.215.13",
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


_netact = Netact("10.97.122.47")
# Testline configuration
tl = TestLine(
    test_pc=_test_pc,
    ues=[_android],
    gnbs=[_cbts],
    enbs=[_real_enb],
    tl_cloud_topology="CLOUD_5G_AIC_OCP_RealUE_NSA_1xvDU__OE19_FHGW_1xAEQY",
    cloud_hostings=[_ncir],
    test_pcs=[_enb_test_pc],
    attenuators=[_attenuator_5G, _attenuator_4G],
    core=_realcore,
    nms=_netact,
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
# it's a WA, please see https://jira3.int.net.nokia.com/browse/TALIB-846,
# this jira has blocked a few transport TA cases design and debug
# one of other WA is declare a global python variable, 'TRANS_PARA = _trans_para'
# i don't know which WA is better, please give me suggestion if you like to change WA.
tl._trans_para = _trans_para

# only tl variable can be accessed by user
__all__ = ["tl"]
