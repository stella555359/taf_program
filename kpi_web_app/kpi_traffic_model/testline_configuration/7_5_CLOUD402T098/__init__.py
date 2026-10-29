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
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.core import EPCSim, LTEEmuCore, PrismaCore
from taf.config.testline import RU, DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, HBTE, TopYoung
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import AirphoneCloud, Airphone, Prisma, TM500
from taf.config.testline import Enb, SimEnb, RealEnb, LTEEmuEnb, PrismaEnb, DocomoEnb
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.config.testline.nms import Netact
from taf.config.testline.gnb.networkaddress import NetworkAddress


__maintainer__ = "Jiang Shengyuan"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_8_GMS <I_MN_5G_RAN_IV4_LINE_HZG_8@internal.nsn.com>"
)
__email__ = "shengyuan.jiang@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

##testPc(taf)
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.189.11", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)


# 5GRU for classicalBTS
# PB for RU
_i20_pdu = HBTE(addr="10.57.241.163", port_numbers=range(1, 7))
_i21_pdu = TopYoung(addr="10.57.241.165", port_numbers=range(4, 7))
_i23_pdu = HBTE(addr="10.57.241.169", port_numbers=range(1, 7))
_j21_pdu = HBTE(addr="10.57.241.236", port_numbers=range(1, 7))


_ru_1 = RU(
    ru_hw_group="AEQN",
    serial_number="CV192600347",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.150.60", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_i20_pdu.pdu_ports[5],
)

_ru2 = RU(
    ru_hw_group="AEQN",
    serial_number="CV194200187",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.130.200", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_i20_pdu.pdu_ports[4],
)

_ru3 = RU(
    ru_hw_group="AEQN",
    serial_number="CV193402112",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.150.146", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_i20_pdu.pdu_ports[3],
)

_ru4 = RU(
    ru_hw_group="AQQL",
    serial_number="L1214304633",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.130.17", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_i23_pdu.pdu_ports[1],
)


_ru9 = RU(
    ru_hw_group="AEQY",
    serial_number="1M201202379",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.150.181", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_j21_pdu.pdu_ports[4],
)

##classical gNB parameter
# gNB lmp ip
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
# abil internal ip
_capacity_unit = CapacityUnit(addr="192.168.253.20")
# gNB PB
_bbu_pdu = HBTE(addr="10.57.241.164", port_numbers=range(1, 7))
# gNB VM
_gnb_test_pc_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.189.11", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_bbu_pdu.pdu_ports[1],
    test_pc=_gnb_test_pc_0,
)
_airscale = Airscale(common_units=[_common_unit_0])


_du = DU(airscale=_airscale, rus=[_ru_1, _ru2, _ru3, _ru4,_ru9])

# gNB oam mplane ip
_cu = CU(
    backhaul_site_oam_ip="10.57.227.165",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.236.236", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.236.236", username="Nemuadmin", password="nemuuser"
    ),
)


# ==================================================================================
# ==================================================================================
# ==================================================================================
# X2 ENB
_enb_pdu_0 = FACOM(addr="10.57.241.164", port_numbers=[2])

_enb_test_pc_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.87", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_enb_lmp_connection_0 = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
_enb_common_unit_0 = CommonUnit(
    lmp_connection=_enb_lmp_connection_0,
    capacity_units=[],
    pdu_port=_enb_pdu_0.pdu_ports[2],
    test_pc=_enb_test_pc_0,
    hardware_type=None,
)
_real_enb_0 = Airscale(common_units=[_enb_common_unit_0])
_lte_real_enb = RealEnb(
    system_module=_real_enb_0,
    oam_ip=NetworkAddress(v4="10.57.236.237"),
    instance_id=4098,
    rms=[],
)


## switch Dtor
# switch port to ASIK EIF
_dell_s4048on_ssh = SshServiceDetails(
    addr="10.57.129.140", port=20, username="5gran", password="nokia123"
)
_dell_s4048on_switch = DellS4048ONSwitch(_dell_s4048on_ssh)

##cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

# instance_id = MRBTS_ID
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=98)
# netact ip
_netact = Netact("10.107.178.214")

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    enbs=[_lte_real_enb],
    tl_cloud_topology=_tl_cloud_topology,
    nms=_netact,
    switches=[_dell_s4048on_switch],
)
