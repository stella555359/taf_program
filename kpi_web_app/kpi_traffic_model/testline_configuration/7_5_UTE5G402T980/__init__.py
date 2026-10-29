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
from taf.config.testline.testpc import TestPc
from taf.config.testline.core import EPCSim, LTEEmuCore, PrismaCore
from taf.config.testline import RU, DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, HBTE
from taf.config.testline.attenuator import AttenuationPort
from taf.config.testline.attenuator import HBTE as PA_HBTE
from taf.config.testline import TopYoung_PDU
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
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)
from taf.config.testline.attenuator import AttenuationPort, TopYoung
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.config.testline.appserver import AppServer, TafUeAppServer
from taf.config.testline.testpc import Connection
from taf.config.testline import NetworkAddress, RoutingInformation
from taf.config.testline.taf_ue_data_transfer_protocol import TafUeDataTransferProtocol
from taf.config.testline.ue import TafUeFastmile
from taf.config.testline.ue import (
    TafUeFastmile,
    Qualcomm,
    QualcommUeType,
    Android,
)

__maintainer__ = "yulu"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_2_GMS <I_MN_5G_RAN_IV4_LINE_HZG_2@internal.nsn.com>"
)
__email__ = "lu.1.yu@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))


# huawei
_appserver_ssh = SshServiceDetails(
    addr="10.71.207.143", username="vrf4_sg2", password="Vrf4@sg2_123456"
)

_appserver_ssh_2 = SshServiceDetails(
    addr="10.71.207.143", username="vrf4_sg2", password="Vrf4@sg2_123456", port=51126
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.207.143",
    iperf_path="/usr/bin/iperf",
    port=52980,
)

_iperf_2 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh_2,
    network_interface_address="10.71.207.143",
    iperf_path=None,
    port=51011,
)

_Huawei_host_ssh = SshServiceDetails(
    addr="10.0.176.222", username="mn5gran", password="nokia123@"
)

_appserver = AppServer(_iperf)

_Huawei = Android(
    ssh_connection_details=_Huawei_host_ssh,
    serial_number="9EQUT20903003324",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "Huawei"],
)

_Huawei_1_host_ssh = SshServiceDetails(
    addr="10.71.217.212", username="MN5GRAN", password="nokia123@"
)

_Huawei_1 = Android(
    ssh_connection_details=_Huawei_1_host_ssh,
    serial_number="7TD5T21402010749",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "cell_Mapping: [1]", "huawei"],
)

_Huawei_2_host_ssh = SshServiceDetails(
    addr="10.0.176.222", username="mn5gran", password="nokia123@"
)

_Huawei_2 = Android(
    ssh_connection_details=_Huawei_2_host_ssh,
    serial_number="RFCNC0QW78E",
    server_dir="/cygdrive/c/pyro_server",
    python_path="/cygdrive/c/Python38/python.exe",
    service_call_attach="14",
    service_call_detach="14",
    iperf_details=_iperf_2,
    capabilities=["samsung", "samsung_lte"],
    imsi="460023100013260",
)

# CI_Detail_UE_Type='Nokia_FastMile_5G_Receiver(5G19-A)'
_fastmile_appserver_1 = TafUeAppServer(
    app_server_name="APP_SERVER_1",
    address="10.71.207.143",
    user="vrf4_sg2",
    password="Vrf4@sg2_123456",
    bind_interface_ip="10.71.207.143",
    expected_prompt="[iperf@appserver ~]$ ",
    binary_path="/usr/bin/iperf",
    ports=[52980, 52981],
)

_fastmile_data_transfer_1 = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_fastmile_appserver_1,
    interval=1,
    binary_path="/usr/bin/iperf",
    version=2,
)

_fastmile = TafUeFastmile(
    ue_pc_address="10.57.167.117",
    root_password="MPXf2MnMrjZ-rDpW",
    default_user_password="U,QndrRZKG@xcE,d",
    ue_manage_ip="10.71.215.166",
    serial_number="KLT241000AF1",
    data_transfer=[_fastmile_data_transfer_1],
    proxy_mngr_port=9955,
    ueproxy_force_release=True,
    version="receiver 5g19a",
    capabilities=["REAL_FASTMILE_UE1", "nokia_fastmile"],
)

# #5GRU for classicalBTS
_attenuator = PA_HBTE(
    ip_addr="10.71.215.205",
    port=5000,
    attenuation_port_numbers=[13, 14, 15, 16],
    model="PA-16-16-6-127-0.5-B-S",
)

# 5GRU for classicalBTS
_ru_0_pdu = HBTE(addr="10.71.197.78", port_numbers=[4])

_ru_0 = RU(
    #'AQHA'
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.73.129",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.73.129",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    pdu_port=_ru_0_pdu.pdu_ports[4],
    radio_type=RadioTypes.AQHA.value,
    serial_number="1M221812232",
    attenuation_ports=[
        _attenuator.attenuator_ports[13],
        _attenuator.attenuator_ports[14],
        _attenuator.attenuator_ports[15],
        _attenuator.attenuator_ports[16],
    ],
)

_ru_1_pdu = TopYoung_PDU(addr="10.71.197.84", port_numbers=[4])

_ru_1 = RU(
    #'AHPH'
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.73.129", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.73.129", username="root", password="umniedziala"
    ),
    pdu_port=_ru_1_pdu.pdu_ports[4],
    radio_type=RadioTypes.AHPH.value,
    serial_number="EA220151513",
)

_ru_2_pdu = TopYoung_PDU(addr="10.71.197.84", port_numbers=[5])

_ru_2 = RU(
    #'AHPF'
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.73.129", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.73.129", username="root", password="umniedziala"
    ),
    pdu_port=_ru_2_pdu.pdu_ports[5],
    radio_type=RadioTypes.AHPF.value,
    serial_number="EA211653128",
)

_ru_3_pdu = TopYoung_PDU(addr="10.71.197.84", port_numbers=[2])

_ru_3 = RU(
    #'AHPF'
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.73.129", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.73.129", username="root", password="umniedziala"
    ),
    pdu_port=_ru_3_pdu.pdu_ports[2],
    radio_type=RadioTypes.AHPF.value,
    serial_number="EA211155296",
)

# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(
    addr="192.168.253.20",
    hardware_type="ABIO",
)

_gnb_pdu = HBTE(addr="10.71.197.89", port_numbers=[7])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[7],
    hardware_type="ASIB",
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(
    airscale=_airscale, rus=[_ru_0, _ru_1, _ru_2, _ru_3], f1_m_ip_addr="10.71.201.233"
)

_cu = CU(
    backhaul_site_oam_ip="10.71.201.233",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.201.233", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.201.233", username="Nemuadmin", password="nemuuser"
    ),
)


# cloud_topology
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ANDROID_SA_ASIBL_ABIOB1_AQHA_AHPH_2xAHPF"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=980, global_bts_id=980)

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.251.47", username="ute", password="ute"
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_classical_bts.dus[0].airscale.common_units[0],
            interface_type="lmp",
        )
    ],
)

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    ues=[
        _fastmile,
        _Huawei_1,
        _Huawei_2,
    ],
    attenuator=_attenuator,
    tl_cloud_topology=_tl_cloud_topology,
    appserver=_appserver,
)
