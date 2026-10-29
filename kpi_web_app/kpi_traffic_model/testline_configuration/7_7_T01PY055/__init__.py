# Generated with TL configuration generator at 2025-08-06_10:53:50

# Repository  -> https://wrgitlab.int.net.nokia.com/ran_pz_krk/config_generator
# Jenkins job -> http://krk-pz-jenkins.krk-lab.nsn-rdnet.net:5990/view/Tools/job/Config_Generator/build?delay=0sec

__maintainer__ = "KRKAUTO5GPZ"
__team__ = "I_MN_RAN_VRF_KRK_T03"
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
from taf.config.testline.lmi import SerialOverHost, Local, Remote, SerialOverTcp
import os
import yaml

# ------------------------FPFH_CONFIGURATION------------------------

_bts_fpfh_17 = FPFH(
    port_numbers=[1, 2, 3],
    addr="fpfh-pb05-46-d01.d01-leg.krk-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

_bts_fpfh_18 = FPFH(
    port_numbers=[1, 2, 3, 4],
    addr="fpfh-pb05-22-d01.d01-leg.krk-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

_bts_fpfh_20 = FPFH(
    port_numbers=[1, 2, 3],
    addr="fpfh-pb03-46-d01.d01-leg.krk-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)


# ------------------------GNB0_CONFIGURATION------------------------

_test_pc_gnb_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-T01PY055.d01.krk-lab.nsn-rdnet.net",
        username="ute",
        password="UTE.debian12",
    )
)

_gnb_0_instance_id = 85055
_gnb_0_global_bts_id = 85055

_gnb_0_primary_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_gnb_0.default_ssh_connection_details,
)

_gnb_0_oam_ip = NetworkAddress(
    v4="10.89.3.55/23",
    routing_v4=RoutingInformation(gateway="10.89.3.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_0_f1m_ip = NetworkAddress(
    v4="10.89.3.55/23",
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
    v4="10.89.4.55/23",
    routing_v4=RoutingInformation(gateway="10.89.3.254", destIpAddr="0.0.0.0"),
    vlan_id=507,
)

_gnb_0_x2u_ip = NetworkAddress(
    v4="10.254.5.55/23",
    routing_v4=RoutingInformation(gateway="10.89.3.254", destIpAddr="0.0.0.0"),
    vlan_id=506,
)

_gnb_0_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_0_s1u_ip = NetworkAddress(
    v4="10.254.5.55/23",
    routing_v4=RoutingInformation(gateway="10.89.3.254", destIpAddr="0.0.0.0"),
    vlan_id=506,
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

_gnb_0_radio_unit_0 = RU(
    ru_hw_group="AHPCA",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHPCA",
    serial_number="BL2215B2G25",
    product_code="475075A.101",
    pdu_port=PduPort(pdu=_bts_fpfh_18, port_no=4),
    lmi=SerialOverHost(
        host=TestPc(
            default_ssh_connection_details=SshServiceDetails(
                addr="PLKR-SC5G-PC124.d01.krk-lab.nsn-rdnet.net",
                username=r"pzkrk",
                password="NokiaBts2003",
            )
        ),
        uart_mapping=[Local(port="COM13")],
    ),
)

_gnb_0_radio_unit_1 = RU(
    ru_hw_group="AHFIHA",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFIHA",
    serial_number="RW252101877",
    product_code="475964A.102",
    pdu_port=PduPort(pdu=_bts_fpfh_17, port_no=3),
    lmi=SerialOverTcp(
        uart_mapping=[Remote(addr=NetworkAddress(v4="10.255.60.59"), port=2222)]
    ),
)

_gnb_0_radio_unit_2 = RU(
    ru_hw_group="AHPCA",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHPCA",
    serial_number="BL2215B2FXE",
    product_code="475075A.101",
    pdu_port=PduPort(pdu=_bts_fpfh_18, port_no=3),
    lmi=SerialOverHost(
        host=TestPc(
            default_ssh_connection_details=SshServiceDetails(
                addr="PLKR-SC5G-PC124.d01.krk-lab.nsn-rdnet.net",
                username=r"pzkrk",
                password="NokiaBts2003",
            )
        ),
        uart_mapping=[Local(port="COM8")],
    ),
)

_gnb_0_radio_unit_3 = RU(
    ru_hw_group="AHPCA",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHPCA",
    serial_number="BL2215B2FXF",
    product_code="475075A.101",
    pdu_port=PduPort(pdu=_bts_fpfh_18, port_no=2),
    lmi=SerialOverHost(
        host=TestPc(
            default_ssh_connection_details=SshServiceDetails(
                addr="PLKR-SC5G-PC124.d01.krk-lab.nsn-rdnet.net",
                username=r"pzkrk",
                password="NokiaBts2003",
            )
        ),
        uart_mapping=[Local(port="COM8")],
    ),
)

_gnb_0_radio_unit_4 = RU(
    ru_hw_group="AVQA",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og=",
    ),
    radio_type="AVQA",
    serial_number="L1251900662",
    product_code="476457A.101",
    pdu_port=PduPort(pdu=_bts_fpfh_20, port_no=2),
    lmi=SerialOverTcp(
        uart_mapping=[Remote(addr=NetworkAddress(v4="10.255.60.56"), port=2222)]
    ),
)

_gnb_0_radio_unit_5 = RU(
    ru_hw_group="AVQA",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og=",
    ),
    radio_type="AVQA",
    serial_number="L1251900661",
    product_code="476457A.101",
    pdu_port=PduPort(pdu=_bts_fpfh_20, port_no=1),
    lmi=SerialOverTcp(
        uart_mapping=[Remote(addr=NetworkAddress(v4="10.255.60.57"), port=2222)]
    ),
)

