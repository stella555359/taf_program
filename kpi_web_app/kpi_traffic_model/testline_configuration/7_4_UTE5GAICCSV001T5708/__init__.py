__maintainer__ = "Jaakko Granlund"
__team__ = "I_CLOUD_AGENT_AIC@internal.nsn.com"
__email__ = "I_CLOUD_AGENT_AIC@internal.nsn.com"
__owner_email__ = "jaakko.granlund@nokia.com"

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
    UltraCallerConnectionDetails,
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
from taf.config.testline.nms import NMS
from taf.config.testline.nom import NOM
from taf.config.testline.ue import UltraCaller

# Following mandatory files and parameters should be configured
# Please don't ignore any parameters, you can add, but don't ingore
# Any problem, please check with CI team

#####  FOLLOWING ARE CHECKLIST OF TESTLINE CONFIGURATION #######

#  1. 5gbts_ext_net.env have been configured as following
#  2. 5gbts_flavor.env have been configured as following
#  3. 5gbts_heat.env have been configured as following
#  4. aic-intnet-values-override_${vdu_index}.yaml (vdu_index should start from 0) have been configured as following
#  5. aic-vdu-values-override_${vdu_index}.yaml (vdu_index should start from 0) have been configured as following
#  6. user_config_${fhgw_index}.yaml (fhgw_index should start from 0) have been configured as following (currently, it's not used)
#  7. "vnf_prefix" in 5gbts_flavor.env should be re-configued, don't use common flavor name
#  8. vnf_prefix naming rule should be flavor-<testline name>, e.g: flavor-7_5_UTE5GAIC001T037
#  9. "flavors" in 5gbts_heat.env should be configured and prefix should equal to vnf_prefix value configured on 5gbts_flavor.env
#  10. please make sure 5gbts_ext_net.env, 5gbts_flavor.env, 5gbts_heat.env are new enough for next build
#  11. please make sure aic-intnet-values-override_x.yaml and aic-vdu-values-override_x.yaml are new enough for next build
#  12. please make sure files in step 1,2,3,4,5 have valid configuration
#  13. please make sure ip address of NCIR and test pc can be accessible by network
#  14. please make sure VDU on OE have been cleared or VDU helm release name is equal to name of DeploymentVnfStack before start agent_5g_aic
#  15. please make sure VCU on NCIR have been cleared or VCU stack name is TL_<testline name>_BTS before start agent_5g_aic

#################################################################

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# UTE IP address and User Name, Password,
# this is test PC (UTE VM) for AIC
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.17.42.39", username="ute", password="CsvUTE2021!"
    )
)

# VCU related NCIR controlNode:
_control = ControlNode(
    # Configuration for SSH access
    default_ssh_connection_details=SshServiceDetails(
        addr="10.16.1.116", username="cranuser8", password="systeM!23"
    ),
    # Configuration for openstack connection
    open_stack_connection_details=OpenStackConnectionDetails(
        username="cranuser8",
        password="systeM!23",
        ip_addr="10.16.1.116",
        tenant="cran8",
    ),
    # Configuration of BMC connection, if you need use it in test case, plase config it
    # currently, it's not used in agent
    bmc_connection_details=BmcConnectionDetails(addr="", username="", password=""),
)

# configuration of VCU related NCIR/OSP
_ncir = NCIR(compute_nodes=[], control_nodes=[_control], version="ncir_18")

# CU configuration (vCU-5708):
_cu = CU(
    # CU web UI ip address, oam interface ip of oam vm
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.16.30.50"
        # v6='2a00:8a00:8000:136:10:57:159:1111'
    ),
    # VCU OAM ssh connection, oam interface ip of oam vm
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.16.30.50", username="robot", password="rastre1"
    ),
    # VCU OAM http connection, oam interface ip of oam vm
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.16.30.50", username="Nemuadmin", password="nemuuser", port="443"
    ),
    # route vCU -> SGW
    s1u=NetworkAddress(
        v4="10.16.236.0",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.16.30.193", ip_prefix_length=24),
    ),
    # route vCU -> 4G/SBTS X2 interface
    x2c=NetworkAddress(
        v4="10.16.46.144",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.16.30.193", ip_prefix_length=29),
    ),
    # route vCU -> vDU F1-C interface
    f1c=NetworkAddress(
        v4="10.16.46.32",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.16.30.65", ip_prefix_length=28),
    ),
    # route vCU -> vDU F1-U interfaceS
    f1u=NetworkAddress(
        v4="10.16.46.32",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.16.30.65", ip_prefix_length=28),
    ),
    tracing=None,
)

# enb for NSA (SBTS-4708)
_real_enb = RealEnb(oam_ip="10.16.46.148", instance_id="")

# test pc information of enb
# you can configure it as AIC UTE environment
_enb_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.17.42.39", username="ute", password="CsvUTE2021!"
    ),
    connections=[_real_enb],
)

