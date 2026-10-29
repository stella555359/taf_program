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
    SCRadioConnectionDetails,
    TelnetConnectionDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.core import EPCSim, LTEEmuCore, PrismaCore
from taf.config.testline import RU, DU
from taf.config.testline.pdu import HBTE
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU, DU, ClassicalBts
from taf.config.testline import SC5GRadio, SC4GRadio
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import AirphoneCloud, Airphone, Prisma, TM500
from taf.config.testline import Enb, SimEnb, RealEnb, LTEEmuEnb, PrismaEnb, DocomoEnb
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.nms import Netact
from taf.config.testline import NetworkAddress, RoutingInformation
from taf.config.testline.gnb.du import Cablink, Endpoint
from taf.config.testline.gnb.networkaddress import NetworkAddress, RoutingInformation

__maintainer__ = "5G SC CRT"
__team__ = "5G SC CRT"
__email__ = "nj-fz-crt@list.nokia.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

##host
_test_pc_gnb = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.66.12.239", username="ute", password="ute"
    )
)

# 5GRU for classicalBTS
# _ru_pdu = HBTE(addr="10.57.243.8", port_numbers=[1])
# _ru = RU(
#     ru_hw_group="ASIR-HUB",
#     default_ssh_connection_details=SshServiceDetails(
#         addr="172.16.1.74", username="root", password="umniedziala"
#     ),
#     lmp_connection=SshServiceDetails(
#         addr="172.16.1.74", username="root", password="umniedziala"
#     ),
#     pdu_port=_ru_pdu.pdu_ports[1],
# )

_ru = SC5GRadio(
    ru_hw_group="ASIR-HUB",
    sc_radio_connection_details=SCRadioConnectionDetails(
        ssh_connection_details=SshServiceDetails(
            addr="192.168.255.129",
            username="toor4nsn",
            password="oZPS0POrRieRtu",
            proxy=SshServiceDetails(
                addr="10.66.27.166", username="ute", password="ute"
            ),
        ),
        telnet_connection_details=TelnetConnectionDetails(
            addr="tty-server", username="toor4nsn", password="oZPS0POrRieRtu"
        ),
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=None,
)

##DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")
_gnb_pdu = HBTE(addr="10.57.242.9", port_numbers=[7])

_ru_cablinks = [
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=1),
        target=Endpoint(unit=_ru, label="SFP", port_id=2),
    )
]

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[7],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(
    airscale=_airscale, rus=[_ru], f1_m_ip_addr="10.57.242.220", cablinks=_ru_cablinks
)


_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="192.168.255.129",
        vlan_id=None,
        routing=RoutingInformation(gateway="192.168.255.1", ip_prefix_length=29),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.66.29.244", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.255.129",
        username="Nemuadmin",
        password="Nokia123!",
    ),
    x2c=NetworkAddress(
        v4="10.66.29.244",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.66.29.1", ip_prefix_length=29),
    ),
    x2u=NetworkAddress(
        v4="10.66.29.244",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.66.29.1", ip_prefix_length=29),
    ),
    s1u=NetworkAddress(
        v4="10.66.29.244",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.66.29.1", ip_prefix_length=29),
    ),
)


##cloud_topology
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_SA_ASIKL_ABILB1_AEQN_NETACT"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=42, global_bts_id=42)
_netact = Netact("10.41.146.72")  # srnclab1013 netact

tl = TestLine(
    test_pc=_test_pc_gnb,
    test_pcs=[_test_pc_gnb],
    gnbs=[_classical_bts],
    tl_cloud_topology=_tl_cloud_topology,
    nms=_netact,
)


# # common
# __all__ = ["tl"]
#
# _cfg_dir = os.path.dirname(os.path.abspath(__file__))
# ###########################################
# # Test PC - server running the Robot tests
# ###########################################
# _test_pc = TestPc(
#     default_ssh_connection_details=SshServiceDetails(
#         addr="10.66.12.239", username="ute", password="ute"
#         # Login information for the VM where the test cases will be run
#     )
# )
#
# ###################
# # gNB definition
# ###################
#
# _cu = CU(
#     backhaul_site_oam_ip=NetworkAddress(
#         v4="192.168.255.129",
#         vlan_id=None,
#         routing=RoutingInformation(gateway="10.66.29.0", ip_prefix_length=24),
#     ),
#     oam_ssh_connection_details=SshServiceDetails(
#         addr="10.66.29.244", username="toor4nsn", password="oZPS0POrRieRtu"
#     ),
#     oam_http_connection_details=HttpConnectionDetails(
#         addr="10.66.29.244", username="Nemuadmin", password="nemuuser"
#     ),
#     x2c=NetworkAddress(v4="10.66.29.244", vlan_id=23),
#     x2u=NetworkAddress(v4="172.30.1.11", vlan_id=230),
#     s1c=NetworkAddress(v4="10.66.29.244", vlan_id=23),
#     s1u=NetworkAddress(v4="172.30.1.11", vlan_id=230),
# )
#
# _capacity_unit = CapacityUnit(
#     addr="fsp1_c", hardware_type="ASIK", hardware_version="101"
# )
#
# _common_unit = CommonUnit(
#     lmp_connection=SshServiceDetails(
#         addr="192.168.255.129",
#         username="toor4nsn",
#         password="oZPS0POrRieRtu",
#         proxy=SshServiceDetails(
#             addr="10.66.12.239", username="ute", password="ute"  # Login information for the VM connected to gNB
#         ),
#     ),
#     capacity_units=[_capacity_unit],
#     hardware_type="ASIL",
#     hardware_version="102",
# )
#
# _ru = SC5GRadio(
#     ru_hw_group="ASIR-HUB",
#     sc_radio_connection_details=SCRadioConnectionDetails(
#         ssh_connection_details=SshServiceDetails(
#             addr="192.168.255.129",
#             username="toor4nsn",
#             password="oZPS0POrRieRtu",
#             proxy=SshServiceDetails(
#                 addr="10.66.31.30", username="ute", password="ute"  # Login information for the VM connected to 5G sHUB
#             ),
#         ),
#         telnet_connection_details=TelnetConnectionDetails(
#             addr="tty-server", username="toor4nsn", password="oZPS0POrRieRtu"
#         ),
#     ),
#     lmp_connection=SshServiceDetails(
#         addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
#     ),
#     pdu_port=None,
# )
#
# _airscale = Airscale(common_units=[_common_unit])
# _du = DU(airscale=_airscale, rus=[_ru])
# _cbts = ClassicalBts(
#     cu=_cu,
#     instance_id=42,  # ID of MRBTS object
#     global_bts_id=42,  # ID of NRBTS object
# )
#
#
# #_netact = Netact("10.32.215.128")  # clab397 netact
# _netact = Netact("10.41.146.72")  # srnclab1013 netact
# ####################################################################################################
# # Example of testline definition consists of both 5G and 4G.
# # Add other definitions, such as "ues", "core", etc. according to actual test line configurations.
# ####################################################################################################
# tl = TestLine(
#     test_pc=_test_pc,
#     gnbs=[_cbts],
#     # enbs=[_lteenb],
# )
