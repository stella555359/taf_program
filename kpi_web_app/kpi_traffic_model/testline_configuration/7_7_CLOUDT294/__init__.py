__maintainer__ = "5G SC QT"
__team__ = "5G QT"
__email__ = "I_SC_5G_QT_KRK@internal.nsn.com"

import os
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.ue import Qualcomm
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    SCRadioConnectionDetails,
    TelnetConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline import SC5GRadio
from taf.config.testline import RealEnb
from taf.config.testline.core import EPCSim
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.pdu import PduPort, ATEN


_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7_7_cloudt294.sc5g.krk-lab.nsn-rdnet.net", username="ute", password="ute"
    )
)

_cu = CU(
    backhaul_site_oam_ip="192.168.255.129",  # 10.83.183.44
    oam_ssh_connection_details=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="192.168.255.129", username="Nemuadmin", password="nemuuser"
    ),
)

_du_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_du_capacity_unit = CapacityUnit(
    addr="fsp1_c", hardware_type="ABIL", hardware_version="M02"
)

_du_common_unit = CommonUnit(
    lmp_connection=_du_lmp_connection,
    capacity_units=[_du_capacity_unit],
    hardware_type="ASIK",
    hardware_version="M01",
)


_ru = SC5GRadio(
    ru_hw_group="ASIR-HUB",
    sc_radio_connection_details=SCRadioConnectionDetails(
        ssh_connection_details=SshServiceDetails(
            addr="192.168.255.129",
            username="toor4nsn",
            password="oZPS0POrRieRtu",
            proxy=SshServiceDetails(
                addr="sc5g-hub-067.sc5g.krk-lab.nsn-rdnet.net",
                username="ute",
                password="ute",
            ),
        ),
        telnet_connection_details=TelnetConnectionDetails(
            addr="tty-server", username="toor4nsn", password="oZPS0POrRieRtu"
        ),
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=PduPort(pdu=ATEN(addr="1.1.1.1", port_numbers=[1, 2]), port_no=1),
)

_airscale = Airscale(common_units=[_du_common_unit])

_du = DU(airscale=_airscale, rus=[_ru])

_bts = ClassicalBts(cu=_cu, dus=[_du])

_core = EPCSim(
    default_ssh_connection_details=SshServiceDetails(
        addr="sc5g-enb-089.sc5g.krk-lab.nsn-rdnet.net", username="ute", password="ute"
    ),
    dir_path="/home/ute/epcsim/",
    cfg_filename="sim.cfg",
    mme_ip="10.253.164.89",
    mcc=244,
    mnc=8,
    tac=1024,
    edaemon_port=60002,
    egate_port=60001,
)

_lteenb = RealEnb(airscale=_du, x2_link_addr="10.83.178.244")

# _ue_pc_ssh = SshServiceDetails('10.83.179.91', 'user-lab0', password='Bts2003')
# _iperf_pc_ssh = SshServiceDetails('10.83.178.2445', 'ute', password='ute')
# _android_iperf = IperfDataTransferDetails(_iperf_pc_ssh, '40.1.1.254', None)
# _android_ue1 = Android(ssh_connection_details=_ue_pc_ssh,
#                       serial_number='f57e6b7d', #LG V50
#                       server_dir='/cygdrive/c/pyro_server/ta_ue_plugin_android/ue',
#                       python_path='C:/Python27/python.exe',
#                       qcat_path='C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe',
#                       diag_cfg_path='C:/pyro_server/DIAG.cfg',
#                       iperf_details=_android_iperf)

# _qualcomm_ue = os.environ["ABSTRACT_LIB_CONFIG"] = (os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ue_config_cv294.yml'))


tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_bts],
    enbs=[_lteenb],
    # ues=[_qualcomm_ue],
    core=_core,
    tl_cloud_topology="CLOUD_5G_CLASSICAL_ASIR_ASIKM01L_ABILM02B1",
)

__all__ = ["tl"]
