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
from taf.config.testline.attenuator import (
    AttenuationPort,
    TopYoung,
    HBTE,
)  # added in taf.meta 5.4
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
from taf.config.testline.appserver import AppServer
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.ue import Qualcomm, QualcommUeType, Android, MediaTek

__maintainer__ = "tizeng"
__team__ = "I_NSB_MN_5GSC_5G_PZ_HZ_03_GMS <I_NSB_MN_5GSC_5G_PZ_HZ_03@internal.nsn.com>"
__email__ = "jack.zeng@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# #host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.118", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_appserver_ssh = SshServiceDetails(
    addr="10.57.191.245",
    username="vrf4_sg3",
    password="Haz4_vrf_sg3",
    port="53160",
)
_iperf_1 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.245",
    iperf_path="/cygdrive/c/iperf",
    port="53260",
)

_iperf_2 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.245",
    iperf_path="/cygdrive/c/iperf",
    port="53360",
)

_iperf_3 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.245",
    iperf_path="/cygdrive/c/iperf",
    port="53460",
)

_iperf_details_on_appserver2 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.245",
    iperf_path="iperf",
    port="53560",
)
_appserver = AppServer(_iperf_details_on_appserver2)

# CI_Detail_UE_Type='sumsungS20'
_android_0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.62", username="mn5gran", password="nokia123@"
    ),
    serial_number="RFCX61M63DA",
    server_dir="C:\Program Files (x86)\DingLi\Pilot Pioneer10.5.0.57---08191556\Pioneer.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf_1,
    capabilities=["samsung", "samsung"],
    imsi="262033100009202",
    sec_key="13100009202",
)

# CI_Detail_UE_Type='sumsungS20_HPA'
_android_1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.62", username="mn5gran", password="nokia123@"
    ),
    serial_number="RFCW20HQAHJ",
    server_dir="C:\Program Files (x86)\DingLi\Pilot Pioneer10.5.0.57---08191556\Pioneer.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf_2,
    capabilities=["samsung", "samsung"],
    imsi="262033100010725",
    sec_key="13100010725",
)

# CI_Detail_UE_Type='sumsungS22_MPS'
_android_2 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.62", username="mn5gran", password="nokia123@"
    ),
    serial_number="R5CT310C58T",
    server_dir="C:\Program Files (x86)\DingLi\Pilot Pioneer10.5.0.57---08191556\Pioneer.exe",
    python_path="C:/Python27/python.exe",
    iperf_details=_iperf_3,
    capabilities=["samsung", "samsung"],
    imsi="460023100012397",
    sec_key="13100012397",
)

# #RealEnb
_real_enb1_pdu = FACOM(addr="10.57.246.242", port_numbers=[1])

_real_enb2_pdu = FACOM(addr="10.57.246.242", port_numbers=[5])

_common_unit_0 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.226.228", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb1_pdu.pdu_ports[1],
)

_common_unit_1 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.226.230", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb2_pdu.pdu_ports[5],
)

_real_enb_0 = Airscale(common_units=[_common_unit_0])

_real_enb_1 = Airscale(common_units=[_common_unit_1])

_lte_real_enb_0 = RealEnb(airscale=_real_enb_0, rms=None, instance_id=36021)

_lte_real_enb_1 = RealEnb(airscale=_real_enb_1, rms=None, instance_id=36022)

# #5GRU for classicalBTS
# attenuator
_hbte_params = {
    "ip_addr": "10.57.239.231",
    "port": 5000,
    "attenuation_port_numbers": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    "model": "PA-16-16-6-127-0.5-B-S",
    "version": None,
}
_attenuator = HBTE(**_hbte_params)

_ru1_pdu = FACOM(addr="10.57.249.46", port_numbers=[1])
_ru2_pdu = FACOM(addr="10.57.249.46", port_numbers=[2])
_ru3_pdu = FACOM(addr="10.57.246.242", port_numbers=[3])
_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.48.2", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.48.2", username="root", password="umniedziala"
    ),
    pdu_port=_ru1_pdu.pdu_ports[1],
    radio_type=RadioTypes.AEHC,
    signal_analyzer=None,
    attenuation_ports=[
        _attenuator.attenuator_ports[13],
        _attenuator.attenuator_ports[14],
        _attenuator.attenuator_ports[15],
        _attenuator.attenuator_ports[16],
    ],
)
_ru2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.73.128", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.73.128", username="root", password="umniedziala"
    ),
    pdu_port=_ru2_pdu.pdu_ports[2],
    radio_type=RadioTypes.AHLOA,
    signal_analyzer=None,
    attenuation_ports=[
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[6],
        _attenuator.attenuator_ports[7],
        _attenuator.attenuator_ports[8],
    ],
)

_ru3 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.73.128", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.73.128", username="root", password="umniedziala"
    ),
    pdu_port=_ru3_pdu.pdu_ports[3],
    radio_type=RadioTypes.AWHHF,
    signal_analyzer=None,
    attenuation_ports=[
        _attenuator.attenuator_ports[9],
        _attenuator.attenuator_ports[10],
        _attenuator.attenuator_ports[11],
        _attenuator.attenuator_ports[12],
    ],
)


# #DU for classicalBTS
_lmp_connection_0 = SshServiceDetails(
    addr="10.57.226.227", username="toor4nsn", password="oZPS0POrRieRtu"
)

_lmp_connection_1 = SshServiceDetails(
    addr="10.57.226.229", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_0 = CapacityUnit(addr="192.168.253.20")

_capacity_unit_1 = CapacityUnit(addr="192.168.253.21")

_gnb1_pdu = FACOM(addr="10.57.246.242", port_numbers=[1])

_gnb2_pdu = FACOM(addr="10.57.246.242", port_numbers=[5])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection_0,
    capacity_units=[_capacity_unit_0, _capacity_unit_1],
    pdu_port=_gnb1_pdu.pdu_ports[1],
)

_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection_1,
    capacity_units=_capacity_unit_0,
    pdu_port=_gnb2_pdu.pdu_ports[5],
)

_airscale_0 = Airscale(common_units=[_common_unit_0])

_airscale_1 = Airscale(common_units=[_common_unit_1])

_du_0 = DU(
    airscale=_airscale_0,
    rus=[_ru1, _ru2],
    f1_m_ip_addr="10.57.226.227",
    f1_c_ip_addr="10.57.226.227",
    f1_u_ip_addr="10.57.226.227",
)

_du_1 = DU(
    airscale=_airscale_1,
    rus=[_ru3],
    f1_m_ip_addr="10.57.226.229",
    f1_c_ip_addr="10.57.226.229",
    f1_u_ip_addr="10.57.226.229",
)

# #CU
_cu_0 = CU(
    backhaul_site_oam_ip="10.57.226.227",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.226.227", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.226.227", username="Nemuadmin", password="nemuuser"
    ),
)

_cu_1 = CU(
    backhaul_site_oam_ip="10.57.226.229",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.226.229", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.226.229", username="Nemuadmin", password="nemuuser"
    ),
)

_classical_bts_0 = ClassicalBts(dus=[_du_0], cu=_cu_0, instance_id=36011)

_classical_bts_1 = ClassicalBts(dus=[_du_1], cu=_cu_1, instance_id=36012)

_tl_cloud_topology = "CLOUD_5G_BB3"

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts_0, _classical_bts_1],
    enbs=[_lte_real_enb_0, _lte_real_enb_1],
    ues=[_android_0, _android_1, _android_2],
    appserver=_appserver,
    attenuator=[_attenuator],
    tl_cloud_topology=_tl_cloud_topology,
)
