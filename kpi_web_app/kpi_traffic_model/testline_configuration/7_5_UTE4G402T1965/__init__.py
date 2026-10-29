__maintainer__ = "Li Xudong"
__team__ = "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_05@internal.nsn.com"
__email__ = "xudong.1.li@nokia-sbell.com"

import os
from taf.config.testline.cloud_hosting import (
    ControlNode,
    NCIR,
    CloudDeployment,
    DeploymentFlavorStack,
    DeploymentNetworkStack,
    DeploymentVnfStack,
    ComputeNode,
    OSP,
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
from taf.config.testline.gnb.du import DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, ATEN, RRB, APC, Gude
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import (
    AirphoneCloud,
    Airphone,
    Prisma,
    TM500,
    Qualcomm,
    QualcommUeType,
    Android,
)  # added in taf.meta.5.4
from taf.config.testline.enb import (
    Enb,
    SimEnb,
    RealEnb,
    LTEEmuEnb,
    PrismaEnb,
    DocomoEnb,
)
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.config.testline.attenuator import AttenuationPort, TopYoung

# added in taf.meta 5.4
from taf.config.testline.gnb.networkaddress import NetworkAddress  # add in taf.meta 5.4
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
from taf.config.testline.signal_analyzer import KeysightN9935A
from taf.config.testline.nms import Netact
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.optical_switch import Leoni
from taf.config.testline.appserver import AppServer
from taf.config.testline.core import RealCore4G
from taf.config.testline.attenuator import TopYoung
from taf.config.testline.pdu import HBTE

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# #host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.101.60.88", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)


_appserver_ssh = SshServiceDetails(
    addr="10.71.219.25", username="mmw_sg5", password="mm@5"
)

_appserver_ssh_ute = SshServiceDetails(
    addr="10.101.60.88", username="ute", password="iW_K#8.ute%A10h0m0ra", port="10000"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.219.25",
    iperf_path="/data/data/com.nokia.syve.uemanager.mobile/iperf",
    port="45965",
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.219.25",
    iperf_path="iperf",
    port="45965",
)
_appserver = AppServer(_iperf_details_on_appserver)

_android1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.70.14.239", username="mengli", password="Nokia@123"
    ),
    serial_number="9069ef18",
    server_dir="C:/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",   
    iperf_details=_iperf,
    capabilities=["UE_0", "REAL_ANDROID_UE", "qct_dx50"],
)


# #RealEnb
# _real_enb_pdu = HBTE(addr="10.68.87.114", port_numbers=[3])

_capacity_unit = CapacityUnit(addr="192.168.255.129")
_capacity_unit1 = CapacityUnit(addr="192.168.253.24")
_capacity_unit2 = CapacityUnit(addr="192.168.253.16")

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.70.14.95", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_capacity_unit, _capacity_unit1, _capacity_unit2],
    #    pdu_port=_real_enb_pdu.pdu_ports[3],
)

_real_enb1 = Airscale(common_units=[_common_unit_2])

_lte_real_enb1 = RealEnb(
    airscale=_real_enb1,
    rms=None,
    instance_id=4826,
    global_bts_id=4826,
    oam_ip=NetworkAddress(
        v4="10.70.14.95",
    ),
)

_attenuator = TopYoung(
    ip_addr="10.97.78.15",
    port=1000,
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
)

_ru1 = RU(
    ru_hw_group="mmw",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.33.128", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.33.128", username="root", password="umniedziala"
    ),
    radio_type="AHEGB",
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[6],
        _attenuator.attenuator_ports[7],
        _attenuator.attenuator_ports[8],
        _attenuator.attenuator_ports[9],
        _attenuator.attenuator_ports[10],
        _attenuator.attenuator_ports[11],
        _attenuator.attenuator_ports[12],
        _attenuator.attenuator_ports[13],
        _attenuator.attenuator_ports[14],
        _attenuator.attenuator_ports[15],
        _attenuator.attenuator_ports[16],
    ],
)
_lmp_connection = SshServiceDetails(
    addr="10.70.14.95", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(addr="192.168.255.129")
_capacity_unit1 = CapacityUnit(addr="192.168.253.24")
_capacity_unit2 = CapacityUnit(addr="192.168.253.16")
_du_pdu = ATEN(
    addr="10.101.60.88",
    port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
)
_du_pdu_port = PduPort(pdu=_du_pdu, port_no=2)

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit, _capacity_unit1, _capacity_unit2],
    pdu_port=_du_pdu_port,
)
_airscale = Airscale(common_units=[_common_unit_0])

_enb1_oam_ip = NetworkAddress(v4="10.70.14.95")
_du1 = DU(
    airscale=_airscale,
    rus=[_ru1],
    oam_ip=_enb1_oam_ip.v4,
    f1_m_ip_addr=_enb1_oam_ip.v4,
    f1_c_ip_addr=_enb1_oam_ip.v4,
    f1_u_ip_addr=_enb1_oam_ip.v4,
)
_cu1 = CU(
    backhaul_site_oam_ip="10.70.14.95",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.70.14.95", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.70.14.95", username="Nemuadmin", password="nemuuser"
    ),
)
_cbts1 = ClassicalBts(dus=[_du1], cu=_cu1, instance_id=4826, global_bts_id=4826)

_realcore = RealCore4G()

# ====== WTS ========
_lteemu = LTEEmuCore(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.101.60.88", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    dir_path="/opt/wts/latest",
    cfg_filename="TL81_CA_L1BP.cfg",
    mme_ip="",
    edaemon_port="22222",
    egate_port="33333",
)

_tl_cloud_topology = "CLOUD_5G_BB3"
tl = TestLine(
    test_pc=_host,
    gnbs=[_cbts1],
    core=_lteemu,
    enbs=[_lte_real_enb1],
    ues=[_android1],
    appserver=_appserver,
    tl_cloud_topology=_tl_cloud_topology,
    attenuator=_attenuator,
)
