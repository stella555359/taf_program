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
from taf.config.testline.pdn import PDN, PDPTypes
from taf.config.testline.core import EPCSim, LTEEmuCore, PrismaCore, RealCore
from taf.config.testline.gnb.du import DU
from taf.config.testline.pdu import (
    FACOM,
    PduPort,
    Pdu,
    EPC,
    ATEN,
    RRB,
    APC,
    Gude,
    TopYoung,
)
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
    MediaTek,
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
    #    TopYoung,
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

__maintainer__ = "jack.zeng"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_3_GMS <I_MN_5G_RAN_IV4_LINE_HZG_3@internal.nsn.com>"
)
__email__ = "jack.zeng@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# #host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.150", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_pdns = [
    PDN(pdp_type=PDPTypes.IP.value, apn="dxdata2"),
    PDN(pdp_type=PDPTypes.IP.value, apn="ims"),
    PDN(pdp_type=PDPTypes.IP.value, apn="mdrb1.nokia.com"),
    PDN(pdp_type=PDPTypes.IP.value, apn="mdrb.nokia.com")
]

_realcore = RealCore(
    four_g=None, five_g=None, mcc="460", mnc="02", pdns=_pdns,

)

_appserver_ssh = SshServiceDetails(
    addr="10.57.191.245",
    username="vrf4_sg3",
    password="Haz4_vrf_sg3",
    port="53292",
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.245",
    iperf_path="/cygdrive/c/iperf",
    port="53242",
)

_iperf_details_on_appserver2 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.245",
    iperf_path="iperf",
    port="53292",
)
_appserver = AppServer(_iperf_details_on_appserver2)

# CI_Detail_UE_Type='Huawei_5G_Mate_30_Pro'
_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.46", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="9YS0220227002526",
    imsi="460028001006302",
    sec_key="18001006302",
    server_dir="C:\Program Files (x86)\DingLi\Pilot Pioneer10.5.9.28---01181451\Pioneer.exe",
    python_path="C:/Python27/python.exe",
    qcat_path="",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["Huawei", "REAL_ANDROID_UE"],
)

_android_1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.46", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="9YS5T19C09008603",
    imsi="001013100001043",
    sec_key="13100001043",
    server_dir="C:\Program Files (x86)\DingLi\Pilot Pioneer10.5.9.28---01181451\Pioneer.exe",
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

_mtk_host_ssh = SshServiceDetails(
    addr="10.57.130.57", username="mn5gran", password="nokia123@"
)

_iperf_details_on_appserver_for_caymus_ul=IperfDataTransferDetails(
    ssh_connection_details=_mtk_host_ssh,
    network_interface_address='10.57.130.57',
    iperf_path='/usr/bin/iperf',
    port=54242,
    ports=[54242, 54009, 54006, 54007])

_appserver_for_caymus_ul = AppServer(_iperf_details_on_appserver_for_caymus_ul)

_iperf_details_on_mtk = IperfDataTransferDetails(
    ssh_connection_details=_mtk_host_ssh,
    network_interface_address="",
    iperf_path="/usr/bin/iperf",
    port=53242,
)
_mtk_pdu = FACOM(addr="10.57.151.19", port_numbers=[2]).pdu_ports[2]
_elt_path = "/cygdrive/c/Users/mn5gran/Downloads/ELT_exe_v3.2324.0_customer/ELT_v3.2324.0"

_mtk_ue_box = MediaTek(
    ssh_connection_details=_mtk_host_ssh,
    server_dir="c:/pyro_server",
    server_port=8080,
    edb_file_path="C:/tool/MTK_M60_Redcap/MDDB_MT6815_S00_NR17R.R1.TC42.SP.W23.51.p1.EDB",
    log_filter='2.Gen99_Default_Standard',
    imei="0123456789ABCDEF",
    imsi="460023100012848",
    apn_url="dxdata2",
    iperf_details=_iperf_details_on_mtk,
    capabilities=["REAL_MEDIATEK_UE", "mtk"],
    serial_number="0123456789ABCDEF",
)

_mtk_ue_box.pdu = _mtk_pdu
_mtk_ue_box.elt_path = _elt_path


# #RealEnb
_real_enb_pdu = FACOM(
    addr="10.57.241.219", port_numbers=[3], model="111", version="1.1.1"
)

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.151.243", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[3],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, instance_id=242)

