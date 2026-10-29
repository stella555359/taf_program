# Generated with TL configuration generator at 2025-09-12_08:36:26

# Repository  -> https://wrgitlab.int.net.nokia.com/ran_pz_krk/config_generator
# Jenkins job -> http://krk-pz-jenkins.krk-lab.nsn-rdnet.net:5990/view/Tools/job/Config_Generator/build?delay=0sec

__maintainer__ = "Maksymilian Wolek"
__team__ = "MN RAN RD VRF KRK 7"
__email__ = "maksymilian.wolek@nokia.com"

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
import os
import yaml

# ------------------------PDU_CONFIGURATION------------------------

_bts_pdu = FPFH(
    port_numbers=[5],
    addr="fpfh-pa05-46-d01.d01-leg.krk-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

_hpe_snmp_user = {
    "userName": "administrator",
    "authKey": "password",
    "privKey": "password",
    "authProtocol": "MD5",
    "privProtocol": "AES",
}

#_ru_pdu = HPE(
#    port_numbers=[999],         # update port_no
#    addr="FQDN HPE address",    # update address
#    snmp_user=_hpe_snmp_user,
#)

_ru_pdu_1 = FPFH(
    port_numbers=[4],
    addr="fpfh-pa03-46-d01.d01-leg.krk-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

_ru_pdu_2 = FPFH(
    port_numbers=[1, 2],
    addr="fpfh-pa04-46-d01.d01-leg.krk-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

_ru_pdu_3 = FPFH(
    port_numbers=[1, 2, 3],
    addr="fpfh-pa05-23-d01.d01-leg.krk-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

# ------------------------GNB0_CONFIGURATION------------------------

_test_pc_gnb_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-T01PY074.d01.krk-lab.nsn-rdnet.net",
        username="ute",
        password="UTE.debian12",
    )
)

_gnb_0_instance_id = 85074
_gnb_0_global_bts_id = 85074

_gnb_0_primary_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_gnb_0.default_ssh_connection_details,
)

_gnb_0_oam_ip = NetworkAddress(
    v4="10.89.3.74/24",
    routing_v4=RoutingInformation(gateway="10.89.4.254", destIpAddr="10.27.28.136"),
    vlan_id=504,
) 

_gnb_0_f1m_ip = NetworkAddress(
    v4="10.89.3.74/24",
    routing_v4=RoutingInformation(gateway="10.89.4.254", destIpAddr="10.27.28.136"),
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
    v4="10.89.3.74/24",
    routing_v4=RoutingInformation(gateway="10.89.3.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
) 

_gnb_0_x2u_ip = NetworkAddress(
    v4="10.89.3.74/24",
    routing_v4=RoutingInformation(gateway="10.89.3.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
) 

_gnb_0_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
) 

_gnb_0_s1u_ip = NetworkAddress(
    v4="10.89.3.74/24",
    routing_v4=RoutingInformation(gateway="10.89.3.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
) 

_gnb_0_xnc_ip = NetworkAddress(
    v4="10.89.3.74/24",
    routing_v4=RoutingInformation(gateway="10.89.4.254", destIpAddr="10.27.28.136"),
    vlan_id=504,
) 

_gnb_0_xnu_ip = NetworkAddress(
    v4="172.16.4.74/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
) 

_gnb_0_ngc_ip = NetworkAddress(
    v4="172.16.4.74/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
) 

_gnb_0_ngu_ip = NetworkAddress(
    v4="172.16.4.74/0",
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
    ru_hw_group="AHEGC",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHEGC",
    serial_number="EA192576279",
    product_code="474914A.101",
    pdu_port=PduPort(pdu=_ru_pdu_3, port_no=3),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_1 = RU(
    ru_hw_group="AVQQ",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og=",
    ),
    radio_type="AVQQ",
    serial_number="1M253204145",
    product_code="476400A.101",
    pdu_port=PduPort(pdu=_ru_pdu_2, port_no=2),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_2 = RU(
    ru_hw_group="AHEGC",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHEGC",
    serial_number="EA214551956",
    product_code="474914A.101",
    pdu_port=PduPort(pdu=_ru_pdu_3, port_no=2),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_3 = RU(
    ru_hw_group="AVQQ",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og=",
    ),
    radio_type="AVQQ",
    serial_number="1M245200859",
    product_code="476400A.101",
    pdu_port=PduPort(pdu=_ru_pdu_1, port_no=4),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_4 = RU(
    ru_hw_group="AHEGC",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHEGC",
    serial_number="EA200262099",
    product_code="474914A.101",
    pdu_port=PduPort(pdu=_ru_pdu_3, port_no=1),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_5 = RU(
    ru_hw_group="AVQQ",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og=",
    ),
    radio_type="AVQQ",
    serial_number="1M253204144",
    product_code="476400A.101",
    pdu_port=PduPort(pdu=_ru_pdu_2, port_no=1),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_capacity_unit_0 = CapacityUnit(
    addr="192.168.253.38",
    hardware_type="ABIO",
    hardware_version="A.104",
    serial_number="L1220902279",
    product_code="475266A.104",
    slot_id=SlotId.B4,
    rus=[_gnb_0_radio_unit_0, _gnb_0_radio_unit_2, _gnb_0_radio_unit_4],
)

_gnb_0_capacity_unit_1 = CapacityUnit(
    addr="192.168.253.42",
    hardware_type="ABIP",
    hardware_version="A.102",
    serial_number="L1250605466",
    product_code="475792A.102",
    slot_id=SlotId.B5,
    rus=[_gnb_0_radio_unit_1, _gnb_0_radio_unit_3, _gnb_0_radio_unit_5],
)

_gnb_0_common_unit_0 = CommonUnit(
    lmp_connection=_gnb_0_primary_ssh_lmp_connection,
    capacity_units=[_gnb_0_capacity_unit_0, _gnb_0_capacity_unit_1],
    hardware_type="ASIM",
    hardware_version="A.104",
    serial_number="L1243004528",
    mac_addr="d0:48:4f:04:5d:b4",
    # trs_connections=[TRSInterfaces.EIF1],
    slot_id=SlotId.C2,
    pdu_port=PduPort(pdu=_bts_pdu, port_no=5),  # uncomment & update port_no for gNB - for eNB you can delete
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


def _set_abstract_lib_config_env(ue_config_file):  # <----------
    ue_config_abs_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), ue_config_file
    )
    with open(ue_config_abs_path) as ta_ue_config:
        ue_config = yaml.safe_load(ta_ue_config)
    os.environ["ABSTRACT_LIB_CONFIG"] = ue_config_abs_path
    return ue_config

ue_config = _set_abstract_lib_config_env("ue_config.yaml")


# ------------------------TL_CONFIGURATION------------------------


tl = TestLine(
    test_pc=_test_pc_gnb_0,
    gnbs=[_gnb_0],
    test_pcs=[_test_pc_gnb_0],
    tl_cloud_topology="CLOUD_7_7_T01PY074"
)

tl.ue_config = ue_config
__all__ = ["tl"]
