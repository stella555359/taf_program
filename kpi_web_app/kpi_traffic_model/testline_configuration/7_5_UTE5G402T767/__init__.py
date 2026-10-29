import os
import re
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
from taf.config.testline.core import RealCore
from taf.config.testline.gnb.du import DU
from taf.config.testline.pdu import (
    FACOM,
    PduPort,
    Pdu,
    EPC,
    ATEN,
    RRB,
    APC,
    Gude,
    HBTE,
    TopYoung,
)
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

from taf.config.testline.attenuator import AttenuationPort  # added in taf.meta 5.4
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
from taf.config.testline.appserver import AppServer

__maintainer__ = "Shasha Liu"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_5_GMS <I_MN_5G_RAN_IV4_LINE_HZG_5@internal.nsn.com>"
)
__email__ = "shasha.liu@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

##host #Local VM
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.101.60.19", username="ute", password="ute"
    )
)

##RealEnb

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.71.213.230", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=None)

##5GRU for classicalBTS
_ru_1_pdu = TopYoung(addr="10.71.196.200", port_numbers=[3])
_ru_2_pdu = TopYoung(addr="10.71.196.208", port_numbers=[3])
_ru_3_pdu = TopYoung(addr="10.71.196.208", port_numbers=[1])
_ru_4_pdu = TopYoung(addr="10.71.196.210", port_numbers=[4])
_ru_5_pdu = TopYoung(addr="10.71.196.210", port_numbers=[5])
_ru_6_pdu = TopYoung(addr="10.71.196.210", port_numbers=[6])
_ru_7_pdu = TopYoung(addr="10.71.196.204", port_numbers=[1])
_ru_8_pdu = TopYoung(addr="10.71.196.204", port_numbers=[5])
_ru_9_pdu = TopYoung(addr="10.71.196.204", port_numbers=[4])
_ru_10_pdu = TopYoung(addr="10.71.196.208", port_numbers=[2])
_ru_11_pdu = TopYoung(addr="10.71.196.200", port_numbers=[4])
_ru_12_pdu = TopYoung(addr="10.71.196.200", port_numbers=[5])

