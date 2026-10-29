__maintainer__ = "Pawel Wroblewski"
__team__ = "5G_PZ_MMW_KRK_3_SG"
__email__ = "pawel.wroblewski@nokia.com"

import os

from taf.config.testline import RU, RealEnb, NetworkAddress, RoutingInformation
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
)
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline.pdu import FPFH
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.attenuator import TopYoung


_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT438.sc5g.krk-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    ),
)

_pdu = FPFH(
    port_numbers=[1, 5],
    addr="fpfh-gd15-48-sc5g.sc5g-leg.krk-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

_ru = RU(
    ru_hw_group="hw_group",
    radio_type="AHEB",
    pdu_port=_pdu.pdu_ports[5],
    serial_number="EA192276336",
)

_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.83.183.188/23"
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.83.183.188", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.83.183.188", username="Nemuadmin", password="nemuuser"
    ),
)

_abio = CapacityUnit(addr="192.168.253.20", hardware_type="ABIO")

_asib = CommonUnit(
    pdu_port=_pdu.pdu_ports[1],
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu",
        proxy=SshServiceDetails(
            addr="7-7-UTE5GCLOUDT438.sc5g.krk-lab.nsn-rdnet.net",
            username="ute",
            password="ute",
        ),
    ),
    capacity_units=[_abio],
    hardware_type="ASIB",
)

_airscale = Airscale(common_units=[_asib])

_du = DU(airscale=_airscale, rus=[_ru])

_cbts = ClassicalBts(cu=_cu, dus=[_du], global_bts_id=75438, instance_id=75438)

_attenuator = TopYoung(
    ip_addr="raspberrypi438.sc5g.krk-lab.nsn-rdnet.net", port=["1-1.1", "1-1.4"], attenuation_port_numbers=[1]
)


_lss = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.2.138", username="coam", password="zO&n1W*ktp7"
    ),
    connections=[
        NetworkAddress(v4="172.16.2.138", v6="2a00:8a02:60:1c::1:100"),
        NetworkAddress(v4="10.83.179.99", v6="2a00:8a02:60:3a:250:56ff:fe95:7eb2"),
    ],
)

_test_pc_enb_default_ssh_connection_details = SshServiceDetails(
    addr="sc5g-enb-008.sc5g.krk-lab.nsn-rdnet.net",
    username="ute",
    password="ute",
)

_test_pc_enb = TestPc(
    default_ssh_connection_details=_test_pc_enb_default_ssh_connection_details
)

tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    test_pcs=[_lss, _test_pc_enb],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_ATT_ASIBR_ABIOB4_AHEB_ENB",
    attenuators=_attenuator,
)

__all__ = ["tl"]
