__maintainer__ = "Yao Ying"
__team__ = "I_NJ_SC_SYSTEM_VERF_GMS"
__email__ = "I_NJ_SC_SYSTEM_VERF@internal.nsn.com"
__owner_email__ = "ying.yao@nokia-sbell.com"


import os
from taf.config.testline.testline import TestLine
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.core import LTEEmuCore
from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline.enb import LTEEmuEnb
from taf.config.testline.radio import RU
from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.config.testline import Airphone
from taf.config.testline.pdu import HBTE


_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.66.13.60", username="ute", password="uteUTE!"
    )
)

_pdu1 = HBTE(port_numbers=[1, 2], addr="10.66.13.157")

_capacity_unit = CapacityUnit(addr="192.168.253.36")

_common_unit = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129",
        username="toor4nsn",
        password="oZPS0POrRieRtu",
        proxy=_test_pc.default_ssh_connection_details,
    ),
    capacity_units=[_capacity_unit],
    pdu_port=_pdu1.pdu_ports[1],
)

_airscale = Airscale([_common_unit])

_cu = CU(
    backhaul_site_oam_ip="192.168.255.129",
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.255.129", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(v4="10.0.1.1", vlan_id=1133),
    x2u=NetworkAddress(v4="10.0.1.1", vlan_id=1133),
    s1u=NetworkAddress(v4="10.0.1.1", vlan_id=1133),
)

_ru1 = RU(
    ru_hw_group="cmw",
    radio_type="AEQE",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.200.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=None,
)

_ru2 = RU(
    ru_hw_group="cmw",
    radio_type="AEHC",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.200.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=None,
)

_ru3 = RU(
    ru_hw_group="cmw",
    radio_type="AHFIB",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.200.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=None,
)

_ru4 = RU(
    ru_hw_group="cmw",
    radio_type="AHLOA",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.200.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=None,
)

_du = DU(_airscale, rus=[_ru1, _ru2, _ru3, _ru4])

_cbts = ClassicalBts(cu=_cu, dus=[_du])

_X2_link_ip_v4 = NetworkAddress(v4="10.0.1.13")
_enb = LTEEmuEnb(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.66.13.60", username="ute", password="uteUTE!"
    ),
    dir_path="/opt/iphy/latest",
    cfg_filename="wts.cfg",
    global_bts_id=1,
    x2_link_addr=_X2_link_ip_v4,
)

_ue = Airphone(
    SshServiceDetails("", ""),
    SshServiceDetails("", ""),
    SshServiceDetails("", ""),
    Airscale(
        [
            CommonUnit(
                SshServiceDetails(
                    "192.168.200.129", "toor4nsn", password="oZPS0POrRieRtu"
                ),
                [CapacityUnit(addr="192.168.253.84")],
                pdu_port=_pdu1.pdu_ports[2],
            )
        ]
    ),
)

_ue.capabilities = None
_ue.ssh_connection_details = _test_pc.default_ssh_connection_details
_ue.iperf_details = IperfDataTransferDetails(
    ssh_connection_details=_test_pc.default_ssh_connection_details
)

tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    enbs=[_enb],
    tl_cloud_topology="CLOUD_5G_I_LO_AP_LO_SANSA_FS_ECPRI_CMWV_TDD",
    ues=[_ue],
)

__all__ = ["tl"]
