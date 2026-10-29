__maintainer__ = "Karol Lapczyk"
__team__ = "5G_PZ_MMW_KRK_3_SG"
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
_gnb_pdu_za03_41 = FPFH(
    port_numbers=[1, 2, 3],
    addr="fpfh-za03-41-p04.p04-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

_gnb_pdu_za06_32 = FPFH(
    port_numbers=[1, 2, 3, 4, 5],
    addr="fpfh-za06-32-p04.p04-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

_gnb_pdu_za06_48 = FPFH(
    port_numbers=[3, 4, 6],
    addr="fpfh-za06-48-p04.p04-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

_gnb_oam_ip = NetworkAddress(
    v4="10.84.190.83/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_f1m_ip = NetworkAddress(
    v4="10.84.190.83/23",
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
        addr="7-7-UTE5GCLOUDT4SK083.p04.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_gnb_instance_id = 77083
_gnb_global_bts_id = 77083

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

_secondary_gnb_ssh_lmp_connection = SshServiceDetails(
    addr="",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_gnb_main.default_ssh_connection_details,
)

gnb_capacity_unit_0 = CapacityUnit(
    addr="root@fct-4a:~",
    hardware_type="BB",
    hardware_version="A.103",
    serial_number="F7173768894",
    product_code="472182A.103",
)

gnb_capacity_unit_1 = CapacityUnit(
    addr="root@fct-4a:~",
    hardware_type="BB",
    hardware_version="A.103",
    serial_number="F7173759109",
    product_code="472182A.103",
)

gnb_radio_unit_0 = RU(
    ru_hw_group="AHPCA",
    default_ssh_connection_details=SshServiceDetails(
        addr="", username="root", password=""
    ),
    radio_type="AHPCA",
    serial_number="BL2029B20K8",
    product_code="475075A.101",
    pdu_port=PduPort(pdu=_gnb_pdu_za03_41, port_no=1),
    lmi=SerialOverHost(
        host=TestPc(
            default_ssh_connection_details=SshServiceDetails(addr='PLKR-SC5G-PC07.p04.ska-lab.nsn-rdnet.net',
                                                             port='9093',
                                                             username=r'NOKLAB\pzkrk',
                                                             password='NokiaBts2003')),
        uart_mapping=[Local(port='COM3')]
    )
)


gnb_radio_unit_1 = RU(
    ru_hw_group="AHHB",
    default_ssh_connection_details=SshServiceDetails(
        addr="", username="root", password=""
    ),
    radio_type="AHHB",
    serial_number="L1182707441",
    product_code="474252A.101",
    pdu_port=PduPort(pdu=_gnb_pdu_za06_48, port_no=3),
    lmi=SerialOverHost(
        host=TestPc(
            default_ssh_connection_details=SshServiceDetails(addr='PLKR-SC5G-PC07.p04.ska-lab.nsn-rdnet.net',
                                                             port='9093',
                                                             username=r'NOKLAB\pzkrk',
                                                             password='NokiaBts2003')),
        uart_mapping=[Local(port='COM19')]
    )
)

gnb_radio_unit_2 = RU(
    ru_hw_group="AHHB",
    default_ssh_connection_details=SshServiceDetails(
        addr="", username="root", password=""
    ),
    radio_type="AHHB",
    serial_number="EA221154188",
    product_code="474252A.102",
    pdu_port=PduPort(pdu=_gnb_pdu_za06_48, port_no=4),
    lmi=SerialOverHost(
        host=TestPc(
            default_ssh_connection_details=SshServiceDetails(addr='PLKR-SC5G-PC07.p04.ska-lab.nsn-rdnet.net',
                                                             port='9093',
                                                             username=r'NOKLAB\pzkrk',
                                                             password='NokiaBts2003')),
        uart_mapping=[Local(port='COM10')]
    )
)

gnb_radio_unit_3 = RU(
    ru_hw_group="AHHB",
    default_ssh_connection_details=SshServiceDetails(
        addr="", username="root", password=""
    ),
    radio_type="AHHB",
    serial_number="L1182715983",
    product_code="474252A.101",
    pdu_port=PduPort(pdu=_gnb_pdu_za06_48, port_no=5),
    lmi=SerialOverHost(
        host=TestPc(
            default_ssh_connection_details=SshServiceDetails(addr='PLKR-SC5G-PC07.p04.ska-lab.nsn-rdnet.net',
                                                             port='9093',
                                                             username=r'NOKLAB\pzkrk',
                                                             password='NokiaBts2003')),
        uart_mapping=[Local(port='COM39')]
    )
)

gnb_radio_unit_4 = RU(
    ru_hw_group="AHPCA",
    default_ssh_connection_details=SshServiceDetails(
        addr="", username="root", password=""
    ),
    radio_type="AHPCA",
    serial_number="BL2029B20MC",
    product_code="475075A.101",
    pdu_port=PduPort(pdu=_gnb_pdu_za03_41, port_no=2),
    lmi=SerialOverHost(
        host=TestPc(
            default_ssh_connection_details=SshServiceDetails(addr='PLKR-SC5G-PC07.p04.ska-lab.nsn-rdnet.net',
                                                             port='9093',
                                                             username=r'NOKLAB\pzkrk',
                                                             password='NokiaBts2003')),
        uart_mapping=[Local(port='COM34')]
    )
)

gnb_radio_unit_5 = RU(
    ru_hw_group="AHPCA",
    default_ssh_connection_details=SshServiceDetails(
        addr="", username="root", password=""
    ),
    radio_type="AHPCA",
    serial_number="BL2029B20K7",
    product_code="475075A.101",
    pdu_port=PduPort(pdu=_gnb_pdu_za03_41, port_no=3),
    lmi=SerialOverHost(
        host=TestPc(
            default_ssh_connection_details=SshServiceDetails(addr='PLKR-SC5G-PC07.p04.ska-lab.nsn-rdnet.net',
                                                             port='9093',
                                                             username=r'NOKLAB\pzkrk',
                                                             password='NokiaBts2003')),
        uart_mapping=[Local(port='COM18')]
    )
)

gnb_radio_unit_6 = RU(
    ru_hw_group="AHFIB",
    default_ssh_connection_details=SshServiceDetails(
        addr="", username="root", password="umniedziala"
    ),
    radio_type="AHFIB",
    serial_number="BL2124V0EDJ",
    product_code="474216A.101",
    pdu_port=PduPort(pdu=_gnb_pdu_za06_32, port_no=1),
    lmi=SerialOverHost(
        host=TestPc(
            default_ssh_connection_details=SshServiceDetails(addr='PLKR-SC5G-PC07.p04.ska-lab.nsn-rdnet.net',
                                                             port='9093',
                                                             username=r'NOKLAB\pzkrk',
                                                             password='NokiaBts2003')),
        uart_mapping=[Local(port='COM33')]
    )
)
gnb_radio_unit_7 = RU(
    ru_hw_group="AHFIB",
    default_ssh_connection_details=SshServiceDetails(
        addr="", username="root", password=""
    ),
    radio_type="AHFIB",
    serial_number="BL2044V0QXR",
    product_code="474216A.101",
    pdu_port=PduPort(pdu=_gnb_pdu_za06_32, port_no=1),
    lmi=SerialOverHost(
        host=TestPc(
            default_ssh_connection_details=SshServiceDetails(addr='PLKR-SC5G-PC07.p04.ska-lab.nsn-rdnet.net',
                                                             port='9093',
                                                             username=r'NOKLAB\pzkrk',
                                                             password='NokiaBts2003')),
        uart_mapping=[Local(port='COM4')]
    )
)
gnb_radio_unit_8 = RU(
    ru_hw_group="AHFIB",
    default_ssh_connection_details=SshServiceDetails(
        addr="", username="root", password="umniedziala"
    ),
    radio_type="AHFIB",
    serial_number="K9184308111",
    product_code="474216A.101",
    pdu_port=PduPort(pdu=_gnb_pdu_za06_32, port_no=1),
    lmi=SerialOverHost(
        host=TestPc(
            default_ssh_connection_details=SshServiceDetails(addr='PLKR-SC5G-PC07.p04.ska-lab.nsn-rdnet.net',
                                                             port='9093',
                                                             username=r'NOKLAB\pzkrk',
                                                             password='NokiaBts2003')),
        uart_mapping=[Local(port='COM16')]
    )
)

gnb_capacity_unit_2 = CapacityUnit(
    addr="",
    hardware_type="ABIO",
    hardware_version="A.104",
    serial_number="L1224005029",
    product_code="475266A.104",
    rus=[
        gnb_radio_unit_0,
        gnb_radio_unit_1,
        gnb_radio_unit_2,
        gnb_radio_unit_3,
        gnb_radio_unit_4,
        gnb_radio_unit_5,
        gnb_radio_unit_6,
        gnb_radio_unit_7,
        gnb_radio_unit_8,
    ],
)

gnb_common_unit_0 = CommonUnit(
    lmp_connection=_default_gnb_ssh_lmp_connection,
    capacity_units=[gnb_capacity_unit_0, gnb_capacity_unit_1, gnb_capacity_unit_2],
    hardware_type="ASIB",
    hardware_version="A.102",
    serial_number="DH214541329",
    mac_addr="",
    pdu_port=PduPort(pdu=_gnb_pdu_za06_32, port_no=2),
)

gnb_common_unit_1 = CommonUnit(
    lmp_connection=_default_gnb_ssh_lmp_connection,
    capacity_units=[gnb_capacity_unit_0, gnb_capacity_unit_1, gnb_capacity_unit_2],
    hardware_type="Flexi",
    hardware_version="",
    serial_number="AS172860345",
    mac_addr="",
    pdu_port=PduPort(pdu=_gnb_pdu_za06_32, port_no=1),
)

_airscale_gnb = Airscale(
    common_units=[gnb_common_unit_0, gnb_common_unit_1], product_code="473098A"
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
    pdus=[_gnb_pdu_za06_48, _gnb_pdu_za03_41, _gnb_pdu_za06_32],
    test_pcs=[_test_pc_gnb_main],
)

__all__ = ["tl"]
