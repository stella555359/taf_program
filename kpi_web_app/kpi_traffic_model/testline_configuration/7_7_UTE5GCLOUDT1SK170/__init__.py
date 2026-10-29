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
_test_pc_gnb_default_ssh_connection_details = SshServiceDetails(
    addr="7-7-UTE5GCLOUDT1SK170.p01.ska-lab.nsn-rdnet.net",
    username="ute",
    password="ute",
)

_gnb_bh_ip = "10.84.164.170"
_gbh_bh_gateway = "10.84.165.254"
_gnb_global_bts_id = 76170
_gnb_du_common_unit_hardware_type = "ASIA"
_lmp_ip = "192.168.255.129"

_snmp_user = {
    "userName": "admin",
    "authKey": "password",
    "privKey": "password",
    "authProtocol": "MD5",
    "privProtocol": "DES",
}

_gnb_pdu1 = FPFH(
    port_numbers=[5],
    addr="10.255.10.75",
    login="admin",
    password="admin",
)

_hub_hpe = HPE(
    port_numbers=[2],
    addr="zd16.mgt.ska-lab.nsn-rdnet.net",
    snmp_user=_snmp_user,
)
##############################################################
_gnb_oam_backhaul_ip = NetworkAddress(
    v4="{}/23".format(_gnb_bh_ip),
    routing_v4=RoutingInformation(gateway=_gbh_bh_gateway),
    vlan_id=504,
)
_default_ssh_lmp_connection = SshServiceDetails(
    addr=_lmp_ip, username="toor4nsn", password="oZPS0POrRieRtu"
)
_default_oam_http_connection = HttpConnectionDetails(
    addr=_gnb_bh_ip, username="Nemuadmin", password="nemuuser", port=443
)
##############################################################
####             RU     SECTION               ####
_ru_hw_group = "APHA"
_ru_1_gnb = RU(
    radio_type="APHA",
    ru_hw_group=_ru_hw_group,
    serial_number="NH223400107",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.9.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_hub_hpe.pdu_ports[2],
)

_radio_units_gnb = [_ru_1_gnb]
##############################################################
####                      SMOD & BBMOD                           ###
_cu_gnb = CU(
    oam_ssh_connection_details=_default_ssh_lmp_connection,  # replace if other than default
    oam_http_connection_details=_default_oam_http_connection,
    backhaul_site_oam_ip=_gnb_oam_backhaul_ip,
    x2c=NetworkAddress(v4=_gnb_bh_ip, vlan_id=504),
    x2u=NetworkAddress(v4=_gnb_bh_ip, vlan_id=504),
    s1u=NetworkAddress(v4=_gnb_bh_ip, vlan_id=504),
)  # replace if other than default

_bbmod_L = CapacityUnit(addr="192.168.253.20", hardware_type="ABIA", rus=_radio_units_gnb)
_capacity_units = [_bbmod_L]
_du_lmp_connection_gnb = _default_ssh_lmp_connection
_du_lmp_connection_gnb.proxy = _test_pc_gnb_default_ssh_connection_details
_du_common_unit_gnb = CommonUnit(
    lmp_connection=_du_lmp_connection_gnb,
    pdu_port=_gnb_pdu1.pdu_ports[5],
    hardware_type=_gnb_du_common_unit_hardware_type,
    capacity_units=_capacity_units,
)
_airscale_gnb = Airscale(common_units=[_du_common_unit_gnb])
_du_gnb = DU(airscale=_airscale_gnb, rus=_radio_units_gnb)
_gnb_main = ClassicalBts(
    cu=_cu_gnb,
    dus=[_du_gnb],
    instance_id=_gnb_global_bts_id,
    global_bts_id=_gnb_global_bts_id,
)
########################################################################################
#####                               Test PCs                          #####
_test_pc_gnb_main = TestPc(
    default_ssh_connection_details=_test_pc_gnb_default_ssh_connection_details,
    connections=[_du_common_unit_gnb],
)

tl = TestLine(
    test_pc=_test_pc_gnb_main,
    gnbs=[_gnb_main],
    pdus=[_gnb_pdu1, _hub_hpe],
    test_pcs=[_test_pc_gnb_main],
)
__all__ = ["tl"]
