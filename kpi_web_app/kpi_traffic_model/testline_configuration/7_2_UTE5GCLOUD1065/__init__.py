__maintainer__ = "suraj.singh@nokia.com"
__team__ = "MN_RAN_Pz_BLR_2_SG"
__email__ = "suraj.singh@nokia.com"
__Owner_email__ = "suraj.singh@nokia.com"

from taf.config.testline.airscale import CapacityUnit, CommonUnit, Airscale
from taf.config.testline.pdu import Gude, FACOM, PduPort, Pdu, HBTE, RRB
from taf.config.testline.radio import RU, RadioTypes
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc, Connection
from taf.config.testline.gnb import DU
from taf.config.testline.gnb.gnb import ClassicalBts, CU
from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.config.testline.dcap import DcapRnD
from taf.config.testline.connection_details import (
    SshServiceDetails,
    TelnetConnectionDetails,
    HttpConnectionDetails,
)

_test_pc_master = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.58.238.166", username="ute", password="ute"
    ),
    connections=[NetworkAddress(v4="192.168.255.129")],
)

_pdu_1 = RRB(addr="10.45.153.155", port_numbers=[2, 4, 5])
_pdu_1.pdu_ports[2].contactor = "NORMALLY_OPENED"
_pdu_1.pdu_ports[4].contactor = "NORMALLY_OPENED"
_pdu_1.pdu_ports[5].contactor = "NORMALLY_OPENED"

_pdu_2 = RRB(addr="10.58.242.155", port_numbers=[1, 2, 3])
_pdu_2.pdu_ports[1].contactor = "NORMALLY_OPENED"
_pdu_2.pdu_ports[2].contactor = "NORMALLY_OPENED"
_pdu_2.pdu_ports[3].contactor = "NORMALLY_OPENED"

_rmod_1 = RU(
    ru_hw_group="",
    radio_type=RadioTypes.AQQJ.value,
    serial_number="K9232451495",
    pdu_port=_pdu_2.pdu_ports[2],
)

_rmod_2 = RU(
    ru_hw_group="",
    radio_type=RadioTypes.AQQJ.value,
    serial_number="NQ232691168",
    pdu_port=_pdu_2.pdu_ports[1],
)

_rmod_3 = RU(
    ru_hw_group="",
    radio_type=RadioTypes.AQQJ.value,
    serial_number="NQ232691167",
    pdu_port=_pdu_2.pdu_ports[3],
)

_rmod_4 = RU(
    ru_hw_group="",
    radio_type=RadioTypes.AHPB.value,
    serial_number="DH242419247",
    pdu_port=_pdu_1.pdu_ports[5],
)

_rmod_5 = RU(
    ru_hw_group="",
    radio_type=RadioTypes.AHPJ.value,
    serial_number="K9232924274",
    pdu_port=_pdu_1.pdu_ports[4],
)

_abip = CapacityUnit(
    addr="",
    hardware_type="ABIP",
    hardware_version="A.102",
    serial_number="L1240903933",
    rus=[_rmod_1],
)
_abip = CapacityUnit(
    addr="",
    hardware_type="ABIP",
    hardware_version="A.102",
    serial_number="L1234501013",
    rus=[_rmod_2],
)
_asim = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_abip, _abip],
    pdu_port=_pdu_1.pdu_ports[2],
    hardware_type="ASIM",
    hardware_version="A.104",
    serial_number="L1234204979",
    test_pc=_test_pc_master,
)
_dcap_1 = DcapRnD(
    HttpConnectionDetails(
        addr="10.41.209.120", port="443", username="dcapuser", password="dcapadmin!"
    )
)
_cu_asim = CU(
    backhaul_site_oam_ip=NetworkAddress("10.58.239.161"),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.58.239.161", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.58.239.161", username="Nemuadmin", password="nemuuser"
    ),
)
a = Airscale([_asim])
_du_asim = DU(airscale=a, rus=[_rmod_1, _rmod_2, _rmod_3, _rmod_4, _rmod_5])
_classicalBts = ClassicalBts(
    cu=_cu_asim,
    dus=[_du_asim],
    instance_id=43126,
)
_test_pc_master.connections.append(
    Connection(
        interface="eth1",
        device=_classicalBts.dus[0].airscale.common_units[0],
        interface_type="lmp",
    )
)
tl = TestLine(
    test_pc=_test_pc_master,
    test_pcs=[_test_pc_master],
    gnbs=[_classicalBts],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_1ASIM_2ABIP_3AQQJ_1AHPB_1AHPJ",
)
UTE_UE_CONFIG = "/home/ute/testline_configuration/7_2_UTE5GCLOUD1065/ta_ue_config.yaml"

__all__ = ["tl"]
