__maintainer__ = "Kong xiangli"
__team__ = "MN 5G RAN I&V 4 Pz HZG SG1"
__email__ = "ge.gao@nokia-sbell.com"

import os
import yaml
from taf.config.testline.testline import TestLine
from taf.config.testline.ue import Android
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.testpc import TestPc, Connection
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline import NetworkAddress, RoutingInformation
from taf.config.testline.gnb import ClassicalBts, CU
from taf.config.testline import DU, RU
from taf.config.testline.core import RealCore, RealCore5G
from taf.config.testline import RealEnb
from taf.config.testline.pdu import TopYoung, FACOM
from taf.config.testline.pdu import HBTE as PBHBTE
from taf.config.testline.attenuator import HBTE
from taf.config.testline.radio import (
    RadioTypes,
    RadioModule,
)
from taf.config.testline import LicenseKeeper
from taf.config.testline.pdn import PDN, PDPTypes

# _ue_config = os.environ["ABSTRACT_LIB_CONFIG"] = os.path.join(
#    os.path.dirname(os.path.abspath(__file__)), "ues.yaml"
# )
#
# _pdu1 = ATEN(addr="10.42.61.221", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
#
# _pdu2 = ATEN(addr="10.44.177.39", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
#
# _pdu3 = ATEN(addr="10.42.61.241", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
#
# _pdus = [_pdu1, _pdu2, _pdu3]

# _attenuator1 = TopYoung(
#    ip_addr="10.42.221.124",
#    port=3001,
#    attenuation_port_numbers=range(1, 25),
# )
#
# _attenuator2 = TopYoung(
#    ip_addr="10.42.221.125",
#    port=3001,
#    attenuation_port_numbers=range(1, 13),
# )

# _abil_master = CapacityUnit(addr="192.168.253.20")
# _abil_slave = CapacityUnit(addr="192.168.253.21")
# _abil_loner = CapacityUnit(addr="192.168.253.22")

_ru_1_pdu = PBHBTE(addr="10.68.87.14", port_numbers=[7])
_ru1 = RU(
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="rfsw", password="KRG3dFggxxHw+s0z64U0AR22VyjfnXdHrAVdSv5jpc4="
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="rfsw", password="KRG3dFggxxHw+s0z64U0AR22VyjfnXdHrAVdSv5jpc4="),
    pdu_port=_ru_1_pdu.pdu_ports[7],
    ru_hw_group="hw_group",
    serial_number="EB2209R0659",
    radio_type=RadioTypes.AWHQN.value,
)

_ru_2_pdu = PBHBTE(addr="10.68.87.20", port_numbers=[5])
_ru2 = RU(
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="rfsw", password="KRG3dFggxxHw+s0z64U0AR22VyjfnXdHrAVdSv5jpc4="
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="rfsw", password="KRG3dFggxxHw+s0z64U0AR22VyjfnXdHrAVdSv5jpc4="),
    pdu_port=_ru_2_pdu.pdu_ports[5],
    ru_hw_group="hw_group",
    serial_number="EB2223R0139",
    radio_type=RadioTypes.AWHQX.value,
)

_gnb_pdu1 = PBHBTE(addr="10.68.87.29", port_numbers=[5])
_gnb_pdu2 = PBHBTE(addr="10.68.87.29", port_numbers=[1])

_gnb_1_airscale_cu_capacity_unit_left = CapacityUnit(
    addr="1.1.1.1",
    hardware_type="ABIO",
    rus=[_ru1],
)
_gnb_1_airscale_cu_capacity_unit_right = CapacityUnit(
    addr="1.1.1.1",
    hardware_type="ABIN",
    rus=[_ru2],
)

_common_unit1 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_gnb_1_airscale_cu_capacity_unit_left],
    pdu_port=_gnb_pdu1.pdu_ports[5],
    hardware_type="ASIB",
)

_common_unit2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.119", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_gnb_1_airscale_cu_capacity_unit_right],
    pdu_port=_gnb_pdu2.pdu_ports[1],
    hardware_type="ASIB",
)

_airscale1 = Airscale(common_units=[_common_unit1])

