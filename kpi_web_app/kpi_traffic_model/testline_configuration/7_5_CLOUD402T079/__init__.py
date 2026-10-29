import os
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.gnb.du import DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, ATEN, RRB, APC, Gude
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

__maintainer__ = "Jiao Chuanjiang"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_6_GMS <I_MN_5G_RAN_IV4_LINE_HZG_6@internal.nsn.com>"
)
__email__ = "jasper.jiao@nokia-sbell.com"


# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))
# #host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.22", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# Iperf
_appserver_ssh = SshServiceDetails(
    addr="10.57.252.107", username="root", password="APPpass"
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="9.6.6.6",
    iperf_path="/opt/app/iperf",
)

# Qualcomm
_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.232.38", username="5gran_SG6a", password="5Gran2019"
    ),
    serial_number="a5f05101",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE"],
)

# #RealEnb1
_real_enb_pdu1 = FACOM(addr="10.57.242.6", port_numbers=[6])

_common_unit_2_1 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.231.93", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu1.pdu_ports[6],
)

_real_enb1 = Airscale(common_units=[_common_unit_2_1])

_lte_real_enb1 = RealEnb(airscale=_real_enb1, rms=None)

# #RealEnb2
_real_enb_pdu2 = FACOM(addr="10.57.242.6", port_numbers=[4])

_common_unit_2_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.231.83", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu2.pdu_ports[4],
)

_real_enb2 = Airscale(common_units=[_common_unit_2_2])

_lte_real_enb2 = RealEnb(airscale=_real_enb2, rms=None)

# #RealEnb3
_real_enb_pdu3 = FACOM(addr="10.57.242.6", port_numbers=[4])

_common_unit_2_3 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.231.82", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu3.pdu_ports[4],
)

_real_enb3 = Airscale(common_units=[_common_unit_2_3])

_lte_real_enb3 = RealEnb(airscale=_real_enb3, rms=None)


# attenuator
_attenuator = TopYoung(
    ip_addr="10.57.243.39",
    port=3000,
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6],
    model="TAS16T16-51-120-1SDES",
)

# #5GRU for classicalBTS
# AAHJ1
_ru_pdu1 = FACOM(addr="10.57.243.2", port_numbers=[1])

_ru1 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.34", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.34", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu1.pdu_ports[1],
    radio_type=RadioTypes.AAHJ,
    signal_analyzer=None,
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
    ],
)

# AAHJ2
_ru_pdu2 = FACOM(addr="10.57.243.146", port_numbers=[1])

_ru2 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.34", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.34", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu2.pdu_ports[1],
    radio_type=RadioTypes.AAHJ,
    signal_analyzer=None,
    attenuation_ports=[
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
)

# AAHJ3
_ru_pdu3 = FACOM(addr="10.57.243.146", port_numbers=[2])

_ru3 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.34", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.34", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu3.pdu_ports[2],
    radio_type=RadioTypes.AAHJ,
    signal_analyzer=None,
    attenuation_ports=[
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[6],
    ],
)


# #DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.57.223.70", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")

_gnb_pdu = FACOM(addr="10.57.242.5", port_numbers=[2])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[2],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru1, _ru2, _ru3], f1_m_ip_addr="10.57.223.70")

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
    backhaul_site_oam_ip="10.57.223.70",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.223.70", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.223.70", username="Nemuadmin", password="nemuuser"
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
_classical_bts = ClassicalBts(dus=[_du], cu=_cu)

_tl_cloud_topology = "CLOUD_5G_BB3"

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    tl_cloud_topology=_tl_cloud_topology,
    enbs=[_lte_real_enb1, _lte_real_enb2, _lte_real_enb3],
    ues=[_android],
    attenuator=_attenuator,
)


# old version keyword under robotws5g/resource compatibility workaround
# tl = TestlineWrapper(tl)
