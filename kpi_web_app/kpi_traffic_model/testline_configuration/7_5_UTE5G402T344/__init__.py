import os
import yaml
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
from taf.config.testline.pdn import PDN, PDPTypes
from taf.config.testline.core import (
    EPCSim,
    LTEEmuCore,
    PrismaCore,
    RealCore,
    RealCore4GDetails,
    RealCore5GDetails,
    AMF,
    MME,
)
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
)
from taf.config.testline.enb import (
    Enb,
    SimEnb,
    RealEnb,
    LTEEmuEnb,
    PrismaEnb,
    DocomoEnb,
)
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.config.testline.attenuator import AttenuationPort, TopYoung, HBTE
from taf.config.testline.gnb.networkaddress import NetworkAddress
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

__maintainer__ = "tizeng"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_3_GMS <I_MN_5G_RAN_IV4_LINE_HZG_3@internal.nsn.com>"
)
__email__ = "jack.zeng@nokia-sbell.com"

__all__ = ["tl"]

_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.45", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_pdns = [
    PDN(pdp_type=PDPTypes.IP.value, apn="dxdata2"),
    PDN(pdp_type=PDPTypes.IP.value, apn="ims"),
    PDN(pdp_type=PDPTypes.IP.value, apn="mdrb1.nokia.com"),
    PDN(pdp_type=PDPTypes.IP.value, apn="mdrb.nokia.com")
]


_realcore = RealCore(
    four_g=None, five_g=None, mcc="001", mnc="01", pdns=_pdns,

)

_appserver_ssh = SshServiceDetails(
    addr="10.57.191.245", username="vrf4_sg3", password="Haz4_vrf_sg3"
)

_appserver_ssh1 = SshServiceDetails(
    addr="10.71.207.150", username="vrf4_sg3", password="Haz4_vrf_sg3"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.245",
    iperf_path="/cygdrive/c/iperf",
    port="53344",
)

_iperf_details_on_appserver2 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.245",
    iperf_path="iperf",
    port="53444",
)

_iperf_details_on_appserver3 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh1,
    network_interface_address="10.71.207.150",
    iperf_path="iperf",
    port="53344",
)

_appserver = AppServer(_iperf_details_on_appserver2)

# CI_Detail_UE_Type='Huawei_5G_Mate_30_Pro'
_android_5 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.59", username="mn5gran", password="nokia123@"
    ),
    serial_number="9YS0219C10006912",
    imsi="001010100008830",
    sec_key="13100008830",
    server_dir="C:\Program Files (x86)\DingLi\Pilot Pioneer10.5.9.28---09171441\Pioneer.exe",
    python_path="C:/Python27/python.exe",
    qcat_path="",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["Huawei", "REAL_ANDROID_UE"],
    mobile_network_text="172.249.48.156",
)

_android_6 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.59", username="mn5gran", password="nokia123@"
    ),
    serial_number="9YS0220B11000033",
    imsi="001010032993994",
    sec_key="18032993994",
    server_dir="C:\Program Files (x86)\DingLi\Pilot Pioneer10.5.9.28---09171441\Pioneer.exe",
    python_path="C:/Python27/python.exe",
    qcat_path="",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["Huawei", "REAL_ANDROID_UE"],
    mobile_network_text="172.249.48.159",
)

_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.59", username="mn5gran", password="nokia123@"
    ),
    serial_number="9YS0220624013834",
    imsi="001018001006254",
    sec_key="18001006254",
    server_dir="C:\Program Files (x86)\DingLi\Pilot Pioneer10.5.9.28---09171441\Pioneer.exe",
    python_path="C:/Python27/python.exe",
    qcat_path="",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["Huawei", "REAL_ANDROID_UE"],
)

_android_1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.59", username="mn5gran", password="nokia123@"
    ),
    serial_number="9YS5T19C09008584",
    imsi="001018001006429",
    sec_key="18001006429",
    server_dir="C:\Program Files (x86)\DingLi\Pilot Pioneer10.5.9.28---09171441\Pioneer.exe",
    python_path="C:/Python27/python.exe",
    qcat_path="",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["Huawei", "REAL_ANDROID_UE"],
)

