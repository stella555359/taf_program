# Generated with TL configuration generator at 2025-02-05_15:05:01

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

_bts_pdu = FPFH(
    port_numbers=[6],         # update port_no
    addr="fpfh-ze10-34-p04.p04-leg.ska-lab.nsn-rdnet.net",   # update address
    login="admin",
    password="admin",
)

_bts_pdu_4G = FPFH(
    port_numbers=[1],         # update port_no
    addr="fpfh-ze10-21-p04.p04-leg.ska-lab.nsn-rdnet.net",   # update address
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

_ru_pdu_1 = FPFH(
    port_numbers=[1, 2, 3, 4, 5, 6],         # update port_no
    addr="fpfh-ze08-03-p04.p04-leg.ska-lab.nsn-rdnet.net",   # update address
    login="admin",
    password="admin",
)

_ru_pdu_2 = FPFH(
    port_numbers=[1, 2, 3, 4, 5, 6],         # update port_no
    addr="fpfh-ze08-06-p04.p04-leg.ska-lab.nsn-rdnet.net",   # update address
    login="admin",
    password="admin",
)

_ru_pdu_3 = FPFH(
    port_numbers=[1],         # update port_no
    addr="fpfh-ze08-09-p04.p04-leg.ska-lab.nsn-rdnet.net",   # update address
    login="admin",
    password="admin",
)

_ru_pdu_ZF17 = FPFH(
    port_numbers=[1],         # update port_no
    addr="fpfh-zf17-46-p01.p01-leg.ska-lab.nsn-rdnet.net",   # update address
    login="admin",
    password="admin",
)

_ru_pdu_ZF13 = FPFH(
    port_numbers=[3],         # update port_no
    addr="fpfh-zf13-46-p04.p04-leg.ska-lab.nsn-rdnet.net",   # update address
    login="admin",
    password="admin",
)

_ru_pdu_ZF09 = FPFH(
    port_numbers=[6],         # update port_no
    addr="FPFH-ZF09-46-P04.p04-leg.ska-lab.nsn-rdnet.net",   # update address
    login="admin",
    password="admin",
)

_ru_pdu_ZE10 = FPFH(
    port_numbers=[3],         # update port_no
    addr="fpfh-ze10-46-p04.p04-leg.ska-lab.nsn-rdnet.net",   # update address
    login="admin",
    password="admin",
)

_ru_pdu_ZE13 = FPFH(
    port_numbers=[3],         # update port_no
    addr="fpfh-ze13-46-p09.p09-leg.ska-lab.nsn-rdnet.net",   # update address
    login="admin",
    password="admin",
)

_ru_pdu_ZE17 = FPFH(
    port_numbers=[4],         # update port_no
    addr="fpfh-ze17-40-p01.p01-leg.ska-lab.nsn-rdnet.net",   # update address
    login="admin",
    password="admin",
)

# ------------------------GNB0_CONFIGURATION------------------------

_test_pc_gnb_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT4SK078.p04.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_test_pc_gnb_0_secondary = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT4SK078.p04.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_gnb_0_instance_id = 77078
_gnb_0_global_bts_id = 77078

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
    v4="10.84.190.78/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_0_f1m_ip = NetworkAddress(
    v4="10.84.190.78/23",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
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
    v4="172.16.4.1/16",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=1578,
)

_gnb_0_x2u_ip = NetworkAddress(
    v4="172.16.4.1/16",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=1578,
)

_gnb_0_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_0_s1u_ip = NetworkAddress(
    v4="172.16.4.1/16",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=1578,
)

_gnb_0_xnc_ip = NetworkAddress(
    v4="172.16.4.1/16",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=1578,
)

_gnb_0_xnu_ip = NetworkAddress(
    v4="172.16.4.1/16",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=1578,
)

_gnb_0_ngc_ip = NetworkAddress(
    v4="172.16.4.1/16",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=1578,
)

_gnb_0_ngu_ip = NetworkAddress(
    v4="172.16.4.1/16",
    routing_v4=RoutingInformation(gateway="10.84.191.254", destIpAddr="0.0.0.0"),
    vlan_id=1578,
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
    ru_hw_group="AHCA",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHCA",
    serial_number="L1181711703",
    product_code="473966A.101",
    pdu_port=PduPort(pdu=_ru_pdu_1, port_no=2),  # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_0_radio_unit_1 = RU(
    ru_hw_group="AHCA",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHCA",
    serial_number="L1181800806",
    product_code="473966A.101",
    pdu_port=PduPort(pdu=_ru_pdu_3, port_no=1),  # uncomment & update port_no for gNB - for eNB you can delete
)


