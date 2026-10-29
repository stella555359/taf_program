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
from taf.config.testline import Connection
from taf.config.testline.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline import Enb, SimEnb, RealEnb, LTEEmuEnb, PrismaEnb, DocomoEnb
from taf.config.testline.appserver import AppServer
from taf.config.testline.lmi import LMI, Local


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


__maintainer__ = "Susana Yan"
__team__ = (
    "I_NSB_MN_RAN_RD_VRF_HAZ3_07_GMS <I_NSB_MN_RAN_RD_VRF_HAZ3_07@internal.nsn.com>"
)
__email__ = "susana.yan@nokia-sbell.com"

# common
__all__ = ["tl"]
_cfg_dir = os.path.dirname(os.path.abspath(__file__))


# 5GRU for classicalBTS
_ru_lmi_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.64.57.254", username="mn5gran", password="nokia123@"
    )
)

#_ru_lmi_2 = LMI(product_code="",
#              host=_ru_lmi_pc,
#              uart_mapping=[Local(port="COM3"), Local(port="COM4")])
              
_ru_lmi_1 = LMI(product_code="",
              host=_ru_lmi_pc,
              uart_mapping=[Local(port="COM3")])

_ru_0_pdu = HBTE(addr="10.64.49.4", port_numbers=[5])
_ru_0 = RU(
    #'AEQY'
    ru_hw_group="AEQY",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2", username="serviceuser", password="bobuWrUHk7Xq7WPpY9ZcjEi8zNdX3plZ+/y420RZ7W4="


    ),
    lmp_connection=SshServiceDetails(
        addr="10.64.57.254", username="mn5gran", password="nokia123@"
    ),
    pdu_port=_ru_0_pdu.pdu_ports[5],
    radio_type=RadioTypes.AEQY.value,
    serial_number="1M224419766",
    lmi=_ru_lmi_1
)

# TL info: PA info
# Attenuator
#_attenuator = TopYoung(
_attenuator = AHBTE(
    ip_addr="10.64.56.198",
    port=5000,
    attenuation_port_numbers=[7,8,9,10],
    model="PA-16-16-6-127-0.5-B-S",
)

##DU for classicalBTS

_lmp_connection = SshServiceDetails(
    addr="10.64.54.136", username="toor4nsn", password="oZPS0POrRieRtu"
)



_capacity_unit_1 = CapacityUnit(addr="192.168.253.20")
_gnb_pdu = HBTE(addr="10.64.49.3", port_numbers=[2])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit_1],
    pdu_port=_gnb_pdu.pdu_ports[2],
)

_airscale = Airscale(common_units=[_common_unit_0])
_du = DU(airscale=_airscale, rus=[_ru_0], f1_m_ip_addr="10.64.54.136")
##CU oam


_cu = CU(
    backhaul_site_oam_ip="",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.64.54.136", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.64.54.136", username="Nemuadmin", password="nemuuser"
    ),
)
##cloud_topology
_tl_cloud_topology = "TL2452"
# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, global_bts_id=37342, instance_id=37342)

_appserver_ssh = SshServiceDetails(
    addr="10.57.179.233", username="vrf3_sg7", password="vrf3@sg7"
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.179.233",
    iperf_path="/usr/bin/iperf",
    port="47888",
)

# CI_Detail_UE_Type='Huawei honor 30s'
_android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.64.57.254", username="mn5gran", password="nokia123@"
    ),
    serial_number="FMR0224220016938",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf_details_on_appserver,
    capabilities=["REAL_ANDROID_UE", "Huawei"]
)

_appserver = AppServer(iperf_details=_iperf_details_on_appserver)

##host

_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.107", username="ute", password="iW_K#8.ute%A10h0m0ra"

    ),
    connections=[
        Connection(
            interface="eth1",
            device=_airscale.common_units[0],
            interface_type="lmp",
        )
    ],
)

tl = TestLine(
    test_pc=_host,
    test_pcs=[_host],
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
