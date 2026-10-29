import os
import yaml
import re
from taf.config.testline.cloud_hosting import (
    ControlNode,
    NCIR,
    CloudDeployment,
    DeploymentFlavorStack,
    DeploymentNetworkStack,
    DeploymentVnfStack,
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
from taf.config.testline.ue import (
    AirphoneCloud,
    Airphone,
    Prisma,
    TM500,
    Qualcomm,
    QualcommUeType,
    Android,
    MediaTek,
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
from taf.config.testline.appserver import AppServer
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.ue import Qualcomm, QualcommUeType, Android, MediaTek

__maintainer__ = "Liu Jia"
__team__ = "I_NSB_MN_5GSC_5G_PZ_HZ_03_GMS <I_NSB_MN_5GSC_5G_PZ_HZ_03@internal.nsn.com>"
__email__ = "jia-rebecca.liu@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# #host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.47", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_appserver_ssh = SshServiceDetails(
    addr="10.57.173.233",
    username="vrf4_sg3",
    password="Haz4_vrf_sg3",
    port="53174",
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.219.231",
    iperf_path="/cygdrive/c/iperf",
    port="53274",
)

_iperf_details_on_appserver2 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.219.231",
    iperf_path="iperf",
    port="53374",
)
_appserver = AppServer(_iperf_details_on_appserver2)

_ue_host_ssh = SshServiceDetails(
    addr="10.57.239.216", username="root", password="123456"
)

# CI_Detail_UE_Type='Qualcomm'
_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.118", username="nokia5G", password="noki@123"
    ),
    serial_number="13c72850",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["qct_dx50", "REAL_ANDROID_UE"],
)

_dingli_1 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="11375e40",
    server_dir="D:/Program Files (x86)/DingLi/Pilot PioneerX11.0.9.0---23060718/Pioneer.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    capabilities=["pioneer", "huawei_sigspark"],
    imsi="460023100012836",
)

_dingli_2 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="81d39eb3",
    server_dir="D:/Program Files (x86)/DingLi/Pilot PioneerX11.0.9.0---23060718/Pioneer.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="460023100012838",
)

_dingli_3 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="90bc04e1",
    server_dir="D:/Program Files (x86)/DingLi/Pilot PioneerX11.0.9.0---23060718/Pioneer.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="460023100012840",
)

_dingli_4 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="baf4623d",
    server_dir="D:/Program Files (x86)/DingLi/Pilot PioneerX11.0.9.0---23060718/Pioneer.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="460023100012843",
)

_dingli_5 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="d10d1f35",
    server_dir="D:/Program Files (x86)/DingLi/Pilot PioneerX11.0.9.0---23060718/Pioneer.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="460023100012842",
)

_dingli_6 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="edda48dc",
    server_dir="D:/Program Files (x86)/DingLi/Pilot PioneerX11.0.9.0---23060718/Pioneer.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="460023100012841",
)

_dingli_7 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="8e1985f2",
    server_dir="D:/Program Files (x86)/DingLi/Pilot PioneerX11.0.9.0---23060718/Pioneer.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="460023100012839",
)

_dingli_8 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="7c0260e2",
    server_dir="D:/Program Files (x86)/DingLi/Pilot PioneerX11.0.9.0---23060718/Pioneer.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="460023100012837",
)

# MTK
_ue_host_ssh_mtk = SshServiceDetails(
    addr="10.57.150.194", username="MN5GRAN", password="nokia123@"
)

_mtk = MediaTek(
    ssh_connection_details=_ue_host_ssh_mtk,
    server_dir="c:/pyro_server",
    server_port=8080,
    edb_file_path="auto",
    log_filter="2.Gen98_Default_Standard",
    imei="0123456789ABCDEF",
    imsi="310260032993623",
    apn_url="wap1",
    iperf_details=_iperf,
    capabilities=["REAL_MEDIATEK_UE1", "mtk"],
    serial_number="0123456789ABCDEF",
)

# #RealEnb
_real_enb_pdu = FACOM(addr="10.57.249.13", port_numbers=[1])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.226.131", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[1],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=None, instance_id=10632)

# #5GRU for classicalBTS
# attenuator

## _attenuator = TopYoung(
##     ip_addr="10.57.249.58",
##     port=50000,
##     attenuation_port_numbers=[1, 2, 3, 4],
##     model="Radio_PSA_64X16-1024",
## )

