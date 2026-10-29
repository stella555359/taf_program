import os
from taf.config.testline.testline import TestLine
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.config.testline import Airphone
from taf.config.testline.pdu import TopYoung, FACOM, HBTE


__maintainer__ = "Yuan Hongyan"  # TL owner name
__team__ = "I_NSB_MN_5GSC_5G_PZ_HZ_01_GMS"  # TL owner's team
__email__ = "Hongyan.1.yuan@nokia-sbell.com"  # TL owner

## common
__all__ = ["tl"]

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.149.55", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_pdu_bts = HBTE(addr="10.57.247.207", port_numbers=[8])

_capacity_unit = CapacityUnit(addr="192.168.253.20")

_common_unit = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_capacity_unit],
    pdu_port=_pdu_bts.pdu_ports[8],
)

_airscale = Airscale(common_units=[_common_unit])

_cu = CU(
    backhaul_site_oam_ip="192.168.255.129",
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.147.179", username="Nemuadmin", password="nemuuser", port=443
    ),
    x2c=NetworkAddress(v4="10.0.1.1", vlan_id=810),
    x2u=NetworkAddress(v4="10.0.1.1", vlan_id=810),
    s1u=NetworkAddress(v4="10.0.1.1", vlan_id=810),
)


_du = DU(airscale=_airscale)

_cbts = ClassicalBts(cu=_cu, dus=[_du])

_pdu_ap = HBTE(addr="10.57.247.206", port_numbers=[5])
_capacity_unit_ap = CapacityUnit(addr="192.168.253.84")
_common_unit_ap = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.200.1", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_capacity_unit_ap],
    pdu_port=_pdu_ap.pdu_ports[5],
)

_ue = Airphone(
    l3_ssh_connection_details=SshServiceDetails(addr="10.57.149.55", username="ute", password="iW_K#8.ute%A10h0m0ra"),
    l2_ssh_connection_details=SshServiceDetails("", ""),
    egate=SshServiceDetails("", ""),
    l1=Airscale(common_units=[_common_unit_ap]),
    edaemon_port=22222,
    egate_port=20000,
)


tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_AP",
    pdus=[_pdu_bts, _pdu_ap],
    ues=[_ue],
)

__all__ = ["tl"]
