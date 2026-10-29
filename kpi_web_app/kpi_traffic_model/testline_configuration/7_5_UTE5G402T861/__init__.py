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
from taf.config.testline.core import EPCSim, LTEEmuCore, PrismaCore
from taf.config.testline import RU, DU, NetworkAddress, RoutingInformation, AppServer
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, HBTE
from taf.config.testline.testline import TestLine
from taf.config.testline.ue import Android, AirphoneCloud, Airphone, Prisma, TM500
from taf.config.testline.gnb import CU, ClassicalBts, CloudBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline import Enb, SimEnb, RealEnb, LTEEmuEnb, PrismaEnb, DocomoEnb
from taf.config.testline.core import RealCore
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)
from taf.config.testline.nms import Netact
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch

# from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.attenuator import AttenuationPort, TopYoung
from taf.config.testline.dcap import DcapRnD, DcapBasic
from taf.config.testline.gnb.du import Cablink, Endpoint

from taf.config.testline.radio import RadioTypes  # syj
from taf.config.testline.testpc import Connection

__maintainer__ = "Luo Menghua"  # TL owner name
__team__ = "I_NSB_MN_5GSC_5G_PZ_HZ_07_GMS <I_NSB_MN_5GSC_5G_PZ_HZ_07_GMS@internal.nsn.com>"  # TL owner's team
__email__ = "menghua.luo@nokia-sbell.com"  # TL owner's email

# common
__all__ = ["tl"]
_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# _netact = Netact(addr="10.107.183.26")  # 10.107.183.26--NetAct5-Han
_netact = Netact(addr="10.108.248.82")  # 10.108.248.82--NetAct4-Chen(Gansu)

# epc_sim
# _epcsim = EPCSim(mme_ip='10.70.230.179', mcc=311, mnc=489, tac=788,
#          default_ssh_connection_details=SshServiceDetails(
#          addr='10.70.230.179', username='nokia', password='nokia123'),
#          dir_path='/home/nokia/WTS_QT_NEW', cfg_filename='basic_wts_cy.cfg',
#          edaemon_port='22222', egate_port='20000')

# 5GRU for classicalBTS
# PB for RU
_ru_1_pdu = HBTE(addr="10.101.45.170", port_numbers=[4])
_ru_1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.37.128",
        username="rfsw",
        password="HfBKgqIOogKY3BlGtiniuCI9bs76C8jYsAY6vw8f/Tw=",
    ),
    # lmp_connection=SshServiceDetails(addr='192.168.100.3', username='root', password='umniedziala'),
    pdu_port=_ru_1_pdu.pdu_ports[4],
    radio_type=RadioTypes.AHPE,
)

# DU for classicalBTS
# gNB LMP IP
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

# gNB_capacity_unit
_capacity_unit = CapacityUnit(
    addr="192.168.253.20",
    hardware_type="ABIN",
)

# gNB_common_unit
_gnb_pdu = HBTE(addr="10.101.45.165", port_numbers=[6])
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[6],
    hardware_type="ASIM",
)
_airscale = Airscale(common_units=[_common_unit_0])


# gNB_RU
_ru_1_cablinks = [
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=1),
        target=Endpoint(unit=_ru_1, label="SFP", port_id=1),
    ),
]

# gNB_DU
_du = DU(
    airscale=_airscale,
    rus=[_ru_1],
    f1_m_ip_addr="10.101.50.203",
    cablinks=_ru_1_cablinks,
)

# CU
# gNB OAM Mplane IP
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.101.50.203",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.101.50.193", ip_prefix_length=27),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.50.203", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.50.203", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.101.50.203",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.101.50.193", ip_prefix_length=27),
    ),
    x2u=NetworkAddress(
        v4="10.101.50.203",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.101.50.193", ip_prefix_length=27),
    ),
    s1u=NetworkAddress(
        v4="10.101.50.203",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.101.50.193", ip_prefix_length=27),
    ),
)

