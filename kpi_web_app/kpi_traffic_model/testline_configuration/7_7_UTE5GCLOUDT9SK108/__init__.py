# Generated with TL configuration generator at 2025-10-29_13:30:16

# Repository  -> https://wrgitlab.int.net.nokia.com/ran_pz_krk/config_generator
# Jenkins job -> http://krk-pz-jenkins.krk-lab.nsn-rdnet.net:5990/view/Tools/job/Config_Generator/build?delay=0sec

__maintainer__ = "Dominik Wieczorek"
__team__ = "MN RAN RD VRF KRK 7"
__email__ = "dominik.wieczorek@nokia.com"

from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc, Connection
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
)
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline.gnb.networkaddress import NetworkAddress, RoutingInformation
from taf.config.testline.radio import RU, RUExtension
from taf.config.testline import CUS
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
    port_numbers=[1,3,4,5,6],         # update port_no
    addr="fpfh-hb08-46-p09.p09-leg.ska-lab.nsn-rdnet.net",   # update address
    login="admin",
    password="admin",
)

_ru_pdu0 = FPFH(
    port_numbers=[3,4,5,6],         # update port_no
    addr="fpfh-hb07-21-p09.p09-leg.ska-lab.nsn-rdnet.net",   # update address
    login="admin",
    password="admin",
)

_ru_pdu1 = FPFH(
    port_numbers=[1,2,3],         # update port_no
    addr="fpfh-hb07-21-p09.p09-leg.ska-lab.nsn-rdnet.net",   # update address
    login="admin",
    password="admin",
)

_ru_pdu2 = FPFH(
    port_numbers=[4,5,6],         # update port_no
    addr="fpfh-hb08-34-p09.p09-leg.ska-lab.nsn-rdnet.net",   # update address
    login="admin",
    password="admin",
)

_ru_pdu3 = FPFH(
    port_numbers=[4,5,6],         # update port_no
    addr="fpfh-hb09-21-p09.p09-leg.ska-lab.nsn-rdnet.net",   # update address
    login="admin",
    password="admin",
)

_ru_pdu4 = FPFH(
    port_numbers=[1,2,3],         # update port_no
    addr="fpfh-hb09-46-p09.p09-leg.ska-lab.nsn-rdnet.net",   # update address
    login="admin",
    password="admin",
)

_ru_pdu5 = FPFH(
    port_numbers=[1,2,3,4],         # update port_no
    addr="fpfh-hb10-21-p09.p09-leg.ska-lab.nsn-rdnet.net",   # update address
    login="admin",
    password="admin",
)

