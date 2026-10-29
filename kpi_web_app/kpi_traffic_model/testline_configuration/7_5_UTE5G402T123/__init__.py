import os
from taf.config.testline.cloud_hosting import (
    ControlNode,
    NCIR,
    CloudDeployment,
    DeploymentFlavorStack,
    DeploymentNetworkStack,
    DeploymentVnfStack,
)
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.ue import (
    AirphoneCloud,
    Airphone,
    Prisma,
    TM500,
    Qualcomm,
    QualcommUeType,
    Android,
)  # added in taf.meta.5.4
from taf.config.testline.core import (
    EPCSim,
    RealCore4G,
    RealCore,
    RealCore5GDetails,
    AMF,
)
from taf.config.testline.gnb.du import DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, ATEN, RRB, APC, Gude
from taf.config.testline.pdu import TopYoung, HBTE, FPFH
from taf.config.testline.testline import TestLine
from taf.config.testline.ue import MediaTek, TafUeFastmile
from taf.config.testline.pdn import PDN, PDPTypes
from taf.config.testline.connection_details import (
    SshServiceDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.appserver import AppServer, TafUeAppServer
from taf.config.testline.testpc import TestPc
from taf.config.testline.gnb.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.config.testline.gnb.du import Cablink, Endpoint
from taf.config.testline import NetworkAddress, RoutingInformation, LicenseKeeper
from taf.config.testline.lmi import LMI, Local
from taf.config.testline.taf_ue_data_transfer_protocol import TafUeDataTransferProtocol

# added in taf.meta 5.4
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
from taf.config.testline.enb import (
    Enb,
    SimEnb,
    RealEnb,
    LTEEmuEnb,
    PrismaEnb,
    DocomoEnb,
)


__maintainer__ = "Lusha Zhang"
__team__ = "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_02@internal.nsn.com"
__email__ = "lusha.zhang@nokia-sbell.com"


# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# #host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.19", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
# _docker_pc = TestPc(
#     default_ssh_connection_details=SshServiceDetails(
#         addr="10.57.167.46", username="dcapuser", password="dcapuser123"
#     )
# )
# _tce_pc = TestPc(
#     default_ssh_connection_details=SshServiceDetails(
#         addr="10.57.167.46", username="dcapuser", port=1234
#     )
# )

# PB INFO of ENB IS NOT CORRECT #

# 5GRU
_pdu_WG21_PB1 = TopYoung(addr="10.58.251.248", port_numbers=[1, 2, 3, 4, 5, 6])
_pdu_WG22_PB1 = TopYoung(addr="10.57.251.250", port_numbers=[1, 3, 4, 5, 6])
_pdu_WG23_PB1 = TopYoung(addr="10.57.251.253", port_numbers=[4, 5])
_pdu_WG06_PB2 = TopYoung(addr="10.57.251.235", port_numbers=[2])

##lmi for RU10 AVQQA L1251202485
_ru_lmi_pc_RU10 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.130.230", username="mn5gran", password="nokia123@"
    )
)
_ru_lmi_RU10 = LMI(
    product_code="", host=_ru_lmi_pc_RU10, uart_mapping=[Local(port="COM6")]
)

_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2",
        username="serviceuser",
        password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="root", password="a2%FgSz3$fHmdusap354xujw7a"
    ),
    pdu_port=_pdu_WG21_PB1.pdu_ports[5],
    radio_type=RadioTypes.AVHA,
    serial_number="L1251101919",
)

_ru2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2",
        username="serviceuser",
        password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="root", password="a2%FgSz3$fHmdusap354xujw7a"
    ),
    pdu_port=_pdu_WG22_PB1.pdu_ports[1],
    radio_type=RadioTypes.AVHQB,
    serial_number="1M251000696",
)

_ru3 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="root", password="a2%FgSz3$fHmdusap354xujw7a"
    ),
    pdu_port=_pdu_WG22_PB1.pdu_ports[3],
    radio_type=RadioTypes.AQQQA,
    serial_number="BL2330G603A",
)

_ru4 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2",
        username="serviceuser",
        password="wcdjLlTpqEY3cAmOe11u6aELwGI3rDvpGJQvCkcyHZc=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="root", password="a2%FgSz3$fHmdusap354xujw7a"
    ),
    pdu_port=_pdu_WG21_PB1.pdu_ports[6],
    radio_type=RadioTypes.AZQU,
    serial_number="1M222314633 ",
)

