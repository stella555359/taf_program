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
from taf.config.testline.core import EPCSim, LTEEmuCore, PrismaCore
from taf.config.testline import RU, DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, HBTE
from taf.config.testline import TopYoung_PDU
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import (
    AirphoneCloud,
    Airphone,
    Prisma,
    TM500,
    Qualcomm,
    QualcommUeType,
    Android,
    MediaTek,
)
from taf.config.testline import (
    Enb,
    SimEnb,
    RealEnb,
    RadioModule,
    LTEEmuEnb,
    PrismaEnb,
    DocomoEnb,
)
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)
from taf.config.testline.attenuator import AttenuationPort, TopYoung
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.appserver import AppServer

__maintainer__ = "yulu"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_2_GMS <I_MN_5G_RAN_IV4_LINE_HZG_2@internal.nsn.com>"
)
__email__ = "lu.1.yu@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.70.230.147", username="ute", password="ute"
    )
)


# Huawei
_appserver_ssh = SshServiceDetails(
    addr="10.71.219.230", username="iperf", password="39nBTScHWRf3weyBMK0=", port="52892"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.219.230",
    iperf_path="/usr/bin/iperf",
    port=52977,
)

_Huawei_host_ssh = SshServiceDetails(
    addr="10.71.217.76", username="MN5GRAN", password="nokia123@"
)

_appserver = AppServer(_iperf)

_Huawei = Android(
    ssh_connection_details=_Huawei_host_ssh,
    serial_number="7TD5T21402010749",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "cell_Mapping: [1]", "huawei"],
)

# 5GRU for classicalBTS
_ru_0_pdu = TopYoung_PDU(addr="10.71.197.84", port_numbers=[4])

_ru_0 = RU(
    #'AHPH'
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.73.129", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.73.129", username="root", password="umniedziala"
    ),
    pdu_port=_ru_0_pdu.pdu_ports[4],
    radio_type=RadioTypes.AHPH,
    serial_number="EA214250277",
)

_ru_1_pdu = TopYoung_PDU(addr="10.71.197.84", port_numbers=[5])

_ru_1 = RU(
    #'AHPH'
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.73.129", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.73.129", username="root", password="umniedziala"
    ),
    pdu_port=_ru_1_pdu.pdu_ports[5],
    radio_type=RadioTypes.AHPH,
    serial_number="EA214250274",
)

_ru_2_pdu = TopYoung_PDU(addr="10.71.197.88", port_numbers=[5])

_ru_2 = RU(
    #'AHPH'
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.73.129", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.73.129", username="root", password="umniedziala"
    ),
    pdu_port=_ru_2_pdu.pdu_ports[5],
    radio_type=RadioTypes.AHPH,
    serial_number="EA204954041",
)

# DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")

_gnb_pdu = HBTE(addr="10.71.197.87", port_numbers=[1])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[1],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru_0, _ru_1, _ru_2], f1_m_ip_addr="10.71.215.198")

_cu = CU(
    backhaul_site_oam_ip="10.71.215.198",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.215.198", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.215.198", username="Nemuadmin", password="nemuuser"
    ),
)


# cloud_topology
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ANDROID_SA_ASIBL_ABIOB1_3xAHPH"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=10892, global_bts_id=10892)

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    ues=[_Huawei],
    tl_cloud_topology=_tl_cloud_topology,
    appserver=_appserver,
)
