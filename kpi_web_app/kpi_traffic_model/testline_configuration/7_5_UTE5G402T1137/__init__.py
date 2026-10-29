import os
import yaml
import re
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc, Connection
from taf.config.testline.core import RealCore
from taf.config.testline import RU, DU
from taf.config.testline.gnb.du import Cablink, Endpoint
from taf.config.testline.pdu import HBTE
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, RRB, APC, Gude, FPFH
from taf.config.testline.testline import TestLine
from taf.config.testline.ue import Android
from taf.config.testline.gnb import CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.pdu import Gude, TopYoung
from taf.config.testline.radio import RU, RadioTypes
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
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)
from taf.config.testline.attenuator import AttenuationPort, TopYoung
from taf.config.testline.attenuator import HBTE as AHBTE
from taf.config.testline import NetworkAddress, RoutingInformation
from taf.config.testline.appserver import AppServer
from taf.config.testline import NetAct

__maintainer__ = "Melinda Gao"
__team__ = "I_NSB_MN_5GSC_5G_PZ_HZ_08_GMS <I_NSB_MN_5GSC_5G_PZ_HZ_08@internal.nsn.com>"
__email__ = "xu.3.liu@nokia-sbell.com"
# common
__all__ = ["tl"]
_cfg_dir = os.path.dirname(os.path.abspath(__file__))

_appserver_ssh = SshServiceDetails(
    addr="10.57.191.239", username="vrf3_sg8", password="vrf3@sg8", port="58999"
)
_iperf_1 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.239",
    iperf_path="/usr/bin/iperf",
    port="58325",
)

_appserver = AppServer(_iperf_1)
_appserver.iperf_details.port = 58325

# CI_Detail_UE_Type='Huawei Honor 30s'
_ue1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.152", username="mn5gran", password="nokia123@"
    ),
    serial_number="9YS0219C07033999",
    server_dir="/cygdrive/c/pyro_server",
    python_path="/cygdrive/c/Python27/python.exe",
    iperf_details=_iperf_1,
    capabilities=["SG8_HONOR30s", "cell_Mapping: [1]", "huawei"],
)

_ru_pdu = HBTE(
    addr="10.57.176.132",
    port_numbers=[1, 2, 3, 4, 5, 6],
    model="HBTE",
)

_ru_1 = RU(
    ru_hw_group="hw_group",
    serial_number="1M251401606",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.10.49",
        username="serviceuser",
        password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og=",
    ),
    pdu_port=_ru_pdu.pdu_ports[1],
    radio_type=RadioTypes.AVQD,
)

_ru_2 = RU(
    ru_hw_group="hw_group",
    serial_number="RW201001201",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.10.49",
        username="serviceuser",
        password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og=",
    ),
    pdu_port=_ru_pdu.pdu_ports[6],
    radio_type=RadioTypes.AZNA,
)
# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.57.227.2", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(addr="192.168.253.20", hardware_type="ABIP",)

_ru_cablinks = [
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=1),
        target=Endpoint(unit=_ru_1, label="SFP", port_id=1),
    ),
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=2),
        target=Endpoint(unit=_ru_1, label="SFP", port_id=2),
    ),
]

_gnb_pdu = HBTE(addr="10.57.176.132", port_numbers=[2])
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[2],
    hardware_type="ASIM",
)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(
    airscale=_airscale, rus=[_ru_1,_ru_2], f1_m_ip_addr="10.57.227.2", cablinks=_ru_cablinks
)

# CU
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.57.227.2",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.57.227.2", ip_prefix_length=27),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.227.2", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.227.2", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.57.227.2",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.57.227.1", ip_prefix_length=27),
    ),
    x2u=NetworkAddress(
        v4="10.57.227.2",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.57.227.1", ip_prefix_length=27),
    ),
    s1u=NetworkAddress(
        v4="10.57.227.2",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.57.227.1", ip_prefix_length=27),
    ),
)


# cloud_topology
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ANDROID_SA_ASIML_ABIPB1_AVQD"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=10553, global_bts_id=1137)

# #######Netact########

_netact_ssh_2014 = SshServiceDetails('10.68.84.15', 'omc', password='Nokia123!')
_netact_http_2014 = HttpConnectionDetails('chen2lbwas.chen2.srn.dyn.nesc.nokia.net', 'omc', password='Nokia123!')
_netact_2014 = NetAct(_netact_ssh_2014, _netact_http_2014)

# host
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.11", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# RealEnb

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.227.2", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, instance_id="10553")  # 3136 =？ lxj

tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_classical_bts],
    enbs=[_lte_real_enb],
    appserver=_appserver,
    ues=[_ue1],
    core=RealCore(mcc=262, mnc=3),
    nms=_netact_2014,
    #attenuator=_attenuator,
    tl_cloud_topology=_tl_cloud_topology,
)