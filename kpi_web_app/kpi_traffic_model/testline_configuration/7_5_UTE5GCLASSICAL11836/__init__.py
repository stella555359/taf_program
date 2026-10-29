import os
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
from taf.config.testline.pdn import PDN, PDPTypes
from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.config.testline import LicenseKeeper

__maintainer__ = "Chen Xiaodong"
__team__ = "MN 5G RAN I&V 4 Pz HZG SG2"
__email__ = "xiaodong.d.chen@nokia-sbell.com"

## common
__all__ = ["tl"]

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

# Test PC
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.203.57", username="ute", password="ute"
    )
)

# #pdn
_pdns = [
    PDN(PDPTypes.IPV4V6.value, "dxdata4"),
    PDN(PDPTypes.IPV4V6.value, "ims"),
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
_attenuator = TopYoung(
    ip_addr="10.64.56.164",
    port=3000,
    attenuation_port_numbers=[1, 2, 3, 4],
    model="TAS16T16-51-120-1S-DES",
)

# Real 5G Core is used in real world.  here use EPCsim as the 5GC class is not implemented in tl config lib yet.
_epc_sim = EPCSim(
    mme_ip="10.110.133.68",
    mcc="262",
    mnc="03",
    tac="270",
    default_ssh_connection_details=SshServiceDetails(
        addr="10.110.227.70", username="haijtest", password="Nokia_12341"
    ),
    edaemon_port=10000,
    egate_port=20000,
    dir_path="/opt/iphy/latest",
    cfg_filename="LRC.cfg",
)

# RealEnb
_real_enb_pdu = FACOM(addr="10.64.49.35", port_numbers=[2])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.64.54.71", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[2],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=None)

##5GRU for classical BTS
_ru_pdu = FACOM(addr="10.64.49.36", port_numbers=[1])

_ru = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.37.131", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.101.1", username="user", password="pass"
    ),
    pdu_port=_ru_pdu.pdu_ports[1],
    radio_type=RadioTypes.AHCA,
    signal_analyzer=None,
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
)


##DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.64.54.71", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="6.6.6.6")

_gnb_pdu = FACOM(addr="10.57.242.45", port_numbers=[2])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[2],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru], f1_m_ip_addr="10.64.54.71")

##CU
_cu = CU(
    backhaul_site_oam_ip="10.64.54.71",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.64.54.71", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.64.54.71", username="Nemuadmin", password="nemuuser"
    ),
)

##cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id="1", global_bts_id="37373")

##HBTE_MCS
_hbte = HBTE(
    ip_addr="10.64.56.164",
    port="5000",
    mcs_port_numbers=[1],
    model="PPSAM-64X16-2.3-3.8-90-0.5-360-1-A",
)

# SIGSPARK
_ue_host1_ssh = SshServiceDetails(
    addr="10.64.57.20", username="mn5gran", password="nokia123@"
)

_spark_appserver_ssh = SshServiceDetails(
    addr="10.57.162.6", username="vrf4_sg11", password="vrf4@11"
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_spark_appserver_ssh,
    network_interface_address="10.57.162.6",
    iperf_path="iperf",
    port=21001,
)

_licensekeeper = LicenseKeeper(username="yu.2.li@nokia-sbell.com", password="nokia123")

_sigspark1 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="7ad5ce4f",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.11/Bin/Spark.exe",
    python_path="C:/Python39",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033032996510",
#    capabilities=["REAL_UE", "REAL_ANDROID_UE", "sigspark_multiUE"],
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "huawei_sigspark"],
    licensekeeper=_licensekeeper,	
)

_sigspark2 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="e35b64d0",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.11/Bin/Spark.exe",
    python_path="C:/Python39",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033032996503",
#    capabilities=["REAL_UE", "REAL_ANDROID_UE", "sigspark_multiUE"],
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "huawei_sigspark"],	
    licensekeeper=_licensekeeper,	
)

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    enbs=[_lte_real_enb],
    core=_realcore,
    attenuator=_attenuator,
    mcses=_hbte,
    ues=[
        _sigspark1,
        _sigspark2,
    ],
    tl_cloud_topology=_tl_cloud_topology,
)
