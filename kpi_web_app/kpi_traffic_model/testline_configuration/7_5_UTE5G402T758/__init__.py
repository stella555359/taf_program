import os
import re
import yaml
from taf.config.testline.connection_details import (
    SshServiceDetails,
    TelnetConnectionDetails,
    HttpConnectionDetails,
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
from taf.config.testline.appserver import TafUeAppServer
from taf.config.testline.taf_ue_data_transfer_protocol import TafUeDataTransferProtocol
from taf.config.testline.ue import TafUeFastmile
from taf.config.testline.ue import Android
from taf.config.testline.gnb.du import DU
from taf.config.testline.gnb import CU, ClassicalBts
from taf.config.testline import RoutingInformation

__maintainer__ = "Xuewen Zhang"  # TL owner name
__team__ = "I_NSB_MN_5GSC_5G_PZ_HZ_05_GMS <I_NSB_MN_5GSC_5G_PZ_HZ_05@internal.nsn.com>"  # TL owner's team
__email__ = "xuewen.zhang@nokia-sbell.com"  # TL owner's email

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.104", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_pdu_1 = TopYoung(addr="10.71.196.211", port_numbers=[3])


_ru_pdu_1 = TopYoung(addr="10.71.196.206", port_numbers=[6])
_ru_pdu_2 = TopYoung(addr="10.71.197.14", port_numbers=[8])
_ru_pdu_3 = TopYoung(addr="10.71.197.20", port_numbers=[5])
# _ru_pdu_3 = TopYoung(addr="10.71.196.198", port_numbers=[4])
# _ru_pdu_4 = TopYoung(addr="10.71.196.206", port_numbers=[6])
# _ru_pdu_5 = TopYoung(addr="10.71.197.18", port_numbers=[4])


_rmod_1 = RU(
    ru_hw_group="hw_group",
    radio_type=RadioTypes.AQQJ,
    serial_number="1M232102632",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.3", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu_1.pdu_ports[6],
)
_rmod_2 = RU(
    ru_hw_group="hw_group",
    radio_type=RadioTypes.AEQY,
    serial_number="1M222643817",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52",
        username="serviceuser",
        password="bobuWrUHk7Xq7WPpY9ZcjEi8zNdX3plZ+/y420RZ7W4=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.3", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu_2.pdu_ports[8],
)
_rmod_3 = RU(
    ru_hw_group="hw_group",
    radio_type=RadioTypes.AEQE,
    serial_number="1M212137412",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52",
        username="serviceuser",
        password="bobuWrUHk7Xq7WPpY9ZcjEi8zNdX3plZ+/y420RZ7W4=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.3", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu_3.pdu_ports[5],
)


# _appserver_ssh_1 = SshServiceDetails(
#    addr="10.57.191.247", username="vrf4_sg5", password="vrf4@sg5", port=55310
# )
#
# _iperf = IperfDataTransferDetails(
#    ssh_connection_details=_appserver_ssh_1,
#    network_interface_address="10.57.191.247",
#    iperf_path="iperf",
#    port=55585,
# )
#
#
# _appserver = AppServer(_iperf)

## CI_Detail_UE_Type='Nokia FastMile 5G Gateway 3.1'
# ue_config_path = os.path.join(_cfg_dir, "TestData/ue.yml")
# if os.path.isfile(ue_config_path):
#    with open(ue_config_path) as f:
#        _ue_read = f.read()
#        qci_port = re.findall("(_iperf.*?port)", _ue_read)
#        for item in qci_port:
#            _ue_read = _ue_read.replace(item, str(eval(item)))
#        _ue_config = yaml.load(_ue_read, Loader=yaml.FullLoader)
# else:
#    _ue_config = ""

# for FastMile CPE 3.2
_fastmile_appserver_1 = TafUeAppServer(
    app_server_name="APP_SERVER_1",
    address="10.57.191.247",
    user="vrf4_sg5",
    password="vrf4@sg5",
    bind_interface_ip="10.57.191.247",
    expected_prompt="[vrf4_sg5@appserver ~]$ ",
    binary_path="/home/vrf4_sg5/taf_debug/iperf",
    ports=[55310, 55758],
)

_fastmile_data_transfer_1 = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_fastmile_appserver_1,
    interval=1,
    binary_path="iperf",
    version=2,
)


_fastmile_1 = TafUeFastmile(
    com_port="4",
    ue_pc_address="10.57.157.104",
    root_password="5d5a496254b6",
    ue_manage_ip="10.71.206.9",
    serial_number="0123456789ABCDEF",
    data_transfer=[_fastmile_data_transfer_1],
    version="3.2",
    ue_pc_port=5555,
    capabilities=["REAL_FASTMILE_UE2", "nokia_fastmile"],
)

# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.71.214.4", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(addr="192.168.253.22")

_gnb_pdu = _pdu_1

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[3],
)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(
    airscale=_airscale,
    rus=[_rmod_1, _rmod_2, _rmod_3],
    f1_m_ip_addr="10.71.214.4",
)

# CU
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.71.214.4",
        vlan_id=None,
        routing_v4=RoutingInformation(gateway="10.71.214.1", ip_prefix_length=27),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.214.4", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.214.4", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.71.214.4",
        vlan_id=None,
        routing_v4=RoutingInformation(gateway="10.71.214.1", ip_prefix_length=27),
    ),
    x2u=NetworkAddress(
        v4="10.71.214.4",
        vlan_id=None,
        routing_v4=RoutingInformation(gateway="10.71.214.1", ip_prefix_length=27),
    ),
    s1u=NetworkAddress(
        v4="10.71.214.4",
        vlan_id=None,
        routing_v4=RoutingInformation(gateway="10.71.214.1", ip_prefix_length=27),
    ),
)

# cloud_topology
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ASIBL_ABIOB1_AEQE"

# classicalbts
_classical_bts = ClassicalBts(
    dus=[_du], cu=_cu, instance_id="2658", global_bts_id="2658"
)


tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    enbs=[],
    ues=[_fastmile_1],
    tl_cloud_topology="CLOUD_SRAN_L_1ASIB_1ABIC_1AEQP",
)
