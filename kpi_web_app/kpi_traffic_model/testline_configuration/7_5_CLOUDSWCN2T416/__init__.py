######################################
#  TestLine Cloud TL416 HZ           #
######################################
__maintainer__ = "Carol An"
__team__ = "NSB MN 5G&SC SW Eng 2 CN T&A SG"
__email__ = "carol.an@nokia-sbell.com"

import os
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    SCRadioConnectionDetails,
    TelnetConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline.enb import RealEnb
from taf.config.testline import NetworkAddress, RoutingInformation
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.pdu import ATEN, PduPort
from taf.config.testline.radio import RU
from taf.config.testline.core import LTEEmuCore
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.ue import Android
from taf.config.testline.core import EPCSim
from taf.config.testline.gnb.networkaddress import NetworkAddress

__all__ = ["tl"]

_lmp_vm_gnb_1 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.213.248", username="ute", password="ute"
    )
)

cfg_dir = os.path.dirname(os.path.abspath(__file__))

_cu_gnb_1 = CU(
    backhaul_site_oam_ip=NetworkAddress(v4="192.168.255.1", vlan_id=1098),
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.1", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.255.1", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="172.18.10.10",
        vlan_id=2011,
        routing=RoutingInformation(gateway="172.18.10.0", ip_prefix_length=27),
    ),
    x2u=NetworkAddress(v4="172.18.10.10", vlan_id=2011),
    s1c=NetworkAddress(v4="172.18.10.10", vlan_id=2011),
    s1u=NetworkAddress(v4="172.18.10.10", vlan_id=2011),
)

_pdu_gnb = ATEN(addr="0.0.0.0", port_numbers=[0])
_pdu_gnb_ru = ATEN(addr="0.0.0.0", port_numbers=[0])
_pdu_gnb_ru2 = ATEN(addr="0.0.0.0", port_numbers=[0])
_pdu_fanbreaker = ATEN(addr="0.0.0.0", port_numbers=[0])
_pdu_gpsbreaker = ATEN(addr="0.0.0.0", port_numbers=[0])

_fanbreaker_du1 = PduPort(pdu=_pdu_fanbreaker, port_no=0)
_gpsbreaker_du1 = PduPort(pdu=_pdu_gpsbreaker, port_no=0)

_gnb_ru = RU(
    ru_hw_group="Unknown",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="root", password="umniedziala"
    ),
    # 			 lmp_connection=SshServiceDetails(addr='TO_UPDATE',
    # 											  username='toor4nsn',
    # 											  password='oZPS0POrRieRtu'),
    pdu_port=_pdu_gnb_ru.pdu_ports[0],
)

_abil1_gnb_1_master = CapacityUnit(addr="192.168.253.20")

_abil1_gnb_1_slave = CapacityUnit(addr="192.168.253.21")

_abil1_gnb_1_loner = CapacityUnit(addr="192.168.253.22")

_asik_gnb_1 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_abil1_gnb_1_master, _abil1_gnb_1_loner, _abil1_gnb_1_slave],
    pdu_port=_pdu_gnb.pdu_ports[0],
)

_airscale_gnb_1 = Airscale(common_units=[_asik_gnb_1])

_du_1_gnb_1 = DU(airscale=_airscale_gnb_1, rus=[_gnb_ru])

_lmp_vm_enb_1 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.213.249", username="ute", password="ute"
    )
)

_pdu_enb = ATEN(addr="0.0.0.0", port_numbers=[0])

_asik_enb_1 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_pdu_enb.pdu_ports[0],
)

_airscale_enb_1 = Airscale(common_units=[_asik_enb_1])

# _enb_1 = RealEnb(airscale=_airscale_enb_1,
#                 global_bts_id=416,
#                 instance_id=1900,
#                 x2_link_addr=NetworkAddress(v4='172.18.10.30',
#                                             vlan_id=2011))
#                                             routing=RoutingInformation(gateway='172.18.10.0',
#                                                                       ip_prefix_length=27)))

_enb_1 = RealEnb(
    airscale=_airscale_enb_1,
    global_bts_id=416,
    instance_id=1900,
    x2_link_addr=NetworkAddress(v4="172.18.10.20", vlan_id=2011),
)

_enb_1.m_plane = NetworkAddress(v4="172.18.10.30", vlan_id=2011)

_cbts = ClassicalBts(
    cu=_cu_gnb_1, dus=[_du_1_gnb_1], global_bts_id=416, instance_id=416
)

_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ASIKL_ABILB1_AAHF_ENB"

# _core = RealCore4G()
#########LTEemuSim##########
_core = LTEEmuCore(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.209.204", username="ute", password="ute"
    ),
    dir_path="/home/ute/LTEemu_core2_64_3252",
    cfg_filename="basic_wts_step1.cfg",
    mme_ip="",
    edaemon_port="22222",
    egate_port="20000",
)
# _core = EPCSim(default_ssh_connection_details=SshServiceDetails(
#                                                    addr='7_7_cloudt283.sc5g.krk-lab.nsn-rdnet.net',
#                                                    username='ute',
#                                                    password='ute'),
#               dir_path='/epcsim',  # /opt/core
#               cfg_filename='sim2.cfg',  # epcsim.cfg
#               mme_ip='10.253.165.33',
#               mcc=244,
#              mnc=8,
#              tac=1024,
#               edaemon_port=12345,
#               egate_port=60001)

tl = TestLine(
    test_pc=_lmp_vm_gnb_1,
    gnbs=[_cbts],
    core=_core,
    tl_cloud_topology=_tl_cloud_topology,
    enbs=[_enb_1],
    test_pcs=[_lmp_vm_enb_1],
)

tl = TestlineWrapper(tl)
