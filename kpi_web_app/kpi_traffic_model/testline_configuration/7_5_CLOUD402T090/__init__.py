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
from taf.config.testline.gnb.networkaddress import NetworkAddress

# from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.nms import Netact

__maintainer__ = "Xie JiaLi"  # TL owner name
__team__ = "I_MN_5G_RAN_IV4_LINE_HZG_8_IV@internal.nsn.com"  # TL owner's team
__email__ = "jia.xie@nokia-sbell.com"  # TL owner's email

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

##testPc(taf)
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.25", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# 5GRU for classicalBTS
# PB for RU
_ru_pdu = FACOM(addr="10.57.241.165", port_numbers=[1, 2])
_ru = RU(
    ru_hw_group="AEQD",
    serial_number="6Q194401773",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.5", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.167.103", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    pdu_port=_ru_pdu.pdu_ports[2],
)

_ru2 = RU(
    ru_hw_group="AEQD",
    serial_number="6Q185212550",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.5", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.167.104", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu.pdu_ports[1],
)

##classical gNB parameter
# gNB lmp ip
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
# abil internal ip
_capacity_unit = CapacityUnit(addr="192.168.253.20")
# gNB PB
_gnb_pdu = FACOM(addr="10.57.241.164", port_numbers=[3])
_gnb_test_pc_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.25", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[3],
    test_pc=_gnb_test_pc_0,
)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(airscale=_airscale, rus=[_ru, _ru2])
# _du = DU(airscale=_airscale, rus=[_ru])

# gNB oam mplane ip
_cu = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.236.235", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.236.235", username="Nemuadmin", password="nemuuser"
    ),
)

# RealEnb
_lmp_connection_enb = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
_enb_pdu = FACOM(addr="10.57.241.164", port_numbers=[2])
_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection_enb,
    capacity_units=[],
    pdu_port=_enb_pdu.pdu_ports[2],
    test_pc=None,
    hardware_type=None,
)
_real_enb = Airscale(common_units=[_common_unit_1])
_lte_real_enb = RealEnb(
    system_module=_real_enb,
    rms=None,
    oam_ip=NetworkAddress(v4="10.57.236.227"),
    instance_id=4090,
)


## switch Dtor
# switch prot to ASIK EIF
_dell_s4048on_ssh = SshServiceDetails(
    addr="10.57.129.136", port="1/19", username="5gran", password="nokia123"
)
_dell_s4048on_switch = DellS4048ONSwitch(_dell_s4048on_ssh)

##cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

# instance_id = MRBTS_ID
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=90)
# netact ip
_netact = Netact("10.107.178.214")
tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    enbs=[_lte_real_enb],
    switches=[_dell_s4048on_switch],
    tl_cloud_topology=_tl_cloud_topology,
    nms=_netact,
)
