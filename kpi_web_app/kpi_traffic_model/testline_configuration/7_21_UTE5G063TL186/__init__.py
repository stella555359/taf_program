__maintainer__ = "I_NJ_SC_SYSTEM_VERF@internal.nsn.com"
__team__ = "Nanjing ET"
__email__ = "I_NJ_SC_SYSTEM_VERF@internal.nsn.com"

from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc, Connection
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    SCRadioConnectionDetails,
    TelnetConnectionDetails,
)
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline import SC5GRadio, RU
from taf.config.testline.pdu import PduPort, HBTE
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.gnb.networkaddress import NetworkAddress


_master_cu = CU(
    backhaul_site_oam_ip="172.31.1.41",
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="172.31.1.41", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(v4="172.31.1.41", vlan_id=331),
    x2u=NetworkAddress(v4="172.31.1.41", vlan_id=331),
    s1c=NetworkAddress(v4="172.31.1.41", vlan_id=331),
    s1u=NetworkAddress(v4="172.31.1.41", vlan_id=331),
)

_slave1_cu = CU(
    backhaul_site_oam_ip="172.31.1.42",
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="172.31.1.42", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(v4="172.31.1.42", vlan_id=131),
    x2u=NetworkAddress(v4="172.31.1.42", vlan_id=131),
    s1c=NetworkAddress(v4="172.31.1.42", vlan_id=131),
    s1u=NetworkAddress(v4="172.31.1.42", vlan_id=131),
)

_slave2_cu = CU(
    backhaul_site_oam_ip="172.31.1.43",
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="172.31.1.43", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(v4="172.31.1.43", vlan_id=331),
    x2u=NetworkAddress(v4="172.31.1.43", vlan_id=331),
    s1c=NetworkAddress(v4="172.31.1.43", vlan_id=331),
    s1u=NetworkAddress(v4="172.31.1.43", vlan_id=331),
)

_master_du_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=SshServiceDetails(addr="10.66.16.56", username="ute", password="ute"),
)

_slave1_du_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=SshServiceDetails(addr="10.66.16.51", username="ute", password="ute"),
)

_slave2_du_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=SshServiceDetails(addr="10.66.16.53", username="ute", password="ute"),
)

_master_du_capacity_unit = CapacityUnit(
    addr="asc_0a", hardware_type="ASOE", hardware_version="A102"
)
_slave1_du_capacity_unit = CapacityUnit(
    addr="fct_0a", hardware_type="ASIB", hardware_version="A102"
)
_slave2_du_capacity_unit = CapacityUnit(
    addr="fct_4a", hardware_type="ASIB", hardware_version="A102"
)

_master_du_common_unit = CommonUnit(
    lmp_connection=_master_du_lmp_connection,
    capacity_units=[_master_du_capacity_unit],
    hardware_type="ASOE",
    hardware_version="A102",
    pdu_port=PduPort(
        pdu=HBTE(addr="10.66.47.16", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8]), port_no=6
    ),
)

_slave1_du_common_unit = CommonUnit(
    lmp_connection=_slave1_du_lmp_connection,
    capacity_units=[_slave1_du_capacity_unit],
    hardware_type="ASIB",
    hardware_version="A102",
    pdu_port=PduPort(
        pdu=HBTE(addr="10.66.47.16", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8]), port_no=5
    ),
)

_slave2_du_common_unit = CommonUnit(
    lmp_connection=_slave2_du_lmp_connection,
    capacity_units=[_slave2_du_capacity_unit],
    hardware_type="ASIB",
    hardware_version="A102",
    pdu_port=PduPort(
        pdu=HBTE(addr="10.66.47.16", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8]), port_no=5
    ),
)

_ru_1 = RU(
    ru_hw_group="ASIR-HUB",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129",
        username="toor4nsn",
        password="oZPS0POrRieRtu",
        proxy=SshServiceDetails(addr="10.66.16.76", username="ute", password="ute"),
    ),
    pdu_port=PduPort(
        pdu=HBTE(addr="", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8]), port_no=1
    ),
    radio_type="ASIR-HUB",
)

_ru_2 = RU(
    ru_hw_group="ASIR-HUB",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129",
        username="toor4nsn",
        password="oZPS0POrRieRtu",
        proxy=SshServiceDetails(addr="10.66.13.194", username="ute", password="ute"),
    ),
    pdu_port=PduPort(
        pdu=HBTE(addr="", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8]), port_no=1
    ),
    radio_type="ASIR-HUB",
)

_master_airscale = Airscale(common_units=[_master_du_common_unit])
_slave1_airscale = Airscale(common_units=[_slave1_du_common_unit])
_slave2_airscale = Airscale(common_units=[_slave2_du_common_unit])

_master_du = DU(airscale=_master_airscale, rus=[_ru_1, _ru_2])
_slave1_du = DU(airscale=_slave1_airscale, rus=[_ru_1, _ru_2])
_slave2_du = DU(airscale=_slave2_airscale, rus=[_ru_1, _ru_2])

_master_bts = ClassicalBts(
    cu=_master_cu, dus=[_master_du], instance_id=186, global_bts_id=186
)
_slave1_bts = ClassicalBts(
    cu=_slave1_cu, dus=[_slave1_du], instance_id=286, global_bts_id=286
)
_slave2_bts = ClassicalBts(
    cu=_slave2_cu, dus=[_slave2_du], instance_id=386, global_bts_id=386
)

_master_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.66.16.56", username="ute", password="ute"
    ),
    connections=[
        NetworkAddress(v4="192.168.255.126"),
        Connection(
            interface="eth1",
            interface_type="lmp",
            device=_master_bts.dus[0].airscale.common_units[0],
        ),
    ],
)

_slave1_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.66.16.51", username="ute", password="ute"
    ),
    connections=[
        NetworkAddress(v4="192.168.255.126"),
        Connection(
            interface="eth1",
            interface_type="lmp",
            device=_slave1_bts.dus[0].airscale.common_units[0],
        ),
    ],
)

_slave2_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.66.16.53", username="ute", password="ute"
    ),
    connections=[
        NetworkAddress(v4="192.168.255.126"),
        Connection(
            interface="eth1",
            interface_type="lmp",
            device=_slave2_bts.dus[0].airscale.common_units[0],
        ),
    ],
)

tl = TestLine(
    test_pc=_master_pc,
    test_pcs=[_slave1_pc, _slave2_pc],
    gnbs=[_master_bts, _slave1_bts, _slave2_bts],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_ASOE_1xAPHG_1xAPHA_2xAWHHIQB_2xAHFHIA_1xAHFIH",
)

__all__ = ["tl"]
