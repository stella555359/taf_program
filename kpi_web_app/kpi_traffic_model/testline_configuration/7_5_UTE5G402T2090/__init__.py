__maintainer__ = "Liu, Yuanyuan"
__team__ = "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_03@internal.nsn.com"  # TL owner's team
__email__ = "yuanyuan.2.liu@nokia-sbell.com"
import re
import os
import yaml
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
from taf.config.testline.pdu import HBTE as pdu_HBTE
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
    HBTE,
)  # added in taf.meta 5.4
from taf.config.testline.legacy import SCF

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


from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)
from taf.config.testline.appserver import AppServer

# common
__all__ = ["tl"]


_cfg_dir = os.path.dirname(os.path.abspath(__file__))

_attenuator = HBTE(
    ip_addr="10.57.230.4",
    port="5000",
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6,7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    model="PA-16-16-6-127-0.5-B-S",                              
)
_attenuator_2 = HBTE(
    ip_addr="10.57.226.198",
    port="5000",
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6,
                              7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
)

_ru_pdu_1 = pdu_HBTE(addr="10.57.176.95", port_numbers=[1, 2, 3, 4, 5, 6])
_ru_pdu_2 = pdu_HBTE(addr="10.57.176.91", port_numbers=[1, 2, 3, 4, 5, 6])
_ru_pdu_3 = pdu_HBTE(addr="10.57.176.93", port_numbers=[1, 2, 3, 4, 5, 6])
_ru_1 = RU(
    ru_hw_group="Below6GHZ",  # Above6GHZ or Below6GHZ
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.48.2", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.48.2", username="root", password="umniedziala"
    ),
    serial_number="EA205055277",
    pdu_port=_ru_pdu_2.pdu_ports[3],
    radio_type=RadioTypes.FXEB,
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[6],
        _attenuator.attenuator_ports[7],
        _attenuator.attenuator_ports[8],
        _attenuator.attenuator_ports[9],
        _attenuator.attenuator_ports[10],
        _attenuator.attenuator_ports[11],
        _attenuator.attenuator_ports[12],
        _attenuator.attenuator_ports[13],
        _attenuator.attenuator_ports[14],
        _attenuator.attenuator_ports[15],
        _attenuator.attenuator_ports[16]
    ],
    signal_analyzer=None,
)

_ru_2 = RU(
    ru_hw_group="cmw",
    pdu_port=_ru_pdu_1.pdu_ports[5],
    radio_type=RadioTypes.FXEB,
)

_ru_3 = RU(
    ru_hw_group="cmw",
    pdu_port=_ru_pdu_1.pdu_ports[6],
    # radio_type=RadioTypes.AEQW,
)

_ru_4 = RU(
    ru_hw_group="cmw",
    pdu_port=_ru_pdu_1.pdu_ports[4],
    # radio_type=RadioTypes.AEQW,
)

_ru_5 = RU(
    ru_hw_group="cmw",
    pdu_port=_ru_pdu_1.pdu_ports[2],
    radio_type=RadioTypes.AZNA,
)

_ru_6 = RU(
    ru_hw_group="cmw",
    pdu_port=_ru_pdu_2.pdu_ports[1],
    radio_type=RadioTypes.AZNA,
)

_ru_8 = RU(
    ru_hw_group="cmw",
    pdu_port=_ru_pdu_3.pdu_ports[4],
    radio_type=RadioTypes.AZNA,
)

_ru_7 = RU(
    ru_hw_group="cmw",
    pdu_port=_ru_pdu_2.pdu_ports[2],
    radio_type=RadioTypes.AZNA,
)

_ru_9= RU(
    ru_hw_group="cmw",
    #pdu_port=_ru_pdu_3.pdu_ports[3],
    # radio_type=RadioTypes.AEQW,
)

