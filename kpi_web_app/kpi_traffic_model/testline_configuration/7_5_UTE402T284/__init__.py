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
from taf.config.testline.testpc import TestPc, Connection
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
from taf.config.testline.pdu import FPFH
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, ATEN, RRB, APC, Gude
from taf.config.testline.pdu import HBTE as pdu_HBTE
from taf.config.testline.testline import TestLine
from taf.config.testline.mcs import TopYoung as mcs
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
    JFW,
    HBTE,
    Hytem,
    RadioRack,
)
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
from taf.config.testline.optical_switch import Leoni, Calient
from taf.config.testline.appserver import AppServer
from taf.config.testline.pdn import PDN, PDPTypes
from taf.config.testline.attenuator import RadioRack
from taf.config.testline import LicenseKeeper

__maintainer__ = "Liu Tingting"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_6_GMS <I_MN_5G_RAN_IV4_LINE_HZG_6@internal.nsn.com>"
)
__email__ = "tingting.1.liu@nokia-sbell.com"

_licensekeeper = LicenseKeeper(username="HAZ4_SG6", password="HAZ4_SG6")

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# #pdn
_pdns = [
    PDN(PDPTypes.IPV4V6.value, "weistatic"),
]

# #realcore5g  # updated 2020/02/10
_amf_oam_ssh_connection_details = SshServiceDetails(
    addr="10.110.227.70", username="test", password="Nokia456"
)
_n2_address = NetworkAddress(v4="10.0.0.0", v6="100:00::000", vlan_id=1)
_amf = AMF(oam_ssh_connection_details=_amf_oam_ssh_connection_details, n2=_n2_address)
_real_5g_core_details = RealCore5GDetails(amf=_amf)

# #realcore5g
_realcore = RealCore(five_g=_real_5g_core_details, mcc="460", mnc="2", pdns=_pdns)

# Iperf_Qualcomm X65
_appserver_ssh = SshServiceDetails(
    addr="10.57.191.248", username="vrf4_sg6", password="vrf4@sg6", port="56284"
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.248",
    iperf_path="iperf",
    port="56684",
)

# Iperf_mtk
_appserver_ssh_1 = SshServiceDetails(
    addr="10.57.191.248", username="vrf4_sg6", password="vrf4@sg6", port="56286"
)
_iperf_1 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh_1,
    network_interface_address="10.57.191.248",
    iperf_path="iperf",
    port="56686",
)

_appserver = AppServer(_iperf)

# Qualcomm X55
_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.68.86.184", username="nokia5G", password="noki@123"
    ),
    serial_number="a9f1ce77",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf_1,
    imsi="310260100008744",
    capabilities=["REAL_ANDROID_UE", "qct_dx50"],
    network_mode_switch_method="keyevents",
    # mobile_network_text="Mobile network",
    mobile_network_text="SIMs",
    setting_network_mode_text="Preferred network type",
)

_sigspark = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.101.48.211", username="spark", password="spark"
    ),
    serial_number="33487b2b",
    server_dir="C:/Program Files (x86)/Spark/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_1,
    imsi="310260100008443",
    licensekeeper=_licensekeeper,
    capabilities=["REAL_ANDROID_UE0", "huawei_sigspark"],
)

_sigspark_0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.101.48.211", username="spark", password="spark"
    ),
    serial_number="33487b2b",
    server_dir="C:/Program Files (x86)/Spark/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="460023100010670",
    licensekeeper=_licensekeeper,
    capabilities=["REAL_ANDROID_UE1", "sigspark_multiUE"],
)

_sigspark_1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.101.48.211", username="spark", password="spark"
    ),
    serial_number="33487b2b",
    server_dir="C:/Program Files (x86)/Spark/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="460023100010673",
    licensekeeper=_licensekeeper,
    capabilities=["REAL_ANDROID_UE2", "sigspark_multiUE"],
)

_sigspark_2 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.101.48.211", username="spark", password="spark"
    ),
    serial_number="33487b2b",
    server_dir="C:/Program Files (x86)/Spark/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="460023100010674",
    licensekeeper=_licensekeeper,
    capabilities=["REAL_ANDROID_UE3", "sigspark_multiUE"],
)

_sigspark_3 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.101.48.211", username="spark", password="spark"
    ),
    serial_number="33487b2b",
    server_dir="C:/Program Files (x86)/Spark/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="460023100010681",
    licensekeeper=_licensekeeper,
    capabilities=["REAL_ANDROID_UE4", "sigspark_multiUE"],
)

_sigspark_4 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.101.48.211", username="spark", password="spark"
    ),
    serial_number="33487b2b",
    server_dir="C:/Program Files (x86)/Spark/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="460028001006304",
    licensekeeper=_licensekeeper,
    capabilities=["REAL_ANDROID_UE5", "sigspark_multiUE"],
)

_sigspark_5 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.101.48.211", username="spark", password="spark"
    ),
    serial_number="33487b2b",
    server_dir="C:/Program Files (x86)/Spark/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="460023100010671",
    licensekeeper=_licensekeeper,
    capabilities=["REAL_ANDROID_UE6", "sigspark_multiUE"],
)

