import re
import os
import yaml
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.gnb.du import DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, ATEN, RRB, APC, Gude, HBTE
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
)
from taf.config.testline.enb import (
    Enb,
    SimEnb,
    RealEnb,
    LTEEmuEnb,
    PrismaEnb,
    DocomoEnb,
)

# added in taf.meta 5.4
from taf.config.testline.attenuator import AttenuationPort, TopYoung
from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.appserver import AppServer

__maintainer__ = "Chen Xiaodong"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_2_GMS <I_MN_5G_RAN_IV4_LINE_HZG_2@internal.nsn.com>"
)
__email__ = "xiaodong.d.chen@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# #host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.170", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_appserver_ssh = SshServiceDetails(
    addr="10.57.162.12", username="cmw_sg2", password="cm@2", port=54589
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.162.12",
    iperf_path="/usr/bin/iperf",
    port=54559,
)

_host_ssh = SshServiceDetails(
    addr="10.101.47.11", username="nokia5G", password="noki@123"
)

_iperf_details = IperfDataTransferDetails(
    ssh_connection_details=_host_ssh,
    network_interface_address="10.101.47.11",
    iperf_path="/cygdrive/c/iperf-2.0.8b-win64/iperf",
    port=52559,
)

_appserver = AppServer(_iperf)

# CI_Detail_UE_Type='Nokia FastMile 5G Gateway 3.1'
ue_config_path = os.path.join(_cfg_dir, "TestData/cpe.yml")
if os.path.isfile(ue_config_path):
    with open(ue_config_path) as f:
        _ue_read = f.read()
        qci_port = re.findall("(_iperf.*?port)", _ue_read)
        for item in qci_port:
            _ue_read = _ue_read.replace(item, str(eval(item)))
        _ue_config = yaml.load(_ue_read, Loader=yaml.FullLoader)
else:
    _ue_config = ""

# #RealEnb
_real_enb_pdu = HBTE(addr="2.2.2.2", port_numbers=[3])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="3.3.3.3", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[3],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb)

# #5GRU for classicalBTS
_ru1_pdu = HBTE(addr="4.4.4.4", port_numbers=[3])

_ru1 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.49", username="root", password="a2%FgSz3$fHmdusap354xujw7a"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.49", username="root", password="a2%FgSz3$fHmdusap354xujw7a"
    ),
    pdu_port=_ru1_pdu.pdu_ports[3],
    radio_type=RadioTypes.AEHB,
)

# #DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.57.224.196", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")

_gnb_pdu = HBTE(addr="10.101.48.190", port_numbers=[2])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[2],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru1], f1_m_ip_addr="10.57.224.196")

# #CU
_cu = CU(
    backhaul_site_oam_ip="10.57.224.196",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.224.196", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.224.196", username="Nemuadmin", password="nemuuser"
    ),
)

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, global_bts_id="23", instance_id="542")

_tl_cloud_topology = "CLOUD_5G_BB3"

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    tl_cloud_topology=_tl_cloud_topology,
    enbs=[_lte_real_enb],
    appserver=_appserver,
    ues=[_ue_config],
)
