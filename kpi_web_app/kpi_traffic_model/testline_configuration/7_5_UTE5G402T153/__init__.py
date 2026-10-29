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
from taf.config.testline.testpc import Connection
from taf.config.testline.ue import (
    AirphoneCloud,
    Airphone,
    Prisma,
    TM500,
    Qualcomm,
    QualcommUeType,
    Android,
)  # added in taf.meta.5.4
from taf.config.testline.core import EPCSim, LTEEmuCore, PrismaCore, RealCore
from taf.config.testline.gnb.du import DU, Cablink, Endpoint
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

from taf.config.testline.gnb import ClassicalBts
from taf.config.testline import LicenseKeeper


__maintainer__ = "cheng tan"
__team__ = "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_02@internal.nsn.com"
__email__ = "cheng.1.tan@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))
_licensekeeper = LicenseKeeper(username="HAZ3_SG4", password="HAZ3_SG4")


# PB INFO of ENB IS NOT CORRECT #
# 4GRU for RealEnb
_ru_enb_pdu = HBTE(addr="10.57.246.62", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru_enb = RadioModule(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.71.215.233", username="toor4nsn", password="oZPS0POrRieRtu"
    )
)

# #RealEnb
_real_enb_pdu = HBTE(addr="10.57.246.195", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.71.215.231", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[4],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb)

# #5GRU_0 for cloudBTS
_ru_pdu = HBTE(addr="10.71.197.101", port_numbers=[1])

_ru = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.48.2", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="root", password="w@=EIj7P6R0bVy85OjCVa^ho&8"
    ),
    pdu_port=_ru_pdu.pdu_ports[1],
    radio_type=RadioTypes.AEWB.value,
)

# #######Iperf########
_appserver_ssh = SshServiceDetails(
    addr="10.70.222.53", username="mmw_sg4", password="mm@4", port="44000"
)

_iperf_details = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.70.222.53",
    iperf_path="/data/local/tmp/ipef/",
    port="44000",
    ports=["44000", "44001"],
)
_appserver = AppServer(_iperf_details)

_epcsim = EPCSim(
    mme_ip="192.168.4.1",
    mcc=262,
    mnc=3,
    tac=20000,
    default_ssh_connection_details=SshServiceDetails(
        addr="10.101.49.49", username="mmw_sg4", password="mm@4"
    ),
    dir_path="/opt/wts/latest",
    cfg_filename="TL101_basic_cfg_realLteEnb.cfg",
    edaemon_port="22222",
    egate_port="20021",
)

_android1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.217.48", username="nokia5G", password="noki@123"
    ),
    serial_number="RFCT31FMCGJ",
    server_dir="C:/Program Files (x86)/Spark1.1.1997.3/Bin/Spark.exe",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="/cygdrive/c/pyro_server/DIAG.cfg",
    iperf_details=_iperf_details,
    capabilities=["REAL_ANDROID_UE", "samsung", "huawei_sigspark"],
    imsi="262033100009207",
    licensekeeper=_licensekeeper,
)

# #DU_0 for cloudlBTS
_lmp_connection_0 = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_0 = CapacityUnit(addr="1.1.1.1", rus=[_ru], hardware_type="ABIO")

_du_pdu = HBTE(addr="10.71.197.101", port_numbers=[2])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection_0,
    capacity_units=[_capacity_unit_0],
    pdu_port=_du_pdu.pdu_ports[2],
    hardware_type="ASIL",
)

_airscale = Airscale(common_units=[_common_unit_0])


_ru_cablinks = [
    Cablink(
        source=Endpoint(unit=_capacity_unit_0, label="SFP", port_id=1),
        target=Endpoint(unit=_ru, label="SFP", port_id=1),
    ),
    Cablink(
        source=Endpoint(unit=_capacity_unit_0, label="SFP", port_id=2),
        target=Endpoint(unit=_ru, label="SFP", port_id=2),
    ),
]

_du = DU(
    airscale=_airscale, rus=[_ru], f1_m_ip_addr="10.71.215.230", cablinks=_ru_cablinks
)

# #CU
_cu = CU(
    backhaul_site_oam_ip="10.71.215.230",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.215.230", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.215.230", username="Nemuadmin", password="nemuuser"
    ),
)

# classicalbts------------------------------------------------
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=153, global_bts_id=1)


# #host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.70.230.131", username="ute", password="ute"
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_classical_bts.dus[0].airscale.common_units[0],
            interface_type="lmp",
        )
    ],
)

# #cloud_topology------------------------------------------------
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ANDROID_ASILL_ABIOB1_AEWB_ENB"

tl = TestLine(
    test_pc=_host,
    test_pcs=[_host],
    ues=[_android1],
    core=RealCore(mcc=262, mnc=3),
    gnbs=[_classical_bts],
    enbs=[_lte_real_enb],
    appserver=_appserver,
    tl_cloud_topology=_tl_cloud_topology,
)
