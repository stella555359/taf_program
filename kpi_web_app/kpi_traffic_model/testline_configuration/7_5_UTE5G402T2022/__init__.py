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
from taf.config.testline.pdu import ATEN, PduPort
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
    RadioHeadPositioner,
)
from taf.config.testline.ue import TafUeAndroid
from taf.config.testline.attenuator import HBTE as AHBTE
from taf.config.testline.pdu import Gude, HBTE, TopYoung, FPFH
from collections import OrderedDict
from taf.config.testline.appserver import TafUeAppServer
from taf.config.testline import TafUeDataTransferProtocol
from taf.config.testline.pdn import PDNTafUeAndroidDetails

os.environ["INIT_CONFIG_FILE_PATH"] = os.path.dirname(os.path.abspath(__file__))

__all__ = ["tl"]

os.environ["ABSTRACT_LIB_CONFIG"] = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "ue_config.yaml"
)

# Enb (SA not use)
_common_unit_1 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.71.208.98", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
)

_real_enb = Airscale(common_units=[_common_unit_1])

_lte_real_enb = RealEnb(
    airscale=_real_enb, rms=None, instance_id=1835, global_bts_id=10619
)

# Test VM
_test_vm = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.177.54", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)


_du0_pdu = HBTE(addr="10.71.195.42", port_numbers=[5])

_common_unit_0_pdu_port = PduPort(pdu=_du0_pdu, port_no="5")

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

_appserver_ssh = SshServiceDetails(
    addr="10.71.207.149", username="vrf3_sg5", password="vrf3@sg5"
)

# appserver
_app_server_1 = TafUeAppServer(
    app_server_name="APP_SG5_DXB",
    address="10.71.207.149",
    user="vrf3_sg5",
    password="vrf3@sg5",
    ports=[45022,45822],
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
        addr="10.71.217.92", username="mn5gran", password="nokia123@"
    ),
    serial_number="b7f95a4f",  # f1318050
    capabilities=["REAL_UE", "qualcomm"],
    ue_pc_address="10.71.217.92",
    proxy_mngr_port="9955",
    data_transfer=[_data_transfer_iperf],
    pdns=[_pdn1],
)

# ru
_ru0_pdu = TopYoung(addr="10.71.195.38", port_numbers=[6])
_ru0 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="root", password=""
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.8.2", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru0_pdu.pdu_ports[6],
    radio_type=RadioTypes.ARPA,
    serial_number="AS212512441",
    positioner="1",
)
_ru1_pdu = HBTE(addr="10.71.195.40", port_numbers=[3])
_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.33.129", username="root", password=""
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.8.2", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru1_pdu.pdu_ports[3],
    radio_type=RadioTypes.ARPA,
    serial_number="F7201207760",
    positioner="1",
)
_ru2_pdu = HBTE(addr="10.71.195.40", port_numbers=[1])
_ru2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.18", username="rfsw", password="bdS%ztWG3v7%SjreCVA79wTPb"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.8.2", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru2_pdu.pdu_ports[1],
    radio_type=RadioTypes.AEHC,
    serial_number="K9222600546",
    positioner="1",
)
_ru3_pdu = HBTE(addr="10.71.195.44", port_numbers=[3])
_ru3 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.30",
        username="rfsw",
        password="5rfS2qmWC0AiFYvir7k8JekCN8/NklqDK5E6OWXuUVQ=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.8.2", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru3_pdu.pdu_ports[3],
    radio_type=RadioTypes.AZQS,
    serial_number="1M212807079",
    positioner="1",
)
_ru4_pdu = FPFH(addr="10.71.195.46", port_numbers=[4])
_ru4 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.22",
        username="rfsw",
        password="5rfS2qmWC0AiFYvir7k8JekCN8/NklqDK5E6OWXuUVQ=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.8.2", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru4_pdu.pdu_ports[4],
    radio_type=RadioTypes.AZQU,
    serial_number="1M222506791",
    positioner="1",
)
_ru5_pdu = HBTE(addr="10.71.195.44", port_numbers=[4])
_ru5 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.33.128", username="root", password=""
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.8.2", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru5_pdu.pdu_ports[4],
    radio_type=RadioTypes.AHCA,
    serial_number="AS220200116",
    positioner="1",
)
_ru6_pdu = HBTE(addr="10.71.195.44", port_numbers=[1])
_ru6 = RU(
    ru_hw_group="obsai",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.10.128", username="", password=""
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.8.2", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru6_pdu.pdu_ports[1],
    radio_type=RadioTypes.FRIJ,
    serial_number="1M184302277",
    positioner="1",
)

_common_unit_0_L = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.71.208.133", username="toor4nsn", password="oZPS0POrRieRtu"
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
    pdu_port=_common_unit_0_pdu_port,
)

_airscale = Airscale(common_units=[_common_unit_0_L])

_du = DU(
    airscale=_airscale,
    rus=[_ru0, _ru1, _ru2, _ru3, _ru4, _ru5, _ru6],
    f1_m_ip_addr="10.71.208.133",
)

_cu = CU(
    backhaul_site_oam_ip="10.71.208.133",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.208.133", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.208.133", username="Nemuadmin", password="nemuuser", port=443
    ),
)

_cbts = ClassicalBts(cu=_cu, dus=[_du], instance_id=2022, global_bts_id=36916)

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
        addr="10.71.208.133", username="toor4nsn", password="oZPS0POrRieRtu"
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
