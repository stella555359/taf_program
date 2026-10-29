import os
import yaml
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
from taf.config.testline.testpc import TestPc
from taf.config.testline.core import EPCSim, LTEEmuCore, PrismaCore
from taf.config.testline import RU, DU, RoutingInformation
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, HBTE
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import AirphoneCloud, Airphone, Prisma, TM500, Android
from taf.config.testline import Enb, SimEnb, RealEnb, LTEEmuEnb, PrismaEnb, DocomoEnb
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.nms import Netact
from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.config.testline.dcap import DcapRnD, DcapBasic
from taf.config.testline.gnb.du import Cablink, Endpoint

__maintainer__ = "lin zhe"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_8_GMS <I_MN_5G_RAN_IV4_LINE_HZG_8@internal.nsn.com>"
)
__email__ = "zhe.1.lin@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# testPc(taf)
# _host = TestPc(
#     default_ssh_connection_details=SshServiceDetails(
#         addr="10.57.155.90", username="ute", password="iW_K#8.ute%A10h0m0ra"
#     )
# )
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.70.230.162", username="ute", password="ute"
    )
)

_lss = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.84", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_dcap_1 = DcapBasic(
    connection_details=HttpConnectionDetails(
        addr="10.101.60.40", port="443", username="dcapuser", password="dcapadmin!"
    )
)
_dcap_2 = DcapBasic(
    connection_details=HttpConnectionDetails(
        addr="10.101.60.41", port="443", username="dcapuser", password="dcapadmin!"
    )
)

# 5GRU for classicalBTS

# PB for RU
_ru_1_pdu = HBTE(addr="10.101.45.172", port_numbers=[4])
_ru_1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="a2%FgSz3$fHmdusap354xujw7a"
    ),
    # lmp_connection=SshServiceDetails(addr='10.68.86.50', username='root', password='nokia123'),
    pdu_port=_ru_1_pdu.pdu_ports[4],
)

# gNB LMP IP
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
# ABIL internal ip
_capacity_unit = CapacityUnit(addr="192.168.253.20")
# gNB PB
_gnb_pdu = HBTE(addr="10.101.45.170", port_numbers=[5])
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[5],
)
_airscale = Airscale(common_units=[_common_unit_0])

_ru_cablinks = [
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=1),
        target=Endpoint(unit=_ru_1, label="SFP", port_id=1),
    ),
]

_du = DU(
    airscale=_airscale,
    rus=[_ru_1],
    f1_m_ip_addr="10.101.50.233",
    cablinks=_ru_cablinks,
)

# gNB OAM M-plane IP
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.101.50.233",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.101.50.225", ip_prefix_length=27),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.50.233", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.50.233", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.101.50.233",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.101.50.225", ip_prefix_length=27),
    ),
    x2u=NetworkAddress(
        v4="10.101.50.233",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.101.50.225", ip_prefix_length=27),
    ),
    s1u=NetworkAddress(
        v4="10.101.50.233",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.101.50.225", ip_prefix_length=27),
    ),
)

# ##cloud_topology
# _tl_cloud_topology = "CLOUD_5G_BB3"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, global_bts_id=856, instance_id=856)

# QualComm UE
_appserver_ssh = SshServiceDetails(
    addr="10.57.162.10", username="cmw_sg7", password="Nokia07!", port="57856"
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.162.10",
    iperf_path="/usr/bin/iperf",
    port=57856,
)

# CI_Detail_UE_Type='Huawei Honor 30s'
_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.68.86.102", username="nokia5G", password="noki@123"
    ),
    serial_number="9EQUT20721003466",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "HONOR"],
)

# Askey
ue_config_path = os.path.join(_cfg_dir, "TestData/askey.yml")
if os.path.isfile(ue_config_path):
    with open(ue_config_path) as f:
        ue_config = yaml.safe_load(f)
else:
    ue_config = ""

##cloud_topology
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ASKEY_SA_ASOEB1_3xAZQJ"

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    #    enbs=[_lte_real_enb],
    ues=[ue_config],
    tl_cloud_topology=_tl_cloud_topology,
    test_pcs=[_lss, _dcap_1, _dcap_1, _dcap_2],
)
