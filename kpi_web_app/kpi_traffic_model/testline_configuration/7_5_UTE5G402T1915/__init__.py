__maintainer__ = "Yang Di"
__team__ = "I_NSB_MN_RAN_RD_VRF_HAZ3_05_GMS"
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
from taf.config.testline.pdu import HBTE, PduPort, FACOM
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
        addr="10.57.177.29",
        username="ute",
        password="iW_K#8.ute%A10h0m0ra",
    )
)

_pdu_gnb1 = HBTE(
    port_numbers=[1],
    addr="10.71.195.80",
)

_pdus = [_pdu_gnb1]

_cu1 = CU(
    backhaul_site_oam_ip="10.71.209.6",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.209.6", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.209.6", username="Nemuadmin", password="nemuuser"
    ),
)

_abio_du1 = CapacityUnit(addr="192.168.253.16")
_abio_slave = CapacityUnit(addr="192.168.253.17")
_abio_loner = CapacityUnit(addr="192.168.253.18")

_asil_du1 = CommonUnit(
    pdu_port=_pdus[0].pdu_ports[1],
    lmp_connection=SshServiceDetails(
        addr="10.71.209.6", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_abio_du1, _abio_slave, _abio_loner],
)

_attenuator0 = AHBTE(
    ip_addr="10.71.203.130",
    port=5000,
    attenuation_port_numbers=[15, 16, 13, 14],
    model="PA-16-16-6-127-0.5-B-S",
)

_ru_pdu = HBTE(addr="10.71.195.78", port_numbers=[4])

_ru0 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.33.130", username="rfsw", password="3Is6ezFJ7dFlB29cgs0yp3RCM3fUF1zNO1+6Z08tlAc="
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.77.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    attenuation_ports=[
        _attenuator0.attenuator_ports[15],
        _attenuator0.attenuator_ports[16],
    ],
    pdu_port=_ru_pdu.pdu_ports[4]
)

_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.56.2", username="rfsw", password="3Is6ezFJ7dFlB29cgs0yp3RCM3fUF1zNO1+6Z08tlAc="
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.77.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    attenuation_ports=[
        _attenuator0.attenuator_ports[13],
        _attenuator0.attenuator_ports[14],
    ]
)

_du1 = DU(airscale=Airscale(common_units=[_asil_du1]), f1_m_ip_addr="10.71.209.6", rus=[_ru0, _ru1])

_cbts1 = ClassicalBts(cu=_cu1, dus=[_du1], global_bts_id=10962, instance_id=1915)

_appserver_ssh = SshServiceDetails(
    addr="10.71.207.139",
    username="vrf3_sg5",
    password="vrf3@sg5",
    port="45015"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.207.139",
    iperf_path="/data/data/com.nokia.android.application/",
    port="45915",
    ports=["45115", "45125"],
)
_ue_pc_ssh = SshServiceDetails(
    addr="10.71.217.197", username="mn5gran", password="nokia123@"
)

_android = Android(
    ssh_connection_details=_ue_pc_ssh,
    serial_number="RFCR106L4CJ",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    iperf_directory="/data/data/com.nokia.android.application/",
    capabilities=["REAL_ANDROID_UE","samsung","UE_1"],
    service_call_attach="16",
)

_android1 = Android(
    ssh_connection_details=_ue_pc_ssh,
    serial_number="R5CT32189CK",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    iperf_directory="/data/data/com.nokia.android.application/",
    capabilities=["REAL_ANDROID_UE","samsung","UE_1"],
    service_call_attach="16",
)

_core = RealCore5G(mcc=262, mnc=3)

_pdu = FACOM(
    addr="10.71.195.69", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8], model="FACOM"
)

_asia = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.71.208.205", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
)

_smod_1 = Airscale(common_units=[_asia])

_rmod_1 = RU(ru_hw_group="", serial_number="EA203857361", pdu_port=_pdu.pdu_ports[5])

_enb_sbts_1 = RealEnb(
    airscale=_smod_1,
    rms=[_rmod_1],
    oam_ip=NetworkAddress("10.71.208.205"),
    global_bts_id=10082,instance_id=1964
)

_appserver = AppServer(iperf_details=_iperf)

tl = TestLine(
    test_pc=_test_pc1,
    gnbs=[_cbts1],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_QC_ASOER_AZHA_ENB",
    ues=[_android, _android1],
    pdus=_pdus,
    core=_core,
    enbs=[_enb_sbts_1],
    appserver=_appserver,
    attenuator=_attenuator0,
)

__all__ = ["tl"]

