# Generated with TL configuration generator at 2024-02-26_14:04:56

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
from taf.config.testline.attenuator import RadioRack
from taf.config.testline.pdu import PduPort, FPFH, HPE
import os
import yaml

# ------------------------PDU_CONFIGURATION------------------------


_bts_pdu = FPFH(
    port_numbers=[1],  # update port_no
    addr="fpfh-gh09-46-sc5g.sc5g-leg.krk-lab.nsn-rdnet.net",  # update address
    login="admin",
    password="admin",
)

_hpe_snmp_user = {
    "userName": "administrator",
    "authKey": "password",
    "privKey": "password",
    "authProtocol": "MD5",
    "privProtocol": "AES",  # HPE v2.0.0.K DES, HPE v2.0.0.Q AES, ATEN should be AES
}

_ru_pdu = HPE(
    port_numbers=[3, 4, 5, 9, 10, 11, 12, 13, 16],  # update port_no
    addr="gh09.mgt.krk-lab.nsn-rdnet.net",  # update address
    snmp_user=_hpe_snmp_user,
)

# ------------------------GNB_CONFIGURATION------------------------


_gnb_oam_ip = NetworkAddress(
    v4="10.83.182.103/23",
    routing_v4=RoutingInformation(gateway="10.83.253.254", destIpAddr="10.253.164.188"),
    vlan_id=503,
)

_gnb_f1m_ip = NetworkAddress(
    v4="10.83.182.103/23",
    routing_v4=RoutingInformation(gateway="10.83.253.254", destIpAddr="10.253.164.188"),
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
    v4="10.83.252.103/23",
    routing_v4=RoutingInformation(gateway="10.83.253.254", destIpAddr="10.253.164.188"),
    vlan_id=541,
)

_gnb_x2u_ip = NetworkAddress(
    v4="10.253.212.103/23",
    routing_v4=RoutingInformation(gateway="10.83.253.254", destIpAddr="10.253.164.188"),
    vlan_id=542,
)

_gnb_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_s1u_ip = NetworkAddress(
    v4="10.253.212.103/23",
    routing_v4=RoutingInformation(gateway="10.83.253.254", destIpAddr="10.253.164.188"),
    vlan_id=542,
)

_gnb_xnc_ip = NetworkAddress(
    v4="10.83.182.103/23",
    routing_v4=RoutingInformation(gateway="10.83.253.254", destIpAddr="10.253.164.188"),
    vlan_id=503,
)

_gnb_xnu_ip = NetworkAddress(
    v4="10.83.182.103/23",
    routing_v4=RoutingInformation(gateway="10.83.253.254", destIpAddr="10.253.164.188"),
    vlan_id=503,
)

_gnb_ngc_ip = NetworkAddress(
    v4="10.83.182.103/23",
    routing_v4=RoutingInformation(gateway="10.83.253.254", destIpAddr="10.253.164.188"),
    vlan_id=503,
)

_gnb_ngu_ip = NetworkAddress(
    v4="10.83.182.103/23",
    routing_v4=RoutingInformation(gateway="10.83.253.254", destIpAddr="10.253.164.188"),
    vlan_id=503,
)