_android_2 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.57", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="RFCR10CV12Z",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["samsung", "samsung22"],
)

_android_3 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.59", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="9YS5T19C09008584",
    server_dir="C:\Program Files (x86)\DingLi\Pilot Pioneer10.5.9.28---09171441\Pioneer.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf_details_on_appserver3,
)

_android_4 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.44", username="mn5gran", password="nokia123@"
    ),
    serial_number="9YS0220103031558",
    imsi="001010100010897",
    sec_key="13100010897",
    server_dir="C:\Program Files (x86)\DingLi\Pilot Pioneer10.5.9.28---09171441\Pioneer.exe",
    python_path="C:/Python27/python.exe",
    qcat_path="",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["Huawei", "REAL_ANDROID_UE"],
)

_mtk_host_ssh = SshServiceDetails(
    addr="10.57.130.59", username="MN5GRAN", password="nokia123@"
)

_iperf_details_on_appserver_for_caymus_ul = IperfDataTransferDetails(
    ssh_connection_details=_mtk_host_ssh,
    network_interface_address='10.57.150.4',
    iperf_path='/usr/bin/iperf',
    port=54344,
    ports=[54344, 54009, 54006, 54007])

_appserver_for_caymus_ul = AppServer(_iperf_details_on_appserver_for_caymus_ul)

_iperf_details_on_mtk = IperfDataTransferDetails(
    ssh_connection_details=_mtk_host_ssh,
    network_interface_address="",
    iperf_path="/usr/bin/iperf",
    port=53344,
)
_mtk_pdu = FACOM(addr="10.57.151.19", port_numbers=[2]).pdu_ports[2]
_elt_path = "/cygdrive/c/tool/ELT_32"

_mtk_ue_box = MediaTek(
    ssh_connection_details=_mtk_host_ssh,
    server_dir="c:/pyro_server",
    server_port=8080,
    edb_file_path="C:/tool/MTK_M60_Redcap/MDDB_MT6815_S00_NR17R.R1.TC42.SP.W24.49.p2.EDB",
    log_filter='2.Gen99_Default_Standard',
    imei="012345678901234",
    imsi="001013100011544",
    apn_url="dxdata2",
    iperf_details=_iperf_details_on_mtk,
    capabilities=["REAL_MEDIATEK_UE", "mtk"],
    serial_number="0123456789ABCDEF",
)

_mtk_ue_box.pdu = _mtk_pdu
_mtk_ue_box.elt_path = _elt_path

# #RealEnb
_real_enb_pdu0 = FACOM(addr="10.57.241.219", port_numbers=[2])

_common_unit_0 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.225.230", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu0.pdu_ports[2],
)

_real_enb0 = Airscale(common_units=[_common_unit_0])

_lte_real_enb0 = RealEnb(airscale=_real_enb0, instance_id=5294)

# #attenuator
_hbte_params = {
    "ip_addr": "10.57.151.11",
    "port": 5000,
    "attenuation_port_numbers": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    "model": "PA-16-16-6-127-0.5-B-S",
    "version": None,
}
_attenuator = HBTE(**_hbte_params)

_attenuator2 = TopYoung(
    ip_addr="10.57.246.249",
    port=3000,
    attenuation_port_numbers=[11],
    model="TAS16T16-51-120-1SDES",
)

_hbte_params3 = {
    "ip_addr": "10.57.152.220",
    "port": 5000,
    "attenuation_port_numbers": [1, 2, 9, 10],
    "model": "PA-8-2-6-127-0.5-B-S",
    "version": None,
}
_attenuator3 = HBTE(**_hbte_params3)


_hbte_params4 = {
    "ip_addr": "10.57.249.106",
    "port": 5000,
    "attenuation_port_numbers": [14, 15],
    "model": "PA-8-2-6-127-0.5-B-S",
    "version": None,
}
_attenuator4 = HBTE(**_hbte_params4)

