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
from taf.config.testline.attenuator import AttenuationPort, TopYoung, HBTE
from taf.config.testline.gnb.networkaddress import NetworkAddress, RoutingInformation
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

__maintainer__ = "jack.zeng"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_3_GMS <I_MN_5G_RAN_IV4_LINE_HZG_3@internal.nsn.com>"
)
__email__ = "jack.zeng@nokia-sbell.com"

__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.120", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_real_enb_pdu0 = FACOM(addr="10.57.241.216", port_numbers=[4])
_common_unit_1 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.232.132", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu0.pdu_ports[4],
)
_real_enb0 = Airscale(common_units=[_common_unit_1])

_lte_real_enb0 = RealEnb(airscale=_real_enb0, instance_id=34121)

_realcore = RealCore(four_g=None, five_g=None, mcc="460", mnc="02", pdns=None)

_appserver_ssh = SshServiceDetails(
    addr="10.57.163.50", username="cmw_sg3", password="iW_K#8.ute%A10h0m0ra"
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.163.50",
    iperf_path="/cygdrive/c/iperf",
    port="53341",
)
_iperf_details_on_appserver2 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.163.50",
    iperf_path="iperf",
    port="53441",
)
_appserver = AppServer(_iperf_details_on_appserver2)

_android_0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.44", username="nokia5G", password="noki@123"
    ),
    serial_number="9YS0220114010442",
    server_dir="C:\Program Files (x86)\DingLi\Pilot Pioneer10.5.9.28---09221723\Pioneer.exe",
    imsi="460028001006149",
    sec_key="18001006149",
    python_path="C:/Python27/python.exe",
    qcat_path="",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["Huawei", "REAL_ANDROID_UE"],
)

_android_1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.44", username="nokia5G", password="noki@123"
    ),
    serial_number="9YS0220624004296",
    server_dir="C:\Program Files (x86)\DingLi\Pilot Pioneer10.5.9.28---09221723\Pioneer.exe",
    imsi="001013100001137",
    sec_key="13100001137",
    python_path="C:/Python27/python.exe",
    qcat_path="",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["Huawei", "REAL_ANDROID_UE"],
)

_android_2 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.162", username="nokia5G", password="noki@123"
    ),
    serial_number="4a38407d",
    server_dir="C:\Program Files (x86)\DingLi\Pilot Pioneer10.5.9.28---09221723\Pioneer.exe",
    imsi="460023100009151",
    sec_key="18001009151",
    python_path="C:/Python27/python.exe",
    qcat_path="",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["xiaomi", "REAL_ANDROID_UE"],
)


_mtk_host_ssh = SshServiceDetails(
    addr="10.57.150.44", username="nokia5G", password="noki@123"
)

_iperf_details_on_mtk = IperfDataTransferDetails(
    ssh_connection_details=_mtk_host_ssh,
    network_interface_address="",
    iperf_path="/cygdrive/c/iperf-2.0.8b-win64/iperf",
    port=52029,
)
_mtk_pdu = FACOM(addr="10.57.151.19", port_numbers=[8]).pdu_ports[8]
_elt_path = "/cygdrive/c/MTK/ELT_exe_v2.1943.0_customer_Gen97_FT"

_mtk_ue_box = MediaTek(
    ssh_connection_details=_mtk_host_ssh,
    server_dir="c:/pyro_server",
    server_port=8080,
    edb_file_path="auto",
    imei="0123456789ABCDEF",
    imsi="460028001006393",
    apn_url="wap1.nokia.com",
    iperf_details=_iperf,
    capabilities=["REAL_MEDIATEK_UE", "mtk"],
    serial_number="0123456789ABCDEF",
)

_mtk_ue_box.pdu = _mtk_pdu
_mtk_ue_box.elt_path = _elt_path

# attenuator

_hbte_params = {
    "ip_addr": "10.57.238.22",
    "port": 5000,
    "attenuation_port_numbers": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    "model": "PA-16-16-6-127-0.5-B-S",
    "version": None,
}
_attenuator = HBTE(**_hbte_params)

