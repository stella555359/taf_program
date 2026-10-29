__maintainer__ = "Wang Yun"
__team__ = "I_NSB_MN_5GSC_5GSW_ENG_AIC_SI_CN_PCI_GMS <I_NSB_MN_5GSC_5GSW_ENG_AIC_SI_CN_PCI@internal.nsn.com>"
__email__ = "I_NSB_MN_5GSC_5GSW_ENG_AIC_SI_CN_PCI@internal.nsn.com"
__owner_email__ = "yun.1.wang@nokia-sbell.com"

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
from taf.config.testline import (
    RealEnb,
    NetworkAddress,
    RoutingInformation,
    Airscale,
    CommonUnit,
)
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
from taf.config.testline.ue import Android
from taf.config.testline.attenuator import HBTE
from taf.config.testline.nms import Netact

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
#  16. please check nom mo configured
#################################################################


_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# UTE IP address and User Name, Password,
# this is test PC for AIC
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.108.229.140", username="ute", password="QAZqaz123!@#"
    )
)

# VCU related NCIR controlNode
_control = ControlNode(
    # Configuration for SSH access
    default_ssh_connection_details=SshServiceDetails(
        addr="10.107.123.66", username="core", password="system123"
    ),
    # Configuration for openstack connection
    open_stack_connection_details=OpenStackConnectionDetails(
        username="core",
        password="system123",
        ip_addr="10.107.123.66",
        tenant="cran3",
    ),
    # Configuration of BMC connection, if you need use it in test case, plase config it
    # currently, it's not used in agent
    bmc_connection_details=BmcConnectionDetails(addr="", username="", password=""),
)

# configuration of VCU related NCIR/OSP
_ncir = NCIR(compute_nodes=[], control_nodes=[_control], version="ncir_19")

# CU configuration
_cu = CU(
    # CU web UI ip address, oam interface ip of oam vm
    backhaul_site_oam_ip=NetworkAddress(
        v6="2a00:8a00:8000:5002:0:10:0:605"
        # v6=''
    ),
    # VCU OAM ssh connection, oam interface ip of oam vm
    oam_ssh_connection_details=SshServiceDetails(
        addr="2a00:8a00:8000:5002:0:10:0:605", username="serviceuser", password="Pl(FzaYj5~c5;q"
    ),
    # VCU OAM http connection, oam interface ip of oam vm
    oam_http_connection_details=HttpConnectionDetails(
        addr="2a00:8a00:8000:5002:0:10:0:605", username="Nemuadmin", password="nemuuser", port="443"
    ),
    # route configuration for x2 link to ENB, v4 is network address of ENB x2 link
    x2c=NetworkAddress(
        v4="10.97.122.224",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.110.101.1", ip_prefix_length=24),
    ),
    # route configuration for f1c link to VDU on VCU, v4 is network address of VDU f1c link
    f1c=NetworkAddress(
        v4="2a00:8a00:8000:5002:0:17:0000:0209",
        vlan_id=None,
        routing=RoutingInformation(gateway="2a00:8a00:8000:5002:0:17:0000:0201", ip_prefix_length=29),
    ),
    # route configuration for f1u link to VDU on VCU, v4 is network address of VDU f1u link
    f1u=NetworkAddress(
        v4="2a00:8a00:8000:5002:0:17:0000:0309",
        vlan_id=None,
        routing=RoutingInformation(gateway="2a00:8a00:8000:5002:0:17:0000:0301", ip_prefix_length=29),
    ),
    s1u=NetworkAddress(
        v4="0.0.0.0",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.110.101.1", ip_prefix_length=0),
    ),
    x2u=NetworkAddress(
        v4="10.97.122.224",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.110.101.1", ip_prefix_length=27),
    ),
    tracing=None,
)

# CU configuration
_cu1 = CU(
    # CU web UI ip address, oam interface ip of oam vm
    backhaul_site_oam_ip=NetworkAddress(
        v6="2a00:8a00:8000:5002:0:17:0000:070a"
        # v6=''
    ),
    # VCU OAM ssh connection, oam interface ip of oam vm
    oam_ssh_connection_details=SshServiceDetails(
        addr="2a00:8a00:8000:5002:0:17:0000:070a", username="serviceuser", password="Pl(FzaYj5~c5;q"
    ),
    # VCU OAM http connection, oam interface ip of oam vm
    oam_http_connection_details=HttpConnectionDetails(
        addr="2a00:8a00:8000:5002:0:17:0000:070a", username="Nemuadmin", password="nemuuser", port="443"
    ),
    # route configuration for x2 link to ENB, v4 is network address of ENB x2 link
    x2c=NetworkAddress(
        v4="10.97.122.224",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.110.101.1", ip_prefix_length=24),
    ),
    # route configuration for f1c link to VDU on VCU, v4 is network address of VDU f1c link
    f1c=NetworkAddress(
        v4="2a00:8a00:8000:5002:0:17:0000:020a",
        vlan_id=None,
        routing=RoutingInformation(gateway="2a00:8a00:8000:5002:0:17:0000:0201", ip_prefix_length=29),
    ),
    # route configuration for f1u link to VDU on VCU, v4 is network address of VDU f1u link
    f1u=NetworkAddress(
        v4="2a00:8a00:8000:5002:0:17:0000:030a",
        vlan_id=None,
        routing=RoutingInformation(gateway="2a00:8a00:8000:5002:0:17:0000:0301", ip_prefix_length=29),
    ),
    s1u=NetworkAddress(
        v4="0.0.0.0",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.110.101.1", ip_prefix_length=0),
    ),
    x2u=NetworkAddress(
        v4="10.97.122.224",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.110.101.1", ip_prefix_length=27),
    ),
    tracing=None,
)

