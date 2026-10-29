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
from taf.config.testline import RU, DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, ATEN, RRB, APC, Gude, HBTE
from taf.config.testline.attenuator import HBTE as AHBTE
from taf.config.testline.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline import Enb, SimEnb, RealEnb, LTEEmuEnb, PrismaEnb, DocomoEnb
from taf.config.testline.appserver import AppServer

# added in taf.meta 5.4
from taf.config.testline.ue import (
    AirphoneCloud,
    Airphone,
    Prisma,
    TM500,
    Qualcomm,
    QualcommUeType,
    Android,
)
from taf.config.testline.attenuator import AttenuationPort, TopYoung
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)
from taf.config.testline.gnb.networkaddress import NetworkAddress
#from taf.compatibility.configuration import TestlineWrapper
from taf.config.testline import TafUeDataTransferProtocol
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import SshServiceDetails
from taf.config.testline.appserver import TafUeAppServer
from taf.config.testline.pdu import ATEN
from taf.config.testline.ue import TafUeAt

__maintainer__ = "yili chen"
__team__ = (
    "I_NSB_MN_RAN_RD_VRF_HAZ3_07_GMS <I_NSB_MN_RAN_RD_VRF_HAZ3_07@internal.nsn.com>"
)
__email__ = "yili.chen@nokia-sbell.com"

# common
__all__ = ["tl"]
_cfg_dir = os.path.dirname(os.path.abspath(__file__))

##host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.159.128", username="ute", password="tribe!L3SW1CN@"
    )
)

# 5GRU for classicalBTS
_ru_0_pdu = HBTE(addr="10.64.49.3", port_numbers=[1])
_ru_0 = RU(
    #'AHFIB'
    ru_hw_group="Below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.33.128", username="root", password=""
    ),
    lmp_connection=SshServiceDetails(
        addr="10.64.57.41", username="mn5gran", password="nokia123@"
    ),
    pdu_port=_ru_0_pdu.pdu_ports[1],
)

# TL info: PA info
# Attenuator
#_attenuator = TopYoung(
_attenuator = AHBTE(
    ip_addr="10.106.174.34",
    port=5000,
    attenuation_port_numbers=[7,8,9,10],
    model="PA-16-16-6-127-0.5-B-S",
)

##DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="10.64.54.130", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_1 = CapacityUnit(addr="192.168.253.20")
_gnb_pdu = HBTE(addr="10.64.49.2", port_numbers=[2])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit_1],
    pdu_port=_gnb_pdu.pdu_ports[2],
)
_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(airscale=_airscale, rus=[_ru_0], f1_m_ip_addr="10.64.54.130")
##CU oam
_cu = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.64.54.130", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.64.54.130", username="Nemuadmin", password="nemuuser"
    ),
)
##cloud_topology
_tl_cloud_topology = "CLOUD_5G_VRF"
# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, global_bts_id=37509, instance_id=37509)

_appserver_ssh = SshServiceDetails(
    addr="10.71.187.33", username="ute", password="Ut3pa5s#ff97"
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.71.187.33",
    iperf_path="/usr/bin/iperf",
    port="47100",
)

# CI_Detail_UE_Type='Huawei honor 30s'
_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.106.174.37", username="tester5g", password="Nokia123!"
    ),
    serial_number="XPL5T19A24026737",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf_details_on_appserver,
    capabilities=["REAL_ANDROID_UE", "Huawei"]
)

_appserver = AppServer(iperf_details=_iperf_details_on_appserver)

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    tl_cloud_topology=_tl_cloud_topology,
    ues=[_android],
    appserver=_appserver,
    attenuator=_attenuator,
)
# compatibility workaround
#tl = TestlineWrapper(tl)
if __name__ == "__main__":
    print("Example use of new TL config")
    print("UE_IP is:{}".format(tl.ues[0].data_transfer[0].bind_ue_ip))