_sigspark_6 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.101.48.211", username="spark", password="spark"
    ),
    serial_number="33487b2b",
    server_dir="C:/Program Files (x86)/Spark/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="460023100010682",
    licensekeeper=_licensekeeper,
    capabilities=["REAL_ANDROID_UE7", "sigspark_multiUE"],
)

_sigspark_7 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.101.48.211", username="spark", password="spark"
    ),
    serial_number="33487b2b",
    server_dir="C:/Program Files (x86)/Spark/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="460023100010169",
    licensekeeper=_licensekeeper,
    capabilities=["REAL_ANDROID_UE8", "sigspark_multiUE"],
)

# RealEnb
_real_enb_pdu = pdu_HBTE(addr="10.101.45.175", port_numbers=[5])

_common_unit_6 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.101.53.81", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[5],
)

_real_enb = Airscale(common_units=[_common_unit_6])

_lte_real_enb = RealEnb(
    airscale=_real_enb,
    oam_ip=NetworkAddress(v4="10.101.53.81"),
    system_module=_real_enb,
    rms=None,
    instance_id=284284,
    global_bts_id=284284,
)

# 5GRU for classicalBTS
# attenuator
_attenuator1=TopYoung(
    ip_addr="10.57.156.55",
    port=28888,
    attenuation_port_numbers=[
        1,
        2,
        3,
        4,
    ],
    model="TAS32B32-0.7G8.4-90-0.5S-DES",)

_ru_pdu_0 = FPFH(addr="10.101.45.12", port_numbers=[6])

_ru_0 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.145",
        username="serviceuser",
        password="7B+6yyInfX0uES/FP60uEyhjZHUxB2MoRWvZqUMW42g=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu_0.pdu_ports[6],
    radio_type=RadioTypes.AEHC.value,
    serial_number="K9223525815",
    attenuation_ports=[
        _attenuator1.attenuator_ports[1],
        _attenuator1.attenuator_ports[2],
        _attenuator1.attenuator_ports[3],
        _attenuator1.attenuator_ports[4],
    ],
)

_ru_pdu_1 = pdu_HBTE(addr="10.101.45.34", port_numbers=[6])

_ru_1 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.57.158",
        username="serviceuser",
        password="7B+6yyInfX0uES/FP60uEyhjZHUxB2MoRWvZqUMW42g=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.57.158", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu_1.pdu_ports[6],
    radio_type=RadioTypes.AEHC.value,
    serial_number="L1204708739",
    attenuation_ports=[
        _attenuator1.attenuator_ports[1],
        _attenuator1.attenuator_ports[2],
        _attenuator1.attenuator_ports[3],
        _attenuator1.attenuator_ports[4],
    ],
)

_ru_pdu_2 = pdu_HBTE(addr="10.101.45.34", port_numbers=[5])

_ru_2 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.57.162",
        username="serviceuser",
        password="7B+6yyInfX0uES/FP60uEyhjZHUxB2MoRWvZqUMW42g=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.57.162", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu_2.pdu_ports[5],
    radio_type=RadioTypes.AEHC.value,
    serial_number="L1205002776",
    attenuation_ports=[
        _attenuator1.attenuator_ports[1],
        _attenuator1.attenuator_ports[2],
        _attenuator1.attenuator_ports[3],
        _attenuator1.attenuator_ports[4],
    ],
)

_ru_pdu_3 = pdu_HBTE(addr="10.101.45.176", port_numbers=[6])

_ru_3 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.177",
        username="root",
        password="0q/7SXKjF2AlAba+yisrCxQiKz1PRJJ0IVDZuh/sOaA=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu_3.pdu_ports[6],
    radio_type=RadioTypes.AHFIB.value,
    serial_number="BL2124V0EHO",
    #    attenuation_ports=[
    #        _attenuator.attenuator_ports[13],
    #        _attenuator.attenuator_ports[14],
    #        _attenuator.attenuator_ports[15],
    #        _attenuator.attenuator_ports[16],
    #    ],
)

_ru_pdu_4 = pdu_HBTE(addr="10.101.45.176", port_numbers=[6])

_ru_4 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.177",
        username="root",
        password="0q/7SXKjF2AlAba+yisrCxQiKz1PRJJ0IVDZuh/sOaA=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu_4.pdu_ports[6],
    radio_type=RadioTypes.AHFIB.value,
    serial_number="BL2124V0EHN",
    attenuation_ports=[
        _attenuator1.attenuator_ports[3],
    ],
)

_ru_pdu_5 = pdu_HBTE(addr="10.101.45.176", port_numbers=[6])

_ru_5 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.177",
        username="root",
        password="0q/7SXKjF2AlAba+yisrCxQiKz1PRJJ0IVDZuh/sOaA=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu_5.pdu_ports[6],
    radio_type=RadioTypes.AHFIB.value,
    serial_number="BL2049V0VBP",
    attenuation_ports=[
        _attenuator1.attenuator_ports[4],
    ],
)

