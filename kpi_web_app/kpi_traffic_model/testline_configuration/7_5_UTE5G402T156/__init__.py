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
from taf.config.testline.ue import (
    AirphoneCloud,
    Airphone,
    Prisma,
    TM500,
    Qualcomm,
    QualcommUeType,
    Android,
)  # added in taf.meta.5.4
from taf.config.testline.testpc import Connection
from taf.config.testline.core import RealCore
from taf.config.testline.gnb.du import DU, Cablink, Endpoint
from taf.config.testline.pdu import TopYoung
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, ATEN, RRB, APC, Gude
from taf.config.testline.attenuator import HBTE as HBTE
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import AirphoneCloud, Airphone, Prisma, TM500
from taf.config.testline.enb import (
    Enb,
    SimEnb,
    RealEnb,
    LTEEmuEnb,
    PrismaEnb,
    DocomoEnb,
)
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch

# added in taf.meta 5.4
# from taf.config.testline.gnb.networkaddress import NetworkAddress  # add in taf.meta 5.4
from taf.config.testline import NetworkAddress, RoutingInformation
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)
from taf.config.testline.hardware_controller import (
    AmiaFanHardwareController,
    GPSPowerHardwareController,
)
from taf.config.testline.appserver import AppServer


__maintainer__ = "duqi"
__team__ = "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_02@internal.nsn.com"
__email__ = "qi.du@nokia-sbell.com"


# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# #host
# _host = TestPc(
#     default_ssh_connection_details=SshServiceDetails(
#         addr="10.57.155.210", username="ute", password="iW_K#8.ute%A10h0m0ra"
#     )
# )
#_host = TestPc(
#    default_ssh_connection_details=SshServiceDetails(
#        addr="10.70.230.150", username="ute", password="ute"
#    )
#)






# PB INFO of ENB IS NOT CORRECT #
# 4GRU for RealEnb
_ru_enb_pdu = TopYoung(addr="10.71.196.18", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru_enb = RadioModule(
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.37.128",
        username="root",
        password="XwcvfotfCCOIAqtk7uQjN38d8sG5Yp2Pb2/p6Eqw8+Y=",
    ),
    pdu_port=_ru_enb_pdu.pdu_ports[4],
)

# #RealEnb
_real_enb_pdu = TopYoung(addr="10.71.196.20", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.71.204.194", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb)

# #5GRU_0 for cloudBTS
_ru_pdu = TopYoung(addr="10.71.196.20", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_attenuator_0 = HBTE(
    ip_addr="10.71.204.195",
    port=5000,
    attenuation_port_numbers=[5,6,7,8],
    model="PA-16-16-6-127-0.5-B-S",
)
_ru = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.48.2",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    pdu_port=_ru_pdu.pdu_ports[4],
    attenuation_ports=[
        _attenuator_0.attenuator_ports[5],
        _attenuator_0.attenuator_ports[6],
        _attenuator_0.attenuator_ports[7],
        _attenuator_0.attenuator_ports[8],
    ],
    radio_type=RadioTypes.AQQN.value,
)

# #######Iperf########
_appserver_ssh = SshServiceDetails(
    addr="10.57.191.234", username="vrf3_sg2", password="vrf3@sg2", port="42156"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.234",
    iperf_path="/data/local/tmp",
    port="42156",
)

_iperf_details_on_appserver2 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.234",
    iperf_path="/data/local/tmp",
    port="42156",
)
_appserver = AppServer(_iperf_details_on_appserver2)

# Huawei
_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.217.129", username="mn5gran", password="nokia123@"
    ),
    serial_number="9YS5T19B28006477",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Users/mn5gran/AppData/Local/Programs/Python/Python313/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["huawei"],
)

# #DU_0 for cloudlBTS
_lmp_connection_0 = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_0 = CapacityUnit(
    addr="192.168.253.20",
    hardware_type="ABIO",rus=[_ru])

_du_pdu = TopYoung(addr="10.71.196.20", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru_cablinks = [
    Cablink(
        source=Endpoint(unit=_capacity_unit_0, label="SFP", port_id=1),
        target=Endpoint(unit=_ru, label="SFP", port_id=1),
    ),
    Cablink(
        source=Endpoint(unit=_capacity_unit_0, label="SFP", port_id=7),
        target=Endpoint(unit=_ru, label="SFP", port_id=2),
    ),
]

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection_0,
    capacity_units=[_capacity_unit_0],
    pdu_port=_du_pdu.pdu_ports[2],
    hardware_type="ASIB",
)

_airscale = Airscale(common_units=[_common_unit_0])
_f1_m_ip_addr = "10.71.211.131"
_du = DU(
    airscale=_airscale, rus=[_ru], f1_m_ip_addr=_f1_m_ip_addr, cablinks=_ru_cablinks
)

# #CU
_cu_NetworkAddress = NetworkAddress(
    v4=_f1_m_ip_addr,
    vlan_id=None,
    routing=RoutingInformation(gateway="10.71.211.129", ip_prefix_length=27),
)

_cu = CU(
    backhaul_site_oam_ip=_cu_NetworkAddress,
    oam_ssh_connection_details=SshServiceDetails(
        addr=_f1_m_ip_addr, username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr=_f1_m_ip_addr, username="Nemuadmin", password="nemuuser"
    ),
    x2c=_cu_NetworkAddress,
    x2u=_cu_NetworkAddress,
    s1u=_cu_NetworkAddress,
)

# classicalbts------------------------------------------------
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=11064, global_bts_id=10682)

_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.251.45", username="ute", password="ute"
    ),
    connections=[Connection(interface="eth1", device=_classical_bts.dus[0].airscale.common_units[0], interface_type="lmp")],
)

# #cloud_topology------------------------------------------------
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ASIBL_ABIOB1_AQQN"

tl = TestLine(
    #test_pc=_test_pc_gnb,
    #test_pcs=[_test_pc_gnb],
    test_pc=_host,
    test_pcs=[_host],
    ues=[_android],
    gnbs=[_classical_bts],
    enbs=[_lte_real_enb],
    core=RealCore(mcc=460, mnc=2),
    attenuator=[_attenuator_0],
    appserver=_appserver,
    tl_cloud_topology=_tl_cloud_topology,
)

