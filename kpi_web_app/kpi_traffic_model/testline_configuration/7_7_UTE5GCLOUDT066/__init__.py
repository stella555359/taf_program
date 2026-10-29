# Generated with TL configuration generator at 2025-08-26_07:11:25

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
    port_numbers=[1, 5, 6],         # update port_no
    addr="fpfh-gh02-48-sc5g.sc5g-leg.krk-lab.nsn-rdnet.net",   # update address
    login="admin",
    password="admin",
)

_bts_pdu_2 = FPFH(
    port_numbers=[3],         # update port_no
    addr="fpfh-gh01-48-sc5g.sc5g-leg.krk-lab.nsn-rdnet.net",   # update address
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
        addr="7-7-UTE5GCLOUDT066.sc5g.krk-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_gnb_0_instance_id = 75066
_gnb_0_global_bts_id = 75066

_gnb_0_primary_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_gnb_0.default_ssh_connection_details,
)

_gnb_0_oam_ip = NetworkAddress(
    v4="10.83.182.66/23",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=503,
)

_gnb_0_f1m_ip = NetworkAddress(
    v4="10.83.182.66/23",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
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
    v4="10.83.252.66/23",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=541,
)

_gnb_0_x2u_ip = NetworkAddress(
    v4="10.253.214.66/23",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=543,
)

_gnb_0_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_0_s1u_ip = NetworkAddress(
    v4="10.253.214.66/23",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=543,
)

_gnb_0_xnc_ip = NetworkAddress(
    v4="10.83.182.66/23",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=503,
)

_gnb_0_xnu_ip = NetworkAddress(
    v4="10.83.252.66/23",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=541,
)

_gnb_0_ngc_ip = NetworkAddress(
    v4="10.83.182.66/23",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=503,
)

_gnb_0_ngu_ip = NetworkAddress(
    v4="10.83.252.66/23",
    routing_v4=RoutingInformation(gateway="10.83.183.254", destIpAddr="0.0.0.0"),
    vlan_id=541,
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
    ru_hw_group="AWHQU",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="oBrd1RgbOasUtYAeVfxrW9yGHb6ONl0w+MJUoKrBMGE=",
    ),
    radio_type="AWHQU",
    serial_number="AH242402112",
    product_code="476212A.102",
    pdu_port=PduPort(
        pdu=_bts_pdu, port_no=6
    ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_1 = RU(
    ru_hw_group="AWHQN",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="oBrd1RgbOasUtYAeVfxrW9yGHb6ONl0w+MJUoKrBMGE=",
    ),
    radio_type="AWHQN",
    serial_number="EB2144R0534",
    product_code="475701A.X22",
    pdu_port=PduPort(
        pdu=_bts_pdu, port_no=5
    ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_2 = RU(
    ru_hw_group="AWHQU",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="serviceuser",
        password="oBrd1RgbOasUtYAeVfxrW9yGHb6ONl0w+MJUoKrBMGE=",
    ),
    radio_type="AWHQU",
    serial_number="AH242402095",
    product_code="476212A.102",
    pdu_port=PduPort(
        pdu=_bts_pdu, port_no=1
    ),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_capacity_unit_0 = CapacityUnit(
    addr="192.168.253.26",
    hardware_type="ABIP",
    hardware_version="A.102",
    serial_number="L1233701352",
    product_code="475792A.102",
    slot_id=SlotId.B2,
    rus=[_gnb_0_radio_unit_0],
)

_gnb_0_capacity_unit_1 = CapacityUnit(
    addr="192.168.253.22",
    hardware_type="ABIO",
    hardware_version="A.104",
    serial_number="L1214610654",
    product_code="475266A.104",
    slot_id=SlotId.B1,
    rus=[_gnb_0_radio_unit_1, _gnb_0_radio_unit_2],
)

_gnb_0_common_unit_0 = CommonUnit(
    lmp_connection=_gnb_0_primary_ssh_lmp_connection,
    capacity_units=[_gnb_0_capacity_unit_0, _gnb_0_capacity_unit_1],
    hardware_type="ASIM",
    hardware_version="A.104",
    serial_number="L1233302537",
    mac_addr="28:74:f5:09:fc:9",
    # trs_connections=[TRSInterfaces.EIF1],
    slot_id=SlotId.C1,
    pdu_port=PduPort(
        pdu=_bts_pdu_2, port_no=3
    ),  # uncomment & update port_no for gNB - for eNB you can delete
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
    tl_cloud_topology="CLOUD_5G_CLASSICAL_SMAWAVE_SA_ASIB_ABIO_APHA",
)

__all__ = ["tl"]
