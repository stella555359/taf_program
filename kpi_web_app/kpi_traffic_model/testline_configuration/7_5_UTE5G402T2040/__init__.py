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
from taf.config.testline.testpc import TestPc, Connection
from taf.config.testline import DU, RU, RealEnb
from taf.config.testline.pdu import ATEN, PduPort
from taf.config.testline.gnb import ClassicalBts, CU
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.core import RealCore5G, PCF
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb.networkaddress import NetworkAddress  # add in taf.meta 5.4
from taf.config.testline.gnb.du import Cablink, Endpoint
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

os.environ["INIT_CONFIG_FILE_PATH"] = os.path.dirname(os.path.abspath(__file__))

__all__ = ["tl"]

os.environ["ABSTRACT_LIB_CONFIG"] = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "ue_config.yaml"
)

# Enb (SA not use)
#_common_unit_1 = CommonUnit(
#    lmp_connection=SshServiceDetails(
#        addr="10.71.208.98", username="toor4nsn", password="oZPS0POrRieRtu"
#    ),
#    capacity_units=[],
#)
#
#_real_enb = Airscale(common_units=[_common_unit_1])
#
#_lte_real_enb = RealEnb(
#    airscale=_real_enb, rms=None, instance_id=2040, global_bts_id=11047
#)


_attenuator = AHBTE(
    ip_addr="10.57.230.211",
    port=5000,
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
)

# ru
_ru0_pdu = FPFH(addr="10.57.251.244", port_numbers=[3])
_ru0 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.8.2", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru0_pdu.pdu_ports[3],
    radio_type=RadioTypes.AHFII.value,
#    radio_type="AHFII",
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[14],
        _attenuator.attenuator_ports[15],
    ],

)
_ru1_pdu = FPFH(addr="10.57.251.244", port_numbers=[2])
_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.8.2", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru1_pdu.pdu_ports[2],
    radio_type=RadioTypes.AHLOA.value,
#    radio_type="AHLOA",
    attenuation_ports=[
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
        _attenuator.attenuator_ports[13],
        _attenuator.attenuator_ports[16],
    ],

)
_ru2_pdu = FPFH(addr="10.57.251.244", port_numbers=[4])
_ru2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.8.2", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru2_pdu.pdu_ports[4],
    radio_type=RadioTypes.AEHC.value,
#    radio_type="AEHC",
    attenuation_ports=[
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[6],
        _attenuator.attenuator_ports[7],
        _attenuator.attenuator_ports[8],
    ],

)
_ru3_pdu = HBTE(addr="10.57.251.232", port_numbers=[5,6])
_ru3 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.8.2", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru3_pdu.pdu_ports[5],
    radio_type=RadioTypes.AQQQA.value,
#    radio_type="AQQQA",
    attenuation_ports=[
        _attenuator.attenuator_ports[9],
        _attenuator.attenuator_ports[10],
        _attenuator.attenuator_ports[11],
        _attenuator.attenuator_ports[12],
    ],
)

#bbmod
_du0_capacity_unit_L_0 = CapacityUnit(
    addr="192.168.253.20",
    hardware_type="ABIL",
    rus=[_ru1],
)

_du0_master_capacity_unit_L_0 = CapacityUnit(addr="fsp-1-1a")

_du0_slave_capacity_unit_L_0 = CapacityUnit(addr="fsp-1-1b")

_du0_fpga_capacity_unit_L_0 = CapacityUnit(addr="fsp-1-1c")

_du0_capacity_unit_L_1 = CapacityUnit(
    addr="192.168.253.24",
    hardware_type="ABIL",
)

_du0_master_capacity_unit_L_1 = CapacityUnit(addr="fsp-1-2a")

_du0_slave_capacity_unit_L_1 = CapacityUnit(addr="fsp-1-2b")

_du0_fpga_capacity_unit_L_1 = CapacityUnit(addr="fsp-1-2c")

_du0_capacity_unit_L_2 = CapacityUnit(
    addr="192.168.253.28",
    hardware_type="ABIO",
    rus=[_ru0],
)

_du0_master_capacity_unit_L_2 = CapacityUnit(addr="fsp-1-3a")

_du0_slave_capacity_unit_L_2 = CapacityUnit(addr="fsp-1-3b")

_du0_fpga_capacity_unit_L_2 = CapacityUnit(addr="fsp-1-3c")

_du0_capacity_unit_R_0 = CapacityUnit(
    addr="192.168.253.36",
    hardware_type="ABIP",
    rus=[_ru2],
)

_du0_master_capacity_unit_R_0 = CapacityUnit(addr="fsp-1-5a")

_du0_slave_capacity_unit_R_0 = CapacityUnit(addr="fsp-1-5b")

_du0_fpga_capacity_unit_R_0 = CapacityUnit(addr="fsp-1-5c")

_du0_capacity_unit_R_1 = CapacityUnit(
    addr="192.168.253.40",
    hardware_type="ABIP",
    rus=[_ru3],
)