_ru5 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2",
        username="serviceuser",
        password="wcdjLlTpqEY3cAmOe11u6aELwGI3rDvpGJQvCkcyHZc=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="root", password="a2%FgSz3$fHmdusap354xujw7a"
    ),
    pdu_port=_pdu_WG21_PB1.pdu_ports[6],
    radio_type=RadioTypes.AZQU,
    serial_number="1M222506825 ",
)

_ru5 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2",
        username="serviceuser",
        password="wcdjLlTpqEY3cAmOe11u6aELwGI3rDvpGJQvCkcyHZc=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="root", password="a2%FgSz3$fHmdusap354xujw7a"
    ),
    pdu_port=_pdu_WG21_PB1.pdu_ports[2],
    radio_type=RadioTypes.AZQU,
    serial_number="1M222506825 ",
)

_ru6 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2",
        username="serviceuser",
        password="wcdjLlTpqEY3cAmOe11u6aELwGI3rDvpGJQvCkcyHZc=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="root", password="a2%FgSz3$fHmdusap354xujw7a"
    ),
    pdu_port=_pdu_WG22_PB1.pdu_ports[6],
    radio_type=RadioTypes.AZQU,
    serial_number="1M222314645 ",
)

_ru7 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2",
        username="root",
        password="",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="root", password="a2%FgSz3$fHmdusap354xujw7a"
    ),
    pdu_port=_pdu_WG21_PB1.pdu_ports[3],
    radio_type=RadioTypes.AHHB,
    serial_number="DH240839732 ",
)

_ru8 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2",
        username="root",
        password="",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="root", password="a2%FgSz3$fHmdusap354xujw7a"
    ),
    pdu_port=_pdu_WG21_PB1.pdu_ports[4],
    radio_type=RadioTypes.AHHB,
    serial_number="DH240839729 ",
)

_ru9 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2",
        username="root",
        password="",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="root", password="a2%FgSz3$fHmdusap354xujw7a"
    ),
    pdu_port=_pdu_WG21_PB1.pdu_ports[1],
    radio_type=RadioTypes.AHHB,
    serial_number="DH240839730 ",
)

_ru10 = RU(
    ru_hw_group="AVQL",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2",
        username="serviceuser",
        password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="root", password="a2%FgSz3$fHmdusap354xujw7a"
    ),
    pdu_port=_pdu_WG23_PB1.pdu_ports[4],
    radio_type=RadioTypes.AVQQA.value,
    serial_number="L1251202485",
    lmi=_ru_lmi_RU10,
)

_ru11 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2",
        username="root",
        password="",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="root", password="a2%FgSz3$fHmdusap354xujw7a"
    ),
    pdu_port=_pdu_WG06_PB2.pdu_ports[2],
    radio_type=RadioTypes.AHCA,
    serial_number="AS201817455 ",
)

# enb
_fsp_1 = CapacityUnit(
    addr="192.168.255.129",
    hardware_type="ASOG",
    hardware_version="476254A.102",
    serial_number="L1243303634",
)

_fct_1 = CommonUnit(
    SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_fsp_1],
    pdu_port=_pdu_WG22_PB1.pdu_ports[5],
    hardware_type="ASOG",
    hardware_version="476254A.102",
    serial_number="L1243303634",
)


_enb_sbts_1 = RealEnb(
    system_module=[_fct_1],
    rms=[_ru1],
    oam_ip=NetworkAddress("10.57.228.107"),
    instance_id=123,
    global_bts_id=123,
)


# #######Iperf########
_appserver_ssh = SshServiceDetails(
    addr="10.57.191.234", username="vrf3_sg2", password="vrf3@sg2"
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.234",
    iperf_path="/usr/bin/iperf",
    port=42133,
)
_appserver = AppServer(_iperf_details_on_appserver)


# Multi UE X65
# CI_Detail_UE_Type='STU-M NA'
# UE type: Multi UE System 8UE X62 NA Spark

_8ue_host_ssh = SshServiceDetails(
    addr="10.71.230.194", username="spark", password="spark"
)

_licensekeeper = LicenseKeeper(username="HAZ3_SG2", password="HAZ3_SG2")

_IMSI_1 = "262033100020817"
_IMSI_2 = "262033100020818"
_IMSI_3 = "262033100020819"
_IMSI_4 = "262033100020820"
_IMSI_5 = "262033100020821"
_IMSI_6 = "262033100020822"
_IMSI_7 = "262033100020823"
_IMSI_8 = "262033100020824"

_spark_server_dir_8UE = "/cygdrive/c/Program Files (x86)/Spark1.1.2012.5/Bin/Spark.exe"


