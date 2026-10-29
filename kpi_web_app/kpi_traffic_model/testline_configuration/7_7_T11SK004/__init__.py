# Generated with TL configuration generator at 2025-06-06_09:48:26

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
import os
import yaml

# ------------------------PDU_CONFIGURATION------------------------

_bts_pdu1 = FPFH(
    port_numbers=[1,2,3,4,5,6],         # update port_no
    addr="10.255.41.58",   # update address
    login="admin",
    password="admin",
)

_bts_pdu2 = FPFH(
    port_numbers=[1,2,3,4],         # update port_no
    addr="10.255.41.59",   # update address
    login="admin",
    password="admin",	
)

_hpe_snmp_user = {
    "userName": "administrator",
    "authKey": "password",
    "privKey": "password",
    "authProtocol": "MD5",
    "privProtocol": "AES",      # HPE v2.0.0.K DES, HPE v2.0.0.Q/v2.0.0.T AES, ATEN should be AES
}

_ru_pdu = HPE(
    port_numbers=[999],         # update port_no
    addr="FQDN HPE address",    # update address
    snmp_user=_hpe_snmp_user,
)

# ------------------------GNB0_CONFIGURATION------------------------

_test_pc_gnb_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-T11SK004.p11.ska-lab.nsn-rdnet.net",
        username="ute",
        password="uteUTE!",
    )
)

_gnb_0_instance_id = 81004
_gnb_0_global_bts_id = 81004

_gnb_0_primary_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_gnb_0.default_ssh_connection_details,
)

_gnb_0_oam_ip = NetworkAddress(
    v4="10.82.28.4/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
) 

_gnb_0_f1m_ip = NetworkAddress(
    v4="10.82.28.4/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
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
    v4="10.82.30.4/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=507,
) 

_gnb_0_x2u_ip = NetworkAddress(
    v4="10.255.48.4/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=505,
) 

_gnb_0_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
) 

_gnb_0_s1u_ip = NetworkAddress(
    v4="10.255.50.4/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=506,
) 

_gnb_0_xnc_ip = NetworkAddress(
    v4="10.82.30.4/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=507,
) 

_gnb_0_xnu_ip = NetworkAddress(
    v4="10.255.48.4/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=505,
) 

_gnb_0_ngc_ip = NetworkAddress(
    v4="10.82.30.4/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=507,
) 

