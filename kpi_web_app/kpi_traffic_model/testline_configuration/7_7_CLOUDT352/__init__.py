__maintainer__ = "Mateusz Pajor"
__team__ = "I_5G_SC_MMW_SIM_SC_SW_ENG_KRK_TEST"
__email__ = "I_5G_SC_MMW_SIM_SC_SW_ENG_KRK_TEST@internal.nsn.com"
__owner_email__ = "mateusz.pajor@nokia.com"

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
        addr="10.83.179.225", username="ute", password="ute"
    )
)

_ru_pdu = ATEN(addr="0.0.0.0", port_numbers=[1])

# TO DO
_ru = RU(
    ru_hw_group="hw_group",
    radio_type="AHFIB",
    default_ssh_connection_details=SshServiceDetails(
        addr="TO_UPDATE", username="root", password="TO_UPDATE"
    ),
    lmp_connection=SshServiceDetails(
        addr="TO_UPDATE", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru_pdu.pdu_ports[1],
)

_cu = CU(
    backhaul_site_oam_ip="10.83.183.102",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.83.183.102", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.83.183.102", username="Nemuadmin", password="nemuuser"
    )
    # x2c=NetworkAddress(v4='10.83.183.33', vlan_id=504),
    # x2u=NetworkAddress(v4='10.83.183.33', vlan_id=504),
    # s1u=NetworkAddress(v4='10.83.183.33', vlan_id=504)
)

_du_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)


_du_capacity_unit = CapacityUnit(
    addr="fsp1_c", hardware_type="ABIL", hardware_version="B101"
)

_du_common_unit = CommonUnit(
    lmp_connection=_du_lmp_connection,
    capacity_units=[_du_capacity_unit],
    hardware_type="ASIK",
)

_airscale = Airscale(common_units=[_du_common_unit])

_du = DU(airscale=_airscale, rus=[_ru])

_bts = ClassicalBts(cu=_cu, dus=[_du])

_core = EPCSim(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.253.165.102", username="ute", password="ute"
    ),
    dir_path="/opt/iphy/latest",
    cfg_filename="sim.cfg",  # epcsim.cfg
    mme_ip="10.253.165.102",  # 10.253.165.33
    mcc=244,
    mnc=8,
    tac=1024,
    edaemon_port=12345,
    egate_port=60001,
)

# _lteenb = RealEnb(airscale=_airscale, x2_link_addr='10.83.183.33')

# _ue_pc_ssh = SshServiceDetails('10.83.179.97', 'user-lab0', password='Bts2003')
# _iperf_pc_ssh = SshServiceDetails('SC5G-eNB-188.sc5g.krk-lab.nsn-rdnet.net', 'ute', password='ute')
# _android_iperf = IperfDataTransferDetails(_iperf_pc_ssh, '40.1.1.254', '/data/data/com.magicandroidapps.iperf/bin/')
# _android_ue = Android(ssh_connection_details=_ue_pc_ssh,
#                      serial_number='2b85c7ad',  # Qualcomm 8150/SDX55
#                      server_dir='/cygdrive/c/pyro_server/ta_ue_plugin_android/ue',
#                      python_path='C:/Python27/python.exe',
#                      qcat_path='C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe',
#                      diag_cfg_path='C:/pyro_server/DIAG.cfg',
#                      iperf_details=_android_iperf)

tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_bts],
    # enbs=[_lteenb],
    core=_core,
    tl_cloud_topology="CLOUD_5G_CLASSICAL_ASIKR_ABILB1_AHFIB_SA",
    # ues=[_android_ue]
)


__all__ = ["tl"]
