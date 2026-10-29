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
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.core import EPCSim, LTEEmuCore, PrismaCore
from taf.config.testline import RU, DU
from taf.config.testline.pdu import HBTE, TopYoung
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import AirphoneCloud, Airphone, Prisma, TM500
from taf.config.testline import Enb, SimEnb, RealEnb, LTEEmuEnb, PrismaEnb, DocomoEnb
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.nms import Netact
from taf.config.testline.appserver import AppServer
from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.config.testline.ue import Android
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)

__maintainer__ = "Li Mengting"  # TL owner name
__team__ = "I_NSB_MN_5GSC_5G_PZ_HZ_04_01@internal.nsn.com"  # TL owner's team
__email__ = "mengting.li@nokia-sbell.com"  # TL owner's email

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

##testPc(taf)
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.125", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# enbPC
_enb_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.98", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# 5GRU for classicalBTS
# PB for RU
_ru_pdu1 = HBTE(addr="10.71.196.121", port_numbers=[2])
_ru1 = RU(
    ru_hw_group="AWHHF",
    serial_number="EB2105R9390",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.71.218.42", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu1.pdu_ports[2],
)

_ru_pdu2 = HBTE(addr="10.71.196.118", port_numbers=[5])
_ru2 = RU(
    ru_hw_group="AWHHF",
    serial_number="EB193661015",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.71.218.230", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu2.pdu_ports[5],
)

_ru_pdu3 = HBTE(addr="10.71.196.121", port_numbers=[3])
_ru3 = RU(
    ru_hw_group="AWHHD",
    serial_number="EB2237R0312",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.71.218.41", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu3.pdu_ports[3],
)

##classical gNB parameter
# gNB lmp ip
_gnb_lmp_connection_0 = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
# abil internal ip
_capacity_unit = CapacityUnit(addr="192.168.253.20")
# gNB PB
_gnb_pdu_0 = HBTE(addr="10.71.196.117", port_numbers=[2])
_gnb_test_pc_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.125", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_gnb_common_unit_0 = CommonUnit(
    lmp_connection=_gnb_lmp_connection_0,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu_0.pdu_ports[2],
    test_pc=_gnb_test_pc_0,
)
_gnb_airscale_0 = Airscale(common_units=[_gnb_common_unit_0])
_gnb_du_0 = DU(
    airscale=_gnb_airscale_0,
    rus=[_ru1, _ru2, _ru3],
    f1_m_ip_addr="10.71.212.198",
)

# gNB oam mplane ip
_gnb_cu_0 = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.212.198", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.212.198", username="Nemuadmin", password="nemuuser"
    ),
)

# instance_id = MRBTS_ID
_classical_bts_0 = ClassicalBts(dus=[_gnb_du_0], cu=_gnb_cu_0, instance_id=310)

# RealEnb
_enb_lmp_connection_0 = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
_enb_pdu_0 = HBTE(addr="10.71.196.117", port_numbers=[2])
_enb_common_unit_0 = CommonUnit(
    lmp_connection=_enb_lmp_connection_0,
    capacity_units=[],
    pdu_port=_enb_pdu_0.pdu_ports[2],
    test_pc=None,
    hardware_type=None,
)
_real_enb_0 = Airscale(common_units=[_enb_common_unit_0])
_lte_real_enb_0 = RealEnb(
    system_module=_real_enb_0,
    oam_ip=NetworkAddress(v4="10.71.212.199"),
    instance_id=310,
    rms=[],
)

## switch Dtor
# switch port to ASIK EIF
_dell_s4048on_ssh = SshServiceDetails(
    addr="10.57.129.215", port="1/3", username="5gran", password="nokia123"
)
_dell_s4048on_switch = DellS4048ONSwitch(_dell_s4048on_ssh)

##cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"


# netact ip
_netact = Netact("10.106.161.25")

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts_0],
    enbs=[_lte_real_enb_0],
    switches=[_dell_s4048on_switch],
    nms=_netact,
    tl_cloud_topology=_tl_cloud_topology,
)

tl = TestlineWrapper(tl)