# flavor of VCU
flavor_env_files = [os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/5gbts_flavor.env")]

# ext_net of VCU
net_env_files = [os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/5gbts_ext_net.env")]

# heat parameters
vnf_env_files = [os.path.join(_cfg_dir, "DEP_SCF_FILES/CU_0/5gbts_heat.env")]

_cbts_flavor = DeploymentFlavorStack(
    name="name is not used",  # this name is not used, you need NOT configure it, let it be
    env_files=flavor_env_files,
    default_vnf_prefix="esp-tl5708",
)

_cbts_net = DeploymentNetworkStack(
    name="name is not used",  # this name is not used, you need NOT configure it, let it be
    env_files=net_env_files,
    yaml_file=os.path.join(_cfg_dir, "5gbts_ext_net.yaml"),
)

_cbts_vnf = DeploymentVnfStack(
    name="name is not used",  # this name is not used, you need NOT configure it, let it be
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
_vdu_vnf_0 = DeploymentVnfStack(
    name="aic-vdu-mvp",  # this is vdu release name, the name should only be lower case and only can include alphabet, number, _
    yaml_file=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/aic_vdu_values_override_0.yaml"
    ),
)

# VDU internal network configuration for deployment
_vdu_intnet_0 = DeploymentNetworkStack(
    name="aic-intnet-mvp",  # this is intnet release name, the name should only be lower case and only can include alphabet, number, _
    yaml_file=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/aic_intnet_values_override_0.yaml"
    ),
)

# ssh connection information of OE, for tenant user
_ssh_connection_details = SshServiceDetails(
    addr="10.16.46.26", username="cranuser1", password="systeM!23"
)

# ssh connection information of OE, for cloudadmin user
_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.16.46.26", username="cloudadmin", password="system123", port="22"
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
    networks=[_vdu_intnet_0],
    vnfs=[_vdu_vnf_0],
    cloud_hosting=_k8s,
)

# VDU oam http connection
_vdu_oam_http_connection_details = HttpConnectionDetails(
    addr="10.16.46.50", port="443", username="Nemuadmin", password="nemuuser"
)

# RU configuration
_ru_1 = RU(ru_hw_group="RU_INT_CPRI", serial_number="AS194201388")

# PXE server info for FHGW deployment
_pxe_server_ssh_info = SshServiceDetails(
    addr="10.17.36.133", username="labuser", password="system123"
)
_pxe_server = PxeServer(
    nfs_ip="10.17.36.133", ssh_connection_details=_pxe_server_ssh_info
)

# FHGW information
_fhgw_0 = FHGW(
    user_config_path=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/FHGW_0/user_config_0.yaml"
    ),
    rus=[_ru_1],
    pxe_server=_pxe_server,
)

# VDU global configuration
_vdu_0 = VDU(
    cloud_deployment=_k8s_cloud_deployment,
    oam_http_connection_details=_vdu_oam_http_connection_details,
    fhgws=[_fhgw_0],
    # route vDU -> vCU F1-M interface.
    f1_m_ip_addr=NetworkAddress(
        v4="10.16.30.64",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.16.46.33", ip_prefix_length=26),
    ),
    # route vDU -> vCU F1-C interface
    f1_c_ip_addr=NetworkAddress(
        v4="10.16.30.64",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.16.46.33", ip_prefix_length=26),
    ),
    # route vDU -> vCU F1-U interface
    f1_u_ip_addr=NetworkAddress(
        v4="10.16.30.64",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.16.46.33", ip_prefix_length=26),
    ),
)

# mcc, mnc configuration
_realcore = RealCore(five_g=None, mcc="001", mnc="01", pdns=None)

# VCU global configuration
_cbts_0 = CloudBts(
    dus=[_vdu_0],  # vdu related parameter
    cu=_cu,
    cloud_deployment=_cloud_deployment,
    instance_id="5708",
    global_bts_id="5708",
)

_nom_ssh_connection_edge0 = SshServiceDetails(
    addr="10.17.42.34",
    username="cloud-user"
    #   addr="10.39.156.122", username="cloud-user" As a WA replace NOM IP with a pingable IP (7-4-UTE5GAICCSV001T5701)
)

_nom1 = NOM(
    ssh_connections_info=[_nom_ssh_connection_edge0],
    https_main_info=HttpConnectionDetails(
        addr="https://neo-hosting-page.srncnms04.srnblr.nsn-rdnet.net/",
        username="cnms01",
        password="Qwer1234",
    ),
    neo_endpoints_ip="10.39.156.88",
)

_cnms = NMS(addr="10.17.42.34", nom=_nom1)
# _cnms = NMS(addr="10.39.156.122", nom=_nom1) As a WA replace NOM IP with a pingable IP (7-4-UTE5GAICCSV001T5701)

_uc_server_details = HttpConnectionDetails(addr="10.17.36.180", port=443)
_uc_details = UltraCallerConnectionDetails(
    ultracaller_server_details=_uc_server_details,
    api_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IkFJQ181R19DU1ZfRXNwb29fNTcwOCIsImFkbWluIjoiIn0.hMUxpHhNzcfgu0IvjIVAfjkl2rRXaSm8nPi_WgB35wQ",
)

_uc_ue1 = UltraCaller(
    ultracaller_connection_details=_uc_details,
    head_group="5708",
    sub_group="rf6",
    imei="352620111810759",
)

# Testline configuration, tl is only variable which can be accessed by agent and test case
# you can access all parameters configured upper by tl parameter
tl = TestLine(
    test_pc=_test_pc,
    nms=_cnms,
    gnbs=[_cbts_0],
    enbs=[_real_enb],
    ues=[_uc_ue1],
    tl_cloud_topology="CLOUD_5G_AIC_NCIR_NCIR_FHGW_AHCA",
    cloud_hostings=[_ncir],
    test_pcs=[_enb_test_pc],
    core=_realcore,
)

# only tl variable can be accessed by user
__all__ = ["tl"]
