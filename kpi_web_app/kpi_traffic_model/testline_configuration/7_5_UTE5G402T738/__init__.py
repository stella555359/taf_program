import os
import yaml
import re
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
from taf.config.testline.attenuator import (
    AttenuationPort,
    HBTE,
)  # added in taf.meta 5.4
from taf.config.testline.testpc import TestPc
from taf.config.testline.appserver import AppServer
from taf.config.testline.core import EPCSim, LTEEmuCore, PrismaCore
from taf.config.testline import RU, DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC
from taf.config.testline.pdu import HBTE as HBTE_pb
from taf.config.testline.radio import RadioModule, RadioTypes
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import AirphoneCloud, Airphone, Prisma, TM500, Android
from taf.config.testline import Enb, SimEnb, RealEnb, LTEEmuEnb, PrismaEnb, DocomoEnb
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.config.testline.nms import Netact
from taf.config.testline import LicenseKeeper

__maintainer__ = "Liufengyi"  # TL owner name
__team__ = "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_04@internal.nsn.com"  # TL owner's team
__email__ = "feng.y.liu@nokia-sbell.com"  # TL owner's email
_cfg_dir = os.path.dirname(os.path.abspath(__file__))
_licensekeeper = LicenseKeeper(username="HAZ3_SG4_1", password="HAZ3_SG4_1")
##testPc(taf)
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.32", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
# 5GRU for classicalBTS
# PB for RU
# the sequence accord to webui read out.
_attenuator = HBTE(
    ip_addr="10.57.251.250", port="5000", attenuation_port_numbers=[1, 2, 3, 4]
)
_ru_pdu = HBTE_pb(addr="10.71.207.71", port_numbers=[1])
_ru1 = RU(
    ru_hw_group="AWEUA",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1",
        username="rfsw",
        password="ckBW1r1CX7VUPHcoHd69to3UwvEVm+cGW1aXDlfr51Y=",
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.155.206", username="nokia", password="mmw04UUF3Edcvgy!"
    ),
    pdu_port=_ru_pdu.pdu_ports[1],
    radio_type=RadioTypes.AWEUA,
)
_ru_pdu2 = FACOM(addr="10.71.195.109", port_numbers=[3])
_ru2 = RU(
    ru_hw_group="AWEUA",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="asmr"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.155.207", username="nokia", password="mmw04UUF3Edcvgy!"
    ),
    pdu_port=_ru_pdu2.pdu_ports[3],
)

_ru_pdu3 = FACOM(addr="10.71.195.109", port_numbers=[3])
_ru3 = RU(
    ru_hw_group="AWEUA",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="root", password="asmr"
    ),
    lmp_connection=SshServiceDetails(
        addr="10.57.155.207", username="nokia", password="mmw04UUF3Edcvgy!"
    ),
    pdu_port=_ru_pdu3.pdu_ports[3],
)

##classical gNB parameter
# gNB lmp ip
_lmp_connection = SshServiceDetails(
    addr="10.71.209.233", username="toor4nsn", password="oZPS0POrRieRtu"
)
# abil internal ip
_capacity_unit = CapacityUnit(addr="192.168.253.20")
# gNB PB
_gnb_pdu = FACOM(addr="10.71.195.151", port_numbers=[8])
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[8],
)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(airscale=_airscale, rus=[_ru1, _ru2, _ru3], f1_m_ip_addr="10.71.209.233")

# gNB oam mplane ip
_cu = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.209.233", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.209.233", username="Nemuadmin", password="nemuuser"
    ),
)
# RealEnb
_lmp_connection_enb = SshServiceDetails(
    addr="10.71.209.234", username="toor4nsn", password="oZPS0POrRieRtu"
)
_enb_pdu = FACOM(addr="10.71.195.150", port_numbers=[6])
_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection_enb,
    capacity_units=[],
    pdu_port=_enb_pdu.pdu_ports[6],
)
_real_enb = Airscale(common_units=[_common_unit_1])
_lte_real_enb = RealEnb(airscale=_real_enb, rms=None, instance_id=738, global_bts_id=738)
## switch Dtor
# switch prot to ASIK EIF
_dell_s4048on_ssh = SshServiceDetails(
    addr="10.101.63.81", port="1/22", username="5gran", password="nokia123"
)
_dell_s4048on_switch = DellS4048ONSwitch(_dell_s4048on_ssh)
# cloud_topology
# instance_id = MRBTS_ID
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=738, global_bts_id=738)
# netact ip
_netact = Netact("10.107.178.214")
##L3 call added
# QualComm UE
_appserver_ssh = SshServiceDetails(
    addr="10.70.222.53", username="mmw_sg4", password="mm@4", port="44411"
)
_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.70.222.53",
    iperf_path="/usr/bin/iperf",
    port="44411",
    ports=[44411, 44412, 44413, 44414, 44415, 44416, 44417],
)

_appserver = AppServer(_iperf_details_on_appserver)

# Qualcomm
_android_0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.217.158", username="nokia5G", password="noki@123"
    ),
    serial_number="5a420dc8",
    server_dir="C:/Program Files (x86)/Spark1.1.1997.1/Bin/Spark.exe",
    # server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033100004109",
    capabilities=["REAL_ANDROID_UE", "samsung", "huawei_sigspark"],
    licensekeeper=_licensekeeper,
)

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    enbs=[_lte_real_enb],
    switches=[_dell_s4048on_switch],
    nms=_netact,
    appserver=_appserver,
    ues=[_android_0, _android_0, _lte_real_enb],
)

__all__ = ["tl"]
