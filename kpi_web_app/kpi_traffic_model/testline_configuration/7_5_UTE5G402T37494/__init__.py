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
from taf.config.testline.attenuator import HBTE as HBTEPA
from taf.config.testline.pdu import TopYoung as pdu_TopYoung
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


__maintainer__ = "LICHNAGYAN"
__team__ = "MN 5G RAN I&V 4 Pz HZG SG13"
__email__ = "changyan.li@nokia-sbell.com"

## common
__all__ = ["tl"]

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

##cloud_topology
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ASIML_ABIPB1B2_AVHQA"

_attenuator = HBTEPA(
    ip_addr="10.57.147.148",
    port=5000,
    attenuation_port_numbers=[1, 2, 3, 4, 9, 10, 11, 12,15,16,17,18,129,162,195,228],
    model="PA-16-16-6-127-0.5-B-S",
)
#5GRU for classical BTS
_ru_pdu_0 = pdu_TopYoung(addr="10.57.247.218", port_numbers=[1])

_ru_0 = RU(
    ru_hw_group="hw_group",
    # default_ssh_connection_details=SshServiceDetails(
    #     addr="172.22.0.154",
    #     username="rfsw",
    #     password="bdS%ztWG3v7%SjreCVA79wTPb"
    # ),
    pdu_port=_ru_pdu_0.pdu_ports[1],
    radio_type=RadioTypes.AVQC,
    serial_number="1M240305775",
)


##DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20", hardware_type="ABIP")

_gnb_pdu = pdu_TopYoung(addr="10.57.247.218", port_numbers=[3])

_ru_cablinks = [
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=1),
        target=Endpoint(unit=_ru_0, label="SFP", port_id=2),
    )
]

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[3],
    hardware_type="ASIM",
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru_0], f1_m_ip_addr="10.57.149.2")


##CU
_cu = CU(
    backhaul_site_oam_ip="10.57.149.2",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.149.2", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.149.2", username="Nemuadmin", password="nemuuser"
    ),
)

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id="37494", global_bts_id="37494")

# Test PC
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.251.33", username="ute", password="uteUTE!"
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
# _attenuator = TopYoung(
#     ip_addr="10.57.147.146",
#     port=28888,
#     attenuation_port_numbers=[1, 2, 3, 4],
#     model="MCS2338A2-64B16-A4",
# )


# SIGSPARK
_ue_host1_ssh = SshServiceDetails(
    addr="10.57.147.147", username="spark", password="spark"
)

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
    serial_number="36223656",
    server_dir="C:\Program Files (x86)\Spark1.1.2009.33\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033031397757",
    capabilities=["huawei_sigspark"],
)

_sigspark2 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="26901544",
    server_dir="C:\Program Files (x86)\Spark1.1.2009.33\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033031397661",
    capabilities=["huawei_sigspark"],
)

_sigspark3 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="40235955",
    server_dir="C:\Program Files (x86)\Spark1.1.2009.33\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033031397823",
    capabilities=["huawei_sigspark"],
)

_sigspark4 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="10835129",
    server_dir="C:\Program Files (x86)\Spark1.1.2009.33\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033031397826",
    capabilities=["huawei_sigspark"],
)

_sigspark5 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="13893854",
    server_dir="C:\Program Files (x86)\Spark1.1.2009.33\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033031397732",
    capabilities=["huawei_sigspark"],
)

_sigspark6 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="31851393",
    server_dir="C:\Program Files (x86)\Spark1.1.2009.33\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033031397852",
    capabilities=[ "huawei_sigspark"],
)

_sigspark7 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="14097099",
    server_dir="C:\Program Files (x86)\Spark1.1.2009.33\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033031397822",
    capabilities=["huawei_sigspark"],
)

_sigspark8 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="14220491",
    server_dir="C:\Program Files (x86)\Spark1.1.2009.33\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033030357429",
    capabilities=["huawei_sigspark"],
)


tl = TestLine(
    test_pc=_test_pc,  #(DEPRECATED, will be removed in 9.0.0) TestPc object class
    test_pcs=[_test_pc],
    gnbs=[_classical_bts],
    core=RealCore(mcc=262, mnc=3),
    attenuator = _attenuator,
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
