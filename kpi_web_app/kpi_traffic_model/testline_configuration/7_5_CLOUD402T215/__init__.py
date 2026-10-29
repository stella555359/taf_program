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
from taf.config.testline.core import EPCSim
from taf.config.testline import RU, DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CU, ClassicalBts
from taf.config.testline.ue import Android
from taf.config.testline import RealEnb, RadioModule
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline import Enb, SimEnb, RealEnb, RadioModule, LTEEmuEnb
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.mcs import TopYoung as TopYoung_MCS
from taf.config.testline.mcs import HBTE
from taf.config.testline.core import RealCore
from taf.config.testline.pdu import HBTE, TopYoung
from taf.config.testline.gnb.du import Cablink, Endpoint
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)
from taf.config.testline import NetworkAddress, RoutingInformation
from taf.config.testline.taf_ue_data_transfer_protocol import TafUeDataTransferProtocol
from taf.config.testline.ue import TafUeFastmile
from taf.config.testline.ue import (
    TafUeFastmile,
    Qualcomm,
    QualcommUeType,
    Android,
)
from taf.config.testline.appserver import TafUeAppServer, AppServer
from taf.config.testline.gnb.networkaddress import NetworkAddress

__maintainer__ = "BIJIAJIAN"
__team__ = "MN 5G RAN I&V 4 Pz HZG SG2"
__email__ = "jiajian.bi@nokia-sbell.com"

## common
__all__ = ["tl"]

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

# Test PC
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.195.30", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# Real 5G Core is used in real world.  here use EPCsim as the 5GC class is not implemented in tl config lib yet.
_epc_sim = EPCSim(
    mme_ip="10.110.227.5",
    mcc="460",
    mnc="2",
    tac="0",
    default_ssh_connection_details=SshServiceDetails(
        addr="10.110.227.70", username="haijtest", password="Nokia_1234"
    ),
    edaemon_port=10000,
    egate_port=20000,
    dir_path="/opt/iphy/latest",
    cfg_filename="LRC.cfg",
)

##5GRU for classical BTS
_ru1_pdu = FACOM(addr="10.57.243.26", port_numbers=[6])

_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="rfsw", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.101.1", username="user", password="pass"
    ),
    pdu_port=_ru1_pdu.pdu_ports[6],
)

_ru2_pdu = FACOM(addr="10.57.243.26", port_numbers=[5])

_ru2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="rfsw", password="3Is6ezFJ7dFlB29cgs0yp3RCM3fUF1zNO1+6Z08tlAc="
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.101.1", username="user", password="pass"
    ),
    pdu_port=_ru2_pdu.pdu_ports[5],
)

_ru3_pdu = FACOM(addr="10.57.243.26", port_numbers=[2])

_ru3 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="rfsw", password="3Is6ezFJ7dFlB29cgs0yp3RCM3fUF1zNO1+6Z08tlAc="
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.101.1", username="user", password="pass"
    ),
    pdu_port=_ru3_pdu.pdu_ports[2],
)

_ru4_pdu = FACOM(addr="10.57.243.26", port_numbers=[1])

_ru4 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="rfsw", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.101.1", username="user", password="pass"
    ),
    pdu_port=_ru4_pdu.pdu_ports[1],
)

##DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="6.6.6.6")

_gnb_pdu = FACOM(addr="10.57.242.38", port_numbers=[1])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[1],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru1, _ru2, _ru3, _ru4], f1_m_ip_addr="10.57.223.195")

##CU
_cu = CU(
    backhaul_site_oam_ip="10.57.223.195",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.223.195", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.223.195", username="Nemuadmin", password="nemuuser"
    ),
)

##cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id="1031", global_bts_id="1031")

##TOPYOUNG_MCS
_topyoung = TopYoung_MCS(
    ip_addr="10.57.156.190",
    port=28888,
    mcs_port_numbers=[64],
    #vendor="TopYoung",
    model="MCS2350A2-64B32-E6",
)


_appserver_ssh = SshServiceDetails(
    addr="10.57.191.236", username="vrf4_sg2", password="VERIFICATION@sg2", port="52228"
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.236",
    iperf_path="/usr/bin/iperf",
    port="52228",
)

_appserver = AppServer(_iperf_details_on_appserver)

# #Qualcomm
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.130.235",
    iperf_path="/cygdrive/c/tools",
    port="52229",
)

_qcom = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.235", username="nokia5G", password="noki@123"
    ),
    serial_number="7375f3dc",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files/Qualcomm/QCAT7/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "sdx70", "qct_dx50"],
    clear_server_files="yes",
    clear_logs="yes",
    network_mode_switch_method="keyevents",
    mobile_network_text="SIMs",
    setting_network_mode_text="Preferred network type",
)

# CI_Detail_UE_Type='Nokia FastMile 5G Gateway 3.2'
_fastmile_appserver_1 = TafUeAppServer(
    app_server_name="APP_SERVER_1",
    address="10.57.191.244",
    user="vrf4_sg2",
    password="Vrf4@sg2_123456",
    bind_interface_ip="10.57.191.244",
    expected_prompt="[vrf4_sg2@appserver ~]$ ",
    binary_path="/usr/bin/iperf",
    ports=[52228, 52229],
)

