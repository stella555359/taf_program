# Generated with TL configuration generator at 2025-09-11_06:49:55

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
from taf.config.testline.lmi import SerialOverTcp, Remote
from taf.config.testline.nms import NMS, NetAct
import os
import yaml

# ------------------------PDU_CONFIGURATION------------------------

_bts_pdu_0 = FPFH(
    port_numbers=[3],
    addr="fpfh-pc04-48-d01.d01-leg.krk-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

_bts_pdu_1 = FPFH(
    port_numbers=[4],
    addr="fpfh-pc04-23-d01.d01-leg.krk-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

_bts_ru_pdu_0 = FPFH(
    port_numbers=[4, 5, 6],
    addr="fpfh-pc07-48-d01.d01-leg.krk-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

_bts_ru_pdu_1 = FPFH(
    port_numbers=[4],
    addr="fpfh-pc05-40-d01.d01-leg.krk-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

# ------------------------RUS_CONFIGURATION------------------------

_radio_unit_ahpmdk_0 = RU(
    ru_hw_group="AHPMDK",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="WAH26M0DHuXSxpqpUSLmklXrKUfF4iPrXQ+8YULFNuM=",
    ),
    radio_type="AHPMDK",
    serial_number="L1254503787",
    product_code="476714A",
    pdu_port=PduPort(pdu=_bts_ru_pdu_0, port_no=4),
)

_radio_unit_ahfii_0 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="WAH26M0DHuXSxpqpUSLmklXrKUfF4iPrXQ+8YULFNuM=",
    ),
    radio_type="AHFII",
    serial_number="BL2228N40WL",
    product_code="475656A",
    pdu_port=PduPort(pdu=_bts_ru_pdu_0, port_no=6),
)

_radio_unit_ahca_0 = RU(
    ru_hw_group="AHCA",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="",
    ),
    radio_type="AHCA",
    serial_number="1M192827799",
    product_code="473966A",
    pdu_port=PduPort(pdu=_bts_ru_pdu_0, port_no=5),
)

_radio_unit_avqj_0 = RU(
    ru_hw_group="AVQJ",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og=",
    ),
    radio_type="AVQJ",
    serial_number="1M252100543",
    product_code="476724A",
    pdu_port=PduPort(pdu=_bts_ru_pdu_1, port_no=4),
)

# ------------------------GNB0_CONFIGURATION------------------------

_test_pc_gnb_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-T01PY083-1.d01.krk-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_gnb_0_instance_id = 85083
_gnb_0_global_bts_id = 85083

_gnb_0_primary_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_gnb_0.default_ssh_connection_details,
)

