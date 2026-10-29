__maintainer__ = "Kongshuai Fan"
__team__ = "I_MN_5G_RAN_IV4_QT_HZG_GMS <I_MN_5G_RAN_IV4_QT_HZG@internal.nsn.com>"
__email__ = "kongshuai.fan@nokia-sbell.com"


import os
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    TelnetConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.gnb.gnb import ClassicalBts, CU
from taf.config.testline.gnb.du import DU
from taf.config.testline.radio import RU, RadioModule
from taf.config.testline.attenuator import AttenuationPort, HBTE
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.enb import RealEnb
from taf.config.testline.core import EPCSim
from taf.config.testline.ue import TM500
from taf.config.testline.appserver import AppServer
from taf.config.testline.pdu import FACOM, PduPort
from taf.config.testline.ue import Prisma

# from taf.compatibility.configuration import TestlineWrapper
_cfg_dir = os.path.dirname(os.path.abspath(__file__))

#########Testpc##########
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.106.164.48", username="root", password="uteadmin"
    )
)

#########CU##########
_cu = CU(
    backhaul_site_oam_ip="10.57.236.195",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.236.195", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.236.195", username="Nemuadmin", password="nemuuser"
    ),
)

#########DU##########
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_common_unit_pdu = FACOM(addr="10.57.241.162", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_capacity_unit = CapacityUnit(addr="192.168.253.20")

_common_unit = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_common_unit_pdu.pdu_ports[4],
    hardware_type="ASIK",
    hardware_version="A.101",
)

_airscale = Airscale(common_units=[_common_unit])

#########5G RU##########
_5g_ru_pdu = FACOM(addr="10.57.249.13", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru = RU(
    ru_hw_group="mmw",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.49", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="root", password="umniedziala"
    ),
    pdu_port=_5g_ru_pdu.pdu_ports[3],
    radio_type="AEUD",
)

# attenuator
_attenuator = HBTE(
    ip_addr="10.106.211.141",
    port=5000,
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    model="PA-16-16-6-127-0.5-B-S",
)
#########DU##########
_du = DU(
    airscale=_airscale,
    rus=[_ru],
    f1_m_ip_addr="10.57.236.195",
    f1_c_ip_addr="10.57.236.195",
    f1_u_ip_addr="10.57.236.195",
)

#########ClassicalBts##########
_classicalbts = ClassicalBts(cu=_cu, dus=[_du])

#########4G RU##########
_4g_ru_pdu = FACOM(addr="10.57.246.244", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_RadioModule = RadioModule(
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="umniedziala"
    ),
    pdu_port=_4g_ru_pdu.pdu_ports[3],
)

#########RealEnb##########
_real_enb_pdu = FACOM(addr="10.57.241.162", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_common_unit_enb = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.236.196", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[5],
    hardware_type="ASIA",
    hardware_version="A.103",
)

_real_enb = Airscale(common_units=[_common_unit_enb])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=[_RadioModule])

#########EPCSim##########
_epc_sim = EPCSim(
    mme_ip=None,
    tac=None,
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.170.46", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    mcc=None,
    mnc=None,
    dir_path=None,
    cfg_filename=None,
)

_airmosaic_ssh = SshServiceDetails(
    addr="10.57.130.51", username="nokia5G", password="noki@123"
)
_airmosaic_harness = HttpConnectionDetails(addr="10.57.130.51", port=8090)
_lsu_uu_ssh = SshServiceDetails(addr="10.57.238.27", username="user", password="user")
_tstm_uu_ssh = SshServiceDetails(addr="10.57.238.27", username="user", password="user")


_appserver_ssh = SshServiceDetails(
    addr="10.106.164.48", username="root", password="uteadmin"
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.106.164.48",
    iperf_path="iperf",
    port=5002,
)
_appserver = AppServer(_iperf_details_on_appserver)

_ue_prisma = Prisma(
    airmosaic_ssh_connection_details=_airmosaic_ssh,
    airmosaic_harness_connection_details=_airmosaic_harness,
    lsu_uu_ssh_connection_details=_lsu_uu_ssh,
    tstm_uu_ssh_connection_details=_tstm_uu_ssh,
    iperf_details=_iperf_details_on_appserver,
)
_ue_prisma.ue_type = "prisma"

#########TestLine##########
tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_classicalbts],
    enbs=[_lte_real_enb],
    core=_epc_sim,
    ues=[_ue_prisma],
    appserver=_appserver,
    attenuator=_attenuator,
    tl_cloud_topology="hgz-tl118",
)

# tl = TestlineWrapper(tl)

__all__ = ["tl"]