_ru_10 = RU(
    ru_hw_group="cmw",
    #pdu_port=_ru_pdu_3.pdu_ports[2],
    radio_type=RadioTypes.FRGT,
)
_ru_11 = RU(
    ru_hw_group="cmw",
    #pdu_port=_ru_pdu_2.pdu_ports[1],
    radio_type=RadioTypes.AZNA,
)

_ru_12 = RU(
    ru_hw_group="cmw",
    #pdu_port=_ru_pdu_2.pdu_ports[2],
    radio_type=RadioTypes.AZNA,
)

_ru_13 = RU(
    ru_hw_group="cmw",
    #pdu_port=_ru_pdu_3.pdu_ports[4],
    radio_type=RadioTypes.AZNA,
)

_ru_14 = RU(
    ru_hw_group="cmw",
    #pdu_port=_ru_pdu_1.pdu_ports[2],
    radio_type=RadioTypes.AZNA,
)

_ru_15= RU(
    ru_hw_group="cmw",
    pdu_port=_ru_pdu_3.pdu_ports[3],
    # radio_type=RadioTypes.AEQW,
)

_ru_16 = RU(
    ru_hw_group="cmw",
    pdu_port=_ru_pdu_3.pdu_ports[2],
    radio_type=RadioTypes.FRGT,
)

_ru_17 = RU(
    ru_hw_group="cmw",
    pdu_port=_ru_pdu_3.pdu_ports[1],
    radio_type=RadioTypes.FRGT,
)

#########5G_gNB_Start##########
_gnb_pdu = pdu_HBTE(addr="10.57.176.94", port_numbers=[4])
_capacity_unit = CapacityUnit(addr="192.168.253.20")
_common_unit_0 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.226.196", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[4],
)
_airscale = Airscale(common_units=[_common_unit_0])
_cu = CU(
    backhaul_site_oam_ip="10.57.226.196",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.226.196", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.226.196", username="Nemuadmin", password="nemuuser"
    ),
)

# _du = DU(airscale=_airscale, rus=None)
_du = DU(airscale=_airscale, rus=[_ru_1, _ru_2, _ru_3, _ru_4, _ru_5, _ru_6, _ru_7, _ru_8,
                                  _ru_9, _ru_10, _ru_11, _ru_12, _ru_13, _ru_14, _ru_15, _ru_16, _ru_17],
         f1_m_ip_addr="10.57.226.196")
_cbts = ClassicalBts(cu=_cu, dus=[_du], instance_id=10600, global_bts_id=2090)
#########5G_gNB_Stop##########

#########4G_eNB_Start##########
_real_enb_pdu = FACOM(addr="10.57.176.95", port_numbers=[1])
_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.226.196", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[1],
)

_real_enb = Airscale(common_units=[_common_unit_2])
_lte_real_enb = RealEnb(airscale=_real_enb, rms=None)
#########4G_eNB_Stop##########

#########Testpc##########
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.177.26", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)


#########LteEmu##########
_lteemu = LTEEmuCore(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.68.88.232", username="nokia", password="nokia123"
    ),
    dir_path="/home/nokia/LTEemu_core2_64_3252",
    cfg_filename="basic_wts_step1.cfg",
    mme_ip="",
    edaemon_port="22222",
    egate_port="9880",
)


_appserver_ssh = SshServiceDetails(
    addr="10.57.191.235",
    username="vrf3_sg3",
    password="vrf3@sg3",
    port="46666",
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.235",
    iperf_path="/usr/bin/iperf",
    port="46667",
)


_appserver = AppServer(_iperf)

# Qualcomm
_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.33", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="9f435829",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python310/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_UE", "qct_dx50"],
)

_appserver_ssh = SshServiceDetails(
    addr="10.57.191.235", username="vrf3_sg3", password="vrf3@sg3", port="43703"
)

# Testline
tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    enbs=[_lte_real_enb],
    core=_lteemu,
    appserver=_appserver,
    attenuator=_attenuator,
    ues=[_android],
)
