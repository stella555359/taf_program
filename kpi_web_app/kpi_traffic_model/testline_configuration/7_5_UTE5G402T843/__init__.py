import os
import re
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
from taf.config.testline.testline import TestLine
from taf.config.testline.core import EPCSim, LTEEmuCore, PrismaCore
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
from taf.config.testline import RU, DU, Cablink, Endpoint
from taf.config.testline.pdn import PDN, PDPTypes
from taf.config.testline.pdu import FACOM, HBTE, PduPort, Pdu, EPC
from taf.config.testline.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline import Enb, SimEnb, RealEnb, LTEEmuEnb, PrismaEnb, DocomoEnb
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.config.testline.nms import Netact
from taf.config.testline.appserver import AppServer
from taf.config.testline.dcap import DcapRnD, DcapBasic
from taf.config.testline.ue import AirphoneCloud, Airphone, Prisma, TM500, MediaTek
from taf.config.testline.ue import Qualcomm, QualcommUeType, Android
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
from taf.config.testline.core import RealCore  # Use RealCore() for Real Core TL

__maintainer__ = "Luo Menghua"
__email__ = "menghua.luo@nokia-sbell.com"
__team__ = "i_nsb_mn_ran_rd_vrf_haz4_07 <i_nsb_mn_ran_rd_vrf_haz4_07@internal.nsn.com>"

##common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# Below _docker_pc is a TestPC() object, representing a DCAP Server Container, which DOES NOT connect to SMOD's LMP port via vLAN
_docker_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.195.83",
        username="utfuser",
        password="utfadmin!",
        port=49148,
    )
)

_tce_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.195.83",
        username="utfuser",
        password="utfadmin!",
        port=49148,
    )
)
External_PCs_For_CellTrace = dict(docker=_docker_pc, tce=_tce_pc)

_dcap_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.195.83",
        username="utfuser",
        password="utfadmin!",
        port=49148,
    )
)

##DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    #    addr="10.101.50.229", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(
    addr="192.168.253.20",
    hardware_type="ABIO",
    # rus=[_ru1, _ru2, _ru3],
)

_gnb_pdu = HBTE(addr="10.101.45.164", port_numbers=[4])
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[4],
    hardware_type="ASIL",
)
_airscale = Airscale(common_units=[_common_unit_0])

# 5GRU for classicalBTS
_ru1_pdu = HBTE(addr="10.101.45.162", port_numbers=[4])
_ru1 = RU(
    ru_hw_group="AEQN",
    #    default_ssh_connection_details=SshServiceDetails(addr="1.1.1.1",username="rfsw",password="HfBKgqIOogKY3BlGtiniuCI9bs76C8jYsAY6vw8f/Tw=",),
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1",
        username="serviceuser",
        password="KdtPWG5UscF/BANWYrnUc7XNPxfZTNDu9KAM8+8+XGU=",
    ),
    lmp_connection=SshServiceDetails(
        addr="1.1.1.1", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru1_pdu.pdu_ports[4],
    radio_type=RadioTypes.AEQN.value,
)

_ru2_pdu = HBTE(addr="10.101.45.162", port_numbers=[5])
_ru2 = RU(
    ru_hw_group="AEQN",
    #    default_ssh_connection_details=SshServiceDetails(addr="1.1.1.1",username="rfsw",password="HfBKgqIOogKY3BlGtiniuCI9bs76C8jYsAY6vw8f/Tw=",),
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1",
        username="serviceuser",
        password="KdtPWG5UscF/BANWYrnUc7XNPxfZTNDu9KAM8+8+XGU=",
    ),
    lmp_connection=SshServiceDetails(
        addr="1.1.1.1", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru2_pdu.pdu_ports[5],
    radio_type=RadioTypes.AEQN.value,
)

_ru3_pdu = HBTE(addr="10.101.45.166", port_numbers=[2])
_ru3 = RU(
    ru_hw_group="hw_group",
    #    default_ssh_connection_details=SshServiceDetails(addr="1.1.1.1",username="rfsw",password="HfBKgqIOogKY3BlGtiniuCI9bs76C8jYsAY6vw8f/Tw=",),
    default_ssh_connection_details=SshServiceDetails(
        addr="1.1.1.1",
        username="serviceuser",
        password="KdtPWG5UscF/BANWYrnUc7XNPxfZTNDu9KAM8+8+XGU=",
    ),
    lmp_connection=SshServiceDetails(
        addr="1.1.1.1", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru3_pdu.pdu_ports[2],
    radio_type=RadioTypes.AEQN.value,
)

_ru_cablinks = [
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="OPT", port_id=1),
        target=Endpoint(unit=_ru1, label="SFP", port_id=2),
    ),
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="OPT", port_id=2),
        target=Endpoint(unit=_ru2, label="SFP", port_id=2),
    ),
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="OPT", port_id=3),
        target=Endpoint(unit=_ru3, label="SFP", port_id=2),
    ),
]

_du = DU(airscale=_airscale, rus=[_ru1, _ru2, _ru3], f1_m_ip_addr="10.101.50.229")

##CU
_cu = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.50.229", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.50.229", username="Nemuadmin", password="nemuuser"
    ),
)

# classicalbts
_classical_bts = ClassicalBts(
    dus=[_du], cu=_cu, global_bts_id=843, instance_id=843, dcap=_tce_pc
)

##host
# _host = TestPc(default_ssh_connection_details=SshServiceDetails(addr="10.57.157.235", username="ute", password="iW_K#8.ute%A10h0m0ra"))
_gnb_testpc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.217.53", username="ute", password="uteUTE!"
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_classical_bts.dus[0].airscale.common_units[0],
            interface_type="lmp",
        )
    ],
)

##NMS
_netact = Netact("10.107.178.214")

##appserver
_appserver_ssh = SshServiceDetails(
    addr="10.57.191.238", username="vrf3_sg6", password="vrf3@sg6"
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.238",
    iperf_path="/usr/bin/iperf",
    port=57843,
)

##Huawei UE
_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.68.86.218", username="mn5gran", password="nokia123@"
    ),
    serial_number="9EQUT20721012243",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["ANDROID_UE0", "huawei"],
)

##RealCore
_real_5g_core_details = RealCore5GDetails(
    amf=AMF(
        oam_ssh_connection_details=SshServiceDetails(
            addr="10.110.133.68", username="xxx", password="xxx"
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
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ANDROID_SA_ASILL_ABIOB1_3xAEQN"

tl = TestLine(
    test_pc=_gnb_testpc,
    gnbs=[_classical_bts],
    tl_cloud_topology=_tl_cloud_topology,
    ues=[_android],
    host=[_docker_pc, _tce_pc, _dcap_pc],
    nms=_netact,
    core=_realcore,
)
