__maintainer__ = "Pawel Zabawczuk"
__team__ = "RRM team"
__email__ = "pawel.k.zabawczuk@nokia.com"
__owner_email__ = "pawel.k.zabawczuk@nokia.com"

import os
from taf.config.testline.testline import TestLine
from taf.config.testline.ue import Android
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline import NetworkAddress, RoutingInformation
from taf.config.testline.gnb import ClassicalBts, CU
from taf.config.testline import DU, RU
from taf.config.testline.core import EPCSim
from taf.config.testline import RealEnb

from taf.config.testline.core import RealCore, RealCore5GDetails, AMF
from taf.config.testline.pdu import ATEN, EPC
from taf.config.testline.gnb.du import Cablink, Endpoint

__all__ = ["tl"]

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.28.0.42", username="ute", password="uteUTE!"
    )
)

_cfg_dir = os.path.dirname(os.path.abspath(__file__))
os.environ["ABSTRACT_LIB_CONFIG"] = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "ue_config.yaml"
)

_abio_master = CapacityUnit(addr="192.168.253.20")
_abio_lokia = CapacityUnit(addr="192.168.253.21")
_abio_lokib = CapacityUnit(addr="192.168.253.22")

_common_unit = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_abio_master, _abio_lokia, _abio_lokib],
    pdu_port=None,
)

_airscale = Airscale([_common_unit])

_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.14.48.61",
        v6=None,
        vlan_id="1000",
        routing=RoutingInformation(gateway="10.14.49.254", ip_prefix_length=23),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.255.129", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.28.25.145",
        vlan_id="4002",
        routing_v4=RoutingInformation(gateway="10.28.25.149", ip_prefix_length=29),
    ),
    x2u=NetworkAddress(
        v4="10.28.25.146",
        vlan_id="4002",
        routing_v4=RoutingInformation(gateway="10.28.25.149", ip_prefix_length=29),
    ),
    s1u=NetworkAddress(
        v4="10.28.25.146",
        vlan_id="4002",
        routing_v4=RoutingInformation(gateway="10.28.25.149", ip_prefix_length=29),
    ),
    ngc=NetworkAddress(
        v4="10.28.25.145",
        vlan_id="4002",
        routing_v4=RoutingInformation(gateway="10.28.25.149", ip_prefix_length=29),
    ),
    ngu=NetworkAddress(
        v4="10.28.25.146",
        vlan_id="4002",
        routing_v4=RoutingInformation(gateway="10.28.25.149", ip_prefix_length=29),
    ),
    xnc=NetworkAddress(
        v4="10.28.25.145",
        vlan_id="4002",
        routing_v4=RoutingInformation(gateway="10.28.25.149", ip_prefix_length=29),
    ),
    xnu=NetworkAddress(
        v4="10.28.25.146",
        vlan_id="4002",
        routing_v4=RoutingInformation(gateway="10.28.25.149", ip_prefix_length=29),
    ),
)


_ru1 = RU(
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(addr="", username=""),
    pdu_port=None,
    ru_hw_group="",
    radio_type="AHLOA",
)

_ru_cablinks = [
    Cablink(
        source=Endpoint(unit=_abio_lokia, label="SFP", port_id=1),
        target=Endpoint(unit=_ru1, label="SFP", port_id=1),
    )
]

_du = DU(_airscale, rus=[_ru1], cablinks=_ru_cablinks)

_amf_oam_ssh_connection_details = SshServiceDetails(
    addr=None, username=None, password=None
)

_n2_address = NetworkAddress(v4="10.94.232.6")

_amf = AMF(oam_ssh_connection_details=_amf_oam_ssh_connection_details, n2=_n2_address)


_real_5g_core_details = RealCore5GDetails(amf=_amf, tac=8101)

_core = RealCore(mcc=540, mnc=1, five_g=_real_5g_core_details)

_cbts = ClassicalBts(cu=_cu, dus=[_du], instance_id=61, global_bts_id=61)

_common_unit_lte_ssh = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_common_unit_lte = CommonUnit(
    _common_unit_lte_ssh, capacity_units=[_abio_lokib], pdu_port=None
)

_ue_pc_ssh = SshServiceDetails("10.0.96.101", "cv5g1_5", password="P@scal5G")

_android_ue = Android(
    ssh_connection_details=_ue_pc_ssh,
    serial_number="519f111b",
    server_dir="/cygdrive/c/UEManager/ue_manager_files/pyro_server",
    python_path="python2",
    qcat_path="/cygdrive/c/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="/cygdrive/c/UEManager/ue_manager_files/pyro_server/DIAG.cfg",
)

tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_SA_ASIB_ABIO_AHLOA",
    core=_core,
    pdus=None,
    ues=[_android_ue],
)
