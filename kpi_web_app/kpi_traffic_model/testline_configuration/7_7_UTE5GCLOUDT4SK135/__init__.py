__maintainer__ = "I_MN_5GSC_KRK_AUTO"
__team__ = "I_MN_5GSC_KRK_AUTO"
__email__ = "I_MN_5GSC_KRK_AUTO@internal.nsn.com"

import os
import yaml
from copy import copy
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc, Connection
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
)
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline import NetworkAddress, RU, RoutingInformation
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit, CoreUnit
from taf.config.testline.pdu import PduPort, FPFH, HPE
from taf.config.testline.attenuator import RadioRack


# The most commonly used testline configuration. #
def _set_abstract_lib_config_env(ue_config_file):
    tl_config_dir = os.path.dirname(os.path.abspath(__file__))

    ue_config_abs_path = os.path.join(tl_config_dir, ue_config_file)

    with open(ue_config_abs_path) as ta_ue_config:
        ue_config = yaml.safe_load(ta_ue_config)
    os.environ["ABSTRACT_LIB_CONFIG"] = ue_config_abs_path

    return ue_config


_test_pc_gnb1 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT4SK135-1.p04.ska-lab.nsn-rdnet.net",
        username="ute",
        password="uteUTE!",
    )
)

_test_pc_gnb2 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT4SK135-2.p04.ska-lab.nsn-rdnet.net",
        username="ute",
        password="uteUTE!",
    )
)

_lmp_ip = "192.168.255.129"

_snmp_user = {
    "userName": "admin",
    "authKey": "password",
    "privKey": "password",
    "authProtocol": "MD5",
    "privProtocol": "DES",
}


####################################################
#                    GNB1
####################################################
_default_gnb1_ssh_lmp_connection_gnb = SshServiceDetails(
    addr=_lmp_ip,
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_gnb1.default_ssh_connection_details,
)
_gnb1_bh_ip = "10.84.190.135"
_gnb1_oam_ip = _gnb1_bh_ip
_gnb1_oam_backhaul_ip = NetworkAddress(
    v4="{}/23".format(_gnb1_bh_ip),
    routing_v4=RoutingInformation(gateway="10.84.191.254"),
    vlan_id=504,
)

_default_oam_http_connection_gnb1 = HttpConnectionDetails(
    addr=_gnb1_oam_ip, username="Nemuadmin", password="nemuuser", port=443
)


_gnb1_u_plane_ip = NetworkAddress(v4="10.84.190.135", vlan_id=504)
_gnb1_c_plane_ip = NetworkAddress(v4="10.84.190.135", vlan_id=504)
_gnb1_s1_plane_ip = NetworkAddress(v4="10.84.190.135", vlan_id=504)
_gnb1_instance_id = 77135
_gnb1_global_bts_id = 77135
_gnb1_du_common_unit_hardware_type = "ASOE"
_gnb1_ru_1_ip = NetworkAddress(v4="")
_gnb1_ru_2_ip = NetworkAddress(v4="")

