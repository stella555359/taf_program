__maintainer__ = "Xu Huilin"
__team__ = "I_NSB_MN_5GSC_5GSW_ENG_AIC_SI_CN_2SISO_GMS <I_NSB_MN_5GSC_5GSW_ENG_AIC_SI_CN_2SISO@internal.nsn.com>"
__email__ = "I_NSB_MN_5GSC_5GSW_ENG_AIC_SI_CN_2SISO@internal.nsn.com"
__owner_email__ = "huilin.xu@nokia-sbell.com"

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

from taf.config.testline.connection_details import K8SConnectionDetails
from taf.config.testline.gnb.du import FHGW
from taf.config.testline.gnb.du import VDU
from taf.config.testline.cloud_hosting import MasterNode, K8S, ComputeNode
from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.config.testline.gnb.networkaddress import RoutingInformation
from taf.config.testline.radio import RU
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.nms import NMS
from taf.config.testline.nms import NOM
from taf.config.testline.nms import Netact

from taf.config.testline.appserver import TafUeAppServer
from taf.config.testline import TafUeDataTransferProtocol
from taf.config.testline.pdn import PDNTafUeAndroidDetails
from taf.config.testline.ue import TafUeAndroid

# Following all parameters should be configured for one testline
# please don't ignore any parameters, you can add, but don't ingore
# any problem, please check with CI team

#####  FOLLOWING ARE CHECKLIST OF TESTLINE CONFIGURATION #######

#  1. 5gbts_ext_net.env have been configured as following
#  2. 5gbts_flavor.env have been configured as following
#  3. 5gbts_heat.env have been configured as following
#  4. aic-intnet-values-override_x.yaml have been configured as following
#  5. aic-vdu-values-override_x.yaml have been configured as following
#  6. user_config_x.yaml have been configured as following (currently, it's not used)
#  7. "vnf_prefix" in 5gbts_flavor.env should be re-configued, don't use common flavor name
#  8. vnf_prefix naming rule should be flavor-<testline name>, e.g: flavor-7_5_UTE5GAIC001T001
#  9. "flavors" in 5gbts_heat.env should be configured and prefix should equal to vnf_prefix value configured on 5gbts_flavor.env
#  10. please make sure 5gbts_ext_net.env, 5gbts_flavor.env, 5gbts_heat.env are new enough for next build
#  11. please make sure aic-intnet-values-override_x.yaml and aic-vdu-values-override_x.yaml are new enough for next build
#  12. please make sure files in step 1,2,3,4,5 have valid configuration
#  13. please make sure ip address of NCIR and test pc can be accessible by network
#  14. please make sure VDU on OE have been cleared or VDU helm release name is equal to name of DeploymentVnfStack before start agent_5g_aic
#  15. please make sure VCU on NCIR have been cleared or VCU stack name is TL_<testline name>_BTS before start agent_5g_aic
#################################################################


_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# this is test PC for AIC, including UTE IP address, User Name and Password.
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.108.229.115", username="ute", password="QAZqaz123!@#"
    )
)

# ######## start of vCU ##########################################################
# #################### START of VCU CNF platform ##########################
_vcu_intnet_1 = DeploymentNetworkStack(
    name="aic-vcu-intnet",
    yaml_file=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/aic_intnet_values_override_0.yaml"
    ),
)

_vcu_vnf_1 = DeploymentVnfStack(
    name="aic-vcu",
    yaml_file=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/aic_vdu_values_override_0.yaml"
    ),
)

# ssh connection information of OE, for tenant user
_vcu_ssh_connection_details = SshServiceDetails(
    addr="10.110.11.130", username="cranuser4", password="systeM!23"
)
# ssh connection information of OE, for root user
_vcu_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.110.11.130", username="cranuser4", password="systeM!23", port="22"
)

_vcu_master_node = MasterNode(
    k8s_connection_details=_vcu_k8s_connection_details,
    ssh_connection_details=_vcu_ssh_connection_details,
)

_vcu_k8s = K8S(namespace="cran4", master_node=_vcu_master_node)

_vcu_k8s_cloud_deployment = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    networks=[_vcu_intnet_1],
    vnfs=[_vcu_vnf_1],
    cloud_hosting=_vcu_k8s,
)
# #################### End of VCU CNF platform ##########################

