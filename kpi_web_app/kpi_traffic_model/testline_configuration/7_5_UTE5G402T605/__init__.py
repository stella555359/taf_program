import os
import re
import yaml
from taf.config.testline.connection_details import (
    SshServiceDetails,
    TelnetConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.airscale import Airscale, CapacityUnit, CommonUnit
from taf.config.testline.enb import RealEnb
from taf.config.testline.flexi import Flexi
from taf.config.testline.pdu import HBTE, TopYoung
from taf.config.testline.radio import RU, RadioTypes
from taf.config.testline.ran import BSC, RNC
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.config.testline.testpc import TestPc
from taf.config.testline.appserver import AppServer
from taf.config.testline.ue import Android

__maintainer__ = "Zhihao Shi"  # TL owner name
__team__ = "I_NSB_MN_5GSC_5G_PZ_HZ_04_GMS <I_NSB_MN_5GSC_5G_PZ_HZ_04@internal.nsn.com>"  # TL owner's team
__email__ = "zhihao.shi@nokia-sbell.com"  # TL owner's email

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.198", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_pdu_1 = HBTE(addr="10.71.196.163", port_numbers=[1])

_fct_1 = CommonUnit(
    SshServiceDetails(
        addr="192.168.255.1", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=None,
    pdu_port=_pdu_1.pdu_ports[1],
    hardware_type="ASOE",
    hardware_version="A.101",
    serial_number="EA211854173",
)

_ru_pdu = TopYoung(addr="10.71.196.168", port_numbers=[6])

_rmod_1 = RU(
    ru_hw_group="hw_group",
    radio_type=RadioTypes.AZNA,
    serial_number="RW201001196",
    default_telnet_connection_details=TelnetConnectionDetails(
        addr="192.168.253.", port=2323
    ),
    pdu_port=_ru_pdu.pdu_ports[6],
)

_ru_pdu2 = TopYoung(addr="10.71.196.171", port_numbers=[2])

_rmod_2 = RU(
    ru_hw_group="hw_group",
    radio_type=RadioTypes.AZNA,
    serial_number="EA204859669",
    default_telnet_connection_details=TelnetConnectionDetails(
        addr="192.168.253.", port=2323
    ),
    pdu_port=_ru_pdu2.pdu_ports[2],
)

_enb_sbts_1 = RealEnb(
    system_module=[_fct_1],
    rms=[_rmod_1, _rmod_2],
    oam_ip=NetworkAddress("10.71.213.107"),
    instance_id=605,
    global_bts_id=605,
)


_appserver_ssh_1 = SshServiceDetails(
    addr="10.57.191.246", username="vrf4_sg4", password="vrf4@sg4", port=54605
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh_1,
    network_interface_address="10.57.191.246",
    iperf_path=None,
    port=54605,
)

_appserver = AppServer(_iperf)

_android0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.217.34", username="nokia5G", password="noki@123"
    ),
    serial_number="RFCNC0LD9JB",
    server_dir="/cygdrive/c/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["samsung", "samsung_lte"],
    imsi="505023100008503",
    service_call_attach=17,
    service_call_detach=17,
)

tl = TestLine(
    test_pc=_host,
    enbs=[_enb_sbts_1],
    appserver=_appserver,
    ues=[
        _android0,
    ],
    tl_cloud_topology="CLOUD_SRAN_L_1ASOE_1AZNA_2AZNA",
)
