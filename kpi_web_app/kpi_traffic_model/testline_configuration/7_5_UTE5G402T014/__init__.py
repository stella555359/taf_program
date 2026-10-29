__maintainer__ = "Kong xiangli"
__team__ = "MN 5G RAN I&V 4 Pz HZG SG1"
__email__ = "Shuhui.lou@nokia-sbell.com"

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
from taf.config.testline.pdu import ATEN
from taf.config.testline.pdu import TopYoung, FACOM, HBTE
from taf.config.testline.radio import RadioTypes
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
_gnb_pdu1 = HBTE(addr="10.71.197.53", port_numbers=[4])
_gnb_pdu2 = HBTE(addr="10.71.197.53", port_numbers=[6])

_gnb_1_airscale_cu_capacity_unit_left = CapacityUnit(
    addr="1.1.1.1", hardware_type="ABIL"
)
_gnb_1_airscale_cu_capacity_unit_right = CapacityUnit(
    addr="1.1.1.1", hardware_type="ABIL"
)

_common_unit1 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_gnb_1_airscale_cu_capacity_unit_left],
    pdu_port=_gnb_pdu1.pdu_ports[4],
    hardware_type="ASIK",
)

_common_unit2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.119", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_gnb_1_airscale_cu_capacity_unit_right],
    pdu_port=_gnb_pdu2.pdu_ports[6],
    hardware_type="ASIK",
)

_airscale1 = Airscale([_common_unit1])

_airscale2 = Airscale([_common_unit2])

_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.71.215.70",
        v6=None,
        vlan_id=None,
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.215.70", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.215.70", username="Nemuadmin", password="nemuuser"
    ),
    f1m=None,
    f1c=None,
    f1u=None,
    x2c=NetworkAddress(
        v4="10.71.215.70",
        v6=None,
        vlan_id=None,
    ),
    x2u=NetworkAddress(
        v4="10.71.215.70",
        v6=None,
        vlan_id=None,
    ),
    s1u=NetworkAddress(
        v4="10.71.215.70",
        v6=None,
        vlan_id=None,
    ),
)

_ru_1_pdu = HBTE(addr="10.71.197.56", port_numbers=[1])
_ru1 = RU(
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(addr="", username=""),
    pdu_port=_ru_1_pdu.pdu_ports[1],
    ru_hw_group="",
    radio_type=RadioTypes.AHPE.value,
)

_ru_2_pdu = HBTE(addr="10.71.197.56", port_numbers=[2])
_ru2 = RU(
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(addr="", username=""),
    pdu_port=_ru_2_pdu.pdu_ports[2],
    ru_hw_group="",
    radio_type=RadioTypes.AEHC.value,
)


_du1 = DU(_airscale1, rus=[_ru1])

_du2 = DU(_airscale2, rus=[_ru2])

_cbts1 = ClassicalBts(cu=_cu, dus=[_du1], instance_id=1914, global_bts_id=14)

_cbts2 = ClassicalBts(cu=_cu, dus=[_du2], instance_id=1914, global_bts_id=14)

# #pdn
_pdns = [
    PDN(PDPTypes.IPV4V6.value, "dxdata2"),
    PDN(PDPTypes.IPV4V6.value, "wap2.nokia.com"),
]

_core = RealCore(mcc=262, mnc=3, pdns=_pdns)

_test_pc1 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.251.77", username="ute", password="ute"
    ),
    #    connections=[_cbts1],
    connections=[
        Connection(
            interface="eth1",
            device=_cbts1.dus[0].airscale.common_units[0],
            interface_type="lmp",
        )
    ],
)

_test_pc2 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.251.76", username="ute", password="ute"
    ),
    #    connections=[_cbts2],
    connections=[
        Connection(
            interface="eth1",
            device=_cbts2.dus[0].airscale.common_units[0],
            interface_type="lmp",
        )
    ],
)

_ue_pc_ssh = SshServiceDetails(
    addr="10.71.218.217", username="mn5gran", password="nokia123@"
)

_iperf_ue = IperfDataTransferDetails(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.191.243", username="vrf4_sg1", password="vrf4@sg1"
    ),
    network_interface_address="10.57.191.243",
    iperf_path="/usr/bin/iperf",
    port="51100",
)

_licensekeeper = LicenseKeeper(username="xiangli.kong@nokia-sbell.com", password="123456")
_android_ue1 = Android(
    ssh_connection_details=_ue_pc_ssh,
    serial_number="f20825f3",
    server_dir="C:/Program Files (x86)/Spark/Bin/Spark.exe",
    python_path="C:/Python38",
    iperf_details=_iperf_ue,
    imsi="460028001006299",
    capabilities=["huawei_sigspark"],
    licensekeeper=_licensekeeper,
)

_android_ue2 = Android(
    ssh_connection_details=_ue_pc_ssh,
    serial_number="c08c718d",
    server_dir="C:/Program Files (x86)/Spark/Bin/Spark.exe",
    python_path="C:/Python38",
    iperf_details=_iperf_ue,
    imsi="460028001006298",
    capabilities=["huawei_sigspark"],
    licensekeeper=_licensekeeper,
)


tl = TestLine(
    test_pc=_test_pc1,
    test_pcs=[_test_pc1, _test_pc2],
    gnbs=[_cbts1, _cbts2],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_FULLRACK_QC_SA_ASIKL_ABILB1_AHPE-ASIKR_ABILB4_AEHC",
    core=_core,
    # pdus=_pdus,
    ues=[_android_ue1, _android_ue2],
    # attenuator=_attenuator1,
    # attenuators=[_attenuator1, _attenuator2],
)

__all__ = ["tl"]
