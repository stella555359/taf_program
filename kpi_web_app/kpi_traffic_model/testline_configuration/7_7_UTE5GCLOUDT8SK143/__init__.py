__maintainer__ = "KRKAUTO5GPZ"
__team__ = "I_MN_RAN_PZ_KRK_TAG"
__email__ = "I_MN_RAN_PZ_KRK_TAG@internal.nsn.com"

from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc, Connection
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    SCRadioConnectionDetails,
    TelnetConnectionDetails,
)
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline.gnb.networkaddress import NetworkAddress, RoutingInformation
from taf.config.testline.radio import RU, RUExtension, SC5GRadio
from taf.config.testline.enb import RealEnb
from taf.config.testline.airscale import (
    Airscale,
    CommonUnit,
    CoreUnit,
    CapacityUnit,
    SlotId,
    TRSInterfaces,
)
from taf.config.testline.pdu import PduPort, Pdu, FPFH
from taf.config.testline.ue import TafUeAndroid
from taf.config.testline.appserver import AppServer
from taf.config.testline.connection_details import IperfDataTransferDetails
from taf.config.testline.taf_ue_data_transfer_protocol import TafUeDataTransferProtocol
from taf.config.testline.appserver import TafUeAppServer
import os
import yaml

_gnb_pdu_0 = FPFH(
    port_numbers=[1, 2, 3, 4, 5, 6],
    addr="fpfh-zh09-48-p08.p08-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

_gnb_pdu_1 = FPFH(
    port_numbers=[1, 2, 3, 4, 5, 6],
    addr="fpfh-zh10-35-p08.p08-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

_pdus = [_gnb_pdu_0, _gnb_pdu_1]
# ------------------------GNB_CONFIGURATION------------------------

_gnb_oam_ip = NetworkAddress(
    v4="10.84.152.143/23",
    routing_v4=RoutingInformation(gateway="10.84.153.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_f1m_ip = NetworkAddress(
    v4="10.84.152.143/23",
    routing_v4=RoutingInformation(gateway="10.84.153.254", destIpAddr="0.0.0.0"),
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
    v4="10.84.152.143/23",
    routing_v4=RoutingInformation(gateway="10.84.153.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_x2u_ip = NetworkAddress(
    v4="10.84.152.143/23",
    routing_v4=RoutingInformation(gateway="10.84.153.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_s1u_ip = NetworkAddress(
    v4="10.84.152.143/23",
    routing_v4=RoutingInformation(gateway="10.84.153.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_xnc_ip = NetworkAddress(
    v4="10.84.152.143/23",
    routing_v4=RoutingInformation(gateway="10.84.153.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_xnu_ip = NetworkAddress(
    v4="10.84.152.143/23",
    routing_v4=RoutingInformation(gateway="10.84.153.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_ngc_ip = NetworkAddress(
    v4="10.84.152.143/23",
    routing_v4=RoutingInformation(gateway="10.84.153.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_ngu_ip = NetworkAddress(
    v4="10.84.152.143/23",
    routing_v4=RoutingInformation(gateway="10.84.153.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_test_pc_gnb = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT8SK143.p08.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_gnb_instance_id = 79143
_gnb_global_bts_id = 79143

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
    ru_hw_group="AQQN",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2", username="root", password="umniedziala"
    ),
    radio_type="AQQN",
    serial_number="L1223403775",
    product_code="475937A.102",
    pdu_port=_gnb_pdu_0.pdu_ports[1],
)

_gnb_core_unit_0 = CoreUnit(
    lmp_connection=_default_gnb_ssh_lmp_connection,
    hardware_type="ASOE",
    hardware_version="A.102",
    serial_number="EA214652579",
    mac_addr="",
    pdu_port=_gnb_pdu_1.pdu_ports[1],
)

_airscale_gnb = Airscale(core_units=[_gnb_core_unit_0], product_code="475587A.102")

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

_appserver_ssh = SshServiceDetails(addr="10.84.168.120", username="5g", password="5g")
_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.84.169.60",
    iperf_path="/usr/bin/iperf",
    ports=[2123, 2124],
)

_appserver = AppServer(_iperf_details_on_appserver)

_ue23_pc_ssh = SshServiceDetails(
    "PLKR-P08-UE011.intra.noklab.net", ".\\user-lab0", password="Bts2003"
)

_android_iperf = IperfDataTransferDetails(_appserver_ssh, "40.1.1.254", None)

_taf_appserv = TafUeAppServer(
    app_server_name="SKA-HC14-15-AppServer",
    address="10.84.168.120",
    bind_interface_ip="10.84.169.60",
    user="5g",
    password="5g",
)

_taf_data_transfer_1 = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_taf_appserv,
    binary_path="/data/data/com.nokia.android.application/",
    interval=1,
    # interface_name='5gsakrk2/rmnet_data1',
    server_close_delay=50,
)

_taf_data_transfer = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_taf_appserv,
    binary_path="/data/data/com.nokia.android.application/",
    interval=1,
    # interface_name='5gsakrk2/rmnet_data0',
    server_close_delay=50,
)

_android_ue1 = TafUeAndroid(
    capabilities=["REAL_UE", "REAL_ANDROID_UE_S22"],
    ssh_connection_details=_ue23_pc_ssh,
    serial_number="R5CT34BHC7Z",  # S22
    ue_pc_address="10.84.129.188",
    data_transfer=[_taf_data_transfer_1, _taf_data_transfer],
    network_mode_switch_method="ADB",
    service_call_attach="16",
    # service_call_detach='16',
    voice_call_technology_timeout=60.0,
    voice_call_dialing_timeout=-1.0,
)


def _set_abstract_lib_config_env(ue_config_file):
    tl_config_dir = os.path.dirname(os.path.abspath(__file__))
    ue_config_abs_path = os.path.join(tl_config_dir, ue_config_file)

    with open(ue_config_abs_path) as ta_ue_config:
        ue_config = yaml.safe_load(ta_ue_config)

    os.environ["ABSTRACT_LIB_CONFIG"] = ue_config_abs_path

    return ue_config


_ue_config = _set_abstract_lib_config_env("ue.yaml")
# ------------------------TL_CONFIGURATION------------------------

tl = TestLine(
    test_pc=_test_pc_gnb,
    gnbs=[_gnb],
    ues=[_android_ue1],
    test_pcs=[_test_pc_gnb],
    pdus=_pdus,
    tl_cloud_topology="CLOUD_5G_CLASSICAL_SA_ANDROID_ASOE_AQQN",
)

__all__ = ["tl"]
