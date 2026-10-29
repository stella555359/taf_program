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
from taf.config.testline.core import EPCSim, LTEEmuCore, PrismaCore, RealCore, RealCore5GDetails, AMF, PCF
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
from taf.config.testline.attenuator import (
    AttenuationPort,
    TopYoung,
    HBTE,
)  # added in taf.meta 5.4
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
from taf.config.testline.pdn import PDN, PDPTypes

__maintainer__ = "Liu Jia."
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_3_GMS <I_MN_5G_RAN_IV4_LINE_HZG_3@internal.nsn.com>"
)
__email__ = "jia-rebecca.liu@nokia-sbell.com"

__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.36", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# realcore
_amf_ssh = SshServiceDetails(
    addr="to_be_updated", username="to_be_updated", password="to_be_updated"
)

_amf_n2_addr = NetworkAddress(v4="10.110.133.68", v6="to_be_updated", vlan_id=None)

_amf = AMF(oam_ssh_connection_details=_amf_ssh, n2=_amf_n2_addr)

_pcf_ssh = SshServiceDetails(
    addr="10.57.150.82", username="ute", password="Ut3pa5s#ff97"
)

_pcf = PCF(oam_ssh_connection_details=_pcf_ssh)



_epc_sim0 = EPCSim(
    mme_ip="10.110.227.5",
    mcc="460",
    mnc="02",
    tac="210",
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.36", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    edaemon_port=10000,
    egate_port=20000,
    dir_path="/opt/iphy/WTS_7577/",
    cfg_filename="1927_Samsung_MDRB.cfg",
)

_epc_sim1 = EPCSim(
    mme_ip="10.110.227.5",
    mcc="460",
    mnc="02",
    tac="210",
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.36", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    edaemon_port=10000,
    egate_port=20000,
    dir_path="/opt/iphy/WTS_7577/",
    cfg_filename="1927_Samsung_MDRB.cfg",
)

_appserver_ssh = SshServiceDetails(
    addr="10.57.191.245",
    username="vrf4_sg3",
    password="Haz4_vrf_sg3",
    port="53167",
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.245",
    iperf_path="/cygdrive/c/iperf",
    port="53267",
)

_iperf_details_on_appserver2 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.245",
    iperf_path="iperf",
    port="53367",
)
_appserver = AppServer(_iperf_details_on_appserver2)
_android_0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.204", username="mn5gran", password="nokia123@"
    ),
    serial_number="9YS0219C07033999",
    server_dir="C:\Program Files (x86)\DingLi\Pilot Pioneer10.4.9.113---01111615\Pioneer.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "huawei"],
    imsi="460028001006408",
    sec_key="18001006408",
    pdn=["wap2.nokia.com", "zmdrb.nokia.com", "zwap1.nokia.com", "zzmdrbxj.nokia.com", "zzzmdrb1",
         "zzmdrb2.nokia.com", "zmdrb2.nokia.com", "zzmdrb1.nokia.com"],
)

_android_1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.204", username="mn5gran", password="nokia123@"
    ),
    serial_number="QKX4C20428009127",
    server_dir="C:\Program Files (x86)\DingLi\Pilot Pioneer10.4.9.113---01111615\Pioneer.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "huawei"],
    imsi="001018001006377",
    sec_key="18001006377",
)

_android_2 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.205", username="mn5gran", password="nokia123@"
    ),
    serial_number="54f1d86c",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Users/mn5gran/AppData/Local/Programs/Python/Python38/python.exe",
    iperf_details=_iperf,
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    # python_path="C:/Python27",
    capabilities=["qct_dx50", "REAL_ANDROID_UE", "qct_dx50"],
    imsi="310260100008779",
    sec_key="13100008779",
)

_real_enb_pdu = FACOM(
    addr="10.57.246.59", port_numbers=[7], model="111", version="1.1.1"
)

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.226.4", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[7],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=None, instance_id=36721)

# attenuator
_hbte_params = {
    "ip_addr": "10.57.239.138",
    "port": 5000,
    "attenuation_port_numbers": [1, 2, 3, 4, 5, 6, 7, 8],
    "model": "PA-16-16-6-127-0.5-B-S",
    "version": None,
}
_attenuator = HBTE(**_hbte_params)

