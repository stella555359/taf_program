__maintainer__ = "Michal Machowski"
__team__ = "MN_RAN_RD_VRF_KRK_3"
__email__ = "michal.machowski@nokia.com"

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

_bts_pdu = FPFH(
    port_numbers=[1],
    addr="fpfh-za18-46-p09.p09-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

_hpe_snmp_user = {
    "userName": "administrator",
    "authKey": "password",
    "privKey": "password",
    "authProtocol": "MD5",
    "privProtocol": "AES",      # HPE v2.0.0.K DES, HPE v2.0.0.Q AES, ATEN should be AES
}

_ru_pdu = HPE(
    port_numbers=[2, 3, 4, 5, 6, 7, 9, 10],
    addr="za18.mgt.ska-lab.nsn-rdnet.net",
    snmp_user=_hpe_snmp_user,
)

# ------------------------GNB0_CONFIGURATION------------------------

_gnb_oam_ip = NetworkAddress(
    v4="10.84.140.10/23",
    routing_v4=RoutingInformation(gateway="10.84.141.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
)

_gnb_f1m_ip = NetworkAddress(
    v4="10.84.140.10/23",
    routing_v4=RoutingInformation(gateway="10.84.141.254", destIpAddr="0.0.0.0"),
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
        addr="7-7-UTE5GCLOUDT9SK010.p09.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_gnb_instance_id = 78310
_gnb_global_bts_id = 78310

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
     ru_hw_group="APHA",
     default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="toor4nsn",
        password="oZPS0POrRieRtu",
     ),
     radio_type="APHA",
     serial_number="NH190500712",
     product_code="474657A.101",
     pdu_port=PduPort(pdu=_ru_pdu, port_no=9),
)

_gnb_radio_unit_1 = RU(
     ru_hw_group="APHA",
     default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="toor4nsn",
        password="oZPS0POrRieRtu",
     ),
     radio_type="APHA",
     serial_number="NH190500019",
     product_code="474657A.101",
     pdu_port=PduPort(pdu=_ru_pdu, port_no=10),
)

_gnb_radio_unit_2 = RU(
     ru_hw_group="APHA",
     default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="toor4nsn",
        password="oZPS0POrRieRtu",
     ),
     radio_type="APHA",
     serial_number="NH190500392",
     product_code="474657A.101",
     pdu_port=PduPort(pdu=_ru_pdu, port_no=3),
)

_gnb_radio_unit_3 = RU(
     ru_hw_group="APHA",
     default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="toor4nsn",
        password="oZPS0POrRieRtu",
     ),
     radio_type="APHA",
     serial_number="NH190500501",
     product_code="474657A.101",
     pdu_port=PduPort(pdu=_ru_pdu, port_no=2),
)

_gnb_radio_unit_4 = RU(
     ru_hw_group="APHG",
     default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="toor4nsn",
        password="oZPS0POrRieRtu",
     ),
     radio_type="APHG",
     serial_number="NH213100586",
     product_code="475295A.101",
     pdu_port=PduPort(pdu=_ru_pdu, port_no=5),
)

_gnb_radio_unit_5 = RU(
     ru_hw_group="APHA",
     default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="toor4nsn",
        password="oZPS0POrRieRtu",
     ),
     radio_type="APHA",
     serial_number="NH190500706",
     product_code="474657A.101",
     pdu_port=PduPort(pdu=_ru_pdu, port_no=6),
)

_gnb_radio_unit_6 = RU(
     ru_hw_group="APHA",
     default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="toor4nsn",
        password="oZPS0POrRieRtu",
     ),
     radio_type="APHA",
     serial_number="NH190500424",
     product_code="474657A.101",
     pdu_port=PduPort(pdu=_ru_pdu, port_no=4),
)

_gnb_radio_unit_7 = RU(
     ru_hw_group="APHA",
     default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="toor4nsn",
        password="oZPS0POrRieRtu",
     ),
     radio_type="APHA",
     serial_number="NH190500489",
     product_code="474657A.101",
     pdu_port=PduPort(pdu=_ru_pdu, port_no=7),
)

_gnb_capacity_unit_0 = CapacityUnit(
    addr="",
    hardware_type="ABIA",
    hardware_version="A.103",
    serial_number="EA184580653",
    product_code="473096A.103",
    slot_id=SlotId.B1,
    rus=[_gnb_radio_unit_2, _gnb_radio_unit_3, _gnb_radio_unit_4, _gnb_radio_unit_6],
    )

_gnb_capacity_unit_1 = CapacityUnit(
    addr="",
    hardware_type="ABIA",
    hardware_version="A.103",
    serial_number="DH192956727",
    product_code="473096A.103",
    slot_id=SlotId.B2,
    rus=[_gnb_radio_unit_0, _gnb_radio_unit_1, _gnb_radio_unit_5, _gnb_radio_unit_7],
    )

_gnb_common_unit_0 = CommonUnit(
    lmp_connection=_default_gnb_ssh_lmp_connection,
    capacity_units=[_gnb_capacity_unit_0, _gnb_capacity_unit_1],
    hardware_type="ASIA",
    hardware_version="A.204",
    serial_number="DH210566363",
    mac_addr="",
    # trs_connections=[],
    slot_id=SlotId.C1,
    pdu_port=PduPort(pdu=_bts_pdu, port_no=1),
)

_gnb_airscale = Airscale(
    common_units=[_gnb_common_unit_0],
    product_code="473098A",
    )

_du_gnb = DU(
    airscale=_gnb_airscale,
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


tl = TestLine(
    test_pc=_test_pc_gnb_main,
    gnbs=[_gnb_main],
    test_pcs=[_test_pc_gnb_main],
    tl_cloud_topology="CLOUD_4G_CLASSICAL_ASIR_ASIAL_2xABIA_7xAPHA_APHG_2xAHENA_AHFID_AHFIH_40xAHGEB"
)

__all__ = ["tl"]
