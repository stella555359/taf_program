__maintainer__ = "chenjian"
__team__ = (
    "i_nsb_mn_5gsc_mmw_sc_pz_hz_05@internal.nsn.com"
)
__email__ = "jian.1.chen@nokia-sbell.com"

import os
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline import DU, RU, RealEnb
from taf.config.testline.pdu import ATEN, HBTE, TopYoung, PduPort
from taf.config.testline.gnb import ClassicalBts, CU
from taf.config.testline.gnb.du import Cablink, Endpoint
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
from taf.config.testline import NetworkAddress, RoutingInformation
from taf.config.testline.attenuator import HBTE as AHBTE
from taf.config.testline.attenuator import TopYoung as ATopYoung
from collections import OrderedDict
from taf.config.testline.appserver import TafUeAppServer
from taf.config.testline import TafUeDataTransferProtocol
from taf.config.testline.pdn import PDNTafUeAndroidDetails

os.environ["INIT_CONFIG_FILE_PATH"] = os.path.dirname(os.path.abspath(__file__))
__all__ = ["tl"]
os.environ["ABSTRACT_LIB_CONFIG"] = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "ue_config.yaml"
)

# RealCore
_pcf = PCF(
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.217.23", username="feat1", password="Nokia@123"
    )
)
_realcore = RealCore(pcf=_pcf)


# Enb
_common_unit_1 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.233.210", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
)
_real_enb = Airscale(common_units=[_common_unit_1])
_lte_real_enb = RealEnb(
    airscale=_real_enb, rms=None, instance_id=2028, global_bts_id=11087
)

# Test PC
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.177.114", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# ru
_ru0_pdu = TopYoung(addr="10.57.251.241", port_numbers=[5])
_ru0 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.8.2", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru0_pdu.pdu_ports[5],
    radio_type=RadioTypes.AHFII,
)
_ru1_pdu = TopYoung(addr="10.57.251.241", port_numbers=[2])
_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.8.2", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru1_pdu.pdu_ports[2],
    radio_type=RadioTypes.AHLOA,
)
_ru2_pdu = TopYoung(addr="10.57.251.241", port_numbers=[6])
_ru2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.8.2", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru2_pdu.pdu_ports[6],
    radio_type=RadioTypes.AEHC,
)
_ru3_pdu = TopYoung(addr="10.57.251.241", port_numbers=[1])
_ru3 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.8.2", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru3_pdu.pdu_ports[1],
    radio_type=RadioTypes.AEQV,
)

# du
_capacity_unit = CapacityUnit(addr="192.168.255.129")
_du0_pdu = TopYoung(addr="10.57.251.241", port_numbers=[3])
_common_unit_0_pdu_port = PduPort(pdu=_du0_pdu, port_no="3")
_common_unit_0 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_capacity_unit],
    pdu_port=_common_unit_0_pdu_port,
)
_airscale = Airscale(common_units=[_common_unit_0])
_capacity_unit = CapacityUnit(addr="192.168.255.129")
_ru_cablinks = [
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=1),
        target=Endpoint(unit=_ru0, label="SFP", port_id=1),
    )
]
_du = DU(
    airscale=_airscale, rus=[_ru0, _ru1, _ru2, _ru3], f1_m_ip_addr="10.57.228.130", cablinks=_ru_cablinks
)

# cu
_cu = CU(
    backhaul_site_oam_ip="10.57.228.130",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.228.130", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.228.130", username="Nemuadmin", password="nemuuser", port=443
    ),
)
_classical_bts = ClassicalBts(
    dus=[_du], cu=_cu, instance_id=2028, global_bts_id=37177
)

# cloud_topology. if ute not migrate to cloud, there is empty
_tl_cloud_topology = "not_cloud"

# default gnb_test_pc
_gnb_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    connections=[_du],
)

# appserver
_app_server_1 = TafUeAppServer(
    app_server_name="APP_SG5_DXE",
    address="10.57.191.249",
    user="vrf3_sg5",
    password="vrf3@sg5",
    ports=[45028,45128,45228],
)

_data_transfer_iperf = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_app_server_1,
    interval=1,
    server_close_delay=50,
)

_pdn1 = PDNTafUeAndroidDetails(
    entryName="wap3.nokia.com", apnName="wap3.nokia.com", apnType=["DEFAULT"]
)

# HETE renamed as AHBTE, TopYoung renamed as ATopYoung
_attenuator = AHBTE(
    ip_addr="10.57.230.210",
    port=23,
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
)

# ue info include control pc, ue serial number, ue type
_android0 = TafUeAndroid(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.199", username="mn5gran", password="nokia123@"
    ),
    serial_number="50c0ffb1",
    capabilities=["REAL_UE", "qualcomm"],
    ue_pc_address="10.57.150.199",
    proxy_mngr_port="9955",
    data_transfer=[_data_transfer_iperf],
    pdns=[_pdn1],
)

# test line configuration information
tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_classical_bts],
    tl_cloud_topology=_tl_cloud_topology,
    core=_realcore,
    enbs=[_lte_real_enb],
    test_pcs=[_gnb_test_pc],
    attenuator=_attenuator,
    ues=[_android0],
)
