__team__ = "5G_PZ_MMW_KRK_3_SG"
__maintainer__ = "Karol Lapczyk"
__email__ = "karol.lapczyk@nokia.com"


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
from taf.config.testline.pdu import PduPort, ATEN, HPE, FPFH
from taf.config.testline.lmi import SerialOverHost, Local, Remote, SerialOverTcp
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
_gnb_pdu_75_za04_left = FPFH(
    port_numbers=[1, 2, 3],
    addr="fpfh-za04-left-p04.p04-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)
_gnb_pdu_75_za04_right = FPFH(
    port_numbers=[4],
    addr="fpfh-za04-right-p04.p04-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)
_gnb_pdu_48 = FPFH(
    port_numbers=[4],
    addr="fpfh-za03-48-p04.p04-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)
_gnb_oam_ip = NetworkAddress(
    v4="10.84.190.84/23",
    routing_v4=RoutingInformation(gateway="10.255.23.254", destIpAddr="10.84.169.0"),
    vlan_id=504,
)

_gnb_f1m_ip = NetworkAddress(
    v4="10.84.190.84/23",
    routing_v4=RoutingInformation(gateway="10.255.23.254", destIpAddr="10.84.169.0"),
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
    v4="10.84.148.84/23",
    routing_v4=RoutingInformation(gateway="10.255.23.254", destIpAddr="10.84.169.0"),
    vlan_id=507,
)

_gnb_x2u_ip = NetworkAddress(
    v4="10.255.20.84/23",
    routing_v4=RoutingInformation(gateway="10.255.23.254", destIpAddr="10.84.169.0"),
    vlan_id=505,
)

_gnb_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_s1u_ip = NetworkAddress(
    v4="10.255.22.84/23",
    routing_v4=RoutingInformation(gateway="10.255.23.254", destIpAddr="10.84.169.0"),
    vlan_id=506,
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

_test_pc_gnb_main = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT4SK084.p04.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_gnb_instance_id = 77084
_gnb_global_bts_id = 77084

_default_gnb_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_gnb_main.default_ssh_connection_details,
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
    ru_hw_group="AQQA",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    radio_type="AQQA",
    serial_number="1M231704088",
    product_code="475695A.208",
    pdu_port=PduPort(pdu=_gnb_pdu_75_za04_left, port_no=3),
    lmi=SerialOverTcp(
       uart_mapping=[Remote(addr=NetworkAddress(v4="10.255.13.136"), port=2222)]
    )
)

_gnb_radio_unit_1 = RU(
    ru_hw_group="AQQA",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    radio_type="AQQA",
    serial_number="1M223105105",
    product_code="475695A.202",
    pdu_port=PduPort(pdu=_gnb_pdu_75_za04_left, port_no=2),
    lmi=SerialOverTcp(
       uart_mapping=[Remote(addr=NetworkAddress(v4="10.255.13.139"), port=2222)]
    )
)

_gnb_radio_unit_2 = RU(
    ru_hw_group="AQQA",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    radio_type="AQQA",
    serial_number="1M223105137",
    product_code="475695A.202",
    pdu_port=PduPort(pdu=_gnb_pdu_75_za04_left, port_no=1),
    lmi=SerialOverTcp(
       uart_mapping=[Remote(addr=NetworkAddress(v4="10.255.13.137"), port=2222)]
    )
)

_gnb_radio_unit_3 = RU(
    ru_hw_group="AQQA",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    radio_type="AQQA",
    serial_number="1M232109755",
    product_code="475695A.202",
    pdu_port=PduPort(pdu=_gnb_pdu_75_za04_right, port_no=4),
    lmi=SerialOverTcp(
    uart_mapping=[Remote(addr=NetworkAddress(v4="10.255.13.138"), port=2222)]
    )
 )

_gnb_capacity_unit_0 = CapacityUnit(
    addr="",
    hardware_type="ABIO",
    hardware_version="A.101",
    serial_number="L1204301231",
    product_code="475266A.101",
    slot_id=SlotId.B4,
    rus=[_gnb_radio_unit_0, _gnb_radio_unit_1, _gnb_radio_unit_2, _gnb_radio_unit_3],
)

_gnb_common_unit_0 = CommonUnit(
    lmp_connection=_default_gnb_ssh_lmp_connection,
    capacity_units=[_gnb_capacity_unit_0],
    hardware_type="ASIB",
    hardware_version="A.102",
    serial_number="DH212766979",
    mac_addr="",
    slot_id=SlotId.C2,
    pdu_port=PduPort(pdu=_gnb_pdu_48, port_no=4),
)

_airscale_gnb = Airscale(common_units=[_gnb_common_unit_0], product_code="473098A")

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

_gnb_main = ClassicalBts(
    cu=_cu_gnb,
    dus=[_du_gnb],
    instance_id=_gnb_instance_id,
    global_bts_id=_gnb_global_bts_id,
)

_test_pc_gnb_main.connections = [
    Connection(
        device=_gnb_main.dus[0].airscale.common_units[0],
        interface="eth1",
        interface_type="lmp",
    )
]

# ------------------------TL_CONFIGURATION------------------------
_ue_config = _set_abstract_lib_config_env("ue.yaml")

tl = TestLine(
    test_pc=_test_pc_gnb_main,
    gnbs=[_gnb_main],
    pdus=[_gnb_pdu_75_za04_right, _gnb_pdu_75_za04_left, _gnb_pdu_48],
    test_pcs=[_test_pc_gnb_main],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_ASIBR_ABIOB4_3xAQQA_ENB",
)

__all__ = ["tl"]
