import os
from taf.config.testline.cloud_hosting import (
    ControlNode,
    NCIR,
    CloudDeployment,
    DeploymentFlavorStack,
    DeploymentNetworkStack,
    DeploymentVnfStack,
    DeploymentSecurityGroupStack,
    ComputeNode,
    OSP,
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
from taf.config.testline.gnb.du import DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, ATEN, RRB, APC, Gude
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.core import RealCore, RealCore5GDetails, AMF
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
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.config.testline.attenuator import (
    AttenuationPort,
    TopYoung,
    HBTE,
)  # added in taf.meta 5.4
from taf.config.testline.gnb.networkaddress import (
    NetworkAddress,
    RoutingInformation,
)  # add in taf.meta 5.4
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
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.optical_switch import Leoni
from taf.config.testline.appserver import AppServer
from taf.config.testline.ue import Qualcomm, QualcommUeType, Android, MediaTek

__maintainer__ = "ming shi"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_3_GMS <I_MN_5G_RAN_IV4_LINE_HZG_3@internal.nsn.com>"
)
__email__ = "ming.shi@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# testPC(TAF)
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.145", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_appserver_ssh = SshServiceDetails(
    addr="10.71.207.150", username="vrf4_sg3", password="Haz4_vrf_sg3", port="53366"
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.207.150",
    iperf_path="/usr/bin/iperf",
    port="53366",
)

_appserver = AppServer(_iperf_details_on_appserver)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.207.150",
    iperf_path="/cygdrive/c/iperf",
    port="53466",
)

_ue_host_ssh = SshServiceDetails(
    addr="10.71.206.73", username="root", password="123456"
)

# CI_Detail_UE_Type='Qualcomm'
_pioneer_1 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="11375e40",
    server_dir="D:/Program Files (x86)/DingLi/Pilot PioneerX11.0.9.0---06171309/Pioneer.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    capabilities=["pioneer", "huawei_sigspark"],
    imsi="460023100001215",
    pdn="dxdata1",
)

_pioneer_2 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="81d39eb3",
    server_dir="D:/Program Files (x86)/DingLi/Pilot PioneerX11.0.9.0---06171309/Pioneer.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="460023100001214",
)

_pioneer_3 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="90bc04e1",
    server_dir="D:/Program Files (x86)/DingLi/Pilot PioneerX11.0.9.0---06171309/Pioneer.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="460023100001213",
)

_pioneer_4 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="baf4623d",
    server_dir="D:/Program Files (x86)/DingLi/Pilot PioneerX11.0.9.0---06171309/Pioneer.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="460023100001211",
)

_pioneer_5 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="d10d1f35",
    server_dir="D:/Program Files (x86)/DingLi/Pilot PioneerX11.0.9.0---06171309/Pioneer.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="460023100001218",
)

_pioneer_6 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="edda48dc",
    server_dir="D:/Program Files (x86)/DingLi/Pilot PioneerX11.0.9.0---06171309/Pioneer.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="460023100001212",
)

_pioneer_7 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="8e1985f2",
    server_dir="D:/Program Files (x86)/DingLi/Pilot PioneerX11.0.9.0---06171309/Pioneer.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="460023100001216",
)

_pioneer_8 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="7c0260e2",
    server_dir="D:/Program Files (x86)/DingLi/Pilot PioneerX11.0.9.0---06171309/Pioneer.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="262033100001217",
)

_pioneer_9 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="11375e40",
    server_dir="D:/Program Files (x86)/DingLi/Pilot PioneerX11.0.9.0---06171309/Pioneer.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    capabilities=["pioneer", "huawei_sigspark"],
    imsi="460023100001215",
    pdn="dxdata1",
)

_pioneer_10 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="81d39eb3",
    server_dir="D:/Program Files (x86)/DingLi/Pilot PioneerX11.0.9.0---06171309/Pioneer.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="460023100001214",
)

_pioneer_11 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="90bc04e1",
    server_dir="D:/Program Files (x86)/DingLi/Pilot PioneerX11.0.9.0---06171309/Pioneer.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="460023100001213",
)

_pioneer_12 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="baf4623d",
    server_dir="D:/Program Files (x86)/DingLi/Pilot PioneerX11.0.9.0---06171309/Pioneer.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="460023100001211",
)

