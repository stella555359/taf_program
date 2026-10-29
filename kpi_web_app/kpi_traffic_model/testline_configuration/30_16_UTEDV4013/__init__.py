__maintainer__ = "Marek Jozwik"
__team__ = "DCM"
__email__ = "marek.jozwik@nokia.com"


from taf.config.testline.testline import TestLine
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
)
from taf.config.testline.gnb import ClassicalBts, CU
from taf.config.testline import DU, RU
from taf.config.testline.core import RealCore5G
from taf.config.testline.pdu import ATEN, Gude, EPC
from taf.config.testline.ue import TafUeAt, TafUeAndroid, Android
from taf.config.testline.connection_details import SshServiceDetails, IperfDataTransferDetails
from taf.config.testline.appserver import TafUeAppServer
from taf.config.testline.taf_ue_data_transfer_protocol import TafUeDataTransferProtocol
from taf.config.testline.pdn import PDNTafUeAndroidDetails
from taf.config.testline.attenuator import JFW


__all__ = ["tl"]

_cu_gnb_1 = CU(
    backhaul_site_oam_ip="192.168.255.1",
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.255.129", username="Nemuadmin", password="nemuuser", port=443
    )
)

_pdu_gnb = Gude(addr="10.44.200.89", port_numbers=[7], model="EPC", version="8220-1")
_pdu_hdbde = Gude(addr="10.44.200.90", port_numbers=[3], model="EPC", version="8220-1")
_pdu_frgh = Gude(addr="10.44.200.99", port_numbers=[5], model="EPC", version="8220-1")
_pdu_ompa = Gude(addr="10.44.200.99", port_numbers=[2], model="EPC", version="8220-1")
_pdu_omqa = Gude(addr="10.44.200.99", port_numbers=[7], model="EPC", version="8220-1")

_abip_gnb = CapacityUnit(
    addr="192.168.253.22",
    hardware_type="ABIP",
    hardware_version="A101",
    serial_number="L1231901147",
)

_asim_gnb = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_abip_gnb],
    hardware_type="ASIM",
    hardware_version="A101",
    serial_number="L1224309168",
    pdu_port=_pdu_gnb.pdu_ports[7],
)

_gnb_ru_1 = RU(
    ru_hw_group="FRGH",
    radio_type="472822A.101",
    serial_number="HFR2313M098.51",
    attenuation_ports=[],
    pdu_port="1.1.1.1",
)

_gnb_ru_2 = RU(
    ru_hw_group="OMPA",
    radio_type="476984A.X15",
    serial_number="UM254500002",
    default_ssh_connection_details=SshServiceDetails(
        addr="", username="rfsw", password="f6gh0K2nXq0O8XqVFkUuMtJnzuKm0U3box0QcYgugn0="
    ),
    attenuation_ports=[],
    pdu_port=_pdu_ompa.pdu_ports[2]
)

_gnb_ru_3 = RU(
    ru_hw_group="OMQA",
    radio_type="G37RRH-46-01B-31",
    serial_number="MR192590001",
    default_ssh_connection_details=SshServiceDetails(
        addr="", username="rfsw", password="f6gh0K2nXq0O8XqVFkUuMtJnzuKm0U3box0QcYgugn0="
    ),
    attenuation_ports=[],
    pdu_port=_pdu_omqa.pdu_ports[7]
)


_lmp_vm_gnb_1 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.42.75.224", username="ute", password="ute"
    ),
    connections=[_asim_gnb],
)

_airscale_gnb_1 = Airscale([_asim_gnb])

_du_1_gnb_1 = DU(airscale=_airscale_gnb_1, rus=[_gnb_ru_1,_gnb_ru_2,_gnb_ru_3])

_cbts = ClassicalBts(
    cu=_cu_gnb_1, dus=[_du_1_gnb_1], global_bts_id=1, instance_id=1
)


tl = TestLine(
    test_pc=_lmp_vm_gnb_1,
    test_pcs=[_lmp_vm_gnb_1],
    gnbs=[_cbts],
    tl_cloud_topology="CLOUD_DCM_ASIML_ABIPB1_FRGH_HDBDE_OMPA_OMQA",
    pdus=[_pdu_gnb,_pdu_hdbde,_pdu_frgh,_pdu_ompa,_pdu_omqa],
)

class HDBDE:
    hostname = "192.168.129.3"
    username = "toor4nsn"
    password = "oZPS0POrRieRtu"

class KVM:
    hostname = "10.42.75.113"
