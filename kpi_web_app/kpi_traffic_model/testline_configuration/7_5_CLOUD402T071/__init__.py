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
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, ATEN, RRB, APC, Gude, HBTE
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.core import RealCore  # Use RealCore() for Real Core TL
from taf.config.testline.gnb.du import Cablink, Endpoint
from taf.config.testline import NetworkAddress, RoutingInformation
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
from taf.config.testline.appserver import AppServer

__maintainer__ = "Chu Xiangsheng"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_6_GMS <I_MN_5G_RAN_IV4_LINE_HZG_6@internal.nsn.com>"
)
__email__ = "xiangsheng.chu@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))
# #host
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.145", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
# Iperf
_appserver_ssh = SshServiceDetails(
    addr="10.57.191.248", username="vrf4_sg6", password="vrf4@sg6", port="56280"
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.248",
    iperf_path="/usr/bin/iperf",
    port="56380",
)
_appserver = AppServer(_iperf)

# CI_Detail_UE_Type='Huawei Mate 30 Pro 5G;Huawei Mate 30 Pro 5G'
_android_sa = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.49", username="nokia5G", password="noki@123"
    ),
    serial_number="9YS0220110015223",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_UE1", "huawei"],
)
# Iperf
_appserver_ssh = SshServiceDetails(
    addr="10.57.191.248", username="vrf4_sg6", password="vrf4@sg6", port="56071"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.248",
    iperf_path="/usr/bin/iperf",
    port="56171",
)

# CI_Detail_UE_Type='Qualcomm;Qualcomm'
_android_nsa = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.122", username="nokia5G", password="noki@123"
    ),
    serial_number="b97b6771",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_UE0", "qct_dx50"],
)

# #RealEnb
_real_enb_pdu = HBTE(addr="10.57.242.60", port_numbers=[1])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.231.27", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[1],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=None)

# attenuator
_attenuator = TopYoung(
    ip_addr="10.57.232.102",
    port=3000,
    attenuation_port_numbers=[3, 4, 9, 10],
    model="TAS16T16-51-120-1SDES",
)

# #5GRU for classicalBTS
_ru_pdu = HBTE(addr="10.57.242.28", port_numbers=[1])

_ru = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.52", username="root", password="root"
    ),
    pdu_port=_ru_pdu.pdu_ports[1],
    radio_type=RadioTypes.AAHF,
    signal_analyzer=None,
    attenuation_ports=[
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
        _attenuator.attenuator_ports[9],
        _attenuator.attenuator_ports[10],
    ],
)

# #DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.57.223.40", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")

_gnb_pdu = HBTE(addr="10.57.242.4", port_numbers=[3])

_capacity_unit1 = CapacityUnit(addr="192.168.253.20")
_ru_cablinks = [
    Cablink(
        source=Endpoint(unit=_capacity_unit1, label="SFP", port_id=1),
        target=Endpoint(unit=_ru, label="SFP", port_id=1),
    ),
    Cablink(
        source=Endpoint(unit=_capacity_unit1, label="QSFP", port_id=2),
        target=Endpoint(unit=_ru, label="SFP", port_id=1),
    ),
]

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[3],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(
    airscale=_airscale,
    rus=[_ru],
    f1_m_ip_addr="10.57.223.40",
    cablinks=_ru_cablinks,
)

# CU
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.57.223.40",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.57.223.33", ip_prefix_length=27),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.223.40", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.223.40", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.57.223.40",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.57.223.33", ip_prefix_length=27),
    ),
    x2u=NetworkAddress(
        v4="10.57.223.40",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.57.223.33", ip_prefix_length=27),
    ),
    s1u=NetworkAddress(
        v4="10.57.223.40",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.57.223.33", ip_prefix_length=27),
    ),
)


# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=71, global_bts_id=710000)

_tl_cloud_topology = "CLOUD_5G_BB3"

tl = TestLine(
    test_pc=_test_pc,
    test_pcs=[_test_pc],
    gnbs=[_classical_bts],
    ues=[_android_sa, _android_nsa],
    enbs=[_lte_real_enb],
    core=RealCore(mcc=262, mnc=3),  # Use RealCore() for Real Core TL
    tl_cloud_topology=_tl_cloud_topology,
    attenuator=_attenuator,
    appserver=_appserver,
)


# old version keyword under robotws5g/resource compatibility workaround
# tl = TestlineWrapper(tl)
