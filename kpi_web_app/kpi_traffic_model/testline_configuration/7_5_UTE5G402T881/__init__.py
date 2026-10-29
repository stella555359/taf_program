import os
from taf.config.testline.cloud_hosting import (
    ControlNode,
    NCIR,
    CloudDeployment,
    DeploymentFlavorStack,
    DeploymentNetworkStack,
    DeploymentVnfStack,
)
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.core import EPCSim, LTEEmuCore, PrismaCore
from taf.config.testline import RU, DU, AppServer
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, HBTE
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import Qualcomm, QualcommUeType, Android
from taf.config.testline import Enb, SimEnb, RealEnb, LTEEmuEnb, PrismaEnb, DocomoEnb
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.config.testline.nms import Netact
from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)


__maintainer__ = "lei wang"  # TL owner name

__team__ = "I_MN_5G_RAN_IV4_LINE_HZG_7_IV@internal.nsn.com"  # TL owner's team

__email__ = "lei.24.wang@nokia-sbell.com"  # TL owner's email

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# classical gNB LMP
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.19", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_docker_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.172",
        username="dcapuser",
        password="iW_K#8.ute%A10h0m0ra",
        port=49151,
    )
)
_tce_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.101.60.40",
        username="dcapuser",
        password="dcapadmin!",
        port=49148,
    )
)

##RealEnb
_real_enb_pdu = HBTE(addr="10.57.241.144", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.227.166", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[1],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=None)


# 5GRU for classicalBTS
_ru_1_pdu = HBTE(addr="10.57.241.169", port_numbers=[4])
_ru_1 = RU(
    ru_hw_group="AEHC",
    serial_number="AH242420603",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1",
        username="serviceuser",
        password="7B+6yyInfX0uES/FP60uEyhjZHUxB2MoRWvZqUMW42g=",
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.130.235", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_1_pdu.pdu_ports[4],
    radio_type=RadioTypes.AEHC,
)

_ru_2_pdu = HBTE(addr="10.57.241.169", port_numbers=[5])
_ru_2 = RU(
    ru_hw_group="AZQJ",
    serial_number="1M212127965",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1",
        username="rfsw",
        password="5rfS2qmWC0AiFYvir7k8JekCN8/NklqDK5E6OWXuUVQ=",
    ),
    lmp_connection=SshServiceDetails(
        addr="1.1.1.1", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_2_pdu.pdu_ports[5],
    radio_type=RadioTypes.AZQJ,
)

_ru_3_pdu = HBTE(addr="10.57.241.148", port_numbers=[4])
_ru_3 = RU(
    ru_hw_group="AVQC",
    serial_number="	1M242100007",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1",
        username="serviceuser",
        password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og=",
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.150.176", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_3_pdu.pdu_ports[4],
    radio_type=RadioTypes.AVQC,
)

_ru_4_pdu = HBTE(addr="10.57.241.148", port_numbers=[5])
_ru_4 = RU(
    ru_hw_group="AVQC",
    serial_number="1M241103650",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1",
        username="serviceuser",
        password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og=",
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.130.45", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_4_pdu.pdu_ports[5],
    radio_type=RadioTypes.AVQC,
)

# gNB LMP IP
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

# # abin internal IP
# _capacity_unit = CapacityUnit(addr="192.168.253.20")
_capacity_cpue = CapacityUnit(addr="192.168.253.36")
_capacity_loki = CapacityUnit(addr="192.168.253.37")

# gNB PB
_gnb_pdu = HBTE(addr="10.57.241.144", port_numbers=[3])


_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_cpue, _capacity_loki],
    pdu_port=_gnb_pdu.pdu_ports[3],
)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(
    airscale=_airscale, rus=[_ru_1, _ru_2, _ru_3, _ru_4], f1_m_ip_addr="10.57.227.180"
)

# gNB MPlane IP
_cu = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.227.180", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.227.180", username="Nemuadmin", password="nemuuser"
    ),
)


# cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

# instance_id=MRBTS_ID
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=881, global_bts_id=881)


# CI_Detail_UE_Type='Huawei'
_appserver_ssh = SshServiceDetails(
    addr="10.57.191.238", username="vrf3_sg6", password="vrf3@sg6"
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.238",
    iperf_path="/usr/bin/iperf",
    port=57881,
)
_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.37", username="mn5gran", password="nokia123@"
    ),
    serial_number="QKX4C20428008480",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "honor"],
)

_appserver_ul = SshServiceDetails(
    addr="10.57.162.10", username="cmw_sg7", password="Nokia07!"
)
_iperf_ul = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ul,
    network_interface_address="10.57.162.10",
    iperf_path="/usr/bin/iperf",
    port=58881,
)

_appserver = AppServer(iperf_details=_iperf_ul)
tl = TestLine(
    test_pc=_host,
    test_pcs=[_docker_pc, _tce_pc],
    gnbs=[_classical_bts],
    enbs=[_lte_real_enb],
    tl_cloud_topology=_tl_cloud_topology,
    ues=[_android],
    appserver=_appserver,
)
