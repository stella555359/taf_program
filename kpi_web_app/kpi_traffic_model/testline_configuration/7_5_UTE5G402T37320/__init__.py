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
from taf.config.testline import RU, DU, AppServer
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import AirphoneCloud, Airphone, Prisma, TM500, Android
from taf.config.testline import Enb, SimEnb, RealEnb, LTEEmuEnb, PrismaEnb, DocomoEnb
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline.dcap import DcapRnD, DcapBasic
from taf.config.testline.nms import Netact

__maintainer__ = "Ma mike"  # TL owner name
__team__ = "mike.ma@nokia-sbell.com"  # TL owner's team
__email__ = "mike.ma@nokia-sbell.com"  # TL owner's email

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

##host
# _host = TestPc(
#     default_ssh_connection_details=SshServiceDetails(addr='10.57.167.31', username='root', password='nokia123'))

_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.159.112", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

#_dcap_1 = DcapBasic(
#    connection_details=HttpConnectionDetails(
#        addr="10.101.60.40", port="443", username="dcapuser", password="dcapadmin!"
#    )
#)
#_dcap_2 = DcapBasic(
#    connection_details=HttpConnectionDetails(
#        addr="10.101.60.56", port="443", username="dcapuser", password="dcapadmin!"
#    )
#)

#_lss = TestPc(
#    default_ssh_connection_details=SshServiceDetails(
#        addr="10.57.157.233", port="22", username="coam", password="zO&n1W*ktp7"
#    )
#)

# _netact = Netact(addr="10.107.183.26", username="omc", password="Nokia126_")  # 10.107.183.26--NetAct5-Han
#_netact = Netact(addr="10.108.248.82")  # 10.108.248.82--NetAct4-Chen(Gansu)

# epc_sim
# _epcsim = EPCSim(mme_ip='10.57.157.63', mcc=311, mnc=489, tac=788,
#          default_ssh_connection_details=SshServiceDetails(
#          addr='10.57.157.63', username='nokia', password='nokia123'),
#          dir_path='/home/nokia/WTS_QT_NEW', cfg_filename='basic_wts_cy.cfg',
#          edaemon_port='22222', egate_port='20000')

##Cobham

# 5GRU for classicalBTS
# _ru_pdu = FACOM(addr='10.57.242.26', port_numbers=[2])
#
# _ru = RU(
#     ru_hw_group='hw_group',
#     default_ssh_connection_details=SshServiceDetails(addr='192.168.254.52', username='root', password='root'),
#     lmp_connection=SshServiceDetails(addr='172.16.1.5', username='root', password='umniedziala'),
#     pdu_port=_ru_pdu.pdu_ports[2])

#########ClassicalBts##########
#########5G RU##########
_5g_ru_pdu = FACOM(addr="10.64.49.18", port_numbers=[1, 2, 3, 4, 5, 6])

_ru = RU(
    ru_hw_group="cmw",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.49", username="serviceuser", password="7B+6yyInfX0uES/FP60uEyhjZHUxB2MoRWvZqUMW42g="
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.102.1", username="serviceuser", password="7B+6yyInfX0uES/FP60uEyhjZHUxB2MoRWvZqUMW42g="
    ),
    pdu_port=_5g_ru_pdu.pdu_ports[1],
    radio_type="AEHC",
)

##DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.64.54.67", username="toor4nsn", password="oZPS0POrRieRtu"
)
_capacity_unit = CapacityUnit(addr="192.168.253.20")
_common_unit_pdu = FACOM(addr="10.64.49.28", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])



_common_unit = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_common_unit_pdu.pdu_ports[3],
    hardware_type="ASIB",
    hardware_version="A.103",
)

_airscale = Airscale(common_units=[_common_unit])
_du = DU(
    airscale=_airscale,
    rus=[_ru],
    f1_m_ip_addr="10.64.54.67",
    f1_c_ip_addr="10.64.54.67",
    f1_u_ip_addr="10.64.54.67",
)


_cu = CU(
    backhaul_site_oam_ip="10.64.54.67",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.64.54.67", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.64.54.67", username="Nemuadmin", password="nemuuser"
    ),
)
_classical_bts = ClassicalBts(cu=_cu, dus=[_du])


# QualComm UE
_appserver_ssh = SshServiceDetails(
    addr="10.57.162.13", username="vrf4_sg12", password="vrf4@12", port="22340"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.162.13",
    iperf_path="/usr/bin/iperf",
    port=22340,
)

_iperf_ul = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.162.13",
    iperf_path="iperf",
    port=22350,
)
_appserver = AppServer(iperf_details=_iperf_ul)

## CI_Detail_UE_Type='Huawei Honor 30s'
# _android = Android(
#    ssh_connection_details=SshServiceDetails(
#        addr="10.68.86.53", username="nokia5G", password="noki@123"
#    ),
#    serial_number="9EQUT20721010191",
#    server_dir="/cygdrive/c/pyro_server",
#    python_path="C:/Python27/python.exe",
#    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
#    diag_cfg_path="C:/pyro_server/DIAG.cfg",
#    iperf_details=_iperf,
#    capabilities=["REAL_ANDROID_UE", "HUAWEI"],
# )

# askey
_ue_config_path = os.path.join(_cfg_dir, "TestData/askey.yml")
if os.path.isfile(_ue_config_path):
    with open(_ue_config_path) as f:
        _ue_askey = f.read()
        qci_port = re.findall("(_iperf.*?port)", _ue_askey)
        for item in qci_port:
            _ue_askey = _ue_askey.replace(item, str(eval(item)))
        _ue_config = yaml.safe_load(_ue_askey)
else:
    _ue_config = ""
# askey

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    #    enbs=[_lte_real_enb],
    tl_cloud_topology="hgz-tl1003",
    #nms=_netact,
    # ues=[_android],
    ues=[_ue_config],
    #test_pcs=[_dcap_1, _lss],
    appserver=_appserver,
)