# enb for NSA
_hbte_params_1 = {
    "ip_addr": "10.97.122.177",
    "port": 5000,
    "attenuation_port_numbers": [4, 8],
    "model": "PA-16-16-6-127-0.5-B-S",
    "version": None,
}
_attenuator_4G = HBTE(**_hbte_params_1)

_ru_4 = RU(
    ru_hw_group="hw_group",
    attenuation_ports=[
        _attenuator_4G.attenuator_ports[4],
        _attenuator_4G.attenuator_ports[8],
    ],
)
##RealEnb
# _real_enb_pdu = HBTE(addr="10.101.45.134", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.97.122.239", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    # pdu_port=_real_enb_pdu.pdu_ports[2],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(
    airscale=_real_enb,
    oam_ip="10.97.122.239",
    instance_id="",
    rms=[_ru_4],
    global_bts_id="5152",
)
# test pc information of enb
# you can configure it as AIC UTE environment
_enb_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.108.229.140", username="ute", password="QAZqaz123!@#"
    ),
    connections=[_lte_real_enb],
)

# VDU configuration for deployment
_vdu_vnf_1 = DeploymentVnfStack(
    name="vducran1",
    yaml_file=os.path.join(
        _cfg_dir,
        "DEP_SCF_FILES/CU_0/vDU_0/aic_vdu_values_override_0.yaml",  # replace "DEP_SCF_FILES/CU_0/vDU_0/aic_vdu_values_override_0.yaml"
    ),
)

# VDU internal network configuration for deployment
_vdu_intnet_1 = DeploymentNetworkStack(
    name="intnetcran1",
    yaml_file=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/aic_intnet_values_override_0.yaml"
    ),
)

# ssh connection information of OE, for tenant user
_ssh_connection_details = SshServiceDetails(
    addr="2a00:8a00:8000:117:1:46:400:2", username="cranuser1", password="systeM!23"
)

# ssh connection information of OE, for cloudadmin user
_k8s_connection_details = K8SConnectionDetails(
    ip_addr="2a00:8a00:8000:117:1:2:a47:a772", username="core", password="system123", port="22"
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
    addr="2a00:8a00:8000:117:1:46:405:2", port="443", username="Nemuadmin", password="nemuuser"
)

# RU configuration
_hbte_params = {
    "ip_addr": "10.97.122.177",
    "port": 5000,
    "attenuation_port_numbers": [1, 2, 3, 4, 5, 6, 7, 8],
    "model": "PA-16-16-6-127-0.5-B-S",
    "version": None,
}
_attenuator_5G = HBTE(**_hbte_params)

# RU configuration
_ru_1 = RU(
    ru_hw_group="RU_INT_ECPRI",
    serial_number="AS202612683",
    attenuation_ports=[
        _attenuator_5G.attenuator_ports[1],
        _attenuator_5G.attenuator_ports[5],
    ],
)

_ru_2 = RU(
    ru_hw_group="RU_INT_ECPRI",
    serial_number="AS202612681",
    attenuation_ports=[
        _attenuator_5G.attenuator_ports[2],
        _attenuator_5G.attenuator_ports[6],
    ],
)

_ru_3 = RU(
    ru_hw_group="RU_INT_ECPRI",
    serial_number="AS202612684",
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
    user_config_path=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/FHGW_0/fhgw_user_config_0.yaml"
    ),
    rus=[_ru_1, _ru_2, _ru_3],
    pxe_server=_pxe_server,
)

# VDU global configuration
_vdu_1 = VDU(
    cloud_deployment=_k8s_cloud_deployment,
    oam_http_connection_details=_vdu_oam_http_connection_details,
    fhgws=[_fhgw_1],
    # route configuration of f1m link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_m_ip_addr=NetworkAddress(
        v4="10.110.100.0",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.167.73", ip_prefix_length=24),
    ),
    # route configuration of f1c link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_c_ip_addr=NetworkAddress(
        v4="10.110.100.0",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.167.73", ip_prefix_length=24),
    ),
    # route configuration of f1u link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_u_ip_addr=NetworkAddress(
        v4="10.110.100.0",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.167.73", ip_prefix_length=24),
    ),
)