_ru1_pdu = FACOM(addr="10.57.241.217", port_numbers=[2])

_ru2_pdu = FACOM(addr="10.57.241.217", port_numbers=[1])

_ru3_pdu = FACOM(addr="10.57.241.217", port_numbers=[5])

_ru4_pdu = FACOM(addr="10.57.241.217", port_numbers=[3])

_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.55", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.55", username="root", password="umniedziala"
    ),
    pdu_port=_ru1_pdu.pdu_ports[2],
    radio_type=RadioTypes.AHPB,
    signal_analyzer=None,
    attenuation_ports=[
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[6],
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
    pdu_port=_ru2_pdu.pdu_ports[1],
    radio_type=RadioTypes.AEQN,
    signal_analyzer=None,
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
    ],
)

_ru3 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.55", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.55", username="root", password="umniedziala"
    ),
    pdu_port=_ru3_pdu.pdu_ports[5],
    radio_type=RadioTypes.AHPB,
    signal_analyzer=None,
    attenuation_ports=[
        _attenuator.attenuator_ports[7],
        _attenuator.attenuator_ports[8],
    ],
)

_ru4 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.55", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.55", username="root", password="umniedziala"
    ),
    pdu_port=_ru4_pdu.pdu_ports[3],
    radio_type=RadioTypes.AEQN,
    signal_analyzer=None,
    attenuation_ports=[
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
)

_lmp_connection = SshServiceDetails(
    addr="10.57.232.148", username="toor4nsn", password="oZPS0POrRieRtu"
)
_lmp_connection2 = SshServiceDetails(
    addr="10.57.232.149", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.33")

_capacity_unit2 = CapacityUnit(addr="192.168.253.33")

_gnb_pdu = FACOM(addr="10.57.241.216", port_numbers=[5])
_gnb_pdu2 = FACOM(addr="10.57.241.216", port_numbers=[5])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[5],
)
_common_unit_2 = CommonUnit(
    lmp_connection=_lmp_connection2,
    capacity_units=[_capacity_unit2],
    pdu_port=_gnb_pdu2.pdu_ports[5],
)

_airscale = Airscale(common_units=[_common_unit_0])

_airscale2 = Airscale(common_units=[_common_unit_2])

_du = DU(
    airscale=_airscale,
    rus=[_ru1, _ru3],
    f1_m_ip_addr="10.57.232.148",
    f1_c_ip_addr="10.57.232.148",
    f1_u_ip_addr="10.57.232.148",
)

_f1m = NetworkAddress(v6="fd5f:4268:2387:a881:40:43ff:fe80:101")
_cu = CU(
    backhaul_site_oam_ip="10.57.232.148",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.232.148", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.232.148", username="Nemuadmin", password="nemuuser"
    ),
    f1m=_f1m,
)

_du2 = DU(
    airscale=_airscale2,
    rus=[_ru2, _ru4],
    f1_m_ip_addr="10.57.232.149",
    f1_c_ip_addr="10.57.232.149",
    f1_u_ip_addr="10.57.232.149",
)

_f1m2 = NetworkAddress(v6="fd5f:4268:2387:a881:40:43ff:fe80:101")
_cu2 = CU(
    backhaul_site_oam_ip="10.57.232.149",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.232.149", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.232.149", username="Nemuadmin", password="nemuuser"
    ),
    f1m=_f1m2,
)


_classical_bts2 = ClassicalBts(dus=[_du], cu=_cu, instance_id=34112)

_classical_bts1 = ClassicalBts(dus=[_du2], cu=_cu2, instance_id=34111)


_tl_cloud_topology = "CLOUD_5G_BB3"

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts1, _classical_bts2],
    enbs=[_lte_real_enb0],
    core=_realcore,
    ues=[_android_0, _android_1, _android_2, _mtk_ue_box],
    attenuator=[_attenuator],
    appserver=_appserver,
    tl_cloud_topology=_tl_cloud_topology,
)
