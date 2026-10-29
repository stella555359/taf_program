import os
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.core import EPCSim, LTEEmuCore, PrismaCore
from taf.config.testline import RU, DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, ATEN, RRB, APC, Gude
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.ue import Android
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import AirphoneCloud, Airphone, Prisma, TM500, MediaTek
from taf.config.testline.channel_emulator import Vertex
from taf.config.testline import (
    Enb,
    SimEnb,
    RealEnb,
    RadioModule,
    LTEEmuEnb,
    PrismaEnb,
    DocomoEnb,
)
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
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

__maintainer__ = "Ji Jian"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_2_GMS <I_MN_5G_RAN_IV4_LINE_HZG_2@internal.nsn.com>"
)
__email__ = "jian.ji@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.228", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# epcsim
_epc_sim = EPCSim(
    mme_ip="10.110.90.130",
    mcc="262",
    mnc="03",
    tac="0",
    default_ssh_connection_details=SshServiceDetails(
        addr="10.110.90.130", username="test", password="NOKIA123"
    ),
    edaemon_port=10000,
    egate_port=20000,
    dir_path="/opt/iphy/latest",
    cfg_filename="LRC.cfg",
)

# vertex
_channel_emulators = Vertex(
    ip_addr="10.101.49.133",
    channel_emulator_port_numbers=["A5", "A6", "A7", "A8"],
    port=3003,
    proxy=SshServiceDetails(
        addr="10.57.157.228", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    model="vce6",
)

# 4GRU for RealEnb

# RealEnb
_real_enb_pdu = FACOM(addr="10.101.45.66", port_numbers=[4])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.101.49.131", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[4],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=None)

# 5GRU for classicalBTS
_ru_pdu = FACOM(addr="10.101.45.66", port_numbers=[5])


_ru = RU(
    # "AEHC"
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.53", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.53", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu.pdu_ports[5],
)

# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.101.49.130", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")

_gnb_pdu = FACOM(addr="10.101.45.66", port_numbers=[2])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[2],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru], f1_m_ip_addr="10.101.49.130")

_cu = CU(
    backhaul_site_oam_ip="10.101.49.130",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.49.130", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.49.130", username="Nemuadmin", password="nemuuser"
    ),
)

# cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id="1", global_bts_id="966")

_appserver_ssh = SshServiceDetails(
    addr="10.57.163.35", username="cmw_sg2", password="12345678"
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.163.35",
    iperf_path="/usr/bin/iperf",
    port=52966,
)

_Qualcomm_host_ssh = SshServiceDetails(
    addr="10.68.86.194", username="nokia5g", password="noki@123"
)

iperf_details = IperfDataTransferDetails(
    ssh_connection_details=_Qualcomm_host_ssh,
    network_interface_address="10.57.163.35",
    iperf_path="/cygdrive/c/iperf-2.0.8b-win64/iperf",
    port=52696,
)

_appserver = AppServer(iperf_details)

# CI_Detail_UE_Type='Qualcomm'
_Qualcomm = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.68.86.194", username="nokia5g", password="noki@123"
    ),
    serial_number="6e256d7",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf_details_on_appserver,
    capabilities=["REAL_UE", "qct_dx50"],
)
tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    enbs=[_lte_real_enb],
    core=_epc_sim,
    ues=[_Qualcomm],
    tl_cloud_topology=_tl_cloud_topology,
    appserver=_appserver,
    channel_emulators=_channel_emulators,
)
