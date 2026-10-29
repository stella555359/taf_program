import os
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
    MediaTek,
    LicenseKeeper,
)
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
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)
from taf.config.testline import RU, DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CU, ClassicalBts
from taf.config.testline.ue import Android
from taf.config.testline import RealEnb, RadioModule
from taf.config.testline.attenuator import HBTE
from taf.config.testline.attenuator import AttenuationPort, TopYoung
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline import Enb, SimEnb, RealEnb, RadioModule, LTEEmuEnb
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.mcs import HBTE
from taf.config.testline.mcs import TopYoung
from taf.config.testline.pdn import PDN, PDPTypes
from taf.config.testline.gnb.networkaddress import NetworkAddress

__maintainer__ = "Yu Lu"
__team__ = "MN 5G RAN I&V 4 Pz HZG SG2"
__email__ = "lu.1.yu@nokia-sbell.com"

## common
__all__ = ["tl"]

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

# Test PC
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.177.107", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# #pdn
_pdns = [
    PDN(PDPTypes.IPV4V6.value, "wap1.nokia.com"),
    PDN(PDPTypes.IPV4V6.value, "wap2.nokia.com"),
]

# #realcore5g  # updated 2020/02/10
_amf_oam_ssh_connection_details = SshServiceDetails(
    addr="10.110.227.70", username="test", password="Nokia456"
)
_n2_address = NetworkAddress(v4="10.0.0.0", v6="100:00::000", vlan_id=1)
_amf = AMF(oam_ssh_connection_details=_amf_oam_ssh_connection_details, n2=_n2_address)
_real_5g_core_details = RealCore5GDetails(amf=_amf)

# #realcore5g
_realcore = RealCore(five_g=_real_5g_core_details, mcc="460", mnc="02", pdns=_pdns)

# PA topyoung
# _attenuator = TopYoung(
#  ip_addr="10.57.231.147",
#  port=3000,
#  attenuation_port_numbers=[1, 2, 3, 4],
#  model="TAS16T16-51-120-1S-DES",
# )

# Real 5G Core is used in real world.  here use EPCsim as the 5GC class is not implemented in tl config lib yet.
_epc_sim = EPCSim(
    mme_ip="10.110.227.5",
    mcc="460",
    mnc="2",
    tac="0",
    default_ssh_connection_details=SshServiceDetails(
        addr="10.110.227.70", username="haijtest", password="Nokia_1234"
    ),
    edaemon_port=10000,
    egate_port=20000,
    dir_path="/opt/iphy/latest",
    cfg_filename="LRC.cfg",
)

# RealEnb
_real_enb_pdu = FACOM(addr="10.71.197.85", port_numbers=[2])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.71.206.229", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[2],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=None)

##5GRU for classical BTS
_ru_0_pdu = FACOM(addr="10.71.197.82", port_numbers=[4])

_ru_0 = RU(
    #'AQHA'
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.73.129",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.73.129",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    pdu_port=_ru_0_pdu.pdu_ports[4],
    radio_type=RadioTypes.AQHA,
    serial_number="1M222225877",
    #    attenuation_ports=[
    #        _attenuator.attenuator_ports[1],
    #        _attenuator.attenuator_ports[2],
    #        _attenuator.attenuator_ports[3],
    #        _attenuator.attenuator_ports[4],
    #    ],
)

_ru_1_pdu = FACOM(addr="10.71.197.78", port_numbers=[1])

_ru_1 = RU(
    #'AQHA'
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.73.129",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.73.129",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    pdu_port=_ru_1_pdu.pdu_ports[1],
    radio_type=RadioTypes.AQHA,
    serial_number="1M230508547",
    #    attenuation_ports=[
    #        _attenuator.attenuator_ports[1],
    #        _attenuator.attenuator_ports[2],
    #        _attenuator.attenuator_ports[3],
    #        _attenuator.attenuator_ports[4],
    #    ],,
)

##DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="6.6.6.6")

_gnb_pdu = FACOM(addr="10.71.197.85", port_numbers=[2])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[2],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru_0, _ru_1], f1_m_ip_addr="10.71.206.229")

##CU
_cu = CU(
    backhaul_site_oam_ip="10.71.206.229",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.206.229", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.206.229", username="Nemuadmin", password="nemuuser"
    ),
)

##cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id="1", global_bts_id="10812")

##HBTE_MCS
# _topyoung = TopYoung(
#    ip_addr="10.71.215.204",
#    port=28888,
#    mcs_port_numbers=[128],
#    model="MCS2350A2-128B16-E6",
# )

##HBTE_MCS
_topyoung = TopYoung(
    ip_addr="10.71.206.201",
    port=28888,
    mcs_port_numbers=[128],
    model="MCS2350A2-128B16-E6",
)

# SIGSPARK
_ue_host1_ssh = SshServiceDetails(
    addr="10.71.215.162", username="spark", password=""
)

_ue_host2_ssh = SshServiceDetails(
    addr="10.71.206.210", username="spark", password="spark"
)

_spark_appserver_ssh = SshServiceDetails(
    addr="10.57.191.236", username="vrf4_sg2", password="VERIFICATION@sg2"
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_spark_appserver_ssh,
    network_interface_address="10.57.191.236",
    iperf_path="iperf",
    port=52228,
)

_sigspark1 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="7cc1bde4",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.47/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262038001006431",
    licensekeeper=LicenseKeeper(username="HAZ4_SG2", password="HAZ4_SG2"),
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark2 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="516eb97b",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.47/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033032995918",
    licensekeeper=LicenseKeeper(username="HAZ4_SG2", password="HAZ4_SG2"),
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark3 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="eee4bd88",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.47/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033100011500",
    licensekeeper=LicenseKeeper(username="HAZ4_SG2", password="HAZ4_SG2"),
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark4 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="b0d223cd",
    server_dir="C:/Program Files (x86)/Spark1.1.2008.12/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033100004133",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark5 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="74e2dcf6",
    server_dir="C:/Program Files (x86)/Spark1.1.1998.1/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262038001006084",
    licensekeeper=LicenseKeeper(username="HAZ4_SG2", password="HAZ4_SG2"),
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark6 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="d07e4a2b",
    server_dir="C:/Program Files (x86)/Spark1.1.1998.1/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033100004082",
    licensekeeper=LicenseKeeper(username="HAZ4_SG2", password="HAZ4_SG2"),
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark7 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="e846e2eb",
    server_dir="C:/Program Files (x86)/Spark1.1.1998.1/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033032995930",
    licensekeeper=LicenseKeeper(username="HAZ4_SG2", password="HAZ4_SG2"),
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark8 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="706760dd",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.47/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033100011500",
    licensekeeper=LicenseKeeper(username="HAZ4_SG2", password="HAZ4_SG2"),
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)


tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    enbs=[_lte_real_enb],
    core=_realcore,
    #attenuator=_attenuator,
    mcses=[_topyoung],
    ues=[
        _sigspark1,
        _sigspark3,
        _sigspark5,
        _sigspark7,
        _sigspark2,
        _sigspark4,
        _sigspark6,
        _sigspark8,
    ],
    tl_cloud_topology=_tl_cloud_topology,
)
