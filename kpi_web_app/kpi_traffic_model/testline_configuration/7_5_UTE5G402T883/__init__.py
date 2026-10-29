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
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import AirphoneCloud, Airphone, Prisma, TM500
from taf.config.testline import Enb, SimEnb, RealEnb, LTEEmuEnb, PrismaEnb, DocomoEnb
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.nms import Netact

__maintainer__ = "Li Qing"  # TL owner name
__team__ = "I_MN_5G_RAN_IV4_LINE_HZG_8_IV@internal.nsn.com"  # TL owner's team
__email__ = "qing.li@nokia-sbell.com"  # TL owner's email

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

##testPc(taf)
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.13", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# 5GRU for classicalBTS
# PB for RU
_ru_pdu = FACOM(addr="10.71.196.59", port_numbers=[1])

_ru = RU(
    ru_hw_group="AEQZ",
    serial_number="1M203907049",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.71.218.144", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu.pdu_ports[1],
)

_ru_pdu2 = FACOM(addr="10.71.196.59", port_numbers=[2])
_ru2 = RU(
    ru_hw_group="AEQZ",
    serial_number="1M202406698",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.71.218.142", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu2.pdu_ports[2],
)

_ru_pdu3 = FACOM(addr="10.71.196.59", port_numbers=[3])
_ru3 = RU(
    ru_hw_group="AEQZ",
    serial_number="1M222643806",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.71.218.143", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu3.pdu_ports[3],
)

_ru_pdu4 = FACOM(addr="10.71.196.58", port_numbers=[2])
_ru4 = RU(
    ru_hw_group="AHPB",
    serial_number="K9224138871",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.71.218.155", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu4.pdu_ports[2],
)

_ru_pdu5 = FACOM(addr="10.71.196.58", port_numbers=[3])
_ru5 = RU(
    ru_hw_group="AHPB",
    serial_number="K9224138870",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.71.218.154", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu5.pdu_ports[3],
)

##classical gNB parameter
# gNB lmp ip
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
# abil internal ip
_capacity_unit = CapacityUnit(addr="192.168.253.20")
# gNB PB
_gnb_pdu = FACOM(addr="10.71.196.58", port_numbers=[1])
_gnb_test_pc_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.13", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[1],
    test_pc=_gnb_test_pc_0,
)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(
    airscale=_airscale,
    rus=[_ru, _ru2, _ru3, _ru4, _ru5],
    f1_m_ip_addr="10.71.212.2",
)

# gNB oam mplane ip
_cu = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.212.2", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.212.2", username="Nemuadmin", password="nemuuser"
    ),
)

# RealEnb
_lmp_connection_enb = SshServiceDetails(
    addr="1.1.1.1", username="toor4nsn", password="oZPS0POrRieRtu"
)
_enb_pdu = FACOM(addr="10.57.1.1", port_numbers=[2])
_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection_enb,
    capacity_units=[],
    pdu_port=_enb_pdu.pdu_ports[2],
)
_real_enb = Airscale(common_units=[_common_unit_1])
_lte_real_enb = RealEnb(airscale=_real_enb)


## switch Dtor
# switch prot to ASIK EIF
_dell_s4048on_ssh = SshServiceDetails(
    addr="1.1.1.1", port="1/7", username="5gran", password="nokia123"
)
_dell_s4048on_switch = DellS4048ONSwitch(_dell_s4048on_ssh)

##cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

# instance_id = MRBTS_ID
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=883)
# netact ip
_netact = Netact("10.106.161.25")
tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    enbs=[],
    switches=[_dell_s4048on_switch],
    tl_cloud_topology=_tl_cloud_topology,
    nms=_netact,
)

tl = TestlineWrapper(tl)
