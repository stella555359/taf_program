__maintainer__ = "Adam Moszczynski"
__team__ = "I_MN_5G_SC_PZ_SC_5G_VRF_GMS"
__email__ = "I_MN_5G_SC_PZ_SC_5G_VRF@internal.nsn.com"
__owner_email__ = "adam.1.moszczynski@nokia.com"

import os

from taf.config.testline.testpc import TestPc
from taf.config.testline import RU, DU
from taf.config.testline.pdu import ATEN, PduPort
from taf.config.testline.ue import Android
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import ClassicalBts, CU
from taf.config.testline.airscale import CommonUnit, CapacityUnit, Airscale
from taf.config.testline.enb import RealEnb
from taf.config.testline.core import EPCSim
from taf.config.testline.attenuator import AttenuationPort, JFW
from taf.config.testline.pdu import PduPort, ATEN
from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    SCRadioConnectionDetails,
    TelnetConnectionDetails,
    IperfDataTransferDetails,
)

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7_7_CLOUDT283.sc5g.krk-lab.nsn-rdnet.net", username="ute", password="ute"
    )
)

_ru_pdu = ATEN(addr="0.0.0.0", port_numbers=[1])

_ru_1 = RU(
    ru_hw_group="hw_group",
    radio_type="AHLOA",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.253.52", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="TO_UPDATE", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru_pdu.pdu_ports[1],
)

_ru_2 = RU(
    ru_hw_group="hw_group",
    radio_type="AHLOA",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.253.53", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="TO_UPDATE", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru_pdu.pdu_ports[1],
)

_ru_3 = RU(
    ru_hw_group="hw_group",
    radio_type="AHLOA",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.253.54", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="TO_UPDATE", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru_pdu.pdu_ports[1],
)

_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(v4="10.83.183.33"),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.83.183.33", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.83.183.33", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(v4="10.83.183.33"),
    x2u=NetworkAddress(v4="10.83.183.33"),
    s1u=NetworkAddress(v4="10.83.183.33"),
)

_du_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_du_capacity_unit = CapacityUnit(
    # addr='fsp1_c',
    addr="192.168.253.20",
    hardware_type="ABIL",
    hardware_version="A101B1",
)

_du_common_unit = CommonUnit(
    lmp_connection=_du_lmp_connection,
    capacity_units=[_du_capacity_unit],
    hardware_type="ASIK",
    pdu_port=PduPort(pdu=ATEN(addr="1.1.1.1", port_numbers=[1]), port_no=1),
)

_airscale = Airscale(common_units=[_du_common_unit])

_du = DU(airscale=_airscale, rus=[_ru_1, _ru_2, _ru_3], f1_m_ip_addr="10.83.183.33")

_bts = ClassicalBts(cu=_cu, dus=[_du])

_core = EPCSim(
    default_ssh_connection_details=SshServiceDetails(
        addr="7_7_cloudt283.sc5g.krk-lab.nsn-rdnet.net", username="ute", password="ute"
    ),
    dir_path="/epcsim",
    cfg_filename="sim2.cfg",
    mme_ip="10.253.165.33",
    mcc=244,
    mnc=8,
    tac=1024,
    edaemon_port=12345,
    egate_port=60001,
)

_lteenb = NetworkAddress(v4="10.83.183.33")
# RealEnb(airscale=_airscale, x2_link_addr='10.83.183.33')

_ue_pc_ssh = SshServiceDetails("10.83.179.97", "user-lab0", password="Bts2003")
_iperf_pc_ssh = SshServiceDetails(
    "SC5G-eNB-188.sc5g.krk-lab.nsn-rdnet.net", "ute", password="ute"
)
_android_iperf = IperfDataTransferDetails(
    _iperf_pc_ssh, "40.1.1.254", "/data/data/com.magicandroidapps.iperf/bin/iperf"
)
_android_ue = Android(
    ssh_connection_details=_ue_pc_ssh,
    serial_number="R3CN105QZ0H",  # Qualcomm 8150/SDX55
    server_dir="/cygdrive/c/pyro_server/ta_ue_plugin_android/ue",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    dmc_path="c:/software/sdx55.dmc",
    diag_com=65,
    iperf_details=_android_iperf,
    capabilities=["REAL_ANDROID_UE"],
)

_attenuator = JFW(ip_addr="10.83.176.36", port=3001, attenuation_port_numbers=[1, 2])

tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_bts],
    enbs=[_lteenb],
    core=_core,
    ues=[_android_ue],
    attenuator=_attenuator,
    tl_cloud_topology="CLOUD_5G_CLASSICAL_QC_ASIKL_ABILB1_AHLOA_ENB",
)

__all__ = ["tl"]
