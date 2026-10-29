import os
import yaml
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.gnb.du import DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, ATEN, RRB, APC, Gude, HBTE
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import (
    AirphoneCloud,
    Airphone,
    Prisma,
    TM500,
    Qualcomm,
    QualcommUeType,
    Android,
)  # added in taf.meta.5.4
from taf.config.testline.enb import (
    Enb,
    SimEnb,
    RealEnb,
    LTEEmuEnb,
    PrismaEnb,
    DocomoEnb,
)

# added in taf.meta 5.4
from taf.config.testline.attenuator import AttenuationPort, TopYoung
from taf.config.testline.gnb.networkaddress import NetworkAddress  # add in taf.meta 5.4
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)
from taf.compatibility.configuration import TestlineWrapper

__maintainer__ = "Hu Jay"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_6_GMS <I_MN_5G_RAN_IV4_LINE_HZG_6@internal.nsn.com>"
)
__email__ = "jay.hu@nokia-sbell.com"

# common
__all__ = ["tl"]

# #host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.29", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# Iperf
_appserver_ssh = SshServiceDetails(
    addr="10.57.191.240", username="vrf4_sg6", password="Nokia@1234567", port="56075"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="9.6.6.6",
    iperf_path="/opt/app/iperf",
    port="56175",
)

# CI_Detail_UE_Type='Qualcomm;Qualcomm'
_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.31", username="tester", password="tester123"
    ),
    serial_number="aadd0d90",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "qct_dx50"],
)

# #RealEnb
_real_enb_pdu = HBTE(addr="10.57.172.16", port_numbers=[3])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.231.38", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[3],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=None)

# attenuator
_attenuator = TopYoung(
    ip_addr="10.57.243.53",
    port=3000,
    attenuation_port_numbers=[7, 8, 9, 10],
    model="TAS16T16-51-120-1SDES",
)

# #5GRU for classicalBTS
_ru_0_pdu = HBTE(addr="10.57.172.27", port_numbers=[6])

_ru_0 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.52", username="root", password="root"
    ),
    pdu_port=_ru_0_pdu.pdu_ports[6],
    radio_type=RadioTypes.AZQG,
    signal_analyzer=None,
    attenuation_ports=[],
    serial_number=None,
)

_ru_1_pdu = HBTE(addr="10.57.172.24", port_numbers=[2])

_ru_1 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.85", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.85", username="root", password="root"
    ),
    pdu_port=_ru_1_pdu.pdu_ports[2],
    radio_type=RadioTypes.AZQG,
    signal_analyzer=None,
    attenuation_ports=[],
    serial_number=None,
)

_ru_2_pdu = HBTE(addr="10.57.242.23", port_numbers=[1])

_ru_2 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.117", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.117", username="root", password="root"
    ),
    pdu_port=_ru_2_pdu.pdu_ports[1],
    radio_type=RadioTypes.AZQG.value,
    signal_analyzer=None,
    attenuation_ports=[],
    serial_number=None,
)

_ru_3_pdu = HBTE(addr="10.57.242.26", port_numbers=[1])

_ru_3 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.54", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.54", username="root", password="root"
    ),
    pdu_port=_ru_3_pdu.pdu_ports[1],
    radio_type=RadioTypes.AZQG.value,
    signal_analyzer=None,
    attenuation_ports=[],
    serial_number=None,
)

_ru_4_pdu = HBTE(addr="10.57.242.23", port_numbers=[2])

_ru_4 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.84", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.84", username="root", password="root"
    ),
    pdu_port=_ru_4_pdu.pdu_ports[2],
    radio_type=RadioTypes.AZQG.value,
    signal_analyzer=None,
    attenuation_ports=[],
    serial_number=None,
)

_ru_5_pdu = HBTE(addr="10.57.242.26", port_numbers=[4])

_ru_5 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.116", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.116", username="root", password="root"
    ),
    pdu_port=_ru_5_pdu.pdu_ports[4],
    radio_type=RadioTypes.AZQG.value,
    signal_analyzer=None,
    attenuation_ports=[],
    serial_number=None,
)

# #DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.57.223.71", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")

_gnb_pdu = HBTE(addr="10.57.172.16", port_numbers=[3])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[3],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru_0, _ru_1], f1_m_ip_addr="10.57.223.71")

# #CU
_f1m = NetworkAddress(v4="9.9.1.1", v6="xxxx", vlan_id=1)
_f1c = NetworkAddress(v4="9.9.1.2", v6="xxxx", vlan_id=2)
_f1u = NetworkAddress(v4="9.9.1.3", v6="xxxx", vlan_id=3)
_x2c = NetworkAddress(v4="9.9.2.1", v6="xxxx", vlan_id=1)
_x2u = NetworkAddress(v4="9.9.2.2", v6="xxxx", vlan_id=2)
_s1c = NetworkAddress(v4="9.9.3.1", v6="xxxx", vlan_id=1)
_s1u = NetworkAddress(v4="9.9.3.2", v6="xxxx", vlan_id=2)
_tracing = NetworkAddress(v4="9.9.1.2", v6="xxxx", vlan_id=1)

_cu = CU(
    backhaul_site_oam_ip="10.57.223.71",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.223.71", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.223.71", username="Nemuadmin", password="nemuuser"
    ),
    f1m=_f1m,
    f1c=_f1c,
    f1u=_f1u,
    x2c=_x2c,
    x2u=_x2u,
    s1c=_s1c,
    s1u=_s1u,
    tracing=_tracing,
)


# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=75, global_bts_id=1)

_tl_cloud_topology = "CLOUD_5G_BB3"

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    tl_cloud_topology=_tl_cloud_topology,
    enbs=[_lte_real_enb],
    ues=[_android],
    attenuator=_attenuator,
)
# old version keyword under robotws5g/resource compatibility workaround
# tl = TestlineWrapper(tl)