_ru_pdu6 = FPFH(
    port_numbers=[1,2,3],         # update port_no
    addr="fpfh-hb10-46-p09.p09-leg.ska-lab.nsn-rdnet.net",   # update address
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


_gnb0_pdu_port = PduPort(pdu=_bts_pdu, port_no=3) # ASIL SN: L1224211824
_gnb1_pdu_port = PduPort(pdu=_bts_pdu, port_no=4) # ASIL SN: L1213609083

_cus1_pdu_port = PduPort(pdu=_bts_pdu, port_no=5)
_cus2_pdu_port = PduPort(pdu=_bts_pdu, port_no=1)
_cus3_pdu_port = PduPort(pdu=_bts_pdu, port_no=6)

_ru0_pdu_port = PduPort(pdu=_ru_pdu0, port_no=6) # AHEB SN: EA220351218
_ru1_pdu_port = PduPort(pdu=_ru_pdu0, port_no=5) # AHEB SN: EA220657588
_ru2_pdu_port = PduPort(pdu=_ru_pdu0, port_no=4) # AHEB SN: EA202450266
_ru3_pdu_port = PduPort(pdu=_ru_pdu0, port_no=3) # AHEB SN: EA204650447

_ru4_pdu_port = PduPort(pdu=_ru_pdu1, port_no=3) # AHCA SN: 1M193119196
_ru5_pdu_port = PduPort(pdu=_ru_pdu1, port_no=2) # AHCA SN: AS204801898
_ru6_pdu_port = PduPort(pdu=_ru_pdu1, port_no=1) # AHCA SN: AS210105209

_ru7_pdu_port = PduPort(pdu=_ru_pdu2, port_no=6) # AHCA SN: AS193605502
_ru8_pdu_port = PduPort(pdu=_ru_pdu2, port_no=5) # AHCA SN: AS212504932
_ru9_pdu_port = PduPort(pdu=_ru_pdu2, port_no=4) # AHCA SN: AS200704299

_ru10_pdu_port = PduPort(pdu=_ru_pdu3, port_no=6) # AHFIB SN: BL2150V0UDB
_ru11_pdu_port = PduPort(pdu=_ru_pdu3, port_no=5) # AHFIB SN: BL2135V0JZ4
_ru12_pdu_port = PduPort(pdu=_ru_pdu3, port_no=4) # AHFIB SN: BL2045V0RYG
_ru13_pdu_port = PduPort(pdu=_ru_pdu3, port_no=3) # AHFIB SN: BL2045V0RVM

_ru14_pdu_port = PduPort(pdu=_ru_pdu4, port_no=3) # AHFIB SN: BL2039V0M82
_ru15_pdu_port = PduPort(pdu=_ru_pdu4, port_no=2) # AHFIB SN: BL2042V0PPY
_ru16_pdu_port = PduPort(pdu=_ru_pdu4, port_no=1) # AHFIB SN: BL2042V0PQB

_ru17_pdu_port = PduPort(pdu=_ru_pdu5, port_no=4) # AHFIB SN: BL2031V0F1V
_ru18_pdu_port = PduPort(pdu=_ru_pdu5, port_no=3) # AHFIB SN: BL1923V0A77
_ru19_pdu_port = PduPort(pdu=_ru_pdu5, port_no=2) # AHEGG SN: RW234301812
_ru20_pdu_port = PduPort(pdu=_ru_pdu5, port_no=1) # AHEB SN: EA220351216

_ru21_pdu_port = PduPort(pdu=_ru_pdu6, port_no=3) # AHEB SN: EA204650409
_ru22_pdu_port = PduPort(pdu=_ru_pdu6, port_no=2) # AHEB SN: EA204650274
_ru23_pdu_port = PduPort(pdu=_ru_pdu6, port_no=1) # AHEB SN: EA204650408


# ------------------------GNB0_CONFIGURATION------------------------

_test_pc_gnb_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT9SK108.p09.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_test_pc_gnb_0_secondary = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT9SK096.p09.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_gnb_0_instance_id = 80108
_gnb_0_global_bts_id = 80108

_gnb_0_primary_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_gnb_0.default_ssh_connection_details,
)

_gnb_0_secondary_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.119",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_gnb_0_secondary.default_ssh_connection_details,
)