# mcc, mnc configuration
_realcore = RealCore(five_g=None, mcc="262", mnc="03", pdns=None)

_appserver_ssh = SshServiceDetails(
    addr="10.108.229.140", username="ute", password="QAZqaz123!@#"
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.108.229.140",
)
_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.97.123.112", username="aic.cn", password="Nokia123!"
    ),
    serial_number="R5CR10DCQYN",  # R5CN20LYP5R R5CN20HRWLM R5CN212N3RX
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "samsung"],
    #service_call_attach=17,
    #service_call_detach=17,
)
_nom_ssh_connection_edge0 = SshServiceDetails(
    addr="10.39.156.122", username="cloud-user"
)

_nom1 = NOM(
    ssh_connections_info=[_nom_ssh_connection_edge0],
    https_main_info=HttpConnectionDetails(
        addr="https://neo-hosting-page.srncnms04.srnblr.nsn-rdnet.net/",
        username="cnms01",
        password="Qwer1234",
    ),
    https_user_mgmt_info=HttpConnectionDetails(
        addr="https://user-mgmt.srncnms04.srnblr.nsn-rdnet.net",
    ),
    https_rest_info=HttpConnectionDetails(
        addr="https://apigw.srncnms04.srnblr.nsn-rdnet.net",
    ),
    neo_endpoints_ip="10.39.156.88",
)


netact_id = {
    "SRNCLAB2003": {
        "netact_id": "SRNCLAB2003",
        "node_ip": "10.82.47.46",
        "user": "omc",
        "password": "Medsql!_1893",
        "url": "https://srnclab2003lbwas.srnblr.nsn-rdnet.net",
        "url_user": "omc",
        "url_password": "Medsql!_1893",
        "mr": "MRC-10728/MR-10728",
        "ca_file": "nom/clab33ca.pem",
        "ca_sn": "0x9B",
        "ca_id": "",
    },
}

_netact = Netact(netact_id)

_vcu_intnet_1 = DeploymentNetworkStack(
    name="aic-vcu-intnet",
    yaml_file=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/aic_intnet_values_override_0.yaml"
    ),
)

_vcu_vnf_1 = DeploymentVnfStack(
    name="aic-vcu-cnf",
    yaml_file=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/aic_vdu_values_override_0.yaml"
    ),
)


# ssh connection information of OE, for tenant user
_vcu_ssh_connection_details = SshServiceDetails(
    addr="10.107.123.66", username="cranuser6", password="systeM!23"
)
# ssh connection information of OE, for root user
_vcu_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.107.123.66", username="core", password="system123", port="22"
)

_vcu_master_node = MasterNode(
    k8s_connection_details=_vcu_k8s_connection_details,
    ssh_connection_details=_vcu_ssh_connection_details,
)

_vcu_k8s = K8S(namespace="cran6", master_node=_vcu_master_node)

_vcu_k8s_cloud_deployment = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    networks=[_vcu_intnet_1],
    vnfs=[_vcu_vnf_1],
    cloud_hosting=_vcu_k8s,
)


# VCU global configuration
_cbts_0 = CloudBts(
    dus=[_vdu_1],  # vdu related parameter
    cu=_cu,
    cloud_deployment=_vcu_k8s_cloud_deployment,
    instance_id="5471",
    global_bts_id="5471",
)

_cbts_1 = CloudBts(
    dus=[],  # vdu related parameter
    cu=_cu1,
    cloud_deployment=_vcu_k8s_cloud_deployment,
    instance_id="54711",
    global_bts_id="54711",
)

_misc = {
    # 1-Use NOM config in __init__.py, 0-Use NOM config in global_variable.py.
    # If this key is not given, default value is 1
    "nom_config_source_from_init_py": "0",
    # 1-Use Netact config in __init__.py, 0-Use Netact config in global_variable.py.
    # If this key is not given, default value is 1
    "netact_config_source_from_init_py": "0",
}


# Testline configuration, tl is only variable which can be accessed by agent and test case
# you can access all parameters configured upper by tl parameter
tl = TestLine(
    test_pc=_test_pc,
    nms=_netact,
    gnbs=[_cbts_0, _cbts_1],
    enbs=[_lte_real_enb],
    tl_cloud_topology="CLOUD_5G_AIC_OCP_UE_OCP_1xvDU__OE19_FHGW_3xAHCA",
    cloud_hostings=[_ncir],
    test_pcs=[_enb_test_pc],
    attenuators=[_attenuator_5G, _attenuator_4G],
    ues=[_android],
    core=_realcore,
)
tl._misc = _misc

# only tl variable can be accessed by user
__all__ = ["tl"]
