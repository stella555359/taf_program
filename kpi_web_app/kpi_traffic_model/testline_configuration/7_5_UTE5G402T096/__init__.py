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
from taf.config.testline.testpc import TestPc, Connection
from taf.config.testline.core import (
    EPCSim,
    LTEEmuCore,
    PrismaCore,
    RealCore,
    RealCore4GDetails,
    RealCore5GDetails,
    AMF,
    MME,
)
from taf.config.testline import RU, DU
from taf.config.testline.pdn import PDN, PDPTypes
from taf.config.testline.pdu import HBTE, PduPort, Pdu, EPC
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import AirphoneCloud, Airphone, Prisma, Android
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
from taf.config.testline.dcap import DcapRnD, DcapBasic

__maintainer__ = "Li Xiaofei"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_7_GMS <I_MN_5G_RAN_IV4_LINE_HZG_7@internal.nsn.com>"
)
__email__ = "xiaofei.li@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

##Cobham
_appserver_ssh = SshServiceDetails(
    addr="10.57.191.238", username="vrf3_sg6", password="vrf3@sg6"
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.238",
    iperf_path="/usr/bin/iperf",
    port=57096,
)

# 5GRU for classicalBTS
_ru_pdu = HBTE(addr="10.68.87.78", port_numbers=[1])

_ru = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.1.5", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu.pdu_ports[1],
    radio_type=RadioTypes.AEQV.value,
)

##DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(
    addr="192.168.253.20",
    hardware_type="ABIL",
    # rus=[_ru],
)
_gnb_pdu = HBTE(addr="10.68.87.106", port_numbers=[8])
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[8],
    hardware_type="ASIB",
)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(airscale=_airscale, rus=[_ru], f1_m_ip_addr="10.68.89.2")

##CU
_cu = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.68.89.2", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.68.89.2", username="Nemuadmin", password="nemuuser"
    ),
)

# RealEnb
_lmp_connection_enb = SshServiceDetails(
    addr="10.68.88.246", username="toor4nsn", password="oZPS0POrRieRtu"
)
_enb_pb = HBTE(addr="10.68.87.107", port_numbers=[8])
_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection_enb,
    capacity_units=[],
    pdu_port=_enb_pb.pdu_ports[8],
    hardware_type="ABIA",
)
_real_enb = Airscale(common_units=[_common_unit_1])
_lte_real_enb = RealEnb(airscale=_real_enb, rms=None, global_bts_id=96, instance_id=96)

# _docker_pc = TestPc(
#    default_ssh_connection_details=SshServiceDetails(
#        addr="10.57.195.82",
#        username="utfuser",
#        password="utfadmin!",
#        port=49148,
#    ),  # for dcap
# )
_docker_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.195.83",
        username="utfuser",
        password="utfadmin!",
        port=49148,
    ),  # for dcap
)
# _tce_pc = DcapBasic(
#    connection_details=HttpConnectionDetails(
#        addr="10.57.195.82",
#        username="utfuser",
#        password="utfadmin!",
#        port=49148,
#    )
# )
_tce_pc = DcapBasic(
    connection_details=HttpConnectionDetails(
        addr="10.57.195.83",
        username="utfuser",
        password="utfadmin!",
        port=49148,
    )
)
# TestPc(
#     default_ssh_connection_details=SshServiceDetails(
#         addr="10.57.167.172",
#         username="utfuser",
#         password="iW_K#8.ute%A10h0m0ra",
#         port=49151,
#     ),         # for dcap
# )

# classicalbts
_classical_bts = ClassicalBts(
    dus=[_du], cu=_cu, global_bts_id=96, instance_id=96, dcap=_tce_pc
)

##host
_gnb_testpc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.251.66", username="ute", password="uteUTE!"
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_classical_bts.dus[0].airscale.common_units[0],
            interface_type="lmp",
        )
    ],
)

_enb_testpc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.251.66", username="ute", password="uteUTE!"  # use gNB TestPC IP
    ),
    connections=[],  # Leave the "connection" empty for eNB TestPC
)

_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.68.86.53", username="mn5gran", password="nokia123@"
    ),
    serial_number="L8K5T19911001657",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["ANDROID_UE0", "huawei"],
)

# Real Core
_real_5g_core_details = RealCore5GDetails(
    amf=AMF(
        oam_ssh_connection_details=SshServiceDetails(
            addr="10.110.227.5", username="xxx", password="xxx"
        ),
        n2=NetworkAddress(v4="xxx.xxx.xx.xx", v6="xxx:xx::xxx", vlan_id=1),
    )
)
_pdns = [
    PDN(pdp_type=PDPTypes.IPV4V6.value, apn="dxdata1"),
    PDN(pdp_type=PDPTypes.IPV4V6.value, apn="wap1.nokia.com"),
]
_realcore = RealCore(five_g=_real_5g_core_details, mcc="460", mnc="2", pdns=_pdns)

##cloud_topology
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ANDROID_ASIBL_ABILB1_AEQV_ENB"

tl = TestLine(
    test_pc=_gnb_testpc,
    test_pcs=[_gnb_testpc],
    gnbs=[_classical_bts],
    enbs=[_lte_real_enb],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_ANDROID_ASIBL_ABILB1_AEQV_ENB",
    ues=[_android],
    core=_realcore,
    # appserver=_appserver,
)
