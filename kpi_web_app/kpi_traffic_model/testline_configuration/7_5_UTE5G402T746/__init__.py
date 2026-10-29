__maintainer__ = "Wang Debbie"
__team__ = "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_04_GMS "
__email__ = (
    "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_04_GMS <I_NSB_MN_5GSC_MMW_SC_PZ_HZ_04@internal.nsn.com"
)
__owner_email__ = "debbie.wang@nokia-sbell.com"

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
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.core import EPCSim
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import ClassicalBts, CU
from taf.config.testline.enb import RealEnb
from taf.config.testline.ue import TM500, Android
from taf.config.testline import DU, RU
from taf.config.testline.attenuator import (
    AttenuationPort,
    HBTE,
)  # added in taf.meta 5.4
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC
from taf.config.testline.pdu import HBTE as HBTE_pb
from taf.config.testline.pdu import TopYoung as TopYoung_pb
from taf.config.testline.radio import RadioModule, RadioTypes
from taf.config.testline import IperfDataTransferDetails
from taf.config.testline.appserver import AppServer

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

_attenuator = HBTE(
    ip_addr="10.57.251.250", port="5000", attenuation_port_numbers=[1, 2, 3, 4]
)

# Testpc
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.101.60.96", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_cu = CU(
    backhaul_site_oam_ip="10.71.209.205",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.209.205", username="toor4nsn", password="oZPS0POrRieRtu", port="22"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.209.205", username="Nemuadmin", password="nemuuser"
    ),
)

# DU
_common_unit_pdu = FACOM(addr="10.57.242.11", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_lmp_connection_0 = SshServiceDetails(
    addr="10.71.209.205", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_0 = CapacityUnit(addr="192.168.253.17")

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection_0,
    capacity_units=[_capacity_unit_0],
    pdu_port=_common_unit_pdu.pdu_ports[5],
)

# airscale
_airscale_0 = Airscale(common_units=[_common_unit_0])

# 5G RU
_ru1_pdu = HBTE_pb(addr="10.71.195.134", port_numbers=[1])
_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.77.129", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.3", username="root", password="umniedziala"
    ),
    pdu_port=_ru1_pdu.pdu_ports[1],
    radio_type=RadioTypes.AHLOA,
)

_ru2_pdu = HBTE_pb(addr="10.71.195.134", port_numbers=[2])
_ru2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.77.129", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.3", username="root", password="umniedziala"
    ),
    pdu_port=_ru2_pdu.pdu_ports[2],
    radio_type=RadioTypes.AHLOA,
)

_ru3_pdu = HBTE_pb(addr="10.71.195.134", port_numbers=[3])
_ru3 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.77.129", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.3", username="root", password="umniedziala"
    ),
    pdu_port=_ru3_pdu.pdu_ports[3],
    radio_type=RadioTypes.AHFIB,
)

_ru4_pdu = HBTE_pb(addr="10.71.195.134", port_numbers=[4])
_ru4 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.77.129", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.3", username="root", password="umniedziala"
    ),
    pdu_port=_ru4_pdu.pdu_ports[4],
    radio_type=RadioTypes.AHFIB,
)

_ru5_pdu = HBTE_pb(addr="10.71.195.134", port_numbers=[5])
_ru5 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.77.129", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.3", username="root", password="umniedziala"
    ),
    pdu_port=_ru5_pdu.pdu_ports[5],
    radio_type=RadioTypes.AEHC,
)

_ru6_pdu = TopYoung_pb(addr="10.71.195.145", port_numbers=[6])
_ru6 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.77.129", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.3", username="root", password="umniedziala"
    ),
    pdu_port=_ru6_pdu.pdu_ports[6],
    radio_type=RadioTypes.AEHC,
)
# du
_du_0 = DU(
    airscale=_airscale_0,
    rus=[_ru1, _ru2, _ru3, _ru4, _ru5, _ru6],
    f1_m_ip_addr="10.71.209.205",
)

