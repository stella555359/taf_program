import os
import re
import yaml
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.core import RealCore
from taf.config.testline import RU, DU
from taf.config.testline.pdu import (
    PduPort,
    Pdu,
    EPC,
    ATEN,
    RRB,
    APC,
    Gude,
    HBTE,
    TopYoung,
)
from taf.config.testline.testline import TestLine
from taf.config.testline.ue import Android
from taf.config.testline.gnb import CU, ClassicalBts
from taf.config.testline.gnb.du import Cablink, Endpoint
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
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
from taf.config.testline.attenuator import AttenuationPort
from taf.config.testline import NetworkAddress, RoutingInformation
from taf.config.testline.appserver import AppServer

__maintainer__ = "Shasha Liu"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_5_GMS <I_MN_5G_RAN_IV4_LINE_HZG_5@internal.nsn.com>"
)
__email__ = "shasha.liu@nokia-sbell.com"
# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# 5GRU for classicalBTS
_ru_pdu = HBTE(addr="10.71.196.197", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2",
        username="serviceuser",
        password="oBrd1RgbOasUtYAeVfxrW9yGHb6ONl0w+MJUoKrBMGE=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="user", password="pass"
    ),
    pdu_port=_ru_pdu.pdu_ports[8],
    radio_type=RadioTypes.AWHQX,
)

_ru2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.6",
        username="serviceuser",
        password="oBrd1RgbOasUtYAeVfxrW9yGHb6ONl0w+MJUoKrBMGE=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="user", password="pass"
    ),
    pdu_port=_ru_pdu.pdu_ports[6],
    radio_type=RadioTypes.AWHQX,
)


# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.71.214.5", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(addr="192.168.253.20")
_gnb_pdu = HBTE(addr="10.71.196.211", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru_cablinks = [
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=1),
        target=Endpoint(unit=_ru, label="SFP", port_id=1),
    ),
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=2),
        target=Endpoint(unit=_ru2, label="SFP", port_id=1),
    ),
]

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[8],
)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(
    airscale=_airscale,
    rus=[_ru, _ru2],
    f1_m_ip_addr="10.71.214.5",
    cablinks=_ru_cablinks,
)

# CU
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.71.214.5",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.101.50.129", ip_prefix_length=27),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.214.5", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.214.5", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.71.214.5",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.101.50.129", ip_prefix_length=27),
    ),
    x2u=NetworkAddress(
        v4="10.71.214.5",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.101.50.129", ip_prefix_length=27),
    ),
    s1u=NetworkAddress(
        v4="10.71.214.5",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.101.50.129", ip_prefix_length=27),
    ),
)

# RealEnb
# _lmp_connection_enb = SshServiceDetails(
#     addr="10.101.40.37", username="toor4nsn", password="oZPS0POrRieRtu"
# )
# _enb_pdu = HBTE(addr="10.101.45.132", port_numbers=[8])
# _common_unit_1 = CommonUnit(
#     lmp_connection=_lmp_connection_enb,
#     capacity_units=[],
#     pdu_port=_enb_pdu.pdu_ports[8],
# )
# _real_enb = Airscale(common_units=[_common_unit_1])
# _lte_real_enb = RealEnb(airscale=_real_enb, rms=None)

# cloud_topology
_tl_cloud_topology = "CLOUD_5G_ASIBA102R_ABIOA103B4_AQQL"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=2462, global_bts_id=2462)

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.128", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    connections=[_classical_bts],
)

_appserver_ssh = SshServiceDetails(
    addr="10.57.191.247", username="vrf4_sg5", password="vrf4@sg5", port=55910
)

_appserver_ssh_2 = SshServiceDetails(
    addr="10.57.191.247", username="vrf4_sg5", password="vrf4@sg5", port=55911
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.247",
    iperf_path="/data/data/com.nokia.syve.uemanager.mobile/",
    port=55912,
)

_iperf_2 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh_2,
    network_interface_address="10.57.191.247",
    iperf_path="/data/data/com.nokia.syve.uemanager.mobile/",
    port=55913,
)

_appserver = AppServer(_iperf)

# CI_Detail_UE_Type='Nokia FastMile 5G Gateway 3.1'
ue_config_path = os.path.join(_cfg_dir, "TestData/ue.yml")
if os.path.isfile(ue_config_path):
    with open(ue_config_path) as f:
        _ue_read = f.read()
        qci_port = re.findall("(_iperf.*?port)", _ue_read)
        for item in qci_port:
            _ue_read = _ue_read.replace(item, str(eval(item)))
        _ue_config = yaml.load(_ue_read, Loader=yaml.FullLoader)
else:
    _ue_config = ""

# switch Dtor
_dell_s4048on_ssh = SshServiceDetails(
    addr="0.0.0.0", port="1", username="5gran", password="nokia123"
)
_dell_s4048on_switch = DellS4048ONSwitch(_dell_s4048on_ssh)

# switch Mtor
_dell_s4048ton_ssh = SshServiceDetails(
    addr="0.0.0.0", port="1", username="5gran", password="nokia123"
)
_dell_s4048ton_switch = DellS4048TONSwitch(_dell_s4048ton_ssh)


tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    # enbs=[_lte_real_enb],
    core=RealCore(mcc=460, mnc=2),
    tl_cloud_topology=_tl_cloud_topology,
    ues=[_ue_config],
    switches=[_dell_s4048on_switch, _dell_s4048ton_switch],
    appserver=_appserver,
)