_test_pc_gnb = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT103.sc5g.krk-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_gnb_instance_id = 75103
_gnb_global_bts_id = 75103

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
    ru_hw_group="APHG",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="APHG",
    serial_number="NH211600111",
    product_code="475295A.101",
    pdu_port=PduPort(
        pdu=_ru_pdu, port_no=12
    ),  # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_radio_unit_1 = RU(
     ru_hw_group="APHG",
     default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="APHG",
    serial_number="NH210200293",
    product_code="475295A.101S",
    pdu_port=PduPort(
        pdu=_ru_pdu, port_no=4
    ),  # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_radio_unit_2 = RU(
    ru_hw_group="APHG",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="APHG",
    serial_number="NH211300652",
    product_code="475295A.101",
    pdu_port=PduPort(
        pdu=_ru_pdu, port_no=16
    ),  # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_radio_unit_3 = RU(
    ru_hw_group="APHG",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="APHG",
    serial_number="NH211600105",
    product_code="475295A.101",
    pdu_port=PduPort(
        pdu=_ru_pdu, port_no=13
    ),  # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_radio_unit_4 = RU(
    ru_hw_group="APHG",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="APHG",
    serial_number="NH213100499",
    product_code="475295A.101",
    pdu_port=PduPort(
        pdu=_ru_pdu, port_no=11
    ),  # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_radio_unit_5 = RU(
    ru_hw_group="APHG",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="APHG",
    serial_number="NH213100441",
    product_code="475295A.101",
    pdu_port=PduPort(
        pdu=_ru_pdu, port_no=9
    ),  # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_radio_unit_6 = RU(
    ru_hw_group="APHG",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="APHG",
    serial_number="NH211300650",
    product_code="475295A.101",
    pdu_port=PduPort(
        pdu=_ru_pdu, port_no=5
    ),  # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_radio_unit_7 = RU(
    ru_hw_group="APHG",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="APHG",
    serial_number="NH210300316",
    product_code="475295A.101S",
    pdu_port=PduPort(
        pdu=_ru_pdu, port_no=10
    ),  # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_radio_unit_8 = RU(
    ru_hw_group="APHG",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="APHG",
    serial_number="NH211300646",
    product_code="475295A.101",
    pdu_port=PduPort(
        pdu=_ru_pdu, port_no=3
    ),  # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_capacity_unit_0 = CapacityUnit(
    addr="",
    hardware_type="ABIO",
    hardware_version="A.102",
    serial_number="L1205102748",
    product_code="475266A.102",
    slot_id=SlotId.B1,
    rus=[
        _gnb_radio_unit_0,
        _gnb_radio_unit_1,
        _gnb_radio_unit_2,
        _gnb_radio_unit_3,
        _gnb_radio_unit_4,
        _gnb_radio_unit_5,
        _gnb_radio_unit_6,
        _gnb_radio_unit_7,
        _gnb_radio_unit_8
        ],
    )

_gnb_common_unit_0 = CommonUnit(
    lmp_connection=_default_gnb_ssh_lmp_connection,
    capacity_units=[_gnb_capacity_unit_0],
    hardware_type="ASIB",
    hardware_version="A.102",
    serial_number="L1213008244",
    mac_addr="",
    # trs_connections=[],
    slot_id=SlotId.C1,
    pdu_port=PduPort(pdu=_bts_pdu, port_no=1),    # uncomment & update port_no for gNB - for eNB you can delete
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

_attenuator = RadioRack(
    ip_addr="10.253.166.50", port=50000, attenuation_port_numbers=range(1, 17)
)

_attenuator2 = RadioRack(
    ip_addr="10.253.166.51", port=50000, attenuation_port_numbers=range(1, 17)
)

# ------------------------TL_CONFIGURATION------------------------

def _set_abstract_lib_config_env(ue_config_file):
    tl_config_dir = os.path.dirname(os.path.abspath(__file__))
    ue_config_abs_path = os.path.join(tl_config_dir, ue_config_file)
    with open(ue_config_abs_path) as ta_ue_config:
        ue_config = yaml.safe_load(ta_ue_config)
    os.environ["ABSTRACT_LIB_CONFIG"] = ue_config_abs_path
    return ue_config


_ue_config = _set_abstract_lib_config_env("ue_config.yaml")

def _set_abstract_lib_config_env(ue_config_file):
    tl_config_dir = os.path.dirname(os.path.abspath(__file__))
    ue_config_abs_path = os.path.join(tl_config_dir, ue_config_file)
    with open(ue_config_abs_path) as ta_ue_config:
        ue_config = yaml.safe_load(ta_ue_config)
    os.environ["ABSTRACT_LIB_CONFIG"] = ue_config_abs_path
    return ue_config


_ue_config = _set_abstract_lib_config_env("ue_config.yaml")

tl = TestLine(
    test_pc=_test_pc_gnb,
    gnbs=[_gnb],
    test_pcs=[_test_pc_gnb],
    attenuators=[_attenuator, _attenuator2],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_ASIBL_ABIOB1_9xAPHG_16xAWHGEQH"
)

__all__ = ["tl"]