_pdu1_gnb1 = FPFH(
    port_numbers=[5],
    addr="fpfh-zf03-40-p04.p04-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

_pdu2_gnb1 = HPE(
    port_numbers=[11, 19], addr="zf03.mgt.ska-lab.nsn-rdnet.net", snmp_user=_snmp_user
)

##############################################################
_ru_1_gnb1 = RU(
    radio_type="APHA",
    ru_hw_group="APHA",
    serial_number="NH193300287",
    default_ssh_connection_details=SshServiceDetails(
        addr=_gnb1_ru_1_ip.v4, username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=PduPort(pdu=_pdu2_gnb1, port_no=19),
)
_ru_2_gnb1 = RU(
    radio_type="APHG",
    ru_hw_group="APHG",
    serial_number="NH225300370",
    default_ssh_connection_details=SshServiceDetails(
        addr=_gnb1_ru_2_ip.v4, username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=PduPort(pdu=_pdu2_gnb1, port_no=11),
)

_cu_gnb1 = CU(
    oam_ssh_connection_details=_default_gnb1_ssh_lmp_connection_gnb,
    oam_http_connection_details=_default_oam_http_connection_gnb1,
    backhaul_site_oam_ip=_gnb1_oam_backhaul_ip,
    x2c=_gnb1_c_plane_ip,
    x2u=_gnb1_u_plane_ip,
    s1u=_gnb1_s1_plane_ip,
)

_asoe_gnb1 = CoreUnit(
    lmp_connection=copy(_default_gnb1_ssh_lmp_connection_gnb),
    hardware_type="ASOE",
    rus=[_ru_1_gnb1, _ru_2_gnb1],
    pdu_port=_pdu1_gnb1.pdu_ports[5],
    test_pc=_test_pc_gnb1.default_ssh_connection_details,
)

_airscale_gnb1 = Airscale(core_units=[_asoe_gnb1])
_du_gnb1 = DU(
    airscale=_airscale_gnb1,
    oam_ip=_gnb1_oam_backhaul_ip,
    instance_id=_gnb1_instance_id,
    global_bts_id=_gnb1_global_bts_id,
)
_gnb1_main = ClassicalBts(
    cu=_cu_gnb1,
    dus=[_du_gnb1],
    instance_id=_gnb1_instance_id,
    global_bts_id=_gnb1_global_bts_id,
)

####################################################
#                    GNB2
####################################################
_default_gnb2_ssh_lmp_connection_gnb = SshServiceDetails(
    addr=_lmp_ip,
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_gnb2.default_ssh_connection_details,
)
_gnb2_bh_ip = "10.84.190.88"
_gnb2_oam_ip = _gnb2_bh_ip
_gnb2_oam_backhaul_ip = NetworkAddress(
    v4="{}/23".format(_gnb2_bh_ip),
    routing_v4=RoutingInformation(gateway="10.84.191.254"),
    vlan_id=504,
)

_default_oam_http_connection_gnb2 = HttpConnectionDetails(
    addr=_gnb2_oam_ip, username="Nemuadmin", password="nemuuser", port=443
)

_gnb2_u_plane_ip = NetworkAddress(v4="10.84.190.88", vlan_id=504)
_gnb2_c_plane_ip = NetworkAddress(v4="10.84.190.99", vlan_id=504)
_gnb2_s1_plane_ip = NetworkAddress(v4="10.84.190.88", vlan_id=504)
_gnb2_instance_id = 77088
_gnb2_global_bts_id = 77088
_gnb2_ru_1_ip = NetworkAddress(v4="")
_gnb2_ru_2_ip = NetworkAddress(v4="")

_pdu1_gnb2 = FPFH(
    port_numbers=[6],
    addr="fpfh-zf03-48-p04.p04-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)
_pdu2_gnb2 = HPE(
    port_numbers=[9, 10, 18, 20],
    addr="zf03.mgt.ska-lab.nsn-rdnet.net",
    snmp_user=_snmp_user,
)

##############################################################
_ru_1_gnb2 = RU(
    radio_type="APHA",
    ru_hw_group="APHA",
    serial_number="NH193900623",
    default_ssh_connection_details=SshServiceDetails(
        addr=_gnb2_ru_1_ip.v4, username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=PduPort(pdu=_pdu2_gnb2, port_no=20),
)
_ru_2_gnb2 = RU(
    radio_type="APHG",
    ru_hw_group="APHG",
    serial_number="NH225300345",
    default_ssh_connection_details=SshServiceDetails(
        addr=_gnb2_ru_2_ip.v4, username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=PduPort(pdu=_pdu2_gnb2, port_no=18),
)

_cu_gnb2 = CU(
    oam_ssh_connection_details=_default_gnb2_ssh_lmp_connection_gnb,
    oam_http_connection_details=_default_oam_http_connection_gnb2,
    backhaul_site_oam_ip=_gnb2_oam_backhaul_ip,
    x2c=_gnb2_c_plane_ip,
    x2u=_gnb2_u_plane_ip,
    s1u=_gnb2_s1_plane_ip,
)

_abio_gnb2 = CapacityUnit(
    addr="192.168.253.20", hardware_type="ABIO", rus=[_ru_1_gnb2, _ru_2_gnb2]
)
_lmp_connection_gnb2 = copy(_default_gnb2_ssh_lmp_connection_gnb)
_lmp_connection_gnb2.proxy = _test_pc_gnb2.default_ssh_connection_details
_common_unit_gnb2 = CommonUnit(
    lmp_connection=_lmp_connection_gnb2,
    pdu_port=_pdu1_gnb2.pdu_ports[6],
    hardware_type="ASIB",
    capacity_units=[_abio_gnb2],
)

_airscale_gnb2 = Airscale(common_units=[_common_unit_gnb2])
_du_gnb2 = DU(
    airscale=_airscale_gnb2,
    oam_ip=_gnb2_oam_backhaul_ip,
    instance_id=_gnb2_instance_id,
    global_bts_id=_gnb2_global_bts_id,
)
_gnb2 = ClassicalBts(
    cu=_cu_gnb2,
    dus=[_du_gnb2],
    instance_id=_gnb2_instance_id,
    global_bts_id=_gnb2_global_bts_id,
)


##############################################################
#                     Attenuators
##############################################################
_attenuator1 = RadioRack(
    ip_addr="10.255.13.93", port=50000, attenuation_port_numbers=[1, 2, 3, 4, 5, 6]
)

# Test PCs
_test_pc_gnb1.connections = [
    Connection(
        device=_gnb1_main.dus[0].airscale.core_units[0],
        interface="eth1",
        interface_type="lmp",
    )
]
_test_pc_gnb2.connections = [
    Connection(
        device=_gnb2.dus[0].airscale.common_units[0],
        interface="eth1",
        interface_type="lmp",
    )
]

_ue_config = _set_abstract_lib_config_env("ue_config.yaml")
# Testline
tl = TestLine(
    gnbs=[_gnb1_main, _gnb2],
    test_pc=_test_pc_gnb1,
    test_pcs=[_test_pc_gnb1, _test_pc_gnb2],
    pdus=[_pdu1_gnb1, _pdu2_gnb1, _pdu1_gnb2, _pdu2_gnb2],
    attenuators=[_attenuator1],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_ASIBL_ABIOB1_ASOE_ASIR_2xAPHA_2XAPHG_2xAHFIH_4xAWHGEQH_AWHHC",
)
__all__ = ["tl"]
