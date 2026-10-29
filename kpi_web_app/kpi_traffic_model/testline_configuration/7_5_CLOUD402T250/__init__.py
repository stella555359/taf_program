import os
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
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline import Enb, SimEnb, RealEnb, LTEEmuEnb, PrismaEnb, DocomoEnb
from taf.compatibility.configuration import TestlineWrapper

# added in taf.meta 5.4
from taf.config.testline.ue import (
    AirphoneCloud,
    Airphone,
    Prisma,
    TM500,
    Qualcomm,
    QualcommUeType,
    Android,
    ASC,
)
from taf.config.testline.attenuator import AttenuationPort, TopYoung
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)
from taf.config.testline.appserver import AppServer

__maintainer__ = "Cui Lingxue"
__team__ = (
    "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_01_GMS <I_NSB_MN_5GSC_MMW_SC_PZ_HZ_01@internal.nsn.com>"
)
__email__ = "lingxue.cui@nokia-sbell.com"

# common
__all__ = ["tl"]

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.253", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)


# App Server
_appserver_ssh = SshServiceDetails(
    addr="10.57.162.4", username="mmw_sg1", password="mm@1"
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.162.4",
    iperf_path="iperf",
    port="5410",
)

_appserver = AppServer(iperf_details=_iperf_details_on_appserver)

# #Cobham
_tm500_ssh = SshServiceDetails(
    addr="10.57.130.96", username="nokia5G", password="noki@123"
)

_tm500_iperf = IperfDataTransferDetails(
    ssh_connection_details=_tm500_ssh,
    network_interface_address="9.6.6.6",
    iperf_path="/cygdrive/c/Users/nokia5G/Desktop/iperf_2.0.8/",
    port="41501",
)

_tm500 = TM500(
    tma_host=SshServiceDetails(
        addr="10.57.130.96", username="nokia5G", password="noki@123", private_key=""
    ),
    tma_command_port=5030,
    pdu_port=None,
    tma_path="/cygdrive/c/Program Files (x86)/Aeroflex/TM500/5G NR - NLA 4.48.0/Test Mobile Application/"
    "TmaApplication.exe",
    iperf_details=_tm500_iperf,
    asc=ASC(ipaddr="192.168.10.8", port=10011),
)

# RealEnb---------------------------------------------------------
_real_enb_pdu = FACOM(addr="10.57.241.169", port_numbers=[6])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.237.61", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[6],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, instance_id=250, global_bts_id=250)

# 5GRU------------------------------------
_attenuator = TopYoung(ip_addr="10.57.249.44", port=23, attenuation_port_numbers=[5, 6])
_ru_pdu = FACOM(addr="10.57.249.5", port_numbers=[8])

_ru = RU(
    ru_hw_group="Below6GHZ",  # Above6GHZ or Below6GHZ
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_ru_pdu.pdu_ports[8],
    radio_type=RadioTypes.AEQN,
    attenuation_ports=[
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[6],
    ],
)

# #DU
_lmp_connection = SshServiceDetails(
    addr="10.57.237.49", username="toor4nsn", password="oZPS0POrRieRtu"
)
# as the configuration of TL250 ASKI and ABIL are on right hand side, the IP of ABIL master is different.
_capacity_unit = CapacityUnit(addr="192.168.253.36")

_gnb_pdu = FACOM(addr="10.57.241.169", port_numbers=[1])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[1],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru], f1_m_ip_addr="10.57.237.49")

# CU
_cu = CU(
    backhaul_site_oam_ip="10.57.237.49",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.237.49", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.237.49", username="Nemuadmin", password="nemuuser"
    ),
)

# classicalbts------------------------------------------------
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=250, global_bts_id=250)

# #cloud_topology------------------------------------------------
_tl_cloud_topology = "Refers to TAF UTE TL Type"

tl = TestLine(
    test_pc=_host,
    test_pcs=[_host],
    appserver=_appserver,
    enbs=[_lte_real_enb],
    gnbs=[_classical_bts],
    ues=[_tm500],
    tl_cloud_topology=_tl_cloud_topology,
    attenuator=_attenuator,
)