_fastmile_data_transfer_1 = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_fastmile_appserver_1,
    interval=1,
    binary_path="/usr/bin/iperf",
    version=2,
)

_fastmile_1 = TafUeFastmile(
    ue_pc_address="10.57.195.30",
    root_password="c75a4492bdc3",
    ue_manage_ip="10.70.222.185",
    serial_number="LPL2214005A4",
    data_transfer=[_fastmile_data_transfer_1],
    proxy_mngr_port=9955,
    ueproxy_force_release=True,
    version="3.2",
    capabilities=["REAL_FASTMILE_UE1", "nokia_fastmile"],
)

_fastmile_2 = TafUeFastmile(
    ue_pc_address="10.57.195.30",
    root_password="cd4a3db28f5e",
    ue_manage_ip="10.70.222.188",
    serial_number="LPL2214004E9",
    data_transfer=[_fastmile_data_transfer_1],
    proxy_mngr_port=9955,
    ueproxy_force_release=True,
    version="3.2",
    capabilities=["REAL_FASTMILE_UE2", "nokia_fastmile"],
)

_fastmile_3 = TafUeFastmile(
    ue_pc_address="10.57.195.30",
    root_password="474ae69285b6",
    ue_manage_ip="10.70.222.186",
    serial_number="LPL22140062C",
    data_transfer=[_fastmile_data_transfer_1],
    proxy_mngr_port=9955,
    ueproxy_force_release=True,
    version="3.2",
    capabilities=["REAL_FASTMILE_UE3", "nokia_fastmile"],
)

_fastmile_4 = TafUeFastmile(
    ue_pc_address="10.57.195.30",
    root_password="44baba522e9d",
    ue_manage_ip="10.70.222.184",
    serial_number="LPL22140060E",
    data_transfer=[_fastmile_data_transfer_1],
    proxy_mngr_port=9955,
    ueproxy_force_release=True,
    version="3.2",
    capabilities=["REAL_FASTMILE_UE4", "nokia_fastmile"],
)

_fastmile_5 = TafUeFastmile(
    ue_pc_address="10.57.195.30",
    root_password="38aab3e285b9",
    ue_manage_ip="10.70.222.183",
    serial_number="LPL221400622",
    data_transfer=[_fastmile_data_transfer_1],
    proxy_mngr_port=9955,
    ueproxy_force_release=True,
    version="3.2",
    capabilities=["REAL_FASTMILE_UE5", "nokia_fastmile"],
)

_fastmile_6 = TafUeFastmile(
    ue_pc_address="10.57.195.30",
    root_password="ccda26a2c38a",
    ue_manage_ip="10.70.222.187",
    serial_number="LPL221400584",
    data_transfer=[_fastmile_data_transfer_1],
    proxy_mngr_port=9955,
    ueproxy_force_release=True,
    version="3.2",
    capabilities=["REAL_FASTMILE_UE6", "nokia_fastmile"],
)

_fastmile_7 = TafUeFastmile(
    ue_pc_address="10.57.195.30",
    root_password="2f7a97526777",
    ue_manage_ip="10.70.222.189",
    serial_number="LPL22140068D",
    data_transfer=[_fastmile_data_transfer_1],
    proxy_mngr_port=9955,
    ueproxy_force_release=True,
    version="3.2",
    capabilities=["REAL_FASTMILE_UE7", "nokia_fastmile"],
)

_fastmile_8 = TafUeFastmile(
    ue_pc_address="10.57.195.30",
    root_password="c7da54829ef7",
    ue_manage_ip="10.57.156.189",
    serial_number="LPL221400629",
    data_transfer=[_fastmile_data_transfer_1],
    proxy_mngr_port=9955,
    ueproxy_force_release=True,
    version="3.2",
    capabilities=["REAL_FASTMILE_UE8", "nokia_fastmile"],
)

_fastmile_9 = TafUeFastmile(
    ue_pc_address="10.57.195.30",
    root_password="7b9ade4293ee",
    ue_manage_ip="10.57.156.185",
    serial_number="LPL221400577",
    data_transfer=[_fastmile_data_transfer_1],
    proxy_mngr_port=9955,
    ueproxy_force_release=True,
    version="3.2",
    capabilities=["REAL_FASTMILE_UE8", "nokia_fastmile"],
)

# switch Dtor
_dell_s4048on_ssh = SshServiceDetails(
    addr="0.0.0.0", port="1", username="5gran", password="nokia123"
)
_dell_s4048on_switch = DellS4048ONSwitch(_dell_s4048on_ssh)

# switch Mtor
_dell_s4048ton_ssh = SshServiceDetails(
    addr="0.0.0.0", port="1", username="5gran", password="nokia123"
)
_dell_s4048ton_switch = DellS4048TONSwitch(_dell_s4048ton_ssh)

tl = TestLine(
    test_pc=_host,
    appserver=_appserver,
    gnbs=[_classical_bts],
    core=_epc_sim,
    mcses=[_topyoung],
    ues=[_fastmile_1, _fastmile_2, _fastmile_3, _fastmile_4, _fastmile_5, _fastmile_6, _fastmile_7, _fastmile_8, _qcom, _fastmile_9],
    tl_cloud_topology=_tl_cloud_topology,
)
