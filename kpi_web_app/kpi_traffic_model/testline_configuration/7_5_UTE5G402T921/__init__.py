__maintainer__ = "yzhai"
__team__ = "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_03@internal.nsn.com"  # TL owner's team
__email__ = "Yuxing.zhai@nokia.com"

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
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.core import EPCSim
from taf.config.testline.core import RealCore
from taf.config.testline.flexi import Flexi
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import ClassicalBts, CU
from taf.config.testline.enb import RealEnb
from taf.config.testline.ue import TM500, Android
from taf.config.testline import DU, RU
from taf.config.testline.attenuator import HBTE as AHBTE
from taf.config.testline.testpc import Connection
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, HBTE, FPFH
from taf.config.testline.radio import RadioModule
from taf.config.testline import IperfDataTransferDetails
from taf.config.testline.appserver import AppServer
from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

_attenuator = AHBTE(
    ip_addr="10.71.203.151", port="7", attenuation_port_numbers=[1, 2, 3, 4]
)

_lmp_connection_0 = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_0 = CapacityUnit(
    addr="192.168.253.17",
    hardware_type="ABIO",
)
_capacity_unit_1 = CapacityUnit(
    addr="192.168.253.18",
    hardware_type="ABIP",
)

# DU
_common_unit_pdu = HBTE(addr="10.57.176.88", port_numbers=[3])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection_0,
    capacity_units=[_capacity_unit_0, _capacity_unit_1],
    pdu_port=_common_unit_pdu.pdu_ports[3],
    hardware_type="ASIB",
)


_cu = CU(
    backhaul_site_oam_ip="10.57.226.228",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.226.228", username="toor4nsn", password="oZPS0POrRieRtu", port="22"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.226.228", username="Nemuadmin", password="nemuuser"
    ),
)



# 5G RU
_ru_pdu = FPFH(addr="10.57.176.88", port_numbers=[4])

_ru = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.17", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.17", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu.pdu_ports[4],
    radio_type=RadioTypes.AVHQA.value,
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
)



_appserver_ssh = SshServiceDetails(
    addr="10.71.207.147", username="vrf3_sg3", password="Vrf3@sg3Nokia", port="43567"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.207.147",
    iperf_path="/usr/bin/iperf",
    # iperf_path='/cygdrive/c/iperf',
    port="43567",
    ports=["43666", "43667", "43567", "43669", "43670", "43671", "43672", "43673"],
)

_cobham = TM500(
    tma_host=SshServiceDetails(
        addr="10.57.130.139", username="nokia5G", password="noki@123"
    ),
    tma_command_port=5004,
    iperf_details=_iperf,
    tma_path="/cygdrive/c/Program Files (x86)/Aeroflex/TM500/5G NR - NLA latest_version/Test Mobile Application/TmaApplication.exe",
)

# #Qualcomm

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.207.147",
    iperf_path="iperf",
    port="43567",
)

_appserver = AppServer(_iperf_details_on_appserver)

_android_0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.202", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="75cefbe3",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["qct_dx50"],
)
# #Qualcomm

_epcsim = EPCSim(
    mme_ip="192.168.4.1",
    mcc=777,
    mnc=44,
    tac=777,
    default_ssh_connection_details=SshServiceDetails(
        addr="10.47.199.241", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    dir_path="/opt/wts/latest",
    cfg_filename="TL101_basic_cfg_realLteEnb.cfg",
    edaemon_port="22222",
    egate_port="20021",
)

_du0_pdu = FPFH(
    addr="10.57.176.88",
    port_numbers=[3],
    login="admin",
    password="admin",
)
_ru1_pdu = FPFH(
    addr="10.57.176.88",
    port_numbers=[4],
    login="admin",
    password="admin",
)

_pdus = [_du0_pdu, _ru_pdu]

# airscale
_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru], f1_m_ip_addr="10.57.226.228")

# cloud_topology
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ANDROID_SA_ASIBL_ABIOB1_ABIPB2_AVHQA"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=10039, global_bts_id=10039)

# SIGSPARK
_ue_host_ssh = SshServiceDetails(
    addr="10.71.203.162", username="spark", password="spark"
)

_sigspark1 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="4abcfe3c",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.48/Bin/Spark.exe",
    python_path="C:/Python38",
    iperf_details=_iperf_details_on_appserver,
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="262033100000052",
)

_sigspark2 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="82ff39c2",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.48/Bin/Spark.exe",
    python_path="C:/Python38",
    iperf_details=_iperf_details_on_appserver,
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="262033100012824",
)

_sigspark3 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="fbc5c795",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.48/Bin/Spark.exe",
    python_path="C:/Python38",
    iperf_details=_iperf_details_on_appserver,
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="262033100000053",
)

_sigspark4 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="cfa1993e",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.48/Bin/Spark.exe",
    python_path="C:/Python38",
    iperf_details=_iperf_details_on_appserver,
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="262033100000058",
)

_sigspark5 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="342015c",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.48/Bin/Spark.exe",
    python_path="C:/Python38",
    iperf_details=_iperf_details_on_appserver,
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="262033100000055",
)

_sigspark6 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="133acf3b",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.48/Bin/Spark.exe",
    python_path="C:/Python38",
    iperf_details=_iperf_details_on_appserver,
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="262033100012824",
)

_sigspark7 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="1a8edebd",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.48/Bin/Spark.exe",
    python_path="C:/Python38",
    iperf_details=_iperf_details_on_appserver,
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="262033100000052",
)

_sigspark8 = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="abf29656",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.48/Bin/Spark.exe",
    python_path="C:/Python38",
    iperf_details=_iperf_details_on_appserver,
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
    imsi="262033100012824",
)

_fsp_1 = CapacityUnit(
    addr="192.168.253.20",
    hardware_type="ABIO",
    hardware_version="475266A.104",
    serial_number="L1213010405",
    rus=[_ru],
)

_fsp_2 = CapacityUnit(
    addr="192.168.253.24",
    hardware_type="ABIP",
    hardware_version="475266A.102",
    serial_number="L1233201705",
    rus=[_ru],
)

_fct_1 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.226.228", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_common_unit_pdu.pdu_ports[3],
    hardware_type="ASIB",
    hardware_version="A.102",
    serial_number="DH212871016",
    capacity_units=[_fsp_1, _fsp_2],
)

_smod_1 = Flexi([_fct_1])


_enb_sbts_1 = RealEnb(
    system_module=_smod_1,
    rms=[_ru],
    oam_ip=NetworkAddress("10.57.226.228"),
    instance_id=10039,
)

# Testpc
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.217.82", username="ute", password="uteUTE!"
    ),
    connections=[
        NetworkAddress(v4="192.168.255.126"),
        Connection(
            interface="eth1",
#            device=_classical_bts.dus[0].airscale.common_units[0],
            device=_enb_sbts_1.system_module.common_units[0],
            interface_type="lmp",
        )
    ],
)

tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_classical_bts],
    enbs=[_enb_sbts_1],
    core=RealCore(mcc=262, mnc=3),
    attenuator=_attenuator,
    ues=[_sigspark1, _sigspark2, _sigspark3, _sigspark4],
    appserver=_appserver,
    tl_cloud_topology=_tl_cloud_topology,
    pdus=_pdus,
)


__all__ = ["tl"]
