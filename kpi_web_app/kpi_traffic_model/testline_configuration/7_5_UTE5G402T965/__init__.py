import os
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
from taf.config.testline.attenuator import HBTE as PA_HBTE
from taf.config.testline.core import EPCSim, LTEEmuCore, PrismaCore
from taf.config.testline import RU, DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, ATEN, RRB, APC, Gude, FPFH
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.ue import Android
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import AirphoneCloud, Airphone, Prisma, TM500, MediaTek
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

__maintainer__ = "Chen Yin"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_2_GMS <I_MN_5G_RAN_IV4_LINE_HZG_2@internal.nsn.com>"
)
__email__ = "yin.1.chen@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

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

# PA
_attenuator = PA_HBTE(
    ip_addr="10.57.223.203",
    port=5000,
    attenuation_port_numbers=[1, 2, 3, 4],
    model="PA-16-16-6-127-0.5-B-S",
)


# 5GRU for classicalBTS
_ru1_pdu = FPFH(addr="10.57.172.74", port_numbers=[6], login='admin', password='admin')

_ru1 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.33.131",
        port=5,
        username="root",
        password="a2%FgSz3$fHmdusap354xujw7a",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.33.131", username="root", password="a2%FgSz3$fHmdusap354xujw7a"
    ),
    pdu_port=_ru1_pdu.pdu_ports[6],
    radio_type=RadioTypes.AHLOA,
    serial_number="K9183920943",
)

_ru2_pdu = FACOM(addr="10.57.242.35", port_numbers=[2])

_ru2 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.33.130",
        port=5,
        username="root",
        password="root",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.33.130", username="root", password="root"
    ),
    pdu_port=_ru2_pdu.pdu_ports[2],
    radio_type=RadioTypes.AHLOA,
    serial_number="BL2209G1034",
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
)

_ru3_pdu = FPFH(addr="10.57.172.74", port_numbers=[1], login='admin', password='admin')

_ru3 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.33.128",
        port=5,
        username="root",
        password="a2%FgSz3$fHmdusap354xujw7a",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.33.128", username="root", password="a2%FgSz3$fHmdusap354xujw7a"
    ),
    pdu_port=_ru3_pdu.pdu_ports[1],
    radio_type=RadioTypes.AHFIB,
    serial_number="BL2215V011M",
)

_ru4_pdu = FPFH(addr="10.57.172.74", port_numbers=[3], login='admin', password='admin')

_ru4 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.33.128",
        port=5,
        username="root",
        password="a2%FgSz3$fHmdusap354xujw7a",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.33.128", username="root", password="a2%FgSz3$fHmdusap354xujw7a"
    ),
    pdu_port=_ru4_pdu.pdu_ports[3],
    radio_type=RadioTypes.AHFIB,
    serial_number="BL2215V011J",
)

_ru5_pdu = FACOM(addr="10.57.242.35", port_numbers=[1])

_ru5 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.49.154",
        port=5,
        username="rfsw",
        password="bdS%ztWG3v7%SjreCVA79wTPb",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.73.129", username="rfsw", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    pdu_port=_ru5_pdu.pdu_ports[1],
    radio_type=RadioTypes.AEHC,
    serial_number="L1212614396",
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
)
# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.57.223.196", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")

_gnb_pdu = FACOM(addr="10.57.242.37", port_numbers=[1])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[1],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru1, _ru2, _ru5], f1_m_ip_addr="10.57.223.196")

_cu = CU(
    backhaul_site_oam_ip="10.57.223.196",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.223.196", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.223.196", username="Nemuadmin", password="nemuuser"
    ),
)

# cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

# classicalbts
_classical_bts = ClassicalBts(
    dus=[_du], cu=_cu, instance_id="5394", global_bts_id="5394"
)

# host
# 10.57.167.170
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.170", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    connections=[_classical_bts],
)

_appserver_ssh = SshServiceDetails(
    addr="10.71.207.143", username="vrf4_sg2", password="Vrf4@sg2_123456"
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.207.143",
    iperf_path="/usr/bin/iperf",
    port=52965,
)

_huawei_host_ssh = SshServiceDetails(
    addr="10.57.150.78", username="mn5gran", password="nokia123@"
)

iperf_details = IperfDataTransferDetails(
    ssh_connection_details=_huawei_host_ssh,
    network_interface_address="10.71.207.143",
    iperf_path="/cygdrive/c/iperf-2.0.8b-win64/iperf",
    port=52596,
)

_appserver = AppServer(iperf_details)

_mtk_pdu = FACOM(addr="1.1.1.1", port_numbers=[1]).pdu_ports[1]
_elt_path = "/cygdrive/c/MTK/ELT_exe_v2.2008.0_customer_Gen97_FT"

# CI_Detail_UE_Type='Huawei Honor 30s'
_huawei = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.78", username="mn5gran", password="nokia123@"
    ),
    serial_number="QKXUT20519006609",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf_details_on_appserver,
    capabilities=["REAL_ANDROID_UE", "huawei"],
)

_ue_host_ssh = SshServiceDetails(
    addr="10.57.150.78", username="mn5gran", password="nokia123@"
)


_xiaomi = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="1101ca",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf_details_on_appserver,
    capabilities=["REAL_ANDROID_UE", "Mi11UI13", "xiaomi"],
)

# #Qualcomm
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.150.177",
    iperf_path="/cygdrive/c/tools",
    port="52965",
)

_qcom = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.177", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="e6d3d63a",
    #serial_number="27abd0a0",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files/Qualcomm/QCAT7/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["sdx70", "REAL_ANDROID_UE", "qct_dx50"],
    clear_server_files="yes",
    clear_logs="yes",
    network_mode_switch_method="keyevents",
    mobile_network_text="SIMs",
    setting_network_mode_text="Preferred network type",
)

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    core=_epc_sim,
    ues=[_xiaomi, _qcom],
    attenuator=_attenuator,
    tl_cloud_topology=_tl_cloud_topology,
    appserver=_appserver,
    test_pcs=[_host],
)
