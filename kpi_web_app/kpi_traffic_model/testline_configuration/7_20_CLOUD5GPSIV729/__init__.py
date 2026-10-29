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
    os.path.dirname(os.path.abspath(__file__)), "ue_config_wnc_tl729.yaml"
)

# vm UTE
_test_pc_gnb = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.28.0.61", username="ute", password="ute"
    )
)

_test_pc_enb = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.28.0.62", username="ute", password="ute"
    )
)

_AEQD = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.14.48.220", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=[0],
    radio_type="AEQD",
)

_du_capacity_unit = CapacityUnit(
    addr="fsp1_c", hardware_type="ABIL", hardware_version="M02"
)


_du_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_du_common_unit_0 = CommonUnit(
    lmp_connection=_du_lmp_connection,
    capacity_units=[_du_capacity_unit],
    hardware_type="ASIK",
    hardware_version="M01",
)

_du = DU(Airscale(common_units=[_du_common_unit_0]), rus=[_AEQD])


# _cu = CU(backhaul_site_oam_ip='10.14.48.220',
# declaration d'une route statique
# NetworkAddress(v4='10.44.77.80',
#                v6=None,
#                 vlan_id=837,
#                 routing=RoutingInformation(gateway='10.44.77.177',
#                                            ip_prefix_length=28))
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.14.48.220",
        vlan_id=1000,
        routing=RoutingInformation(gateway="10.14.49.254", ip_prefix_length=0),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.14.48.220", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.14.48.220", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(v4="10.28.25.105", vlan_id=4002),
    x2u=NetworkAddress(v4="10.28.25.105", vlan_id=4002),
    s1c=NetworkAddress(v4="10.28.25.106", vlan_id=4002),
    s1u=NetworkAddress(v4="10.28.25.106", vlan_id=4002),
)

_cbts = ClassicalBts(cu=_cu, dus=[_du], instance_id=23262, global_bts_id=23262)

_core_5G_real = RealCore5G(mcc="540", mnc="01")


# _qualcomm = Qualcomm(
#    ssh_connection_details=SshServiceDetails(addr='10.0.96.1', username='user', password='pwd'),
#    serial_number='abcd',
#    qxdm_version=1,
#    ue_type=QualcommUeType.android,
#    com_port=9857,
#    heartbeat_port=5962,
#    server_command_input_port=1234,  # type: int
#    server_qxdm_messages_port=2345,  # type: int
#    server_command_output_port=3456,  # type: int
#    message_stream_port=4567,  # type: int
#    iperf_details=_iperf,  # type: Optional[IperfDataTransferDetails]
#    imsi='123456777',
#    sec_key='xxxxxxxxxxxxx',
#    capabilities=['REAL_UE', 'REAL_QUALCOMM_UE']  # type: Optional[List[str]]
# )


_du_enb_capacity_unit = CapacityUnit(
    addr="fsp1_c", hardware_type="ABIA", hardware_version="A101"
)

_du_enb_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_eNB_common_unit = CommonUnit(
    lmp_connection=_du_enb_lmp_connection,
    capacity_units=[_du_enb_capacity_unit],
    hardware_type="ASIA",
    hardware_version="A101",
)
_real_enb = Airscale(common_units=[_eNB_common_unit])
_lte_real_enb = RealEnb(
    airscale=_real_enb,
    x2_link_addr=NetworkAddress(
        v4="10.28.25.112",
        routing=RoutingInformation(gateway="10.28.25.110", ip_prefix_length=29),
    ),
    instance_id=22262,
    global_bts_id=22262,
)


tl = TestLine(
    test_pc=[_test_pc_gnb, _test_pc_enb],
    gnbs=[_cbts],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_QC_ASIKL_ABILB1_AEQD_EPC_ENB_4Mimo",
    core=_core_5G_real,
    enbs=[_lte_real_enb],
)


tl_name = "7-20-CLOUD5GPSIV729"

__all__ = ["tl"]
