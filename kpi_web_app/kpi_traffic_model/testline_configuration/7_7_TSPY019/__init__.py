# Generated with TL configuration generator at 2024-09-17_08:43:56

# Repository  -> https://wrgitlab.int.net.nokia.com/ran_pz_krk/config_generator
# Jenkins job -> http://krk-pz-jenkins.krk-lab.nsn-rdnet.net:5990/view/Tools/job/Config_Generator/build?delay=0sec

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
from taf.config.testline.pdu import PduPort, FPFH, HPE
from taf.config.testline.attenuator import (RadioRack,
                                            AttenuationPort, )
import os
import yaml

# ------------------------PDU_CONFIGURATION------------------------

_bts_pdu = FPFH(
    port_numbers=[2],  # update port_no
    addr="fpfh-gi06-46-sc5g.sc5g-leg.krk-lab.nsn-rdnet.net",  # update address
    login="admin",
    password="admin",
)

_hpe_snmp_user = {
    "userName": "administrator",
    "authKey": "password",
    "privKey": "password",
    "authProtocol": "MD5",
    "privProtocol": "AES",  # HPE v2.0.0.K DES, HPE v2.0.0.Q/v2.0.0.T AES, ATEN should be AES
}

# _ru_pdu = HPE(
#     port_numbers=[19, 20],         # update port_no
#     addr="gi07.mgt.krk-lab.nsn-rdnet.net",    # update address
#     snmp_user=_hpe_snmp_user,
# )

_ru_pdu_1 = FPFH(
    port_numbers=[1, 3, 4, 5, 6],
    addr="fpfh-gi06-46-sc5g.sc5g-leg.krk-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

_ru_pdu_2 = FPFH(
    port_numbers=[1, 2],
    addr="fpfh-gi06-26-sc5g.sc5g-leg.krk-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

_ac_pdu = HPE(
    port_numbers=[
        14,     # APHG
        19,     # UEPC PLKR-TP-UE46
        20      # ATT RadioRack
    ],
    addr="gi07.mgt.krk-lab.nsn-rdnet.net",  # update address
    snmp_user=_hpe_snmp_user,
)

_attenuator = RadioRack(
    ip_addr="10.253.176.134",
    port="50000",
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    version=None,
)

# ------------------------GNB0_CONFIGURATION------------------------

_test_pc_gnb_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-TSPY019.sc5g.krk-lab.nsn-rdnet.net",
        username="ute",
        password="uteUTE!",
    )
)

_gnb_0_instance_id = 75019
_gnb_0_global_bts_id = 75019

_gnb_0_primary_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_gnb_0.default_ssh_connection_details,
)

_gnb_0_oam_ip = NetworkAddress(
    v4="10.83.182.19/23",
    routing_v4=RoutingInformation(gateway="10.83.253.254", destIpAddr="0.0.0.0"),
    vlan_id=503,
)

_gnb_0_f1m_ip = NetworkAddress(
    v4="10.83.182.19/23",
    routing_v4=RoutingInformation(gateway="10.83.253.254", destIpAddr="0.0.0.0"),
    vlan_id=503,
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
    v4="10.83.182.19/23",
    routing_v4=RoutingInformation(gateway="10.83.253.254", destIpAddr="0.0.0.0"),
    vlan_id=503,
)

_gnb_0_x2u_ip = NetworkAddress(
    v4="10.83.182.19/23",
    routing_v4=RoutingInformation(gateway="10.83.253.254", destIpAddr="0.0.0.0"),
    vlan_id=503,
)

_gnb_0_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_0_s1u_ip = NetworkAddress(
    v4="10.83.182.19/23",
    routing_v4=RoutingInformation(gateway="10.83.253.254", destIpAddr="0.0.0.0"),
    vlan_id=503,
)

_gnb_0_xnc_ip = NetworkAddress(
    v4="10.83.182.19/23",
    routing_v4=RoutingInformation(gateway="10.83.253.254", destIpAddr="0.0.0.0"),
    vlan_id=503,
)

_gnb_0_xnu_ip = NetworkAddress(
    v4="10.83.182.19/23",
    routing_v4=RoutingInformation(gateway="10.83.253.254", destIpAddr="0.0.0.0"),
    vlan_id=503,
)

