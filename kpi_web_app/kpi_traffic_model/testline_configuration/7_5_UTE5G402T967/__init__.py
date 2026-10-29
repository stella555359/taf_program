import os
import yaml
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc
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
    HBTE,
    TopYoung,
)
from taf.config.testline.attenuator import AttenuationPort
from taf.config.testline.attenuator import HBTE as PA_HBTE
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
from taf.config.testline.pdn import PDN, PDPTypes
from taf.config.testline.testline import TestLine
from taf.config.testline import TopYoung_PDU
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
    LicenseKeeper,
)  # added in taf.meta.5.4
from taf.config.testline.enb import (
    Enb,
    SimEnb,
    RealEnb,
    LTEEmuEnb,
    PrismaEnb,
    DocomoEnb,
)

# added in taf.meta 5.4
from taf.config.testline.attenuator import AttenuationPort, TopYoung
from taf.config.testline.gnb.networkaddress import NetworkAddress  # add in taf.meta 5.4
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.appserver import AppServer

__maintainer__ = "Chen Yin"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_2_GMS <I_MN_5G_RAN_IV4_LINE_HZG_2@internal.nsn.com>"
)
__email__ = "yin.1.chen@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# UE
_appserver_ssh = SshServiceDetails(
    addr="10.71.219.230",
    username="iperf",
    password="39nBTScHWRf3weyBMK0=",
    port="52967",
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.219.230",
    iperf_path="/usr/bin/iperf",
    port=52967,
)

_Huawei_host_ssh = SshServiceDetails(
    addr="10.71.217.40", username="nokia5G", password="noki@123"
)

iperf_details = IperfDataTransferDetails(
    ssh_connection_details=_Huawei_host_ssh,
    network_interface_address="10.71.219.230",
    iperf_path="/cygdrive/c/iperf-2.0.8b-win64/iperf",
    port=52967,
)

_appserver = AppServer(iperf_details)

_Huawei = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.217.40", username="nokia5G", password="noki@123"
    ),
    serial_number="PLG5T20C01007859",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "cell_Mapping: [1]", "huawei"],
)

# CI_Detail_UE_Type='Huawei Mate 30 Pro 5G'
_sigspark = Android(
    ssh_connection_details=_Huawei_host_ssh,
    serial_number="PLG5T20C01007859",
    server_dir="C:/Program Files (x86)/Spark1.1.2005.9/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf,
    imsi="262038001006089",
    licensekeeper=LicenseKeeper(username="HAZ4_SG2", password="HAZ4_SG2"),
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_Xiaomi_host_ssh = SshServiceDetails(
    addr="10.71.217.40", username="nokia5G", password="noki@123"
)

_xiaomi = Android(
    ssh_connection_details=_Xiaomi_host_ssh,
    serial_number="d2fbd581",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["cell_Mapping: [1,2,3]", "Mi12UI13.0.12", "xiaomi"],
)

_Xiaomi2_host_ssh = SshServiceDetails(
    addr="10.71.217.190", username="mn5gran", password="nokia123@"
)

_xiaomi2 = Android(
    ssh_connection_details=_Xiaomi2_host_ssh,
    serial_number="cda3bfd2",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["cell_Mapping: [4,5,6]", "Mi11UI13", "xiaomi"],
)

# #pdn
_pdns = [PDN(PDPTypes.IPV4V6.value, "dxdata2")]

# #realcore5g  # updated 2020/02/10
_amf_oam_ssh_connection_details = SshServiceDetails(
    addr="10.110.66.198", username="test", password="Nokia456"
)
_n2_address = NetworkAddress(v4="10.0.0.0", v6="100:00::000", vlan_id=1)
_amf = AMF(oam_ssh_connection_details=_amf_oam_ssh_connection_details, n2=_n2_address)
_real_5g_core_details = RealCore5GDetails(amf=_amf)

# #realcore5g
_realcore = RealCore(five_g=_real_5g_core_details, mcc="460", mnc="02", pdns=_pdns)


# #RealEnb
_real_enb_pdu = HBTE(addr="10.71.197.87", port_numbers=[2])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.71.215.200", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[2],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb)

# #5GRU for classicalBTS
_attenuator1 = PA_HBTE(
    ip_addr="10.71.206.228",
    port=5000,
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    model="PA-16-16-6-127-0.5-B-S",
)

# #5GRU for classicalBTS
_attenuator2 = PA_HBTE(
    ip_addr="10.71.206.200",
    port=5000,
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8],
    model="PA-16-16-6-127-0.5-B-S",
)


# #5GRU for classicalBTS
_ru1_pdu = TopYoung_PDU(addr="10.71.197.84", port_numbers=[3])

_ru1 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.154",
        port=5,
        username="rfsw",
        password="bdS%ztWG3v7%SjreCVA79wTPb",
    ),
    lmp_connection=SshServiceDetails(
        addr="10.71.217.231", username="nokia5G", password="noki@123"
    ),
    pdu_port=_ru1_pdu.pdu_ports[3],
    radio_type=RadioTypes.AEHC,
    attenuation_ports=[
        _attenuator1.attenuator_ports[5],
        _attenuator1.attenuator_ports[6],
        _attenuator1.attenuator_ports[7],
        _attenuator1.attenuator_ports[8],
    ],
)

_ru2_pdu = HBTE(addr="10.71.197.74", port_numbers=[1])

_ru2 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.158",
        port=12,
        username="rfsw",
        password="bdS%ztWG3v7%SjreCVA79wTPb",
    ),
    lmp_connection=SshServiceDetails(
        addr="10.0.176.71", username="nokia5G", password="noki@123"
    ),
    pdu_port=_ru2_pdu.pdu_ports[1],
    radio_type=RadioTypes.AEHB,
    attenuation_ports=[
        _attenuator1.attenuator_ports[13],
        _attenuator1.attenuator_ports[14],
        _attenuator1.attenuator_ports[15],
        _attenuator1.attenuator_ports[16],
    ],
)

_ru3_pdu = HBTE(addr="10.71.197.74", port_numbers=[2])

_ru3 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.162",
        port=3,
        username="rfsw",
        password="bdS%ztWG3v7%SjreCVA79wTPb",
    ),
    lmp_connection=SshServiceDetails(
        addr="10.0.176.70", username="mn5gran", password="nokia123@"
    ),
    pdu_port=_ru3_pdu.pdu_ports[2],
    radio_type=RadioTypes.AEHB,
    attenuation_ports=[
        _attenuator1.attenuator_ports[9],
        _attenuator1.attenuator_ports[10],
        _attenuator1.attenuator_ports[11],
        _attenuator1.attenuator_ports[12],
    ],
)

# #DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.71.215.167", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")

_gnb_pdu = TopYoung_PDU(addr="10.71.197.76", port_numbers=[1])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[1],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(
    airscale=_airscale,
    rus=[_ru1, _ru2, _ru3],
    f1_m_ip_addr="10.71.215.167",
)

# #CU
_cu = CU(
    backhaul_site_oam_ip="10.71.215.167",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.215.167", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.215.167", username="Nemuadmin", password="nemuuser"
    ),
)

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, global_bts_id="967", instance_id="967")

# #host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.92", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    connections=[_classical_bts],
)

_tl_cloud_topology = "CLOUD_5G_BB3"

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    core=_realcore,
    tl_cloud_topology=_tl_cloud_topology,
    # enbs=[_lte_real_enb],
    attenuator=[_attenuator1, _attenuator2],
    ues=[_xiaomi, _xiaomi2],
    appserver=_appserver,
    test_pcs=[_host],
)