_ru_1 = RU(
    ru_hw_group="below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2",
        username="serviceuser",
        password="wcdjLlTpqEY3cAmOe11u6aELwGI3rDvpGJQvCkcyHZc=",
    ),
    radio_type=RadioTypes.AZQU,  # radio_type='AZQU'
    pdu_port=_ru_1_pdu.pdu_ports[3],
)
_ru_2 = RU(
    ru_hw_group="below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.6",
        username="serviceuser",
        password="wcdjLlTpqEY3cAmOe11u6aELwGI3rDvpGJQvCkcyHZc=",
    ),
    radio_type=RadioTypes.AZQU,  # radio_type='AZQU'
    pdu_port=_ru_2_pdu.pdu_ports[3],
)
_ru_3 = RU(
    ru_hw_group="below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.154",
        username="serviceuser",
        password="wcdjLlTpqEY3cAmOe11u6aELwGI3rDvpGJQvCkcyHZc=",
    ),
    radio_type=RadioTypes.AZQU,  # radio_type='AZQU'
    pdu_port=_ru_3_pdu.pdu_ports[1],
)
_ru_4 = RU(
    ru_hw_group="below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.1.2",
        username="serviceuser",
        password="wcdjLlTpqEY3cAmOe11u6aELwGI3rDvpGJQvCkcyHZc=",
    ),
    radio_type=RadioTypes.AZQU,  # radio_type='AZQS'
    pdu_port=_ru_4_pdu.pdu_ports[4],
)
_ru_5 = RU(
    ru_hw_group="below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.1.6",
        username="serviceuser",
        password="wcdjLlTpqEY3cAmOe11u6aELwGI3rDvpGJQvCkcyHZc=",
    ),
    radio_type=RadioTypes.AZQU,  # radio_type='AZQS'
    pdu_port=_ru_5_pdu.pdu_ports[5],
)
_ru_6 = RU(
    ru_hw_group="below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.1.10",
        username="serviceuser",
        password="wcdjLlTpqEY3cAmOe11u6aELwGI3rDvpGJQvCkcyHZc=",
    ),
    radio_type=RadioTypes.AZQU,  # radio_type='AZQS'
    pdu_port=_ru_6_pdu.pdu_ports[6],
)
_ru_7 = RU(
    ru_hw_group="above6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.33.128",
        username="toor4nsn",
        password="oZPS0POrRieRtu",
    ),
    radio_type=RadioTypes.AHPE,  # radio_type='AHPE'
    pdu_port=_ru_7_pdu.pdu_ports[1],
)
_ru_8 = RU(
    ru_hw_group="above6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.33.130",
        username="toor4nsn",
        password="oZPS0POrRieRtu",
    ),
    radio_type=RadioTypes.AHPE,  # radio_type='AHPE'
    pdu_port=_ru_8_pdu.pdu_ports[5],
)
_ru_9 = RU(
    ru_hw_group="above6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.33.129",
        username="toor4nsn",
        password="oZPS0POrRieRtu",
    ),
    radio_type=RadioTypes.AHPE,  # radio_type='AHPE'
    pdu_port=_ru_9_pdu.pdu_ports[4],
)
_ru_10 = RU(
    ru_hw_group="above6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.33.133",
        username="toor4nsn",
        password="oZPS0POrRieRtu",
    ),
    radio_type=RadioTypes.AHPE,  # radio_type='AHPE'
    pdu_port=_ru_10_pdu.pdu_ports[2],
)
_ru_11 = RU(
    ru_hw_group="above6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.33.131",
        username="toor4nsn",
        password="oZPS0POrRieRtu",
    ),
    radio_type=RadioTypes.AHPE,  # radio_type='AHPE'
    pdu_port=_ru_11_pdu.pdu_ports[4],
)
_ru_12 = RU(
    ru_hw_group="above6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.33.132",
        username="toor4nsn",
        password="oZPS0POrRieRtu",
    ),
    radio_type=RadioTypes.AHPE,  # radio_type='AHPE'
    pdu_port=_ru_12_pdu.pdu_ports[5],
)

##DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.71.213.228", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.22")

_gnb_pdu = TopYoung(addr="10.71.196.203", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[1],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(
    airscale=_airscale,
    rus=[
        _ru_1,
        _ru_2,
        _ru_3,
        _ru_4,
        _ru_5,
        _ru_6,
        _ru_7,
        _ru_8,
        _ru_9,
        _ru_10,
        _ru_11,
        _ru_12,
    ],
    f1_m_ip_addr="10.71.213.228",
)

##CU #Auto TL Upgrading
_cu = CU(
    backhaul_site_oam_ip="10.71.213.228",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.213.228", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.213.228", username="Nemuadmin", password="nemuuser"
    ),
)


# classicalbts
_classical_bts = ClassicalBts(
    dus=[_du], cu=_cu, instance_id="2670", global_bts_id="2670"
)

_appserver_ssh = SshServiceDetails(
    addr="10.57.191.247", username="vrf4_sg5", password="vrf4@sg5", port="55912"
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.247",
    iperf_path="/data/data/com.nokia.syve.uemanager.mobile/",
    port=55914,
)
_appserver = AppServer(_iperf)

_ue1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.217.105", username="nokia5G", password="noki@123"
    ),
    serial_number="9YS0220114010364",
    server_dir="/cygdrive/c/pyro_server",
    python_path="/cygdrive/c/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["SG5_Mate30", "cell_Mapping: [4]", "huawei"],
)


# CI_Detail_UE_Type='Nokia FastMile 5G Gateway 3.1'

_netact = Netact("10.107.178.203")

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    nms=_netact,
    enbs=[_lte_real_enb],
    core=RealCore(mcc=262, mnc=3),
    ues=[_ue1],
    appserver=_appserver,
)

# old version keyword under robotws5g/resource compatibility workaround
# tl = TestlineWrapper(tl)
