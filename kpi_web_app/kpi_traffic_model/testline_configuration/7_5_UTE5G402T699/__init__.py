import os
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.core import RealCore
from taf.config.testline.gnb.du import DU
from taf.config.testline.pdu import PduPort, Pdu, EPC, ATEN, RRB, APC, Gude, HBTE
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.enb import (
    Enb,
    SimEnb,
    RealEnb,
    LTEEmuEnb,
    PrismaEnb,
    DocomoEnb,
)
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.config.testline.attenuator import (
    AttenuationPort,
    TopYoung,
)  # added in taf.meta 5.4
from taf.config.testline.gnb.networkaddress import NetworkAddress  # add in taf.meta 5.4
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)
from taf.config.testline.hardware_controller import (
    AmiaFanHardwareController,
    GPSPowerHardwareController,
)
from taf.config.testline.signal_analyzer import KeysightN9935A
from taf.config.testline.nms import Netact

# from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.appserver import AppServer, TafUeAppServer
from taf.config.testline.ue import (
    Qualcomm,
    QualcommUeType,
    Android,
    MediaTek,
    TafUeAndroid,
)
from taf.config.testline import (
    NetworkAddress,
    RoutingInformation,
    TafUeDataTransferProtocol,
)
from taf.config.testline.pdn import PDNTafUeAndroidDetails
from taf.config.testline.ue import TafUeFastmile


__maintainer__ = "Shasha Liu"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_5_GMS <I_MN_5G_RAN_IV4_LINE_HZG_5@internal.nsn.com>"
)
__email__ = "shasha.liu@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

##host #Local VM
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.157", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

##RealEnb
_real_enb_pdu = HBTE(addr="10.10.10.10", port_numbers=[0, 1, 2, 3, 4, 5, 6, 7])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.101.50.167", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[0],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=None)

##5GRU for classicalBTS

_ru1_pdu = HBTE(addr="10.101.45.140", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_ru2_pdu = HBTE(addr="10.101.45.136", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru1 = RU(
    ru_hw_group="below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.0.2",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    pdu_port=_ru1_pdu.pdu_ports[2],
    radio_type=RadioTypes.AQQL,  # radio_type='AQQL'
    serial_number="L1212604426",
)

_ru2 = RU(
    ru_hw_group="below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2",
        username="serviceuser",
        password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.0.2",
        username="serviceuser",
        password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og=",
    ),
    pdu_port=_ru2_pdu.pdu_ports[1],
    radio_type=RadioTypes.AVQQ,  # radio_type='AQQL'
    serial_number="1M241103672",
)
###DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.101.50.147", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.22")

_gnb_pdu = HBTE(addr="10.101.45.134", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[5],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru1, _ru2], f1_m_ip_addr="10.101.50.147")

##CU #Auto TL Upgrading
_cu = CU(
    backhaul_site_oam_ip="10.101.50.147",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.50.147", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.50.147", username="Nemuadmin", password="nemuuser"
    ),
)

##cloud_topology #UTE Type
_tl_cloud_topology = "CLOUD_5G_RPI_SB_ASIKA102L_ABILB102B1_AQQL"

# classicalbts
_classical_bts = ClassicalBts(
    dus=[_du], cu=_cu, instance_id="2599", global_bts_id="2599"
)

# CI_Detail_UE_Type='samsung S21'
_appserver_ssh = SshServiceDetails(
    addr="10.57.191.247", username="vrf4_sg5", password="vrf4@sg5", port=55985
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.247",
    iperf_path="/data/data/com.nokia.syve.uemanager.mobile/",
    port=55986,
)

_appserver = AppServer(_iperf)

_ue1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.68.86.150", username="mn5gran", password="nokia123@"
    ),
    serial_number="R3CNC096TCT",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung S21", "cell_Mapping: [1]", "samsung"],
)

_iperf2 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.247",
    iperf_path="iperf",
    port="55699",
)

# CI_Detail_UE_Type='Qualcomm X55'
_app_server_1 = TafUeAppServer(
    app_server_name="APP_SERVER_1",
    address="10.57.191.247",
    user="vrf4_sg5",
    password="vrf4@sg5",
    bind_interface_ip="10.57.191.247",
    expected_prompt="[vrf4_sg5@appserver ~]$ ",
    binary_path="/home/vrf4_sg5/taf_debug/iperf",
    ports=[55698, 55699],
)


_data_transfer_iperf = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_app_server_1,
    # interface_name="rmnet_data1",
    interval=1,
    binary_path="/data/data/com.nokia.android.application/",
    version=2,
)

_pdn1 = PDNTafUeAndroidDetails(
    entryName="dxdata1", apnName="dxdata1", apnType=["DEFAULT"]
)

_ue2 = TafUeAndroid(
    serial_number="7f99d07c",
    capabilities=["REAL_ANDROID_UE", "cell_Mapping: [1]", "qualcomm"],
    ue_pc_address="10.68.86.227",
    data_transfer=[_data_transfer_iperf],
    ssh_connection_details=SshServiceDetails(
        addr="10.68.86.227", username="nokia5G", password="noki@123"
    ),
    ue_pc_port="9090",
    pdns=[_pdn1],
    imei="868701057847034",
    imsi="262033100013170",
)

# CI_Detail_UE_Type='Nokia FastMile 5G Receiver 5G19-A'
_fastmile_appserver_1 = TafUeAppServer(
    app_server_name="APP_SERVER_1",
    address="10.57.191.247",
    user="vrf4_sg5",
    password="vrf4@sg5",
    bind_interface_ip="10.57.191.247",
    expected_prompt="[vrf4_sg5@appserver ~]$ ",
    binary_path="/home/vrf4_sg5/taf_debug/iperf",
    ports=[55260, 55264],
)

_fastmile_data_transfer_1 = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_fastmile_appserver_1,
    interval=1,
    binary_path="iperf",
    version=2,
)


_fastmile_1 = TafUeFastmile(
    ue_pc_address="10.68.86.227",
    root_password="Xn-Vs=!RE6_9Umbi",
    default_user_password="AZ=vE66Vq-o7F9g2",
    ue_manage_ip="192.168.0.1",
    serial_number="KLT232200BC8",
    version="Receiver 5G19-A",
    data_transfer=[_fastmile_data_transfer_1],
    ue_pc_port=5555,
    capabilities=["REAL_FASTMILE_UE1", "nokia_fastmile"],
)

# # netact - kongfu
_netact = Netact("10.106.161.25")

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    nms=_netact,
    enbs=[_lte_real_enb],
    ues=[_ue1, _fastmile_1],
    appserver=_appserver,
    tl_cloud_topology=_tl_cloud_topology,
)