_cbts = ClassicalBts(cu=_cu, dus=[_du_0], instance_id="746", global_bts_id="746")

_appserver_ssh = SshServiceDetails(
    addr="10.70.222.53", username="mmw_sg4", password="mm@4", port="44491"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.70.222.53",
    iperf_path="/usr/bin/iperf",
    # iperf_path='/cygdrive/c/iperf',
    port="44491",
    ports=["44491", "44492", "44493", "44494", "44495", "44496", "44497", "44498"],
)

_cobham = TM500(
    tma_host=SshServiceDetails(
        addr="10.71.217.225", username="nokia5G", password="noki@123"
    ),
    tma_command_port=5004,
    iperf_details=_iperf,
    tma_path="/cygdrive/c/Program Files (x86)/Aeroflex/TM500/5G NR - NLA latest_version/Test Mobile Application/TmaApplication.exe",
)

# #Qualcomm

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.70.222.53",
    iperf_path="iperf",
    port="44101",
)

_appserver = AppServer(_iperf_details_on_appserver)

_android_4 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.217.166", username="nokia5G", password="noki@123"
    ),
    serial_number="RFCR10LXHTX",
    # server_dir="/cygdrive/c/pyro_server",
    server_dir="C:/Program Files (x86)/Spark1.1.1998.4/Bin/Spark.exe",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    imsi="310260100010821",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark", "samsung"],
)

_android_3 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.217.225", username="nokia5G", password="noki@123"
    ),
    serial_number="RFCRA03BLVV",
    # server_dir="/cygdrive/c/pyro_server",
    server_dir="C:/Program Files (x86)/Spark1.1.1998.4/Bin/Spark.exe",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    imsi="310260100010826",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark", "samsung"],
)

_android_2 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.217.225", username="nokia5G", password="noki@123"
    ),
    serial_number="RFCRA03B2KT",
    # server_dir="/cygdrive/c/pyro_server",
    server_dir="C:/Program Files (x86)/Spark1.1.1998.4/Bin/Spark.exe",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    imsi="310260100010825",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark", "samsung"],
)

_android_0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.217.226", username="nokia5G", password="noki@123"
    ),
    serial_number="R3CR412WBWE",
    # server_dir="/cygdrive/c/pyro_server",
    server_dir="C:/Program Files (x86)/Spark1.1.1998.4/Bin/Spark.exe",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    imsi="262038001006258",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark", "samsung"],
)

_android_1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.217.226", username="nokia5G", password="noki@123"
    ),
    serial_number="R3CNC0ACNRE",
    # server_dir="/cygdrive/c/pyro_server",
    server_dir="C:/Program Files (x86)/Spark1.1.1998.4/Bin/Spark.exe",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    imsi="310260100010823",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark", "samsung"],
)
# #Qualcomm

_epcsim = EPCSim(
    mme_ip="192.168.4.1",
    mcc=777,
    mnc=44,
    tac=777,
    default_ssh_connection_details=SshServiceDetails(
        addr="10.47.199.241", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    dir_path="/opt/wts/latest",
    cfg_filename="TL101_basic_cfg_realLteEnb.cfg",
    edaemon_port="22222",
    egate_port="20021",
)
_eNB_capacity_unit = CapacityUnit(addr="192.168.253.36")
_real_enb_pdu = FACOM(addr="10.57.241.158", port_numbers=[2])
_eNB_common_unit = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.71.209.207", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_real_enb_pdu.pdu_ports[2],
    capacity_units=[_eNB_capacity_unit],
)
_enb_airscale = Airscale(common_units=[_eNB_common_unit])
_enb = RealEnb(airscale=_enb_airscale, global_bts_id="7461", instance_id="746")


tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    core=_epcsim,
    enbs=[_enb],
    attenuator=_attenuator,
    ues=[_android_0, _android_1, _android_2, _android_3, _android_4],
    appserver=_appserver,
)


__all__ = ["tl"]
