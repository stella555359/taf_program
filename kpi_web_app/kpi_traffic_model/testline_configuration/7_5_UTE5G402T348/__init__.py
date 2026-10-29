import os
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
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.appserver import AppServer
from taf.config.testline.pdn import PDN, PDPTypes

__maintainer__ = "Ming Shi"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_3_GMS <I_MN_5G_RAN_IV4_LINE_HZG_3@internal.nsn.com>"
)
__email__ = "ming.shi@nokia-sbell.com"

__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.195.130", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_appserver_ssh = SshServiceDetails(
    addr="10.57.191.245",
    username="vrf4_sg3",
    password="Haz4_vrf_sg3",
    port="53348",
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.245",
    iperf_path="/cygdrive/c/iperf",
    port="53448",
)

_appserver = AppServer(_iperf)

_appserver_ssh2 = SshServiceDetails(
    addr="10.57.191.245",
    username="vrf4_sg3",
    password="Haz4_vrf_sg3",
    port="53348",
)

_iperf2 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh2,
    network_interface_address="10.57.191.245",
    iperf_path="/cygdrive/c/iperf",
    port="53448",
)

_appserver2 = AppServer(_iperf2)

# CI_Detail_UE_Type='Huawei Honor 30s'
_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.216", username="mn5gran", password="nokia123@"
    ),
    serial_number="RFCW32AYMQJ",
    server_dir="C:\Program Files (x86)\DingLi\Pilot Pioneer10.5.0.57---08191556\Pioneer.exe",
    python_path="C:/Python37/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung", "samsung"],
    imsi="310260100010822",
    sec_key="13100010822",
)

# # #MTK
# _ue_host_ssh = SshServiceDetails(
#     addr="10.57.150.216", username="mn5gran", password="nokia123@"
# )

# # CI_Detail_UE_Type='MTK phoneB'
# _mtk = MediaTek(
#     ssh_connection_details=_ue_host_ssh,
#     server_dir="c:/pyro_server",
#     server_port=8080,
#     edb_file_path="auto",
#     log_filter="2.Gen98_Default_Standard",
#     imei="0123456789ABCDEF",
#     imsi="310260100011554",
#     apn_url="dxdata2",
#     iperf_details=_iperf2,
#     capabilities=["REAL_MEDIATEK_UE", "mtk"],
#     serial_number="0123456789ABCDEF",
# )

_android_2 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.216", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="b1ca5adf",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Users/mn5gran/AppData/Local/Programs/Python/Python37/python.exe",
    iperf_details=_iperf,
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    capabilities=["qct_dx50", "REAL_ANDROID_UE", "qct_dx50"],
    imsi="310260100011554",
    sec_key="13100011554",
    pdn=["dxdata2", "mdrb.nokia.com", "mdrb1.nokia.com"],
)

_android_3 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.205", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="a5ea9ca",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Users/mn5gran/AppData/Local/Programs/Python/Python38/python.exe",
    iperf_details=_iperf,
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    capabilities=["qct_dx50", "REAL_ANDROID_UE", "qualcomm"],
    imsi="310260100026807",
    sec_key="13100026807",
    pdn=["dxdata2", "mdrb.nokia.com", "mdrb1.nokia.com"],
)

_real_enb_pdu = FACOM(
    addr="10.57.176.166", port_numbers=[2], model="111", version="1.1.1"
)

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.227.140", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[2],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=None, instance_id=34821)

_pdns = [PDN(PDPTypes.IP.value, 'dxdata2'), PDN(PDPTypes.IP.value, 'mdrb.nokia.com'),
         PDN(PDPTypes.IP.value, 'mdrb1.nokia.com')]

# #Real Core
_realcore = RealCore(four_g=None, five_g=None, mcc="310", mnc="260", pdns=_pdns)

# #attenuator
_hbte_params = {
    "ip_addr": "10.57.230.76",
    "port": 5000,
    "attenuation_port_numbers": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    "model": "PA-16-16-6-127-0.5-B-S",
    "version": None,
}
_attenuator = HBTE(**_hbte_params)

_hbte_params2 = {
    "ip_addr": "10.57.230.71",
    "port": 5000,
    "attenuation_port_numbers": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    "model": "PA-16-16-6-127-0.5-B-S",
    "version": None,
}
_attenuator2 = HBTE(**_hbte_params2)

_ru1_pdu = FACOM(addr="10.57.176.152", port_numbers=[3])
_ru2_pdu = FACOM(addr="10.57.176.151", port_numbers=[3])
_ru3_pdu = FACOM(addr="10.57.176.151", port_numbers=[5])
_ru4_pdu = FACOM(addr="10.57.176.151", port_numbers=[6])
_ru5_pdu = FACOM(addr="10.57.176.152", port_numbers=[6])
_ru6_pdu = FACOM(addr="10.57.176.152", port_numbers=[1])

