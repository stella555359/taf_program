import os
from taf.config.testline.cloud_hosting import (
    ControlNode,
    NCIR,
    CloudDeployment,
    DeploymentFlavorStack,
    DeploymentNetworkStack,
    DeploymentVnfStack,
    ComputeNode,
    OSP,
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
from taf.config.testline.gnb.du import DU
from taf.config.testline.pdu import PduPort, Pdu, EPC, ATEN, RRB, APC, Gude, HBTE, FACOM
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import (
    AirphoneCloud,
    Airphone,
    Prisma,
    TM500,
    Qualcomm,
    QualcommUeType,
    Android,
)  # added in taf.meta.5.4
from taf.config.testline.enb import (
    Enb,
    SimEnb,
    RealEnb,
    LTEEmuEnb,
    PrismaEnb,
    DocomoEnb,
)
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.config.testline.attenuator import (
    AttenuationPort,
    TopYoung,
)  # added in taf.meta 5.4
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
from taf.config.testline.signal_analyzer import KeysightN9935A
from taf.config.testline.nms import Netact

# from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline import NetworkAddress, RoutingInformation
from taf.config.testline.appserver import AppServer

__maintainer__ = "Shasha Liu"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_5_GMS <I_MN_5G_RAN_IV4_LINE_HZG_5@internal.nsn.com>"
)
__email__ = "shasha.liu@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

##host #Local VM
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.58", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

##RealEnb
_real_enb_pdu = FACOM(addr="10.68.87.98", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.68.88.237", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[5],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=None)

##5GRU for classicalBTS

_attenuator = TopYoung(
    ip_addr="10.57.249.53", port=23, attenuation_port_numbers=[13, 14, 15, 16]
)

_ru1_pdu = HBTE(addr="10.68.87.102", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru1 = RU(
    ru_hw_group="below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.52", username="root", password="root"
    ),
    pdu_port=_ru1_pdu.pdu_ports[4],
    radio_type=RadioTypes.AWHQM,  # radio_type='AWHQM'
    serial_number="EB2013R0057",
    attenuation_ports=[
        _attenuator.attenuator_ports[13],
        _attenuator.attenuator_ports[14],
        _attenuator.attenuator_ports[15],
        _attenuator.attenuator_ports[16],
    ],
)

###DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.68.88.236", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(addr="192.168.253.22")

_gnb_pdu = HBTE(addr="10.68.87.98", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[5],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru1], f1_m_ip_addr="10.68.88.236")

##CU #Auto TL Upgrading
_cu = CU(
    backhaul_site_oam_ip="10.68.88.236",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.68.88.236", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.68.88.236", username="Nemuadmin", password="nemuuser"
    ),
)

##cloud_topology #UTE Type
_tl_cloud_topology = "CLOUD_5G_RPI_SB_ASIKA102L_ABILB101B1_AWHQM_19B"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id="3135", global_bts_id="1")

# switch Dtor
_dell_s4048on_ssh = SshServiceDetails(
    addr="4.4.4.4", port="1/18", username="5gran", password="nokia123"
)  # EIF1 Port
_dell_s4048on_switch = DellS4048ONSwitch(_dell_s4048on_ssh)

# switch Mtor
_dell_s4048ton_ssh = SshServiceDetails(
    addr="5.5.5.5", port="1/18", username="5gran", password="nokia123"
)
_dell_s4048ton_switch = DellS4048TONSwitch(_dell_s4048ton_ssh)

# # netact - kongfu
_netact = Netact("10.106.161.25")


_appserver_ssh = SshServiceDetails(
    addr="10.57.191.247", username="vrf4_sg5", password="vrf4@sg5", port="55931"
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.247",
    iperf_path="/data/data/com.nokia.syve.uemanager.mobile/",
    port=55933,
)
_appserver = AppServer(_iperf)
# _appserver.iperf_details.port = 55915

# CI_Detail_UE_Type='Huawei Mate 20'

_ue1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.68.86.64", username="nokia5G", password="noki@123"
    ),
    serial_number="L8K5T19919006382",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["HUAWEI_20X", "huawei"]
    # serial_com='12',
    # reset_interface='no',
    # enable_disable_cfun='yes',
    # processes_to_kill=['ttermpro', 'ATCom'],
    # ue_class = 'QualcommNoLicenseUe',
    # turn_off_on_firewall='yes',
    # diag_com='10',
    # iperf_directory ='adb shell /data/iperf'
)


tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    nms=_netact,
    enbs=[_lte_real_enb],
    ues=[_ue1],
    tl_cloud_topology=_tl_cloud_topology,
    attenuator=_attenuator,
    appserver=_appserver,
    switches=[_dell_s4048on_switch, _dell_s4048ton_switch],
)

# old version keyword under robotws5g/resource compatibility workaround
# tl = TestlineWrapper(tl)