_hbte_params = {
    "ip_addr": "10.57.239.210",
    "port": 5000,
    "attenuation_port_numbers": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    "model": "PPSAM-64X16-2.3-5-90-0.5-360-1-S",
    "version": None,
}

_attenuator = HBTE(**_hbte_params)

_hbte_params1 = {
    "ip_addr": "10.57.239.219",
    "port": 5000,
    "attenuation_port_numbers": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    "model": "PA-16-16-6-127-0.5-B-S",
    "version": None,
}

_attenuator1 = HBTE(**_hbte_params1)

_ru1_pdu = FACOM(addr="10.57.176.67", port_numbers=[4])

_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.49", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.49", username="root", password="umniedziala"
    ),
    pdu_port=_ru1_pdu.pdu_ports[4],
    radio_type=RadioTypes.AQQA,
    signal_analyzer=None,
    # attenuation_ports=[_attenuator.attenuator_ports[11], _attenuator.attenuator_ports[12]]
)

_ru2_pdu = FACOM(addr="10.57.176.66", port_numbers=[1])

_ru2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.49", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.49", username="root", password="umniedziala"
    ),
    pdu_port=_ru2_pdu.pdu_ports[1],
    radio_type=RadioTypes.AHEGA,
    signal_analyzer=None,
    # attenuation_ports=[_attenuator.attenuator_ports[11], _attenuator.attenuator_ports[12]]
)

_ru3_pdu = FACOM(addr="10.57.176.67", port_numbers=[5])

_ru3 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.49", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.49", username="root", password="umniedziala"
    ),
    pdu_port=_ru3_pdu.pdu_ports[5],
    radio_type=RadioTypes.AZNA,
    signal_analyzer=None,
    # attenuation_ports=[_attenuator.attenuator_ports[11], _attenuator.attenuator_ports[12]]
)

_ru4_pdu = FACOM(addr="10.57.176.70", port_numbers=[2])

_ru4 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.49", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.49", username="root", password="umniedziala"
    ),
    pdu_port=_ru4_pdu.pdu_ports[2],
    radio_type=RadioTypes.AZNA,
    signal_analyzer=None,
    # attenuation_ports=[_attenuator.attenuator_ports[11], _attenuator.attenuator_ports[12]]
)

# #DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.57.226.130", username="toor4nsn", password="oZPS0POrRieRtu"
)

_lmp_connection_2 = SshServiceDetails(
    addr="10.57.226.143", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")

_gnb_pdu = FACOM(addr="10.57.249.13", port_numbers=[4])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=_capacity_unit,
    pdu_port=_gnb_pdu.pdu_ports[4],
)

_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection_2,
    capacity_units=_capacity_unit,
    pdu_port=_gnb_pdu.pdu_ports[4],
)

_airscale = Airscale(common_units=[_common_unit_0])

_airscale2 = Airscale(common_units=[_common_unit_1])

_du = DU(
    airscale=_airscale,
    rus=[_ru1, _ru2, _ru3],
    f1_m_ip_addr="10.57.226.130",
    f1_c_ip_addr="10.57.226.130",
    f1_u_ip_addr="10.57.226.130",
)

_du2 = DU(
    airscale=_airscale2,
    rus=[_ru4],
    f1_m_ip_addr="10.57.226.143",
    f1_c_ip_addr="10.57.226.143",
    f1_u_ip_addr="10.57.226.143",
)

# #CU
_cu = CU(
    backhaul_site_oam_ip="10.57.226.130",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.226.130", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.226.130", username="Nemuadmin", password="nemuuser"
    ),
)

_cu2 = CU(
    backhaul_site_oam_ip="10.57.226.143",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.226.143", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.226.143", username="Nemuadmin", password="nemuuser"
    ),
)

_classical_bts0 = ClassicalBts(dus=[_du], cu=_cu, instance_id=11006, global_bts_id=3741199999)

_classical_bts1 = ClassicalBts(dus=[_du2], cu=_cu2, instance_id=37673, global_bts_id=37673)

_tl_cloud_topology = "CLOUD_5G_BB3"

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts0, _classical_bts1],
    enbs=[_lte_real_enb],
    ues=[
        _dingli_1,
        _dingli_2,
        _dingli_3,
        _dingli_4,
        _dingli_5,
        _dingli_6,
        _dingli_7,
        _dingli_8,
        _mtk
    ],
    appserver=_appserver,
    attenuator=[_attenuator, _attenuator1],
    tl_cloud_topology=_tl_cloud_topology,
)
