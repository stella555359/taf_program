__maintainer__ = "arunkumar.a@nokia.com"
__team__ = "MN_RAN_Pz_BLR_2_SG"
__email__ = "arunkumar.a@nokia.com"
__Owner_email__ = "arunkumar.a@nokia.com"

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
        addr="10.58.238.109", username="ute", password="ute"
    ),
    connections=[NetworkAddress(v4="192.168.255.129")],
)

_pdu_1 = RRB(
    addr="10.45.153.150", 
    port_numbers=[2, 6, 8]
)
_pdu_1.pdu_ports[2].contactor = "NORMALLY_OPENED"
_pdu_1.pdu_ports[6].contactor = "NORMALLY_OPENED"
_pdu_1.pdu_ports[8].contactor = "NORMALLY_OPENED"

_rmod_1 = RU(
    ru_hw_group="",
    radio_type=RadioTypes.AZHA.value,
    serial_number="EA204859627",
    pdu_port=_pdu_1.pdu_ports[8],
)

_rmod_2 = RU(
    ru_hw_group="",
    radio_type=RadioTypes.AZQI.value,
    serial_number="1M212323107",
    pdu_port=_pdu_1.pdu_ports[6],
)

_abio = CapacityUnit(
    addr="", 
    hardware_type="ABIO",
    hardware_version="A.101",
    serial_number="L1204505956",
    rus=[_rmod_1],
)
_abin = CapacityUnit(
    addr="",
    hardware_type="ABIN",
    hardware_version="A.102",  
    serial_number="L1204214666",
    rus=[_rmod_2],
)
_asib = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_abio, _abin],
    pdu_port=_pdu_1.pdu_ports[2],
    hardware_type="ASIB",
    hardware_version="A.102",
    serial_number="DH212871601",
    test_pc=_test_pc_master,
)
_dcap_1 = DcapRnD(
    HttpConnectionDetails(
        addr="10.41.209.120", port="443", username="dcapuser", password="dcapadmin!"
    )
)
_cu_asib = CU(
    backhaul_site_oam_ip=NetworkAddress("10.58.239.183"),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.58.239.183", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.58.239.183", username="Nemuadmin", password="nemuuser"
    ),
)
a = Airscale([_asib])
_du_asib = DU(airscale=a, rus=[_rmod_1, _rmod_2])
_classicalBts = ClassicalBts(
    cu=_cu_asib,
    dus=[_du_asib],
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
    tl_cloud_topology="CLOUD_5G_CLASSICAL_1ASIB_1ABIO_1ABIN_1AZHA",
)  
UTE_UE_CONFIG = "/home/ute/testline_configuration/7_2_UTE5GCLOUD1008/ta_ue_config.yaml"

__all__ = ["tl"]


