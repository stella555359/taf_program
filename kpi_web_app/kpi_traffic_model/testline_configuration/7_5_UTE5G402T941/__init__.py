import os
import yaml
import re
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.core import RealCore
from taf.config.testline import RU, DU
from taf.config.testline.pdu import HBTE, TopYoung
from taf.config.testline.testline import TestLine
from taf.config.testline.ue import Android
from taf.config.testline.gnb import CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import (
    AirphoneCloud,
    Airphone,
    Prisma,
    TM500,
    Qualcomm,
    QualcommUeType,
    Android,
)  # added in taf.meta.5.4
from taf.config.testline import RealEnb
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)
from taf.config.testline.attenuator import HBTE as AHBTE
from taf.config.testline import NetworkAddress, RoutingInformation
from taf.config.testline.appserver import AppServer
import yaml
import re

__maintainer__ = "melinda, Gao"
__team__ = "I_NSB_MN_5GSC_5G_PZ_HZ_08_GMS <I_NSB_MN_5GSC_5G_PZ_HZ_08@internal.nsn.com>"
__email__ = "melinda.gao@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# AZQF1 PA
_attenuator1 = AHBTE(
    ip_addr="10.71.210.137",
    port=5000,
    attenuation_port_numbers=[9, 10, 11, 12],
    model="PA-16-16-6-127-0.5-B-S",
)

# AZQF2 PA
_attenuator2 = AHBTE(
    ip_addr="10.71.210.137",
    port=5000,
    attenuation_port_numbers=[13, 14, 15, 16],
    model="PA-16-16-6-127-0.5-B-S",
)

# host
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.166", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_appserver_ssh = SshServiceDetails(
    addr="10.70.222.52", username="cmw_sg8", password="Bestcm@8", port="58999"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.70.222.52",
    iperf_path="/usr/bin/iperf",
    port="58155",
)
_appserver = AppServer(_iperf)
_appserver.iperf_details.port = 58155

# # CI_Detail_UE_Type='inseego'
# inseego
_ue_config_path = os.path.join(_cfg_dir, "TestData/inseego.yml")
if os.path.isfile(_ue_config_path):
    with open(_ue_config_path) as f:
        _ue_inseego = f.read()
        # qci_port = re.findall("(_iperf.*?port)", _ue_inseego)
        # for item in qci_port:
        #     _ue_inseego = _ue_inseego.replace(item, str(eval(item)))
        _ue_config = yaml.safe_load(_ue_inseego)
else:
    _ue_config = ""
# inseego

# RU PB
# RU1: AZQF1
_ru1_pdu = TopYoung(addr="10.71.195.196", port_numbers=[2])

_ru1 = RU(
    ru_hw_group="hw_group",
    # RU username/password need modify
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.33.129", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.3", username="root", password="umniedziala"
    ),
    pdu_port=_ru1_pdu.pdu_ports[2],
    radio_type=RadioTypes.AZQF,
    attenuation_ports=[
        _attenuator1.attenuator_ports[9],
        _attenuator1.attenuator_ports[10],
        _attenuator1.attenuator_ports[11],
        _attenuator1.attenuator_ports[12],
    ],
)

# RU2: AZQF
_ru2_pdu = TopYoung(addr="10.71.195.196", port_numbers=[3])

_ru2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.33.128", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.3", username="root", password="umniedziala"
    ),
    pdu_port=_ru2_pdu.pdu_ports[3],
    radio_type=RadioTypes.AZQF,
    attenuation_ports=[
        _attenuator2.attenuator_ports[13],
        _attenuator2.attenuator_ports[14],
        _attenuator2.attenuator_ports[15],
        _attenuator2.attenuator_ports[16],
    ],
)


# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.71.210.142", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(addr="192.168.253.20")
_gnb_pdu = HBTE(addr="10.71.195.209", port_numbers=[5])
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[5],
)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(airscale=_airscale, rus=[_ru1, _ru2], f1_m_ip_addr="10.71.210.142")

# CU
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.71.210.142",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.210.129", ip_prefix_length=27),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.210.142", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.210.142", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.71.210.142",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.210.129", ip_prefix_length=27),
    ),
    x2u=NetworkAddress(
        v4="10.71.210.142",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.210.129", ip_prefix_length=27),
    ),
    s1u=NetworkAddress(
        v4="10.71.210.142",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.71.210.129", ip_prefix_length=27),
    ),
)

# RealEnb  enb&enb_HBTE ip_addr
# _lmp_connection_enb = SshServiceDetails(
#     addr="10.101.48.99", username="toor4nsn", password="oZPS0POrRieRtu"
# )
# _enb_pdu = TopYoung(addr="10.68.87.229", port_numbers=[6])
# _common_unit_1 = CommonUnit(
#     lmp_connection=_lmp_connection_enb,
#     capacity_units=[],
#     # pdu_port=_enb_pdu.pdu_ports[6],
# )
# _real_enb = Airscale(common_units=[_common_unit_1])
# _lte_real_enb = RealEnb(airscale=_real_enb)

# cloud_topology
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ASKEY_SA_ASIBL_ABIOB1_AZQFX2"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=941, global_bts_id=1110)


tl = TestLine(
    test_pc=_test_pc,
    test_pcs=[_test_pc],
    gnbs=[_classical_bts],
    # enbs=[_lte_real_enb],
    appserver=_appserver,
    # ues=[_ue1],
    ues=[_ue_config],
    core=RealCore(mcc=262, mnc=3),
    attenuator=[_attenuator1, _attenuator2],
    tl_cloud_topology=_tl_cloud_topology,
)
