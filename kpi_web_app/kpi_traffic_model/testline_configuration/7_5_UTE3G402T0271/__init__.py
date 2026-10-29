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
from taf.config.testline.testpc import TestPc, Connection
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
from taf.config.testline.attenuator import TopYoung as PATopYoung
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
from taf.config.testline.ran import RNC, BSC

__maintainer__ = "chun.li"
__team__ = (
    "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_05_GMS <I_NSB_MN_5GSC_MMW_SC_PZ_HZ_05@internal.nsn.com>"
)
__email__ = "chun.li@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))


_pdns = [
    PDN(pdp_type=PDPTypes.IP.value, apn="dxdata2"),
    PDN(pdp_type=PDPTypes.IP.value, apn="ims"),
    PDN(pdp_type=PDPTypes.IP.value, apn="HSDPA"),
    PDN(pdp_type=PDPTypes.IP.value, apn="mdrb.nokia.com")
]

_realcore = RealCore(
    four_g=None, five_g=None, mcc="442", mnc="03", pdns=_pdns,

)

_appserver_ssh = SshServiceDetails(
    addr="10.71.207.139",
    username="vrf3_sg5",
    password="vrf3@sg5",
    port="45271",
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.207.139",
    iperf_path="/data/local/tmp/iperf3",
    port="46271",
    ports=[46271, 45271],
)

_iperf_details_on_appserver2 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.207.139",
    iperf_path="iperf",
    port="45271",
)
_appserver = AppServer(_iperf_details_on_appserver2)

# CI_Detail_UE_Type='Huawei_5G_Mate_30_Pro'
_android_1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.0.176.106", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="9YS5T19C10004977",
    imsi="442033031521126",
    sec_key="+8613031521126",
    server_dir="C:\Program Files (x86)\DingLi\Pilot Pioneer10.6.9.37---01231639\Pioneer.exe",
    python_path="C:/Python27/python.exe",
    qcat_path="",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["Huawei", "REAL_ANDROID_UE"],
)

_android_2 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.0.176.106", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="9YS0220714001790",
    imsi="442033031521263",
    sec_key="+8613031521263",
    server_dir="C:\Program Files (x86)\DingLi\Pilot Pioneer10.6.9.37---01231639\Pioneer.exe",
    python_path="C:/Python27/python.exe",
    qcat_path="",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["Huawei", "REAL_ANDROID_UE"],
)

_android_3 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.0.176.106", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="c15ccac",
    imsi="442033031521234",
    sec_key="+8613031521234",
    server_dir="C:\Program Files (x86)\DingLi\Pilot Pioneer10.6.9.37---01231639\Pioneer.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "xiaomi"],
)

_android_4 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.0.176.106", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="QKXUT20519006574",
    imsi="442033031521250",
    sec_key="+8613031521250",
    server_dir="C:\Program Files (x86)\DingLi\Pilot Pioneer10.6.9.37---01231639\Pioneer.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "Huawei"],
)

# #RealEnb
_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.71.208.98", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(
    system_module=_real_enb,
    oam_ip=NetworkAddress(
        v4="10.71.208.98"),
    instance_id=4294967121,
    global_bts_id=10619,
)

# #5GRU for classicalBTS
# #attenuator
_attenuator = PATopYoung(
    ip_addr="10.71.203.53",
    port=5000,
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    model="TAS16T3-51-120-1N-DES",
)


_ru_pdu1 = TopYoung(addr="10.71.195.34", port_numbers=[4])
_ru_pdu2 = TopYoung(addr="10.71.195.36", port_numbers=[1])
_ru_pdu3 = TopYoung(addr="10.71.195.38", port_numbers=[5])

_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="root", password=""
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.34", username="root", password=""
    ),
    pdu_port=_ru_pdu1.pdu_ports[4],
    radio_type=RadioTypes.FRGU,
    signal_analyzer=None,
    # attenuation_ports=[_attenuator.attenuator_ports[9], _attenuator.attenuator_ports[10]]
)

_ru3 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.84", username="root", password=""
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.84", username="root", password=""
    ),
    pdu_port=_ru_pdu2.pdu_ports[1],
    radio_type=RadioTypes.AEHC,
    signal_analyzer=None,
    # attenuation_ports=[_attenuator.attenuator_ports[2], _attenuator.attenuator_ports[2]]
)

_ru4 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.84", username="root", password=""
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.84", username="root", password=""
    ),
    pdu_port=_ru_pdu3.pdu_ports[5],
    radio_type=RadioTypes.AVHA,
    signal_analyzer=None,
    # attenuation_ports=[_attenuator.attenuator_ports[2], _attenuator.attenuator_ports[2]]
)


# #DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.71.208.98", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")
_capacity_unit1 = CapacityUnit(addr="192.168.253.24")

_gnb_pdu = FACOM(addr="10.71.195.37", port_numbers=[8])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit, _capacity_unit1],
    pdu_port=_gnb_pdu.pdu_ports[8],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(
    airscale=_airscale,
    rus=[_ru1, _ru3, _ru4],
    f1_m_ip_addr="10.71.208.98",
    f1_c_ip_addr="10.71.208.98",
    f1_u_ip_addr="10.71.208.98",
)

_cu = CU(
    backhaul_site_oam_ip="10.71.208.98",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.208.98", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.208.98", username="Nemuadmin", password="nemuuser"
    ),
)


_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=4294967121, global_bts_id=33554430)

# #host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.177.106", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    connections = [
        Connection(
            interface="eth1",
            device=_lte_real_enb.system_module.common_units[0],
            interface_type="lmp",
        )
    ],
)

_rnc = RNC(
    rnc_id=227,
    oms_ip=NetworkAddress("10.107.129.100"),
    logging_ssh_connection_details=SshServiceDetails(
        addr="10.110.62.182", username="_nokiadmin", password="nokia123"
    ),
)

_tl_cloud_topology = "CLOUD_5G_BB3"

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    enbs=[_lte_real_enb],
    ues=[_android_1, _android_2, _android_3, _android_4],
    appserver=_appserver,
    attenuator=_attenuator,
    tl_cloud_topology=_tl_cloud_topology,
    core=_realcore,
    rncs=[_rnc]
)
