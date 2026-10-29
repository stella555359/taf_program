__maintainer__ = "Chen Jian"
__team__ = (
    "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_05_GMS <I_NSB_MN_5GSC_MMW_SC_PZ_HZ_05@internal.nsn.com>"
)
__email__ = "jian.1.chen@nokia.com"

import os
import shutil

from taf.config.testline.appserver import AppServer
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc, Connection
from taf.config.testline import DU, RU, RealEnb
from taf.config.testline.pdu import ATEN, HBTE, TopYoung, PduPort
from taf.config.testline.gnb import ClassicalBts, CU
from taf.config.testline.gnb.du import Cablink, Endpoint
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.core import RealCore, PCF
from taf.config.testline.testline import TestLine
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)
from taf.config.testline.ue import Android, Qualcomm
from taf.config.testline import NetworkAddress, RoutingInformation
from taf.config.testline.attenuator import HBTE as AHBTE
from collections import OrderedDict

os.environ["INIT_CONFIG_FILE_PATH"] = os.path.dirname(os.path.abspath(__file__))

__all__ = ["tl"]

os.environ["ABSTRACT_LIB_CONFIG"] = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "ue_config.yaml"
)

# Enb
_common_unit_1 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
)

_real_enb = Airscale(common_units=[_common_unit_1])

_lte_real_enb = RealEnb(
    airscale=_real_enb, rms=None, instance_id=2032, global_bts_id=10444
)


_ru0_pdu = HBTE(addr="10.71.195.36", port_numbers=[1])
_ru1_pdu = HBTE(addr="10.71.195.36", port_numbers=[2])

_ru0 = RU(
    ru_hw_group="cMAArChile_64T64",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.8.2", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru0_pdu.pdu_ports[1],
    radio_type=RadioTypes.AEHC.value,
)

_ru1 = RU(
    ru_hw_group="cMAArChile_64T64",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.8.2", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru1_pdu.pdu_ports[2],
    radio_type=RadioTypes.AEHC.value,
)

_du0_pdu = HBTE(addr="10.71.195.37", port_numbers=[6])

_common_unit_0_pdu_port = PduPort(pdu=_du0_pdu, port_no="6")

_appserver_ssh = SshServiceDetails(
    addr="10.71.207.149", username="vrf3_sg5", password="vrf3@sg5"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.207.149",
    iperf_path="/data/data/com.nokia.syve.uemanager.mobile/iperf",
    port="45006",
)

_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.218.58", username="mn5gran", password="nokia123@"
    ),
    serial_number="R3CNC0DGPBE",  #R5CN20LYP5R R5CN20HRWLM R5CN212N3RX R3CN600Q08B RFCR11BREQR R3CR50B3Q3B RFCT31XBW5M
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "samsung"],
)

_capacity_unit0 = CapacityUnit(
    addr="192.168.253.20",
    hardware_type="ABIO",
    rus=[_ru0]
    )
_capacity_unit1 = CapacityUnit(
    addr="192.168.253.21",
    hardware_type="ABIN",
    rus=[_ru1]
    )

_common_unit_0_L = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_capacity_unit0,_capacity_unit1],
    pdu_port=_common_unit_0_pdu_port,
    hardware_type="ASIL",
)

_airscale = Airscale(common_units=[_common_unit_0_L])

# Cablinks should be defined in the bottom of DU section
_ru_cablinks = [
    Cablink(
        source=Endpoint(unit=_capacity_unit0, label="SFP", port_id=1),
        target=Endpoint(unit=_ru0, label="SFP", port_id=3),
    ),
    Cablink(
        source=Endpoint(unit=_capacity_unit0, label="SFP", port_id=7),
        target=Endpoint(unit=_ru0, label="SFP",port_id=4),
    ),
]

_du = DU(
    airscale=_airscale, rus=[_ru0, _ru1], f1_m_ip_addr="10.71.208.102", cablinks=_ru_cablinks
)

_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.71.208.102",
        vlan_id=None,
        routing_v4=RoutingInformation(gateway="10.71.208.1", ip_prefix_length=24),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.208.102", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.208.102", username="Nemuadmin", password="nemuuser", port=443
    ),
    x2c=NetworkAddress(
        v4="10.71.208.102",
        vlan_id=None,
        routing_v4=RoutingInformation(gateway="10.71.208.1", ip_prefix_length=24),
    ),
    x2u=NetworkAddress(
        v4="10.71.208.102",
        vlan_id=None,
        routing_v4=RoutingInformation(gateway="10.71.208.1", ip_prefix_length=24),
    ),
    s1u=NetworkAddress(
        v4="10.71.208.102",
        vlan_id=None,
        routing_v4=RoutingInformation(gateway="10.71.208.1", ip_prefix_length=24),
    ),
)


_cbts = ClassicalBts(cu=_cu, dus=[_du], instance_id=2006, global_bts_id=11010)

# RealCore
_pcf = PCF(
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.217.23", username="feat1", password="Nokia@123"
    )
)
_realcore = RealCore(mcc=262, mnc=3)

# cloud_topology
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ASILR_ABIOB4_2xAEHC_ENB"

_gnb_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.251.40", username="ute", password="ute"
    ),
    connections=[],
)

# Test VM
_test_vm = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.251.40", username="ute", password="ute"
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_cbts.dus[0].airscale.common_units[0],
            interface_type="lmp",
        )
    ],
)

_appserver = AppServer(iperf_details=_iperf)

_attenuator = AHBTE(ip_addr="x.x.x.x", port=23, attenuation_port_numbers=[7, 8])


tl = TestLine(
    test_pc=_test_vm,
    gnbs=[_cbts],
    tl_cloud_topology=_tl_cloud_topology,
    core=_realcore,
    enbs=[_lte_real_enb],
    ues=[_android],
    test_pcs=[_test_vm],
    appserver=_appserver,
    attenuator=_attenuator,
)
