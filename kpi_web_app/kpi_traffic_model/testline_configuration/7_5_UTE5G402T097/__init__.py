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
from taf.config.testline.core import EPCSim, LTEEmuCore, PrismaCore
from taf.config.testline import RU, DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit

# from taf.config.testline.ue import AirphoneCloud, Airphone, Prisma, TM500
from taf.config.testline import Enb, SimEnb, RealEnb, LTEEmuEnb, PrismaEnb, DocomoEnb
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.nms import Netact
from taf.config.testline.gnb.networkaddress import NetworkAddress

__maintainer__ = "Shen Jian"  # TL owner name
__team__ = "I_MN_5G_RAN_IV4_LINE_HZG_8_IV@internal.nsn.com"  # TL owner's team
__email__ = "Jenny.chang@nokia-sbell.com"  # TL owner's email

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

##host
# _host = TestPc(
#     default_ssh_connection_details=SshServiceDetails(addr='10.57.157.137', username='root', password='nokia123'))

_gnb_test_pc_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.189.19", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

# epc_sim
# _epcsim = EPCSim(mme_ip='10.57.157.137', mcc=311, mnc=489, tac=788,
#          default_ssh_connection_details=SshServiceDetails(
#          addr='10.57.157.137', username='nokia', password='nokia123'),
#          dir_path='/home/nokia/Jenny/Binary64bits_RrcWithNrRrc', cfg_filename='basic_wts_step1_175.cfg',
#          edaemon_port='22222', egate_port='20000')

##Cobham

# 5GRU for classicalBTS
_ru_pdu4 = FACOM(addr="10.68.87.119", port_numbers=[4])
_ru4 = RU(
    ru_hw_group="AEQY",
    serial_number="1M201202419",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.101.1", username="rfsw", password="gSDBExyEbO33komYWL6iPrtSaYc5XimHAGrsJ/K8+AY="
    ),
    lmp_connection=SshServiceDetails(
        addr="10.68.86.189", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu4.pdu_ports[4],
)

_ru_pdu5 = FACOM(addr="10.101.45.168", port_numbers=[1])
_ru5 = RU(
    ru_hw_group="AQQL",
    serial_number="L1214304634",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="serviceuser", password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY="
    ),
    lmp_connection=SshServiceDetails(
        addr="10.101.47.59", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu5.pdu_ports[1],
)

_ru_pdu6 = FACOM(addr="10.101.45.166", port_numbers=[5])
_ru6 = RU(
    ru_hw_group="AVQL",
    serial_number="L1233410014",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="serviceuser", password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og="
    ),
    lmp_connection=SshServiceDetails(
        addr="10.101.47.81", username="ute", password="3edc4rfv%TGB"
    ),
    pdu_port=_ru_pdu6.pdu_ports[5],
)

##DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(addr="192.168.253.20")
_gnb_pdu = FACOM(addr="10.101.45.170", port_numbers=[2])
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[2],
    test_pc=_gnb_test_pc_0,
)
_airscale = Airscale(common_units=[_common_unit_0])
##_ru3 temp remove for fault10 PR620022
_du = DU(airscale=_airscale, rus=[_ru4, _ru5, _ru6])

##CU
_cu = CU(
    backhaul_site_oam_ip="10.101.50.232",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.50.232", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.50.232", username="Nemuadmin", password="nemuuser"
    ),
)

# RealEnb
_enb_pdu_0 = FACOM(addr="10.57.241.233", port_numbers=[5])
_enb_lmp_connection_0 = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
_enb_common_unit_0 = CommonUnit(
    lmp_connection=_enb_lmp_connection_0,
    capacity_units=[],
    pdu_port=_enb_pdu_0.pdu_ports[5],
    test_pc=None,
    hardware_type=None,
)
_real_enb_0 = Airscale(common_units=[_enb_common_unit_0])
_lte_real_enb = RealEnb(
    system_module=_real_enb_0,
    oam_ip=NetworkAddress(v4="10.57.151.27"),
    instance_id=10255,
    rms=[],
)

##cloud_topology
# _tl_cloud_topology = "CLOUD_5G_BB3"

# instance_id = MRBTS_ID
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=97)
# netact ip
# _netact = Netact("10.107.178.214")

tl = TestLine(
    test_pc=_gnb_test_pc_0,
    gnbs=[_classical_bts],
    enbs=[_lte_real_enb],
    #    ues=[_android],
    #    tl_cloud_topology=_tl_cloud_topology,
    # switches=[_dell_s4048on_switch, _dell_s4048ton_switch],
)

# tl = TestlineWrapper(tl)
