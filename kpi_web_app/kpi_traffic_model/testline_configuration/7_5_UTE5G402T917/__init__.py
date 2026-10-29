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
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, ATEN, RRB, APC, Gude, HBTE
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
#    HBTE,
    Hytem,
    RadioRack,
)
from taf.compatibility.configuration import TestlineWrapper

__maintainer__ = "lixia.tang"
__team__ = "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_03@internal.nsn.com"
__email__ = "lixia.tang@nokia-sbell.com"


PARAMS_TO_MODIFY_TL = [
    dict(
        value="10.68.90.44",
        dist_name="MRBTS-917/TNLSVC-1/TNL-1/IPNO-1/IPIF-1/IPADDRESSV4-1",
        p_name="localIpAddr",
    ),
]

LIST_ITEM_TO_ADD_TL = [
    dict(
        dist_name="MRBTS-917/TNLSVC-1/TNL-1/IPNO-1/IPRT-1",
        list_name="staticRoutes",
        elements={
            "destIpAddr": "0.0.0.0",
            "destinationIpPrefixLength": "0",
            "gateway": "10.68.90.33",
        },
    ),
]

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# #host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.89", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)


# RealEnb
_real_enb_pdu = FACOM(addr="10.68.87.242", port_numbers=[4])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.68.90.44", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[4],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, instance_id="239")

# attenuator
#_attenuator = HBTE(
#    ip_addr="10.101.51.136",
#    port=5000,
#    attenuation_port_numbers=[1, 9, 2, 10, 3, 11, 4, 12],
#    model="PA-16-16-6-127-0.5-B-S",
#)


# #######Iperf########
_appserver_ssh = SshServiceDetails(
    addr="10.70.222.51", username="mmw_sg3", password="mm@3", port="43121"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.70.222.51",
    iperf_path="/usr/bin/iperf",
    port=43120,
)

# Qualcomm
_android1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.101.47.105", username="nokia5G", password="noki@123"
    ),
    serial_number="R5CT32DDQEB",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_UE", "samsung"],
)

_android2 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.101.47.105", username="nokia5G", password="noki@123"
    ),
    serial_number="R5CN20LYX0Y",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["REAL_UE", "samsung"],
)

# #DU_0 for classicalBTS
_lmp_connection_0 = SshServiceDetails(
    addr="10.68.90.44", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_0 = CapacityUnit(addr="1.1.1.1")

_gnb_pdu = HBTE(addr="10.68.87.242", port_numbers=[4])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection_0,
    capacity_units=[_capacity_unit_0],
    pdu_port=_gnb_pdu.pdu_ports[4],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, f1_m_ip_addr="10.68.90.44")

##CU
_cu = CU(
    backhaul_site_oam_ip="10.68.90.44",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.68.90.44", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.68.90.44", username="Nemuadmin", password="nemuuser"
    ),
)

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id="917", global_bts_id="917")

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.70.222.51",
    iperf_path="iperf",
    port="43121",
)

_appserver = AppServer(_iperf_details_on_appserver)

tl = TestLine(
    test_pc=_host,
    ues=[_android1, _android2],
    gnbs=[_classical_bts],
    # cloud_hostings=[_ncir],
    enbs=[_lte_real_enb],
    # tl_cloud_topology=_tl_cloud_topology,
    appserver=_appserver,
)
