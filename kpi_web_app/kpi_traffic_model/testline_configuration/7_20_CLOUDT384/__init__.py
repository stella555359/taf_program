__maintainer__ = "Piotr Dziedzic"
__team__ = "I_SC_KRK_PROD_NITROGEN_GMS"
__email__ = "I_SC_KRK_PROD_NITROGEN@internal.nsn.com"
__owner_email__ = "piotr.dziedzic@nokia.com"

import os

from taf.config.testline import SshServiceDetails, HttpConnectionDetails
from taf.config.testline.testpc import TestPc
from taf.config.testline import RU, DU
from taf.config.testline.pdu import ATEN
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import ClassicalBts, CU
from taf.config.testline.airscale import CommonUnit, CapacityUnit, Airscale
from taf.config.testline.ue import Prisma
from taf.config.testline.enb import RealEnb  # currently unknown
from taf.config.testline.core import EPCSim  # currently unknown
from taf.config.testline.connection_details import IperfDataTransferDetails


_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.14.39.125",  # original ip in gitlab: '10.83.179.141'
        username="localuser",
        password="10c@1user",
    )
)

_ru_pdu = ATEN(addr="TO_UPDATE", port_numbers=[1])

_ru = RU(
    ru_hw_group="hw_group",
    radio_type="AHLOA",
    default_ssh_connection_details=SshServiceDetails(
        addr="TO_UPDATE", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="TO_UPDATE", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru_pdu.pdu_ports[1],
)

_cu = CU(
    backhaul_site_oam_ip="10.14.49.129",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.14.49.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.255.129", username="Nemuadmin", password="nemuuser"
    ),
)

_du_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_du_capacity_unit = CapacityUnit(
    addr="fsp1_c", hardware_type="ABIL", hardware_version="A101B1"
)

_du_common_unit = CommonUnit(
    lmp_connection=_du_lmp_connection,
    capacity_units=[_du_capacity_unit],
    hardware_type="ASIK",
)

_airmosaic_ssh = SshServiceDetails(
    addr="10.14.39.125", username="localuser", password="10c@1user"
)  # ssh not available
_airmosaic_harness = HttpConnectionDetails(addr="10.14.39.125", port=8090)
_lsu_uu_ssh = SshServiceDetails(
    addr="10.28.0.173", username="user", password="user", proxy=_airmosaic_ssh
)
_tstm_uu_ssh = SshServiceDetails(
    addr="10.28.0.173", username="user", password="user", proxy=_airmosaic_ssh
)
_prisma_config_file = None
_scripts_dir = None
_default_sid_file = None
_app_server_ssh = SshServiceDetails(
    addr="10.14.42.228", username="ran5g", password="nokia2018"
)
_ue_host_ssh = SshServiceDetails(addr="10.14.42.156", username="ftp", password="ftp")
_app_server_iperf_details = IperfDataTransferDetails(
    ssh_connection_details=_app_server_ssh,
    network_interface_address="192.168.60.254",
    iperf_path="/usr/bin/iperf",
    port=50001,
)
_ue_host_iperf_details = IperfDataTransferDetails(
    ssh_connection_details=_ue_host_ssh,
    network_interface_address="192.168.70.125",
    iperf_path="iperf",
    port=50002,
)


_iperf_data_transfer = IperfDataTransferDetails(
    ssh_connection_details=SshServiceDetails(
        addr="10.14.42.228", username="ran5g", password="nokia2018"
    ),
    network_interface_address="10.14.42.228",  # What is this adress?
    iperf_path="/usr/bin/iperf",
)

_ue_prisma = Prisma(
    airmosaic_ssh_connection_details=_airmosaic_ssh,
    airmosaic_harness_connection_details=_airmosaic_harness,
    lsu_uu_ssh_connection_details=_lsu_uu_ssh,
    tstm_uu_ssh_connection_details=_tstm_uu_ssh,
    iperf_details=_iperf_data_transfer,
)

# _core = EPCSim(mme_ip='10.1.1.100', mcc=311, mnc=489, tac=124,
#                default_ssh_connection_details=_testp_pc_ssh,
#                dir_path='/home/ute', cfg_filename='EPCoulu.cfg')
#

_common_unit_lte_ssh = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_airscale = Airscale(common_units=[_du_common_unit])

# _lteenb = RealEnb(airscale=_airscale, x2_link_addr = '10.1.1.3')

_du = DU(airscale=_airscale, rus=[_ru])

_bts = ClassicalBts(cu=_cu, dus=[_du])


tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_bts],
    tl_cloud_topology="test",
    ues=[_ue_prisma]
    # enbs=[_lteenb],
    # core=_core,
)


__all__ = ["tl"]