# CU configuration
_cu = CU(
    # CU web UI ip address, oam interface ip of oam vm
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.110.93.7"
        # v6='2a00:8a00:8000:136:10:57:159:1111'
    ),
    # VCU OAM ssh connection, oam interface ip of oam vm
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.110.93.7", username="serviceuser", password="Pl(FzaYj5~c5;q"
    ),
    # VCU OAM http connection, oam interface ip of oam vm
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.110.93.7", username="Nemuadmin", password="nemuuser", port="443"
    ),
    # route configuration for x2 link to ENB, v4 is network address of ENB x2 link
    f1c=NetworkAddress(
        v4="10.110.76.11",
        vlan_id=None,
        routing_v4=RoutingInformation(gateway="10.110.76.1", ip_prefix_length=24),
    ),
    # route configuration for f1u link to VDU on VCU, v4 is network address of VDU f1u link
    f1u=NetworkAddress(
        v4="10.110.76.12",
        vlan_id=None,
        routing_v4=RoutingInformation(gateway="10.110.76.1", ip_prefix_length=24),
    ),
    tracing=None,
    global_bts_id=11279,
)

# mcc, mnc configuration
_realcore = RealCore(five_g=None, mcc="262", mnc="03", pdns=None)


# ######## start of ENB #############################
_capacity_unit = CapacityUnit(addr="6.6.6.6")

_common_unit = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.97.120.152", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_capacity_unit],
)

_airscale = Airscale(common_units=[_common_unit])

_real_enb = RealEnb(airscale=_airscale, oam_ip="10.97.120.152")

# you can configure it as AIC UTE environment
_enb_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.108.229.115", username="ute", password="ute"
    ),
    connections=[_real_enb],
)


# ######## start of vDU ######################################################
# VDU deployment
_vdu_vnf_0 = DeploymentVnfStack(
    # this is vdu release name, the name should only be lower case and only can include alphabet, number,
    name="aic-vdu",
    yaml_file=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/aic_vdu_values_override_0.yaml"
    ),
)

_vdu_intnet_0 = DeploymentNetworkStack(
    # this is intnet release name, the name should only be lower case and only can include alphabet, number,
    name="aic-intnet",
    yaml_file=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/aic_intnet_values_override_0.yaml"
    ),
)

# ssh connection information of OE, for tenant user
_ssh_connection_details = SshServiceDetails(
    addr="10.69.183.2", username="cranuser1", password="systeM!23"
)
# ssh connection information of OE, for cloudadmin user
_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.69.183.2", username="core", password="system123", port="22"
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

_vdu_oam_http_connection_details = HttpConnectionDetails(
    addr="10.69.183.42", port="443", username="Nemuadmin", password="nemuuser"
)
# RU configuration
_hbte_params_1 = {
    "ip_addr": "10.108.213.139",
    "port": 5000,
    "attenuation_port_numbers": [1, 2, 3, 4, 5, 6],
    "model": "PA-8-8-4-127-0.5-B-S",
    "version": None,
}
_attenuator_5G_1 = HBTE(**_hbte_params_1)

# RU configuration
_ru_1 = RU(
    ru_hw_group="RU_INT_CPRI",
    serial_number="1M211917780",
    attenuation_ports=[
        _attenuator_5G_1.attenuator_ports[1],
        _attenuator_5G_1.attenuator_ports[2],
    ],
)
_ru_2 = RU(
    ru_hw_group="RU_INT_CPRI",
    serial_number="1M223231028",
    attenuation_ports=[
        _attenuator_5G_1.attenuator_ports[3],
        _attenuator_5G_1.attenuator_ports[4],
    ],
)
_ru_3 = RU(
    ru_hw_group="RU_INT_CPRI",
    serial_number="1M213303651",
    attenuation_ports=[
        _attenuator_5G_1.attenuator_ports[5],
        _attenuator_5G_1.attenuator_ports[6],
    ],
)

_hbte_params_2 = {
    "ip_addr": "10.108.213.167",
    "port": 5000,
    "attenuation_port_numbers": [1, 2, 3, 4, 5, 6, 7, 8, 13, 14, 15, 16],
    "model": "PA-8-8-4-127-0.5-B-S",
    "version": None,
}
_attenuator_5G_2 = HBTE(**_hbte_params_2)