_gnb_0_ngc_ip = NetworkAddress(
    v4="10.83.182.19/23",
    routing_v4=RoutingInformation(gateway="10.83.253.254", destIpAddr="0.0.0.0"),
    vlan_id=503,
)

_gnb_0_ngu_ip = NetworkAddress(
    v4="10.83.182.19/23",
    routing_v4=RoutingInformation(gateway="10.83.253.254", destIpAddr="0.0.0.0"),
    vlan_id=503,
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

_gnb_0_radio_unit_4 = RU(
    ru_hw_group="AHEGC",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHEGC",
    serial_number="EA232050647",
    product_code="474914A.101",
    pdu_port=PduPort(pdu=_ru_pdu_1, port_no=5),  # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_0_radio_unit_2 = RU(
    ru_hw_group="AHCA",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHCA",
    serial_number="AS210709326",
    product_code="473966A.101",
    pdu_port=PduPort(pdu=_ru_pdu_1, port_no=4),  # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_0_radio_unit_8 = RU(
    ru_hw_group="FXED",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="FXED",
    serial_number="F7165121675",
    product_code="472924A.202",
    pdu_port=PduPort(pdu=_ru_pdu_2, port_no=1),  # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_0_radio_unit_1 = RU(
    ru_hw_group="AHCA",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHCA",
    serial_number="AS210708434",
    product_code="473966A.101",
    pdu_port=PduPort(pdu=_ru_pdu_1, port_no=3),  # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_0_radio_unit_9 = RU(
     ru_hw_group="FXED",
     default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
     ),
     radio_type="FXED",
     serial_number="F7174516433",
     product_code="472924A.203",
     pdu_port=PduPort(pdu=_ru_pdu_2, port_no=2),    # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_0_radio_unit_6 = RU(
    ru_hw_group="AHCA",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHCA",
    serial_number="AS212504939",
    product_code="473966B.101",
    pdu_port=PduPort(pdu=_ru_pdu_1, port_no=1),  # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_0_radio_unit_5 = RU(
    ru_hw_group="AHCA",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHCA",
    serial_number="AS210708398",
    product_code="473966A.101",
    pdu_port=PduPort(pdu=_ru_pdu_1, port_no=6),  # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_0_radio_unit_0 = RU(
    ru_hw_group="APHG",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="APHG",
    serial_number="NH225300348",
    product_code="475295A.101",
    pdu_port=PduPort(pdu=_ac_pdu, port_no=14),    # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_0_common_unit_0 = CommonUnit(
    lmp_connection=_gnb_0_primary_ssh_lmp_connection,
    capacity_units=[],
    hardware_type="ASOG",
    hardware_version="A.101",
    serial_number="L1240913036",
    mac_addr="",
    # trs_connections=[],
    slot_id=SlotId.C1,
    rus=[_gnb_0_radio_unit_0, _gnb_0_radio_unit_1, _gnb_0_radio_unit_2, _gnb_0_radio_unit_8,
         _gnb_0_radio_unit_4, _gnb_0_radio_unit_5, _gnb_0_radio_unit_6, _gnb_0_radio_unit_9, ],
    pdu_port=PduPort(pdu=_bts_pdu, port_no=2),  # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_0_airscale = Airscale(
    common_units=[_gnb_0_common_unit_0],
    product_code="N/A",
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


# ------------------------TL_CONFIGURATION------------------------
def _set_abstract_lib_config_env(ue_config_file):
    tl_config_dir = os.path.dirname(os.path.abspath(__file__))
    ue_config_abs_path = os.path.join(tl_config_dir, ue_config_file)
    with open(ue_config_abs_path) as ta_ue_config:
        ue_config = yaml.safe_load(ta_ue_config)
    os.environ["ABSTRACT_LIB_CONFIG"] = ue_config_abs_path
    return ue_config


_ue_config = _set_abstract_lib_config_env("ue_config.yaml")

tl = TestLine(
    test_pc=_test_pc_gnb_0,
    gnbs=[_gnb_0],
    test_pcs=[_test_pc_gnb_0],
    tl_cloud_topology="CLOUD_7_7_TSPY019",
    attenuator=[_attenuator],
    pdus=[_bts_pdu, _ru_pdu_1, _ru_pdu_2],
    ues=[_ue_config],
)

__all__ = ["tl"]
