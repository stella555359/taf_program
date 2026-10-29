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
from taf.config.testline import RU, RUExtension
from taf.config.testline.enb import RealEnb
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.pdu import FPFH, HPE
from taf.config.testline.gnb.networkaddress import NetworkAddress, RoutingInformation
from taf.config.testline.gnb.du import Cablink, Endpoint


def _set_abstract_lib_config_env(ue_config_file):
    tl_config_dir = os.path.dirname(os.path.abspath(__file__))

    ue_config_abs_path = os.path.join(tl_config_dir, ue_config_file)

    with open(ue_config_abs_path) as ta_ue_config:
        ue_config = yaml.safe_load(ta_ue_config)
    os.environ["ABSTRACT_LIB_CONFIG"] = ue_config_abs_path

    return ue_config


###############################################

# UTE Krakow 5G Classical BTS NSA configuration #

###############################################

# LMP virtual machine
_test_pc_gnb_main = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT1SK067-1.p01.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

# Power breakers
_pdu_gnb = FPFH(addr="1.1.1.1", login="admin", password="admin", port_numbers=[1])
_snmp_user = {
    "userName": "administrator",
    "authKey": "password",
    "privKey": "password",
    "authProtocol": "MD5",
    "privProtocol": "DES",
}
_pdu_gnb_ru = HPE(addr="1.1.1.1", port_numbers=[1], snmp_user=_snmp_user)
_pdu_enb = FPFH(addr="1.1.1.1", login="admin", password="admin", port_numbers=[1])
_pdu_enb_ru = FPFH(addr="1.1.1.1", login="admin", password="admin", port_numbers=[1])

# 5G Radio units

# No password needed when ssh to RMOD

_ru = RU(
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.48.2", username="root", password="asmr"
    ),
    ru_hw_group="ASMR",
    radio_type="AWEUA",
    pdu_port=_pdu_gnb_ru.pdu_ports[1],
    ru_extensions=[
        RUExtension(radio_type="FA3UA", serial_number="to_do", product_code="to_do"),
    ],
)

_radio_units_gnb = [_ru]

# 5G Cloud unit
_cloud_unit_gnb = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.84.164.67/23",
        vlan_id=504,
        routing_v4=RoutingInformation(gateway="10.84.164.254"),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.255.129", username="Nemuadmin", password="nemuuser", port=443
    ),
    x2c=NetworkAddress(
        v4="10.84.150.67/23",
        vlan_id=507,
        routing_v4=RoutingInformation(gateway="10.84.151.254"),
    ),
    x2u=NetworkAddress(
        v4="10.255.6.67/23",
        vlan_id=505,
        routing_v4=RoutingInformation(gateway="10.255.7.254"),
    ),
    s1u=NetworkAddress(
        v4="10.255.8.67/23",
        vlan_id=506,
        routing_v4=RoutingInformation(gateway="10.255.9.254"),
    ),
)

# 5G Distributed unit
"""
192.168.253.20 fsp-2-5a fsp1 fsp1_a
192.168.253.21 fsp-2-5b  fsp1_b
192.168.253.22 fsp-2-5c  fsp1_c
"""

_abio_master = CapacityUnit(addr="192.168.253.20")
_abio_slave = CapacityUnit(addr="192.168.253.21")
_abio_loner = CapacityUnit(addr="192.168.253.22")

_capacity_units_gnb = [_abio_master, _abio_slave, _abio_loner]

_common_unit_gnb = CommonUnit(
    hardware_type="ASIB",
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129",
        username="toor4nsn",
        password="oZPS0POrRieRtu",
        proxy=_test_pc_gnb_main.default_ssh_connection_details,
    ),
    capacity_units=_capacity_units_gnb,
    pdu_port=_pdu_gnb.pdu_ports[1],
)

_airscale_gnb = Airscale(common_units=[_common_unit_gnb])

_ru_cablinks = [
    Cablink(
        source=Endpoint(unit=_abio_master, label="SFP", port_id=1),
        target=Endpoint(unit=_ru, label="SFP", port_id=1),
    ),
    Cablink(
        source=Endpoint(unit=_abio_master, label="SFP", port_id=2),
        target=Endpoint(unit=_ru, label="SFP", port_id=2),
    ),
]

_distributed_unit_gnb = DU(
    airscale=_airscale_gnb, rus=_radio_units_gnb, cablinks=_ru_cablinks
)

# 5G Classical BTS

_classical_bts_gnb_main = ClassicalBts(
    cu=_cloud_unit_gnb,
    dus=[_distributed_unit_gnb],
    instance_id=76067,
    global_bts_id=76067,
)

# 4G radio units

_radio_units_enb = [
    RU(ru_hw_group="LTE_RADIO", radio_type="AHFIB", pdu_port=_pdu_enb_ru.pdu_ports[1])
]

# 4G anchor BTS

_capacity_units_enb = [CapacityUnit(addr="192.168.253.20", hardware_type="ABIA")]

_common_unit_enb = CommonUnit(
    hardware_type="ASIA",
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129",
        username="toor4nsn",
        password="oZPS0POrRieRtu",
        proxy=SshServiceDetails(
            addr="7-7-UTE5GCLOUDT1SK067-2.p01.ska-lab.nsn-rdnet.net",
            username="ute",
            password="ute",
        ),
    ),
    capacity_units=_capacity_units_enb,
    pdu_port=_pdu_enb.pdu_ports[1],
)

_airscale_enb = Airscale(common_units=[_common_unit_enb])

_lte_enb = RealEnb(
    system_module=_airscale_enb,
    rms=_radio_units_enb,
    instance_id=76066,
    global_bts_id=76066,
    oam_ip=NetworkAddress(
        v4="10.84.164.66/23",
        routing_v4=RoutingInformation(gateway="10.84.164.254"),
    ),
    x2_link_addr=NetworkAddress(v4="10.84.150.67"),
)

# enb test VM

_test_pc_enb = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT1SK067-2.p01.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    ),
    connections=[_lte_enb],
)

# Testline

_ue_config = _set_abstract_lib_config_env("ue_config.yaml")

tl = TestLine(
    test_pc=_test_pc_gnb_main,
    test_pcs=[_test_pc_gnb_main, _test_pc_enb],
    gnbs=[_classical_bts_gnb_main],
    enbs=[_lte_enb],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_2xANDROID_ASIBL_ABIOB1_AWEUA_FA3UA",
)

__all__ = ["tl"]
