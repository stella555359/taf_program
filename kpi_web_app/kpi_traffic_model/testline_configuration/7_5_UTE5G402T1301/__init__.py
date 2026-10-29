import os
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.core import RealCore
from taf.config.testline.testpc import TestPc, Connection
from taf.config.testline.core import EPCSim
from taf.config.testline import RU, DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, HBTE
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CU, ClassicalBts
from taf.config.testline.ue import Android
from taf.config.testline import RealEnb, RadioModule
#from taf.config.testline.attenuator import HBTE
from taf.config.testline.gnb.du import Cablink, Endpoint
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline import Enb, SimEnb, RealEnb, RadioModule, LTEEmuEnb
#from taf.compatibility.configuration import TestlineWrapper
#from taf.config.testline.mcs import HBTE
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.config.testline.attenuator import (
    AttenuationPort,
    TopYoung,
)
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)
from taf.config.testline.appserver import AppServer


__maintainer__ = "LICHNAGYAN"
__team__ = "MN 5G RAN I&V 4 Pz HZG SG13"
__email__ = "changyan.li@nokia-sbell.com"

## common
__all__ = ["tl"]

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

##cloud_topology
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ASILL_ABIOB1_3xAEHC_ENB_VEFHAZ4"


#5GRU for classical BTS
_ru_pdu_0 = HBTE(addr="10.57.234.4", port_numbers=[1])

_ru_0 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.154", 
        username="rfsw", 
        password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    #lmp_connection=SshServiceDetails(
    #    addr="192.168.101.1", username="user", password="pass"
    #},
    pdu_port=_ru_pdu_0.pdu_ports[1],
    radio_type=RadioTypes.AEHC,
    serial_number="L1210602520",
)

_ru_pdu_1 = HBTE(addr="10.57.234.4", port_numbers=[2])

_ru_1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.162", 
        username="rfsw", 
        password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    #lmp_connection=SshServiceDetails(
    #    addr="192.168.101.1", username="user", password="pass"
    #},
    pdu_port=_ru_pdu_1.pdu_ports[2],
    radio_type=RadioTypes.AEHC,
    serial_number="L1211203222",
)


_ru_pdu_2 = HBTE(addr="10.57.234.4", port_numbers=[5])

_ru_2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.158", 
        username="rfsw", 
        password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    #lmp_connection=SshServiceDetails(
    #    addr="192.168.101.1", username="user", password="pass"
    #},
    pdu_port=_ru_pdu_2.pdu_ports[5],
    radio_type=RadioTypes.AEHC,
    serial_number="L1213413668",
)


##DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20", hardware_type="ABIO")

_gnb_pdu = HBTE(addr="10.57.234.2", port_numbers=[1])

_ru_cablinks = [
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=1),
        target=Endpoint(unit=_ru_0, label="SFP", port_id=2),
    )
]

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[1],
    hardware_type="ASIL",
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru_0,_ru_1,_ru_2], f1_m_ip_addr="10.57.149.99")


##CU
_cu = CU(
    backhaul_site_oam_ip="10.57.149.99",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.149.99", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.149.99", username="Nemuadmin", password="nemuuser"
    ),
)

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id="10317", global_bts_id="10317")

# Test PC
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.251.51", username="ute", password="uteUTE!"
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_classical_bts.dus[0].airscale.common_units[0],
            interface_type="lmp",
        )
    ],
)

# attenuator
_attenuator = TopYoung(
    ip_addr="10.57.147.210",
    port=28888,
    attenuation_port_numbers=[1, 2, 3, 4],
    model="MCS2338A2-64B16-A4",
)


# SIGSPARK
_ue_host1_ssh = SshServiceDetails(
    addr="10.57.147.4", username="spark", password="spark"
)

# _spark_appserver_ssh = SshServiceDetails(
#     # addr="10.57.163.35",username="cmw_sg2",password="12345678"
#     addr="10.106.164.200",
#     username="ute",
#     password="%EjvHVvvkQD6",
#)
#
#
# _iperf_details_on_appserver = IperfDataTransferDetails(
#     ssh_connection_details=_spark_appserver_ssh,
#     network_interface_address="10.106.164.200",
#     iperf_path="iperf",
#     port="56578",
# )

_spark_appserver_ssh = SshServiceDetails(
    # addr="10.57.163.35",username="cmw_sg2",password="12345678"
     addr="10.57.191.242",
     username="vrf4_sg13",
     password="vrf4@sg13",
)


_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_spark_appserver_ssh,
    network_interface_address="10.57.191.242",
    iperf_path="iperf",
    port="56578",
)

_iperf_details_on_appserver2 = IperfDataTransferDetails(
    ssh_connection_details=_spark_appserver_ssh,
    network_interface_address="10.57.191.242",
    iperf_path="/usr/bin/iperf",
    port="56579",
)

_appserver = AppServer(_iperf_details_on_appserver2)

_sigspark1 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="17142156",
    server_dir="C:\Program Files (x86)\Spark1.1.2008.60\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033100011004",
    capabilities=["huawei_sigspark"],
)

_sigspark2 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="21774205",
    server_dir="C:\Program Files (x86)\Spark1.1.2008.60\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033100011000",
    capabilities=["huawei_sigspark"],
)

_sigspark3 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="77518950",
    server_dir="C:\Program Files (x86)\Spark1.1.2008.60\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033100010996",
    capabilities=["huawei_sigspark"],
)

_sigspark4 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="10220778",
    server_dir="C:\Program Files (x86)\Spark1.1.2008.60\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033100011003",
    capabilities=["huawei_sigspark"],
)

_sigspark5 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="30257237",
    server_dir="C:\Program Files (x86)\Spark1.1.2008.60\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033100010999",
    capabilities=["huawei_sigspark"],
)

_sigspark6 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="30257237",
    server_dir="C:\Program Files (x86)\Spark1.1.2008.60\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033100011001",
    capabilities=[ "huawei_sigspark"],
)

_sigspark7 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="30257237",
    server_dir="C:\Program Files (x86)\Spark1.1.2008.60\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033100011006",
    capabilities=["huawei_sigspark"],
)

_sigspark8 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="34374805",
    server_dir="C:\Program Files (x86)\Spark1.1.2008.60\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033100011007",
    capabilities=["huawei_sigspark"],
)


tl = TestLine(
    test_pc=_test_pc,  #(DEPRECATED, will be removed in 9.0.0) TestPc object class
    test_pcs=[_test_pc],
    gnbs=[_classical_bts],
    core=RealCore(mcc=262, mnc=3),
    #mcses=[_attenuator],
    ues=[
        _sigspark1,
        _sigspark2,
        _sigspark3,
        _sigspark4,
        _sigspark5,
        _sigspark6,
        _sigspark7,
        _sigspark8,
    ],
    tl_cloud_topology=_tl_cloud_topology,
    appserver=_appserver,
)
