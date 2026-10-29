__maintainer__ = "Jakub Kowalczyk"
__team__ = "MN RAN RD VRF KRK 7"
__email__ = "jakub.kowalczyk@nokia.com"

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
from taf.config.testline.pdu import PduPort, FPFH
import os
import yaml
from taf.config.testline import JFW


def _set_abstract_lib_config_env(ue_config_file):
    tl_config_dir = os.path.dirname(os.path.abspath(__file__))

    ue_config_abs_path = os.path.join(tl_config_dir, ue_config_file)

    with open(ue_config_abs_path) as ta_ue_config:
        ue_config = yaml.safe_load(ta_ue_config)
    os.environ["ABSTRACT_LIB_CONFIG"] = ue_config_abs_path

    return ue_config


# ------------------------PDU_CONFIGURATION------------------------

_bts_ru_pdu = FPFH(
    addr="FPFH-GI07-46-SC5G.sc5g-leg.krk-lab.nsn-rdnet.net",
    port_numbers=[
        5,  # ASIB L1192904071
        1,  # FXEF K9173120831
        2,  # FXEF K9173120869
        3,  # FXEF K9171809795
        4,  # FXEF EA180412405
    ],
    login="admin",
    password="admin",
)

_ru_pdu = FPFH(
    addr="FPFH-GI07-22-SC5G.sc5g-leg.krk-lab.nsn-rdnet.net",
    port_numbers=[
        1,  # FXED F7154748457
        2,  # FXED L1174405578
    ],
    login="admin",
    password="admin",
)


# ------------------------GNB_CONFIGURATION------------------------

_gnb_oam_ip = NetworkAddress(
    v4="10.83.182.166/23",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=503,
)

_gnb_f1m_ip = NetworkAddress(
    v4="10.83.182.166/23",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=503,
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
    v4="10.83.182.166/23",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=503,
)

_gnb_x2u_ip = NetworkAddress(
    v4="10.83.182.166/23",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=503,
)

_gnb_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_s1u_ip = NetworkAddress(
    v4="10.83.182.166/23",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=503,
)

_gnb_xnc_ip = NetworkAddress(
    v4="10.83.182.166/23",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=503,
)

_gnb_xnu_ip = NetworkAddress(
    v4="10.83.182.166/23",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=503,
)

_gnb_ngc_ip = NetworkAddress(
    v4="10.83.182.166/23",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=503,
)

_gnb_ngu_ip = NetworkAddress(
    v4="10.83.182.166/23",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=503,
)

_test_pc_gnb = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT166.sc5g.krk-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_gnb_instance_id = 75166
_gnb_global_bts_id = 75166

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
    ru_hw_group="FXEF",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="FXEF",
    serial_number="K9171809795",
    product_code="473439A.202",
    pdu_port=PduPort(pdu=_bts_ru_pdu, port_no=3),
)

_gnb_radio_unit_1 = RU(
    ru_hw_group="FXEF",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="FXEF",
    serial_number="EA180412405",
    product_code="473439A.202",
    pdu_port=PduPort(pdu=_bts_ru_pdu, port_no=4),
)

_gnb_radio_unit_2 = RU(
    ru_hw_group="FXEF",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="FXEF",
    serial_number="K9173120831",
    product_code="473439A.202",
    pdu_port=PduPort(pdu=_bts_ru_pdu, port_no=1),
)

_gnb_radio_unit_3 = RU(
    ru_hw_group="FXED",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="FXED",
    serial_number="F7154748457",
    product_code="472924A.101",
    pdu_port=PduPort(pdu=_ru_pdu, port_no=1),
)

_gnb_radio_unit_4 = RU(
    ru_hw_group="FXEF",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="FXEF",
    serial_number="K9173120869",
    product_code="473439A.202",
    pdu_port=PduPort(pdu=_bts_ru_pdu, port_no=2),
)

_gnb_radio_unit_5 = RU(
    ru_hw_group="FXED",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="FXED",
    serial_number="L1174405578",
    product_code="472924A.203",
    pdu_port=PduPort(pdu=_ru_pdu, port_no=2),
)

_gnb_capacity_unit_0 = CapacityUnit(
    addr="",
    hardware_type="ABIQ",
    hardware_version="A.102",
    serial_number="L1233104891",
    product_code="476397A.102",
    slot_id=SlotId.B1,
    rus=[_gnb_radio_unit_2, _gnb_radio_unit_3, _gnb_radio_unit_4, _gnb_radio_unit_5],
)

_gnb_capacity_unit_1 = CapacityUnit(
    addr="",
    hardware_type="ABIQ",
    hardware_version="A.102",
    serial_number="L1233105825",
    product_code="476397A.102",
    slot_id=SlotId.B2,
    rus=[_gnb_radio_unit_0, _gnb_radio_unit_1],
)

_gnb_common_unit_0 = CommonUnit(
    lmp_connection=_default_gnb_ssh_lmp_connection,
    capacity_units=[_gnb_capacity_unit_0, _gnb_capacity_unit_1],
    hardware_type="ASIB",
    hardware_version="A.102",
    serial_number="L1192904071",
    mac_addr="",
    # trs_connections=[],
    slot_id=SlotId.C1,
    pdu_port=PduPort(pdu=_bts_ru_pdu, port_no=5),
)

_airscale_gnb = Airscale(
    common_units=[_gnb_common_unit_0],
    product_code="473098A",
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
        device=_gnb.dus[0].airscale.common_units[0],
        interface="eth1",
        interface_type="lmp",
    )
]
# ------------------------ATTENUATOR_CONFIGURATION------------------------

_attenuator = JFW(
    ip_addr="10.253.166.20",
    port=3001,
    attenuation_port_numbers=range(1, 6 + 1),
    model="50PA-775",
)

# ------------------------TL_CONFIGURATION------------------------

_quectel = _set_abstract_lib_config_env("ue_config.yaml")
_ue_config = _set_abstract_lib_config_env("ue_config.yaml")

tl = TestLine(
    test_pc=_test_pc_gnb,
    gnbs=[_gnb],
    test_pcs=[_test_pc_gnb],
    ues=[_ue_config],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_QUECTEL_SA_ASIB_ABIQB1B2_2xFXED_4xFXEF_MRAT",
    pdus=[_bts_ru_pdu, _ru_pdu],
    attenuator=[_attenuator],
)

__all__ = ["tl"]
