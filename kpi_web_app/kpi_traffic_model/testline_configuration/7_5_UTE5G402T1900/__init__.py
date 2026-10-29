import re
import os
import yaml
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc, Connection
from taf.config.testline.core import RealCore
from taf.config.testline import RU, DU
from taf.config.testline.pdu import TopYoung
from taf.config.testline.testline import TestLine
from taf.config.testline.ue import Android, Qualcomm
from taf.config.testline.gnb import CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.gnb.du import Cablink, Endpoint
from taf.config.testline.ue import (
    AirphoneCloud,
    Airphone,
    Prisma,
    TM500,
    Qualcomm,
    QualcommUeType,
    Android,
)  # added in taf.meta.5.4
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)
from taf.config.testline import NetworkAddress, RoutingInformation
from taf.config.testline.appserver import AppServer
from taf.config.testline.taf_ue_data_transfer_protocol import TafUeDataTransferProtocol
from taf.config.testline.ue import TafUeFastmile
from taf.config.testline.appserver import TafUeAppServer

__maintainer__ = "Jianhua Li"  # TL owner name
__team__ = "I_NSB_MN_5GSC_5G_PZ_HZ_08_01_GMS <I_NSB_MN_5GSC_5G_PZ_HZ_08_01@internal.nsn.com>"  # TL owner's team
__email__ = "jianhua.h.li@nokia-sbell.com"  # TL owner's email

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

_appserver_ssh = SshServiceDetails(
    addr="10.57.162.11", username="cmw_sg8", password="Bestcm@8", port="58999"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.162.11",
    iperf_path="/system/bin",
    port="58082",
)

_appserver = AppServer(_iperf)

# CI_Detail_UE_Type='Qualcomm'
_ue1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.68.86.26", username="nokia5G", password="noki@123"
    ),
    serial_number="0123456789ABCDEF",
    server_dir="/cygdrive/c/pyro_server",
    python_path="/cygdrive/c/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["SG8_samsung", "cell_Mapping: [1]", "samsung"],
)

# 5GRU for classicalBTS RU PB
_ru_pdu = TopYoung(addr="10.71.195.211", port_numbers=[3])

_ru = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.73.128",
        username="root",
        password="a2%FgSz3$fHmdusap354xujw7a",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.3", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu.pdu_ports[3],
    radio_type=RadioTypes.AZQC,
)

# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(
    addr="192.168.253.20",
    hardware_type="ABIO",
)

_ru_cablinks = Cablink(
    source=Endpoint(unit=_capacity_unit, label="SFP", port_id=1),
    target=Endpoint(unit=_ru, label="SFP", port_id=1),
)

_gnb_pdu = TopYoung(addr="10.71.195.215", port_numbers=[2])
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[2],
    hardware_type="ASIL",
)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(
    airscale=_airscale, rus=[_ru], f1_m_ip_addr="10.71.210.195", cablinks=_ru_cablinks
)

# CU
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.71.210.195",
        routing=RoutingInformation(gateway="10.71.210.193", ip_prefix_length=27),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.210.195", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.210.195", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.71.210.195",
        routing=RoutingInformation(gateway="10.71.210.193", ip_prefix_length=27),
    ),
    x2u=NetworkAddress(
        v4="10.71.210.195",
        routing=RoutingInformation(gateway="10.71.210.193", ip_prefix_length=27),
    ),
    s1u=NetworkAddress(
        v4="10.71.210.195",
        routing=RoutingInformation(gateway="10.71.210.193", ip_prefix_length=27),
    ),
)

# cloud_topology
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_SA_ASILL_ABIOL_AZQC"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=1900, global_bts_id=10742)

# host
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.70.230.190", username="ute", password="ute"
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_classical_bts.dus[0].airscale.common_units[0],
            interface_type="lmp",
        )
    ],
)

tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_classical_bts],
    tl_cloud_topology=_tl_cloud_topology,
    ues=[_ue1],
    appserver=_appserver,
    core=RealCore(mcc=262, mnc=3),
)
