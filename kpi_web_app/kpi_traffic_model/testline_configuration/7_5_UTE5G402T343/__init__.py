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

__maintainer__ = "Zhang Yayun"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_3_GMS <I_MN_5G_RAN_IV4_LINE_HZG_3@internal.nsn.com>"
)
__email__ = "yayun.zhang@nokia-sbell.com"

__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.132", username="ute", password="iW_K#8.ute%A10h0m0ra"
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

# realcore
# _amf_ssh = SshServiceDetails(
#     addr="to_be_updated", username="to_be_updated", password="to_be_updated"
# )
#
# _amf_n2_addr = NetworkAddress(v4="10.110.133.68", v6="to_be_updated", vlan_id=None)
#
# _amf = AMF(oam_ssh_connection_details=_amf_ssh, n2=_amf_n2_addr)
#
# _pcf_ssh = SshServiceDetails(
#     addr="10.57.150.82", username="ute", password="Ut3pa5s#ff97"
# )
#
# _pcf = PCF(oam_ssh_connection_details=_pcf_ssh)

# _core = RealCore(five_g=RealCore5GDetails(amf=_amf), mcc=310, mnc=260, pcf=_pcf)
#
# _epc_sim0 = EPCSim(
#     mme_ip="10.110.227.5",
#     mcc="460",
#     mnc="02",
#     tac="270",
#     default_ssh_connection_details=SshServiceDetails(
#         addr="10.57.157.132", username="ute", password="iW_K#8.ute%A10h0m0ra"
#     ),
#     edaemon_port=10000,
#     egate_port=20000,
#     dir_path="/opt/iphy/WTS_7577/",
#     cfg_filename="1927_Samsung_MDRB.cfg",
# )
#
# _epc_sim1 = EPCSim(
#     mme_ip="10.110.227.5",
#     mcc="460",
#     mnc="02",
#     tac="270",
#     default_ssh_connection_details=SshServiceDetails(
#         addr="10.57.157.132", username="ute", password="iW_K#8.ute%A10h0m0ra"
#     ),
#     edaemon_port=10000,
#     egate_port=20000,
#     dir_path="/opt/iphy/WTS_7577/",
#     cfg_filename="1927_Samsung_MDRB.cfg",
# )

_appserver_ssh = SshServiceDetails(
    addr="10.57.163.50",
    username="cmw_sg3",
    password="iW_K#8.ute%A10h0m0ra",
    port="53443",
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.163.50",
    iperf_path="/cygdrive/c/iperf",
    port="53343",
)

_iperf_details_on_appserver2 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.163.50",
    iperf_path="iperf",
    port="53443",
)
_appserver = AppServer(_iperf_details_on_appserver2)

# CI_Detail_UE_Type='MTK'
_mtk_host_ssh = SshServiceDetails(
    addr="10.57.150.126", username="mn5gran", password="nokia123@"
)

_iperf_details_on_appserver_for_caymus_ul = IperfDataTransferDetails(
    ssh_connection_details=_mtk_host_ssh,
    network_interface_address='10.57.150.126',
    iperf_path='/usr/bin/iperf',
    port=54343,
    ports=[53343, 53443, 53543, 53643])

_appserver_for_caymus_ul = AppServer(_iperf_details_on_appserver_for_caymus_ul)

_iperf_details_on_mtk = IperfDataTransferDetails(
    ssh_connection_details=_mtk_host_ssh,
    network_interface_address="",
    iperf_path="/usr/bin/iperf",
    port=53343,
)
# _mtk_pdu = FACOM(addr="10.57.151.19", port_numbers=[2]).pdu_ports[5]
_elt_path = "C:\tool\ELT_exe_v3.2416.0_customer_x64"

_mtk_ue_box = MediaTek(
    ssh_connection_details=_mtk_host_ssh,
    server_dir="c:/pyro_server",
    server_port=8080,
    edb_file_path="auto",
    log_filter='2.Gen98_Default_Standard',
    imei="0123456789ABCDEF",
    imsi="001013100011544",
    apn_url="dxdata2",
    iperf_details=_iperf_details_on_mtk,
    capabilities=["mtk", "huawei"],
    serial_number="0123456789ABCDEF",
)

# _mtk_ue_box.pdu = _mtk_pdu
_mtk_ue_box.elt_path = _elt_path
# attenuator
_hbte_params = {
    "ip_addr": "10.57.239.139",
    "port": 5000,
    "attenuation_port_numbers": [1, 2, 3, 4, 5, 6, 7, 8],
    "model": "PA-16-16-6-127-0.5-B-S",
    "version": None,
}

_attenuator = HBTE(**_hbte_params)

_ru1_pdu = FACOM(addr="10.57.176.42", port_numbers=[3])
_ru2_pdu = FACOM(addr="10.57.241.217", port_numbers=[5])

_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.84", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.84", username="root", password="umniedziala"
    ),
    pdu_port=_ru1_pdu.pdu_ports[3],
    radio_type=RadioTypes.AEQV,
    signal_analyzer=None,
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
    serial_number="1M211808426",
)

_ru2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.52", username="root", password="umniedziala"
    ),
    pdu_port=_ru2_pdu.pdu_ports[5],
    radio_type=RadioTypes.AHEGA,
    signal_analyzer=None,
    attenuation_ports=[
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[6],
        _attenuator.attenuator_ports[7],
        _attenuator.attenuator_ports[8],
    ],
    serial_number="	EA205152439",
)

_lmp_connection = SshServiceDetails(
    addr="10.57.226.8", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")

_gnb_pdu = FACOM(addr="10.57.241.215", port_numbers=[1])

_common_unit = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[1],
)

_airscale = Airscale(common_units=[_common_unit])

_du = DU(
    airscale=_airscale,
    rus=[_ru1, _ru2],
    f1_m_ip_addr="10.57.226.8",
    f1_c_ip_addr="10.57.226.8",
    f1_u_ip_addr="10.57.226.8",
)

_f1m = NetworkAddress(v6="2a00:8a00:8000:136:10:57:227:11")

_cu = CU(
    backhaul_site_oam_ip="10.57.226.8",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.226.8", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.226.8", username="Nemuadmin", password="nemuuser"
    ),
)

_classical_bts0 = ClassicalBts(dus=[_du], cu=_cu, instance_id=34311)


_tl_cloud_topology = "CLOUD_5G_BB3"

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts0],
    core=_realcore,
    ues=[_mtk_ue_box, _mtk_ue_box],
    appserver=_appserver,
    attenuator=[_attenuator],
    tl_cloud_topology=_tl_cloud_topology,
)
