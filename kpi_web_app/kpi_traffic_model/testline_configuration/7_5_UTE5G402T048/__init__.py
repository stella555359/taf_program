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
from taf.config.testline import RU, DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC
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


__maintainer__ = "Cui Lingxue"
__team__ = (
    "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_01_GMS <I_NSB_MN_5GSC_MMW_SC_PZ_HZ_01@internal.nsn.com>"
)
__email__ = "lingxue.cui@nokia-sbell.com"

# common
__all__ = ["tl"]

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.175", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# #Qualcomm
_appserver_ssh = SshServiceDetails(
    addr="10.57.162.4", username="mmw_sg1", password="mm@1", port="41096"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.162.4",
    iperf_path="iperf",
    port="41097",
)

_android_0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.218.145", username="nokia5G", password="noki@123"
    ),
    serial_number="RFCR103WRMT",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE"],
)

# 5GRU------------------------------------
# add 2 more 5g ru info
_ru_pdu = FACOM(addr="10.71.195.166", port_numbers=[3, 5])

_ru1 = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_ru_pdu.pdu_ports[5],
    radio_type=RadioTypes.AHLOA,
    serial_number="BL2048G1RC7",
)

_ru2 = RU(
    ru_hw_group="Below6GHZ",
    default_ssh_connection_details=SshServiceDetails(
        addr="7.7.7.7", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(addr="8.8.8.8", username="user", password="pass"),
    pdu_port=_ru_pdu.pdu_ports[3],
    radio_type=RadioTypes.AEHC,
    serial_number="L1205002769",
)

# #DU
_lmp_connection = SshServiceDetails(
    addr="10.71.210.3", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")

_gnb_pdu = FACOM(addr="xx.xx.xx.xx", port_numbers=[5])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[5],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru1], f1_m_ip_addr="10.71.210.3")

# CU
_cu = CU(
    backhaul_site_oam_ip="10.71.210.3",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.210.3", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.210.3", username="Nemuadmin", password="nemuuser"
    ),
)

# classicalbts------------------------------------------------
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=10150, global_bts_id=10150)

# #cloud_topology------------------------------------------------
_tl_cloud_topology = "Refers to TAF UTE TL Type"

_attenuator = []

# #realcore4g
_mme_oam_ssh_connection_details = SshServiceDetails(
    addr="x.x.x.x", username="ute1", password="ute1"
)
_s1_address = NetworkAddress(v4="xxx.xxx.xx.xx", v6="xxx:xx::xxx", vlan_id=1)
_mme = MME(oam_ssh_connection_details=_mme_oam_ssh_connection_details, s1=_s1_address)
_real_4g_core_details = RealCore4GDetails(mme=_mme)

# #realcore5g
_amf_oam_ssh_connection_details = SshServiceDetails(
    addr="x.x.x.x", username="ute1", password="ute1"
)
_n2_address = NetworkAddress(v4="10.110.66.198")
_amf = AMF(oam_ssh_connection_details=_amf_oam_ssh_connection_details, n2=_n2_address)
_real_5g_core_details = RealCore5GDetails(amf=_amf)

_realcore = RealCore(
    four_g=_real_4g_core_details,
    five_g=_real_5g_core_details,
    mcc="310",
    mnc="260",
    pdn=None,
)

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    ues=[_android_0],
    tl_cloud_topology=_tl_cloud_topology,
    test_pcs=[_host],
    appserver=_appserver_ssh,
    attenuators=[_attenuator],
    core=_realcore,
)
