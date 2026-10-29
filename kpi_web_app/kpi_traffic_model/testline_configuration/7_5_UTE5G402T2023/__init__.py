__maintainer__ = "Li Chun"
__team__ = (
    "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_05_GMS <I_NSB_MN_5GSC_MMW_SC_PZ_HZ_05@internal.nsn.com>"
)
__email__ = "chun.li@nokia.com"

import os
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.gnb import CU, ClassicalBts
from taf.config.testline import DU, RU
from taf.config.testline.airscale import CapacityUnit, CommonUnit, Airscale
from taf.config.testline.pdu import TopYoung, FACOM, HBTE
from taf.config.testline.ue import Qualcomm, QualcommUeType, Android, MediaTek
from taf.config.testline.core import EPCSim, RealCore5G 
from taf.config.testline import RealEnb, RadioModule
from taf.config.testline import LicenseKeeper
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)

from taf.config.testline.attenuator import HBTE as AHBTE
from taf.config.testline.attenuator import AttenuationPort
from taf.config.testline.appserver import AppServer

## common
__all__ = ["tl"]
_CFG_DIR = os.path.dirname(os.path.abspath(__file__))
# Test PC
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.177.55", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
# HETE renamed as AHBTE, TopYoung renamed as ATopYoung
_attenuator = AHBTE(
    ip_addr="10.71.203.54",
    port=5000,
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
)
##epcsim
#_epc_sim = EPCSim(
#    mme_ip="10.110.227.5",
#    mcc="460",
#    mnc="2",
#    tac="0",
#    default_ssh_connection_details=SshServiceDetails(
#        addr="10.108.221.135", username="haijtest", password="Nokia@12345"
#    ),
#    edaemon_port=10000,
#    egate_port=20000,
#    dir_path="/opt/iphy/latest",
#    cfg_filename="LRC.cfg",
#)

# RealCore
_realcore = RealCore5G(mcc=262, mnc=3)

# 4GRU for RealEnb_1
#_ru_enb_1_pdu = HBTE(addr="10.68.87.10", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_ru_enb_1 = RadioModule(
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="usr", password="psswd"
    ),
)

# 4GRU for RealEnb_2
#_ru_enb_2_pdu = HBTE(addr="10.68.87.29", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
#_ru_enb_2 = RadioModule(
#    default_ssh_connection_details=SshServiceDetails(
#        addr="1.1.1.1", username="usr", password="psswd"
#    ),
#    pdu_port=_ru_enb_2_pdu.pdu_ports[5],
#)

# #RealEnb_1
_real_enb_1_pdu = HBTE(addr="10.68.87.13", port_numbers=[3])
_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.71.208.203", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_1_pdu.pdu_ports[3],
)
_real_enb_1 = Airscale(common_units=[_common_unit_2])
_lte_real_enb_1 = RealEnb(airscale=_real_enb_1, rms=_ru_enb_1)

##5GRU for classicalBTS
_ru_1_pdu = HBTE(addr="10.71.195.40", port_numbers=[2])
_ru_1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2", username="rfsw", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="mn5gran", password="noki@123"),
    pdu_port=_ru_1_pdu.pdu_ports[2],
    radio_type="AEHC",
)
#_ru_2_pdu = HBTE(addr="10.68.87.10", port_numbers=[5])
#_ru_2 = RU(
#    ru_hw_group="hw_group",
#    default_ssh_connection_details=SshServiceDetails(
#        addr="1.1.1.1", username="user", password="pass"
#    ),
#    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
#    pdu_port=_ru_2_pdu.pdu_ports[5],
#    radio_type="AHLOA",
#)


##DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(addr="192.168.253.20")
_gnb_pdu = HBTE(addr="10.71.195.42", port_numbers=[1])
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[1],
)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(airscale=_airscale, rus=[_ru_1], f1_m_ip_addr="10.71.202.139")

##CU
_cu = CU(
    backhaul_site_oam_ip="10.71.202.139",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.202.139", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.202.139", username="Nemuadmin", password="nemuuser"
    ),
)
##cloud_topology
_tl_cloud_topology = "CLOUD_5G_INVENTORY"

_classical_bts = ClassicalBts(
    dus=[_du], cu=_cu, instance_id="2023", global_bts_id="36917"
)

# SIGSPARK

_appserver_ssh = SshServiceDetails(
    addr="10.71.207.139", username="vrf3_sg5", password="vrf3@sg5", port="45378"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.207.139",
    iperf_path="/usr/bin/iperf",
    # iperf_path='/cygdrive/c/iperf',
    port="45181",
    ports=[45600, 45601, 45602, 45603, 45604, 45605, 45606, 45607],
)


spark_UE_0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.203.68", username="SPARK", password="SPARK"
    ),
    serial_number="57a5268",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.45/Bin/Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "sigspark_multiUE", "sigspark"],
    imsi="262033100013211",
)

spark_UE_1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.203.68", username="SPARK", password="SPARK"
    ),
    serial_number="57a526a",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.45/Bin/Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "sigspark_multiUE", "sigspark"],
    imsi="262033032993995",
)

spark_UE_2 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.203.68", username="SPARK", password="SPARK"
    ),
    serial_number="57a5319",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.45/Bin/Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "sigspark_multiUE", "sigspark"],
    imsi="460023100012829",
)

spark_UE_3 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.203.68", username="SPARK", password="SPARK"
    ),
    serial_number="57a53ea",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.45/Bin/Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "sigspark_multiUE", "sigspark"],
    imsi="262033100016920",
)

spark_UE_4 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.203.68", username="SPARK", password="SPARK"
    ),
    serial_number="57e52a2",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.45/Bin/Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "sigspark_multiUE", "sigspark"],
    imsi="262033100016919",
)

spark_UE_5 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.203.68", username="SPARK", password="SPARK"
    ),
    serial_number="57e52b0",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.45/Bin/Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "sigspark_multiUE", "sigspark"],
    imsi="262033100013209",
)

spark_UE_6 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.203.68", username="SPARK", password="SPARK"
    ),
    serial_number="57e52b1",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.45/Bin/Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "sigspark_multiUE", "sigspark"],
    imsi="262033032990252",
)

spark_UE_7 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.203.68", username="SPARK", password="SPARK"
    ),
    serial_number="57e52b2",
    server_dir="C:/Program Files (x86)/Spark1.1.2009.45/Bin/Spark.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "sigspark_multiUE", "sigspark"],
    imsi="262033100013216",
)


# #Qualcomm

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.207.139",
    iperf_path="iperf",
    port="44379",
)

_appserver = AppServer(_iperf_details_on_appserver)

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    core=_realcore,
    enbs=[_lte_real_enb_1],
    ues=[
        spark_UE_0,
        spark_UE_1,
        spark_UE_2,
        spark_UE_3,
        spark_UE_4,
        spark_UE_5,
        spark_UE_6,
        spark_UE_7,
    ],
    tl_cloud_topology=_tl_cloud_topology,
    attenuator=_attenuator,
)
