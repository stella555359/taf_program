__maintainer__ = "Anil Pachauri"
__team__ = "MN RAN L3 AP 3 BLR 2 SG"
__email__ = "I_MN_5G_AIRPHONE_QT_BLR@internal.nsn.com"
__owner_email__ = "anil.1.pachauri@nokia.com"
import os
from taf.config.testline.airscale import Airscale, CapacityUnit, CommonUnit
from taf.config.testline.connection_details import (
    HttpConnectionDetails,
    SshServiceDetails,
)
from taf.config.testline.enb import RealEnb
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.config.testline.pdu import ATEN
from taf.config.testline.pdu import RRB
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc, Connection
from taf.config.testline.ue import Airphone, IPHY, CUS


_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

_pdu = RRB(addr="10.45.131.44", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_pdus = [_pdu]

_airscale_gnb = Airscale(
    common_units=[
        CommonUnit(
            lmp_connection=SshServiceDetails(
                addr="192.168.255.119", username="toor4nsn", password="oZPS0POrRieRtu"
            ),
            capacity_units=[CapacityUnit(addr="192.168.253.20", hardware_type="ABIO"),],
            pdu_port=_pdus[0].pdu_ports[8],
            hardware_type="ASIL",
        )
    ]
)

_du = DU(_airscale_gnb)

_cu = CU(
    backhaul_site_oam_ip="192.168.255.129",
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.255.129", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(v4="10.0.1.2", vlan_id=202),
    x2u=NetworkAddress(v4="10.0.1.2", vlan_id=202),
    s1u=NetworkAddress(v4="10.0.1.2", vlan_id=202),
)

_gnb = ClassicalBts(cu=_cu, dus=[_du], instance_id=7200010181)

_airscale_enb = Airscale(
    common_units=[
        CommonUnit(
            lmp_connection=SshServiceDetails(
                addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
            ),
            capacity_units=[CapacityUnit(addr="192.168.253.20", hardware_type="ABIA")],
            pdu_port=_pdus[0].pdu_ports[6],
            hardware_type="ASIL"
        )
    ]
)

_enb = RealEnb(system_module=_airscale_enb)

_airscale_ap = Airscale(
    common_units=[
        CommonUnit(
            lmp_connection=SshServiceDetails(
                addr="192.168.200.1", username="toor4nsn", password="oZPS0POrRieRtu"
            ),
            capacity_units=[CapacityUnit(addr="192.168.253.84", hardware_type="ABIO"),],
            pdu_port=_pdus[0].pdu_ports[7],
            hardware_type="ASIL",
        )
    ]
)

_ap = Airphone(
    egate=None,
    l3_ssh_connection_details=None,
    l2_ssh_connection_details=None,
    l1=_airscale_ap,
)

_airscale_cus = Airscale(
    common_units=[
        CommonUnit(
            lmp_connection=SshServiceDetails(
                addr="192.168.200.1", username="toor4nsn", password="oZPS0POrRieRtu"
            ),
            capacity_units=[CapacityUnit(addr="192.168.253.84", hardware_type="ABIA"),],
            pdu_port=_pdus[0].pdu_ports[5],
            hardware_type="ASIB",
        )
    ]
)

_cus = CUS(
    l1=_airscale_cus,
)

_test_pc1 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.63.68.8", username="ute", password="ute",
    ),
    connections=[Connection(interface="eth1", device=_gnb.dus[0].airscale.common_units[0], interface_type="lmp"), _ap],
)

_test_pc2 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.63.68.9", username="ute", password="ute",
    ),
    connections=[Connection(interface="eth1", device=_enb.system_module.common_units[0], interface_type="lmp"), _cus],
)

tl = TestLine(
    test_pc=_test_pc1,
    test_pcs=[_test_pc1, _test_pc2],
    gnbs=[_gnb],
    enbs=[_enb],
    tl_cloud_topology="CLOUD_5G_I_LO_AP_LO-4G_I_LA_CUS_BA",
    ues=[_ap, _cus],
    pdus=_pdus,
)

__all__ = ["tl"]
