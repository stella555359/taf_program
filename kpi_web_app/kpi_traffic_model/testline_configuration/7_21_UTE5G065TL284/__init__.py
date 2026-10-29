__maintainer__ = "Guo Shuxian"
__team__ = "MG_5G_NJN_UUF_PET"
__email__ = "I_5GASIR_UUF_PET@internal.nsn.com"
__owner_email__ = "shuxian.guo@nokia-sbell.com"

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
from taf.config.testline import DU, RealEnb, NetworkAddress
from taf.config.testline import SC5GRadio
from taf.config.testline.core import EPCSim
from taf.config.testline.pdu import PduPort, ATEN

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.66.31.241", username="ute", password="ute"
    )
)

_du_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_du_capacity_unit = CapacityUnit(
    addr="192.168.253.22", hardware_type="ABIO", hardware_version="A103"
)

_du_pdu = ATEN("1.1.1.1", [0])
_du_pdu_port = PduPort(_du_pdu, 0)

_du_common_unit = CommonUnit(
    lmp_connection=_du_lmp_connection,
    capacity_units=[_du_capacity_unit],
    hardware_type="ASIB",
    hardware_version="A102",
)

_ru_1 = SC5GRadio(
    ru_hw_group="ASIR-HUB",
    sc_radio_connection_details=SCRadioConnectionDetails(
        ssh_connection_details=SshServiceDetails(
            addr="192.168.255.129",
            username="toor4nsn",
            password="oZPS0POrRieRtu",
            proxy=SshServiceDetails(
                addr="10.66.31.244", username="ute", password="ute"
            ),
        ),
        telnet_connection_details=TelnetConnectionDetails(
            addr="tty-server", username="toor4nsn", password="oZPS0POrRieRtu"
        ),
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=PduPort(pdu=ATEN(addr="1.1.1.1", port_numbers=[1, 2]), port_no=1),
)

_cu = CU(
    backhaul_site_oam_ip="172.30.1.11",
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.66.30.161", username="Nemuadmin", password="nemuuser"
    ),
)

_airscale = Airscale([_du_common_unit])

_du = DU(
    airscale=_airscale,
    rus=[_ru_1],
)

_gnb = ClassicalBts(cu=_cu, dus=[_du], instance_id=284, global_bts_id=284)

_lte_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=SshServiceDetails(addr="10.66.31.242", username="ute", password="ute"),
)

_lte_capacity_unit = CapacityUnit(
    addr="fsp1_c", hardware_type="ABIA", hardware_version="A104"
)

_lte_common_unit = CommonUnit(
    lmp_connection=_lte_lmp_connection,
    capacity_units=[_lte_capacity_unit],
    hardware_type="ASIA",
    hardware_version="A203",
)

_airscale_enb = Airscale(common_units=[_lte_common_unit])

_enb = RealEnb(system_module=_airscale_enb, oam_ip=NetworkAddress(v4="10.66.30.162"))

_core_pc_ssh = SshServiceDetails(addr="10.66.31.243", username="ute", password="ute")
_core_pc = TestPc(default_ssh_connection_details=_core_pc_ssh)
_core = EPCSim(
    mme_ip="172.31.1.1",
    mcc="460",
    mnc="2",
    tac=1,
    default_ssh_connection_details=_core_pc_ssh,
    dir_path="/home/epc",
    cfg_filename="sim_wmp.cfg",
    edaemon_port=60002,
    egate_port=60001,
)

tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_gnb],
    enbs=[_enb],
    ues=None,
    core=_core,
    tl_cloud_topology="CLOUD_5G_CLASSICAL_ASIR_ASILA101L_ABILA102B1_PERF",
)

__all__ = ["tl"]
