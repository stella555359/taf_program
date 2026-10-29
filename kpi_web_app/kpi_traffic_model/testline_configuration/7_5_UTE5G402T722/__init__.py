__maintainer__ = "Wang Zhouqun"
__team__ = (
    "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_04_GMS <I_NSB_MN_5GSC_MMW_SC_PZ_HZ_04@internal.nsn.com>"
)
__email__ = "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_04@internal.nsn.com"
__owner_email__ = "zhouqun.wang@nokia-sbell.com"

# import os
#
# from taf.config.testline.cloud_hosting import (
#     ControlNode,
#     NCIR,
#     CloudDeployment,
#     DeploymentFlavorStack,
#     DeploymentNetworkStack,
#     DeploymentVnfStack,
# )
# from taf.config.testline.connection_details import (
#     OpenStackConnectionDetails,
#     SshServiceDetails,
#     BmcConnectionDetails,
#     HttpConnectionDetails,
# )
# from taf.config.testline.testpc import TestPc
# from taf.config.testline.core import EPCSim
# from taf.config.testline.testline import TestLine
# from taf.config.testline.gnb import ClassicalBts, CU
# from taf.config.testline.enb import RealEnb
# from taf.config.testline.ue import TM500, Android
# from taf.config.testline import DU, RU
# from taf.config.testline.attenuator import (
#     AttenuationPort,
#     HBTE,
# )  # added in taf.meta 5.4
# from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
# from taf.config.testline.pdu import HBTE
# # taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC
# from taf.config.testline.radio import RadioModule
# from taf.config.testline import IperfDataTransferDetails
# from taf.config.testline.appserver import AppServer

import os
import yaml
from taf.config.testline.testline import TestLine
from taf.config.testline.ue import Android
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.testpc import TestPc, Connection
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline import NetworkAddress, RoutingInformation
from taf.config.testline.gnb import ClassicalBts, CU
from taf.config.testline import DU, RU
from taf.config.testline.core import RealCore5G
from taf.config.testline import RealEnb
from taf.config.testline.pdu import TopYoung, FACOM
from taf.config.testline.pdu import HBTE as PBHBTE
from taf.config.testline.attenuator import HBTE
from taf.config.testline.radio import RadioTypes
from taf.config.testline import LicenseKeeper


_cfg_dir = os.path.dirname(os.path.abspath(__file__))


# CU
# _cu = CU(
#    backhaul_site_oam_ip="10.101.48.85",
#    oam_ssh_connection_details=SshServiceDetails(
#        addr="10.101.48.85", username="toor4nsn", password="oZPS0POrRieRtu", port="22"
#    ),
#    oam_http_connection_details=HttpConnectionDetails(
#        addr="10.101.48.85", username="Nemuadmin", password="nemuuser"
#    ),
# )

# DU
# _common_unit_pdu = HBTE(addr="10.68.87.178", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
# _lmp_connection_0 = SshServiceDetails(
#     addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
# )
#
# _capacity_unit_0 = CapacityUnit(addr="192.168.253.17")
#
# _common_unit_0 = CommonUnit(
#     lmp_connection=_lmp_connection_0,
#     capacity_units=[_capacity_unit_0],
#     pdu_port=_common_unit_pdu.pdu_ports[4],
# )


# RU
_ru_1_pdu = PBHBTE(addr="10.68.87.213", port_numbers=[4])
_ru1 = RU(
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52",
        username="rfsw",
        password="HfBKgqIOogKY3BlGtiniuCI9bs76C8jYsAY6vw8f/Tw=",
    ),
    lmp_connection=SshServiceDetails(addr="", username=""),
    pdu_port=_ru_1_pdu.pdu_ports[4],
    ru_hw_group="",
    serial_number="CV193500854",
    radio_type=RadioTypes.AEQN.value,
)

