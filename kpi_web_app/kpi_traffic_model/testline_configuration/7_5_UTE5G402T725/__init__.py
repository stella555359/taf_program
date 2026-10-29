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
)
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.ue import (
    AirphoneCloud,
    Airphone,
    Prisma,
    TM500,
    Qualcomm,
    QualcommUeType,
    Android,
)
from taf.config.testline.attenuator import (
    AttenuationPort,
    HBTE,
)  # added in taf.meta 5.4
from taf.config.testline.testpc import TestPc
from taf.config.testline.testpc import Connection
from taf.config.testline.appserver import AppServer
from taf.config.testline.core import EPCSim, LTEEmuCore, PrismaCore
from taf.config.testline import RU, DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC
from taf.config.testline.pdu import HBTE as HBTE_pb
from taf.config.testline.radio import RadioModule, RadioTypes
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import AirphoneCloud, Airphone, Prisma, TM500
from taf.config.testline import Enb, SimEnb, RealEnb, LTEEmuEnb, PrismaEnb, DocomoEnb
from taf.config.testline.switch import DellS4048ONSwitch

# from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.nms import Netact
from taf.config.testline.appserver import AppServer
from taf.config.testline import LicenseKeeper
from taf.config.testline.core import RealCore
from taf.config.testline.gnb.du import Cablink, Endpoint

__maintainer__ = "Wu Pengliang"  # TL owner name
__team__ = "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_04@internal.nsn.com"  # TL owner's team
__email__ = "pengliang.wu@nokia-sbell.com"  # TL owner's email

# common
# __all__ = ["tl"]
_cfg_dir = os.path.dirname(os.path.abspath(__file__))
_licensekeeper = LicenseKeeper(username="HAZ3_SG4_1", password="HAZ3_SG4_1")

_attenuator = HBTE(
    ip_addr="10.57.251.250", port="5000", attenuation_port_numbers=[1, 2, 3, 4]
)

# 5GRU for classicalBTS
_ru_pdu1 = HBTE_pb(addr="10.71.197.104", port_numbers=[8])
_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2",
        username="rfsw",
        password="gSDBExyEbO33komYWL6iPrtSaYc5XimHAGrsJ/K8+AY=",
    ),
    lmp_connection=SshServiceDetails(
        addr="10.70.230.200", username="ute", password="ute"
    ),
    pdu_port=_ru_pdu1.pdu_ports[8],
    radio_type=RadioTypes.AWEUA,
)

_ru_pdu2 = HBTE_pb(addr="10.70.230.200", port_numbers=[1])
_ru2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.142",
        username="rfsw",
        password="gSDBExyEbO33komYWL6iPrtSaYc5XimHAGrsJ/K8+AY=",
    ),
    lmp_connection=SshServiceDetails(
        addr="10.70.230.200", username="ute", password="ute"
    ),
    pdu_port=_ru_pdu2.pdu_ports[1],
    radio_type=RadioTypes.AWEUA,
)

_ru_pdu3 = HBTE_pb(addr="10.68.87.247", port_numbers=[2])
_ru3 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.146",
        username="rfsw",
        password="ckBW1r1CX7VUPHcoHd69to3UwvEVm+cGW1aXDlfr51Y=",
    ),
    lmp_connection=SshServiceDetails(
        addr="10.70.230.200", username="ute", password="ute"
    ),
    pdu_port=_ru_pdu3.pdu_ports[2],
    radio_type=RadioTypes.AWEUA,
)

# _ru_pdu4 = HBTE_pb(addr="10.101.45.44", port_numbers=[1])
# _ru4 = RU(
#     ru_hw_group="hw_group",
#     default_ssh_connection_details=SshServiceDetails(
#         addr="192.168.100.1", username="rfsw", password="ckBW1r1CX7VUPHcoHd69to3UwvEVm+cGW1aXDlfr51Y="
#     ),
#     lmp_connection=SshServiceDetails(
#         addr="10.57.157.161", username="ute", password="ute"
#     ),
#     pdu_port=_ru_pdu4.pdu_ports[1],
#     radio_type=RadioTypes.AWHQF,
# )
#
# _ru_pdu5 = HBTE_pb(addr="10.68.87.248", port_numbers=[1])
# _ru5 = RU(
#     ru_hw_group="hw_group",
#     default_ssh_connection_details=SshServiceDetails(
#         addr="192.168.100.1", username="rfsw", password="ckBW1r1CX7VUPHcoHd69to3UwvEVm+cGW1aXDlfr51Y="
#     ),
#     lmp_connection=SshServiceDetails(
#         addr="10.57.157.161", username="ute", password="ute"
#     ),
#     pdu_port=_ru_pdu5.pdu_ports[1],
#     radio_type=RadioTypes.AWHQF,
# )

##DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.68.88.68", username="toor4nsn", password="oZPS0POrRieRtu"
)
# _capacity_unit1 = CapacityUnit(addr="192.168.253.22", hardware_type="ABIL")
# _capacity_unit2 = CapacityUnit(addr="192.168.253.26", hardware_type="ABIL")
# _capacity_unit3 = CapacityUnit(addr="192.168.253.30", hardware_type="ABIL")
_gnb_pdu = HBTE_pb(addr="10.71.197.101", port_numbers=[3])
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    # capacity_units=[_capacity_unit1, _capacity_unit2, _capacity_unit3],
    capacity_units=[],
    pdu_port=_gnb_pdu.pdu_ports[3],
    hardware_type="ASOF",
)
_airscale = Airscale(common_units=[_common_unit_0])

