__maintainer__ = "Sebastian Mikos"
__team__ = "MN 5G&SC 5G Pz 2 WRO 5 SG"
__email__ = "I_5GSC_5G_PZ2_WRO_5@internal.nsn.com"
__owner_email__ = "sebastian.mikos@nokia.com"

import os
from taf.config.testline.testline import TestLine
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.testpc import TestPc
from taf.config.testline.pdu import HBTE, TopYoung, PduPort
from taf.config.testline.radio import (
    RadioTypes,
    RU,
)
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.appserver import AppServer
from taf.config.testline.gnb import ClassicalBts, CU
from taf.config.testline import DU, RU, RealEnb, NetworkAddress, RoutingInformation
from taf.config.testline.core import RealCore5G
from taf.config.testline.ue import Android
from taf.config.testline.gnb.du import Cablink, Endpoint


_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.177.120", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_abil_master = CapacityUnit(addr="fsp-5a")
_abil_slave = CapacityUnit(addr="fsp-5b")
_abil_loner = CapacityUnit(addr="192.168.253.22")

# _pdu_1 = Gude("10.44.206.32", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], "EPC", "8221-1")

_pdu_1 = HBTE(addr="10.71.195.74", port_numbers=[5])
_common_unit_0_pdu_port = PduPort(pdu=_pdu_1, port_no="5")
_common_unit = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.228.34", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_abil_master, _abil_slave, _abil_loner],
    pdu_port=_common_unit_0_pdu_port,
)

_airscale = Airscale(common_units=[_common_unit])

# #CU
_cu = CU(
    backhaul_site_oam_ip="10.57.228.34",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.228.34", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.228.34", username="Nemuadmin", password="nemuuser"
    ),
)

_ru_pdu = HBTE(addr="10.57.176.2", port_numbers=[1, 2])
#_ru_pdu = TopYoung(addr="10.71.195.79", port_numbers=[1])

_ru0 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2", username="serviceuser", password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY="
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.77.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru_pdu.pdu_ports[1],
    radio_type=RadioTypes.AQQQA,

)

_ru_cablinks = [
    Cablink(
        source=Endpoint(unit=_common_unit,label="SFP", port_id=1),
        target=Endpoint(unit=_ru0 ,label="SFP", port_id=3),
    )
]

_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.6", username="serviceuser", password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY="
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.0.6", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru_pdu.pdu_ports[2],
    radio_type=RadioTypes.AQQJ,
)

_du = DU(airscale=_airscale, rus=[_ru0, _ru1], f1_m_ip_addr="10.57.228.34",cablinks=_ru_cablinks)

_classical_bts = ClassicalBts(cu=_cu, dus=[_du], global_bts_id=37404, instance_id=1940)

_core = RealCore5G(mcc=460, mnc=2)


_appserver_ssh = SshServiceDetails(
    addr="10.71.207.139", username="vrf3_sg5", password="vrf3@sg5", port="45840"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.207.139",
    port="45940",
    ports=["45940", "45840"],
)

# 10.71.217.58
# noklab\nokia5g
# noki@123
_ue_pc_ssh = SshServiceDetails(
    addr="10.57.150.49", username="mn5gran", password="nokia123@"
)


_android_1 = Android(
    ssh_connection_details=_ue_pc_ssh,
    serial_number="9YS0220720002158",
    server_dir="C:/pyro_server/",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "huawei"],
)


_appserver = AppServer(iperf_details=_iperf)

_abia = CapacityUnit(addr="192.168.253.20")

_asia = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.71.208.205", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_abia],
)

_lteenb = RealEnb(
    airscale=Airscale(common_units=[_asia]),
    x2_link_addr=NetworkAddress(
        v4="10.71.208.205",
        routing=RoutingInformation(gateway="10.71.208.1", ip_prefix_length=27),
    ),
    global_bts_id=10082,instance_id=1964
)

tl = TestLine(
    test_pc=_test_pc,
    test_pcs=[_test_pc],
    gnbs=[_classical_bts],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_QC_ASIBR_ABIN1_2xAHLOA_ENB",
    core=_core,
    ues=[_android_1],
    appserver=_appserver,
    enbs=[_lteenb]
)

__all__ = ["tl"]