_ru_2_pdu = PBHBTE(addr="10.101.45.46", port_numbers=[1])
_ru2 = RU(
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1",
        username="rfsw",
        password="HfBKgqIOogKY3BlGtiniuCI9bs76C8jYsAY6vw8f/Tw=",
    ),
    lmp_connection=SshServiceDetails(addr="", username=""),
    pdu_port=_ru_2_pdu.pdu_ports[1],
    ru_hw_group="",
    serial_number="CV193601214",
    radio_type=RadioTypes.AEQN.value,
)


# DU
_gnb_pdu1 = PBHBTE(addr="10.68.87.90", port_numbers=[8])
_gnb_pdu2 = TopYoung(addr="10.68.87.93", port_numbers=[1])

_gnb_1_airscale_cu_capacity_unit_left = CapacityUnit(
    addr="1.1.1.1", rus=[_ru1], hardware_type="ABIO"
)
_gnb_1_airscale_cu_capacity_unit_right = CapacityUnit(
    addr="1.1.1.1", rus=[_ru2], hardware_type="ABIO"
)

_common_unit1 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_gnb_1_airscale_cu_capacity_unit_left],
    pdu_port=_gnb_pdu1.pdu_ports[8],
    hardware_type="ASIL",
)

_common_unit2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.119", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_gnb_1_airscale_cu_capacity_unit_right],
    pdu_port=_gnb_pdu2.pdu_ports[1],
    hardware_type="ASIL",
)

_airscale1 = Airscale(common_units=[_common_unit1])

_airscale2 = Airscale(common_units=[_common_unit2])

# CU
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.101.48.85",
        v6=None,
        vlan_id=None,
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.48.85", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.48.85", username="Nemuadmin", password="nemuuser"
    ),
    f1m=None,
    f1c=None,
    f1u=None,
    x2c=NetworkAddress(
        v4="10.101.48.85",
        v6=None,
        vlan_id=None,
    ),
    x2u=NetworkAddress(
        v4="10.101.48.85",
        v6=None,
        vlan_id=None,
    ),
    s1u=NetworkAddress(
        v4="10.101.48.85",
        v6=None,
        vlan_id=None,
    ),
)


_du1 = DU(
    airscale=_airscale1,
    rus=[_ru1],
    f1_m_ip_addr="192.168.255.129",
)


_du2 = DU(
    airscale=_airscale2,
    rus=[_ru2],
)

_cbts1 = ClassicalBts(cu=_cu, dus=[_du1], instance_id="10353", global_bts_id="10353")

_cbts2 = ClassicalBts(cu=_cu, dus=[_du2], instance_id="10353", global_bts_id="10353")

_core = RealCore5G(mcc=262, mnc=3)

# airscale
# _airscale_0 = Airscale(common_units=[_common_unit_0])

# 5G RU
# _ru_pdu = HBTE(addr="10.68.87.213", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
# _ru = RU(
#    ru_hw_group="hw_group",
#    default_ssh_connection_details=SshServiceDetails(
#        addr="172.22.48.2", username="root", password="umniedziala"
#    ),
#    lmp_connection=SshServiceDetails(
#        addr="172.22.48.2", username="root", password="umniedziala"
#    ),
#    pdu_port=_ru_pdu.pdu_ports[4],
# )

# _du_0 = DU(airscale=_airscale_0, rus=[_ru], f1_m_ip_addr="10.101.48.85")


_test_pc1 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.70.230.164", username="ute", password="ute"
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_cbts1.dus[0].airscale.common_units[0],
            interface_type="lmp",
        )
    ],
)

_test_pc2 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.70.230.165", username="ute", password="ute"
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_cbts2.dus[0].airscale.common_units[0],
            interface_type="lmp",
        )
    ],
)


tl = TestLine(
    test_pc=_test_pc1,
    test_pcs=[_test_pc1, _test_pc2],
    gnbs=[_cbts1, _cbts2],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_FULLRACK_SA_ASILL_ABIOB1_AEQN-ASILR_ABIOB4_AEQN",
    core=_core,
)


__all__ = ["tl"]