_gnb_0_radio_unit_2 = RU(
    ru_hw_group="AEWB",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="wv48zrV4zEjjQ5nIWXuwfWlQ23oNBkEr7/5AMdaUDIQ=",
    ),
    radio_type="AEWB",
    serial_number="AH211900313",
    product_code="474609A.105",
    pdu_port=PduPort(pdu=_ru_pdu_ZE10, port_no=3),  # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_0_radio_unit_3 = RU(
    ru_hw_group="AQQK",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    radio_type="AQQK",
    serial_number="L1223214939",
    product_code="476138A.101",
    pdu_port=PduPort(pdu=_ru_pdu_2, port_no=3),  # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_0_radio_unit_4 = RU(
    ru_hw_group="AQQK",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    radio_type="AQQK",
    serial_number="L1223613424",
    product_code="476138A.101",
    pdu_port=PduPort(pdu=_ru_pdu_2, port_no=1),  # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_0_radio_unit_5 = RU(
    ru_hw_group="AHFIB",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFIB",
    serial_number="K9180218179",
    product_code="474216A.101",
    pdu_port=PduPort(pdu=_ru_pdu_ZF09, port_no=6),  # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_0_radio_unit_6 = RU(
    ru_hw_group="AHCA",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHCA",
    serial_number="L1181711698",
    product_code="473966A.101",
    pdu_port=PduPort(pdu=_ru_pdu_1, port_no=3),  # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_0_radio_unit_7 = RU(
    ru_hw_group="AHFIB",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFIB",
    serial_number="BL2124V0E1G",
    product_code="474216A.101",
    pdu_port=PduPort(pdu=_ru_pdu_ZF17, port_no=1),  # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_0_radio_unit_8 = RU(
    ru_hw_group="AQQK",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    radio_type="AQQK",
    serial_number="L1223613422",
    product_code="476138A.101",
    pdu_port=PduPort(pdu=_ru_pdu_1, port_no=1),  # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_0_radio_unit_9 = RU(
    ru_hw_group="AEQU",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="bobuWrUHk7Xq7WPpY9ZcjEi8zNdX3plZ+/y420RZ7W4=",
    ),
    radio_type="AEQU",
    serial_number="DH223305085",
    product_code="476085A.101",
    pdu_port=PduPort(pdu=_ru_pdu_2, port_no=4),  # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_0_radio_unit_10 = RU(
    ru_hw_group="AEQU",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="bobuWrUHk7Xq7WPpY9ZcjEi8zNdX3plZ+/y420RZ7W4=",
    ),
    radio_type="AEQU",
    serial_number="DH223600249",
    product_code="476085A.101",
    pdu_port=PduPort(pdu=_ru_pdu_2, port_no=5),  # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_0_radio_unit_11 = RU(
    ru_hw_group="AHLOA",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHLOA",
    serial_number="BL2027G1AV3",
    product_code="474331A.101",
    pdu_port=PduPort(pdu=_ru_pdu_1, port_no=6),  # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_0_radio_unit_12 = RU(
    ru_hw_group="AEWB",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="wv48zrV4zEjjQ5nIWXuwfWlQ23oNBkEr7/5AMdaUDIQ=",
    ),
    radio_type="AEWB",
    serial_number="AH194806900",
    product_code="474609A.103",
    pdu_port=PduPort(pdu=_ru_pdu_ZE13, port_no=3),  # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_0_radio_unit_13 = RU(
    ru_hw_group="AEWB",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="wv48zrV4zEjjQ5nIWXuwfWlQ23oNBkEr7/5AMdaUDIQ=",
    ),
    radio_type="AEWB",
    serial_number="AH220602870",
    product_code="474609A.105",
    pdu_port=PduPort(pdu=_ru_pdu_ZE17, port_no=4),  # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_0_radio_unit_14 = RU(
    ru_hw_group="AHFIB",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHFIB",
    serial_number="BL2124V0E4N",
    product_code="474216A.101",
    pdu_port=PduPort(pdu=_ru_pdu_ZF13, port_no=3),  # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_0_radio_unit_15 = RU(
    ru_hw_group="AHLOA",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHLOA",
    serial_number="BL2050G1SHE",
    product_code="474331A.101",
    pdu_port=PduPort(pdu=_ru_pdu_1, port_no=5),  # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_0_radio_unit_16 = RU(
    ru_hw_group="AHLOA",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHLOA",
    serial_number="BL1933G101J",
    product_code="474331A.101",
    pdu_port=PduPort(pdu=_ru_pdu_2, port_no=2),  # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_0_radio_unit_17 = RU(
    ru_hw_group="AEQU",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="bobuWrUHk7Xq7WPpY9ZcjEi8zNdX3plZ+/y420RZ7W4=",
    ),
    radio_type="AEQU",
    serial_number="DH223705220",
    product_code="476085A.101",
    pdu_port=PduPort(pdu=_ru_pdu_2, port_no=6),  # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_0_capacity_unit_0 = CapacityUnit(
    addr="",
    hardware_type="ABIO",
    hardware_version="A.104",
    serial_number="L1223704736",
    product_code="475266A.104",
    slot_id=SlotId.B2,
    rus=[_gnb_0_radio_unit_10, _gnb_0_radio_unit_17, _gnb_0_radio_unit_3, _gnb_0_radio_unit_4, _gnb_0_radio_unit_8, _gnb_0_radio_unit_9],
    )