_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="root", password=""
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.52", username="root", password=""
    ),
    pdu_port=_ru1_pdu.pdu_ports[3],
    radio_type=RadioTypes.AHLOA,
    signal_analyzer=None,
    serial_number="K9183920824",
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
)

_ru2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.57", username="root", password=""
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.57", username="root", password=""
    ),
    pdu_port=_ru2_pdu.pdu_ports[3],
    radio_type=RadioTypes.AHLOA,
    signal_analyzer=None,
    serial_number="BL2032G1GMR",
    attenuation_ports=[
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[6],
        _attenuator.attenuator_ports[7],
        _attenuator.attenuator_ports[8],
    ],
)

_ru3 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.84", username="root", password=""
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.84", username="root", password=""
    ),
    pdu_port=_ru3_pdu.pdu_ports[5],
    radio_type=RadioTypes.AHFIB,
    signal_analyzer=None,
    serial_number="BL2215V011E",
    attenuation_ports=[
        _attenuator.attenuator_ports[9],
        _attenuator.attenuator_ports[10],
        _attenuator.attenuator_ports[11],
        _attenuator.attenuator_ports[12],
    ],
)

_ru4 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.57", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.57", username="root", password="umniedziala"
    ),
    pdu_port=_ru4_pdu.pdu_ports[6],
    radio_type=RadioTypes.AHFIB,
    signal_analyzer=None,
    serial_number="BL1945V00IK",
    attenuation_ports=[
        _attenuator.attenuator_ports[13],
        _attenuator.attenuator_ports[14],
        _attenuator.attenuator_ports[15],
        _attenuator.attenuator_ports[16],
    ],
)

_ru5 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.84", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.84", username="root", password="umniedziala"
    ),
    pdu_port=_ru5_pdu.pdu_ports[6],
    radio_type=RadioTypes.AVHA,
    signal_analyzer=None,
    serial_number="L1251101918",
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
)

_ru6 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.84", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.84", username="root", password="umniedziala"
    ),
    pdu_port=_ru6_pdu.pdu_ports[1],
    radio_type=RadioTypes.AHLOB,
    signal_analyzer=None,
    serial_number="BL2243D50WN",
    attenuation_ports=[
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[6],
        _attenuator.attenuator_ports[7],
        _attenuator.attenuator_ports[8],
    ],
)

_lmp_connection = SshServiceDetails(
    addr="10.57.227.139", username="toor4nsn", password="oZPS0POrRieRtu"
)

_lmp_connection1 = SshServiceDetails(
    addr="10.57.227.138", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")
_capacity_unit1 = CapacityUnit(addr="192.168.253.24")
_capacity_unit2 = CapacityUnit(addr="192.168.253.28")
_capacity_unit3 = CapacityUnit(addr="192.168.253.26")

_gnb_pdu = FACOM(addr="10.57.176.166", port_numbers=[2])

_gnb_pdu1 = FACOM(addr="10.57.176.166", port_numbers=[1])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit, _capacity_unit1, _capacity_unit2],
    pdu_port=_gnb_pdu.pdu_ports[2],
)

_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection1,
    capacity_units=[_capacity_unit3],
    pdu_port=_gnb_pdu1.pdu_ports[1],
)

_airscale = Airscale(common_units=[_common_unit_0])

_airscale1 = Airscale(common_units=[_common_unit_1])

_du = DU(
    airscale=_airscale,
    rus=[_ru1, _ru2, _ru3, _ru4, _ru5],
    f1_m_ip_addr="10.57.227.139",
    f1_c_ip_addr="10.57.227.139",
    f1_u_ip_addr="10.57.227.139",
)

_du1 = DU(
    airscale=_airscale1,
    rus=[_ru6],
    f1_m_ip_addr="10.57.227.138",
    f1_c_ip_addr="10.57.227.138",
    f1_u_ip_addr="10.57.227.138",
)

_cu = CU(
    backhaul_site_oam_ip="10.57.227.139",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.227.139", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.227.139", username="Nemuadmin", password="nemuuser"
    ),
)

_cu1 = CU(
    backhaul_site_oam_ip="10.57.227.138",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.227.138", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.227.138", username="Nemuadmin", password="nemuuser"
    ),
)

_classical_bts0 = ClassicalBts(dus=[_du], cu=_cu, instance_id=34811, global_bts_id=3481100000)

_classical_bts1 = ClassicalBts(
    dus=[_du1], cu=_cu1, instance_id=34812, global_bts_id=34812
)

_tl_cloud_topology = "CLOUD_5G_BB3"

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts0, _classical_bts1],
    core=_realcore,
    enbs=[_lte_real_enb],
    # ues=[_android,_mtk],
    ues=[_android, _android_2, _android_3],
    appserver=_appserver,
    attenuator=[_attenuator, _attenuator2],
    tl_cloud_topology=_tl_cloud_topology,
)
