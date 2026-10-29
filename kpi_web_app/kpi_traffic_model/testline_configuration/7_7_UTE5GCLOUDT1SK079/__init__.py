__maintainer__ = "I_MN_5GSC_KRK_AUTO"
__team__ = "I_MN_5GSC_KRK_AUTO"
__email__ = "I_MN_5GSC_KRK_AUTO@internal.nsn.com"

import os
import yaml
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
)
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline import NetworkAddress, RU, RoutingInformation
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.pdu import PduPort, FPFH, HPE


# The most commonly used testline configuration. #
_lmp_ip = "192.168.255.129"

_test_pc_gnb_default_ssh_connection_details = SshServiceDetails(
    addr="7-7-UTE5GCLOUDT1SK079.p01.ska-lab.nsn-rdnet.net",
    username="ute",
    password="ute",
)
_hub_proxy_pc_ssh_connection_details = SshServiceDetails(
    addr="7-7-UTE5GCLOUDT1SK020.p01.ska-lab.nsn-rdnet.net",
    username="ute",
    password="ute",
)

_gnb_bh_ip_v4 = "10.84.164.79"
_gnb_bh_ip_v6 = "2a00:8a02:60:48::79"
_gnb_oam_ip = _gnb_bh_ip_v4
_gnb_oam_backhaul_ip = NetworkAddress(
    v4="{}/23".format(_gnb_bh_ip_v4),
    routing_v4=RoutingInformation(gateway="10.84.165.254"),
    v6=_gnb_bh_ip_v6,
    routing_v6=RoutingInformation(gateway="2a00:8a02:60:48:ffff:ffff:ffff:fffe"),
    vlan_id=504,
)
_gnb_u_plane_ip = NetworkAddress(v4=_gnb_bh_ip_v4, vlan_id=504)
_gnb_c_plane_ip = NetworkAddress(v4=_gnb_bh_ip_v4, vlan_id=504)
_gnb_s1_plane_ip = NetworkAddress(v4=_gnb_bh_ip_v4, vlan_id=504)
_gnb_instance_id = 76079
_gnb_global_bts_id = 76079
_gnb_du_common_unit_hardware_type = "ASIA"

_gnb_ru_1_ip = NetworkAddress(v4="172.16.9.129")

_pdu1 = FPFH(
    port_numbers=[3],
    addr="fpfh-zc18-46-p01.p01-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

_snmp_user = {
    "userName": "admin",
    "authKey": "password",
    "privKey": "password",
    "authProtocol": "MD5",
    "privProtocol": "DES",
}

_pdu2 = HPE(
    port_numbers=[14], addr="zc18.mgt.ska-lab.nsn-rdnet.net", snmp_user=_snmp_user
)

##############################################################
# Default values
_default_ssh_lmp_connection = SshServiceDetails(
    addr=_lmp_ip, username="toor4nsn", password="oZPS0POrRieRtu"
)
_default_oam_http_connection_gnb = HttpConnectionDetails(
    addr=_gnb_oam_ip, username="Nemuadmin", password="nemuuser", port=443
)

##############################################################
# Important!: check and change below if other than default #
# gNB section
_ru_1_gnb = RU(
    radio_type="APHA",
    ru_hw_group="APHA",
    serial_number="NH224300809",
    default_ssh_connection_details=SshServiceDetails(
        addr=_gnb_ru_1_ip.v4, username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=PduPort(pdu=_pdu2, port_no=14),
)

_radio_units_gnb = [_ru_1_gnb]

_cu_gnb = CU(
    oam_ssh_connection_details=_default_ssh_lmp_connection,  # replace if other than default
    oam_http_connection_details=_default_oam_http_connection_gnb,
    backhaul_site_oam_ip=_gnb_oam_backhaul_ip,
    x2c=_gnb_c_plane_ip,
    x2u=_gnb_u_plane_ip,
    s1u=_gnb_s1_plane_ip,
)  # replace if other than default

_abia1_gnb = CapacityUnit(addr="192.168.253.20", hardware_type="ABIA")
_abia2_gnb = CapacityUnit(addr="192.168.253.24", hardware_type="ABIA")
_asia1_gnb = CapacityUnit(addr="192.168.253.16", hardware_type="ASIA")
_capacity_units_gnb = [_asia1_gnb, _abia1_gnb, _abia2_gnb]
_du_lmp_connection_gnb = _default_ssh_lmp_connection
_du_lmp_connection_gnb.proxy = _test_pc_gnb_default_ssh_connection_details
_du_common_unit_gnb = CommonUnit(
    lmp_connection=_du_lmp_connection_gnb,
    pdu_port=_pdu1.pdu_ports[3],
    hardware_type=_gnb_du_common_unit_hardware_type,
    capacity_units=_capacity_units_gnb,
)

_airscale_gnb = Airscale(common_units=[_du_common_unit_gnb])
_du_gnb = DU(airscale=_airscale_gnb, rus=_radio_units_gnb)
_gnb_main = ClassicalBts(
    cu=_cu_gnb,
    dus=[_du_gnb],
    instance_id=_gnb_instance_id,
    global_bts_id=_gnb_global_bts_id,
)

##############################################################
# Important!: check and change below if other than default #
# Test PCs
_test_pc_gnb = TestPc(
    default_ssh_connection_details=_test_pc_gnb_default_ssh_connection_details,
    connections=[_du_common_unit_gnb],
)

_hub_proxy_pc = TestPc(
    default_ssh_connection_details=_hub_proxy_pc_ssh_connection_details
)

# Testline
tl = TestLine(
    gnbs=[_gnb_main],
    test_pc=_test_pc_gnb,
    test_pcs=[_test_pc_gnb, _hub_proxy_pc],
    pdus=[_pdu1, _pdu2],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_ASIAL_ASIR_ABIAB1B2_2xAHENB_APHA",
)
__all__ = ["tl"]
