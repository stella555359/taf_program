# Generated with TL configuration generator at 2023-08-24_09:04:25

# Repository  -> https://wrgitlab.int.net.nokia.com/ran_pz_krk/config_generator
# Jenkins job -> http://krk-pz-jenkins.krk-lab.nsn-rdnet.net:5990/view/Tools/job/Config_Generator/build?delay=0sec

__maintainer__ = "KRKAUTO5GPZ"
__team__ = "I_MN_RAN_PZ_KRK_TAG"
__email__ = "I_MN_RAN_PZ_KRK_TAG@internal.nsn.com"

from taf.config.testline import (
    TafUeAppServer,
    TafUeDataTransferProtocol,
    TafUeAt,
    Connection,
)
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
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
    CapacityUnit,
    SlotId,
    TRSInterfaces,
)
from taf.config.testline.pdu import PduPort, Pdu, FPFH
import os
import yaml


def _set_abstract_lib_config_env(ue_config_file):
    tl_config_dir = os.path.dirname(os.path.abspath(__file__))

    ue_config_abs_path = os.path.join(tl_config_dir, ue_config_file)

    with open(ue_config_abs_path) as ta_ue_config:
        ue_config = yaml.safe_load(ta_ue_config)
    os.environ["ABSTRACT_LIB_CONFIG"] = ue_config_abs_path

    return ue_config


# ------------------------GNB_CONFIGURATION------------------------


_pdu1 = FPFH(
    addr="fpfh-za07-45-p04.p04-leg.ska-lab.nsn-rdnet.net",
    port_numbers=[3],
    login="admin",
    password="admin",
)


_gnb_oam_ip = NetworkAddress(
    v4="10.84.190.140/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_f1m_ip = NetworkAddress(
    v4="10.84.190.140/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
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
    v4="10.84.190.140/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_x2u_ip = NetworkAddress(
    v4="10.84.190.140/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_s1u_ip = NetworkAddress(
    v4="10.84.190.140/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_xnc_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_xnu_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_ngc_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_ngu_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_instance_id = 77140
_gnb_global_bts_id = 77140

_default_gnb_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT4SK140.p04.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    ),
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

gnb_capacity_unit_0 = CapacityUnit(
    addr="192.168.253.38",
    hardware_type="ABIO",
    hardware_version="A.104",
    serial_number="DH223447754",
    product_code="475266A.104",
    # slot_id=SlotId.B4
)

gnb_common_unit_0 = CommonUnit(
    lmp_connection=_default_gnb_ssh_lmp_connection,
    capacity_units=[gnb_capacity_unit_0],
    pdu_port=_pdu1.pdu_ports[3],
    hardware_type="ASIM",
    hardware_version="A.101",
    serial_number="L1224401612",
    mac_addr="",
    # trs_connections=[],
    # slot_id=SlotId.C2,
)

gnb_radio_unit_0 = RU(
    ru_hw_group="APHA",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.77.128", username="root", password="umniedziala"
    ),
    pdu_port=_pdu1.pdu_ports[3],
    radio_type="APHA",
    serial_number="NH191100275",
    product_code="474657A.101",
)

_airscale_gnb = Airscale(common_units=[gnb_common_unit_0], product_code="473098A")

_du_gnb = DU(
    airscale=_airscale_gnb,
    rus=[gnb_radio_unit_0],
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

# ------------------------ENB_CONFIGURATION------------------------

_enb_oam_ip = NetworkAddress(
    v4="10.84.190.139/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_enb_f1m_ip = NetworkAddress(
    v4="10.84.190.139/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_test_pc_enb = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT4SK139.p04.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_enb_instance_id = 77139
_enb_global_bts_id = 77139

_default_enb_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_enb.default_ssh_connection_details,
)

enb_capacity_unit_0 = CapacityUnit(
    addr="",
    hardware_type="ABIA",
    hardware_version="A.104",
    serial_number="L1193404236",
    product_code="473096A.104",
    # slot_id=SlotId.B1
)

enb_common_unit_0 = CommonUnit(
    lmp_connection=_default_enb_ssh_lmp_connection,
    capacity_units=[enb_capacity_unit_0],
    pdu_port=_pdu1.pdu_ports[3],
    hardware_type="ASIA",
    hardware_version="A.101",
    serial_number="L1164704542",
    mac_addr="",
    # trs_connections=[],
    # slot_id=SlotId.C1,
)

enb_radio_unit_0 = RU(
    ru_hw_group="APHA",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.9.129", username="root", password="umniedziala"
    ),
    radio_type="APHA",
    serial_number="NH191100275",
    product_code="474657A.101",
)

_airscale_enb = Airscale(common_units=[enb_common_unit_0], product_code="473098A")

_enb = RealEnb(
    rms=[enb_radio_unit_0],
    x2_link_addr=_enb_oam_ip,
    instance_id=_enb_instance_id,
    global_bts_id=_enb_global_bts_id,
    system_module=_airscale_enb,
    oam_ip=_enb_oam_ip,
)

# ------------------TafUeAndroid--------------------

_realcore_appsrv = TafUeAppServer(
    app_server_name="realcore",
    address="10.84.168.120",
    bind_interface_ip="10.84.169.60",
    user="5g",
    password="5g",
    expected_prompt="5g@SKA-HC14-15-AppServer",
)

_iperf_ue_sa = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_realcore_appsrv,
    binary_path="/data/data/com.nokia.android.application/",
    interval=1,
    server_close_delay=50,
)

_android_ue_1 = TafUeAt(
    com_port="8",
    # ssh_connection_details=SshServiceDetails(
    #     addr="10.84.182.31",
    #     username="user-lab0",
    #     password="Rz0dkiewk@2022",
    # ),
    ue_pc_address="10.84.182.31",
    ue_pc_login="user-lab0",
    ue_pc_password="Rz0dkiewk@2022",
    ue_pc_expected_prompt="user-lab0@PLKR-ASIR-CIT1",
    # serial_number="867978050006179",
    capabilities=["QUECTEL_UE_2"],
    data_transfer=[_iperf_ue_sa],
    # network_mode_switch_method="ADB",
    # airplane_mode_switcher_text="Airplane",
    # airplane_mode_confirm_button_text="OK",
    # secret_code="*#*#4636#*#*",
    # voice_call_technology_timeout=60.0,
    # voice_call_dialing_timeout=-1.0
)

_test_pc_gnb = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT4SK140.p04.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    ),
    connections=[
        NetworkAddress(v4="192.168.255.126"),
        Connection(
            interface="eth1",
            interface_type="lmp",
            device=_gnb.dus[0].airscale.common_units[0],
        ),
    ],
)

# ------------------------TL_CONFIGURATION------------------------
_ue_config = _set_abstract_lib_config_env("ue_config.yaml")

tl = TestLine(
    test_pc=_test_pc_gnb,
    gnbs=[_gnb],
    enbs=[_enb],
    test_pcs=[_test_pc_gnb, _test_pc_enb],
    ues=[_ue_config],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_QUECTEL_ASIMR_ABIOB4_APHA",
    pdus=[_pdu1],
)

__all__ = ["tl"]
