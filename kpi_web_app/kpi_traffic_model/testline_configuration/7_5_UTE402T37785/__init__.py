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
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, HBTE, FPFH
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


__maintainer__ = "TangShaoyong"
__team__ = "MN 5G RAN I&V 4 Pz HZG SG13"
__email__ = "shaoyong.tang@nokia.com"

## common
__all__ = ["tl"]

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

##cloud_topology
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ASIM_ABIP_1xAVQC_2xAVQD"


#5GRU for classical BTS
_ru_pdu_0 = FPFH(addr="10.71.196.68", port_numbers=[4])

_ru_0 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.10.162", 
        username="serviceuser", 
        password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og="
    ),
    #lmp_connection=SshServiceDetails(
    #    addr="192.168.101.1", username="user", password="pass"
    #},
    pdu_port=_ru_pdu_0.pdu_ports[4],
    radio_type=RadioTypes.AEQY,
    serial_number="1M202722864",
)

_ru_pdu_1 = FPFH(addr="10.71.196.68", port_numbers=[2])

_ru_1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.10.154", 
        username="serviceuser", 
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=" 
    ),
    #lmp_connection=SshServiceDetails(
    #    addr="192.168.101.1", username="user", password="pass"
    #},
    pdu_port=_ru_pdu_1.pdu_ports[2],
    radio_type=RadioTypes.AVQD,
    serial_number="1M242501185",
)

_ru_pdu_2 = FPFH(addr="10.71.196.68", port_numbers=[5])

_ru_2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.10.158", 
        username="serviceuser", 
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=" 
    ),
    #lmp_connection=SshServiceDetails(
    #    addr="192.168.101.1", username="user", password="pass"
    #},
    pdu_port=_ru_pdu_2.pdu_ports[5],
    radio_type=RadioTypes.AVQD,
    serial_number="1M242501186",
)

##DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_0 = CapacityUnit(addr="192.168.253.20", hardware_type="ABIO")
_gnb_pdu = HBTE(addr="10.71.196.66", port_numbers=[3])

_ru_cablinks = [
    Cablink(
        source=Endpoint(unit=_capacity_unit_0, label="SFP", port_id=7),
        target=Endpoint(unit=_ru_1, label="SFP", port_id=1),
    ),
        Cablink(
        source=Endpoint(unit=_capacity_unit_0, label="SFP", port_id=8),
        target=Endpoint(unit=_ru_2, label="SFP", port_id=1),
    ),
        Cablink(
        source=Endpoint(unit=_capacity_unit_0, label="SFP", port_id=9),
        target=Endpoint(unit=_ru_0, label="SFP", port_id=1),
    )
]

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit_0],
    pdu_port=_gnb_pdu.pdu_ports[3],
    hardware_type="ASIM",
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru_0,_ru_1], f1_m_ip_addr="10.71.212.5",cablinks=_ru_cablinks)


##CU
_cu = CU(
    backhaul_site_oam_ip="10.71.212.5",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.212.5", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.212.5", username="Nemuadmin", password="nemuuser"
    ),
)

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id="37785", global_bts_id="37785")

# Test PC
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.57", username="ute", password="iW_K#8.ute%A10h0m0ra"
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
    ip_addr="10.57.156.242",
    port=28888,
    attenuation_port_numbers=[1, 2, 3, 4],
    model="HBTE PA 16-16",
)


# SIGSPARK
_ue_host1_ssh = SshServiceDetails(
    addr="10.71.205.2", username="spark", password="spark_err_err_err"
)

_spark_appserver_ssh = SshServiceDetails(
    # addr="10.57.163.35",username="cmw_sg2",password="12345678"
     addr="10.57.149.138",
     username="ute",
     password="Ut3pa5s#ff97",
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_spark_appserver_ssh,
    network_interface_address="10.57.149.138",
    iperf_path="iperf",
    port="33000",
)

_iperf_details_on_appserver2 = IperfDataTransferDetails(
    ssh_connection_details=_spark_appserver_ssh,
    network_interface_address="10.57.149.138",
    iperf_path="/usr/bin/iperf",
    port="33100",
)

_appserver = AppServer(_iperf_details_on_appserver2)

_sigspark0 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="0000000",
    server_dir="C:\Program Files (x86)\Spark1.1.2013.2\Bin\Spark.exe",
    python_path="C:/Program Files/Python310",
    iperf_details=_iperf_details_on_appserver,
    imsi="00000000000",
    capabilities=["huawei_sigspark"],
)

_sigspark1 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="32262124",
    server_dir="C:\Program Files (x86)\Spark1.1.2013.2\Bin\Spark.exe",
    python_path="C:/Program Files/Python310",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033031397709",
    capabilities=["huawei_sigspark"],
)

_sigspark2 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="38527208",
    server_dir="C:\Program Files (x86)\Spark1.1.2013.2\Bin\Spark.exe",
    python_path="C:/Program Files/Python310",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033031397710",
    capabilities=["huawei_sigspark"],
)

_sigspark3 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="61863501",
    server_dir="C:\Program Files (x86)\Spark1.1.2013.2\Bin\Spark.exe",
    python_path="C:/Program Files/Python310",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033031397711",
    capabilities=["huawei_sigspark"],
)

_sigspark4 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="32182383",
    server_dir="C:\Program Files (x86)\Spark1.1.2013.2\Bin\Spark.exe",
    python_path="C:/Program Files/Python310",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033031397712",
    capabilities=["huawei_sigspark"],
)

_sigspark5 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="69037490",
    server_dir="C:\Program Files (x86)\Spark1.1.2013.2\Bin\Spark.exe",
    python_path="C:/Program Files/Python310",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033031397713",
    capabilities=["huawei_sigspark"],
)

_sigspark6 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="46683158",
    server_dir="C:\Program Files (x86)\Spark1.1.2013.2\Bin\Spark.exe",
    python_path="C:/Program Files/Python310",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033031397714",
    capabilities=["huawei_sigspark"],
)

_sigspark7 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="39594427",
    server_dir="C:\Program Files (x86)\Spark1.1.2013.2\Bin\Spark.exe",
    python_path="C:/Program Files/Python310",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033031397716",
    capabilities=["huawei_sigspark"],
)

_sigspark8 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="78036614",
    server_dir="C:\Program Files (x86)\Spark1.1.2013.2\Bin\Spark.exe",
    python_path="C:/Program Files/Python310",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033031397715",
    capabilities=["huawei_sigspark"],
)


tl = TestLine(
    test_pc=_test_pc,  #(DEPRECATED, will be removed in 9.0.0) TestPc object class
    test_pcs=[_test_pc],
    gnbs=[_classical_bts],
    core=RealCore(mcc=262, mnc=3),
    #mcses=[_attenuator],
    ues=[
        _sigspark0,
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
