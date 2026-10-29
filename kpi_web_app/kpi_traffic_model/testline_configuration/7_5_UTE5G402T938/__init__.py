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

_attenuator = RadioRack(
    ip_addr="10.101.36.166",
    port="5000",
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8],
)

_ru_pdu = FACOM(addr="10.57.241.208", port_numbers=[1])

_ru = RU(
    ru_hw_group="Below6GHZ",  # Above6GHZ or Below6GHZ
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.48.2", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.48.2", username="root", password="umniedziala"
    ),
    serial_number="EA205055277",
    pdu_port=_ru_pdu.pdu_ports[1],
    radio_type=RadioTypes.AZQG,
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[6],
        _attenuator.attenuator_ports[7],
        _attenuator.attenuator_ports[8],
    ],
    signal_analyzer=None,
)

#########5G_gNB_Start##########
_gnb_pdu = FACOM(addr="10.57.241.205", port_numbers=[3])
_capacity_unit = CapacityUnit(addr="192.168.253.21")
_common_unit_0 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.68.88.235", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[3],
)
_airscale = Airscale(common_units=[_common_unit_0])
_cu = CU(
    backhaul_site_oam_ip="10.68.88.235",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.68.88.235", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.68.88.235", username="Nemuadmin", password="nemuuser"
    ),
)

# _du = DU(airscale=_airscale, rus=None)
_du = DU(airscale=_airscale, rus=[_ru], f1_m_ip_addr="10.68.88.235")
_cbts = ClassicalBts(cu=_cu, dus=[_du], instance_id=938, global_bts_id=938)
#########5G_gNB_Stop##########

#########4G_eNB_Start##########
_real_enb_pdu = FACOM(addr="10.57.241.205", port_numbers=[3])
_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.68.88.232", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[3],
)

_real_enb = Airscale(common_units=[_common_unit_2])
_lte_real_enb = RealEnb(airscale=_real_enb, rms=None)
#########4G_eNB_Stop##########

#########Testpc##########
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.146", username="ute", password="iW_K#8.ute%A10h0m0ra"
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
    addr="10.70.222.51",
    username="mmw_sg3",
    password="mm@3",
    port="43666",
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.70.222.51",
    iperf_path="/usr/bin/iperf",
    port="43667",
)


_appserver = AppServer(_iperf)

# Qualcomm
_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.68.86.152", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="420b36e2",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python310/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_UE", "askey"],
)

# for MTK UE, just a placeholder for now, TL config not supported yet.
_mtk_host_ssh = SshServiceDetails(
    addr="10.68.86.152", username="MN5GRAN", password="nokia123@"
)
_iperf_details_on_mtk = IperfDataTransferDetails(
    ssh_connection_details=_mtk_host_ssh,
    network_interface_address="10.70.222.51",
    iperf_path="iperf",
    port="43668",
)

_mtk = MediaTek(
    ssh_connection_details=_mtk_host_ssh,
    #                serial_number='2867e6fc',
    server_dir="C:/pyro_server",
    server_port=8080,
    edb_file_path=r"C:\MTK\sw\w19.41_1400/MDDB_MT6297_S00_VMOLY_W19_43_P3.EDB",
    #                python_path='C:/Python27/python.exe',
    imei="352569090028547",
    apn_url="wap2.nokia.com",
    #                qcat_path='C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe',
    #                diag_cfg_path='C:/pyro_server/DIAG.cfg',
    iperf_details=_iperf,
    capabilities=["REAL_MEDIATEK_UE", "askey"],
)
_mtk.inject_file = r"C:\MTK\ELT\nsa_tl923.tcl"


# inseego
_ue_config_path = os.path.join(_cfg_dir, "TestData/inseego.yml")
if os.path.isfile(_ue_config_path):
    with open(_ue_config_path) as f:
        _ue_inseego = f.read()
        qci_port = re.findall("(_iperf.*?port)", _ue_inseego)
        for item in qci_port:
            _ue_inseego = _ue_inseego.replace(item, str(eval(item)))
        _ue_config = yaml.safe_load(_ue_inseego)
else:
    _ue_config = ""


# Testline
tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    enbs=[_lte_real_enb],
    core=_lteemu,
    attenuator=_attenuator,
    appserver=_appserver,
    ues=[_ue_config, _mtk],
)