_ru_4 = RU(
    ru_hw_group="RU_INT_ECPRI",
    serial_number="1M192827829",
    radio_type="78:f9:b4:2d:1f:1c",
    attenuation_ports=[
        _attenuator_5G_2.attenuator_ports[5],
        _attenuator_5G_2.attenuator_ports[6],
        _attenuator_5G_2.attenuator_ports[7],
        _attenuator_5G_2.attenuator_ports[8],
    ],
)
_ru_5 = RU(
    ru_hw_group="RU_INT_ECPRI",
    serial_number="L1180603010",
    radio_type="78:f9:b4:2d:1f:1c",
    attenuation_ports=[
        _attenuator_5G_2.attenuator_ports[1],
        _attenuator_5G_2.attenuator_ports[2],
        _attenuator_5G_2.attenuator_ports[3],
        _attenuator_5G_2.attenuator_ports[4],
    ],
)
_ru_6 = RU(
    ru_hw_group="RU_INT_ECPRI",
    serial_number="L1174911133",
    radio_type="78:f9:b4:2d:1f:1c",
    attenuation_ports=[
        _attenuator_5G_2.attenuator_ports[13],
        _attenuator_5G_2.attenuator_ports[14],
        _attenuator_5G_2.attenuator_ports[15],
        _attenuator_5G_2.attenuator_ports[16],
    ],
)
# PXE server info for FHGW deployment
_pxe_server_ssh_info = SshServiceDetails(
    addr="10.108.227.13", username="ute", password="Ut3pa5s#ff97"
)
_pxe_server = PxeServer(
    nfs_ip="10.108.227.13", ssh_connection_details=_pxe_server_ssh_info
)
# FHGW information
_fhgw_0 = FHGW(
    user_config_path=os.path.join(
        _cfg_dir, "DEP_SCF_FILES/CU_0/vDU_0/FHGW_0/fhgw_user_config_0.yaml"
    ),
    rus=[_ru_1, _ru_2, _ru_3, _ru_4, _ru_5, _ru_6],
    pxe_server=_pxe_server,
    fhgw_id=11279,
)
_vdu_0 = VDU(
    cloud_deployment=_k8s_cloud_deployment,
    oam_http_connection_details=_vdu_oam_http_connection_details,
    fhgws=[_fhgw_0],
    # route configuration of f1m link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_m_ip_addr=NetworkAddress(
        v4="10.69.183.42",
        vlan_id=None,
        routing_v4=RoutingInformation(gateway="10.69.183.41", ip_prefix_length=28),
    ),
    # route configuration of f1c link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_c_ip_addr=NetworkAddress(
        v4="10.69.183.26",
        vlan_id=None,
        routing_v4=RoutingInformation(gateway="10.69.183.25", ip_prefix_length=28),
    ),
    # route configuration of f1u link to VCU on VDU, v4 is VCU fronthaul port network address
    f1_u_ip_addr=NetworkAddress(
        v4="10.69.183.27",
        vlan_id=None,
        routing_v4=RoutingInformation(gateway="10.69.183.25", ip_prefix_length=27),
    ),
    instance_id=11279,
)

_cbts_0 = CloudBts(
    dus=[_vdu_0],  # vdu related parameter
    cu=_cu,
    cloud_deployment=_vcu_k8s_cloud_deployment,
    instance_id="11279",
    global_bts_id="11279",
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
    "du_switch_ip": "10.108.212.106",
    "username": "chriscd",
    "password": "12345678",
    "en_password": "",
    "port": "23",
    "switch_interface": "1/1/1",
    "simu4DU_interface": "",
    "acl_number": "188",
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

#  UE
# AppServer info
_app_server_1 = TafUeAppServer(
    app_server_name="APP_1",
    address="10.108.229.115",
    user="ute",
    password="QAZqaz123!@#",
)

_data_transfer_iperf = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_app_server_1,
    interval=1,
    # binary_path="/data/data/com.nokia.android.application/",
    interface_name="rmnet_data0",
    # bind_ue_ip=False,
    server_close_delay=50,
    version=2,
)

_pdn1 = PDNTafUeAndroidDetails(
    entryName="stdata2", apnName="stdata2", apnType=["DEFAULT"]
)

# UE info
_android_1 = TafUeAndroid(
    serial_number="R3CW10X08QJ",
    capabilities=["REAL_UE"],
    ue_pc_address="10.108.213.146",
    data_transfer=[_data_transfer_iperf],
    ssh_connection_details=SshServiceDetails(
        addr="10.108.213.146", username="aic", password="Nokia123!"
    ),
    # phone_number="+358480500013",
    ue_pc_port="8080",
    # imei="12345678912345",
    # imsi="260123456789",
    pdns=[_pdn1],
    # qualcomm_prototype=True,
    service_call_attach="17",
    service_call_detach="17",
    # network_mode_switch_method="ADB",
    # airplane_mode_switcher_text="Airplane",
    # airplane_mode_confirm_button_text="OK",
    # path_to_network_mode_type="Mobile networks/Preferred network type",
    # secret_code="*#0808#*",
    # is_rooted="no",
)
# Testline configuration, tl is only variable which can be accessed by agent and test case
# you can access all parameters configured upper by tl parameter
tl = TestLine(
    test_pc=_test_pc,
    ues=[_android_1],
    attenuators=[_attenuator_5G_1, _attenuator_5G_2],
    gnbs=[_cbts_0],
    enbs=[_real_enb],
    tl_cloud_topology="CLOUD_5G_AIC_OCP_UE_SA_1xvDU__OE20_FHGW_2xAEQY",
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
tl._trans_para = _trans_para
__all__ = ["tl"]
