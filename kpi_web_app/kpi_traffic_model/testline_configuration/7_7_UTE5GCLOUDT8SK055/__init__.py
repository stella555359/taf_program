# Generated with TL configuration generator at 2024-01-04_10:28:27

# Repository  -> https://wrgitlab.int.net.nokia.com/ran_pz_krk/config_generator
# Jenkins job -> http://krk-pz-jenkins.krk-lab.nsn-rdnet.net:5990/view/Tools/job/Config_Generator/build?delay=0sec

__maintainer__ = "KRKAUTO5GPZ"
__team__ = "I_MN_RAN_PZ_KRK_TAG"
__email__ = "I_MN_RAN_PZ_KRK_TAG@internal.nsn.com"

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
import os
import yaml

# ------------------------PDU_CONFIGURATION------------------------

_gnb_pdu = FPFH(
    port_numbers=[1, 5, 6],
    addr="fpfh-zg07-48-p08.p08-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

_gnb_ru_pdu_1 = FPFH(
    port_numbers=[4, 5, 6],
    addr="fpfh-zg09-48-p08.p08-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

_gnb_ru_pdu_2 = FPFH(
    port_numbers=[3, 4, 5, 6],
    addr="fpfh-zg07-28-p08.p08-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)


# ------------------------GNB_CONFIGURATION------------------------

_gnb_oam_ip = NetworkAddress(
    v4="10.84.152.55/23",
    routing_v4=RoutingInformation(gateway="10.84.153.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_f1m_ip = NetworkAddress(
    v4="10.84.152.55/23",
    routing_v4=RoutingInformation(gateway="10.84.153.254", destIpAddr="0.0.0.0"),
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
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_x2u_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_s1u_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_xnc_ip = NetworkAddress(
    v4="10.84.154.55/24",
    routing_v4=RoutingInformation(gateway="10.84.153.254", destIpAddr="0.0.0.0"),
    vlan_id=507,
)

_gnb_xnu_ip = NetworkAddress(
    v4="10.255.28.55/23",
    routing_v4=RoutingInformation(gateway="10.84.153.254", destIpAddr="0.0.0.0"),
    vlan_id=505,
)

_gnb_ngc_ip = NetworkAddress(
    v4="10.84.154.55/24",
    routing_v4=RoutingInformation(gateway="10.84.153.254", destIpAddr="0.0.0.0"),
    vlan_id=507,
)

_gnb_ngu_ip = NetworkAddress(
    v4="10.255.28.55/23",
    routing_v4=RoutingInformation(gateway="10.84.153.254", destIpAddr="0.0.0.0"),
    vlan_id=505,
)

_test_pc_gnb = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT8SK055.p08.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_gnb_instance_id = 79055
_gnb_global_bts_id = 79055

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
    ru_hw_group="AQQJ",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    radio_type="AQQJ",
    serial_number="K9233016047",
    product_code="476383A.108",
    pdu_port=PduPort(pdu=_gnb_ru_pdu_1, port_no=4),
)

_gnb_radio_unit_1 = RU(
    ru_hw_group="AQQJ",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    radio_type="AQQJ",
    serial_number="1M230700947",
    product_code="476383A.103",
    pdu_port=PduPort(pdu=_gnb_ru_pdu_1, port_no=6),
)

_gnb_radio_unit_2 = RU(
    ru_hw_group="AQQJ",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    radio_type="AQQJ",
    serial_number="1M230700980",
    product_code="476383A.103",
    pdu_port=PduPort(pdu=_gnb_ru_pdu_1, port_no=5),
)

_gnb_radio_unit_3 = RU(
    ru_hw_group="AHPB",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="",
    ),
    radio_type="AHPB",
    serial_number="K9182839872",
    product_code="474119A.101",
    pdu_port=PduPort(pdu=_gnb_ru_pdu_2, port_no=5),
)

_gnb_radio_unit_4 = RU(
    ru_hw_group="AHPB",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="",
    ),
    radio_type="AHPB",
    serial_number="EA222355911",
    product_code="474119A.101",
    pdu_port=PduPort(pdu=_gnb_ru_pdu_2, port_no=3),
)

_gnb_radio_unit_5 = RU(
    ru_hw_group="AHPB",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="",
    ),
    radio_type="AHPB",
    serial_number="EA222356194",
    product_code="474119A.101",
    pdu_port=PduPort(pdu=_gnb_ru_pdu_2, port_no=4),
)

_gnb_radio_unit_6 = RU(
    ru_hw_group="FRIJ",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="",
    ),
    radio_type="FRIJ",
    serial_number="EA194364620",
    product_code="473368A.101",
    pdu_port=PduPort(pdu=_gnb_ru_pdu_2, port_no=6),
)

_gnb_radio_unit_7 = RU(
    ru_hw_group="FRIJ",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="",
    ),
    radio_type="FRIJ",
    serial_number="EA194364645",
    product_code="473368A.101",
    pdu_port=PduPort(pdu=_gnb_pdu, port_no=6),
)

_gnb_radio_unit_8 = RU(
    ru_hw_group="FRIJ",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="",
    ),
    radio_type="FRIJ",
    serial_number="EA194364632",
    product_code="473368A.101",
    pdu_port=PduPort(pdu=_gnb_pdu, port_no=1),
)

_gnb_core_unit_0 = CoreUnit(
    lmp_connection=_default_gnb_ssh_lmp_connection,
    hardware_type="ASOH",
    hardware_version="A.101",
    serial_number="L1242202499",
    mac_addr="",
    # trs_connections=[],
    rus=[
        _gnb_radio_unit_0,
        _gnb_radio_unit_1,
        _gnb_radio_unit_2,
        _gnb_radio_unit_3,
        _gnb_radio_unit_4,
        _gnb_radio_unit_5,
        _gnb_radio_unit_6,
        _gnb_radio_unit_7,
        _gnb_radio_unit_8,
    ],
    pdu_port=PduPort(pdu=_gnb_pdu, port_no=5),
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

# ------------------------UE_CONFIGURATION------------------------


def _set_abstract_lib_config_env(ue_config_file):
    tl_config_dir = os.path.dirname(os.path.abspath(__file__))
    ue_config_abs_path = os.path.join(tl_config_dir, ue_config_file)
    with open(ue_config_abs_path) as ta_ue_config:
        ue_config = yaml.safe_load(ta_ue_config)
    os.environ["ABSTRACT_LIB_CONFIG"] = ue_config_abs_path
    return ue_config


_ue = _set_abstract_lib_config_env("ue.yaml")

# ------------------------TL_CONFIGURATION------------------------


tl = TestLine(
    test_pc=_test_pc_gnb,
    gnbs=[_gnb],
    test_pcs=[_test_pc_gnb],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_ANDROID_ASOH_3xAQQJ_3xAHPB_3xFRIJ",
)

__all__ = ["tl"]
