__maintainer__ = "Agnieszka Pacia"
__team__ = "I_SC_KRK_PROD_NITROGEN_GMS"
__email__ = "I_SC_KRK_PROD_NITROGEN@internal.nsn.com"
__owner_email__ = "agnieszka.pacia@nokia.com"

import os

from taf.config.testline import SshServiceDetails, HttpConnectionDetails
from taf.config.testline.testpc import TestPc
from taf.config.testline import RU, DU
from taf.config.testline.pdu import ATEN, PduPort
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import ClassicalBts, CU
from taf.config.testline.airscale import CommonUnit, CapacityUnit, Airscale


_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="SC5G-eNB-271.sc5g.krk-lab.nsn-rdnet.net", username="ute", password="ute"
    )
)


_ru_1 = RU(
    ru_hw_group="hw_group",
    radio_type="AHCA",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.148", username="root", password="umniedziala"
    ),
    lmp_connection=" ",
    pdu_port=PduPort(pdu=ATEN(addr="1.1.1.1", port_numbers=[1, 2]), port_no=1),
)

_ru_2 = RU(
    ru_hw_group="hw_group",
    radio_type="AHCA",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.149", username="root", password="umniedziala"
    ),
    lmp_connection=" ",
    pdu_port=PduPort(pdu=ATEN(addr="1.1.1.1", port_numbers=[1, 2]), port_no=1),
)

_ru_3 = RU(
    ru_hw_group="hw_group",
    radio_type="AHCA",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.150", username="root", password="umniedziala"
    ),
    lmp_connection=" ",
    pdu_port=PduPort(pdu=ATEN(addr="1.1.1.1", port_numbers=[1, 2]), port_no=1),
)

_cu = CU(
    backhaul_site_oam_ip="10.83.182.21",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.83.182.21", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.255.129", username="Nemuadmin", password="nemuuser"
    ),
)

_du_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_du_capacity_unit = CapacityUnit(
    addr="fsp2_c", hardware_type="ABIL", hardware_version="102"
)

_du_common_unit = CommonUnit(
    lmp_connection=_du_lmp_connection,
    capacity_units=[_du_capacity_unit],
    hardware_type="ASIK",
    hardware_version="101",
)

_airscale = Airscale(common_units=[_du_common_unit])

_du = DU(airscale=_airscale, rus=[_ru_1, _ru_2, _ru_3])

_bts = ClassicalBts(cu=_cu, dus=[_du])

tl = TestLine(test_pc=_test_pc, gnbs=[_bts], tl_cloud_topology="test")


__all__ = ["tl"]
