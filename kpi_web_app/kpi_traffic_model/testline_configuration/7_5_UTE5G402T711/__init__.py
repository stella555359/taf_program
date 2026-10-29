__maintainer__ = "Chen Zheyuan"
__team__ = (
    "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_04_GMS <I_NSB_MN_5GSC_MMW_SC_PZ_HZ_04@internal.nsn.com>"
)
__email__ = "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_04@internal.nsn.com"
__owner_email__ = "zheyuan.chen@nokia-sbell.com"

import os

from taf.config.testline.cloud_hosting import (
    ControlNode,
    NCIR,
    CloudDeployment,
    DeploymentFlavorStack,
    DeploymentNetworkStack,
    DeploymentVnfStack,
)
from taf.config.testline.core import RealCore
from taf.config.testline.testpc import TestPc, Connection
from taf.config.testline.connection_details import (
    OpenStackConnectionDetails,
    SshServiceDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
)
from taf.config.testline.testpc import TestPc
#from taf.config.testline.core import EPCSim
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
from taf.config.testline.radio import RadioTypes, RU
from taf.config.testline.pdu import HBTE as HBTE_pb

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

_attenuator = HBTE(
    ip_addr="10.101.48.87",
    port="5000",
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8],
)

# cloud_topology
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_QC_SA_ASIBL_ABIOB1B2_6xAWHHD_AWHQE"


_cu = CU(
    backhaul_site_oam_ip="10.68.89.162",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.68.89.162", username="toor4nsn", password="oZPS0POrRieRtu", port="22"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.68.89.162", username="Nemuadmin", password="nemuuser"
    ),
)

# DU
_common_unit_pdu = HBTE_pb(addr="10.68.87.40", port_numbers=[1, 2, 3, 4, 5, 6])
_lmp_connection_0 = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_gnb_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.142", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
)

# 5G RU1
_ru_pdu1 = HBTE_pb(addr="10.68.87.35", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru1 = RU(
    ru_hw_group="AWHHD",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.101.47.108", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    pdu_port=_ru_pdu1.pdu_ports[4],
    radio_type=RadioTypes.AWHHD.value,
    serial_number="EB2245R1272",
)

_capacity_unit_0 = CapacityUnit(addr="192.168.255.129", hardware_type="ABIO", rus=[_ru1],)

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection_0,
    capacity_units=[_capacity_unit_0],
    pdu_port=_common_unit_pdu.pdu_ports[5],
    hardware_type="ASIB",
    test_pc=_gnb_test_pc,
)
# airscale
_airscale_0 = Airscale(common_units=[_common_unit_0])

_du_0 = DU(airscale=_airscale_0, rus=[_ru1], f1_m_ip_addr="10.68.89.162")

_classical_bts = ClassicalBts(cu=_cu, dus=[_du_0], instance_id="37530", global_bts_id="37530")

# Testpc
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.217.51", username="ute", password="uteUTE!"
    ),
        connections=[
        Connection(
            interface="eth1",
            device=_classical_bts.dus[0].airscale.common_units[0],
            interface_type="lmp",
        )
    ],
)
_appserver_ssh = SshServiceDetails(
    addr="10.57.191.197", username="vrf3_sg4", password="vrf3@sg4", port="44711"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.197",
    iperf_path="/usr/bin/iperf",
    # iperf_path='/cygdrive/c/iperf',
    port="44710",
    ports=[44711, 44712, 44713, 44714],
)

_cobham = TM500(
    tma_host=SshServiceDetails(
        addr="10.68.86.124", username="mn5gran", password="nokia123@"
    ),
    tma_command_port=5004,
    iperf_details=_iperf,
    tma_path="/cygdrive/c/Program Files (x86)/Aeroflex/TM500/5G NR - NLA latest_version/"
    "Test Mobile Application/TmaApplication.exe",
)

# #Qualcomm
_appserver = AppServer(_iperf)

# UE0
_ue1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.68.86.124", username="mn5gran", password="nokia123@"
    ),
    serial_number="RFCT30V6JCX",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python39/python.exe",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "samsung"],
    imsi="262038001006257",
)

#Qualcomm


# _epcsim = EPCSim(
#     mme_ip="192.168.4.1",
#     mcc=777,
#     mnc=44,
#     tac=777,
#     default_ssh_connection_details=SshServiceDetails(
#         addr="10.47.199.241", username="ute", password="ute"
#     ),
#     dir_path="/opt/wts/latest",
#     cfg_filename="TL101_basic_cfg_realLteEnb.cfg",
#     edaemon_port="22222",
#     egate_port="20021",
# )
# _eNB_capacity_unit = CapacityUnit(addr="192.168.253.36")
# _real_enb_pdu = FACOM(addr="10.57.241.158", port_numbers=[2])
# _eNB_common_unit = CommonUnit(
#     lmp_connection=SshServiceDetails(
#         addr="10.101.49.89", username="toor4nsn", password="oZPS0POrRieRtu"
#     ),
#     pdu_port=_real_enb_pdu.pdu_ports[2],
#     capacity_units=[_eNB_capacity_unit],
# )
# _enb_airscale = Airscale(common_units=[_eNB_common_unit])
# _enb_0 = RealEnb(airscale=_enb_airscale, instance_id="7012", global_bts_id="7012")

tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_classical_bts],
    core=RealCore(mcc=262, mnc=3),
    #enbs=[_enb_0],
    attenuator=_common_unit_pdu,
    ues=[_ue1],
    appserver=_appserver,
    tl_cloud_topology=_tl_cloud_topology,
)


__all__ = ["tl"]

# if __name__=='__main__':
#     print 'hhhh'
