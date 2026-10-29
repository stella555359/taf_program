__maintainer__ = "Shi Longgan"
__team__ = "MG_5G_NJN_UUF_PET"
__email__ = "I_5GASIR_UUF_PET@internal.nsn.com"
__owner_email__ = "longgan.shi@nokia-sbell.com"

from taf.config.testline.testline import TestLine
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    SCRadioConnectionDetails,
    TelnetConnectionDetails,
)
from taf.config.testline.gnb import ClassicalBts, CU
from taf.config.testline import DU
from taf.config.testline import SC5GRadio
from taf.config.testline.core import EPCSim
from taf.config.testline.pdu import PduPort, ATEN

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.66.24.6", username="ute", password="Nokia666@ute!"
    )
)

_du_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_du_capacity_unit = CapacityUnit(
    addr="192.168.253.22", hardware_type="ABIO", hardware_version="A102"
)

_du_pdu = ATEN("1.1.1.1", [0])
_du_pdu_port = PduPort(_du_pdu, 0)

_du_common_unit = CommonUnit(
    lmp_connection=_du_lmp_connection,
    capacity_units=[_du_capacity_unit],
    hardware_type="ASIM",
    hardware_version="A102",
    pdu_port=_du_pdu_port,
)

# _ru_1 = SC5GRadio(
#     ru_hw_group="ASIR-HUB",
#     sc_radio_connection_details=SCRadioConnectionDetails(
#         ssh_connection_details=SshServiceDetails(
#             addr="192.168.255.129",
#             username="toor4nsn",
#             password="oZPS0POrRieRtu",
#             proxy=SshServiceDetails(addr="10.66.24.7", username="ute", password="ute"),
#         ),
#         telnet_connection_details=TelnetConnectionDetails(
#             addr="tty-server", username="toor4nsn", password="oZPS0POrRieRtu"
#         ),
#     ),
#     lmp_connection=SshServiceDetails(
#         addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
#     ),
#     pdu_port=PduPort(pdu=ATEN(addr="1.1.1.1", port_numbers=[1, 2]), port_no=1),
# )

# _ru_2 = SC5GRadio(
#     ru_hw_group="ASIR-HUB",
#     sc_radio_connection_details=SCRadioConnectionDetails(
#         ssh_connection_details=SshServiceDetails(
#             addr="192.168.255.129",
#             username="toor4nsn",
#             password="oZPS0POrRieRtu",
#             proxy=SshServiceDetails(
#                 addr="10.66.24.252", username="ute", password="ute"
#             ),
#         ),
#         telnet_connection_details=TelnetConnectionDetails(
#             addr="tty-server", username="toor4nsn", password="oZPS0POrRieRtu"
#         ),
#     ),
#     lmp_connection=SshServiceDetails(
#         addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
#     ),
#     pdu_port=PduPort(pdu=ATEN(addr="1.1.1.1", port_numbers=[1, 2]), port_no=1),
# )

# _ru_3 = SC5GRadio(
#     ru_hw_group="ASIR-HUB",
#     sc_radio_connection_details=SCRadioConnectionDetails(
#         ssh_connection_details=SshServiceDetails(
#             addr="192.168.255.129",
#             username="toor4nsn",
#             password="oZPS0POrRieRtu",
#             proxy=SshServiceDetails(addr="10.66.24.8", username="ute", password="ute"),
#         ),
#         telnet_connection_details=TelnetConnectionDetails(
#             addr="tty-server", username="toor4nsn", password="oZPS0POrRieRtu"
#         ),
#     ),
#     lmp_connection=SshServiceDetails(
#         addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
#     ),
#     pdu_port=PduPort(pdu=ATEN(addr="1.1.1.1", port_numbers=[1, 2]), port_no=1),
# )

# _ru_4 = SC5GRadio(
#     ru_hw_group="ASIR-HUB",
#     sc_radio_connection_details=SCRadioConnectionDetails(
#         ssh_connection_details=SshServiceDetails(
#             addr="192.168.255.129",
#             username="toor4nsn",
#             password="oZPS0POrRieRtu",
#             proxy=SshServiceDetails(
#                 addr="10.66.24.249", username="ute", password="ute"
#             ),
#         ),
#         telnet_connection_details=TelnetConnectionDetails(
#             addr="tty-server", username="toor4nsn", password="oZPS0POrRieRtu"
#         ),
#     ),
#     lmp_connection=SshServiceDetails(
#         addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
#     ),
#     pdu_port=PduPort(pdu=ATEN(addr="1.1.1.1", port_numbers=[1, 2]), port_no=1),
# )

_cu = CU(
    backhaul_site_oam_ip="192.168.255.129",
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.255.129", username="Nemuadmin", password="nemuuser"
    ),
)

_airscale = Airscale([_du_common_unit])

# _du = DU(airscale=_airscale, rus=[_ru_1, _ru_2, _ru_3, _ru_4])
_du = DU(airscale=_airscale)

_cbts = ClassicalBts(cu=_cu, dus=[_du], instance_id=11316, global_bts_id=11316)

_core_pc_ssh = SshServiceDetails(addr="10.66.31.192", username="ute", password="ute")
_core_pc = TestPc(default_ssh_connection_details=_core_pc_ssh)
_core = EPCSim(
    mme_ip="172.31.1.1",
    mcc=460,
    mnc=6,
    tac=1,
    default_ssh_connection_details=_core_pc_ssh,
    dir_path="/home/wts",
    cfg_filename="epcsim.cfg",
    edaemon_port=60002,
    egate_port=60001,
)

tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_ASIR_ASIBA102L_ABILA102B1_ABILA102B2_ABILA102B3_UUF",
    core=_core,
)

__all__ = ["tl"]