_du0_master_capacity_unit_R_1 = CapacityUnit(addr="fsp-1-6a")

_du0_slave_capacity_unit_R_1 = CapacityUnit(addr="fsp-1-6b")

_du0_fpga_capacity_unit_R_1 = CapacityUnit(addr="fsp-1-6c")

_du0_capacity_unit_R_2 = CapacityUnit(addr="192.168.253.44")

_du0_master_capacity_unit_R_2 = CapacityUnit(addr="fsp-1-7a")

_du0_slave_capacity_unit_R_2 = CapacityUnit(addr="fsp-1-7b")

_du0_fpga_capacity_unit_R_2 = CapacityUnit(addr="fsp-1-7c")

_gnb_ru_cablinks = [
    Cablink(source=Endpoint(unit=_du0_capacity_unit_L_0, label='SFP', port_id=1),target=Endpoint(unit=_ru1, label='SFP', port_id=2)),
    Cablink(source=Endpoint(unit=_du0_capacity_unit_L_2, label='SFP', port_id=1),target=Endpoint(unit=_ru0, label='SFP', port_id=2)),
    Cablink(source=Endpoint(unit=_du0_capacity_unit_R_0, label='SFP', port_id=1),target=Endpoint(unit=_ru2, label='SFP', port_id=1)),
    Cablink(source=Endpoint(unit=_du0_capacity_unit_R_0, label='SFP', port_id=7),target=Endpoint(unit=_ru2, label='SFP', port_id=2)),
    Cablink(source=Endpoint(unit=_du0_capacity_unit_R_1, label='SFP', port_id=1),target=Endpoint(unit=_ru3, label='SFP', port_id=1)),
    Cablink(source=Endpoint(unit=_du0_capacity_unit_R_1, label='SFP', port_id=7),target=Endpoint(unit=_ru3, label='SFP', port_id=2)),
]

_du0_pdu = HBTE(addr="10.57.251.231", port_numbers=[7,8])

_common_unit_L_master = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[
        _du0_capacity_unit_L_0,
        _du0_capacity_unit_L_1,
        _du0_capacity_unit_L_2,
    ],
    pdu_port=_du0_pdu.pdu_ports[8],
    hardware_type="ASIL",
)

_common_unit_R_slave = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.119", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[
        _du0_capacity_unit_R_0,
        _du0_capacity_unit_R_1,
    ],
    pdu_port=_du0_pdu.pdu_ports[7],
    hardware_type="ASIL",
)

_airscale = Airscale(common_units=[_common_unit_L_master,_common_unit_R_slave])

_du = DU(
    airscale=_airscale,
    rus=[_ru0, _ru1,_ru2, _ru3],
    f1_m_ip_addr="10.57.228.131",
    cablinks=_gnb_ru_cablinks,
)


_cu = CU(
    backhaul_site_oam_ip="10.57.228.131",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.228.131", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.228.131", username="Nemuadmin", password="nemuuser", port=443
    ),
)

_cbts = ClassicalBts(cu=_cu, dus=[_du], instance_id=2040, global_bts_id=37148)

_realcore = RealCore5G(mcc=262, mnc=3)


# appserver
_app_server_1 = TafUeAppServer(
    app_server_name="APP_SG5_DXE",
    address="10.57.191.249",
    user="vrf3_sg5",
    password="vrf3@sg5",
    ports=[45040,45840],
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
        addr="10.57.130.87", username="mn5gran", password="nokia123@"
    ),
    serial_number="8bb34476",  # f1318050 bb9c8103
    capabilities=["REAL_UE", "qualcomm"],
    ue_pc_address="10.57.130.87",
    proxy_mngr_port="9955",
    data_transfer=[_data_transfer_iperf],
    pdns=[_pdn1],
)

# Test VM
_test_vm = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.251.78", username="ute", password="uteUTE!"
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_cbts.dus[0].airscale.common_units[0],
            interface_type="lmp",
        )
    ],
)

_test_vm_R = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.251.79", username="ute", password="uteUTE!"
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_cbts.dus[0].airscale.common_units[1],
            interface_type="lmp",
        )
    ],
)


_tl_cloud_topology = "CLOUD_5G_CLASSICAL_FULLRACK_QC_SA_ASILL_ABILB1B2_ABIOB3_AHFII_AHLOA-ASILR_ABIPB4B5_AEHC_AQQQA"


_attenuator = AHBTE(
    ip_addr="10.57.230.211",
    port=5000,
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    model="PA-16-16-6-127-0.5-B-S",
)

tl = TestLine(
    test_pc=_test_vm,
    test_pcs=[_test_vm, _test_vm_R],
    gnbs=[_cbts],
    tl_cloud_topology=_tl_cloud_topology,
    core=_realcore,
    # enbs=[_lte_real_enb],
    ues=[_android],
    attenuator=_attenuator,
)