_gnb_0_oam_ip = NetworkAddress(
    v4="10.84.140.108/23",
    routing_v4=RoutingInformation(gateway="10.84.141.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
) 

_gnb_0_f1m_ip = NetworkAddress(
    v4="10.84.140.108/23",
    routing_v4=RoutingInformation(gateway="10.84.141.254", destIpAddr="0.0.0.0"),
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
    v4="10.84.140.108/23",
    routing_v4=RoutingInformation(gateway="10.84.141.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
) 

_gnb_0_x2u_ip = NetworkAddress(
    v4="10.84.140.108/23",
    routing_v4=RoutingInformation(gateway="10.84.141.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
) 

_gnb_0_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
) 

_gnb_0_s1u_ip = NetworkAddress(
    v4="10.84.140.108/23",
    routing_v4=RoutingInformation(gateway="10.84.141.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
) 

_gnb_0_xnc_ip = NetworkAddress(
    v4="10.84.140.108/23",
    routing_v4=RoutingInformation(gateway="10.84.141.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
) 

_gnb_0_xnu_ip = NetworkAddress(
    v4="10.84.140.108/23",
    routing_v4=RoutingInformation(gateway="10.84.141.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
) 

_gnb_0_ngc_ip = NetworkAddress(
    v4="10.84.140.108/23",
    routing_v4=RoutingInformation(gateway="10.84.141.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
) 

_gnb_0_ngu_ip = NetworkAddress(
    v4="10.84.140.108/23",
    routing_v4=RoutingInformation(gateway="10.84.141.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
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
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS003105C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_1 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS003106C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_2 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS001010C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_3 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS001001C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_4 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS003103C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_5 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS003104C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_6 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS003100C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_7 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS003102C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_8 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS003101C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_9 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS001002C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_10 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS003107C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_11 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS001004C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_12 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS001035C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_13 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS001018C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_14 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS003118C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_15 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS003115C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_16 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS001040C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_17 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS001014C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_18 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS001028C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_19 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS003111C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_20 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS001039C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_21 = RU(
    ru_hw_group="AHEB",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHEB",
    serial_number="EA202450266",
    product_code="473484A.101",
    pdu_port=_ru2_pdu_port,
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_22 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS001024C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_23 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS001012C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_24 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS001005C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_25 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS001048C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_26 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS001026C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_27 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS002056C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_28 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS001041C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_29 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS002057C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_30 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS001030C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_31 = RU(
    ru_hw_group="AHFIB",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFIB",
    serial_number="BL1923V0A77",
    product_code="474216A.101",
    pdu_port=_ru18_pdu_port,
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_32 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS001038C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_33 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS003112C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_34 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS003109C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_35 = RU(
    ru_hw_group="AHFIB",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFIB",
    serial_number="BL2042V0PQB",
    product_code="474216A.101",
    pdu_port=_ru16_pdu_port,
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_36 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS001044C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_37 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS003113C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_38 = RU(
    ru_hw_group="AHFIB",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFIB",
    serial_number="BL2045V0RYG",
    product_code="474216A.101",
    pdu_port=_ru12_pdu_port,
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_39 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS001016C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_40 = RU(
    ru_hw_group="AHCA",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHCA",
    serial_number="AS212504932",
    product_code="473966B.101",
    pdu_port=_ru8_pdu_port,
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_41 = RU(
    ru_hw_group="AHFIB",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFIB",
    serial_number="BL2150V0UDB",
    product_code="474216A.101",
    pdu_port=_ru10_pdu_port,
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_42 = RU(
    ru_hw_group="AHCA",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHCA",
    serial_number="AS193605502",
    product_code="473966A.101",
    pdu_port=_ru7_pdu_port,
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_43 = RU(
    ru_hw_group="AHEB",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHEB",
    serial_number="EA204650447",
    product_code="473484A.101",
    pdu_port=_ru3_pdu_port,
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_44 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS003116C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_45 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS001027C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_46 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS001037C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_47 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS001020C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_48 = RU(
    ru_hw_group="AHFIB",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFIB",
    serial_number="BL2135V0JZ4",
    product_code="474216A.101",
    pdu_port=_ru11_pdu_port,
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_49 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS001025C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_50 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS001003C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_51 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS001017C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_52 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS003110C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_53 = RU(
    ru_hw_group="AHCA",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHCA",
    serial_number="AS210105209",
    product_code="473966A.101",
    pdu_port=_ru6_pdu_port,
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_54 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS003114C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_55 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS001023C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_56 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS001032C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_57 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS001034C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_58 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS001013C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_59 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS001036C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_60 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS001031C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_61 = RU(
    ru_hw_group="AHCA",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHCA",
    serial_number="1M193119196",
    product_code="473966B.101",
    pdu_port=_ru4_pdu_port,
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_62 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS002058C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_63 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS001033C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_64 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS001022C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_65 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS001015C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_66 = RU(
    ru_hw_group="AHCA",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHCA",
    serial_number="AS200704299",
    product_code="473966A.101",
    pdu_port=_ru9_pdu_port,
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_67 = RU(
    ru_hw_group="AHEB",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHEB",
    serial_number="EA220351216",
    product_code="473484A.101",
    pdu_port=_ru20_pdu_port,
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_68 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS003108C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_69 = RU(
    ru_hw_group="AHEGG",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHEGG",
    serial_number="RW234301812",
    product_code="476123A.101",
    pdu_port=_ru19_pdu_port,
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_70 = RU(
    ru_hw_group="AHCA",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHCA",
    serial_number="AS204801898",
    product_code="473966A.101",
    pdu_port=_ru5_pdu_port,
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_71 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS003120C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_72 = RU(
    ru_hw_group="AHFIB",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFIB",
    serial_number="BL2045V0RVM",
    product_code="474216A.101",
    pdu_port=_ru13_pdu_port,
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_73 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS001045C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_74 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS001047C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_75 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS002053C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_76 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS001043C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_77 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS001011C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_78 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS002054C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_79 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS002051C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_80 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS002049C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_81 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS002052C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_82 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS003119C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_83 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS002050C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_84 = RU(
    ru_hw_group="AHEB",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHEB",
    serial_number="EA204650409",
    product_code="473484A.101",
    pdu_port=_ru21_pdu_port,
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_85 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS002055C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_86 = RU(
    ru_hw_group="AHEB",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHEB",
    serial_number="EA204650274",
    product_code="473484A.101",
    pdu_port=_ru22_pdu_port,
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_87 = RU(
    ru_hw_group="AHFIB",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFIB",
    serial_number="BL2031V0F1V",
    product_code="474216A.101",
    pdu_port=_ru17_pdu_port,
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_88 = RU(
    ru_hw_group="AHEB",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHEB",
    serial_number="EA220351218",
    product_code="473484A.101",
    pdu_port=_ru0_pdu_port,
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_89 = RU(
    ru_hw_group="AHFIB",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFIB",
    serial_number="BL2039V0M82",
    product_code="474216A.101",
    pdu_port=_ru14_pdu_port,
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_90 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS001019C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_91 = RU(
    ru_hw_group="AHEB",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHEB",
    serial_number="EA220657588",
    product_code="473484A.101",
    pdu_port=_ru1_pdu_port,
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_92 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS001046C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_93 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS001029C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_94 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS001042C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_95 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS001021C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_96 = RU(
    ru_hw_group="AHEB",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHEB",
    serial_number="EA204650408",
    product_code="473484A.101",
    pdu_port=_ru23_pdu_port,
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_97 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS003117C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_98 = RU(
    ru_hw_group="AHFIB",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFIB",
    serial_number="BL2042V0PPY",
    product_code="474216A.101",
    pdu_port=_ru15_pdu_port,
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_99 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS003076C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_100 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS003098C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_101 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS003094C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_102 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS003099C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_103 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS002065C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_104 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS003077C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_105 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS003080C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_106 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS001009C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_107 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS002064C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_108 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS003084C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_109 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS003093C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_110 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS003090C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_111 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS002059C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_112 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS002061C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_113 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS002062C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_114 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS002066C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_115 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS001006C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_116 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS001008C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_117 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS002060C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_118 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS003085C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_119 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS003092C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_120 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS003081C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_121 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS002072C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_122 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS002071C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_123 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS003087C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_124 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS002068C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_125 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS003083C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_126 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS003074C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_127 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS003079C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_128 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS001007C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_129 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS003073C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_130 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS003091C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_131 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS003082C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_132 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS002070C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_133 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS003096C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_134 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS003095C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_135 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS003075C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_136 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS003078C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_137 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS003089C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_138 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS003086C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_139 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS002067C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_140 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS002063C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_141 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS002069C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_142 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS003097C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_143 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFII",
    serial_number="CUS003088C7",
    product_code="475656A.101",
    # pdu_port=PduPort(
    #     pdu=_ru_pdu, port_no=999
    # ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_capacity_unit_0 = CapacityUnit(
    addr="192.168.253.26",
    hardware_type="ABIO",
    hardware_version="A.105",
    serial_number="L1230606001",
    product_code="475266A.105",
    slot_id=SlotId.B2,
    rus=[_gnb_0_radio_unit_12, _gnb_0_radio_unit_16, _gnb_0_radio_unit_18, _gnb_0_radio_unit_20, _gnb_0_radio_unit_25, _gnb_0_radio_unit_26, _gnb_0_radio_unit_28, _gnb_0_radio_unit_30, _gnb_0_radio_unit_32, _gnb_0_radio_unit_36, _gnb_0_radio_unit_45, _gnb_0_radio_unit_46, _gnb_0_radio_unit_49, _gnb_0_radio_unit_56, _gnb_0_radio_unit_57, _gnb_0_radio_unit_59, _gnb_0_radio_unit_60, _gnb_0_radio_unit_63, _gnb_0_radio_unit_73, _gnb_0_radio_unit_74, _gnb_0_radio_unit_76, _gnb_0_radio_unit_92, _gnb_0_radio_unit_93, _gnb_0_radio_unit_94],
)

_gnb_0_capacity_unit_1 = CapacityUnit(
    addr="192.168.253.22",
    hardware_type="ABIO",
    hardware_version="A.104",
    serial_number="DH222840595",
    product_code="475266A.104",
    slot_id=SlotId.B1,
    rus=[_gnb_0_radio_unit_106, _gnb_0_radio_unit_11, _gnb_0_radio_unit_115, _gnb_0_radio_unit_116, _gnb_0_radio_unit_128, _gnb_0_radio_unit_13, _gnb_0_radio_unit_17, _gnb_0_radio_unit_2, _gnb_0_radio_unit_22, _gnb_0_radio_unit_23, _gnb_0_radio_unit_24, _gnb_0_radio_unit_3, _gnb_0_radio_unit_39, _gnb_0_radio_unit_47, _gnb_0_radio_unit_50, _gnb_0_radio_unit_51, _gnb_0_radio_unit_55, _gnb_0_radio_unit_58, _gnb_0_radio_unit_64, _gnb_0_radio_unit_65, _gnb_0_radio_unit_77, _gnb_0_radio_unit_9, _gnb_0_radio_unit_90, _gnb_0_radio_unit_95],
)

_gnb_0_capacity_unit_2 = CapacityUnit(
    addr="",
    hardware_type="ABIO",
    hardware_version="A.104",
    serial_number="DH221847287",
    product_code="475266A.104",
    slot_id=SlotId.B4,
    rus=[_gnb_0_radio_unit_101, _gnb_0_radio_unit_104, _gnb_0_radio_unit_105, _gnb_0_radio_unit_108, _gnb_0_radio_unit_109, _gnb_0_radio_unit_110, _gnb_0_radio_unit_118, _gnb_0_radio_unit_119, _gnb_0_radio_unit_120, _gnb_0_radio_unit_123, _gnb_0_radio_unit_125, _gnb_0_radio_unit_126, _gnb_0_radio_unit_127, _gnb_0_radio_unit_129, _gnb_0_radio_unit_130, _gnb_0_radio_unit_131, _gnb_0_radio_unit_133, _gnb_0_radio_unit_134, _gnb_0_radio_unit_135, _gnb_0_radio_unit_136, _gnb_0_radio_unit_137, _gnb_0_radio_unit_138, _gnb_0_radio_unit_143, _gnb_0_radio_unit_99],
)

_gnb_0_capacity_unit_3 = CapacityUnit(
    addr="",
    hardware_type="ABIO",
    hardware_version="A.105",
    serial_number="L1230613319",
    product_code="475266A.105",
    slot_id=SlotId.B6,
    rus=[_gnb_0_radio_unit_21, _gnb_0_radio_unit_31, _gnb_0_radio_unit_35, _gnb_0_radio_unit_38, _gnb_0_radio_unit_40, _gnb_0_radio_unit_41, _gnb_0_radio_unit_42, _gnb_0_radio_unit_43, _gnb_0_radio_unit_48, _gnb_0_radio_unit_53, _gnb_0_radio_unit_61, _gnb_0_radio_unit_66, _gnb_0_radio_unit_67, _gnb_0_radio_unit_69, _gnb_0_radio_unit_70, _gnb_0_radio_unit_72, _gnb_0_radio_unit_84, _gnb_0_radio_unit_86, _gnb_0_radio_unit_87, _gnb_0_radio_unit_88, _gnb_0_radio_unit_89, _gnb_0_radio_unit_91, _gnb_0_radio_unit_96, _gnb_0_radio_unit_98],
)

_gnb_0_capacity_unit_4 = CapacityUnit(
    addr="",
    hardware_type="ABIO",
    hardware_version="A.104",
    serial_number="DH221847286",
    product_code="475266A.104",
    slot_id=SlotId.B5,
    rus=[_gnb_0_radio_unit_0, _gnb_0_radio_unit_1, _gnb_0_radio_unit_10, _gnb_0_radio_unit_100, _gnb_0_radio_unit_102, _gnb_0_radio_unit_14, _gnb_0_radio_unit_142, _gnb_0_radio_unit_15, _gnb_0_radio_unit_19, _gnb_0_radio_unit_33, _gnb_0_radio_unit_34, _gnb_0_radio_unit_37, _gnb_0_radio_unit_4, _gnb_0_radio_unit_44, _gnb_0_radio_unit_5, _gnb_0_radio_unit_52, _gnb_0_radio_unit_54, _gnb_0_radio_unit_6, _gnb_0_radio_unit_68, _gnb_0_radio_unit_7, _gnb_0_radio_unit_71, _gnb_0_radio_unit_8, _gnb_0_radio_unit_82, _gnb_0_radio_unit_97],
)

_gnb_0_capacity_unit_5 = CapacityUnit(
    addr="192.168.253.30",
    hardware_type="ABIO",
    hardware_version="A.104",
    serial_number="L1222606859",
    product_code="475266A.104",
    slot_id=SlotId.B3,
    rus=[_gnb_0_radio_unit_103, _gnb_0_radio_unit_107, _gnb_0_radio_unit_111, _gnb_0_radio_unit_112, _gnb_0_radio_unit_113, _gnb_0_radio_unit_114, _gnb_0_radio_unit_117, _gnb_0_radio_unit_121, _gnb_0_radio_unit_122, _gnb_0_radio_unit_124, _gnb_0_radio_unit_132, _gnb_0_radio_unit_139, _gnb_0_radio_unit_140, _gnb_0_radio_unit_141, _gnb_0_radio_unit_27, _gnb_0_radio_unit_29, _gnb_0_radio_unit_62, _gnb_0_radio_unit_75, _gnb_0_radio_unit_78, _gnb_0_radio_unit_79, _gnb_0_radio_unit_80, _gnb_0_radio_unit_81, _gnb_0_radio_unit_83, _gnb_0_radio_unit_85],
)

_gnb_0_common_unit_0 = CommonUnit(
    lmp_connection=_gnb_0_primary_ssh_lmp_connection,
    capacity_units=[_gnb_0_capacity_unit_0, _gnb_0_capacity_unit_1, _gnb_0_capacity_unit_5],
    hardware_type="ASIL",
    hardware_version="A.103",
    serial_number="L1224211824",
    mac_addr="60:8f:a4:bf:f0:5",
    # trs_connections=[TRSInterfaces.EIF1],
    slot_id=SlotId.C1,
    pdu_port=_gnb0_pdu_port
)

_gnb_0_common_unit_1 = CommonUnit(
    lmp_connection=_gnb_0_secondary_ssh_lmp_connection,
    capacity_units=[_gnb_0_capacity_unit_2, _gnb_0_capacity_unit_3, _gnb_0_capacity_unit_4],
    hardware_type="ASIL",
    hardware_version="A.101",
    serial_number="L1213609083",
    mac_addr="60:8f:a4:bf:f0:5",
    # trs_connections=[TRSInterfaces.EIF1],
    slot_id=SlotId.C2,
    pdu_port=_gnb1_pdu_port
)

_gnb_0_airscale = Airscale(
    common_units=[_gnb_0_common_unit_0, _gnb_0_common_unit_1],
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

_test_pc_gnb_0_secondary.connections = [
    Connection(
        device=_gnb_0.dus[0].airscale.common_units[1],
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


_ue_config=_set_abstract_lib_config_env("ue_config.yaml")

# ------------------------CUS_CONFIGURATION------------------------

## CUS1
_cus_common_unit1 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.200.1",
        username="toor4nsn",
        password="oZPS0POrRieRtu"
    ),
    capacity_units=[CapacityUnit(
        addr="192.168.253.36",
        hardware_type="ABIA"
    )],
    pdu_port=_cus1_pdu_port,
    hardware_type="ASIA"
)
_cus_airscale1 = Airscale(common_units=[_cus_common_unit1])
_cus1 = CUS(l1=_cus_airscale1)

## CUS2
_cus_common_unit2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.200.2",
        username="toor4nsn",
        password="oZPS0POrRieRtu"
    ),
    capacity_units=[CapacityUnit(
        addr="192.168.253.40",
        hardware_type="ABIA"
    )],
    pdu_port=_cus2_pdu_port,
    hardware_type="ASIA"
)
_cus_airscale2 = Airscale(common_units=[_cus_common_unit2])
_cus2 = CUS(l1=_cus_airscale2)

## CUS3
_cus_common_unit1 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.200.3",
        username="toor4nsn",
        password="oZPS0POrRieRtu"
    ),
    capacity_units=[CapacityUnit(
        addr="192.168.253.44",
        hardware_type="ABIA"
    )],
    pdu_port=_cus3_pdu_port,
    hardware_type="ASIA"
)
_cus_airscale3 = Airscale(common_units=[_cus_common_unit1])
_cus3 = CUS(l1=_cus_airscale3)

# ------------------------TL_CONFIGURATION------------------------


tl = TestLine(
    test_pc=_test_pc_gnb_0,
    gnbs=[_gnb_0],
    enbs=[_gnb_0], # uncomment for OAM KPI TCs
    ues=[_ue_config, _cus1, _cus2, _cus3],
    test_pcs=[_test_pc_gnb_0, _test_pc_gnb_0_secondary],
    tl_cloud_topology="CLOUD_7_7_T09SK108",
    pdus=[_bts_pdu, _ru_pdu0, _ru_pdu1, _ru_pdu2, _ru_pdu3, _ru_pdu4, _ru_pdu5, _ru_pdu6],
)

__all__ = ["tl"]