_ru1_pdu = FACOM(addr="10.57.241.218", port_numbers=[6])
_ru2_pdu = FACOM(addr="10.57.241.218", port_numbers=[4])
_ru3_pdu = FACOM(addr="10.57.241.219", port_numbers=[6])

_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.55", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.55", username="root", password="umniedziala"
    ),
    pdu_port=_ru1_pdu.pdu_ports[6],
    radio_type=RadioTypes.AEQC,
    signal_analyzer=None,
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[13],
        _attenuator.attenuator_ports[14],
    ],
)
_ru2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.55", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.55", username="root", password="umniedziala"
    ),
    pdu_port=_ru2_pdu.pdu_ports[4],
    radio_type=RadioTypes.AEQC,
    signal_analyzer=None,
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[13],
        _attenuator.attenuator_ports[14],
    ],)

_ru3 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.55", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.55", username="root", password="umniedziala"
    ),
    pdu_port=_ru3_pdu.pdu_ports[6],
    radio_type=RadioTypes.AHIB,
    signal_analyzer=None,
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[13],
        _attenuator.attenuator_ports[14],
    ],)

_ru4 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.55", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.55", username="root", password="umniedziala"
    ),
    pdu_port=_ru3_pdu.pdu_ports[6],
    radio_type=RadioTypes.AHIB,
    signal_analyzer=None,
    attenuation_ports=[
        _attenuator.attenuator_ports[6],
        _attenuator.attenuator_ports[8],
        _attenuator.attenuator_ports[10],
        _attenuator.attenuator_ports[12],
    ],)

_lmp_connection = SshServiceDetails(
    addr="10.57.225.227", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.33")

_gnb_pdu = FACOM(addr="10.57.241.219", port_numbers=[2])

_gnb_pdu2 = FACOM(addr="10.57.241.219", port_numbers=[1])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[2],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(
    airscale=_airscale,
    rus=[_ru1, _ru2, _ru3, _ru4],
    f1_m_ip_addr="10.57.225.227",
    f1_c_ip_addr="10.57.225.227",
    f1_u_ip_addr="10.57.225.227",
)

_f1m = NetworkAddress(v6="fd5f:4268:2387:a881:40:43ff:fe80:101")

# #CU
_cu = CU(
    backhaul_site_oam_ip="10.57.225.227",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.225.227", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.225.227", username="Nemuadmin", password="nemuuser"
    ),
    f1m=_f1m,
)

_lmp_connection1 = SshServiceDetails(
    addr="10.57.225.228", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit1 = CapacityUnit(addr="192.168.253.20")

_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection1,
    capacity_units=[_capacity_unit1],
    pdu_port=_gnb_pdu2.pdu_ports[1],
)

_airscale1 = Airscale(common_units=[_common_unit_1])

_du1 = DU(
    airscale=_airscale1,
    rus=[_ru1, _ru2],
    f1_m_ip_addr="10.57.225.228",
    f1_c_ip_addr="10.57.225.228",
    f1_u_ip_addr="10.57.225.228",
)


_f1m2 = NetworkAddress(v6="fd5f:4268:2387:a881:40:43ff:fe80:101")
_cu1 = CU(
    backhaul_site_oam_ip="10.57.225.228",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.225.228", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.225.228", username="Nemuadmin", password="nemuuser"
    ),
    f1m=_f1m2,
)

_classical_bts0 = ClassicalBts(dus=[_du], cu=_cu, instance_id=34411, global_bts_id=34411)

_classical_bts1 = ClassicalBts(dus=[_du1], cu=_cu1, instance_id=34412, global_bts_id=34412)

_tl_cloud_topology = "CLOUD_5G_BB3"

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts0, _classical_bts1],
    core=_realcore,
    enbs=[_lte_real_enb0],
    ues=[_android_5, _android_1, _android_6, _android_2, _android_3, _android_4, _android, _mtk_ue_box],
    appserver=_appserver,
    attenuator=[_attenuator, _attenuator2, _attenuator3, _attenuator4],
    tl_cloud_topology=_tl_cloud_topology,
    appservers=[_appserver, _appserver_for_caymus_ul],
)
