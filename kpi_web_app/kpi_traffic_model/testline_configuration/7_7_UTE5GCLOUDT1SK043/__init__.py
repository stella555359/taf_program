__maintainer__ = "Mateusz Iwankiewicz"
__team__ = "I_MN_RAN_PZ_KRK_SG_8_GMS"
__email__ = "I_MN_RAN_PZ_KRK_SG_8@internal.nsn.com"
__owner_email__ = "mateusz.iwankiewicz@nokia.com"

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


def _set_abstract_lib_config_env(ue_config_file):
    tl_config_dir = os.path.dirname(os.path.abspath(__file__))
    ue_config_abs_path = os.path.join(tl_config_dir, ue_config_file)
    with open(ue_config_abs_path) as ta_ue_config:
        ue_config = yaml.safe_load(ta_ue_config)
    os.environ["ABSTRACT_LIB_CONFIG"] = ue_config_abs_path
    return ue_config


# ------------------------PDU_CONFIGURATION------------------------

_bts_pdu = FPFH(
    port_numbers=[1, 2, 3, 4, 5, 6],
    addr="fpfh-zg11-48-p01.p01-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

# ------------------------GNB_CONFIGURATION------------------------

_gnb_oam_ip = NetworkAddress(
    v4="10.84.164.43/23",
    routing_v4=RoutingInformation(gateway="10.84.151.254", destIpAddr="10.84.169.0"),
    vlan_id=0,
)

_gnb_f1m_ip = NetworkAddress(
    v4="10.84.164.43/23",
    routing_v4=RoutingInformation(gateway="10.84.151.254", destIpAddr="10.84.169.0"),
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
    v4="10.84.150.43/23",
    routing_v4=RoutingInformation(gateway="10.84.151.254", destIpAddr="10.84.169.0"),
    vlan_id=507,
)

_gnb_x2u_ip = NetworkAddress(
    v4="10.84.150.43/23",
    routing_v4=RoutingInformation(gateway="10.84.151.254", destIpAddr="10.84.169.0"),
    vlan_id=507,
)

_gnb_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_s1u_ip = NetworkAddress(
    v4="10.84.150.43/23",
    routing_v4=RoutingInformation(gateway="10.84.151.254", destIpAddr="10.84.169.0"),
    vlan_id=507,
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

_test_pc_gnb = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT1SK043.p01.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_gnb_instance_id = 76043
_gnb_global_bts_id = 76043

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
    ru_hw_group="AEWB",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="wv48zrV4zEjjQ5nIWXuwfWlQ23oNBkEr7/5AMdaUDIQ=",
    ),
    radio_type="AEWB",
    serial_number="AH201501318",
    product_code="474609A.103",
    pdu_port=PduPort(pdu=_bts_pdu, port_no=6),
    # lmi=SerialOverHost(
    #     host=TestPc(
    #         default_ssh_connection_details=SshServiceDetails(
    #             addr="plkr-tp-ue104.intra.noklab.net",
    #             username=r"pzkrk",
    #             password="NokiaBts2003",
    #         )
    #     ),
    #     uart_mapping=[Local(port="COM4")],
    # ),
)

_gnb_radio_unit_1 = RU(
    ru_hw_group="AEWB",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="wv48zrV4zEjjQ5nIWXuwfWlQ23oNBkEr7/5AMdaUDIQ=",
    ),
    radio_type="AEWB",
    serial_number="AH195105306",
    product_code="474609A.103",
    pdu_port=PduPort(pdu=_bts_pdu, port_no=5),
    # lmi=SerialOverHost(
    #     host=TestPc(
    #         default_ssh_connection_details=SshServiceDetails(
    #             addr="plkr-tp-ue104.intra.noklab.net",
    #             username=r"pzkrk",
    #             password="NokiaBts2003",
    #         )
    #     ),
    #     uart_mapping=[Local(port="COM3")],
    # ),
)

_gnb_radio_unit_2 = RU(
    ru_hw_group="AEWB",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="wv48zrV4zEjjQ5nIWXuwfWlQ23oNBkEr7/5AMdaUDIQ=",
    ),
    radio_type="AEWB",
    serial_number="AH201501422",
    product_code="474609A.103",
    pdu_port=PduPort(pdu=_bts_pdu, port_no=4),
    # lmi=SerialOverHost(
    #     host=TestPc(
    #         default_ssh_connection_details=SshServiceDetails(
    #             addr="plkr-tp-ue104.intra.noklab.net",
    #             username=r"pzkrk",
    #             password="NokiaBts2003",
    #         )
    #     ),
    #     uart_mapping=[Local(port="COM5")],
    # ),
)

_gnb_capacity_unit_0 = CapacityUnit(
    addr="192.168.253.30",
    hardware_type="ABIL",
    hardware_version="A.102",
    serial_number="EA194551478",
    product_code="474020A.102",
    slot_id=SlotId.B3,
    rus=[_gnb_radio_unit_1],
)

_gnb_capacity_unit_1 = CapacityUnit(
    addr="192.168.253.26",
    hardware_type="ABIL",
    hardware_version="A.102",
    serial_number="EA200750972",
    product_code="474020A.102",
    slot_id=SlotId.B2,
    rus=[_gnb_radio_unit_2],
)

_gnb_capacity_unit_2 = CapacityUnit(
    addr="192.168.253.22",
    hardware_type="ABIL",
    hardware_version="B.101",
    serial_number="EA195160103",
    product_code="474020B.101",
    slot_id=SlotId.B1,
    rus=[_gnb_radio_unit_0],
)

_gnb_common_unit_0 = CommonUnit(
    lmp_connection=_default_gnb_ssh_lmp_connection,
    capacity_units=[_gnb_capacity_unit_0, _gnb_capacity_unit_1, _gnb_capacity_unit_2],
    hardware_type="ASIK",
    hardware_version="A.101",
    serial_number="L1190401108",
    mac_addr="",
    # trs_connections=[],
    slot_id=SlotId.C1,
    pdu_port=PduPort(pdu=_bts_pdu, port_no=2),
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

# ------------------------TL_CONFIGURATION------------------------

_ue_config = _set_abstract_lib_config_env("ue_config.yaml")

tl = TestLine(
    test_pc=_test_pc_gnb,
    gnbs=[_gnb],
    enbs=[],
    test_pcs=[_test_pc_gnb],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_ASIK_3xABIL_3xAEWB",
)

__all__ = ["tl"]