_gnb_0_oam_ip = NetworkAddress(
    v4="10.89.3.83/24",
    routing_v4=RoutingInformation(gateway="10.89.3.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_0_f1m_ip = NetworkAddress(
    v4="10.89.3.83/24",
    routing_v4=RoutingInformation(gateway="10.89.3.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_0_f1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_0_f1u_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_0_x2c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_0_x2u_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_0_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_0_s1u_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_0_xnc_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_0_xnu_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_0_ngc_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_0_ngu_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_0_oam_http_connection = HttpConnectionDetails(
    addr=_gnb_0_oam_ip.v4.split("/")[0],
    username="Nemuadmin",
    password="nemuuser",
    port=443,
)

_cu_gnb_0 = CU(
    backhaul_site_oam_ip=_gnb_0_oam_ip,
    oam_ssh_connection_details=_gnb_0_primary_ssh_lmp_connection,
    oam_http_connection_details=_gnb_0_oam_http_connection,
    f1m=_gnb_0_f1m_ip,
    f1c=_gnb_0_f1c_ip,
    f1u=_gnb_0_f1u_ip,
    x2c=_gnb_0_x2c_ip,
    x2u=_gnb_0_x2u_ip,
    s1c=_gnb_0_s1c_ip,
    s1u=_gnb_0_s1u_ip,
    xnc=_gnb_0_xnc_ip,
    xnu=_gnb_0_xnu_ip,
    ngc=_gnb_0_ngc_ip,
    ngu=_gnb_0_ngu_ip,
    instance_id=_gnb_0_instance_id,
    global_bts_id=_gnb_0_global_bts_id,
)

_gnb_0_capacity_unit_0 = CapacityUnit(
    addr="192.168.253.22",
    hardware_type="ABIA",
    hardware_version="A.103",
    serial_number="L1164712639",
    product_code="473096A.103",
    slot_id=SlotId.B1,
    rus=[
        _radio_unit_ahpmdk_0,
    ],
)

_gnb_0_capacity_unit_1 = CapacityUnit(
    addr="192.168.253.26",
    hardware_type="ABIQ",
    hardware_version="A.101",
    serial_number="L1232208174",
    product_code="476397A.101",
    slot_id=SlotId.B2,
    rus=[
        _radio_unit_ahca_0,
        _radio_unit_ahfii_0,
        _radio_unit_avqj_0,
    ],
)

_gnb_0_capacity_unit_2 = CapacityUnit(
    addr="192.168.253.30",
    hardware_type="ABIQ",
    hardware_version="A.102",
    serial_number="L1241505051",
    product_code="476397A.101",
    slot_id=SlotId.B3,
    rus=[
        _radio_unit_ahpmdk_0,
        _radio_unit_ahfii_0,
    ],
)

_gnb_0_common_unit_0 = CommonUnit(
    lmp_connection=_gnb_0_primary_ssh_lmp_connection,
    capacity_units=[
        _gnb_0_capacity_unit_0,
        _gnb_0_capacity_unit_1,
        _gnb_0_capacity_unit_2,
    ],
    hardware_type="ASIM",
    hardware_version="A.104",
    serial_number="L1233406321",
    mac_addr="28:74:f5:0b:62:9",
    # trs_connections=[TRSInterfaces.EIF1],
    slot_id=SlotId.C1,
    pdu_port=PduPort(pdu=_bts_pdu_0, port_no=3),
)

_gnb_0_airscale = Airscale(
    common_units=[_gnb_0_common_unit_0],
    product_code="475773A",
)

_du_gnb_0 = DU(
    airscale=_gnb_0_airscale,
    oam_ip=_gnb_0_oam_ip,
    f1_m_ip_addr=_gnb_0_f1m_ip,
    f1_c_ip_addr=_gnb_0_f1c_ip,
    f1_u_ip_addr=_gnb_0_f1u_ip,
    f1_m_cu=_gnb_0_f1m_ip,
    f1_c_cu=_gnb_0_f1c_ip,
    f1_u_cu=_gnb_0_f1u_ip,
    instance_id=_gnb_0_instance_id,
    global_bts_id=_gnb_0_global_bts_id,
)

_gnb_0 = ClassicalBts(
    cu=_cu_gnb_0,
    dus=[_du_gnb_0],
    instance_id=_gnb_0_instance_id,
    global_bts_id=_gnb_0_global_bts_id,
)

_test_pc_gnb_0.connections = [
    Connection(
        device=_gnb_0.dus[0].airscale.common_units[0],
        interface="eth1",
        interface_type="lmp",
    )
]

# ------------------------GNB1_CONFIGURATION------------------------

_test_pc_gnb_1 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-T01PY083-2.d01.krk-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_gnb_1_instance_id = 85089
_gnb_1_global_bts_id = 85089

_gnb_1_primary_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_gnb_1.default_ssh_connection_details,
)

_gnb_1_oam_ip = NetworkAddress(
    v4="10.89.3.89/24",
    routing_v4=RoutingInformation(gateway="10.89.3.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_1_f1m_ip = NetworkAddress(
    v4="10.89.3.89/24",
    routing_v4=RoutingInformation(gateway="10.89.3.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_1_f1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_1_f1u_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_1_x2c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_1_x2u_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_1_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_1_s1u_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_1_xnc_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_1_xnu_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_1_ngc_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_1_ngu_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_1_oam_http_connection = HttpConnectionDetails(
    addr=_gnb_1_oam_ip.v4.split("/")[0],
    username="Nemuadmin",
    password="nemuuser",
    port=443,
)

_cu_gnb_1 = CU(
    backhaul_site_oam_ip=_gnb_1_oam_ip,
    oam_ssh_connection_details=_gnb_1_primary_ssh_lmp_connection,
    oam_http_connection_details=_gnb_1_oam_http_connection,
    f1m=_gnb_1_f1m_ip,
    f1c=_gnb_1_f1c_ip,
    f1u=_gnb_1_f1u_ip,
    x2c=_gnb_1_x2c_ip,
    x2u=_gnb_1_x2u_ip,
    s1c=_gnb_1_s1c_ip,
    s1u=_gnb_1_s1u_ip,
    xnc=_gnb_1_xnc_ip,
    xnu=_gnb_1_xnu_ip,
    ngc=_gnb_1_ngc_ip,
    ngu=_gnb_1_ngu_ip,
    instance_id=_gnb_1_instance_id,
    global_bts_id=_gnb_1_global_bts_id,
)

_gnb_1_capacity_unit_0 = CapacityUnit(
    addr="192.168.253.22",
    hardware_type="ABIQ",
    hardware_version="A.102",
    serial_number="",
    product_code="476397A.102",
    slot_id=SlotId.B4,
    rus=[_radio_unit_ahpmdk_0],
)

_gnb_1_capacity_unit_1 = CapacityUnit(
    addr="192.168.253.26",
    hardware_type="ABIQ",
    hardware_version="A.102",
    serial_number="",
    product_code="476397A.102",
    slot_id=SlotId.B5,
    rus=[
        _radio_unit_ahca_0,
        _radio_unit_ahfii_0,
    ],
)

_gnb_1_common_unit_0 = CommonUnit(
    lmp_connection=_gnb_1_primary_ssh_lmp_connection,
    capacity_units=[
        _gnb_1_capacity_unit_0,
        _gnb_1_capacity_unit_1,
    ],
    hardware_type="ASIM",
    hardware_version="A.104",
    serial_number="",
    mac_addr="28:74:f5:0b:74:87",
    # trs_connections=[TRSInterfaces.EIF1],
    slot_id=SlotId.C2,
    pdu_port=PduPort(pdu=_bts_pdu_1, port_no=4),
)

_gnb_1_airscale = Airscale(
    common_units=[_gnb_1_common_unit_0],
    product_code="475773A",
)

_du_gnb_1 = DU(
    airscale=_gnb_1_airscale,
    oam_ip=_gnb_1_oam_ip,
    f1_m_ip_addr=_gnb_1_f1m_ip,
    f1_c_ip_addr=_gnb_1_f1c_ip,
    f1_u_ip_addr=_gnb_1_f1u_ip,
    f1_m_cu=_gnb_1_f1m_ip,
    f1_c_cu=_gnb_1_f1c_ip,
    f1_u_cu=_gnb_1_f1u_ip,
    instance_id=_gnb_1_instance_id,
    global_bts_id=_gnb_1_global_bts_id,
)

_gnb_1 = ClassicalBts(
    cu=_cu_gnb_1,
    dus=[_du_gnb_1],
    instance_id=_gnb_1_instance_id,
    global_bts_id=_gnb_1_global_bts_id,
)

_test_pc_gnb_1.connections = [
    Connection(
        device=_gnb_1.dus[0].airscale.common_units[0],
        interface="eth1",
        interface_type="lmp",
    )
]


# --------------------------MantaRay netact------------------------
_nms = NMS(
    netact=NetAct(
        ssh_connections_info=SshServiceDetails(
            addr="10.43.48.76",
            username="omc",
            password="Medsql!_1893",
        ),
        https_main_info=HttpConnectionDetails(
            addr="srnclab1044lbwas.srnblr.nsn-rdnet.net",
        ),
    ),
)

# ------------------------UE_CONFIGURATION------------------------


def _set_abstract_lib_config_env(ue_config_file):
    tl_config_dir = os.path.dirname(os.path.abspath(__file__))
    ue_config_abs_path = os.path.join(tl_config_dir, ue_config_file)
    with open(ue_config_abs_path) as ta_ue_config:
        ue_config = yaml.safe_load(ta_ue_config)
    os.environ["ABSTRACT_LIB_CONFIG"] = ue_config_abs_path
    return ue_config


_set_abstract_lib_config_env("ue.yaml")

# ------------------------TL_CONFIGURATION------------------------


tl = TestLine(
    test_pc=_test_pc_gnb_0,
    gnbs=[_gnb_0, _gnb_1],
    test_pcs=[_test_pc_gnb_0, _test_pc_gnb_1],
    tl_cloud_topology="CLOUD_7_7_T01PY083",
    nms=_nms,
)

tl.netact_dn = 'PLMN-PLMN/MRBTS-85083'

__all__ = ["tl"]
