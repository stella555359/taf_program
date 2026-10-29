__maintainer__ = "Liu Yuanyuan"
__team__ = "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_03@internal.nsn.com"  # TL owner's team
__email__ = "yuanyuan.liu@nokia-sbell.com"

import os

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
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.core import EPCSim
from taf.config.testline.core import RealCore
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import ClassicalBts, CU
from taf.config.testline.enb import RealEnb
from taf.config.testline.ue import TM500, Android
from taf.config.testline import DU, RU
from taf.config.testline.attenuator import HBTE as AHBTE
from taf.config.testline.testpc import Connection
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, HBTE, FPFH
from taf.config.testline.radio import RadioModule
from taf.config.testline import IperfDataTransferDetails
from taf.config.testline.appserver import AppServer
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

_attenuator = AHBTE(
    ip_addr="10.71.203.155", port="5000", attenuation_port_numbers=[9, 10, 11, 12]
)

_lmp_connection_0 = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_0 = CapacityUnit(
    addr="192.168.253.17",
    hardware_type="ABIP",
)

# DU
_common_unit_pdu = HBTE(addr="10.71.195.101", port_numbers=[6])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection_0,
    capacity_units=[_capacity_unit_0],
    pdu_port=_common_unit_pdu.pdu_ports[6],
    hardware_type="ASIM",
)



_cu = CU(
    backhaul_site_oam_ip="10.71.209.43",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.209.43", username="toor4nsn", password="oZPS0POrRieRtu", port="22"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.209.43", username="Nemuadmin", password="nemuuser"
    ),
)



# 5G RU
_ru_pdu = FPFH(addr="10.71.195.98", port_numbers=[5])

_ru = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.2", username="serviceuser", password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og="
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.0.2", username="serviceuser", password="kQ2QZWY22987AsO4QaK/Yzj/gh3yksrLESosPRHF6Og="
    ),
    pdu_port=_ru_pdu.pdu_ports[5],
    radio_type="AVQY",
    attenuation_ports=[
        _attenuator.attenuator_ports[9],
        _attenuator.attenuator_ports[10],
        _attenuator.attenuator_ports[11],
        _attenuator.attenuator_ports[12],
    ],
)



_appserver_ssh = SshServiceDetails(
    addr="10.57.191.235", username="vrf3_sg3", password="vrf3@sg3", port="43702"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.157.134",
    iperf_path="/usr/bin/iperf",
    # iperf_path='/cygdrive/c/iperf',
    port="43702",
    ports=["43666", "43667", "43668", "43702", "43670", "43671", "43672", "43673"],
)


# #Qualcomm

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.157.134",
    iperf_path="iperf",
    port="43702",
)

_appserver = AppServer(_iperf_details_on_appserver)

_android_0 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.0.176.6", username="MN5GRAN", password="nokia123@"
    ),
    serial_number="ec55aac3",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python310/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_UE", "qct_dx50"],
)


# airscale
_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru], f1_m_ip_addr="10.71.209.43")

# cloud_topology
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ANDROID_SA_ASIML_ABIPB1_AVQY"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=2071, global_bts_id=2071)

# Testpc
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.217.69", username="ute", password="uteUTE!"
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_classical_bts.dus[0].airscale.common_units[0],
            interface_type="lmp",
        )
    ],
)

tl = TestLine(
    test_pc=_test_pc,
    gnbs=[_classical_bts],
    core=RealCore(mcc=262, mnc=3),
    attenuator=_attenuator,
    ues=[_android_0],
    appserver=_appserver,
    tl_cloud_topology=_tl_cloud_topology,

)


__all__ = ["tl"]
