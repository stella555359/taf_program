__maintainer__ = "I_MN_5GSC_KRK_AUTO"
__team__ = "I_MN_5GSC_KRK_AUTO"
__email__ = "I_MN_5GSC_KRK_AUTO@internal.nsn.com"

import os
import yaml
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc, Connection
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
)
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline.radio import RU, RUExtension
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.pdu import HPE, FPFH
from taf.config.testline.gnb.networkaddress import NetworkAddress, RoutingInformation
from taf.config.testline.gnb.du import Cablink, Endpoint
from taf.config.testline.nms import NMS, NetAct


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
        addr="7-7-UTE5GCLOUDT4SK071.p04.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

# Power breakers
_pdu_enb = FPFH(
    addr="fpfh-zb08-46-p04.p04-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
    port_numbers=[1],
)

_pdu_enb_ru2 = FPFH(
    addr="fpfh-zb08-14-p04.p04-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
    port_numbers=[3],
)

_pdu_enb_ru3 = FPFH(
    addr="fpfh-zb08-14-p04.p04-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
    port_numbers=[2],
)

# 5G Cloud unit
_cloud_unit_gnb = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.84.190.71/23",
        vlan_id=504,
        routing_v4=RoutingInformation(gateway="10.84.191.254"),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.84.190.71", username="Nemuadmin", password="nemuuser", port=443
    ),
)

# 5G Radio units
# No password needed when ssh to RMOD
_enb_radio_unit_2 = RU(
    ru_hw_group="AHLOA",
    default_ssh_connection_details=SshServiceDetails(
        addr="", username="root", password="umniedziala"
    ),
    radio_type="AHLOA",
    serial_number="BL1930G11NE",
    product_code="474331A.101",
    pdu_port=_pdu_enb_ru2.pdu_ports[3],
)

_enb_radio_unit_3 = RU(
    ru_hw_group="AHFII",
    default_ssh_connection_details=SshServiceDetails(
        addr="", username="root", password="umniedziala"
    ),
    radio_type="AHFII",
    serial_number="BL2224N40AI",
    product_code="475656A.101",
    pdu_port=_pdu_enb_ru3.pdu_ports[2],
)


# 5G Distributed unit
"""
192.168.253.20 fsp-2-5a fsp1 fsp1_a
192.168.253.21 fsp-2-5b  fsp1_b
192.168.253.22 fsp-2-5c  fsp1_c
"""
_enb_capacity_unit_1 = CapacityUnit(
    addr="192.168.253.22",
    hardware_type="ABIN",
    hardware_version="A.102",
    serial_number="L1213805932",
    product_code="474824A.102",
    # slot_id=SlotId.B5
    rus=[],
)

_enb_capacity_unit_2 = CapacityUnit(
    addr="192.168.253.26",
    hardware_type="ABIA",
    hardware_version="A.103",
    serial_number="L1171818772",
    product_code="473096A.103",
    # slot_id=SlotId.B4
    rus=[_enb_radio_unit_2],
)

_enb_capacity_unit_3 = CapacityUnit(
    addr="192.168.253.27",  # need to check
    hardware_type="ABIO",
    hardware_version="A.101",
    serial_number="L1204304777",
    product_code="475266A.101",
    # slot_id=SlotId.B4
    rus=[_enb_radio_unit_3],
)

_capacity_units_gnb = [_enb_capacity_unit_1, _enb_capacity_unit_2, _enb_capacity_unit_3]


_common_unit_gnb = CommonUnit(
    hardware_type="ASIL",
    serial_number="L1232304190",
    pdu_port=_pdu_enb.pdu_ports[1],
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129",
        username="toor4nsn",
        password="oZPS0POrRieRtu",
        proxy=_test_pc_gnb_main.default_ssh_connection_details,
    ),
    capacity_units=_capacity_units_gnb,
)
_airscale_gnb = Airscale(common_units=[_common_unit_gnb])

_ru_cablinks = [
    Cablink(
        source=Endpoint(unit=_enb_capacity_unit_2, label="SFP", port_id=1),
        target=Endpoint(unit=_enb_radio_unit_2, label="SFP", port_id=1),
    ),
    Cablink(
        source=Endpoint(unit=_enb_capacity_unit_2, label="SFP", port_id=2),
        target=Endpoint(unit=_enb_radio_unit_2, label="SFP", port_id=2),
    ),
    Cablink(
        source=Endpoint(unit=_enb_capacity_unit_3, label="SFP", port_id=1),
        target=Endpoint(unit=_enb_radio_unit_3, label="SFP", port_id=1),
    ),
    Cablink(
        source=Endpoint(unit=_enb_capacity_unit_3, label="SFP", port_id=2),
        target=Endpoint(unit=_enb_radio_unit_3, label="SFP", port_id=2),
    ),
]

_distributed_unit_gnb = DU(
    airscale=_airscale_gnb, cablinks=_ru_cablinks
)

# 5G Classical BTS

_classical_bts_gnb_main = ClassicalBts(
    cu=_cloud_unit_gnb,
    dus=[_distributed_unit_gnb],
    instance_id=77071,
    global_bts_id=77071,
)
# NetAct

_cmwas_node = SshServiceDetails(
    addr="10.82.47.46",
    username="omc",
    password="Medsql!_1893",
    port=443,
)

_nms = NMS(
    netact=NetAct(
        ssh_connections_info=[_cmwas_node],
        https_main_info=HttpConnectionDetails(
            addr="srnclab2003lbwas.srnblr.nsn-rdnet.net",
            username="omc",
            password="Medsql!_1893",
            port=443,
        ),
    ),
)

_test_pc_gnb_main.connections = [
    Connection(
        device=_classical_bts_gnb_main.dus[0].airscale.common_units[0],
        interface="eth1",
        interface_type="lmp",
    )
]

# Testline

tl = TestLine(
    test_pc=_test_pc_gnb_main,
    test_pcs=[_test_pc_gnb_main],
    gnbs=[_classical_bts_gnb_main],
    nms=_nms,
    tl_cloud_topology="CLOUD_4G_CLASSICAL_ASIBL_ABIAB2_ABINB1_ABIOB3_AHFII_AHLOA_FHDI",
)

__all__ = ["tl"]
