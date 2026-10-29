__maintainer__ = "MN RAN L2 SW 2 KRK Vrf SG"
__team__ = "I_5GSC_SW_ENG_KRK_VRF_GMS"
__email__ = "I_5GSC_SW_ENG_KRK_VRF_GMS <I_5GSC_SW_ENG_KRK_VRF@internal.nsn.com>"

import os
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.gnb import ClassicalBts, CU
from taf.config.testline import DU, RU
from taf.config.testline.pdu import FPFH
from taf.config.testline import NetworkAddress
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.appserver import AppServer
from taf.config.testline.ue import Prisma
from taf.config.testline.attenuator import JFW


_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT411.sc5g.krk-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

# gNB

_pdu1 = FPFH(
    port_numbers=[1],
    addr="fpfh-gd06-1.leg.krk-lab.nsn-rdnet.net",
    login="admin",
    password="emssim123",
)

_ru_du1 = RU(
    ru_hw_group="",
    default_ssh_connection_details=SshServiceDetails(addr="", username=""),
    lmp_connection=SshServiceDetails(addr="", username=""),
    radio_type="AEQE",
)

_abil1_du1 = CapacityUnit(addr="192.168.253.20", hardware_type="ABIL")

_asik_du1 = CommonUnit(
    pdu_port=_pdu1.pdu_ports[1],
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_abil1_du1],
    hardware_type="ASIK",
)

_du1 = DU(airscale=Airscale(common_units=[_asik_du1]), rus=[_ru_du1])

_cu = CU(
    backhaul_site_oam_ip="10.0.1.111",
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.255.129", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(v4="10.0.1.1", vlan_id=1911),
    x2u=NetworkAddress(v4="10.0.1.1", vlan_id=1911),
    s1u=NetworkAddress(v4="10.0.1.1", vlan_id=1911),
)

_cbts = ClassicalBts(cu=_cu, dus=[_du1])

# Prisma

_airmosaic_ssh = SshServiceDetails(
    addr="7-7-UTE5GCLOUDT411.sc5g.krk-lab.nsn-rdnet.net",
    username="ute",
    password="ute",
)

_airmosaic_harness = HttpConnectionDetails(addr="", port=None)

_lsu_uu_ssh = SshServiceDetails(
    addr="172.25.30.150", username="user", password="user", proxy=_airmosaic_ssh
)

_tstm_uu_ssh = SshServiceDetails(
    addr="172.25.30.150", username="user", password="user", proxy=_airmosaic_ssh
)

_ue_host_ssh = SshServiceDetails(
    addr="SC5G-eNB-411-uesim.sc5g.krk-lab.nsn-rdnet.net",
    username="ute",
    password="ute",
)

_ue_host_iperf_details = IperfDataTransferDetails(
    ssh_connection_details=_ue_host_ssh,
    network_interface_address="192.168.60.124",
    iperf_path="/usr/bin/iperf",
)

_ue_prisma = Prisma(
    airmosaic_ssh_connection_details=_airmosaic_ssh,
    airmosaic_harness_connection_details=_airmosaic_harness,
    lsu_uu_ssh_connection_details=_lsu_uu_ssh,
    tstm_uu_ssh_connection_details=_tstm_uu_ssh,
    iperf_details=_ue_host_iperf_details,
    sec_key="11111111111111111111111111111111",
)

# Attenuator

_attenuator = JFW(
    ip_addr="10.83.176.48",
    port=501,
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8],
    model="50PA-628",
)

# Iper VM

_app_server_ssh = SshServiceDetails(
    addr="SC5G-eNB-411-uesim.sc5g.krk-lab.nsn-rdnet.net", username="ute", password="ute"
)

_app_server_iperf_details = IperfDataTransferDetails(
    ssh_connection_details=_app_server_ssh,
    network_interface_address="10.12.2.1",
    iperf_path="/usr/bin/iperf",
)

# Testline

tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    tl_cloud_topology="CLOUD_5G_ASIK_ABIL_AEQE",
    ues=[_ue_prisma],
    attenuator=[_attenuator],
    appserver=AppServer(_app_server_iperf_details),
)

__all__ = ["tl"]