_gnb_0_ngu_ip = NetworkAddress(
    v4="10.255.50.4/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=506,
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
    ru_hw_group="AHPE",
    default_ssh_connection_details=SshServiceDetails(
       addr="",
       username="root",
       password="umniedziala",
    ),
    radio_type="AHPE",
    serial_number="1M211904056",
    product_code="475208A.101",
    pdu_port=PduPort(pdu=_bts_pdu2, port_no=1),    # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_1 = RU(
    ru_hw_group="AHEGC",
    default_ssh_connection_details=SshServiceDetails(
       addr="",
       username="root",
       password="umniedziala",
    ),
    radio_type="AHEGC",
    serial_number="EA205053902",
    product_code="474914A.101",
    pdu_port=PduPort(pdu=_bts_pdu2, port_no=2),    # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_2 = RU(
    ru_hw_group="AWHQN",
    default_ssh_connection_details=SshServiceDetails(
       addr="",
       username="root",
       password="umniedziala",
    ),
    radio_type="AWHQN",
    serial_number="AH250705101",
    product_code="475701A.103",
    pdu_port=PduPort(pdu=_bts_pdu1, port_no=4),    # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_3 = RU(
    ru_hw_group="AWHQN",
    default_ssh_connection_details=SshServiceDetails(
       addr="",
       username="root",
       password="umniedziala",
    ),
    radio_type="AWHQN",
    serial_number="EB2244R1890",
    product_code="475701A.102",
    pdu_port=PduPort(pdu=_bts_pdu1, port_no=5),    # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_4 = RU(
    ru_hw_group="AWHQN",
    default_ssh_connection_details=SshServiceDetails(
       addr="",
       username="root",
       password="umniedziala",
    ),
    radio_type="AWHQN",
    serial_number="AH250705106",
    product_code="475701A.103",
    pdu_port=PduPort(pdu=_bts_pdu1, port_no=6),    # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_5 = RU(
    ru_hw_group="AWHQN",
    default_ssh_connection_details=SshServiceDetails(
       addr="",
       username="root",
       password="umniedziala",
    ),
    radio_type="AWHQN",
    serial_number="AH250705056",
    product_code="475701A.103",
    pdu_port=PduPort(pdu=_bts_pdu1, port_no=3),    # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_6 = RU(
    ru_hw_group="AWHQN",
    default_ssh_connection_details=SshServiceDetails(
       addr="",
       username="root",
       password="umniedziala",
    ),
    radio_type="AWHQN",
    serial_number="AH250705064",
    product_code="475701A.103",
    pdu_port=PduPort(pdu=_bts_pdu1, port_no=2),    # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_7 = RU(
    ru_hw_group="AHEGC",
    default_ssh_connection_details=SshServiceDetails(
       addr="",
       username="root",
       password="umniedziala",
    ),
    radio_type="AHEGC",
    serial_number="EA215050200",
    product_code="474914A.101",
    pdu_port=PduPort(pdu=_bts_pdu2, port_no=3),    # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_8 = RU(
    ru_hw_group="AQQN",
    default_ssh_connection_details=SshServiceDetails(
       addr="",
       username="root",
       password="umniedziala",
    ),
    radio_type="AQQN",
    serial_number="L1223403771",
    product_code="475937A.102",
    pdu_port=PduPort(pdu=_bts_pdu2, port_no=4),    # fake part, uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_9 = RU(
    ru_hw_group="None",
    default_ssh_connection_details=SshServiceDetails(
       addr="",
       username="root",
       password="umniedziala",
    ),
    radio_type="None",
    serial_number="None",
    product_code="475946A.103",
   # pdu_port=PduPort(pdu=_ru_pdu, port_no=999),    # uncomment & update port_no for gNB - for eNB you can delete
   # lmi=SerialOverTcp(
   #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
   # )
)

_gnb_0_capacity_unit_0 = CapacityUnit(
    addr="192.168.253.26",
    hardware_type="ABIP",
    hardware_version="A.102",
    serial_number="L1233201715",
    product_code="475792A.102",
    slot_id=SlotId.B2,
    rus=[_gnb_0_radio_unit_0, _gnb_0_radio_unit_1, _gnb_0_radio_unit_7],
    )

_gnb_0_capacity_unit_1 = CapacityUnit(
    addr="192.168.253.22",
    hardware_type="ABIP",
    hardware_version="A.102",
    serial_number="L1232804647",
    product_code="475792A.102",
    slot_id=SlotId.B1,
    rus=[],
    )

_gnb_0_capacity_unit_2 = CapacityUnit(
    addr="192.168.253.30",
    hardware_type="ABIP",
    hardware_version="A.102",
    serial_number="L1232807138",
    product_code="475792A.102",
    slot_id=SlotId.B3,
    rus=[_gnb_0_radio_unit_2, _gnb_0_radio_unit_3, _gnb_0_radio_unit_4, _gnb_0_radio_unit_5, _gnb_0_radio_unit_6, _gnb_0_radio_unit_8],
    )

_gnb_0_common_unit_0 = CommonUnit(
    lmp_connection=_gnb_0_primary_ssh_lmp_connection,
    capacity_units=[_gnb_0_capacity_unit_0, _gnb_0_capacity_unit_1, _gnb_0_capacity_unit_2],
    hardware_type="ASIL",
    hardware_version="A.101",
    serial_number="L1213704501",
    mac_addr="00:77:e4:97:64:bf",
    # trs_connections=[TRSInterfaces.EIF1],
    slot_id=SlotId.C1,
    pdu_port=PduPort(pdu=_bts_pdu1, port_no=1),    # uncomment & update port_no for gNB - for eNB you can delete
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

# ------------------------TL_CONFIGURATION------------------------


tl = TestLine(
    test_pc=_test_pc_gnb_0,
    gnbs=[_gnb_0],
    test_pcs=[_test_pc_gnb_0],
    tl_cloud_topology="CLOUD_7_7_T11SK004"
)

__all__ = ["tl"]