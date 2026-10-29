__maintainer__ = "Merwane CHEMSSI"
__team__ = "MN 5G&SC Pz 5G I&V 1 NPS 4 SG"
__email__ = "merwane.chemssi@nokia.com"
__owner_email__ = "merwane.chemssi@nokia.com"

import os

from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.gnb.du import RU, DU
from taf.config.testline.pdu import ATEN, FACOM, PduPort
from taf.config.testline.gnb.gnb import ClassicalBts, CU
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.testline import TestLine

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

_vm_ute = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.28.0.36", username="ute", password="ute"
    )
)

_du0_pdu = ATEN(addr="", port_numbers=[1])

_common_unit_0_pdu_port = PduPort(pdu=_du0_pdu, port_no=_du0_pdu.pdu_ports[1])

_du0_capacity_unit_L_0 = CapacityUnit(addr="192.168.253.20")

_common_unit_0_L = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_du0_capacity_unit_L_0],
    pdu_port=_common_unit_0_pdu_port,
)

_pdu1 = ATEN(addr="", port_numbers=[1])

ru_pdu = FACOM(addr="", port_numbers=[1])

_pdus = [_pdu1, ru_pdu]

_airscale = Airscale(common_units=[_common_unit_0_L])

_cu = CU(
    backhaul_site_oam_ip="10.14.49.206",
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.255.129", username="Nemuadmin", password="nemuuser"
    ),
)

_ru = RU(
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.34", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(addr="", username=""),
    pdu_port=None,
    ru_hw_group="",
    radio_type="AHLOA",
)

_du = DU(_airscale, rus=[_ru])

_cbts = ClassicalBts(dus=[_du], cu=_cu)

_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ASIBR_ABILB4_AHLOA"

tl = TestLine(
    test_pc=_vm_ute, gnbs=[_cbts], tl_cloud_topology=_tl_cloud_topology, pdus=_pdus
)

__all__ = ["tl"]