# #5GRU for classicalBTS
# #attenuator
_hbte_params = {
    "ip_addr": "10.57.151.22",
    "port": 5000,
    "attenuation_port_numbers": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    "model": "PA-16-16-6-127-0.5-B-S",
    "version": None,
}
_attenuator = HBTE(**_hbte_params)


_ru1_pdu = TopYoung(addr="10.57.241.221", port_numbers=[2])
_ru2_pdu = TopYoung(addr="10.57.241.221", port_numbers=[3])

_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.34", username="root", password="umniedziala"
    ),
    pdu_port=_ru1_pdu.pdu_ports[2],
    radio_type=RadioTypes.AHPB,
    signal_analyzer=None,
    # attenuation_ports=[_attenuator.attenuator_ports[1], _attenuator.attenuator_ports[1]]
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
    radio_type=RadioTypes.AHPB,
    signal_analyzer=None,
    # attenuation_ports=[_attenuator.attenuator_ports[2], _attenuator.attenuator_ports[2]]
)


_ru3_pdu = TopYoung(addr="10.57.241.221", port_numbers=[1])
_ru4_pdu = TopYoung(addr="10.57.241.221", port_numbers=[4])

_ru3 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.34", username="root", password="umniedziala"
    ),
    pdu_port=_ru3_pdu.pdu_ports[1],
    radio_type=RadioTypes.AEQE,
    signal_analyzer=None,
    # attenuation_ports=[_attenuator.attenuator_ports[1], _attenuator.attenuator_ports[1]]
)

_ru4 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.84", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.84", username="root", password="umniedziala"
    ),
    pdu_port=_ru4_pdu.pdu_ports[4],
    radio_type=RadioTypes.AEQQ,
    signal_analyzer=None,
    # attenuation_ports=[_attenuator.attenuator_ports[2], _attenuator.attenuator_ports[2]]
)

# #DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.57.151.244", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")
_capacity_unit1 = CapacityUnit(addr="192.168.253.24")

_gnb_pdu = FACOM(addr="10.57.241.219", port_numbers=[3])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit, _capacity_unit1],
    pdu_port=_gnb_pdu.pdu_ports[3],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(
    airscale=_airscale,
    rus=[_ru1, _ru2],
    f1_m_ip_addr="10.57.151.244",
    f1_c_ip_addr="10.57.151.244",
    f1_u_ip_addr="10.57.151.244",
)

_cu = CU(
    backhaul_site_oam_ip="10.57.151.244",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.151.244", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.151.244", username="Nemuadmin", password="nemuuser"
    ),
)

# #DU for classicalBTS2
_lmp_connection1_1 = SshServiceDetails(
    addr="10.57.151.245", username="toor4nsn", password="oZPS0POrRieRtu"
)

_lmp_connection2 = SshServiceDetails(
    addr="10.57.226.12", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_1 = CapacityUnit(addr="192.168.253.20")
_capacity_unit1_1 = CapacityUnit(addr="192.168.253.24")

_gnb_pdu_1 = FACOM(addr="10.57.241.221", port_numbers=[5])

_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection1_1,
    capacity_units=[_capacity_unit_1, _capacity_unit1_1],
    pdu_port=_gnb_pdu_1.pdu_ports[5],
)

_common_unit_2 = CommonUnit(
    lmp_connection=_lmp_connection2,
    capacity_units=[_capacity_unit, _capacity_unit1],
    pdu_port=_gnb_pdu.pdu_ports[3],
)

_airscale_1 = Airscale(common_units=[_common_unit_1])
_airscale_2 = Airscale(common_units=[_common_unit_2])

_du_1 = DU(
    airscale=_airscale_1,
    rus=[_ru3, _ru4],
    f1_m_ip_addr="10.57.151.245",
    f1_c_ip_addr="10.57.151.245",
    f1_u_ip_addr="10.57.151.245",
)

_cu1 = CU(
    backhaul_site_oam_ip="10.57.151.245",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.151.245", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.151.245", username="Nemuadmin", password="nemuuser"
    ),
)

_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=24212)
_classical_bts_1 = ClassicalBts(dus=[_du_1], cu=_cu1, instance_id=24211)


_tl_cloud_topology = "CLOUD_5G_BB3"

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts_1, _classical_bts],
    enbs=[_lte_real_enb],
    ues=[_android, _android_1, _mtk_ue_box, _android_2],
    appserver=_appserver,
    attenuator=[_attenuator],
    tl_cloud_topology=_tl_cloud_topology,
    appservers=[_appserver, _appserver_for_caymus_ul],
    core=_realcore,
)
