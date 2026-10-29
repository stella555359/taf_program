import os
import yaml
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
from taf.config.testline.attenuator import HBTE as AHBTE
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, ATEN, RRB, APC, Gude, HBTE
from taf.config.testline import RU, DU
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import Qualcomm, QualcommUeType, Android
from taf.config.testline import Enb, SimEnb, RealEnb, LTEEmuEnb, PrismaEnb, DocomoEnb
from taf.config.testline.switch import DellS4048ONSwitch, DellS4048TONSwitch
from taf.config.testline.nms import Netact
from taf.config.testline.gnb.networkaddress import NetworkAddress

__maintainer__ = "chen yili"
__team__ = (
    "I_NSB_MN_RAN_RD_VRF_HAZ3_07@internal.nsn.com"
)
__email__ = "yili.chen@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# testPc(taf)
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.71.187.138", username="ute", password="tribe!L3SW1CN@"
    )
)

# 5GRU for classicalBTS

# PB for RU
_ru_pdu = HBTE(addr="10.71.182.30", port_numbers=[1])

_ru = RU(
    ru_hw_group="AEQE",
    serial_number="DH223803733",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="rfsw", password="gSDBExyEbO33komYWL6iPrtSaYc5XimHAGrsJ/K8+AY="
    ),
    lmp_connection=SshServiceDetails(
        addr="10.71.180.133", username="tester5g", password="Nokia123!"
    ),
    pdu_port=_ru_pdu.pdu_ports[1],
)

_ru_pdu2 = FACOM(addr="10.71.180.45", port_numbers=[1])
_ru2 = RU(
    ru_hw_group="AVQC",
    serial_number="1M240305752",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.100.1", username="rfsw", password="f6gh0K2nXq0O8XqVFkUuMtJnzuKm0U3box0QcYgugn0="
    ),
    lmp_connection=SshServiceDetails(
        addr="10.71.182.43", username="tester5g", password="Nokia123!"
    ),
    pdu_port=_ru_pdu2.pdu_ports[1],
)


# TL info: PA info
# Attenuator
#_attenuator = TopYoung(
_attenuator = AHBTE(
    ip_addr="10.71.180.137",
    port=5000,
    attenuation_port_numbers=[1,2],
    model="PA-16-16-6-127-0.5-B-S",
)

# gNB LMP IP
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
# ABIM internal ip
_capacity_unit = CapacityUnit(addr="192.168.253.20")
# gNB PB
_gnb_pdu = HBTE(addr="10.71.182.49", port_numbers=[1])
_gnb_test_pc_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.71.187.138", username="ute", password="tribe!L3SW1CN@"
    )
)
_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[1],
    test_pc=_gnb_test_pc_0,
)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(airscale=_airscale, rus=[_ru, _ru2], f1_m_ip_addr="10.106.174.130")

# gNB OAM M-plane IP
_cu = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.106.174.130", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.106.174.130", username="Nemuadmin", password="nemuuser"
    ),
)

# RealEnb
_lmp_connection_enb = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)
_enb_pdu = FACOM(addr="10.71.180.173", port_numbers=[1])
_enb_pc_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.71.180.136", username="tester5g", password="Nokia123!"
    )
)
_common_unit_1 = CommonUnit(
    lmp_connection=_lmp_connection_enb,
    capacity_units=[],
    pdu_port=_enb_pdu.pdu_ports[1],
    test_pc=_enb_pc_0,
    hardware_type=None,
)
_real_enb = Airscale(common_units=[_common_unit_1])
_lte_real_enb = RealEnb(
    system_module=_real_enb,
    rms=None,
    oam_ip=NetworkAddress(v4="10.106.174.7"),
    instance_id=2465,
)

##cloud_topology
_tl_cloud_topology = "CLOUD_5G_MP"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=2455)
## switch Dtor
_dell_s4048on_ssh = SshServiceDetails(
    addr="10.57.129.120", port="1/9", username="5gran", password="nokia123"
)
_dell_s4048on_switch = DellS4048ONSwitch(_dell_s4048on_ssh)

## switch Mtor
_dell_s4048ton_ssh = SshServiceDetails(
    addr="10.57.129.136", port="1/18", username="5gran", password="nokia123"
)
_dell_s4048ton_switch = DellS4048TONSwitch(_dell_s4048ton_ssh)

_netact = Netact("10.107.178.214")

#iperf
_appserver_ssh = SshServiceDetails(
    addr="10.71.187.33", username="ute", password="Ut3pa5s#ff97", port="47666"
)
_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.187.33",
    iperf_path="/usr/bin/iperf",
    port="47622",
)

# CI_Detail_UE_Type='Huawei honor 30s'
_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.180.133", username="tester5g", password="Nokia123!"
    ),
    serial_number="XPL5T19A24031418",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf_details_on_appserver,
    capabilities=["REAL_ANDROID_UE", "Huawei"],
)

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    enbs=[_lte_real_enb],
    tl_cloud_topology=_tl_cloud_topology,
    #nms=_netact,
    ues=[_android],
    #switches=[_dell_s4048on_switch, _dell_s4048ton_switch],
)
