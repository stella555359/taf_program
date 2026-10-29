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
from taf.config.testline.testpc import TestPc
from taf.config.testline.ue import (
    AirphoneCloud,
    Airphone,
    Prisma,
    TM500,
    Qualcomm,
    QualcommUeType,
    Android,
    MediaTek,
)  # added in taf.meta.5.4
from taf.config.testline.core import EPCSim, LTEEmuCore, PrismaCore
from taf.config.testline.gnb.du import DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, ATEN, RRB, APC, Gude
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit

# from taf.config.testline.ue import AirphoneCloud, Airphone, Prisma, TM500
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
from taf.config.testline.appserver import AppServer
from taf.config.testline.attenuator import (
    AttenuationPort,
    TopYoung,
    JFW,
    HBTE,
    Hytem,
    RadioRack,
)
from taf.compatibility.configuration import TestlineWrapper

__maintainer__ = "y6lu"
__team__ = "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_03@internal.nsn.com"
__email__ = "lu.yu@nokia-sbell.com"


# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# #host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.149", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

_appserver_ssh = SshServiceDetails(
    addr="10.70.222.51", username="mmw_sg3", password="mm@3", port="43325"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.70.222.51",
    iperf_path="/usr/bin/iperf",
    port=43326,
)

# Qualcomm
_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.101.47.23", username="nokia5G", password="noki@123"
    ),
    serial_number="be0c151c",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_UE", "qct_dx50"],
)

##CU
_cu = CU(
    backhaul_site_oam_ip="10.101.51.131",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.51.131", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.51.131", username="Nemuadmin", password="nemuuser"
    ),
)

# attenuator
_attenuator = HBTE(
    ip_addr="10.101.51.132",
    port=5000,
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8],
    model="PA-16-16-6-127-0.5-B-S",
)


# #DU_0 for classicalBTS
_lmp_connection_0 = SshServiceDetails(
    addr="10.101.51.131", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_0 = CapacityUnit(addr="1.1.1.1")

_gnb_pdu = FACOM(addr="10.101.45.228", port_numbers=[2])


_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection_0,
    capacity_units=[_capacity_unit_0],
    pdu_port=_gnb_pdu.pdu_ports[2],
)


_airscale = Airscale(common_units=[_common_unit_0])

_ru_pdu = FACOM(addr="10.101.45.226", port_numbers=[2])

_ru = RU(
    ru_hw_group="AZQO",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.56.2", username="root", password="a2%FgSz3$fHmdusap354xujw7a"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.56.2", username="root", password="a2%FgSz3$fHmdusap354xujw7a"
    ),
    pdu_port=_ru_pdu.pdu_ports[2],
    radio_type="AZQO",
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[4],
        _attenuator.attenuator_ports[5],
        _attenuator.attenuator_ports[6],
        _attenuator.attenuator_ports[7],
        _attenuator.attenuator_ports[8],
    ],
)

_du = DU(airscale=_airscale, rus=[_ru], f1_m_ip_addr="10.101.51.131")

# classicalbts
_classical_bts = ClassicalBts(
    dus=[_du], cu=_cu, instance_id="10045", global_bts_id="10045"
)


# RealEnb
_real_enb_pdu = FACOM(addr="10.101.45.228", port_numbers=[1])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.101.51.130", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[1],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, instance_id="925")


_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.70.222.51",
    iperf_path="iperf",
    port="43327",
)
_appserver = AppServer(_iperf_details_on_appserver)


tl = TestLine(
    test_pc=_host,
    ues=[_android],
    gnbs=[_classical_bts],
    enbs=[_lte_real_enb],
    appserver=_appserver,
    attenuator=_attenuator,
)
