# Generated with TL configuration generator at 2024-03-12_14:46:19

# Repository  -> https://wrgitlab.int.net.nokia.com/ran_pz_krk/config_generator
# Jenkins job -> http://krk-pz-jenkins.krk-lab.nsn-rdnet.net:5990/view/Tools/job/Config_Generator/build?delay=0sec

__maintainer__ = "KRKAUTO5GPZ"
__team__ = "I_MN_RAN_RD_VRF_KRK2"
__email__ = "OU_MN_RAN_RD_VRF_KRK_2_53115523@internal.nsn.com"
__owner_email__ = "przemyslaw.gajewski@nokia.com"

from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc, Connection
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
)
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline.gnb.networkaddress import NetworkAddress, RoutingInformation
from taf.config.testline.radio import RU, RUExtension
from taf.config.testline.enb import RealEnb
from taf.config.testline.airscale import (
    Airscale,
    CommonUnit,
    CoreUnit,
    CapacityUnit,
    SlotId,
    TRSInterfaces,
)
from taf.config.testline.pdu import PduPort, FPFH, HPE
from taf.config.testline.appserver import AppServer
from taf.config.testline.connection_details import IperfDataTransferDetails
from taf.config.testline.appserver import TafUeAppServer
from taf.config.testline.taf_ue_data_transfer_protocol import TafUeDataTransferProtocol
from taf.config.testline.ue import TafUeAndroid
from taf.config.testline.attenuator import RadioRack, TopYoung
from taf.config.testline.pdn import PDNTafUeAndroidDetails
import os
import yaml

# ------------------------PDU_CONFIGURATION------------------------

_bts_pdu = FPFH(
    port_numbers=[1],
    addr="10.255.10.11",
    login="admin",
    password="admin",
)

_hpe_snmp_user = {
    "userName": "administrator",
    "authKey": "password",
    "privKey": "password",
    "authProtocol": "MD5",
    "privProtocol": "DES",
}

_ru_pdu = HPE(
    port_numbers=[4, 5, 7],
    addr="hd02.mgt.ska-lab.nsn-rdnet.net",
    snmp_user=_hpe_snmp_user,
)

# ------------------------GNB_TEST_PC------------------------

_test_pc_gnb = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT1SK186.p01.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

# ------------------------GNB_CONFIGURATION------------------------