# RealEnb
# _lmp_connection_enb = SshServiceDetails(addr='10.68.89.53', username='toor4nsn', password='oZPS0POrRieRtu')
# _enb_pdu = HBTE(addr='10.68.87.115', port_numbers=[1])
# _common_unit_1 = CommonUnit(lmp_connection=_lmp_connection_enb, capacity_units=[], pdu_port=_enb_pdu.pdu_ports[1])
# _real_enb = Airscale(common_units=[_common_unit_1])
# _lte_real_enb = RealEnb(airscale=_real_enb, rms=None)

# cloud_topology
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ANDROID_SA_ASIMR_ABINB4_AHPE"

# dcap_server
_dcap_1 = DcapBasic(
    connection_details=HttpConnectionDetails(
        addr="10.101.60.56",
        port="",
        username="utfuser",
        password="utfadmin!",
        # addr="10.101.60.40", port="", username="dcapuser", password="dcapadmin!"
    )
)


# classicalbts
_classical_bts = ClassicalBts(
    dus=[_du], cu=_cu, instance_id=861, global_bts_id=861, dcap=_dcap_1
)

# test pc
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.172",
        username="dcapuser",
        password="iW_K#8.ute%A10h0m0ra",
        port=49151,
    )
)

# host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.70.230.169", username="ute", password="uteUTE!"
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_classical_bts.dus[0].airscale.common_units[0],
            interface_type="lmp",
        )
    ],
)

_lss = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.157.233", port="22", username="coam", password="zO&n1W*ktp7"
    )
)

# Android UE
_appserver_ssh = SshServiceDetails(
    addr="10.57.191.238", username="vrf3_sg6", password="vrf3@sg6", port="57861"
)
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.238",
    iperf_path="/usr/bin/iperf",
    port=57861,
)
_appserver = AppServer(_iperf)
_appserver.iperf_details.port = 57861

_ue1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.101.50.237", username="nokia5G", password="noki@123"
    ),
    serial_number="9YS0220818001286",
    # '9YS0220103005528', # 'L8K5T19919002146',# 'QKX4C20415011221'
    server_dir="/cygdrive/c/pyro_server",
    python_path="/cygdrive/c/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["REAL_ANDROID_UE", "Huawei"],
    # qcat_path='C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe',
    # diag_cfg_path='C:/pyro_server/DIAG.cfg',
    # serial_com='12',
    # reset_interface='no',
    # enable_disable_cfun='yes',
    # processes_to_kill=['ttermpro', 'ATCom'],
    # ue_class = 'QualcommNoLicenseUe',
    # turn_off_on_firewall='yes',
    # diag_com='10',
    # iperf_directory ='adb shell /data/iperf'
)

# switch Dtor
# _dell_s4048on_ssh = SshServiceDetails(addr='0.0.0.0', port='1', username='5gran', password='nokia123')
# _dell_s4048on_switch = DellS4048ONSwitch(_dell_s4048on_ssh)

# switch Mtor
# _dell_s4048ton_ssh = SshServiceDetails(addr='0.0.0.0', port='1', username='5gran', password='nokia123')
# _dell_s4048ton_switch = DellS4048TONSwitch(_dell_s4048ton_ssh)

# attenuator
# _attenuator = HBTE(
#    ip_addr='10.101.45.165',
#    port=23,
#    attenuation_port_numbers=[6])

tl = TestLine(
    test_pc=_host,
    # test_pcs=[_test_pc, _lss, _dcap_1, _dcap_2],
    # test_pcs=[_test_pc, _lss],
    test_pcs=[_host, _lss],  # syj
    gnbs=[_classical_bts],
    # enbs=[_lte_real_enb],
    core=RealCore(mcc=1, mnc=1),
    tl_cloud_topology=_tl_cloud_topology,
    nms=_netact,
    ues=[_ue1],
    # attenuator=_attenuator,
    # switches=[_dell_s4048on_switch, _dell_s4048ton_switch],
    appserver=_appserver,
)
