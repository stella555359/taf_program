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
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, ATEN, RRB, APC, Gude, HBTE
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline import Enb, SimEnb, RealEnb, LTEEmuEnb, PrismaEnb, DocomoEnb
from taf.compatibility.configuration import TestlineWrapper

# added in taf.meta 5.4
from taf.config.testline.ue import (
    AirphoneCloud,
    Airphone,
    Prisma,
    TM500,
    Qualcomm,
    QualcommUeType,
    Android,
)
from taf.config.testline.attenuator import AttenuationPort, TopYoung
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)
from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.config.testline.attenuator import HBTE as ATTEN_HBTE

__maintainer__ = "Wang Yixiang"
__team__ = "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_01@internal.nsn.com"
__email__ = "yixiang.x.wang@nokia-sbell.com"

# common
__all__ = ["tl"]

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.180", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_attenuator = ATTEN_HBTE(
    ip_addr="10.101.51.210",
    port=5000,
    model="PA-16-16-6-127-0.5-B-S",
    attenuation_port_numbers=[149, 182, 157, 190, 223, 256],
)

# #Qualcomm
_appserver_ssh = SshServiceDetails(
    addr="10.57.162.4", username="mmw_sg1", password="mm@1", port="41507"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="XX.XX.XX.XX",
    iperf_path="/XX/XX/XX",
    port="41506",
)

# CI_Detail_UE_Type='Qualcomm'
_android_0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.101.47.193", username="nokia5G", password="noki@123"
    ),
    serial_number="34801d0",
    server_dir="C:/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "qct_dx50"],
    clear_server_files="yes",
    clear_logs="yes",
)


# 5GRU------------------------------------
_ru1_pdu = HBTE(addr="10.57.241.215", port_numbers=[4])
_ru2_pdu = HBTE(addr="10.57.241.215", port_numbers=[5])

_ru1_pdu_254_0 = HBTE(addr="10.101.45.246", port_numbers=[1])
_ru2_pdu_254_1 = HBTE(addr="10.101.45.246", port_numbers=[2])

_ru1 = RU(
    ru_hw_group="Below6GHZ",  # Above6GHZ or Below6GHZ
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_ru1_pdu.pdu_ports[4],
    radio_type=RadioTypes.AHEGA,
    serial_number="K9182603864",
    attenuation_ports=[
        _attenuator.attenuator_ports[157],
        _attenuator.attenuator_ports[190],
        _attenuator.attenuator_ports[223],
        _attenuator.attenuator_ports[256],
    ],
)


_ru2 = RU(
    ru_hw_group="Below6GHZ",  # Above6GHZ or Below6GHZ
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_ru2_pdu.pdu_ports[5],
    radio_type=RadioTypes.AWHQG,
    serial_number="EB1948R0251",
)

_ru_254_0 = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_ru1_pdu_254_0.pdu_ports[1],
    radio_type=RadioTypes.AHLOA,
    serial_number="BL2051G1TRB",
    attenuation_ports=[
        _attenuator.attenuator_ports[149],
        _attenuator.attenuator_ports[182],
    ],
)

_ru_254_1 = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_ru2_pdu_254_1.pdu_ports[2],
    radio_type=RadioTypes.AEHC,
    serial_number="L1205002770",
)

# #DU
_lmp_connection = SshServiceDetails(
    addr="10.101.51.211", username="toor4nsn", password="oZPS0POrRieRtu"
)

_lmp_connection_254 = SshServiceDetails(
    addr="10.101.51.202", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_254 = CapacityUnit(addr="192.168.253.20")

_capacity_unit = CapacityUnit(addr="192.168.253.20")

_gnb_pdu = HBTE(addr="10.57.241.157", port_numbers=[2])
_gnb_pdu_254 = HBTE(addr="10.101.45.240", port_numbers=[6])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[2],
)

_common_unit_254 = CommonUnit(
    lmp_connection=_lmp_connection_254,
    capacity_units=[_capacity_unit_254],
    pdu_port=_gnb_pdu_254.pdu_ports[6],
)

_airscale = Airscale(common_units=[_common_unit_0])
_airscale_254 = Airscale(common_units=[_common_unit_254])

_du_254 = DU(
    airscale=_airscale_254, rus=[_ru_254_0, _ru_254_1], f1_m_ip_addr="10.101.51.202"
)

_du = DU(airscale=_airscale, rus=[_ru1, _ru2], f1_m_ip_addr="10.101.51.211")

# CU
_cu = CU(
    backhaul_site_oam_ip="10.101.51.211",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.51.211", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.51.211", username="Nemuadmin", password="nemuuser"
    ),
)

_cu_254 = CU(
    backhaul_site_oam_ip="10.101.51.202",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.51.202", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.51.202", username="Nemuadmin", password="nemuuser"
    ),
)

# classicalbts------------------------------------------------
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=564, global_bts_id=564)

# classicalbts------------------------------------------------
_classical_bts_254 = ClassicalBts(
    dus=[_du_254], cu=_cu_254, instance_id=1170, global_bts_id=1170
)

# #cloud_topology------------------------------------------------
_tl_cloud_topology = "Refers to TAF UTE TL Type"

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts, _classical_bts_254],
    ues=[_android_0],
    tl_cloud_topology=_tl_cloud_topology,
    test_pcs=[_host],
    attenuators=[_attenuator],
)


# print(tl.enbs[0].global_bts_id)
# print(tl.gnbs[0].dus[0].rus[0].attenuation_ports[0].port_no)
# print(tl.ues[0].iperf_details.port)
# print (tl.gnbs[0].dus[0].rus[0].attenuation_ports[3].port_no)
# print (tl.gnbs[1].dus[0].f1_m_ip_addr)