_gnb_oam_ip = NetworkAddress(
    v4="10.84.164.186/23",
    routing_v4=RoutingInformation(gateway="10.84.165.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_f1m_ip = NetworkAddress(
    v4="10.84.164.186/23",
    routing_v4=RoutingInformation(gateway="10.84.165.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_f1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_f1u_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_x2c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_x2u_ip = NetworkAddress(
    v4="10.84.164.186/23",
    routing_v4=RoutingInformation(gateway="10.84.165.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_s1u_ip = NetworkAddress(
    v4="10.84.164.186/23",
    routing_v4=RoutingInformation(gateway="10.84.165.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_xnc_ip = NetworkAddress(
    v4="10.84.164.186/23",
    routing_v4=RoutingInformation(gateway="10.84.165.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_xnu_ip = NetworkAddress(
    v4="10.84.164.186/23",
    routing_v4=RoutingInformation(gateway="10.84.165.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_ngc_ip = NetworkAddress(
    v4="10.84.164.186/23",
    routing_v4=RoutingInformation(gateway="10.84.165.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_ngu_ip = NetworkAddress(
    v4="10.84.164.186/23",
    routing_v4=RoutingInformation(gateway="10.84.165.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_instance_id = 76186
_gnb_global_bts_id = 76186

_default_gnb_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_gnb.default_ssh_connection_details,
)

_default_oam_http_connection = HttpConnectionDetails(
    addr=_gnb_oam_ip.v4.split("/")[0],
    username="Nemuadmin",
    password="nemuuser",
    port=443,
)

_cu_gnb = CU(
    backhaul_site_oam_ip=_gnb_oam_ip,
    oam_ssh_connection_details=_default_gnb_ssh_lmp_connection,
    oam_http_connection_details=_default_oam_http_connection,
    f1m=_gnb_f1m_ip,
    f1c=_gnb_f1c_ip,
    f1u=_gnb_f1u_ip,
    x2c=_gnb_x2c_ip,
    x2u=_gnb_x2u_ip,
    s1c=_gnb_s1c_ip,
    s1u=_gnb_s1u_ip,
    xnc=_gnb_xnc_ip,
    xnu=_gnb_xnu_ip,
    ngc=_gnb_ngc_ip,
    ngu=_gnb_ngu_ip,
    instance_id=_gnb_instance_id,
    global_bts_id=_gnb_global_bts_id,
)

_gnb_radio_unit_0 = RU(
     ru_hw_group="APHG",
     default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="toor4nsn",
        password="oZPS0POrRieRtu",
     ),
     radio_type="APHG",
     serial_number="NH211600047",
     product_code="475295A.101",
     pdu_port=PduPort(pdu=_ru_pdu, port_no=4),
)

_gnb_radio_unit_1 = RU(
     ru_hw_group="APHG",
     default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="toor4nsn",
        password="oZPS0POrRieRtu",
     ),
     radio_type="APHG",
     serial_number="NH213100521",
     product_code="475295A.101",
     pdu_port=PduPort(pdu=_ru_pdu, port_no=5),
)

_gnb_radio_unit_2 = RU(
     ru_hw_group="APHG",
     default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="toor4nsn",
        password="oZPS0POrRieRtu",
     ),
     radio_type="APHG",
     serial_number="NH211600101",
     product_code="475295A.101",
     pdu_port=PduPort(pdu=_ru_pdu, port_no=7),
)

_gnb_core_unit_0 = CoreUnit(
    lmp_connection=_default_gnb_ssh_lmp_connection,
    hardware_type="ASOE",
    hardware_version="A.102",
    serial_number="EA213353893",
    mac_addr="",
    # trs_connections=[],
    rus=[_gnb_radio_unit_0, _gnb_radio_unit_1, _gnb_radio_unit_2],
    pdu_port=PduPort(pdu=_bts_pdu, port_no=1),
)

_airscale_gnb = Airscale(
    core_units=[_gnb_core_unit_0],
    product_code="N/A",
    )

_du_gnb = DU(
    airscale=_airscale_gnb,
    oam_ip=_gnb_oam_ip,
    f1_m_ip_addr=_gnb_f1m_ip,
    f1_c_ip_addr=_gnb_f1c_ip,
    f1_u_ip_addr=_gnb_f1u_ip,
    f1_m_cu=_gnb_f1m_ip,
    f1_c_cu=_gnb_f1c_ip,
    f1_u_cu=_gnb_f1u_ip,
    instance_id=_gnb_instance_id,
    global_bts_id=_gnb_global_bts_id,
    )

_gnb = ClassicalBts(
    cu=_cu_gnb,
    dus=[_du_gnb],
    instance_id=_gnb_instance_id,
    global_bts_id=_gnb_global_bts_id,
)

_test_pc_gnb.connections = [
    Connection(
        device=_gnb.dus[0].airscale.core_units[0],
        interface="eth1",
        interface_type="lmp",
    )
]

_pdn1 = \
    PDNTafUeAndroidDetails(entryName='default',
                           apnName='5gsakrk',
                           apnType=['DEFAULT', 'MMS', 'XCAP'],
    )

_pdn2 = \
    PDNTafUeAndroidDetails(entryName='default',
                           apnName='5gkrk2',
                           apnType=['DEFAULT', 'MMS', 'XCAP'],
    )

_appserver_ssh_4g = TafUeAppServer(
    app_server_name="APP_1",
    address="10.84.172.214",
    user="ute",
    password="ute",
    bind_interface_ip="41.1.2.254",
)
_appserver_ssh_5g = TafUeAppServer(
    app_server_name="APP_2",
    address="10.84.139.190",
    user="ute",
    password="ute",
    # bind_interface_ip="10.84.139.255",
    bind_interface_ip="41.1.1.254",
)
_appserver_SKA = TafUeAppServer(
    app_server_name="APP_3",
    address="10.84.168.70",
    user='5g',
    password='5g',
    bind_interface_ip='10.84.169.54',
    expected_prompt='5g@SKA-HC14s17-1:.*\$\s+',
)

_nokia_iperf_5g = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_appserver_ssh_5g,
)
_nokia_iperf_4g = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_appserver_ssh_4g,
)
_nokia_iperf_SKA = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_appserver_SKA,
    # version=3,
)

_nokia_5g = TafUeAndroid(
    serial_number="AQKSLVH002N33100399",
    ue_pc_address="PLKR-SG02-154.intra.noklab.net",
    ssh_connection_details=SshServiceDetails(
        addr="PLKR-SG02-154.intra.noklab.net", username="pzkrk", password="NokiaBts2003"
    ),
    capabilities=["REAL_UE", "REAL_ANDROID_UE, REAL_QUALCOMM_UE"],
    qualcomm_prototype=False,
    data_transfer=[_nokia_iperf_SKA],
    network_mode_switch_method="secretcode",
    secret_code='*#*#4636#*#*',
    path_to_network_mode_type='Set Preferred Network Type',
    is_rooted="yes",
)

_nokia_4g = TafUeAndroid(
    serial_number="AQKSLVH002N33100399",
    ue_pc_address="PLKR-SG02-154.intra.noklab.net",
    ssh_connection_details=SshServiceDetails(
        addr="PLKR-SG02-154.intra.noklab.net", username="pzkrk", password="NokiaBts2003"
    ),
    capabilities=["REAL_UE", "REAL_ANDROID_UE, REAL_QUALCOMM_UE"],
    qualcomm_prototype=False,
    data_transfer=[_nokia_iperf_4g],
    is_rooted="yes",
    network_mode_switch_method="keyevents",
)

_attenuator_radiorack = RadioRack(
    ip_addr="10.255.10.94", port=50000, attenuation_port_numbers=range(1, 16)
)
_attenuator_topyoung = TopYoung(
    ip_addr="10.255.10.92", port=23, attenuation_port_numbers=range(1, 324)
)

# ------------------------TL_CONFIGURATION------------------------


tl = TestLine(
    test_pc=_test_pc_gnb,
    gnbs=[_gnb],
    test_pcs=[_test_pc_gnb],
    ues=[_nokia_5g, _nokia_4g],
    attenuators=[_attenuator_radiorack],
    tl_cloud_topology='CLOUD_5G_CLASSICAL_ANDROID_SA_ASOE_3xAPHG_12xAWHGEQH'
)

__all__ = ["tl"]
