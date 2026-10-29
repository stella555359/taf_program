import os
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.core import RealCore
from taf.config.testline.core import EPCSim
from taf.config.testline import RU, DU
from taf.config.testline.pdu import HBTE
from taf.config.testline.pdu import HBTE, TopYoung
from taf.config.testline.testline import TestLine
from taf.config.testline.ue import Android
from taf.config.testline.gnb import CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import (
    AirphoneCloud,
    Airphone,
    Prisma,
    TM500,
    Qualcomm,
    QualcommUeType,
    Android,
)  # added in taf.meta.5.4
from taf.config.testline import RealEnb
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)
from taf.config.testline.attenuator import HBTE as AHBTE
from taf.config.testline import NetworkAddress, RoutingInformation
from taf.config.testline.appserver import AppServer

__maintainer__ = "ying.15.li"
__team__ = (
    "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_03_GMS <I_NSB_MN_5GSC_MMW_SC_PZ_HZ_03@internal.nsn.com>"
)
__email__ = "ying.15.li@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# attenuator
_attenuator = AHBTE(
    ip_addr="10.101.41.37",
    port=5000,
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    model="PA-16-16-6-127-0.5-B-S",
)

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.149", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.149", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_appserver_ssh = SshServiceDetails(
    addr="10.57.173.231", username="vrf3_sg3", password="vrf3@sg3Newnew", port="43389"
)


_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.173.231",
    iperf_path="/usr/bin/iperf",
    port="43389",
    ports=["43381", "43382", "43383", "43384", "43385", "43386", "43387", "43389"],
)

_ue_host_ssh = SshServiceDetails(
    addr="10.101.47.8", username="mn5gran", password="nokia123@"
)

_appserver = AppServer(_iperf)

# CI_Detail_UE_Type='Qualcomm'
_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.101.47.8", username="mn5gran", password="nokia123@"
    ),
    serial_number="68b6779b",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python310/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_UE", "qct_dx50"],
)

_epcsim = EPCSim(
    mme_ip="192.168.4.1",
    mcc=777,
    mnc=44,
    tac=777,
    default_ssh_connection_details=SshServiceDetails(
        addr="10.47.199.241", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    dir_path="/opt/wts/latest",
    cfg_filename="TL101_basic_cfg_realLteEnb.cfg",
    edaemon_port="22222",
    egate_port="20021",
)

# 5GRU for classicalBTS
_ru_pdu = TopYoung(addr="10.101.45.226", port_numbers=[4, 7, 3])

_ru1 = RU(
    ru_hw_group="AZQG",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.56.2", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.56.2", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    pdu_port=_ru_pdu.pdu_ports[4],
    radio_type="AZQG",
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
)


_ru2 = RU(
    ru_hw_group="AZQG",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.56.6", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.56.6", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    pdu_port=_ru_pdu.pdu_ports[7],
    radio_type="AZQG",
    attenuation_ports=[
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[6],
        _attenuator.attenuator_ports[7],
        _attenuator.attenuator_ports[8],
    ],
)


_ru3 = RU(
    ru_hw_group="AZQG",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.56.10", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.56.10", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    pdu_port=_ru_pdu.pdu_ports[3],
    radio_type="AZQG",
    attenuation_ports=[
        _attenuator.attenuator_ports[9],
        _attenuator.attenuator_ports[10],
        _attenuator.attenuator_ports[11],
        _attenuator.attenuator_ports[12],
    ],
)


# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.101.51.139", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(
    addr="192.168.253.20",
    rus=[_ru1, _ru2, _ru3],
    hardware_type="ABIO",
)
_gnb_pdu = TopYoung(addr="10.101.45.228", port_numbers=[5])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    hardware_type="ASIB",
    pdu_port=_gnb_pdu.pdu_ports[5],
)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(
    airscale=_airscale,
    rus=[_ru1, _ru2, _ru3],
    f1_m_ip_addr="10.101.51.139",
)

# CU
_cu = CU(
    backhaul_site_oam_ip="10.101.51.139",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.51.139", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.51.139", username="Nemuadmin", password="nemuuser"
    ),
)


# RealEnb
_lmp_connection_enb = SshServiceDetails(
    addr="10.101.51.137", username="toor4nsn", password="oZPS0POrRieRtu"
)
_enb_pdu = TopYoung(addr="10.101.45.228", port_numbers=[2])
_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection_enb,
    capacity_units=[],
    pdu_port=_enb_pdu.pdu_ports[2],
)
_real_enb = Airscale(common_units=[_common_unit_1])
_lte_real_enb = RealEnb(airscale=_real_enb, instance_id="922")

# cloud_topology
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ASKEY_ASIBR_ABIOB4_3xAZQG"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=10479, global_bts_id=10479)

tl = TestLine(
    test_pc=_test_pc,
	host=[_host],
    gnbs=[_classical_bts],
    enbs=[_lte_real_enb],
    appserver=_appserver,
    ues=[_android],
    core=_epcsim,
    attenuator=_attenuator,
    tl_cloud_topology=_tl_cloud_topology,
)