_pioneer_13 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="d10d1f35",
    server_dir="D:/Program Files (x86)/DingLi/Pilot PioneerX11.0.9.0---06171309/Pioneer.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="460023100001218",
)

_pioneer_14 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="edda48dc",
    server_dir="D:/Program Files (x86)/DingLi/Pilot PioneerX11.0.9.0---06171309/Pioneer.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="460023100001212",
)

_pioneer_15 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="8e1985f2",
    server_dir="D:/Program Files (x86)/DingLi/Pilot PioneerX11.0.9.0---06171309/Pioneer.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="460023100001216",
)

_pioneer_16 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="7c0260e2",
    server_dir="D:/Program Files (x86)/DingLi/Pilot PioneerX11.0.9.0---06171309/Pioneer.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="262033100001217",
)

# _android0 = Android(
#     ssh_connection_details=SshServiceDetails(
#         addr="10.57.130.174", username="nokia5G", password="noki@123"
#     ),
#     serial_number="17468ace",
#     server_dir="/cygdrive/c/pyro_server/",
#     python_path="C:/Python27/python.exe",
#     iperf_details=_iperf,
#     capabilities=["Qualcomm SDX55", "qct_dx50"],
# )
#
# _android = Android(
#     ssh_connection_details=SshServiceDetails(
#         addr="10.57.152.90", username="tester", password="tester123"
#     ),
#     serial_number="5101394b",
#     server_dir="/cygdrive/c/pyro_server/",
#     python_path="C:/Python27/python.exe",
#     qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
#     diag_cfg_path="C:/pyro_server/DIAG.cfg",
#     iperf_details=_iperf,
#     capabilities=["REAL_UE", "REAL_ANDROID_UE"],
# )

_hbte_params = {
    "ip_addr": "10.71.206.21",
    "port": 5000,
    "attenuation_port_numbers": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    "model": "PA-16-16-6-127-0.5-B-S",
    "version": None,
}
_attenuator = HBTE(**_hbte_params)

_hbte_params_2 = {
    "ip_addr": "10.71.206.25",
    "port": 5000,
    "attenuation_port_numbers": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    "model": "PA-16-16-6-127-0.5-B-S",
    "version": None,
}
_attenuator_2 = HBTE(**_hbte_params_2)

_attenuator_3 = TopYoung(
    ip_addr="10.71.206.72",
    port=50000,
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    model="MCS2338A-64B16-B1",
)

# 5GRU for classicalBTS
_ru_pdu1 = FACOM(addr="10.71.196.247", port_numbers=[1])

_ru1 = RU(
    ru_hw_group="AHLOB",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.101.1", username="nokia", password="nokia123"
    ),
    pdu_port=_ru_pdu1.pdu_ports[1],
    radio_type=RadioTypes.AHLOB,
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
)

_ru_pdu2 = FACOM(addr="10.71.196.248", port_numbers=[4])

_ru2 = RU(
    ru_hw_group="AHLOB",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.101.1", username="nokia", password="nokia123"
    ),
    pdu_port=_ru_pdu2.pdu_ports[4],
    radio_type=RadioTypes.AHLOB,
    attenuation_ports=[
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[6],
        _attenuator.attenuator_ports[7],
        _attenuator.attenuator_ports[8],
    ],
)

_ru_pdu3 = FACOM(addr="10.71.196.248", port_numbers=[6])

_ru3 = RU(
    ru_hw_group="AHFIB",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.101.1", username="nokia", password="nokia123"
    ),
    pdu_port=_ru_pdu3.pdu_ports[6],
    radio_type=RadioTypes.AHFIB,
    attenuation_ports=[
        _attenuator.attenuator_ports[9],
        _attenuator.attenuator_ports[10],
        _attenuator.attenuator_ports[11],
        _attenuator.attenuator_ports[12],
    ],
)

_ru_pdu4 = FACOM(addr="10.71.196.248", port_numbers=[5])
_ru4 = RU(
    ru_hw_group="AHFIB",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.101.1", username="nokia", password="nokia123"
    ),
    pdu_port=_ru_pdu4.pdu_ports[5],
    radio_type=RadioTypes.AHFIB,
    attenuation_ports=[
        _attenuator.attenuator_ports[13],
        _attenuator.attenuator_ports[14],
        _attenuator.attenuator_ports[15],
        _attenuator.attenuator_ports[16],
    ],
)

