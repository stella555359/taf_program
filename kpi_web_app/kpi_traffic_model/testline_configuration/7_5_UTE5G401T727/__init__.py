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
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.core import EPCSim
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import ClassicalBts, CU
from taf.config.testline.enb import RealEnb
from taf.config.testline.ue import TM500, Android
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

__maintainer__ = "Liu Steven"
__team__ = (
    "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_04_GMS <I_NSB_MN_5GSC_MMW_SC_PZ_HZ_04@internal.nsn.com"
)
__email__ = "steven.liu@nokia-sbell.com"

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

_attenuator = HBTE(
    ip_addr="10.101.38.226", port="5000", attenuation_port_numbers=[5, 6, 7, 8]
)

# Testpc
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.74", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_cu = CU(
    backhaul_site_oam_ip="10.57.131.110",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.131.110", username="toor4nsn", password="oZPS0POrRieRtu", port="22"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.131.110", username="Nemuadmin", password="nemuuser"
    ),
)

# DU
_common_unit_pdu = FACOM(addr="10.57.242.11", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_lmp_connection_0 = SshServiceDetails(
    addr="10.57.131.110", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_0 = CapacityUnit(addr="192.168.253.17")

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection_0,
    capacity_units=[_capacity_unit_0],
    pdu_port=_common_unit_pdu.pdu_ports[5],
)

# airscale
_airscale_0 = Airscale(common_units=[_common_unit_0])

# 5G RU
_ru_pdu = FACOM(addr="10.57.243.10", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])


_ru = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.48.162", username="root", password="asmr"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.17", username="root", password="umniedziala"
    ),
    pdu_port=_ru_pdu.pdu_ports[8],
    attenuation_ports=[
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[6],
        _attenuator.attenuator_ports[7],
        _attenuator.attenuator_ports[8],
    ],
)

_du_0 = DU(airscale=_airscale_0, rus=[_ru], f1_m_ip_addr="10.57.131.110")

_cbts = ClassicalBts(cu=_cu, dus=[_du_0], instance_id="7271", global_bts_id="7271")

_appserver_ssh = SshServiceDetails(
    addr="10.57.178.18", username="mmw_sg4", password="mm@4", port="44300"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.178.18",
    iperf_path="/usr/bin/iperf",
    # iperf_path='/cygdrive/c/iperf',
    port="44300",
    ports=["44296", "44297", "44298", "44299", "44230"],
)

_cobham = TM500(
    tma_host=SshServiceDetails(
        addr="10.57.130.7", username="nokia5G", password="noki@123"
    ),
    tma_command_port=5004,
    iperf_details=_iperf,
    tma_path="",
)

# #Qualcomm

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.178.18",
    iperf_path="iperf",
    port="41814",
)

_appserver = AppServer(_iperf_details_on_appserver)

_android_0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.101.47.44", username="nokia5G", password="noki@123"
    ),
    serial_number="3e4c0cde",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "askey"],
)
# #Qualcomm

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
        addr="10.101.49.69", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_real_enb_pdu.pdu_ports[2],
    capacity_units=[_eNB_capacity_unit],
)
_enb_airscale = Airscale(common_units=[_eNB_common_unit])
_enb_0 = RealEnb(airscale=_enb_airscale, instance_id="727")


tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_cbts],
    core=_epcsim,
    enbs=[_enb_0],
    attenuator=_attenuator,
    ues=[_android_0],
    appserver=_appserver,
)


__all__ = ["tl"]
