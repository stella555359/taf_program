__maintainer__ = "Liqin Yang"  # TL owner name
__team__ = "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_05_GMS <I_NSB_MN_5GSC_MMW_SC_PZ_HZ_05@internal.nsn.com>"  # TL owner's team
__email__ = "liqin.yang@nokia-sbell.com"  # TL owner's email

import os
from taf.config.testline.testline import TestLine
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.testpc import TestPc
from taf.config.testline.attenuator import HBTE as AHBTE
from taf.config.testline.pdu import Gude, HBTE, TopYoung
from taf.config.testline.pdu import ATEN, PduPort
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.appserver import AppServer
from taf.config.testline.gnb import ClassicalBts, CU
from taf.config.testline import DU, RU
from taf.config.testline.core import RealCore5G
from taf.config.testline import RealEnb, NetworkAddress, RoutingInformation
from taf.config.testline.ue import Android, Qualcomm

from taf.config.testline.ue import MediaTek
from taf.config.testline.dcap import DcapRnD

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))


_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.205", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_abil_master = CapacityUnit(addr="fsp-5a")
_abil_slave = CapacityUnit(addr="fsp-5b")
_abil_loner = CapacityUnit(addr="192.168.253.22")

#_pdu_1 = Gude("10.44.206.32", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], "EPC", "8221-1")
_pdu_1 = HBTE(addr="10.106.223.72", port_numbers=[2])
_common_unit_0_pdu_port = PduPort(pdu=_pdu_1, port_no="2")
_common_unit = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.106.223.226", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_abil_master, _abil_slave, _abil_loner],
    pdu_port=_common_unit_0_pdu_port,
)

_airscale = Airscale([_common_unit])

# #CU
_cu = CU(
    backhaul_site_oam_ip="10.106.223.226",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.106.223.226", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.106.223.226", username="Nemuadmin", password="nemuuser"
    ),
)

_attenuator = AHBTE(
    ip_addr="10.71.203.130",
    port=5000,
    attenuation_port_numbers=[1, 2, 7, 8, 5, 6],
    model="PA-16-16-6-127-0.5-B-S",
)


_ru_pdu = HBTE(addr="10.71.195.82", port_numbers=[2])
#_ru_pdu = TopYoung(addr="10.71.195.79", port_numbers=[3])


_ru0 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.56.2", username="rfsw", password="3Is6ezFJ7dFlB29cgs0yp3RCM3fUF1zNO1+6Z08tlAc="
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.77.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    # attenuation_ports=[
    #     _attenuator.attenuator_ports[1],
    #     _attenuator.attenuator_ports[2],
    # ],
    pdu_port=_ru_pdu.pdu_ports[2],
    radio_type=RadioTypes.AQQQA,

)




_du = DU(airscale=_airscale, rus=[_ru0], f1_m_ip_addr="10.106.223.226")

_dcap = DcapRnD(
    HttpConnectionDetails(
        addr="10.101.60.54", port="443", username="dcapuser", password="dcapadmin!"
    )
)

_classical_bts = ClassicalBts(cu=_cu, dus=[_du], global_bts_id=11540, instance_id=1930, dcap=_dcap)


_core = RealCore5G(mcc=460, mnc=2)

_core_ssh = SshServiceDetails(addr="10.42.61.65", username="5g", password="2019H@slo")

_common_unit_lte_ssh = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.20")

_common_unit_lte = CommonUnit(
    _common_unit_lte_ssh, capacity_units=[_capacity_unit], pdu_port=None
)

_abia = CapacityUnit(addr="192.168.253.20")

_asia = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.106.223.226", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_abia],
)

_lteenb = RealEnb(
    airscale=Airscale(common_units=[_asia]),
    x2_link_addr=NetworkAddress(
        v4="10.106.223.226",
        routing=RoutingInformation(gateway="10.106.223.225", ip_prefix_length=27),
    ),
    global_bts_id=10515,instance_id=1930
)

_test_pc_enb = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.44.149.64", username="ute", password="ute"
    ),
    connections=[_lteenb],
)

_appserver_ssh = SshServiceDetails(
    addr="10.71.219.229", username="mmw_sg5", password="mm@5", port="45830"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.219.229",
    port="45930",
)


#7b0bf687
_ue_pc_ssh = SshServiceDetails(
    addr="10.106.223.66", username="tester5g", password="Nokia123!"
)
_android = Android(
    ssh_connection_details=_ue_pc_ssh,
    serial_number="ad63a021",  # R5CN20LYP5R R5CN20HRWLM R5CN212N3RX
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["xiaomi"],

)

_samsung3 = Android(
    ssh_connection_details=_ue_pc_ssh,
    serial_number="RFCR70N4J8M",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    iperf_directory="/data/data/com.nokia.android.application/",
    capabilities=["REAL_ANDROID_UE","samsung","UE_1"],
    service_call_attach="16",
)

_appserver = AppServer(iperf_details=_iperf)

tl = TestLine(
    test_pc=_test_pc,
    test_pcs=[_test_pc, _test_pc_enb],
    gnbs=[_classical_bts],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_QC_ASIBR_ABIN1_2xAHLOA_ENB",
    core=_core,
    enbs=[_lteenb],
    #ues=[_android, _samsung2, _mtk],
    ues=[_android, _samsung3],
    appserver=_appserver,
    attenuator=_attenuator,
)

__all__ = ["tl"]
