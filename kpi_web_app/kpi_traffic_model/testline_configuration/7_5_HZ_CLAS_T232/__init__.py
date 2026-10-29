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
from taf.config.testline.core import EPCSim, LTEEmuCore

__maintainer__ = "Jia lei"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_6_GMS <I_MN_5G_RAN_IV4_LINE_HZG_6@internal.nsn.com>"
)
__email__ = "lei.jia@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))
# #host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.209.253", username="ute", password="ute"
    )
)

# Iperf
_appserver_ssh = SshServiceDetails(
    addr="10.57.209.244", username="centos", password="APPpass"
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="9.6.6.6",
    iperf_path="/opt/app/iperf",
)

# #Prisma
_airmosaic_ssh = SshServiceDetails(
    addr="10.57.130.157", username="nokia5G", password="noki@123"
)

_airmosaic_harness = HttpConnectionDetails(addr="10.57.130.157", port=8090)

_lsu_uu_ssh = SshServiceDetails(addr="10.57.233.211", username="user", password="user")

_tstm_uu_ssh = SshServiceDetails(addr="10.57.233.211", username="user", password="user")

_prisma_ue = Prisma(
    airmosaic_ssh_connection_details=_airmosaic_ssh,
    airmosaic_harness_connection_details=_airmosaic_harness,
    lsu_uu_ssh_connection_details=_lsu_uu_ssh,
    iperf_details=_iperf,
    tstm_uu_ssh_connection_details=_tstm_uu_ssh,
)

# Qualcomm
_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.20", username="nokia5G", password="noki@123"
    ),
    serial_number="9e4b1e47",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE"],
)
################       LTEemuSim    ################
_lteemu = LTEEmuCore(
    default_ssh_connection_details=SshServiceDetails(addr="", username="", password=""),
    dir_path="/home/ute/LTEemu_core2_64_3252",
    cfg_filename="basic_wts_step1.cfg",
    mme_ip="",
    edaemon_port="22222",
    egate_port="9880",
)
# #RealEnb
_real_enb_pdu = FACOM(addr="10.57.242.45", port_numbers=[5])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.233.206", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[5],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, instance_id=1573, rms=None)

# attenuator
_attenuator = TopYoung(
    ip_addr="10.57.233.208",
    port=3000,
    attenuation_port_numbers=[1, 8],
    model="TAS16T16-51-120-1SDES",
)

# #5GRU for classicalBTS
_ru_pdu = FACOM(addr="10.57.242.46", port_numbers=[5])

_ru = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.34", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.34", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu.pdu_ports[5],
    radio_type=RadioTypes.AAHF,
    signal_analyzer=None,
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[8],
    ],
)

# #DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.57.233.203", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")

_gnb_pdu = FACOM(addr="10.57.242.46", port_numbers=[5])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[5],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru], f1_m_ip_addr="10.57.233.203")

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
    backhaul_site_oam_ip="10.57.233.203",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.233.203", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.233.203", username="Nemuadmin", password="nemuuser"
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
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=2322)

_tl_cloud_topology = "CLOUD_5G_BB3"

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    core=_lteemu,  # if use EPC ,please use replace with this:   core=_epc_sim,
    tl_cloud_topology=_tl_cloud_topology,
    enbs=[_lte_real_enb],
    ues=[_android, _prisma_ue],
    attenuator=_attenuator,
)


# old version keyword under robotws5g/resource compatibility workaround
# tl = TestlineWrapper(tl)
