__maintainer__ = "Arkadiusz Sobejko"
__team__ = "MN RAN RD VRF KRK 2"
__email__ = "OO_MN_RAN_RD_VRF_KRK_2_53115523_GMS <OO_MN_RAN_RD_VRF_KRK_2_53115523@internal.nsn.com>"
__owner_email__ = "arkadiusz.sobejko@nokia.com"

import os
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc, Connection
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
)
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline import NetworkAddress
from taf.config.testline.pdu import FPFH
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline import Airphone

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

_cu = CU(
    backhaul_site_oam_ip="10.0.1.2",
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.255.129", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(v4="10.0.1.2", vlan_id=1604),
    x2u=NetworkAddress(v4="10.0.1.2", vlan_id=1604),
    s1u=NetworkAddress(v4="10.0.1.2", vlan_id=1604),
)

_pdu1 = FPFH(
    port_numbers=[2],
    addr="fpfh-hc01-34-p02.p02-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

_pdu2 = FPFH(
    port_numbers=[1],
    addr="fpfh-hc01-34-p02.p02-leg.ska-lab.nsn-rdnet.net",
    login="admin",
    password="admin",
)

_abio1_du1 = CapacityUnit(addr="192.168.253.36", hardware_type="ABIO")
_abio1_du2 = CapacityUnit(addr="192.168.253.40", hardware_type="ABIO")
_asib_du1 = CommonUnit(
    pdu_port=_pdu1.pdu_ports[2],
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    hardware_type="ASIB",
    capacity_units=[_abio1_du1, _abio1_du2],
)

_du1 = DU(airscale=Airscale(common_units=[_asib_du1]))
_cbts = ClassicalBts(cu=_cu, dus=[_du1])

_ue = Airphone(
    egate=SshServiceDetails("", ""),
    l2_ssh_connection_details=SshServiceDetails("", ""),
    l3_ssh_connection_details=SshServiceDetails("", ""),
    l1=Airscale(
        common_units=[
            CommonUnit(
                lmp_connection=SshServiceDetails(
                    "192.168.200.1", "toor4nsn", password="oZPS0POrRieRtu"
                ),
                hardware_type="ASIL",
                capacity_units=[
                    CapacityUnit(addr="192.168.253.84", hardware_type="ABIO"),
                    CapacityUnit(addr="192.168.253.88", hardware_type="ABIO"),
                ],
                pdu_port=_pdu2.pdu_ports[1],
            )
        ]
    ),
)

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT2SK104-IWF.p02.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_cbts.dus[0].airscale.common_units[0],
            interface_type="lmp",
        ),
        _ue,
    ],
)

tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    tl_cloud_topology="CLOUD_5G_I_BOO_AP_LOO-IWF",
    pdus=[_pdu1, _pdu2],
    ues=[_ue],
)
__all__ = ["tl"]
