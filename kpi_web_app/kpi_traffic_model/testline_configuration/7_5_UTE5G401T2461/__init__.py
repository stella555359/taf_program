__maintainer__ = "zhu baijie"
__team__ = "NSB MN RAN RD VRF HAZ3 7"
__email__ = "baijie.zhu@nokia-sbell.com"

import os
from taf.config.testline.appserver import AppServer
from taf.config.testline import (
    CloudDeployment,
    DeploymentNetworkStack,
    DeploymentVnfStack,
    MasterNode,
    K8S,
)
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
    K8SConnectionDetails,
)
from taf.config.testline.ue import (
    AirphoneCloud,
    Airphone,
    Prisma,
    TM500,
    Qualcomm,
    QualcommUeType,
    Android,
    MediaTek,
)  # added in taf.meta.5.4
from taf.config.testline import NetworkAddress, RoutingInformation, LicenseKeeper
from taf.config.testline import RealEnb, Airscale, CommonUnit
from taf.config.testline import HBTE_PDU as HBTE
from taf.config.testline.pdu import FPFH
from taf.config.testline import RU, RadioTypes
from taf.config.testline import CloudBts, CU
from taf.config.testline import VDU, FHGW
from taf.config.testline import PxeServer
from taf.config.testline import TestLine
from taf.config.testline import TestPc
from taf.config.testline.nms import NetAct
from taf.config.testline.attenuator import HBTE as AHBTE
from taf.config.testline.appserver import TafUeAppServer
from taf.config.testline import TafUeDataTransferProtocol
from taf.config.testline.pdn import PDNTafUeAndroidDetails
from taf.config.testline.ue import TafUeAndroid



_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# Testpc
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.177.123", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# CU
_cu = CU(
    instance_id=37440,
    global_bts_id=37440,
    backhaul_site_oam_ip=NetworkAddress(v4="10.57.222.134"),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.222.2", username="tl2461", password="systeM!23"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.222.134", username="Nemuadmin", password="Nokia@123", port=443
    ),
    f1c=NetworkAddress(
        v4="10.57.221.8",
        vlan_id=109,
        routing_v4=RoutingInformation(gateway="10.57.221.1", ip_prefix_length=26),
    ),
    f1u=NetworkAddress(
        v4="10.57.221.9",
        vlan_id=109,
        routing_v4=RoutingInformation(gateway="10.57.221.1", ip_prefix_length=26),
    ),
    ngc=NetworkAddress(
        v4="10.57.221.136",
        vlan_id=111,
        routing_v4=RoutingInformation(gateway="10.57.221.129", ip_prefix_length=26),
    ),
    ngu=NetworkAddress(
        v4="10.57.221.137",
        vlan_id=111,
        routing_v4=RoutingInformation(gateway="10.57.221.129", ip_prefix_length=26),
    ),
    x2c=NetworkAddress(
        v4="10.57.221.72",
        vlan_id=110,
        routing_v4=RoutingInformation(gateway="10.57.221.65", ip_prefix_length=26),
    ),
    x2u=NetworkAddress(
        v4="10.57.221.73",
        vlan_id=110,
        routing_v4=RoutingInformation(gateway="10.57.221.65", ip_prefix_length=26),
    ),
    s1u=NetworkAddress(
        v4="10.57.222.38",
        vlan_id=102,
        routing_v4=RoutingInformation(gateway="10.57.222.33", ip_prefix_length=27),
    ),
    tracing=None,
)

# cloud_deployment for vCU
_vcu_cnf_1 = DeploymentVnfStack(
    name="vcutest",
    yaml_file=os.path.join(_cfg_dir, "DEP/gnbs_0/vCU/CU_cnf_values-override.yaml"),
)
_vcu_intnet_1 = DeploymentNetworkStack(
    name=_vcu_cnf_1.name + "-prerequisite",
    yaml_file=os.path.join(_cfg_dir, "DEP/gnbs_0/vCU/CU_pvc_values-override.yaml"),
)

# ssh connection information of OE, for tenant user
_vcu_ssh_connection_details = SshServiceDetails(
    addr="10.57.222.2", username="tl2461", password="systeM!23", port=22
)
# ssh connection information of OE, for root user
_vcu_k8s_connection_details = K8SConnectionDetails(
    ip_addr="10.57.222.2", username="tl2461", password="systeM!23", port=22
)

_vcu_master_node = MasterNode(
    k8s_connection_details=_vcu_k8s_connection_details,
    ssh_connection_details=_vcu_ssh_connection_details,
)

_vcu_k8s = K8S(namespace="tl2461", master_node=_vcu_master_node)

_vcu_k8s_cloud_deployment = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    networks=[_vcu_intnet_1],
    vnfs=[_vcu_cnf_1],
    cloud_hosting=_vcu_k8s,
)


# 5G RU
_ru_pdu1 = FPFH(addr="10.64.49.76", port_numbers=[1])                                                                                                               


_ru1 = RU(
    ru_hw_group="Below6GHz",
    pdu_port=_ru_pdu1.pdu_ports[1],
    radio_type=RadioTypes.AZQJ,
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.37",
        username="rfsw",
        password="f6gh0K2nXq0O8XqVFkUuMtJnzuKm0U3box0QcYgugn0=",
    ),
)

# vDU information need update
_IP_pxe="x.x.x.x"
_pxe_server_ssh_info = SshServiceDetails(
    addr=_IP_pxe, username="root", password="uteadmin"
)
_pxe_server = PxeServer(
    nfs_ip=_IP_pxe, ssh_connection_details=_pxe_server_ssh_info
)

