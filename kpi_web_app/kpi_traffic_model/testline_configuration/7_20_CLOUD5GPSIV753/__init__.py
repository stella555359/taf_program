__maintainer__ = "Fabienne Magueur"
__team__ = "MN 5G RAN I&V 2 5 SG"
__email__ = "fabienne.magueur@nokia.com"
__owner_email__ = "fabienne.magueur@nokia.com"

import os
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
)
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline.gnb.networkaddress import NetworkAddress, RoutingInformation
from taf.config.testline.pdu import ATEN
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.radio import RU
from taf.config.testline.core import RealCore5G
from taf.config.testline.enb import RealEnb

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))
os.environ["ABSTRACT_LIB_CONFIG"] = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "ue_config_wnc_tl753.yaml"
)

# vm UTE
_test_pc_gnb = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.0.101.58", username="localuser", password="10c@1user"
    )
)
_AEQA = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.34", username="root", password="umniedziola"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.14.33.54", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=[0],
    radio_type="AEQA",
)

_AEQN = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.34", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.14.33.54", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=[0],
    radio_type="AEQN",
)

_du_capacity_unit = CapacityUnit(
    addr="fsp1_c", hardware_type="ABIL", hardware_version="A102"
)


_du_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_du_common_unit_0 = CommonUnit(
    lmp_connection=_du_lmp_connection,
    capacity_units=[_du_capacity_unit],
    hardware_type="ASIK",
    hardware_version="A101",
)

_du = DU(Airscale(common_units=[_du_common_unit_0]), rus=[_AEQN, _AEQA])


_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.14.33.54",
        vlan_id=1000,
        routing=RoutingInformation(gateway="10.14.49.254", ip_prefix_length=0),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.14.33.54", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.14.33.54", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(v4="10.28.6.201", vlan_id=4002),
    x2u=NetworkAddress(v4="10.28.6.201", vlan_id=4002),
    s1c=NetworkAddress(v4="10.28.6.202", vlan_id=4002),
    s1u=NetworkAddress(v4="10.28.6.202", vlan_id=4002),
)

_cbts = ClassicalBts(cu=_cu, dus=[_du], instance_id=753, global_bts_id=23135)

_core_5G_real = RealCore5G(mcc="540", mnc="01")

# eNB: commented for now as the testline is not declared in UTE yet
# _du_enb_capacity_unit = CapacityUnit(addr='fsp1_c',
#                                     hardware_type='ABIA',
#                                     hardware_version='A103')
#
# _du_enb_lmp_connection = SshServiceDetails(addr='192.168.255.129',
#                                           username='toor4nsn',
#                                           password='oZPS0POrRieRtu')
#
# _eNB_common_unit = CommonUnit(lmp_connection=_du_enb_lmp_connection,
#                              capacity_units=[_du_enb_capacity_unit],
#                              hardware_type='ASIA',
#                              hardware_version='A101')
# _real_enb = Airscale(common_units=[_eNB_common_unit])
# _lte_real_enb = RealEnb(airscale=_real_enb,
#                        x2_link_addr=NetworkAddress(v4='10.28.14.49',
#                                                    routing=RoutingInformation(gateway='10.28.6.206',
#                                                                               ip_prefix_length=32)),
#                        instance_id=XXXXXXXX,
#                        global_bts_id=XXXXXXX)


tl = TestLine(
    test_pc=[_test_pc_gnb],
    gnbs=[_cbts],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_QC_ASIKL_ABILB1_AEQN_ENB",
    core=_core_5G_real,
)


tl_name = "7-20-CLOUD5GPSIV753"

__all__ = ["tl"]
