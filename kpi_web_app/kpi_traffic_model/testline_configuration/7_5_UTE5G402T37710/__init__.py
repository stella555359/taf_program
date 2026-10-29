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
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.core import EPCSim, LTEEmuCore, PrismaCore
from taf.config.testline import RU, DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, HBTE
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import (
    AirphoneCloud,
    Airphone,
    Prisma,
    TM500,
    Qualcomm,
    QualcommUeType,
    Android,
    MediaTek,
    LicenseKeeper,
)
from taf.config.testline import (
    Enb,
    SimEnb,
    RealEnb,
    RadioModule,
    LTEEmuEnb,
    PrismaEnb,
    DocomoEnb,
)
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.appserver import AppServer

__maintainer__ = "Chen Tong"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_2_GMS <I_MN_5G_RAN_IV4_LINE_HZG_2@internal.nsn.com>"
)
__email__ = "tong.chen@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# SIGSPARK
_ue_host_ssh = SshServiceDetails(
    addr="10.57.130.237", username="MN5GRAN", password="nokia123@"
)

_spark_appserver_ssh = SshServiceDetails(
    addr="10.57.191.244", username="vrf4_sg2", password="Vrf4@sg2_123456"
)
_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_spark_appserver_ssh,
    network_interface_address="10.57.191.244",
    iperf_path="iperf",
    port=52221,
)

# CI_Detail_UE_Type='Huawei Mate 20'
_sigspark = Android(
    ssh_connection_details=_ue_host_ssh,
    serial_number="7TD5T21610004690",
    server_dir="C:/Program Files (x86)/Spark1.1.2008.13/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="460023100012846",
    licensekeeper=LicenseKeeper(username="HAZ4_SG2", password="HAZ4_SG2"),
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

# 5GRU for classicalBTS
_ru_0_pdu = HBTE(addr="10.71.197.15", port_numbers=[1])

_ru_0 = RU(
    #'AVQC'
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.53", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.53", username="root", password="umniedziala"
    ),
    pdu_port=_ru_0_pdu.pdu_ports[1],
    radio_type=RadioTypes.AVQC,
    serial_number="1M242100017",
)

_ru_1_pdu = HBTE(addr="10.71.197.15", port_numbers=[4])

_ru_1 = RU(
    #'AVQC'
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.53", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.53", username="root", password="umniedziala"
    ),
    pdu_port=_ru_1_pdu.pdu_ports[4],
    radio_type=RadioTypes.AVQC,
    serial_number="1M250305326",
)

_ru_2_pdu = HBTE(addr="10.71.197.75", port_numbers=[1])

_ru_2 = RU(
    #'AHEGB'
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.53", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.53", username="root", password="umniedziala"
    ),
    pdu_port=_ru_2_pdu.pdu_ports[1],
    radio_type=RadioTypes.AHEGB,
    serial_number="DH241131447",
)

_ru_3_pdu = HBTE(addr="10.71.197.75", port_numbers=[3])

_ru_3 = RU(
    #'AHEGB'
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.53", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.53", username="root", password="umniedziala"
    ),
    pdu_port=_ru_3_pdu.pdu_ports[3],
    radio_type=RadioTypes.AHEGB,
    serial_number="K9184605243",
)

_ru_4_pdu = HBTE(addr="10.71.197.75", port_numbers=[2])

_ru_4 = RU(
    #'AHEGB'
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.53", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.53", username="root", password="umniedziala"
    ),
    pdu_port=_ru_4_pdu.pdu_ports[2],
    radio_type=RadioTypes.AHEGB,
    serial_number="EA204150627",
)

_ru_5_pdu = HBTE(addr="10.71.197.76", port_numbers=[2])

_ru_5 = RU(
    #'AHEH'
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.53", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.53", username="root", password="umniedziala"
    ),
    pdu_port=_ru_5_pdu.pdu_ports[2],
    radio_type=RadioTypes.AHEH,
    serial_number="EA213657732",
)

_ru_6_pdu = HBTE(addr="10.71.197.76", port_numbers=[4])

_ru_6 = RU(
    #'AHEH'
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.53", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.53", username="root", password="umniedziala"
    ),
    pdu_port=_ru_6_pdu.pdu_ports[4],
    radio_type=RadioTypes.AHEH,
    serial_number="EA203951051",
)

_ru_7_pdu = HBTE(addr="10.71.197.76", port_numbers=[5])

_ru_7 = RU(
    #'AHEH'
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.53", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.53", username="root", password="umniedziala"
    ),
    pdu_port=_ru_7_pdu.pdu_ports[5],
    radio_type=RadioTypes.AHEH,
    serial_number="EA213657729",
)

_ru_8_pdu = HBTE(addr="10.71.197.76", port_numbers=[3])

_ru_8 = RU(
    #'AHEH'
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.53", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.53", username="root", password="umniedziala"
    ),
    pdu_port=_ru_8_pdu.pdu_ports[3],
    radio_type=RadioTypes.AHEH,
    serial_number="EA213657657",
)

_ru_9_pdu = HBTE(addr="10.71.197.80", port_numbers=[3])

_ru_9 = RU(
    #'FXED'
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.53", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.53", username="root", password="umniedziala"
    ),
    pdu_port=_ru_9_pdu.pdu_ports[3],
    radio_type=RadioTypes.FXED,
    serial_number="1M250305326",
)

# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.71.215.215", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")

_gnb_pdu = HBTE(addr="10.57.242.38", port_numbers=[4])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[4],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru_0, _ru_1, _ru_2, _ru_3, _ru_4, _ru_5, _ru_6, _ru_7, _ru_8, _ru_9], f1_m_ip_addr="10.71.215.215")

_cu = CU(
    backhaul_site_oam_ip="10.71.215.215",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.215.215", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.215.215", username="Nemuadmin", password="nemuuser"
    ),
)


# cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=20774, global_bts_id=20774)

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.195.25", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    connections=[_classical_bts],
)

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    ues=[_sigspark],
    tl_cloud_topology=_tl_cloud_topology,
    test_pcs=[_host],
)