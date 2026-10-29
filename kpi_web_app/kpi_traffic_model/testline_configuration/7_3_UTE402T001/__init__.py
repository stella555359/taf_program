import os

from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.gnb import CU, ClassicalBts
from taf.config.testline import DU, RU
from taf.config.testline.airscale import CapacityUnit, CommonUnit, Airscale
from taf.config.testline.pdu import APC
from taf.config.testline.ue import Android
from taf.config.testline.core import EPCSim
from taf.config.testline import RealEnb

__maintainer__ = "Huijun Rong"
__team__ = "NSB MN HetRAN Pz DCM Ops"
__email__ = "huijun.rong@nokia-sbel.com"
__owner_email__ = "huijun.rong@nokia-sbel.com"

# common
__all__ = ["tl"]

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

# Test PC
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.68.235.82", username="ute", password="ute"
    )
)
_docker_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.68.235.42", username="dcapuser", password="ute"
    )
)
_tce_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="166.166.166.40", username="dcapuser", port=49151
    )
)
External_PCs_For_CellTrace = dict(docker=_docker_pc, tce=_tce_pc)
# epcsim
_epc_sim = EPCSim(
    mme_ip="10.68.235.83",
    mcc="440",
    mnc="10",
    tac="61",
    default_ssh_connection_details=SshServiceDetails(
        addr="10.68.235.83", username="ute", password="ute"
    ),
    edaemon_port=10000,
    egate_port=20000,
    dir_path="/opt/iphy/EPCsim_825328",
    cfg_filename="lab5g_BJ_qcomm.cfg",
)

# Prisma
_airmosaic_ssh = SshServiceDetails(
    addr="127.0.0.1", username="CNHZ5GRAN1108+nokia", password="Tester123"
)
_airmosaic_harness = HttpConnectionDetails(addr="127.0.0.1", port=8090)
_lsu_uu_ssh = SshServiceDetails(addr="127.0.0.1", username="user", password="user")
_tstm_uu_ssh = SshServiceDetails(addr="127.0.0.1", username="user", password="user")

_iperf_data_transfer = IperfDataTransferDetails(
    ssh_connection_details=SshServiceDetails(
        addr="10.68.235.83", username="ute", password="ute"
    ),
    network_interface_address="3.7.255.254",
    iperf_path="/usr/bin/iperf",
)

_qualcomm = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.68.249.194", username="ute", password="ute"
    ),
    # serial_number='35ca1930',
    serial_number="87812154",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf_data_transfer,
    capabilities=["REAL_ANDROID_UE"],
)

# RealEnb
_real_enb_pdu = APC(addr="127.0.0.1", port_numbers=[3])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.1", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[3],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=None)

# 5GRU for classicalBTS
_ru_pdu = APC(addr="127.0.0.1", port_numbers=[3])

_ru = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.34", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_ru_pdu.pdu_ports[3],
)

# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="6.6.6.6")

_gnb_pdu = APC(addr="10.68.235.34", port_numbers=[3])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports,
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru])


# CU
_cu = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.255.129", username="Nemuadmin", password="nemuuser"
    ),
)


# cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu)

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    core=_epc_sim,
    enbs=[_lte_real_enb],
    ues=[_qualcomm],
    tl_cloud_topology=_tl_cloud_topology,
)