# FHGW information,need update
_fhgw_0 = FHGW(user_config_path=_cfg_dir, rus=[_ru1], pxe_server=_pxe_server)
_fhgw_0.ip = "x.x.x.x"
_fhgw_0.username = "toor4nsn"
_fhgw_0.password = "Fhgw@nokia123"
_fhgw_0.version = "FHGW24R2"

# OE information

_ssh_connection_details_0 = SshServiceDetails(
    addr="10.64.52.74", username="core", password="system123"
)
_k8s_connection_details_0 = K8SConnectionDetails(
    ip_addr="10.64.52.74", username="core", password="system123", port="22"
)

_master_node_0 = MasterNode(
    k8s_connection_details=_k8s_connection_details_0,
    ssh_connection_details=_ssh_connection_details_0,
)
_k8s_0 = K8S(namespace="tl2461", master_node=_master_node_0)
_vdu_cnf_0 = DeploymentVnfStack(
    name="vdutest",
    yaml_file=os.path.join(_cfg_dir, "DEP/gnbs_0/vDU_0/DU_cnf_values-override.yaml"),
)
_vdu_intnet_0 = DeploymentNetworkStack(
    name=_vdu_cnf_0.name + "-prerequisite",
    yaml_file=os.path.join(_cfg_dir, "DEP/gnbs_0/vDU_0/DU_pvc_values-override.yaml"),
)

_vdu_k8s_cloud_deployment_0 = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    cloud_hosting=_k8s_0,
    networks=[_vdu_intnet_0],
    vnfs=[_vdu_cnf_0],
)


_du_0 = VDU(
    cloud_deployment=_vdu_k8s_cloud_deployment_0,
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.64.52.98", username="Nemuadmin", password="Nokia@123"
    ),
    fhgws=[_fhgw_0],
    instance_id=37440,
    global_bts_id=37440,
)

_attenuator = AHBTE(
    ip_addr="10.64.56.30",
    port=5000,
    attenuation_port_numbers=[5,6,7,8],
    model="PA-16-16-6-127-0.5-B-S",
)

# BTS
_cbts = CloudBts(
    dus=[_du_0],
    cu=_cu,
    cloud_deployment=_vcu_k8s_cloud_deployment,
)



# AppServer info iperf used

_app_server_1 = TafUeAppServer(
    app_server_name="APP_SERVER_1",
    address="10.57.162.5",
    user="vrf3_sg8",
    password="vrf3@8",
    bind_interface_ip="10.57.162.5",
    expected_prompt="\[ute.*\$ ",
    ports=[58000, 58999]
)

_data_transfer_iperf = TafUeDataTransferProtocol(protocol_name='iperf',
                                                 app_server=_app_server_1,
                                                 interval=1,
                                                 binary_path='/data/data/com.nokia.android.application/',
                                                 #interface_name='rmnet_data0',
                                                 server_close_delay=50,
                                                 version=2)
                                                 
_data_transfer_ping = TafUeDataTransferProtocol(
    protocol_name="ping", app_server=_app_server_1, interval=1
)

_data_transfer_ftp = TafUeDataTransferProtocol(
    protocol_name="ftp", app_server=_app_server_1, interval=1
)


# CI_Detail_UE_Type='MTK'
_ue_host_ssh = SshServiceDetails(
        addr="10.0.176.11", username="mn5gran", password="nokia123@"
)




                               
_pdn1 = PDNTafUeAndroidDetails(
    entryName='default',  # MANDATORY / use this entry point as KW argument (pdn)
    apnName='stdata1',  # MANDATORY
    apnType=['DEFAULT', 'MMS', 'XCAP'],  # MANDATORY
    carrierEnabled=True,  # OPTIONAL
    operatorNumeric='55520',  # OPTIONAL
    protocol='IPV4V6',  # OPTIONAL
    roamingProtocol='IPV4V6',  # OPTIONAL
    proxyAddress='192.168.1.55',  # OPTIONAL
    proxyPort=1234,  # OPTIONAL
    mmsc='uri1',  # OPTIONAL
    mmsProxyAddress='192.168.1.66',  # OPTIONAL
    mmsProxyPort=4567,  # OPTIONAL
    user='tafue',  # OPTIONAL
    password='tafue',  # OPTIONAL
    mvnoType='GID',  # OPTIONAL
    networkType='NR',  # OPTIONAL
    authType='PAP')  # OPTIONAL

_pdn2 = PDNTafUeAndroidDetails(
    entryName='emergency',  # use this entry point as KW argument  (pdn)
    apnName='apn2',
    apnType=['SUPL', 'FOTA'])

# UE info
_android1 = TafUeAndroid(serial_number='9YS0219C23024103',
                        capabilities=['REAL_UE','huawei_android'],
                        ue_pc_address='10.64.57.51',
                        data_transfer=[_data_transfer_iperf,
                                       _data_transfer_ping,
                                       _data_transfer_ftp],
                        ssh_connection_details=SshServiceDetails(addr='10.64.57.51',
                                                                 username='tester5g',
                                                                 password='Nokia123!'),
                        phone_number='+8613100010793',
                        ue_pc_port='8080',
                        imei='868938040689392',
                        imsi='262033100010791',
                        #pdns=[_pdn1],
                        # qualcomm_prototype=True,
                        # service_call_attach='17',
                        # service_call_detach='17',
                        )

# TestLine
tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    tl_cloud_topology="tl2461",
    ues=[_android1],
    #appserver=_appserver,
)

__all__ = ["tl"]
