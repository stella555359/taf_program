__maintainer__ = "Li Chun"
__team__ = (
    "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_05_GMS <I_NSB_MN_5GSC_MMW_SC_PZ_HZ_05@internal.nsn.com>"
)
__email__ = "chun.li@nokia.com"

import os
import shutil

from taf.config.testline.appserver import AppServer
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc, Connection
from taf.config.testline import DU, RU, RealEnb
from taf.config.testline.pdu import ATEN, PduPort
from taf.config.testline.pdu import TopYoung, FACOM, HBTE
from taf.config.testline.gnb import ClassicalBts, CU
from taf.config.testline.gnb.du import Cablink, Endpoint
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.core import RealCore5G, PCF
from taf.config.testline.testline import TestLine
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)
from taf.config.testline.ue import Android, Qualcomm
from taf.config.testline.attenuator import HBTE as AHBTE

from collections import OrderedDict

os.environ["INIT_CONFIG_FILE_PATH"] = os.path.dirname(os.path.abspath(__file__))

__all__ = ["tl"]

os.environ["ABSTRACT_LIB_CONFIG"] = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "ue_config.yaml"
)

# Enb
_common_unit_1 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.71.216.0", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
)

_real_enb = Airscale(common_units=[_common_unit_1])

_lte_real_enb = RealEnb(
    airscale=_real_enb, rms=None, instance_id=2035, global_bts_id=10669
)


_ru0_pdu = HBTE(addr="10.71.197.130", port_numbers=[5])

_ru0 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52",
        username="rfsw",
        password="PD6N1DB0lWmwomtNL2qd3ISypbiocdGRy7U+Lipiksk=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.21.1.21", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru0_pdu.pdu_ports[5],
    radio_type=RadioTypes.AHFIB,
)

_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52",
        username="rfsw",
        password="PD6N1DB0lWmwomtNL2qd3ISypbiocdGRy7U+Lipiksk=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.21.1.21", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru0_pdu.pdu_ports[5],
    radio_type=RadioTypes.AEUD,
)

_du0_pdu = HBTE(addr="10.71.197.131", port_numbers=[5])

_common_unit_0_pdu_port = PduPort(pdu=_du0_pdu, port_no="5")

_du0_capacity_unit_L_0 = CapacityUnit(addr="192.168.253.20", hardware_type="ABIO")

_du0_master_capacity_unit_L_0 = CapacityUnit(addr="fsp-1-1a", hardware_type="ABIO")

_du0_slave_capacity_unit_L_0 = CapacityUnit(addr="fsp-1-1b", hardware_type="ABIO")

_du0_fpga_capacity_unit_L_0 = CapacityUnit(addr="fsp-1-1c", hardware_type="ABIO")

_du0_capacity_unit_L_1 = CapacityUnit(addr="192.168.253.24", hardware_type="ABIO")

_du0_master_capacity_unit_L_1 = CapacityUnit(addr="fsp-1-2a", hardware_type="ABIO")

_du0_slave_capacity_unit_L_1 = CapacityUnit(addr="fsp-1-2b", hardware_type="ABIO")

_du0_fpga_capacity_unit_L_1 = CapacityUnit(addr="fsp-1-2c", hardware_type="ABIO")

_du0_capacity_unit_L_2 = CapacityUnit(addr="192.168.253.28", hardware_type="ABIO")

_du0_master_capacity_unit_L_2 = CapacityUnit(addr="fsp-1-3a", hardware_type="ABIO")

_du0_slave_capacity_unit_L_2 = CapacityUnit(addr="fsp-1-3b", hardware_type="ABIO")

_du0_fpga_capacity_unit_L_2 = CapacityUnit(addr="fsp-1-3c", hardware_type="ABIO")

_ru_cablinks = [
    Cablink(source=Endpoint(unit=_du0_capacity_unit_L_0, label='SFP', port_id=1), target=Endpoint(unit=_ru0, label='SFP', port_id=1)),
    Cablink(source=Endpoint(unit=_du0_capacity_unit_L_0, label='SFP', port_id=2), target=Endpoint(unit=_ru0, label='SFP', port_id=2)),
    Cablink(source=Endpoint(unit=_du0_capacity_unit_L_1, label='SFP', port_id=1), target=Endpoint(unit=_ru1, label='SFP', port_id=1)),
    Cablink(source=Endpoint(unit=_du0_capacity_unit_L_1, label='SFP', port_id=2), target=Endpoint(unit=_ru1, label='SFP', port_id=2)),
    ]

_appserver_ssh = SshServiceDetails(
    addr="10.71.219.229", username="mmw_sg5", password="mm@5", port="45046"
)
_appserver_ssh2 = SshServiceDetails(
    addr="10.71.219.27", username="mmw_sg5", password="mm@5", port="45045"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.219.229",
    iperf_path="/data/data/com.nokia.syve.uemanager.mobile/iperf",
    port="45046",
)
_iperf2 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh2,
    network_interface_address="10.71.219.27",
    iperf_path="/data/data/com.nokia.syve.uemanager.mobile/iperf",
    port="45045",
)

_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.217.93", username="nokia5G", password="noki@123"
    ),
    serial_number="2e0dd896",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "qct_dx50"],
)

_common_unit_0_L = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[
        _du0_capacity_unit_L_0,
        _du0_master_capacity_unit_L_0,
        _du0_slave_capacity_unit_L_0,
        _du0_fpga_capacity_unit_L_0,
        _du0_capacity_unit_L_1,
        _du0_master_capacity_unit_L_1,
        _du0_slave_capacity_unit_L_1,
        _du0_fpga_capacity_unit_L_1,
    ],
    pdu_port=_common_unit_0_pdu_port,
    hardware_type="ASIL",
)

_airscale = Airscale(common_units=[_common_unit_0_L])

_du = DU(airscale=_airscale, rus=[_ru0, _ru1], f1_m_ip_addr="10.71.216.9", cablinks=_ru_cablinks)

_cu = CU(
    backhaul_site_oam_ip="10.71.216.9",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.216.9", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.216.9", username="Nemuadmin", password="nemuuser", port=443
    ),
)

_cbts = ClassicalBts(cu=_cu, dus=[_du], instance_id=2045, global_bts_id=11230)

# RealCore
#_pcf = PCF(
#    oam_ssh_connection_details=SshServiceDetails(
#        addr="10.71.0.0", username="nokia5G", password="noki@123"
#    )
#)
#_realcore = RealCore(pcf=_pcf)
_realcore = RealCore5G(mcc=262, mnc=3)

_tl_cloud_topology = "CLOUD_5G_CLASSICAL_QC_ASILL_ABIOB1B2_AHFIB_AEUD"

# Test VM
_test_vm = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.70.230.201", username="ute", password="ute"
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_cbts.dus[0].airscale.common_units[0],
            interface_type="lmp",
        )
    ],
)

_gnb_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.101.60.72", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    connections=[],
)

_appserver = AppServer(iperf_details=_iperf)
_appserver2 = AppServer(iperf_details=_iperf2)

_attenuator = AHBTE(
    ip_addr="10.71.207.2",
    port=5000,
    attenuation_port_numbers=[9, 10, 11, 12],
    model="PA-16-16-6-127-0.5-B-S",
)

tl = TestLine(
    test_pc=_test_vm,
    gnbs=[_cbts],
    tl_cloud_topology=_tl_cloud_topology,
    core=_realcore,
#    enbs=[_lte_real_enb],
    ues=[_android],
    test_pcs=[_test_vm],
    appserver=_appserver,
    appservers=[_appserver2],
    attenuator=_attenuator,
)
