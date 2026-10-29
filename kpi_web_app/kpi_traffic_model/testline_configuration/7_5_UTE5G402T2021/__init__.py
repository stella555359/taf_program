__maintainer__ = "Chen Jian"
__team__ = (
    "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_05_GMS <I_NSB_MN_5GSC_MMW_SC_PZ_HZ_05@internal.nsn.com>"
)
__email__ = "jian.1.chen@nokia.com"

import os
import shutil

from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline import DU, RU, RealEnb
from taf.config.testline.pdu import ATEN, PduPort, FPFH
from taf.config.testline.gnb import ClassicalBts, CU
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.core import RealCore, PCF
from taf.config.testline.testline import TestLine
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)
from taf.config.testline.ue import TafUeAndroid
from taf.config.testline.attenuator import HBTE as AHBTE
from taf.config.testline.pdu import Gude, HBTE, TopYoung, FPFH
from collections import OrderedDict
from taf.config.testline.appserver import TafUeAppServer
from taf.config.testline import TafUeDataTransferProtocol
from taf.config.testline.pdn import PDNTafUeAndroidDetails
from taf.config.testline import NetworkAddress, RoutingInformation

os.environ["INIT_CONFIG_FILE_PATH"] = os.path.dirname(os.path.abspath(__file__))

__all__ = ["tl"]

os.environ["ABSTRACT_LIB_CONFIG"] = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "ue_config.yaml"
)

# Test VM
_test_vm = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.195.46", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)


_du0_pdu = HBTE(addr="10.71.195.48", port_numbers=[1,3])

_common_unit_0_pdu_port = PduPort(pdu=_du0_pdu, port_no="1")

_du0_capacity_unit_L_0 = CapacityUnit(addr="192.168.253.20")

_du0_master_capacity_unit_L_0 = CapacityUnit(addr="fsp-1-1a")

_du0_slave_capacity_unit_L_0 = CapacityUnit(addr="fsp-1-1b")

_du0_fpga_capacity_unit_L_0 = CapacityUnit(addr="fsp-1-1c")

_du0_capacity_unit_L_1 = CapacityUnit(addr="192.168.253.24")

_du0_master_capacity_unit_L_1 = CapacityUnit(addr="fsp-1-2a")

_du0_slave_capacity_unit_L_1 = CapacityUnit(addr="fsp-1-2b")

_du0_fpga_capacity_unit_L_1 = CapacityUnit(addr="fsp-1-2c")

_du0_capacity_unit_L_2 = CapacityUnit(addr="192.168.253.28")

_du0_master_capacity_unit_L_2 = CapacityUnit(addr="fsp-1-3a")

_du0_slave_capacity_unit_L_2 = CapacityUnit(addr="fsp-1-3b")

_du0_fpga_capacity_unit_L_2 = CapacityUnit(addr="fsp-1-3c")

# appserver
_app_server_1 = TafUeAppServer(
    app_server_name="APP_SG5",
    address="10.57.191.249",
    user="vrf3_sg5",
    password="vrf3@sg5",
    ports=[45022],
)

_data_transfer_iperf = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_app_server_1,
    interval=1,
    server_close_delay=50,
)


_pdn1 = PDNTafUeAndroidDetails(
    entryName="dxdata2", apnName="dxdata2", apnType=["DEFAULT"]
)

_android = TafUeAndroid(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.217.9", username="mn5gran", password="nokia123@"
    ),
    ue_pc_address="10.71.217.9",
    proxy_mngr_port="9955",
    serial_number="5730bd24",  # f1318050
    data_transfer=[_data_transfer_iperf],
    pdns=[_pdn1],
    capabilities=["REAL_UE", "qualcomm"],
)

# ru
_ru_pdu1 = TopYoung(addr="10.71.195.50", port_numbers=[1,4])
_ru_pdu2 = TopYoung(addr="10.71.195.49", port_numbers=[1])
_ru0 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.8.2", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru_pdu1.pdu_ports[1],
    radio_type=RadioTypes.AEHC,
    serial_number="K9221730265",
    positioner="1",
)

_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.8.2", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru_pdu1.pdu_ports[4],
    radio_type=RadioTypes.AEHC,
    serial_number="L1205002766",
    positioner="1",
)

_ru2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.8.2", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru_pdu2.pdu_ports[1],
    radio_type=RadioTypes.AVQD,
    serial_number="1M251902125",
    positioner="1",
)

_common_unit_0_L = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.71.208.162", username="toor4nsn", password="oZPS0POrRieRtu"
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
        _du0_capacity_unit_L_2,
        _du0_master_capacity_unit_L_2,
        _du0_slave_capacity_unit_L_2,
        _du0_fpga_capacity_unit_L_2,
    ],
    pdu_port=_du0_pdu.pdu_ports[1],
)

_airscale = Airscale(common_units=[_common_unit_0_L])

_du = DU(
    airscale=_airscale,
    rus=[_ru0, _ru1],
    f1_m_ip_addr="10.71.208.162",
)

_cu = CU(
    backhaul_site_oam_ip="10.71.208.162",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.208.162", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.208.162", username="Nemuadmin", password="nemuuser", port=443
    ),
)

_cbts = ClassicalBts(cu=_cu, dus=[_du], instance_id=2021, global_bts_id=11373)

# Enb (SA not use)
_common_unit_1 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.71.208.98", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_du0_pdu.pdu_ports[1],
)

_real_enb = Airscale(common_units=[_common_unit_1])

_lte_real_enb = RealEnb(
    system_module=_real_enb, rms=[_ru1], oam_ip = NetworkAddress("10.71.208.162"), instance_id=2021, global_bts_id=11372
)

# RealCore
_pcf = PCF(
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.217.23", username="feat1", password="Nokia@123"
    )
)
_realcore = RealCore(pcf=_pcf)

_tl_cloud_topology = "CLOUD_5G_CLASSICAL_MINI_ASIBL_ABIO1_AEUD"

_gnb_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.71.208.162", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    connections=[_du],
)


_attenuator = AHBTE(
    ip_addr="10.101.51.50",
    port=5000,
    attenuation_port_numbers=[1, 2, 3, 4],
    model="PA-16-16-6-127-0.5-B-S",
)

tl = TestLine(
    test_pc=_test_vm,
    gnbs=[_cbts],
    tl_cloud_topology=_tl_cloud_topology,
    core=_realcore,
    enbs=[_lte_real_enb],
    ues=[_android],
    test_pcs=[_gnb_test_pc],
    attenuator=_attenuator,
)

