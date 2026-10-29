__maintainer__ = "Tang Lixia"
__team__ = "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_03@internal.nsn.com"  # TL owner's team
__email__ = "lixia.tang@nokia-sbell.com"

import os

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
from taf.config.testline.core import (
    EPCSim,
    RealCore4G,
    RealCore,
    RealCore5GDetails,
    AMF,
)
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import ClassicalBts, CU
from taf.config.testline.enb import RealEnb
from taf.config.testline.ue import TM500, Android
from taf.config.testline.ue import MediaTek
from taf.config.testline.pdn import PDN, PDPTypes
from taf.config.testline import DU, RU
from taf.config.testline.attenuator import (
    AttenuationPort,
    HBTE,
)  # added in taf.meta 5.4
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC
from taf.config.testline.radio import RadioModule
from taf.config.testline import IperfDataTransferDetails
from taf.config.testline.appserver import AppServer

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

_attenuator = HBTE(
    ip_addr="10.57.241.171", port="7", attenuation_port_numbers=[1, 2, 3, 4]
)

# Testpc
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.195.67", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_cu = CU(
    backhaul_site_oam_ip="10.101.51.143",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.51.143", username="toor4nsn", password="oZPS0POrRieRtu", port="22"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.51.143", username="Nemuadmin", password="nemuuser"
    ),
)

# DU
_common_unit_pdu = FACOM(addr="10.101.45.228", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_lmp_connection_0 = SshServiceDetails(
    addr="10.101.51.143", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_0 = CapacityUnit(addr="192.168.253.17")

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection_0,
    capacity_units=[_capacity_unit_0],
    pdu_port=_common_unit_pdu.pdu_ports[7],
)

# airscale
_airscale_0 = Airscale(common_units=[_common_unit_0])

# 5G RU
_ru1_pdu = FACOM(addr="10.101.45.229", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_ru2_pdu = FACOM(addr="10.101.45.229", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])


_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.17", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.17", username="root", password="umniedziala"
    ),
    pdu_port=_ru1_pdu.pdu_ports[2],
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
)

_ru2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.17", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.17", username="root", password="umniedziala"
    ),
    pdu_port=_ru2_pdu.pdu_ports[4],
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
    ],
)

_du_0 = DU(airscale=_airscale_0, rus=[_ru1, _ru2], f1_m_ip_addr="10.101.51.143")

_cbts = ClassicalBts(cu=_cu, dus=[_du_0], instance_id="10579", global_bts_id="10579")

_appserver_ssh = SshServiceDetails(
    addr="10.57.191.199", username="vrf3_sg3", password="vrf3@sg3", port="43666"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.199",
    iperf_path="/usr/bin/iperf",
    port="43666",
)

_cobham = TM500(
    tma_host=SshServiceDetails(
        addr="10.57.130.139", username="nokia5G", password="noki@123"
    ),
    tma_command_port=5004,
    iperf_details=_iperf,
    tma_path="/cygdrive/c/Program Files (x86)/Aeroflex/TM500/5G NR - NLA latest_version/Test Mobile Application/TmaApplication.exe",
)

# #Qualcomm

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.199",
    iperf_path="iperf",
    port="43666",
)

_appserver = AppServer(_iperf_details_on_appserver)

_android_0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.68.86.235", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="75cefbe3",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python37/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["qct_dx50"],
)
# #Qualcomm

# M80 Figeac
_mtk_host_ssh = SshServiceDetails(
    addr="10.68.86.235", username="MN5GRAN", password="nokia123@"
)

_iperf_details_on_mtk = IperfDataTransferDetails(
    ssh_connection_details=_mtk_host_ssh,
    network_interface_address="",
    iperf_path="/data/local/tmp/iperf",
    port="51000",
)

_mtk = MediaTek(
    ssh_connection_details=_mtk_host_ssh,
    server_dir="c:/pyro_server",
    server_port=8080,
    edb_file_path="C:/UEPC/MTK/Item5_NR16_R2_MP_W23_21_p2_MT6879_SP_bin/MDDB_MT6879_S00_NR16_R2_MP_W23_21_P2.EDB",
    log_filter="2.Gen98_Default_Standard",
    imei="235428746578343",
    imsi="262033031398575",
    apn_url="wap2.nokia.com",
    iperf_details=_iperf_details_on_mtk,
    capabilities=["REAL_MEDIATEK_UE", "SA"],
)

_epcsim = EPCSim(
    mme_ip="192.168.4.1",
    mcc=777,
    mnc=44,
    tac=777,
    default_ssh_connection_details=SshServiceDetails(
        addr="10.47.199.241", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    dir_path="/opt/wts/latest",
    cfg_filename="TL101_basic_cfg_realLteEnb.cfg",
    edaemon_port="22222",
    egate_port="20021",
)
_eNB_capacity_unit = CapacityUnit(addr="192.168.253.36")
_real_enb_pdu = FACOM(addr="10.57.241.158", port_numbers=[2])
_eNB_common_unit = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.101.52.35", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_real_enb_pdu.pdu_ports[2],
    capacity_units=[_eNB_capacity_unit],
)
_enb_airscale = Airscale(common_units=[_eNB_common_unit])
_enb = RealEnb(airscale=_enb_airscale, global_bts_id="712", instance_id="712")

_pdns = [
    PDN(pdp_type=PDPTypes.IP.value, apn="wap2.nokia.com"),
    PDN(pdp_type=PDPTypes.IP.value, apn="wap2.nokia.com"),
]
_core = RealCore(pdns=_pdns)

tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    core=_core,
    enbs=[_enb],
    attenuator=_attenuator,
    ues=[_mtk],
    appserver=_appserver,
    switches=[_test_pc, _test_pc],
)


__all__ = ["tl"]