# _ru_cablinks = [
#     Cablink(source=Endpoint(unit=_capacity_unit0, label='SFP', port_id=1), target=Endpoint(unit=_ru1, label='SFP', port_id=1)),
#     Cablink(source=Endpoint(unit=_capacity_unit0, label='QSFP', port_id=1), target=Endpoint(unit=_ru1, label='SFP', port_id=2)),
#     Cablink(source=Endpoint(unit=_capacity_unit0, label='SFP', port_id=2), target=Endpoint(unit=_ru2, label='SFP', port_id=1)),
#     Cablink(source=Endpoint(unit=_capacity_unit1, label='QSFP', port_id=2), target=Endpoint(unit=_ru2, label='SFP', port_id=2)),
#     Cablink(source=Endpoint(unit=_capacity_unit2, label='SFP', port_id=1), target=Endpoint(unit=_ru3, label='SFP', port_id=1)),
# ]

# _du = DU(airscale=_airscale, rus=[_ru1, _ru2, _ru3], f1_m_ip_addr="10.71.215.244", cablinks=_ru_cablinks)

_du = DU(airscale=_airscale, rus=[_ru1, _ru2, _ru3], f1_m_ip_addr="10.68.88.68")

##CU
_cu = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.68.88.68",
        username="toor4nsn",
        password="oZPS0POrRieRtu",
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.68.88.68",
        username="Nemuadmin",
        password="nemuuser",
    ),
)

# RealEnb
_lmp_connection_enb = SshServiceDetails(
    addr="10.71.216.136", username="toor4nsn", password="oZPS0POrRieRtu"
)

_lmp_connection_enb_1 = SshServiceDetails(
    addr="10.71.215.243", username="toor4nsn", password="oZPS0POrRieRtu"
)

_lmp_connection_enb_2 = SshServiceDetails(
    addr="10.71.215.246", username="toor4nsn", password="oZPS0POrRieRtu"
)
# ENB1
_enb_pdu = HBTE_pb(addr="10.101.45.42", port_numbers=[6])
_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection_enb,
    capacity_units=[],
    pdu_port=_enb_pdu.pdu_ports[6],
)
_real_enb = Airscale(common_units=[_common_unit_1])
_lte_real_enb = RealEnb(airscale=_real_enb, instance_id=716, global_bts_id=716)

# ENB2
_enb_pdu_1 = HBTE_pb(addr="10.101.45.42", port_numbers=[6])
_common_unit_2 = CommonUnit(
    lmp_connection=_lmp_connection_enb_1,
    capacity_units=[],
    pdu_port=_enb_pdu_1.pdu_ports[6],
)
_real_enb_1 = Airscale(common_units=[_common_unit_2])
_lte_real_enb_1 = RealEnb(airscale=_real_enb_1, instance_id=10725, global_bts_id=10725)

# ENB3
_enb_pdu_2 = HBTE_pb(addr="10.101.45.42", port_numbers=[6])
_common_unit_3 = CommonUnit(
    lmp_connection=_lmp_connection_enb_2,
    capacity_units=[],
    pdu_port=_enb_pdu_2.pdu_ports[6],
)
_real_enb_2 = Airscale(common_units=[_common_unit_3])
_lte_real_enb_2 = RealEnb(airscale=_real_enb_2, instance_id=5531, global_bts_id=5531)

## switch Dtor
_dell_s4048on_ssh = SshServiceDetails(
    addr="10.101.63.81", port="1/22", username="5gran", password="nokia123"
)
_dell_s4048on_switch = DellS4048ONSwitch(_dell_s4048on_ssh)

##cloud_topology
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ANDROID_ASOF_3xAWEUA"
# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=37289, global_bts_id=37289)
_netact = Netact("10.107.178.214")

# #######Iperf########
_appserver_ssh = SshServiceDetails(
    addr="10.57.191.197", username="vrf3_sg4", password="vrf3@sg4", port="44311"
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.197",
    iperf_path="/usr/bin/iperf",
    port="44311",
    ports=[44311, 44312, 44313, 44314, 44315, 44316, 44317],
)
_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.197",
    iperf_path="/usr/bin/iperf",
    port="44534",
    ports=[44534, 44535, 44536, 44537, 44538, 44539],
)
_appserver = AppServer(_iperf_details_on_appserver)

# S20 AWEUA23
_android_0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.68.86.142", username="mn5gran", password="nokia123@"
    ),
    serial_number="MTK_M90_003",
    server_dir="C:/Program Files (x86)/Spark1.1.1997.1/Bin/Spark.exe",
    python_path="C:/Program Files/Python39",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033100010067",
    capabilities=["REAL_ANDROID_UE", "samsung", "huawei_sigspark"],
    licensekeeper=_licensekeeper,
)

# gNB VM
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.70.230.200", username="ute", password="ute"
    ),
    # connections=[_classical_bts],
    connections=[
        Connection(
            interface="eth1",
            device=_classical_bts.dus[0].airscale.common_units[0],
            interface_type="lmp",
        )
    ],
)

tl = TestLine(
    test_pc=_host,
    test_pcs=[_host],
    gnbs=[_classical_bts],
    # enbs=[_lte_real_enb],
    core=RealCore(mcc=262, mnc=3),
    tl_cloud_topology=_tl_cloud_topology,
    nms=_netact,
    switches=[_dell_s4048on_switch],
    # attenuator=_attenuator,
    appserver=_appserver,
    ues=[_android_0],
)
# tl = TestlineWrapper(tl)
__all__ = ["tl"]
