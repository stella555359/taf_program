# Generated with TL configuration generator at 2023-12-07_11:01:03

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
import os
import yaml

# ------------------------PDU_CONFIGURATION------------------------

_bts_pdu = FPFH(
    port_numbers=[6],         # update port_no
    addr="fpfh-zd04-31-p09.p09-leg.ska-lab.nsn-rdnet.net",   # update address
    login="admin",
    password="admin",
)

_hpe_snmp_user = {
    "userName": "administrator",
    "authKey": "password",
    "privKey": "password",
    "authProtocol": "MD5",
    "privProtocol": "DES",
}

_ru_pdu = HPE(
    port_numbers=[24],         # update port_no
    addr="zd03.mgt.ska-lab.nsn-rdnet.net",    # update address
    snmp_user=_hpe_snmp_user,
)

# ------------------------GNB_CONFIGURATION------------------------

_gnb_oam_ip = NetworkAddress(
    v4="10.84.165.148/23",
    routing_v4=RoutingInformation(gateway="10.84.165.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
) 

_gnb_f1m_ip = NetworkAddress(
    v4="10.84.165.148/23",
    routing_v4=RoutingInformation(gateway="10.84.165.254", destIpAddr="0.0.0.0"),
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
    v4="10.84.165.148/23",
    routing_v4=RoutingInformation(gateway="10.84.165.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
) 

_gnb_x2u_ip = NetworkAddress(
    v4="10.84.165.148/23",
    routing_v4=RoutingInformation(gateway="10.84.165.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
) 

_gnb_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
) 

_gnb_s1u_ip = NetworkAddress(
    v4="10.84.165.148/23",
    routing_v4=RoutingInformation(gateway="10.84.165.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
) 

_gnb_xnc_ip = NetworkAddress(
    v4="10.84.165.148/23",
    routing_v4=RoutingInformation(gateway="10.84.165.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
) 

_gnb_xnu_ip = NetworkAddress(
    v4="10.84.165.148/23",
    routing_v4=RoutingInformation(gateway="10.84.165.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
) 

_gnb_ngc_ip = NetworkAddress(
    v4="10.84.165.148/23",
    routing_v4=RoutingInformation(gateway="10.84.165.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
) 

_gnb_ngu_ip = NetworkAddress(
    v4="10.84.165.148/23",
    routing_v4=RoutingInformation(gateway="10.84.165.254", destIpAddr="0.0.0.0"),
    vlan_id=0,
) 

_test_pc_gnb = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT9SK148.p09.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_gnb_instance_id = 80148
_gnb_global_bts_id = 80148

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
     ru_hw_group="AWPQZ",
     default_ssh_connection_details=SshServiceDetails(
        addr="172.16.37.128",
        username="toor4nsn",
        password="oZPS0POrRieRtu",
     ),
     radio_type="AWPQZ",
     serial_number="EB2314R0362",
     product_code="476101A.101",
     pdu_port=PduPort(pdu=_ru_pdu, port_no=24),    # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_capacity_unit_0 = CapacityUnit(
    addr="192.168.253.42",
    hardware_type="ABIA",
    hardware_version="A.103",
    serial_number="L1172908171",
    product_code="473096A.103",
    slot_id=SlotId.B5,
    rus=[],
    )

_gnb_common_unit_0 = CommonUnit(
    lmp_connection=_default_gnb_ssh_lmp_connection,
    capacity_units=[_gnb_capacity_unit_0],
    hardware_type="ASOF",
    hardware_version="A.X21",
    serial_number="EA231054124",
    mac_addr="",
    # trs_connections=[],
    slot_id=SlotId.C2,
    pdu_port=PduPort(pdu=_bts_pdu, port_no=6),    # uncomment & update port_no for gNB - for eNB you can delete
)

_airscale_gnb = Airscale(
    common_units=[_gnb_common_unit_0],
    product_code="476147A",
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


tl = TestLine(
    test_pc=_test_pc_gnb,
    gnbs=[_gnb],
    test_pcs=[_test_pc_gnb],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_ASOF_3xAWPQZ_MRAT"
)

__all__ = ["tl"]
