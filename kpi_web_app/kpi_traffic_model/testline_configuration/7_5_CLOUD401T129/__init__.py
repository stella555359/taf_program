import os
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc
from taf.config.testline import RU, DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import MediaTek
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
from taf.config.testline.gnb.networkaddress import NetworkAddress  # add in taf.meta 5.4
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
from taf.config.testline.legacy import SCF

__maintainer__ = "Vivian Huang"
__team__ = "MN 5G RAN I&V 4 Pz HZG SG7"
__email__ = "I_MN_5G_RAN_IV4_LINE_HZG_7@internal.nsn.com"
__owner_email__ = "vivian.huang@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))
ue_config_path = os.path.join(_cfg_dir, "inseego_tl129.yml")

# ########Testpc##########
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.42", username="root", password="nokia123"
    )
)

# #######Iperf########
_appserver_ssh = SshServiceDetails(
    addr="10.57.163.52", username="root", password="nokia123"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="110.57.163.52",
    iperf_path="/system/bin",
)

# ########RealEnb##########
_real_enb_pdu = FACOM(addr="10.57.241.195", port_numbers=[2])
_common_unit_enb = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.237.117", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[2],
)

_real_enb = Airscale(common_units=[_common_unit_enb])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=None)

# #5GRU for classicalBTS
_ru_0_pdu = FACOM(addr="10.57.249.26", port_numbers=[1])

_ru_0 = RU(
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192,168.254.52", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.52", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru_0_pdu.pdu_ports[1],
    radio_type=RadioTypes.AEQC,
    signal_analyzer=None,
)

# gnb for classiclBTS
_gnb_asik_ip = "10.57.236.233"

# #DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr=_gnb_asik_ip, username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.22")

_gnb_pdu = FACOM(addr="10.57.241.165", port_numbers=[1])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[1],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru_0], f1_m_ip_addr=_gnb_asik_ip)

# ########CU##########

_f1m = NetworkAddress(v4="10.57.236.254", v6="xxxx", vlan_id=1)
_f1c = NetworkAddress(v4="10.57.236.254", v6="xxxx", vlan_id=2)
_f1u = NetworkAddress(v4="10.57.236.254", v6="xxxx", vlan_id=3)
_x2c = NetworkAddress(v4="10.57.236.254", v6="xxxx", vlan_id=1)
_x2u = NetworkAddress(v4="10.57.236.254", v6="xxxx", vlan_id=2)
_s1c = NetworkAddress(v4="10.57.236.254", v6="xxxx", vlan_id=1)
_s1u = NetworkAddress(v4="10.57.236.254", v6="xxxx", vlan_id=2)

_cu = CU(
    backhaul_site_oam_ip=_gnb_asik_ip,
    oam_ssh_connection_details=SshServiceDetails(
        addr=_gnb_asik_ip, username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr=_gnb_asik_ip, username="Nemuadmin", password="nemuuser"
    ),
    f1m=_f1m,
    f1c=_f1c,
    f1u=_f1u,
    x2c=_x2c,
    x2u=_x2u,
    s1c=_s1c,
    s1u=_s1u,
)

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=129)

# with open(ue_config_path) as f:
#    ue_config = yaml.load(f)

# ########TestLine##########
_tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_classical_bts],
    tl_cloud_topology="classical",
    enbs=[_lte_real_enb],
)

tl = _tl