_airscale2 = Airscale(common_units=[_common_unit2])

_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.68.88.19",
        v6=None,
        vlan_id=None,
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.68.88.19", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.68.88.19", username="Nemuadmin", password="nemuuser"
    ),
    f1m=None,
    f1c=None,
    f1u=None,
    x2c=NetworkAddress(
        v4="10.68.88.19",
        v6=None,
        vlan_id=None,
    ),
    x2u=NetworkAddress(
        v4="10.68.88.19",
        v6=None,
        vlan_id=None,
    ),
    s1u=NetworkAddress(
        v4="10.68.88.19",
        v6=None,
        vlan_id=None,
    ),
)


# _du1 = DU(_airscale1, rus=[_ru1])
_du1 = DU(
    airscale=_airscale1,
    rus=[_ru1],
    f1_m_ip_addr="192.168.255.129",
)


_du2 = DU(
    airscale=_airscale2,
    rus=[_ru2],
)

_cbts1 = ClassicalBts(cu=_cu, dus=[_du1], instance_id=10035, global_bts_id=10035)

_cbts2 = ClassicalBts(cu=_cu, dus=[_du2], instance_id=10035, global_bts_id=10035)

_pdns = [
    PDN(PDPTypes.IPV4V6.value, "wap1.nokia.com"),
    PDN(PDPTypes.IPV4V6.value, "wap2.nokia.com"),
]


_core = RealCore(mcc=262, mnc=3, pdns=_pdns)

_attenuator = HBTE(
    ip_addr="10.68.88.39",
    port=5000,
    attenuation_port_numbers=[13, 14, 15, 16],
    model="PA-16-16-6-127-0.5-B-S",
)

_test_pc1 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.251.74", username="ute", password="uteUTE!"
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_cbts1.dus[0].airscale.common_units[0],
            interface_type="lmp",
        )
    ],
    # connections=[_cbts1],_cbts1.dus[0].airscale.common_units[0],
)

_test_pc2 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.251.75", username="ute", password="uteUTE!"
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_cbts2.dus[0].airscale.common_units[0],
            interface_type="lmp",
        )
    ],
    # connections=[_cbts2],
)

_ue_pc_ssh = SshServiceDetails(
    addr="10.101.47.22", username="nokia5G", password="noki@123"
)

_iperf_ue = IperfDataTransferDetails(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.207.142", username="vrf4_sg1", password="vrf4@sg1"
    ),
    network_interface_address="10.71.207.142",
    iperf_path="/usr/bin/iperf",
    port="51100",
)

_licensekeeper = LicenseKeeper(username="HAZ4_SG1", password="HAZ4_SG1")
_android_ue1 = Android(
    ssh_connection_details=_ue_pc_ssh,
    serial_number="6b4544d2",
    server_dir="C:/Program Files (x86)/Spark/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_ue,
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "Guanghetong", "huawei_sigspark"],
    imsi="262032001000310",
    licensekeeper=_licensekeeper,
)

_android_ue2 = Android(
    ssh_connection_details=_ue_pc_ssh,
    serial_number="c3d0clae",
    server_dir="C:/Program Files (x86)/Spark/Bin/Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_ue,
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "Guanghetong", "huawei_sigspark"],
    imsi="262033100007809",
    licensekeeper=_licensekeeper,
)

_tl_cloud_topology = (
    "CLOUD_5G_CLASSICAL_FULLRACK_QC_SA_ASIBL_ABIOB1_AWHQN-ASIBR_ABINB4_AWHQX"
)

tl = TestLine(
    test_pc=_test_pc1,
    test_pcs=[_test_pc1, _test_pc2],
    gnbs=[_cbts1, _cbts2],
    tl_cloud_topology=_tl_cloud_topology,
    # core=RealCore(mcc=262, mnc=3),  # Use RealCore() for Real Core TL
    core=_core,
    # pdus=_pdus,
    ues=[_android_ue1, _android_ue2],
    attenuator=_attenuator,
    # attenuators=[_attenuator1, _attenuator2],
)

__all__ = ["tl"]