_gnb_0_radio_unit_6 = RU(
    ru_hw_group="AHFIHA",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFIHA",
    serial_number="RW252101871",
    product_code="475964A.102",
    pdu_port=PduPort(pdu=_bts_fpfh_17, port_no=2),
    lmi=SerialOverTcp(
        uart_mapping=[Remote(addr=NetworkAddress(v4="10.255.60.58"), port=2222)]
    ),
)

_gnb_0_radio_unit_7 = RU(
    ru_hw_group="AVQA",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og=",
    ),
    radio_type="AVQA",
    serial_number="L1252003268",
    product_code="476457A.101",
    pdu_port=PduPort(pdu=_bts_fpfh_20, port_no=3),
    lmi=SerialOverTcp(
        uart_mapping=[Remote(addr=NetworkAddress(v4="10.255.60.55"), port=2222)]
    ),
)

_gnb_0_radio_unit_8 = RU(
    ru_hw_group="AHFIHA",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFIHA",
    serial_number="RW252101889",
    product_code="475964A.102",
    pdu_port=PduPort(pdu=_bts_fpfh_18, port_no=1),
    lmi=SerialOverTcp(
        uart_mapping=[Remote(addr=NetworkAddress(v4="10.255.60.60"), port=2222)]
    ),
)

_gnb_0_capacity_unit_0 = CapacityUnit(
    addr="192.168.253.22",
    hardware_type="ABIQ",
    hardware_version="A.102",
    serial_number="L1234102917",
    product_code="476397A.102",
    slot_id=SlotId.B1,
    rus=[_gnb_0_radio_unit_4, _gnb_0_radio_unit_5, _gnb_0_radio_unit_7],
)

_gnb_0_capacity_unit_1 = CapacityUnit(
    addr="192.168.253.30",
    hardware_type="ABIA",
    hardware_version="A.104",
    serial_number="EA194751703",
    product_code="473096A.104",
    slot_id=SlotId.B3,
    rus=[_gnb_0_radio_unit_0, _gnb_0_radio_unit_2, _gnb_0_radio_unit_3],
)

_gnb_0_capacity_unit_2 = CapacityUnit(
    addr="192.168.253.26",
    hardware_type="ABIQ",
    hardware_version="A.102",
    serial_number="L1241408105",
    product_code="476397A.102",
    slot_id=SlotId.B2,
    rus=[
        _gnb_0_radio_unit_0,
        _gnb_0_radio_unit_1,
        _gnb_0_radio_unit_2,
        _gnb_0_radio_unit_3,
        _gnb_0_radio_unit_6,
        _gnb_0_radio_unit_8,
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
    serial_number="L1243004617",
    mac_addr="d0:48:4f:04:76:0",
    # trs_connections=[TRSInterfaces.EIF1],
    slot_id=SlotId.C1,
    pdu_port=PduPort(pdu=_bts_fpfh_17, port_no=1),
)

_gnb_0_airscale = Airscale(
    common_units=[_gnb_0_common_unit_0],
    product_code="473098A",
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
    gnbs=[_gnb_0],
    test_pcs=[_test_pc_gnb_0],
    tl_cloud_topology="Please complete the cloud topology or remove this line",
)

__all__ = ["tl"]
