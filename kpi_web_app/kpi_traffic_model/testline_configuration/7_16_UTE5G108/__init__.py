__maintainer__ = "Katarzyna Meinhardt"
__team__ = "I_MN_RAN_RD_VRF_WRO3_4"
__email__ = "I_MN_RAN_RD_VRF_WRO3_4@internal.nsn.com"
__owner_email__ = "katarzyna.meinhardt@nokia.com"
__customer__ = "RJIO"

import os
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
)

from taf.config.testline.airscale import Airscale, CapacityUnit, CommonUnit
from taf.config.testline.connection_details import SshServiceDetails, TelnetConnectionDetails, HttpConnectionDetails
from taf.config.testline.enb import RealEnb
from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.config.testline.pdu import ATEN, EPC, Gude
from taf.config.testline.radio import RU, RadioTypes
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import Connection, TestPc
from taf.config.testline.dcap import DcapBasic
from taf.config.testline import RoutingInformation
from taf.config.testline.gnb import ClassicalBts, CU, DU                                   
from taf.config.testline.gnb.du import Cablink, Endpoint
from taf.config.testline.core import RealCore, RealCore5GDetails, AMF
from taf.config.testline.lmi import SerialOverTcp, Remote

                                                     
cfg_dir = os.path.dirname(os.path.abspath(__file__))

_cu_gnb = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.42.84.23",
        v6="2a00:8a00:6000:600c::1b04",
        vlan_id=517,
        routing_v4=RoutingInformation(gateway="10.42.84.1/24"),
        routing_v6=RoutingInformation(gateway="2a00:8a00:6000:600c::1b01/120"),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.255.129", port=443, username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.42.85.26",
        v6="2a00:8a00:6000:600c::1c04",
        vlan_id=518,
        routing_v4=RoutingInformation(gateway="10.42.85.1/26"),
        routing_v6=RoutingInformation(gateway="2a00:8a00:6000:600c::1c01/120"),
    ),
    x2u=NetworkAddress(
        v4="10.42.85.90",
        v6="2a00:8a00:6000:600c::1d04",
        vlan_id=519,
        routing_v4=RoutingInformation(gateway="10.42.85.65/26"),
        routing_v6=RoutingInformation(gateway="2a00:8a00:6000:600c::1d01/120"),
    ),
    s1u=NetworkAddress(
        v4="10.42.85.153",
        v6="2a00:8a00:6000:600c::1e04",
        vlan_id=520,
        routing_v4=RoutingInformation(gateway="10.42.85.129/26"),
        routing_v6=RoutingInformation(gateway="2a00:8a00:6000:600c::1e01/120 "),
    ),
    ngu=NetworkAddress(
        v4="10.42.85.153",
        v6="2a00:8a00:6000:600c::1e04",
        vlan_id=520,
        routing_v4=RoutingInformation(gateway="10.42.85.129/26"),
        routing_v6=RoutingInformation(gateway="2a00:8a00:6000:600c::1e01/120 "),
    ),
    ngc=NetworkAddress(
        v4="10.42.86.23",
        v6="2a00:8a00:6000:600c::2004",
        vlan_id=522,
        routing_v4=RoutingInformation(gateway="10.42.86.1/26"),
        routing_v6=RoutingInformation(gateway="2a00:8a00:6000:600c::2001/120"),
    ),
    xnc=NetworkAddress(
        v4="10.42.85.26",
        v6="2a00:8a00:6000:600c::1c04",
        vlan_id=518,
        routing_v4=RoutingInformation(gateway="10.42.85.1/26"),
        routing_v6=RoutingInformation(gateway="2a00:8a00:6000:600c::1c01/120"),
    ),
    xnu=NetworkAddress(
        v4="10.42.85.90",
        v6="2a00:8a00:6000:600c::1d04",
        vlan_id=519,
        routing_v4=RoutingInformation(gateway="10.42.85.65/26"),
        routing_v6=RoutingInformation(gateway="2a00:8a00:6000:600c::1d01/120"),
    ),
)

_pdu_sm = Gude(addr="10.44.206.53", port_numbers=[11], model="EPC", version="8221-1")
_pdu_ru1 = Gude(addr="10.44.206.85", port_numbers=[6], model="EPC", version="8221-1")
_pdu_ru2 = Gude(addr="10.44.206.85", port_numbers=[10], model="EPC", version="8221-1")
_pdu_ru3 = Gude(addr="10.44.206.85", port_numbers=[7], model="EPC", version="8221-1")
_pdu_ru4 = Gude(addr="10.44.206.85", port_numbers=[9], model="EPC", version="8221-1")
_pdu_ru5 = Gude(addr="10.44.206.85", port_numbers=[12], model="EPC", version="8221-1")

