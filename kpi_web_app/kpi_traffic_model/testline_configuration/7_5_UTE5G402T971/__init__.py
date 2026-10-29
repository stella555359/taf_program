import os
import re
import yaml
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.mcs import HBTE
from taf.config.testline.mcs import TopYoung
from taf.config.testline.appserver import TafUeAppServer
from taf.config.testline.taf_ue_data_transfer_protocol import TafUeDataTransferProtocol
# from taf.config.testline import HBTE
from taf.config.testline.core import EPCSim, LTEEmuCore, PrismaCore
from taf.config.testline import RU, DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, HBTE, TopYoung
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import (
    AirphoneCloud,
    Airphone,
    Prisma,
    TM500,
    Qualcomm,
    QualcommUeType,
    Android,
    MediaTek,
    TafUeAndroid,
    TafUeAt,
    TafUeFastmile,
)
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
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.appserver import AppServer
from taf.config.testline import Mitron

__maintainer__ = "Chen Xiaoqing"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_2_GMS <I_MN_5G_RAN_IV4_LINE_HZG_6@internal.nsn.com>"
)
__email__ = "xiaoqing.chen@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

_optical_switch = Mitron(addr="10.57.156.213", model="OXC1000-32X32-SM-1356-DD-50-LP")

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.177.78", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# 5GRU for classicalBTS
_ru1_pdu = TopYoung(addr="10.57.234.189", port_numbers=[1])

_ru1 = RU(
    #'AEHC'
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.53", username="serviceuser", password="7B+6yyInfX0uES/FP60uEyhjZHUxB2MoRWvZqUMW42g="
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.53", username="root", password="umniedziala"
    ),
    pdu_port=_ru1_pdu.pdu_ports[1],
)

_ru2_pdu = TopYoung(addr="10.57.234.189", port_numbers=[2])

_ru2 = RU(
    #'AEHC'
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.53", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.53", username="root", password="umniedziala"
    ),
    pdu_port=_ru2_pdu.pdu_ports[2],
)

# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")

_gnb_pdu = HBTE(addr="10.57.240.148", port_numbers=[1])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[1],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru1], f1_m_ip_addr="10.57.249.203")

_cu = CU(
    backhaul_site_oam_ip="10.57.249.203",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.249.203", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.249.203", username="Nemuadmin", password="nemuuser"
    ),
)

# cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

# classicalbts
_classical_bts = ClassicalBts(
    dus=[_du], cu=_cu, instance_id="10696", global_bts_id="10696"
)

_appserver_ssh = SshServiceDetails(
    addr="10.57.191.244", username="vrf4_sg2", password="Vrf4@sg2_123456"
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.244",
    iperf_path="/usr/bin/iperf",
    port=52971,
)

_appserver = AppServer(_iperf)

# _tm500 = TM500(
#    tma_host=SshServiceDetails(
#        addr="10.57.130.166",
#        username="nokia5G",
#        password="noki@123",
#    ),
#    tma_command_port=5030,
#    pdu_port=None,
#    iperf_details=_iperf,
#    tma_path="/cygdrive/c/Program Files (x86)/Aeroflex/TM500/5G NR - NLA_4_31_0/Test Mobile Application/TmaApplication.exe",
# )

# ue_config_path = os.path.join(_cfg_dir, "TestData/ue.yml")
# if os.path.isfile(ue_config_path):
#    with open(ue_config_path) as f:
#        _ue_read = f.read()
#        qci_port = re.findall("(_iperf.*?port)", _ue_read)
#        for item in qci_port:
#            _ue_read = _ue_read.replace(item, str(eval(item)))
#        _ue_config = yaml.load(_ue_read, Loader=yaml.FullLoader)
# else:
#    _ue_config = ""


# for FastMile CPE
_fastmile_appserver_1 = TafUeAppServer(
    app_server_name="APP_SERVER_1",
    address="10.57.191.244",
    user="vrf4_sg2",
    password="Vrf4@sg2_123456",
    bind_interface_ip="10.57.191.244",
    expected_prompt="[vrf4_sg2@appserver ~]$ ",
    binary_path="/usr/bin/iperf",
    ports=[52926, 52971],
)

_fastmile_data_transfer_1 = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_fastmile_appserver_1,
    interval=1,
    binary_path="/usr/bin/iperf",
    version=2,
)

_fastmile = TafUeFastmile(
    ue_pc_address="10.57.177.78",
    root_password="384a9742fd2c",
    ue_manage_ip="10.57.156.206",
    serial_number="LPL2214005CD",
    data_transfer=[_fastmile_data_transfer_1],
    version="3.2",
    proxy_mngr_port=9955,
    ueproxy_force_release=True,
    capabilities=["REAL_FASTMILE_UE", "nokia_fastmile"],
)

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    ues=[_fastmile],
    tl_cloud_topology=_tl_cloud_topology,
    appserver=_appserver,
    optical_switches=[
        _optical_switch,
    ],
)

# compatibility workaround