_sigspark_1 = Android(
    ssh_connection_details=_8ue_host_ssh,
    serial_number="042010002144001",
    server_dir=_spark_server_dir_8UE,
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "sigspark_multiUE"],
    imsi=_IMSI_1,
    licensekeeper=_licensekeeper,
)

_sigspark_2 = Android(
    ssh_connection_details=_8ue_host_ssh,
    serial_number="042010002144001",
    server_dir=_spark_server_dir_8UE,
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "huawei_sigspark"],
    imsi=_IMSI_2,
    licensekeeper=_licensekeeper,
)

_sigspark_3 = Android(
    ssh_connection_details=_8ue_host_ssh,
    serial_number="021010032210001",
    server_dir=_spark_server_dir_8UE,
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "huawei_sigspark"],
    imsi=_IMSI_3,
    licensekeeper=_licensekeeper,
)

_sigspark_4 = Android(
    ssh_connection_details=_8ue_host_ssh,
    serial_number="021010032210001",
    server_dir=_spark_server_dir_8UE,
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "huawei_sigspark"],
    imsi=_IMSI_4,
    licensekeeper=_licensekeeper,
)

_sigspark_5 = Android(
    ssh_connection_details=_8ue_host_ssh,
    serial_number="021010032210001",
    server_dir=_spark_server_dir_8UE,
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "huawei_sigspark"],
    imsi=_IMSI_5,
    licensekeeper=_licensekeeper,
)

_sigspark_6 = Android(
    ssh_connection_details=_8ue_host_ssh,
    serial_number="021010032210001",
    server_dir=_spark_server_dir_8UE,
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "huawei_sigspark"],
    imsi=_IMSI_6,
    licensekeeper=_licensekeeper,
)

_sigspark_7 = Android(
    ssh_connection_details=_8ue_host_ssh,
    serial_number="021010032210001",
    server_dir=_spark_server_dir_8UE,
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "huawei_sigspark"],
    imsi=_IMSI_7,
    licensekeeper=_licensekeeper,
)

_sigspark_8 = Android(
    ssh_connection_details=_8ue_host_ssh,
    serial_number="021010032210001",
    server_dir=_spark_server_dir_8UE,
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "huawei_sigspark"],
    imsi=_IMSI_8,
    licensekeeper=_licensekeeper,
)

# #DU_0 for cloudlBTS
_lmp_connection_0 = SshServiceDetails(
    addr="10.57.228.107", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.255.129")

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection_0,
    capacity_units=[_capacity_unit],
    pdu_port=_pdu_WG22_PB1.pdu_ports[5],
)

_airscale = Airscale(common_units=[_common_unit_0])

_ru_cablinks = [
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=3),
        target=Endpoint(unit=_ru1, label="SFP", port_id=4),
    )
]

_du = DU(
    airscale=_airscale,
    rus=[_ru1, _ru2, _ru3, _ru4, _ru5, _ru6, _ru7, _ru8, _ru9, _ru10, _ru11],
    f1_m_ip_addr="10.57.228.107",
    cablinks=_ru_cablinks,
)


# #CU
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.57.228.107",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.211.129", ip_prefix_length=27),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.228.107", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.228.107", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.57.228.107",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.211.129", ip_prefix_length=27),
    ),
    x2u=NetworkAddress(
        v4="10.57.228.107",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.211.129", ip_prefix_length=27),
    ),
    s1u=NetworkAddress(
        v4="10.57.228.107",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.211.129", ip_prefix_length=27),
    ),
)


# classicalbts------------------------------------------------
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=123, global_bts_id=123)

_pdns = [
    PDN(pdp_type=PDPTypes.IP.value, apn="dxdata2"),
    PDN(pdp_type=PDPTypes.IP.value, apn="dxdata4"),
]
_core = RealCore(pdns=_pdns)


# #cloud_topology------------------------------------------------
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_SPARK_SA_ASOG_AVHA_AVHQB_AQQQA_AZQU_AHHB_AVQQA"

tl = TestLine(
    test_pc=_host,
    ues=[
        _sigspark_1,
        _sigspark_2,
        _sigspark_3,
        _sigspark_4,
        _sigspark_5,
        _sigspark_6,
        _sigspark_7,
        _sigspark_8,
    ],
    gnbs=[_classical_bts],
    enbs=[_enb_sbts_1],
    appserver=_appserver,
    core=_core,
    tl_cloud_topology=_tl_cloud_topology,
)