_rmod_1 = RU(
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2", username="root", password="a2%FgSz3$fHmdusap354xujw7"
    ),
    ru_hw_group="cMAAr6.2_32T32R",
    radio_type="AVQA",
    serial_number="K9232709363",
    product_code="476383A.108",
    pdu_port=_pdu_ru1.pdu_ports[6],
)

_rmod_2 = RU(
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.18", username="root", password="a2%FgSz3$fHmdusap354xujw7"
    ),
    ru_hw_group="cMAAr6.2_32T32R",
    radio_type="AVQA",
    serial_number="K9233825574",
    product_code="476383A.108",
    pdu_port=_pdu_ru2.pdu_ports[10],
)

_rmod_3 = RU(
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.10", username="root", password="a2%FgSz3$fHmdusap354xujw7"
    ),
    ru_hw_group="cMAAr6.2_32T32R",
    radio_type="AVQA",
    serial_number="K9231866854",
    product_code="476383A.108",
    pdu_port=_pdu_ru3.pdu_ports[7],
)

_rmod_4 = RU(
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.33.129", username="root", password="a2%FgSz3$fHmdusap354xujw7"
    ),
    ru_hw_group="FRMr5.1_1_4T4R",
    radio_type="AHPB",
    serial_number="EA232250641",
    product_code="474119A.101",
    pdu_port=_pdu_ru4.pdu_ports[9],
    lmi=SerialOverTcp(
        uart_mapping=[
            Remote(addr="10.255.32.135", port=5001),
        ]
    ),

)

_rmod_5 = RU(
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.33.128", username="root", password="a2%FgSz3$fHmdusap354xujw7"
    ),
    ru_hw_group="FRMr5.1_1_2T4R",
    radio_type="AHPJ",
    serial_number="K9232737237",
    product_code="476403A.101",
    pdu_port=_pdu_ru5.pdu_ports[12],
    lmi=SerialOverTcp(
        uart_mapping=[
            Remote(addr="10.255.32.134", port=5001),
        ]
    ),

)

_fct_1 = CommonUnit(
    SshServiceDetails(addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"),
    capacity_units=[],
    pdu_port=_pdu_sm.pdu_ports[11],
    hardware_type="ASOE",
    hardware_version="475587A.102",
    serial_number="EA213353928",
    rus=[_rmod_1, _rmod_2, _rmod_3, _rmod_4, _rmod_5],
)

_smod_1 = Airscale([_fct_1])

_enb_sbts_1 = RealEnb(
    system_module=_smod_1,
    rms=[_rmod_1, _rmod_2, _rmod_3, _rmod_4, _rmod_5],
    instance_id=50202,
    oam_ip=NetworkAddress(
       v4="10.42.84.23",
       v6="2a00:8a00:6000:600c::1b04",
       vlan_id=517,
       routing_v4=RoutingInformation(gateway="10.42.84.1", ip_prefix_length=24),
       routing_v6=RoutingInformation(
         gateway="2a00:8a00:6000:600c::1b01/120", ip_prefix_length=120
      ),
  )
)

_du_1_gnb_1 = DU(airscale=_smod_1, rus=[_rmod_1, _rmod_2, _rmod_3, _rmod_4, _rmod_5])

_dcap = DcapBasic(
    connection_details=HttpConnectionDetails(
        "127.0.0.1", port=9443, username="dcapuser", password="dcapadmin!"
    )
)

_cbts = ClassicalBts(
    cu=_cu_gnb, dus=[_du_1_gnb_1], global_bts_id=50202, instance_id=50202, dcap=_dcap
)


_test_pc_1 = TestPc(
    SshServiceDetails(
        addr="10.44.178.78", username="ute", password="uteUTE!"
    ),
    connections=[
        NetworkAddress(v4="192.168.255.129"),
        Connection(interface="eth1", device=_enb_sbts_1.system_module.common_units[0], interface_type="lmp")
    ],
)

_pdus = [_pdu_sm, _pdu_ru1, _pdu_ru2, _pdu_ru3, _pdu_ru4, _pdu_ru5]

tl = TestLine(
    test_pc=_test_pc_1,
    test_pcs=[_test_pc_1],
    enbs=[_enb_sbts_1],
    gnbs=[_cbts],
    tl_cloud_topology="CLOUD_SRAN_TL108_RJIO-1",
    pdus=_pdus,
)

__all__ = ["tl"]
