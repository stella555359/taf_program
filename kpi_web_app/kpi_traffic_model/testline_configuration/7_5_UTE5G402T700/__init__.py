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

__maintainer__ = "Zhu Xiaofeng"  # TL owner name
__team__ = "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_04@internal.nsn.com"  # TL owner's team
__email__ = "xiaofeng.1.zhu@nokia-sbell.com"  # TL owner's email

# common
# __all__ = ["tl"]
_cfg_dir = os.path.dirname(os.path.abspath(__file__))
_licensekeeper = LicenseKeeper(username="HAZ3_SG4_1", password="HAZ3_SG4_1")

_attenuator = HBTE(
    ip_addr="10.57.251.250", port="5000", attenuation_port_numbers=[1, 2, 3, 4]
)

# 5GRU for classicalBTS
_ru_pdu1 = HBTE_pb(addr="10.101.45.46", port_numbers=[6])
_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="1.1.1.1", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu1.pdu_ports[6],
    radio_type=RadioTypes.AWHHF,
)

_ru_pdu2 = HBTE_pb(addr="10.101.45.44", port_numbers=[1])
_ru2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="serviceuser", password="oBrd1RgbOasUtYAeVfxrW9yGHb6ONl0w+MJUoKrBMGE="
    ),
    lmp_connection=SshServiceDetails(
        addr="1.1.1.1", username="serviceuser", password="oBrd1RgbOasUtYAeVfxrW9yGHb6ONl0w+MJUoKrBMGE="
    ),
    pdu_port=_ru_pdu2.pdu_ports[1],
    radio_type=RadioTypes.AWHHF,
)

_ru_pdu3 = HBTE_pb(addr="10.101.45.44", port_numbers=[3])
_ru3 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="rfsw", password="KRG3dFggxxHw+s0z64U0AR22VyjfnXdHrAVdSv5jpc4="
    ),
    lmp_connection=SshServiceDetails(
        addr="1.1.1.1", username="rfsw", password="KRG3dFggxxHw+s0z64U0AR22VyjfnXdHrAVdSv5jpc4="
    ),
    pdu_port=_ru_pdu3.pdu_ports[3],
    radio_type=RadioTypes.AWHHD,
)

_ru_pdu4 = HBTE_pb(addr="10.101.45.57", port_numbers=[5])
_ru4 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="rfsw", password="ckBW1r1CX7VUPHcoHd69to3UwvEVm+cGW1aXDlfr51Y="
    ),
    lmp_connection=SshServiceDetails(
        addr="1.1.1.1", username="ute", password="ute"
    ),
    pdu_port=_ru_pdu4.pdu_ports[5],
    radio_type=RadioTypes.AWHHJ,
)

##DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit1 = CapacityUnit(addr="192.168.253.36", hardware_type="ABIL")
_capacity_unit2 = CapacityUnit(addr="192.168.253.40", hardware_type="ABIL")
_capacity_unit3 = CapacityUnit(addr="192.168.253.44", hardware_type="ABIL")

_gnb_pdu = HBTE_pb(addr="10.101.45.48", port_numbers=[2])
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit1, _capacity_unit2, _capacity_unit3],
    pdu_port=_gnb_pdu.pdu_ports[2],
    hardware_type="ASIK"
)
_airscale = Airscale(common_units=[_common_unit_0])

_ru_cablinks = [
    Cablink(source=Endpoint(unit=_capacity_unit1, label='SFP', port_id=2), target=Endpoint(unit=_ru1, label='SFP', port_id=2)),
    Cablink(source=Endpoint(unit=_capacity_unit1, label='QSFP', port_id=2), target=Endpoint(unit=_ru1, label='SFP', port_id=3)),
    Cablink(source=Endpoint(unit=_capacity_unit1, label='SFP', port_id=1), target=Endpoint(unit=_ru2, label='SFP', port_id=2)),
    Cablink(source=Endpoint(unit=_capacity_unit1, label='QSFP', port_id=1), target=Endpoint(unit=_ru2, label='SFP', port_id=3)),
    Cablink(source=Endpoint(unit=_capacity_unit2, label='SFP', port_id=1), target=Endpoint(unit=_ru3, label='SFP', port_id=1)),
    Cablink(source=Endpoint(unit=_capacity_unit3, label='SFP', port_id=1), target=Endpoint(unit=_ru4, label='SFP', port_id=1)),
]