_gnb_0_capacity_unit_1 = CapacityUnit(
    addr="",
    hardware_type="ABIO",
    hardware_version="A.104",
    serial_number="L1223704735",
    product_code="475266A.104",
    slot_id=SlotId.B3,
    rus=[_gnb_0_radio_unit_11, _gnb_0_radio_unit_15, _gnb_0_radio_unit_16],
    )

_gnb_0_capacity_unit_2 = CapacityUnit(
    addr="",
    hardware_type="ABIA",
    hardware_version="A.102",
    serial_number="L1162608429",
    product_code="473096A.102",
    slot_id=SlotId.B4,
    rus=[_gnb_0_radio_unit_11, _gnb_0_radio_unit_15, _gnb_0_radio_unit_16],
    )

_gnb_0_capacity_unit_3 = CapacityUnit(
    addr="",
    hardware_type="ABIO",
    hardware_version="A.104",
    serial_number="L1223704737",
    product_code="475266A.104",
    slot_id=SlotId.B1,
    rus=[_gnb_0_radio_unit_12, _gnb_0_radio_unit_13, _gnb_0_radio_unit_2],
    )

_gnb_0_capacity_unit_4 = CapacityUnit(
    addr="",
    hardware_type="ABIA",
    hardware_version="A.103",
    serial_number="DH192250189",
    product_code="473096A.103",
    slot_id=SlotId.B5,
    rus=[_gnb_0_radio_unit_0, _gnb_0_radio_unit_1, _gnb_0_radio_unit_14, _gnb_0_radio_unit_5, _gnb_0_radio_unit_6, _gnb_0_radio_unit_7],
    )

_gnb_0_common_unit_0 = CommonUnit(
    lmp_connection=_gnb_0_secondary_ssh_lmp_connection,
    capacity_units=[_gnb_0_capacity_unit_2, _gnb_0_capacity_unit_4],
    hardware_type="ASIB",
    hardware_version="A.102",
    serial_number="L1213105535",
    mac_addr="00:77:e4:23:58:15",
    # trs_connections=[TRSInterfaces.EIF1],
    slot_id=SlotId.C2,
    # pdu_port=PduPort(pdu=_bts_pdu, port_no=999),    # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_0_common_unit_1 = CommonUnit(
    lmp_connection=_gnb_0_primary_ssh_lmp_connection,
    capacity_units=[_gnb_0_capacity_unit_0, _gnb_0_capacity_unit_1, _gnb_0_capacity_unit_3],
    hardware_type="ASIB",
    hardware_version="A.102",
    serial_number="L1204902408",
    mac_addr="00:77:e4:23:58:15",
    # trs_connections=[TRSInterfaces.EIF1],
    slot_id=SlotId.C1,
    # pdu_port=PduPort(pdu=_bts_pdu, port_no=999),    # uncomment & update port_no for gNB - for eNB you can delete
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

# ------------------------TL_CONFIGURATION------------------------


tl = TestLine(
    test_pc=_test_pc_gnb_0,
    gnbs=[_gnb_0],
    test_pcs=[_test_pc_gnb_0, _test_pc_gnb_0_secondary],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_6xUE_ASIKL_ABILB1B2B3_3xAUEB"
)

__all__ = ["tl"]