_ru_pdu_6 = pdu_HBTE(addr="10.101.45.176", port_numbers=[5])

_ru_6 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.209",
        username="root",
        password="0q/7SXKjF2AlAba+yisrCxQiKz1PRJJ0IVDZuh/sOaA=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu_6.pdu_ports[5],
    radio_type=RadioTypes.AHLOA.value,
    serial_number="K9182103407",
    attenuation_ports=[
        _attenuator1.attenuator_ports[1],
        _attenuator1.attenuator_ports[2],
        _attenuator1.attenuator_ports[3],
        _attenuator1.attenuator_ports[4],
    ],
)

_ru_pdu_7 = pdu_HBTE(addr="10.101.45.176", port_numbers=[6])

_ru_7 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.177",
        username="root",
        password="0q/7SXKjF2AlAba+yisrCxQiKz1PRJJ0IVDZuh/sOaA=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu_7.pdu_ports[6],
    radio_type=RadioTypes.AHLOA.value,
    serial_number="BL2223G1AY9",
    attenuation_ports=[
        _attenuator1.attenuator_ports[1],
        _attenuator1.attenuator_ports[2],
        _attenuator1.attenuator_ports[3],
        _attenuator1.attenuator_ports[4],
    ],
)

_ru_pdu_8 = pdu_HBTE(addr="10.101.45.176", port_numbers=[6])

_ru_8 = RU(
    ru_hw_group="Below6GHz",  # Above6GHz or Below6GHz
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.177",
        username="root",
        password="0q/7SXKjF2AlAba+yisrCxQiKz1PRJJ0IVDZuh/sOaA=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu_8.pdu_ports[6],
    radio_type=RadioTypes.AHLOA.value,
    serial_number="BL2223G1AXP",
    attenuation_ports=[
        _attenuator1.attenuator_ports[1],
        _attenuator1.attenuator_ports[2],
        _attenuator1.attenuator_ports[3],
        _attenuator1.attenuator_ports[4],
    ],
)
# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.101.53.75", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.40")

_gnb_pdu = pdu_HBTE(addr="10.101.45.172", port_numbers=[4])

_gnb_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.53", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_common_unit_4 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[4],
    test_pc=_gnb_test_pc,
)

_airscale = Airscale(common_units=[_common_unit_4])

_du = DU(
    airscale=_airscale,
    rus=[
        _ru_0,
        _ru_1,
        _ru_2,
        _ru_3,
        _ru_4,
        _ru_5,
        _ru_6,
        _ru_7,
        _ru_8,
    ],

    f1_m_ip_addr="10.101.53.75",
)

# #CU
_f1m = NetworkAddress(v4="9.9.1.1", v6="xxxx", vlan_id=1)
_f1c = NetworkAddress(v4="9.9.1.2", v6="xxxx", vlan_id=2)
_f1u = NetworkAddress(v4="9.9.1.3", v6="xxxx", vlan_id=3)
_x2c = NetworkAddress(v4="9.9.2.1", v6="xxxx", vlan_id=1)
_x2u = NetworkAddress(v4="9.9.2.2", v6="xxxx", vlan_id=2)
_s1c = NetworkAddress(v4="9.9.3.1", v6="xxxx", vlan_id=1)
_s1u = NetworkAddress(v4="9.9.3.2", v6="xxxx", vlan_id=2)
_tracing = NetworkAddress(v4="9.9.1.2", v6="xxxx", vlan_id=1)
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(v4="10.101.53.75"),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.53.75", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.53.75", username="Nemuadmin", password="nemuuser"
    ),
    f1m=_f1m,
    f1c=_f1c,
    f1u=_f1u,
    x2c=_x2c,
    x2u=_x2u,
    s1c=_s1c,
    s1u=_s1u,
    tracing=_tracing,
)

# cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"
# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=284, global_bts_id=284)

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.53", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_classical_bts.dus[0].airscale.common_units[0],
            interface_type="lmp",
        ),
        # Connection(
        #     interface="eth1",
        #     device=_lte_real_enb.system_module.common_units[0],
        #     interface_type="lmp",
        # ),
        _android,
    ],
)

_host1 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.53", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_lte_real_enb.system_module.common_units[0],
            interface_type="lmp",
        ),
        _android,
    ],
)
tl = TestLine(
    test_pc=_host,
    test_pcs=[_host, _host1],
    gnbs=[_classical_bts],
    core=_realcore,
    tl_cloud_topology=_tl_cloud_topology,
    enbs=[_lte_real_enb],
    ues=[_sigspark_0,
        _sigspark_1,
        _sigspark_2,
        _sigspark_3,
        _sigspark_4,
        _sigspark_5,
        _sigspark_6,
        _sigspark_7,
        _android,
        _sigspark
    ],
    appserver=_appserver,
    attenuator=[_attenuator1],
)

# old version keyword under robotws5g/resource compatibility workaround
# tl = TestlineWrapper(tl)