_ru_pdu5 = FACOM(addr="10.71.196.247", port_numbers=[5])
_ru5 = RU(
    ru_hw_group="AVHA",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.101.1", username="nokia", password="nokia123"
    ),
    pdu_port=_ru_pdu5.pdu_ports[5],
    radio_type=RadioTypes.AVHA,
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
)

_ru_pdu6 = FACOM(addr="10.71.196.248", port_numbers=[1])
_ru6 = RU(
    ru_hw_group="AVHA",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.101.1", username="nokia", password="nokia123"
    ),
    pdu_port=_ru_pdu6.pdu_ports[1],
    radio_type=RadioTypes.AVHA,
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
)

# classical gNB LMP
_lmp_connection = SshServiceDetails(
    addr="10.71.214.105", username="toor4nsn", password="oZPS0POrRieRtu"
)

# abil internal IP
_capacity_unit = CapacityUnit(addr="192.168.253.20")

# gNB PB
_gnb_pdu = FACOM(addr="10.71.196.246", port_numbers=[1])
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[1],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du1 = DU(
    airscale=_airscale,
    rus=[_ru1, _ru2, _ru3, _ru4, _ru5, _ru6],
    f1_m_ip_addr="10.71.214.105",
    f1_c_ip_addr="10.71.214.105",
    f1_u_ip_addr="10.71.214.105",
)

# gNB MPlane IP
_cu1 = CU(
    backhaul_site_oam_ip="10.71.214.105",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.214.105", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.214.105", username="Nemuadmin", password="nemuuser"
    ),
)

# RealEnb2
_lmp_connection_enb = SshServiceDetails(
    addr="10.71.214.105", username="toor4nsn", password="oZPS0POrRieRtu"
)
_enb_pdu = FACOM(addr="10.71.196.246", port_numbers=[1])
_common_unit_2 = CommonUnit(
    lmp_connection=_lmp_connection_enb,
    capacity_units=[],
    pdu_port=_enb_pdu.pdu_ports[1],
)
_real_enb = Airscale(common_units=[_common_unit_2])
_lte_real_enb = RealEnb(
    airscale=_real_enb, rms=None, instance_id=36621, global_bts_id=3661100000
)
# cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

# switch port to EIF1
_dell_s4048on_ssh = SshServiceDetails(
    addr="10.71.214.97", port="20/37", username="5gran", password="nokia123"
)
_dell_s4048on_switch = DellS4048ONSwitch(_dell_s4048on_ssh)

# instance_id=MRBTS_ID
_classical_bts = ClassicalBts(
    dus=[_du1], cu=_cu1, instance_id=36611, global_bts_id=3661100000
)

# realcore
_amf_ssh = SshServiceDetails(
    addr="to_be_updated", username="to_be_updated", password="to_be_updated"
)

_amf_n2_addr = NetworkAddress(v4="10.70.255.6", v6="to_be_updated", vlan_id=None)

_amf = AMF(oam_ssh_connection_details=_amf_ssh, n2=_amf_n2_addr)

_core = RealCore(five_g=RealCore5GDetails(amf=_amf), mcc=310, mnc=260)

# Netact IP
_netact = Netact("10.106.161.25")

tl = TestLine(
    test_pc=_host,
    core=_core,
    gnbs=[_classical_bts],
    enbs=[_lte_real_enb],
    ues=[
        _pioneer_1,
        _pioneer_2,
        _pioneer_3,
        _pioneer_4,
        _pioneer_5,
        _pioneer_6,
        _pioneer_7,
        _pioneer_8,
        _pioneer_9,
        _pioneer_10,
        _pioneer_11,
        _pioneer_12,
        _pioneer_13,
        _pioneer_14,
        _pioneer_15,
        _pioneer_16
    ],
    appserver=_appserver,
    tl_cloud_topology=_tl_cloud_topology,
    switches=[_dell_s4048on_switch],
    attenuator=[_attenuator, _attenuator_2, _attenuator_3],
    nms=_netact,
)
