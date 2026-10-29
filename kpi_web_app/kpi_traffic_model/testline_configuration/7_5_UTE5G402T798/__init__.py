import os
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.core import EPCSim
from taf.config.testline import RU, DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, TopYoung, HBTE 
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CU, ClassicalBts
from taf.config.testline.ue import Android
from taf.config.testline import RealEnb, RadioModule
#from taf.config.testline.attenuator import HBTE
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline import Enb, SimEnb, RealEnb, RadioModule, LTEEmuEnb
from taf.compatibility.configuration import TestlineWrapper
#from taf.config.testline.mcs import HBTE


__maintainer__ = "Meng.4.li"
__team__ = "MN 5G RAN I&V 4 Pz HZG SG2"
__email__ = "meng.4.li@nokia.com"

## common
__all__ = ["tl"]

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

# Test PC
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.177.81", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)


##5GRU for classical BTS
_ru1_pdu = FACOM(addr="10.57.243.26", port_numbers=[4])

_ru1 = RU(
    #'AVQC SN=1M240305782'
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.26", username="serviceuser", password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og="
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.101.1", username="serviceuser", password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og="
    ),
    pdu_port=_ru1_pdu.pdu_ports[4],
)

_ru2_pdu = FACOM(addr="10.57.172.156", port_numbers=[4])

_ru2 = RU(
    #'AVQC SN=1M241500373'
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.10", username="serviceuser", password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og="
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.101.1", username="serviceuser", password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og="
    ),
    pdu_port=_ru2_pdu.pdu_ports[4],
)

##DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="6.6.6.6")

_gnb_pdu = HBTE(addr="10.57.242.43", port_numbers=[7])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[7],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru1, _ru2], f1_m_ip_addr="10.57.223.230")

##CU
_cu = CU(
    backhaul_site_oam_ip="10.57.223.230",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.223.230", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.223.230", username="Nemuadmin", password="nemuuser"
    ),
)

# cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id="798", global_bts_id="798")


# SIGSPARK*2 X65 UE
_ue_host1_ssh = SshServiceDetails(
    addr="10.57.130.55", username="mn5gran", password="nokia123@"
)

_spark_appserver_ssh = SshServiceDetails(
    # addr="10.57.191.244", username="cmw_sg2", password="cm@2"
    addr="10.57.191.244",
    username="vrf4_sg2",
    password="vrf4@sg2_123456",
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_spark_appserver_ssh,
    network_interface_address="10.57.130.55",
    iperf_path="/usr/bin/iperf",
    port=52228,
)

_sigspark1 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="4921203586015689841",
    server_dir="C:\Program Files (x86)\Spark1.1.2012.7\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262038001006438",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark2 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="4921203586015689841",
    server_dir="C:\Program Files (x86)\Spark1.1.2012.7\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262038001006319",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    ues=[
        _sigspark1,
        _sigspark2,
    ],
    tl_cloud_topology=_tl_cloud_topology,
)
