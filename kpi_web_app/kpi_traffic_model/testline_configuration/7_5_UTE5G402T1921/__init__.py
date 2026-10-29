__maintainer__ = "ChenXu"
__team__ = "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_05_GMS"
__email__ = "xu.2.chen@nokia-sbell.com"

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
from taf.config.testline.pdu import HBTE, PduPort
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
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

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

_test_pc1 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.177.117",
        username="ute",
        password="iW_K#8.ute%A10h0m0ra",
    )
)



# pdu setting is adapted because local tl gnb1/gnb2/ap may be connected to different PDUs
_pdu_gnb1 = HBTE(
    port_numbers=[8],
    addr="10.71.195.80",
)

_pdu_ap1 = HBTE(
    port_numbers=[2],
    addr="10.71.195.80",
)



_pdus = [_pdu_gnb1, _pdu_ap1]

_cu1 = CU(
    backhaul_site_oam_ip="10.71.209.13",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.209.13", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.209.13", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(v4="10.0.1.2", vlan_id=2398),
    x2u=NetworkAddress(v4="10.0.1.2", vlan_id=2398),
    s1u=NetworkAddress(v4="10.0.1.2", vlan_id=2398),
    ngu=NetworkAddress(v4="10.0.1.2", vlan_id=2398),
)

_abip_du1 = CapacityUnit(addr="192.168.253.20")
_abip_slave = CapacityUnit(addr="192.168.253.21")
_abip_loner = CapacityUnit(addr="192.168.253.22")

_asim_du1 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.71.209.13", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_abip_du1, _abip_slave, _abip_loner],
)

_attenuator = AHBTE(
    ip_addr="10.71.203.138",
    port=5000,
    attenuation_port_numbers=[13, 14, 15, 16],
    model="PA-16-16-6-127-0.5-B-S",
)

_ru0 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2", username="rfsw", password="3Is6ezFJ7dFlB29cgs0yp3RCM3fUF1zNO1+6Z08tlAc="
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.77.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    attenuation_ports=[
        _attenuator.attenuator_ports[15],
        _attenuator.attenuator_ports[16],
    ],

)

_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2", username="rfsw", password="3Is6ezFJ7dFlB29cgs0yp3RCM3fUF1zNO1+6Z08tlAc="
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.77.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    attenuation_ports=[
        _attenuator.attenuator_ports[13],
        _attenuator.attenuator_ports[14],
    ],


)

_du1 = DU(airscale=Airscale(common_units=[_asim_du1]), rus=[_ru0,_ru1], f1_m_ip_addr="192.168.255.129")

_cbts1 = ClassicalBts(cu=_cu1, dus=[_du1], global_bts_id=11539, instance_id=1921)


_abil_master = CapacityUnit(addr="fsp-5a")
_abil_slave = CapacityUnit(addr="fsp-5b")
_abil_loner = CapacityUnit(addr="192.168.253.22")

_common_unit = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.71.208.230", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_abil_master, _abil_slave, _abil_loner],
)

_airscale = Airscale([_common_unit])

# #CU
_cu = CU(
    backhaul_site_oam_ip="10.71.208.230",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.208.230", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.208.230", username="Nemuadmin", password="nemuuser"
    ),
)

_ru0 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.56.2", username="rfsw", password="3Is6ezFJ7dFlB29cgs0yp3RCM3fUF1zNO1+6Z08tlAc="
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.77.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
)

_du = DU(airscale=_airscale, rus=[_ru0], f1_m_ip_addr="10.71.208.230")

_classical_bts = ClassicalBts(cu=_cu, dus=[_du], global_bts_id=10959, instance_id=1912)

_core = RealCore5G(mcc=460, mnc=2)

_abia = CapacityUnit(addr="192.168.253.20")

_asia = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.71.209.13", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_abia],
)

_lteenb = RealEnb(
    airscale=Airscale(common_units=[_asia]),
    x2_link_addr=NetworkAddress(
        v4="10.71.208.203",
        routing=RoutingInformation(gateway="10.71.208.193", ip_prefix_length=27),
    ),
    global_bts_id=10080,
    instance_id=1968,
)

_ue_pc_ssh = SshServiceDetails(
    addr="10.71.217.247", username="mn5gran", password="nokia123@"
)

_appserver_ssh = SshServiceDetails(
    addr="10.71.207.139", username="vrf3_sg5", password="vrf3@sg5", port="45821"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.207.139",
    port="45921",
)

_samsung1 = Android(
    ssh_connection_details=_ue_pc_ssh,
    serial_number="RFCR40MJBXF",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    iperf_directory="/data/data/com.nokia.android.application/",
    capabilities=["REAL_ANDROID_UE", "samsung", "UE_1"],
    service_call_attach="16",
)

_samsung2 = Android(
    ssh_connection_details=_ue_pc_ssh,
    serial_number="RFCRA03BN8M",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    iperf_directory="/data/data/com.nokia.android.application/",
    capabilities=["REAL_ANDROID_UE", "samsung", "UE_1"],
    service_call_attach="16",
)

_appserver = AppServer(iperf_details=_iperf)



tl = TestLine(
    test_pc=_test_pc1,
    test_pcs=[_test_pc1],
    gnbs=[_cbts1, _classical_bts],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_QC_ASIBR_ABIN1_2xAHLOA_ENB",
#    tl_cloud_topology="MP_LOOO_LOOO_LOOO",
    ues=[_samsung1, _samsung2],
    pdus=_pdus,
    core=_core,
    enbs=[_lteenb],
    appserver=_appserver,
    attenuator=_attenuator,
)

__all__ = ["tl"]

