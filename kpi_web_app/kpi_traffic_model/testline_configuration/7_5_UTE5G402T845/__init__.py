import os
from taf.config.testline.cloud_hosting import (
    ControlNode,
    NCIR,
    CloudDeployment,
    DeploymentFlavorStack,
    DeploymentNetworkStack,
    DeploymentVnfStack,
)
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.attenuator import (
    AttenuationPort,
    HBTE,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.core import EPCSim, LTEEmuCore, PrismaCore
from taf.config.testline import RU, DU, AppServer
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC
from taf.config.testline.pdu import HBTE as PduHBTE
from taf.config.testline.pdu import TopYoung as PduTopYoung
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import AirphoneCloud, Airphone, Prisma, TM500, Android
from taf.config.testline import Enb, SimEnb, RealEnb, LTEEmuEnb, PrismaEnb, DocomoEnb
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.taf_ue_data_transfer_protocol import TafUeDataTransferProtocol
from taf.config.testline.ue import TafUeFastmile
from taf.config.testline.appserver import TafUeAppServer
from taf.config.testline.dcap import DcapRnD, DcapBasic

__maintainer__ = "lei wang"  # TL owner name
__team__ = "I_MN_5G_RAN_IV4_LINE_HZG_8_IV@internal.nsn.com"  # TL owner's team
__email__ = "lei.24.wang@nokia-sbell.com"  # TL owner's email

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.174", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# RU
_PB_WI16_1 = PduHBTE(addr="10.57.241.156", port_numbers=[5])
_ru_1 = RU(
    ru_hw_group="AHLOA",
    serial_number="BL2004G100H",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password=""
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.130.101", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_PB_WI16_1.pdu_ports[5],
)

_PB_WI16_1 = PduHBTE(addr="10.57.241.156", port_numbers=[6])
_ru_2 = RU(
    ru_hw_group="AHFIB",
    serial_number="BL2112V0A49",
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="xxx", password="xxx"
    ),
    lmp_connection=SshServiceDetails(
        addr="1.1.1.1", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_PB_WI16_1.pdu_ports[6],
)

_PB_WI05_1 = PduHBTE(addr="10.57.172.202", port_numbers=[4])
_PA_WI11_PA210807007 = HBTE(
    ip_addr="10.57.236.3",
    port="5000",
    model="PA-16-16-6-127-0.5-B-S",
    attenuation_port_numbers=[r for r in range(1, 17)],
)
_ru_3 = RU(
    ru_hw_group="AEHC",
    serial_number="K9223130063",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1",
        username="serviceuser",
        password="7B+6yyInfX0uES/FP60uEyhjZHUxB2MoRWvZqUMW42g=",
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.150.188", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_PB_WI05_1.pdu_ports[4],
    attenuation_ports=[
        _PA_WI11_PA210807007.attenuator_ports[7],
        _PA_WI11_PA210807007.attenuator_ports[8],
        _PA_WI11_PA210807007.attenuator_ports[15],
        _PA_WI11_PA210807007.attenuator_ports[16],
    ],
)

_PB_WI17_1 = PduHBTE(addr="10.57.172.222", port_numbers=[4])
_ru_4 = RU(
    ru_hw_group="AHFIB",
    serial_number="BL2124V0E9I",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.150.204", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_PB_WI17_1.pdu_ports[4],
)


# DU for classicalBTS
_PB_WI23_1 = PduHBTE(addr="10.57.241.168", port_numbers=[7])
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(addr="192.168.253.20")
_gnb_test_pc_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.174", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_gnb_test_pc_1 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.28", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_PB_WI23_1.pdu_ports[7],
    test_pc=_gnb_test_pc_0,
)
_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_PB_WI23_1.pdu_ports[7],
    test_pc=_gnb_test_pc_1,
)
_airscale = Airscale(common_units=[_common_unit_0, _common_unit_1])
_du = DU(
    airscale=_airscale,
    rus=[_ru_1, _ru_2, _ru_3, _ru_4],
    f1_m_ip_addr="10.57.228.71",
)

# CU
_cu = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.228.71", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.228.71", username="Nemuadmin", password="nemuuser"
    ),
)

# Dcap
_tce_pc = DcapBasic(
    connection_details=HttpConnectionDetails(
        addr="10.57.195.82",
        username="utfuser",
        password="utfadmin!",
        port=49148,
    )
)

# classicalbts
_classical_bts = ClassicalBts(
    dus=[_du], cu=_cu, global_bts_id=4294967208, instance_id=4294967208, dcap=_tce_pc
)


# QualComm UE
_appserver_ssh = SshServiceDetails(
    addr="10.57.191.238", username="vrf3_sg6", password="vrf3@sg6"
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.238",
    iperf_path="/usr/bin/iperf",
    port=57845,
)
_iperf_ul = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.238",
    iperf_path="iperf",
    port=57845,
)
_appserver = AppServer(iperf_details=_iperf_ul)
_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.52", username="mn5gran", password="nokia123@"
    ),
    serial_number="81f58d05",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Users/mn5gran/AppData/Local/Programs/Python/Python37/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "sdx75", "qct_dx50"],
)

# for FastMile CPE
_fastmile_appserver_1 = TafUeAppServer(
    app_server_name="APP_SERVER_1",
    address="10.57.191.238",
    user="vrf3_sg6",
    password="vrf3@sg6",
    bind_interface_ip="10.57.191.238",
    expected_prompt="[vrf3_sg6@appserver ~]$ ",
    binary_path="/usr/bin/iperf",
    ports=[57845, 57845],
)

_fastmile_data_transfer_1 = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_fastmile_appserver_1,
    interval=1,
    binary_path="iperf",
    version=2,
)

_android_0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.121", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="81f58d05",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python310/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_UE", "qct_dx50"],
)


_sigspark_multiUE = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.236.162", username="MTU", password="MTU"
    ),
    serial_number="835de864",
    server_dir="C:/Program Files (x86)/Spark1.6.2.0/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    # imsi="460023100017081",
    # licensekeeper=_licensekeeper,
    capabilities=["REAL_ANDROID_UE1", "sigspark_multiUE"],
)


_l3call_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.130.121", port="22", username="mn5gran", password="nokia123@"
    )
)

tl = TestLine(
    test_pc=_host,
    test_pcs=[_l3call_pc],
    gnbs=[_classical_bts],
    # enbs=[_lte_real_enb],
    ues=[_android_0, _sigspark_multiUE],
    appserver=_appserver,
)
