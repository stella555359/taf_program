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

__maintainer__ = "Huang Hai"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_3_GMS <I_MN_5G_RAN_IV4_LINE_HZG_3@internal.nsn.com>"
)
__email__ = "hai.2.huang@nokia-sbell.com"

__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.101.60.12", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_epc_sim = EPCSim(
    mme_ip="10.110.227.5",
    mcc="460",
    mnc="02",
    tac="210",
    default_ssh_connection_details=SshServiceDetails(
        addr="10.110.227.70", username="test", password="NOKIA123"
    ),
    edaemon_port=10000,
    egate_port=20000,
    dir_path="/opt/iphy/WTS_7577/",
    cfg_filename="1927_Samsung_MDRB.cfg",
)

_appserver_ssh = SshServiceDetails(
    addr="10.57.163.50", username="cmw_sg3", password="cmw_sg3", port="53389"
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.163.50",
    iperf_path="/cygdrive/c/iperf",
    port="53989",
)

_iperf_details_on_appserver2 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.163.50",
    iperf_path="iperf",
    port="53389",
)
_appserver = AppServer(_iperf_details_on_appserver2)

# CI_Detail_UE_Type='Huawei_Mate_30_Pro_5G'
_android_0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.214", username="nokia5G", password="noki@123"
    ),
    serial_number="9YS0220114010442",
    server_dir="C:\Program Files (x86)\DingLi\Pilot Pioneer10.4.9.113---01111615\Pioneer.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    capabilities=["REAL_UE", "REAL_ANDROID_UE"],
    imsi="460023100007887",
    sec_key="13100007887",
)

_android_1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.77 ", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="QKX4C20616003404",
    server_dir="C:\Program Files (x86)\DingLi\Pilot Pioneer10.4.9.113---01111615\Pioneer.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    capabilities=["REAL_UE", "REAL_ANDROID_UE"],
    imsi="001013032996643",
    sec_key="13032996643",
)

_real_enb_pdu = FACOM(
    addr="10.57.255.255", port_numbers=[4], model="111", version="1.1.1"
)

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.227.18", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[4],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=None, instance_id=38221)

# #5GRU for classicalBTS
# #attenuator
_hbte_params = {
    "ip_addr": "10.57.x.x",
    "port": 5000,
    "attenuation_port_numbers": [9, 10, 11, 12, 15],
    "model": "PA-16-16-6-127-0.5-B-S",
    "version": None,
}
_attenuator = HBTE(**_hbte_params)

_ru1_pdu = FACOM(addr="10.57.249.86", port_numbers=[1])
_ru2_pdu = FACOM(addr="10.57.249.86", port_numbers=[3])
_ru3_pdu = FACOM(addr="10.57.249.86", port_numbers=[2])
_ru4_pdu = FACOM(addr="10.57.249.86", port_numbers=[3])

_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.34", username="root", password="umniedziala"
    ),
    pdu_port=_ru1_pdu.pdu_ports[1],
    radio_type=RadioTypes.AEQI,
    signal_analyzer=None,
    attenuation_ports=[
        _attenuator.attenuator_ports[9],
        _attenuator.attenuator_ports[10],
    ],
)

_ru2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.84", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.84", username="root", password="umniedziala"
    ),
    pdu_port=_ru2_pdu.pdu_ports[3],
    radio_type=RadioTypes.AEQZ,
    signal_analyzer=None,
    attenuation_ports=[_attenuator.attenuator_ports[11]],
)


_ru4 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.143", username="root", password="nokia123"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.155.143", username="root", password="nokia123"
    ),
    pdu_port=_ru4_pdu.pdu_ports[3],
    radio_type=RadioTypes.AEQQ,
    signal_analyzer=None,
    # attenuation_ports=[_attenuator.attenuator_ports[2], _attenuator.attenuator_ports[2]]
)

_ru3 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.34", username="root", password="umniedziala"
    ),
    pdu_port=_ru3_pdu.pdu_ports[2],
    radio_type=RadioTypes.AEQI,
    signal_analyzer=None,
    attenuation_ports=[_attenuator.attenuator_ports[12]],
)


_lmp_connection = SshServiceDetails(
    addr="10.57.225.242", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")

_gnb_pdu = FACOM(addr="10.57.242.142", port_numbers=[8])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[8],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(
    airscale=_airscale,
    rus=[_ru1, _ru3, _ru4],
    f1_m_ip_addr="10.57.225.242",
    f1_c_ip_addr="10.57.225.242",
    f1_u_ip_addr="10.57.225.242",
)


_lmp_connection1 = SshServiceDetails(
    addr="10.57.225.243", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit1 = CapacityUnit(addr="192.168.253.20")

_gnb_pdu1 = FACOM(addr="10.57.240.148", port_numbers=[3])

_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection1,
    capacity_units=[_capacity_unit1],
    pdu_port=_gnb_pdu1.pdu_ports[3],
)

_airscale1 = Airscale(common_units=[_common_unit_1])

_du1 = DU(
    airscale=_airscale1,
    rus=[_ru2],
    f1_m_ip_addr="10.57.225.243",
    f1_c_ip_addr="10.57.225.243",
    f1_u_ip_addr="10.57.225.243",
)

_cu = CU(
    backhaul_site_oam_ip="10.57.225.242",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.225.242", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.225.242", username="Nemuadmin", password="nemuuser"
    ),
)

_cu1 = CU(
    backhaul_site_oam_ip="10.57.225.243",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.225.243", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.225.243", username="Nemuadmin", password="nemuuser"
    ),
)

_classical_bts0 = ClassicalBts(dus=[_du], cu=_cu, instance_id=38911)

_classical_bts1 = ClassicalBts(dus=[_du1], cu=_cu1, instance_id=38912)

_tl_cloud_topology = "CLOUD_5G_BB3"

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts0, _classical_bts1],
    core=_epc_sim,
    enbs=[_lte_real_enb],
    ues=[_android_0, _android_1],
    appserver=_appserver,
    attenuator=[_attenuator],
    tl_cloud_topology=_tl_cloud_topology,
)