_du = DU(airscale=_airscale, rus=[_ru1, _ru2, _ru3, _ru4], f1_m_ip_addr="10.101.49.75", cablinks=_ru_cablinks)

##CU
_cu = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.49.75",
        username="toor4nsn",
        password="oZPS0POrRieRtu",
        port="22",
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.49.75",
        username="Nemuadmin",
        password="nemuuser",
    ),
)

# RealEnb
# _lmp_connection_enb = SshServiceDetails(
#     addr="10.101.49.41", username="toor4nsn", password="oZPS0POrRieRtu"
# )
# _enb_pdu = HBTE_pb(addr="10.101.45.42", port_numbers=[6])
# _common_unit_1 = CommonUnit(
#     lmp_connection=_lmp_connection_enb,
#     capacity_units=[],
#     pdu_port=_enb_pdu.pdu_ports[6],
# )
# _real_enb = Airscale(common_units=[_common_unit_1])
# _lte_real_enb = RealEnb(airscale=_real_enb, instance_id=5531, global_bts_id=5531)

## switch Dtor
_dell_s4048on_ssh = SshServiceDetails(
    addr="10.101.49.75", port="45", username="5gran", password="nokia123"
)
_dell_s4048on_switch = DellS4048ONSwitch(_dell_s4048on_ssh)

##cloud_topology
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ANDROID_SA_ASIBL_ABILB1_2xAWHHF"
# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id="700", global_bts_id="700")
# _netact = Netact("10.107.178.214")

# #######Iperf########
_appserver_ssh = SshServiceDetails(
    addr="10.57.178.18", username="mmw_sg4", password="mm@4", port="44001"
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.178.18",
    iperf_path="/usr/bin/iperf",
    port="44311",
    ports=[44311, 44312, 44313, 44314, 44315, 44316, 44317],
)
_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.178.18",
    iperf_path="/usr/bin/iperf",
    port="44001",
    ports=[44311, 44312, 44313, 44314, 44315, 44316, 44317],
)
_appserver = AppServer(_iperf_details_on_appserver)

# note20
_android_0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.101.47.2", username="nokia5G", password="noki@123"
    ),
    serial_number="R5CR30FF09M",
    server_dir="C:/Program Files (x86)/Spark1.1.1997.1/Bin/Spark.exe",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf_details_on_appserver,
    imsi="440503100001185",
    capabilities=["REAL_ANDROID_UE", "samsung", "huawei_sigspark"],
    licensekeeper=_licensekeeper,
)

# s21
_android_1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.101.47.97", username="nokia5G", password="noki@123"
    ),
    serial_number="RFCR10M3XAD",
    server_dir="C:/Program Files (x86)/Spark1.1.1997.1/Bin/Spark.exe",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033032996917",
    capabilities=["REAL_ANDROID_UE", "samsung", "huawei_sigspark"],
    licensekeeper=_licensekeeper,
)

#gNB VM
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(addr="10.57.251.53", username="ute", password="uteUTE!"),
    # connections=[_classical_bts],
    connections=[Connection(interface="eth1", device=_classical_bts.dus[0].airscale.common_units[0], interface_type="lmp")],
)

tl = TestLine(
    test_pc=_host,
    test_pcs=[_host],
    gnbs=[_classical_bts],
    # enbs=[_lte_real_enb],
    core=RealCore(mcc=262, mnc=3),
    tl_cloud_topology=_tl_cloud_topology,
    # nms=_netact,
    switches=[_dell_s4048on_switch],
    # attenuator=_attenuator,
    appserver=_appserver,
    # ues=[_android_0, _android_1],
)
# tl = TestlineWrapper(tl)
__all__ = ["tl"]
