import os
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.core import RealCore
from taf.config.testline import RU, DU
from taf.config.testline.pdu import FACOM
from taf.config.testline.testline import TestLine
from taf.config.testline.ue import Android
from taf.config.testline.gnb import CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline import RealEnb
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)
from taf.config.testline.attenuator import AttenuationPort, TopYoung
from taf.config.testline import NetworkAddress, RoutingInformation

__maintainer__ = "Zhou Qiang"  # TL owner name
__team__ = "I_MN_SRAN_PROD_HZH_SISO_2_VRF_GMS <I_MN_SRAN_PROD_HZH_SISO_2_VRF@internal.nsn.com>"  # TL owner's team
__email__ = "qiang.1.zhou@nokia-sbell.com"  # TL owner's email

# common
__all__ = ["tl"]

# = os.path.dirname(os.path.abspath(__file__))
_real_enb_pdu = FACOM(addr="10.69.66.100", port_numbers=[5])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.68.94.102", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[5],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=None)


# 5GRU for classicalBTS
_ru_pdu = FACOM(addr="10.56.7.146", port_numbers=[2, 3, 7])

_ru_0 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.52", username="root", password="root"
    ),
    pdu_port=_ru_pdu.pdu_ports[7],
    radio_type=RadioTypes.UHFA.value,
    signal_analyzer=None,
    attenuation_ports=[],
    serial_number="LBALLU-YD17440NX1D",
)

_ru_1 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.52", username="root", password="root"
    ),
    pdu_port=_ru_pdu.pdu_ports[2],
    radio_type=RadioTypes.UHFA.value,
    signal_analyzer=None,
    attenuation_ports=[],
    serial_number="LBALLU-YD17440NX1D",
)

_ru_2 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.52", username="root", password="root"
    ),
    pdu_port=_ru_pdu.pdu_ports[3],
    radio_type=RadioTypes.UHFA.value,
    signal_analyzer=None,
    attenuation_ports=[],
    serial_number="LBALLU-YD17100HH4Q",
)


# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(addr="192.168.253.20")
_gnb_pdu = FACOM(addr="10.69.66.100", port_numbers=[4])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[4],
)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(airscale=_airscale, rus=[_ru_2], f1_m_ip_addr="10.68.94.103")

# CU
_cu = CU(
    backhaul_site_oam_ip="10.68.94.103",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.68.94.103", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.68.94.103", username="Nemuadmin", password="nemuuser"
    ),
)


# cloud_topology
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ASIK_ABILB1_UHFA"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=6165, global_bts_id=6165)

# test pc
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.68.94.121", username="ute", password="ute"
    )
)
_test_pc_enb = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.68.94.120", username="ute", password="ute"
    ),
    connections=[_lte_real_enb],
)

# switch Dtor
_dell_s4048on_ssh = SshServiceDetails(
    addr="0.0.0.0", port="1", username="5gran", password="nokia123"
)  # EIF1 Port
_dell_s4048on_switch = DellS4048ONSwitch(_dell_s4048on_ssh)

# switch Mtor
_dell_s4048ton_ssh = SshServiceDetails(
    addr="0.0.0.0", port="1", username="5gran", password="nokia123"
)
_dell_s4048ton_switch = DellS4048TONSwitch(_dell_s4048ton_ssh)

_attenuator = TopYoung(ip_addr="x.x.x.x", port=23, attenuation_port_numbers=[7, 8])

tl = TestLine(
    test_pc=_test_pc,
    test_pcs=[_test_pc, _test_pc_enb],
    gnbs=[_classical_bts],
    enbs=[_lte_real_enb],
    core=RealCore(mcc=262, mnc=3),
    tl_cloud_topology=_tl_cloud_topology,
    attenuator=_attenuator,
    # switches=[_dell_s4048on_switch, _dell_s4048ton_switch]
)
