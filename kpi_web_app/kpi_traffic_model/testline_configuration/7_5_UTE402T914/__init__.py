__maintainer__ = "Liu, Yuanyuan"
__team__ = "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_03@internal.nsn.com"  # TL owner's team
__email__ = "yuanyuan.2.liu@nokia-sbell.com"

import os
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline import (
    SshServiceDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.gnb import ClassicalBts, CU
from taf.config.testline.core import LTEEmuCore
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC
from taf.config.testline import RU, DU
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline import (
    Enb,
    SimEnb,
    RealEnb,
    RadioModule,
    LTEEmuEnb,
    PrismaEnb,
    DocomoEnb,
)
from taf.config.testline.attenuator import (
    AttenuationPort,
    RadioRack,
)  # added in taf.meta 5.4
from taf.config.testline.legacy import SCF
from taf.config.testline.ue import Android
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)

__all__ = ["tl"]

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

_attenuator = RadioRack(
    ip_addr="10.57.238.18", port="23", attenuation_port_numbers=[5, 6, 7, 8]
)

_ru_pdu = FACOM(addr="10.57.241.203", port_numbers=[1])

_ru = RU(
    ru_hw_group="Below6GHZ",  # Above6GHZ or Below6GHZ
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.55", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.55", username="user", password="pass"
    ),
    pdu_port=_ru_pdu.pdu_ports[1],
    radio_type=RadioTypes.AAHJ,
    attenuation_ports=[
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[6],
        _attenuator.attenuator_ports[7],
        _attenuator.attenuator_ports[8],
    ],
)
#########5G_gNB_Start##########

_gnb_pdu = FACOM(addr="10.57.241.205", port_numbers=[4])
_capacity_unit = CapacityUnit(addr="192.168.253.20")
_common_unit_0 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.230.10", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[4],
)
_airscale = Airscale(common_units=[_common_unit_0])
_cu = CU(
    backhaul_site_oam_ip="10.57.230.10",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.230.10", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.230.10", username="Nemuadmin", password="nemuuser"
    ),
)

# _du = DU(airscale=_airscale, rus=None)
_du = DU(airscale=_airscale, rus=[_ru], f1_m_ip_addr="10.57.230.10")
_cbts = ClassicalBts(cu=_cu, dus=[_du], instance_id=3133, global_bts_id=1)
#########5G_gNB_Stop##########

#########4G_eNB_Start##########
_real_enb_pdu = FACOM(addr="10.57.241.205", port_numbers=[4])
_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.238.23", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[4],
)

_real_enb = Airscale(common_units=[_common_unit_2])
_lte_real_enb = RealEnb(airscale=_real_enb, rms=None)
#########4G_eNB_Stop##########

#########Testpc##########
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.133", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)


#########LteEmu##########
_lteemu = LTEEmuCore(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.238.23", username="nokia", password="nokia123"
    ),
    dir_path="/home/nokia/LTEemu_core2_64_3252",
    cfg_filename="basic_wts_step1.cfg",
    mme_ip="",
    edaemon_port="22222",
    egate_port="9880",
)


_appserver_ssh = SshServiceDetails(
    addr="10.57.162.3", username="mmw_sg3", password="mm@3", port="43026"
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.162.3",
    iperf_path="/usr/bin/iperf",
    port="43027",
)
_qualcomm = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.130.220", username="CNHZ5GRAN1420+labadmin", password="L@badmin$"
    ),
    serial_number="62428a2",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="/cygdrive/c/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE"],
)

# Testline
tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    enbs=[_lte_real_enb],
    core=_lteemu,
    attenuator=_attenuator,
    tl_cloud_topology="",
    ues=[_qualcomm],
)
