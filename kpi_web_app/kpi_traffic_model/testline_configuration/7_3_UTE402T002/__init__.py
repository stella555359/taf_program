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
from taf.config.testline.attenuator import AttenuationPort, TopYoung
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)

__maintainer__ = "Xibing Wang"
__team__ = "NSB MN HetRAN Pz DCM BJG 1 Vrf"
__email__ = "xibing.wang@nokia-sbel.com"
__owner_email__ = "xibing.wang@nokia-sbel.com"

# common
__all__ = ["tl"]

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

# Test PC
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.71.24.65", username="ute", password="ute"
    )
)

# epcsim
_epc_sim = EPCSim(
    mme_ip="10.68.45.139",
    mcc="262",
    mnc="03",
    tac="123",
    default_ssh_connection_details=SshServiceDetails(
        addr="10.68.45.139", username="ute", password="ute"
    ),
    edaemon_port=10000,
    egate_port=20111,
    dir_path="/home/ute/epcSim",
    cfg_filename="lab5g_BJ_BC457_plmn46008.update.cfg",
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
        addr="10.68.45.139", username="ute", password="ute"
    ),
    network_interface_address="3.7.255.254",
    iperf_path="/usr/bin/iperf",
)

_qualcomm = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.24.165", username="ute", password="ute"
    ),
    # serial_number='35ca1930',
    serial_number="L8K5T19801001123",  # huawei mate20x
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
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[3],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=None)

# 5GRU for classicalBTS
_attenuator = TopYoung(
    ip_addr="10.57.249.x", port=23, attenuation_port_numbers=[9, 10, 11, 12]
)
_ru_pdu = APC(addr="127.0.0.1", port_numbers=[3])

_ru = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.34", username="user", password="pass"
    ),
    lmp_connection=SshServiceDetails(addr="1.1.1.1", username="user", password="pass"),
    pdu_port=_ru_pdu.pdu_ports[3],
    radio_type=RadioTypes.AWHQE,
    attenuation_ports=[
        _attenuator.attenuator_ports[9],
        _attenuator.attenuator_ports[10],
        _attenuator.attenuator_ports[11],
        _attenuator.attenuator_ports[12],
    ],
)

# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")

_gnb_pdu = APC(addr="10.71.24.240", port_numbers=[7])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[7],
)

_airscale = Airscale(common_units=[_common_unit_0])

# _du = DU(airscale=_airscale, rus=[_ru], f1_m_ip_addr='10.71.24.65')
_du = DU(airscale=_airscale, rus=[_ru], f1_m_ip_addr="192.168.255.129")

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
_tl_cloud_topology = "CLASSICAL_5G"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=43, global_bts_id=1)

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    core=_epc_sim,
    enbs=[_lte_real_enb],
    ues=[_qualcomm],
    tl_cloud_topology=_tl_cloud_topology,
    attenuator=_attenuator,
)
