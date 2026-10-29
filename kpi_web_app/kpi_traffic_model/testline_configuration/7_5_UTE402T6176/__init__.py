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
from taf.config.testline import DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, HBTE
from taf.config.testline.pdu import TopYoung as pdu_TopYoung
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CU, ClassicalBts
from taf.config.testline.ue import Android
from taf.config.testline.gnb.du import Cablink, Endpoint
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.config.testline.attenuator import AttenuationPort, TopYoung
from taf.config.testline.appserver import AppServer


__maintainer__ = "l3gao"
__team__ = "MN 5G RAN I&V 4 Pz HZG SG13"
__email__ = "changyan.li@nokia-sbell.com"

__all__ = ["tl"]

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

# cloud topology
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ASILL_ABIPB1_ABIAB2_ABIOB3_AVHA"

# --------------------------
# PDU
# --------------------------

_pdu_1 = HBTE(
    addr="10.57.234.36",
    port_numbers=[1, 2, 3, 4, 5, 6],
)

_pdu_2 = HBTE(
    addr="10.57.234.22",
    port_numbers=[1, 2, 3, 4, 5, 6],
)

# --------------------------
# RU
# --------------------------

_ru_0 = RU(
    ru_hw_group="hw_group",
    pdu_port=_pdu_2.pdu_ports[4],
    radio_type=RadioTypes.AVHA,
    serial_number="1M240305775",
)

# --------------------------
# DU / Airscale / Units
# --------------------------

_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20", hardware_type="ABIP")

_ru_cablinks = [
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=1),
        target=Endpoint(unit=_ru_0, label="SFP", port_id=2),
    )
]

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_pdu_1.pdu_ports[3],
    hardware_type="ASIL",
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(
    airscale=_airscale,
    rus=[_ru_0],
    f1_m_ip_addr="10.57.224.230",
)

# --------------------------
# CU
# --------------------------

_cu = CU(
    backhaul_site_oam_ip="10.57.224.230",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.224.230", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.224.230", username="Nemuadmin", password="nemuuser"
    ),
)

# --------------------------
# Classical BTS
# --------------------------

_classical_bts = ClassicalBts(
    dus=[_du],
    cu=_cu,
    instance_id="6176",
    global_bts_id="6176",
)

# --------------------------
# Test PC
# --------------------------

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.217.80", username="ute", password="uteUTE!"
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_classical_bts.dus[0].airscale.common_units[0],
            interface_type="lmp",
        )
    ],
)

# --------------------------
# UE + AppServer
# --------------------------

_tm500_host_ssh = SshServiceDetails(
    addr="10.57.130.38", username="MN5GRAN", password="nokia123@"
)

_ue_host1_ssh = SshServiceDetails(
    addr="10.57.147.147", username="spark", password="spark"
)

_spark_appserver_ssh = SshServiceDetails(
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

# --------------------------
# Android UEs
# --------------------------


_sigspark1 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="a6aebc81",
    server_dir="C:\Program Files (x86)\Spark1.1.2009.15\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033031397733",
    capabilities=["huawei_sigspark"],
)

_sigspark2 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="8346d45e",
    server_dir="C:\Program Files (x86)\Spark1.1.2009.15\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033031397695",
    capabilities=["huawei_sigspark"],
)

_sigspark3 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="95b89491",
    server_dir="C:\Program Files (x86)\Spark1.1.2009.15\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033031397689",
    capabilities=["huawei_sigspark"],
)

_sigspark4 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="b8c9f669",
    server_dir="C:\Program Files (x86)\Spark1.1.2009.15\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033031397734",
    capabilities=["huawei_sigspark"],
)

_sigspark5 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="637d7e3b",
    server_dir="C:\Program Files (x86)\Spark1.1.2009.15\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033031397855",
    capabilities=["huawei_sigspark"],
)

_sigspark6 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="b1fdf16a",
    server_dir="C:\Program Files (x86)\Spark1.1.2009.15\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033031397853",
    capabilities=[ "huawei_sigspark"],
)

_sigspark7 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="b4f0f8ab",
    server_dir="C:\Program Files (x86)\Spark1.1.2009.15\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033031397663",
    capabilities=["huawei_sigspark"],
)

_sigspark8 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="8f0f9cd",
    server_dir="C:\Program Files (x86)\Spark1.1.2009.15\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033031397708",
    capabilities=["huawei_sigspark"],
)
_viaviue0 = Android(
    ssh_connection_details=_tm500_host_ssh,
    serial_number="8f0f9cd",
    server_dir="C:\Program Files (x86)\Spark1.1.2009.15\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033031397708",
    capabilities=["huawei_sigspark"],
)

_viaviue1 = Android(
    ssh_connection_details=_tm500_host_ssh,
    serial_number="8f0f9cd",
    server_dir="C:\Program Files (x86)\Spark1.1.2009.15\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033031397708",
    capabilities=["huawei_sigspark"],
)


# --------------------------
# TestLine
# --------------------------

tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_classical_bts],
    core=RealCore(mcc=262, mnc=3),
    ues=[
        _viaviue0,
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