_ru1_pdu = FACOM(addr="10.57.176.42", port_numbers=[1])
_ru2_pdu = FACOM(addr="10.57.176.19", port_numbers=[1])
_ru3_pdu = FACOM(addr="10.57.176.19", port_numbers=[2])
_ru4_pdu = FACOM(addr="10.57.176.42 ", port_numbers=[1])

_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.34", username="root", password="umniedziala"
    ),
    pdu_port=_ru1_pdu.pdu_ports[1],
    radio_type=RadioTypes.AZQL,
    signal_analyzer=None,
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
    ],
    serial_number="6Q184919888",
)

_ru2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.52", username="root", password="umniedziala"
    ),
    pdu_port=_ru2_pdu.pdu_ports[1],
    radio_type=RadioTypes.AWHHH,
    signal_analyzer=None,
    attenuation_ports=[
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
    serial_number="6Q184317341",
)

_ru3 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.52", username="root", password="umniedziala"
    ),
    pdu_port=_ru3_pdu.pdu_ports[2],
    radio_type=RadioTypes.AWHHH,
    signal_analyzer=None,
    attenuation_ports=[
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[6],
    ],
    serial_number="6Q184317341",
)

#LTE RU
_ru4 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.52", username="root", password="umniedziala"
    ),
    pdu_port=_ru4_pdu.pdu_ports[1],
    radio_type=RadioTypes.FXEB,
    signal_analyzer=None,
    attenuation_ports=[
        _attenuator.attenuator_ports[7],
        _attenuator.attenuator_ports[8],
    ],
    serial_number="6Q184317341",
)

_lmp_connection = SshServiceDetails(
    addr="10.57.226.2", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")

_gnb_pdu = FACOM(addr="10.57.241.210", port_numbers=[2])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[2],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(
    airscale=_airscale,
    rus=[_ru1, _ru2, _ru4],
    f1_m_ip_addr="10.57.226.2",
    f1_c_ip_addr="10.57.226.2",
    f1_u_ip_addr="10.57.226.2",
)


_lmp_connection1 = SshServiceDetails(
    addr="10.57.226.3", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit1 = CapacityUnit(addr="192.168.253.20")

_gnb_pdu1 = FACOM(addr="10.57.241.210", port_numbers=[1])

_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection1,
    capacity_units=[_capacity_unit1],
    pdu_port=_gnb_pdu1.pdu_ports[1],
)

_airscale1 = Airscale(common_units=[_common_unit_1])

_du1 = DU(
    airscale=_airscale1,
    rus=[_ru3],
    f1_m_ip_addr="10.57.226.3",
    f1_c_ip_addr="10.57.226.3",
    f1_u_ip_addr="10.57.226.3",
)


_cu = CU(
    backhaul_site_oam_ip="10.57.226.2",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.226.2", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.226.2", username="Nemuadmin", password="nemuuser"
    ),
)

_cu1 = CU(
    backhaul_site_oam_ip="10.57.226.3",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.226.3", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.226.3", username="Nemuadmin", password="nemuuser"
    ),
)

_classical_bts0 = ClassicalBts(dus=[_du], cu=_cu, instance_id=1061, global_bts_id=1061)

_classical_bts1 = ClassicalBts(
    dus=[_du1], cu=_cu1, instance_id=1040, global_bts_id=1040
)

_tl_cloud_topology = "CLOUD_5G_BB3"

_pdns = [PDN(PDPTypes.IP.value, 'wap2.nokia.com'), PDN(PDPTypes.IP.value, 'zmdrb.nokia.com'),
         PDN(PDPTypes.IP.value, 'zwap1.nokia.com'), PDN(PDPTypes.IP.value, 'zzmdrbxj.nokia.com'), PDN(PDPTypes.IP.value, 'zzzmdrb1')]

# _core = RealCore(five_g=RealCore5GDetails(amf=_amf), mcc=310, mnc=260, pcf=_pcf)
_core = RealCore(four_g=None, five_g=None, mcc="460", mnc="02", pdns=_pdns)

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts0, _classical_bts1],
    # core=[_epc_sim0, _epc_sim1, _core],
    core=_core,
    enbs=[_lte_real_enb],
    ues=[_android_0, _android_1, _android_2],
    appserver=_appserver,
    attenuator=[_attenuator],
    tl_cloud_topology=_tl_cloud_topology,
)
