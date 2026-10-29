__maintainer__ = "Yang Di"
__team__ = "MN RAN VRF 3 HAZ 5 SG"
__email__ = "I_NSB_MN_RAN_RD_VRF_HAZ3_05@internal.nsn.com"
__owner_email__ = "di.yang@nokia-sbell.com"

import os
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import (
    HttpConnectionDetails,
    SshServiceDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline import NetworkAddress
from taf.config.testline.pdu import HBTE, PduPort, FACOM, TopYoung
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline import Airphone
from taf.config.testline.attenuator import HBTE as AHBTE
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)
from taf.config.testline.appserver import AppServer
from taf.config.testline import DU, RU, RealEnb, NetworkAddress, RoutingInformation
from taf.config.testline.core import RealCore5G
from taf.config.testline.ue import Android
from taf.config.testline.flexi import Flexi

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

_test_pc1 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.178",
        username="ute",
        password="iW_K#8.ute%A10h0m0ra",
    )
)

_pdu_gnb1 = HBTE(
    port_numbers=[1],
    addr="10.71.195.74",
)

_pdus = [_pdu_gnb1]

_cu1 = CU(
    backhaul_site_oam_ip="10.71.208.226",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.208.226", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.208.226", username="Nemuadmin", password="nemuuser"
    ),
)

_abio_du1 = CapacityUnit(addr="192.168.253.16")
_abio_slave = CapacityUnit(addr="192.168.253.20")
_abio_loner = CapacityUnit(addr="192.168.253.21")

_asil_du1 = CommonUnit(
    pdu_port=_pdus[0].pdu_ports[1],
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_abio_du1, _abio_slave, _abio_loner],
)

_ru_pdu = TopYoung(addr="10.71.195.46", port_numbers=[1])

_ru0 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2", username="rfsw", password="3Is6ezFJ7dFlB29cgs0yp3RCM3fUF1zNO1+6Z08tlAc="
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.255.254", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru_pdu.pdu_ports[1],
    radio_type=RadioTypes.AQQQA,
)

_du1 = DU(airscale=Airscale(common_units=[_asil_du1]), f1_m_ip_addr="10.71.208.226", rus=[_ru0])

_cbts1 = ClassicalBts(cu=_cu1, dus=[_du1], global_bts_id=19296, instance_id=1969)

_appserver_ssh = SshServiceDetails(
    addr="10.71.207.139",
    username="vrf3_sg5",
    password="vrf3@sg5",
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.207.139",
    iperf_path="/data/data/com.nokia.android.application/",
    port="45969",
)

_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.217.47", username="mn5gran", password="nokia123@"
    ),
    serial_number="9YS5T19C25002033",
    server_dir="/cygdrive/c/pyro_server",
    python_path="/cygdrive/c/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["Commercial", "HUAWEI"],
)


_core = RealCore5G(mcc=262, mnc=3)

tl = TestLine(
    test_pc=_test_pc1,
    gnbs=[_cbts1],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_QC_ASILR_AQQQA",
    ues=[_android],
    pdus=_pdus,
    core=_core,
)

__all__ = ["tl"]
