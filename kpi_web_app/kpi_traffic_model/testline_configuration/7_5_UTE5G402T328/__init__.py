import os
from taf.config.testline.appserver import AppServer
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
from taf.config.testline.ue import (
    AirphoneCloud,
    Airphone,
    Prisma,
    TM500,
    Qualcomm,
    QualcommUeType,
    Android,
)  # added in taf.meta.5.4
from taf.config.testline.core import EPCSim, LTEEmuCore, PrismaCore
from taf.config.testline.gnb.du import DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, ATEN, RRB, APC, Gude
from taf.config.testline.pdu import HBTE
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import AirphoneCloud, Airphone, Prisma, TM500
from taf.config.testline.enb import (
    Enb,
    SimEnb,
    RealEnb,
    LTEEmuEnb,
    PrismaEnb,
    DocomoEnb,
)
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch

# added in taf.meta 5.4
from taf.config.testline.gnb.networkaddress import NetworkAddress  # add in taf.meta 5.4
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)
from taf.config.testline.hardware_controller import (
    AmiaFanHardwareController,
    GPSPowerHardwareController,
)

__maintainer__ = "Jiang Wenwen"
__team__ = "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_02@internal.nsn.com"
__email__ = "wenwen.jiang@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# #host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.195.15", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_docker_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.46", username="dcapuser", password="dcapuser123"
    )
)
_tce_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.46", username="dcapuser", port=1234
    )
)

# PB INFO of ENB IS NOT CORRECT #
# 4GRU for RealEnb
_ru_enb_pdu = HBTE(addr="10.57.246.62", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru_enb = RadioModule(
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.10.49", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru_enb_pdu.pdu_ports[2],
)


# #RealEnb
_real_enb_pdu = HBTE(addr="10.57.246.195", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.71.215.233", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[4],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=_ru_enb)

# #5GRU_0 for BTS
_ru_pdu = HBTE(addr="10.68.87.80", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.48.2", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    pdu_port=_ru_pdu.pdu_ports[4],
    radio_type=RadioTypes.AEQC,
)

# #5GRU_1 for BTS
_ru_pdu1 = HBTE(addr="10.68.87.87", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.48.2", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    pdu_port=_ru_pdu1.pdu_ports[1],
    radio_type=RadioTypes.AEQY,
)

# ####### appserver ######
_appserver_ssh = SshServiceDetails(
    addr="10.57.191.234", username="vrf3_sg2", password="vrf3@sg2", port="42328" # this port used by UE
)
# #######UEs Iperf########
_iperf_details = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.234",
    iperf_path="/usr/bin/iperf/",
    port="42328", # this port used by appserver, so it must be different from UE1 used for UL traffic.
)
_appserver = AppServer(_iperf_details)

_epcsim = EPCSim(  ###do we need?NO!
    mme_ip="192.168.4.1",
    mcc=460,
    mnc=2,
    tac=20000,  ###not need
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.178.20", username="mmw_sg2_3", password="mm@2@3"
    ),
    dir_path="/opt/wts/latest",
    cfg_filename="TL101_basic_cfg_realLteEnb.cfg",
    edaemon_port="22222",
    egate_port="20021",
)

_android1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.68.86.25", username="mn5gran", password="nokia123@"
    ),
    serial_number="RFCR926DQBZ",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="/cygdrive/c/pyro_server/DIAG.cfg",
    iperf_details=_iperf_details,
    capabilities=["samsung"],
    imsi="450053100010770",
)

_android2 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.68.86.203", username="mn5gran", password="nokia123@"
    ),
    serial_number="R5CRB28WDZH",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="/cygdrive/c/pyro_server/DIAG.cfg",
    iperf_details=_iperf_details,
    capabilities=["samsung"],
    imsi="460023100010698",
)

# #DU_0 for TL
_lmp_connection_0 = SshServiceDetails(
    addr="10.68.88.217", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_0 = CapacityUnit(addr="192.168.253.22")

_du_pdu = HBTE(addr="10.68.87.81", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection_0,
    capacity_units=[_capacity_unit_0],
    pdu_port=_du_pdu.pdu_ports[5],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru], f1_m_ip_addr="10.68.88.217")

#DU_1 for TL
_lmp_connection_1 = SshServiceDetails(
    addr="10.68.88.218", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_1 = CapacityUnit(addr="192.168.253.22")

_du_pdu1 = HBTE(addr="10.68.87.81", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection_1,
    capacity_units=[_capacity_unit_1],
    pdu_port=_du_pdu1.pdu_ports[4],
)

_airscale = Airscale(common_units=[_common_unit_1])

_du1 = DU(airscale=_airscale, rus=[_ru1], f1_m_ip_addr="10.68.88.218")

# #CU
_cu = CU(
    backhaul_site_oam_ip="10.68.88.217",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.68.88.217", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.68.88.217", username="Nemuadmin", password="nemuuser"
    ),
)

# #CU1
_cu1 = CU(
    backhaul_site_oam_ip="10.68.88.218",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.68.88.218", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.68.88.218", username="Nemuadmin", password="nemuuser"
    ),
)

# classicalbts------------------------------------------------
_classical_btsfir = ClassicalBts(
    dus=[_du], cu=_cu, instance_id=11192, global_bts_id=11192
    )
_classical_btssec = ClassicalBts(
    dus=[_du1], cu=_cu1, instance_id=11218, global_bts_id=11218
    )

# #cloud_topology------------------------------------------------
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ASIB_ABIO_AEUB_eCPRI" 
_t2_cloud_topology = "CLOUD_5G_CLASSICAL_ASIB_ABIO_AEUB_eCPRI"

tl = TestLine(
    test_pc=_host,
    test_pcs=[_docker_pc, _tce_pc],
    ues=[_android1, _android2],
    core=_epcsim,
    gnbs=[_classical_btsfir, _classical_btssec],
    enbs=[_lte_real_enb],
    appserver=_appserver,
    tl_cloud_topology=_tl_cloud_topology,
) # this is an unique struct, can not be duplicated. 
