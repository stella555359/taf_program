__maintainer__ = "Yang Di"
__team__ = "I_NSB_MN_RAN_RD_VRF_HAZ3_05_GMS"
__email__ = "I_NSB_MN_RAN_RD_VRF_HAZ3_05@internal.nsn.com"
__email__ = "di.yang@nokia-sbell.com"

import os
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import (
    HttpConnectionDetails,
    SshServiceDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline import NetworkAddress
from taf.config.testline.pdu import HBTE, PduPort
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline import Airphone
from taf.config.testline.attenuator import HBTE as AHBTE
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)
from taf.config.testline.appserver import AppServer
from taf.config.testline import DU, RU, RealEnb, NetworkAddress, RoutingInformation
from taf.config.testline.core import RealCore5G
from taf.config.testline.ue import Android

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

_test_pc1 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.159.11",
        username="ute",
        password="iW_K#8.ute%A10h0m0ra",
    )
)

# pdu setting is adapted because local tl gnb1/gnb2/ap may be connected to different PDUs
_pdu_gnb1 = HBTE(
    port_numbers=[8],
    addr="10.71.195.74",
)

_pdu_ap1 = HBTE(
    port_numbers=[7],
    addr="10.71.195.74",
)

_pdus = [_pdu_gnb1, _pdu_ap1]

_cu1 = CU(
    backhaul_site_oam_ip="192.168.255.129",
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.255.129", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(v4="10.0.1.2", vlan_id=2387),
    x2u=NetworkAddress(v4="10.0.1.2", vlan_id=2387),
    s1u=NetworkAddress(v4="10.0.1.2", vlan_id=2387),
    ngu=NetworkAddress(v4="10.0.1.2", vlan_id=2387),
)

_abio_du1 = CapacityUnit(addr="fsp-5a")
_abio_slave = CapacityUnit(addr="fsp-5b")
_abio_loner = CapacityUnit(addr="fsp-5c")

_asib_du1 = CommonUnit(
    pdu_port=_pdus[0].pdu_ports[8],
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_abio_du1, _abio_slave, _abio_loner],
)

_du1 = DU(airscale=Airscale(common_units=[_asib_du1]), f1_m_ip_addr="10.71.208.209")

_cbts1 = ClassicalBts(cu=_cu1, dus=[_du1], global_bts_id=11543, instance_id=1922)

_ue1 = Airphone(
    SshServiceDetails("", ""),
    SshServiceDetails("", ""),
    SshServiceDetails("", ""),
    Airscale(
        [
            CommonUnit(
                pdu_port=_pdus[1].pdu_ports[7],
                lmp_connection=SshServiceDetails(
                    addr="192.168.200.1", username="toor4nsn", password="oZPS0POrRieRtu"
                ),
                capacity_units=[CapacityUnit(addr="192.168.253.84")],
            )
        ]
    ),
)

_core = RealCore5G(mcc=262, mnc=3)

tl = TestLine(
    test_pc=_test_pc1,
    gnbs=[_cbts1],
    tl_cloud_topology="BO_LOO",
    ues=[_ue1],
    pdus=_pdus,
    core=_core,
)

__all__ = ["tl"]


