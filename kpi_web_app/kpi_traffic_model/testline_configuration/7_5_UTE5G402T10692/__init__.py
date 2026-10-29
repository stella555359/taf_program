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
from taf.config.testline.gnb.du import Cablink, Endpoint
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline import Enb, SimEnb, RealEnb, RadioModule, LTEEmuEnb
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


__maintainer__ = "changyli"
__team__ = "MN 5G RAN I&V 4 Pz HZG SG13"
__email__ = "changyan.li@nokia-sbell.com"

## common
__all__ = ["tl"]

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

##cloud_topology
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ASIML_ABIPB12_ABIOB3_2XAVQD_2XAVQC"


#5GRU for classical BTS
_ru_pdu_0 = HBTE(addr="10.57.234.11", port_numbers=[6])

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
    pdu_port=_ru_pdu_0.pdu_ports[6],
    radio_type=RadioTypes.AVQD,
    serial_number="1M242501192",
)

_ru_pdu_1 = HBTE(addr="10.57.234.11", port_numbers=[1])

_ru_1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.154",
        username="rfsw",
        password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    #lmp_connection=SshServiceDetails(
    #    addr="192.168.101.1", username="user", password="pass"
    #},
    pdu_port=_ru_pdu_1.pdu_ports[1],
    radio_type=RadioTypes.AVQC,
    serial_number="1M242100011",
)

_ru_pdu_2 = HBTE(addr="10.57.234.11", port_numbers=[2])

_ru_2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.154",
        username="rfsw",
        password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    #lmp_connection=SshServiceDetails(
    #    addr="192.168.101.1", username="user", password="pass"
    #},
    pdu_port=_ru_pdu_2.pdu_ports[2],
    radio_type=RadioTypes.AVQC,
    serial_number="1M243200004",
)

_ru_pdu_3 = HBTE(addr="10.57.234.11", port_numbers=[3])

_ru_3 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.154",
        username="rfsw",
        password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    #lmp_connection=SshServiceDetails(
    #    addr="192.168.101.1", username="user", password="pass"
    #},
    pdu_port=_ru_pdu_3.pdu_ports[3],
    radio_type=RadioTypes.AVQD,
    serial_number="1M242501191",
)


##DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20", hardware_type="ABIP")

_gnb_pdu = HBTE(addr="10.57.228.226", port_numbers=[1])

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
    hardware_type="ASIM",
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru_0,_ru_1,_ru_2,_ru_3], f1_m_ip_addr="10.57.228.226")


##CU
_cu = CU(
    backhaul_site_oam_ip="10.57.228.226",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.228.226", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.228.226", username="Nemuadmin", password="nemuuser"
    ),
)

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id="10692", global_bts_id="10692")

# Test PC
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.159.76", username="ute", password="iW_K#8.ute%A10h0m0ra"
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
    ip_addr="10.57.230.164",
    port=28888,
    attenuation_port_numbers=[1, 2, 3, 4],
    model="MCS2338A2-64B16-A4",
)


# SIGSPARK
_ue_host1_ssh = SshServiceDetails(
    addr="10.57.230.165", username="spark", password="spark"
)


_spark_appserver_ssh = SshServiceDetails(
    # addr="10.57.163.35",username="cmw_sg2",password="12345678"
     addr="10.21.41.19",
     username="vrf4_sg13",
     password="vrf4@13",
)


_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_spark_appserver_ssh,
    network_interface_address="10.21.41.19",
    iperf_path="iperf",
    port="56578",
)

_iperf_details_on_appserver2 = IperfDataTransferDetails(
    ssh_connection_details=_spark_appserver_ssh,
    network_interface_address="10.21.41.19",
    iperf_path="/usr/bin/iperf",
    port="56579",
)

_appserver = AppServer(_iperf_details_on_appserver2)

_sigspark1 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="32839578",
    server_dir="C:\Program Files (x86)\Spark1.1.2009.45\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033031397859",
    capabilities=["huawei_sigspark"],
)

_sigspark2 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="43273755",
    server_dir="C:\Program Files (x86)\Spark1.1.2009.45\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033031397761",
    capabilities=["huawei_sigspark"],
)

_sigspark3 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="96395590",
    server_dir="C:\Program Files (x86)\Spark1.1.2009.45\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033031397854",
    capabilities=["huawei_sigspark"],
)

_sigspark4 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="29959031",
    server_dir="C:\Program Files (x86)\Spark1.1.2009.45\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033100011099",
    capabilities=["huawei_sigspark"],
)

_sigspark5 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="11455307",
    server_dir="C:\Program Files (x86)\Spark1.1.2009.45\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033031397664",
    capabilities=["huawei_sigspark"],
)

_sigspark6 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="40009666",
    server_dir="C:\Program Files (x86)\Spark1.1.2009.45\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033031397770",
    capabilities=[ "huawei_sigspark"],
)

_sigspark7 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="37941893",
    server_dir="C:\Program Files (x86)\Spark1.1.2009.45\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033031397825",
    capabilities=["huawei_sigspark"],
)

_sigspark8 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="18279805",
    server_dir="C:\Program Files (x86)\Spark1.1.2009.45\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033030360162",
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
