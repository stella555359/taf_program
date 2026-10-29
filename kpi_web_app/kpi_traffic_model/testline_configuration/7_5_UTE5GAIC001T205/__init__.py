__maintainer__ = "Zhao ling"
__team__ = "I_NSB_MN_5GSC_5GSW_ENG_AIC_SI_CN_2SISO_GMS <I_NSB_MN_5GSC_5GSW_ENG_AIC_SI_CN_2SISO@internal.nsn.com>"
__email__ = "I_NSB_MN_5GSC_5GSW_ENG_AIC_SI_CN_2SISO@internal.nsn.com"
__owner_email__ = "ling.2.zhao@nokia-sbell.com"

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
from taf.config.testline import RealEnb, RU
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.connection_details import K8SConnectionDetails
from taf.config.testline.gnb.du import FHGW
from taf.config.testline.gnb.du import VDU
from taf.config.testline.cloud_hosting import MasterNode, K8S
from taf.config.testline.lab_infrastructure import PxeServer
from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.config.testline.nms import Netact


_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# Testpc
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.108.229.98", username="ute", password="ute"
    )
)

# NCIR
_control = ControlNode(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.110.9.116", username="cranuser33", password="systeMi!23"
    ),
    open_stack_connection_details=OpenStackConnectionDetails(
        username="cranuser33",
        password="systeM!23",
        ip_addr="10.110.9.116",
        tenant="cran33",
    ),
    bmc_connection_details=BmcConnectionDetails(addr="", username="", password=""),
)

_ncir = NCIR(compute_nodes=[], control_nodes=[_control], version="ncir_18")

# CU
_cu = CU(
    backhaul_site_oam_ip="10.110.99.36",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.110.99.36", username="serviceuser", password="Pl(FzaYj5~c5;q"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.110.99.36", username="Nemuadmin", password="nemuuser", port="443"
    ),
)


_capacity_unit_2 = CapacityUnit(addr="6.6.6.6")

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.97.120.141", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_capacity_unit_2],
)


_airscale_2 = Airscale(common_units=[_common_unit_2])

# enb
_real_enb = RealEnb(airscale=_airscale_2)

# CloudBts
flavor_env_files = [os.path.join(_cfg_dir, "5gbts_flavor.env")]
net_env_files = [os.path.join(_cfg_dir, "5gbts_ext_net.env")]
vnf_env_files = [
    os.path.join(_cfg_dir, "5gbts_heat.env"),
    os.path.join(_cfg_dir, "5gbts_heat_qt.env"),
]
_cbts_flavor = DeploymentFlavorStack(
    name="hgz-tl001_flavor",
    env_files=flavor_env_files,
    yaml_file=os.path.join(_cfg_dir, "5gbts_flavor.yaml"),
    default_vnf_prefix="hgz-tl4444",
)

_cbts_net = DeploymentNetworkStack(
    name="EXT_NET",
    env_files=net_env_files,
    yaml_file=os.path.join(_cfg_dir, "5gbts_ext_net.yaml"),
)

_cbts_vnf = DeploymentVnfStack(
    name="HGZ-TL001-STACK",
    env_files=vnf_env_files,
    yaml_file=os.path.join(_cfg_dir, "5gbts_heat.yaml"),
)

_cloud_deployment = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    flavors=[_cbts_flavor],
    networks=[_cbts_net],
    vnfs=[_cbts_vnf],
    cloud_hosting=_ncir,
)

_vdu_vnf = DeploymentVnfStack(
    name="test_vdu_vnf",
    yaml_file=os.path.join(_cfg_dir, "aic-vdu-values-override.yaml"),
)

_vdu_intnet = DeploymentNetworkStack(
    name="test_vdu_network",
    yaml_file=os.path.join(_cfg_dir, "aic-intnet-values-override.yaml"),
)

_ssh_connection_details_1 = SshServiceDetails(
    addr="10.71.165.2", username="cranuser1", password="systeM!23"
)
_k8s_connection_details_1 = K8SConnectionDetails(
    ip_addr="10.71.165.2", username="cloudadmin", password="system123", port="22"
)

_master_node_1 = MasterNode(
    k8s_connection_details=_k8s_connection_details_1,
    ssh_connection_details=_ssh_connection_details_1,
)
_k8s_1 = K8S(namespace="cran1", master_node=_master_node_1)
_k8s_cloud_deployment_1 = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    networks=[_vdu_intnet],
    vnfs=[_vdu_vnf],
    cloud_hosting=_k8s_1,
)

_vdu_oam_http_connection_details = HttpConnectionDetails(
    addr="10.71.165.18", username="nemuadmin", password="nemuadmin"
)
_ru_1 = RU(ru_hw_group="RU_INT_ECPRI")
_ru_2 = RU(ru_hw_group="RU_INT_CPRI")
_pxe_server_ssh_info = SshServiceDetails(
    addr="10.68.179.27", username="root", password="centos"
)
_pxe_server = PxeServer(
    nfs_ip="10.68.179.27", ssh_connection_details=_pxe_server_ssh_info
)
_fhgw_1 = FHGW(
    user_config_path=os.path.join(_cfg_dir, "user_config.yaml"),
    rus=[_ru_1],
    pxe_server=_pxe_server,
)
_vdu_1 = VDU(
    cloud_deployment=_k8s_cloud_deployment_1,
    oam_http_connection_details=_vdu_oam_http_connection_details,
    fhgws=[_fhgw_1],
    f1_m_ip_addr=NetworkAddress(v4="10.71.164.18"),
    f1_c_ip_addr=NetworkAddress(v4="10.71.164.10"),
    f1_u_ip_addr=NetworkAddress(v4="10.71.164.11"),
)


_cbts = CloudBts(
    dus=[_vdu_1],
    cu=_cu,
    cloud_deployment=_cloud_deployment,
    vnf_name="hgz-tl001",
    instance_id="3226",
)

# used for CNUMS, but Netact is incomplete now, it will be improved in future
# 10.108.229.91 is a fake CNUMS server ip
_netact = Netact("10.108.229.90")

_tools_repository = {
    "ip": "10.108.229.152",
    "username": "ute",
    "password": "ute",
    "repo_tool_folder": "/opt/tools/trans_test/",
    "repo_data_folder": "/opt/tools/trans_data/",
    "repo_simu4trs_folder": "/opt/tools/trans_simu4trs/",
}

_simulator4DU = {
    "ip": "10.108.227.14",
    "username": "root",
    "password": "rootroot",
    "service_ip": "10.108.227.133",
    "service_ipv6": "2a00:8a00:8000:117:0:8:0:10",
}

_switch_1 = {
    "du_switch_ip": "10.108.212.106",
    "username": "chrisc",
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


_trans_para = {
    "tools_repository": _tools_repository,
    "simulator4DU": _simulator4DU,
    "du_switch": [_switch_1],
}

# TestLine
tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    enbs=[_real_enb],
    tl_cloud_topology="CLOUD_5G_AIC__T1_NSA_VCP_OE19_FHGW_CPRI_N_AHCA",
    cloud_hostings=[_ncir],
    nms=_netact,
)

# it's a WA, please see https://jira3.int.net.nokia.com/browse/TALIB-846,
# this jira has blocked a few transport TA cases design and debug
# one of other WA is declare a global python variable, 'TRANS_PARA = _trans_para'
# i don't know which WA is better, please give me suggestion if you like to change WA.
tl._trans_para = _trans_para

__all__ = ["tl"]
