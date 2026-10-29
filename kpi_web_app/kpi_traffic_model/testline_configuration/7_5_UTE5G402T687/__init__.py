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
from taf.config.testline.testpc import Connection
from taf.config.testline.core import RealCore
from taf.config.testline.core import EPCSim, LTEEmuCore, PrismaCore
from taf.config.testline.gnb.du import DU, Cablink, Endpoint
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, ATEN, RRB, APC, Gude, HBTE
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
from taf.config.testline.appserver import AppServer
from taf.config.testline import NetworkAddress, RoutingInformation
from taf.config.testline.appserver import TafUeAppServer
from taf.config.testline.taf_ue_data_transfer_protocol import TafUeDataTransferProtocol
from taf.config.testline.ue import TafUeFastmile


__maintainer__ = "Shasha Liu"
__team__ = (
    "I_MN_5G_RAN_IV4_LINE_HZG_5_GMS <I_MN_5G_RAN_IV4_LINE_HZG_5@internal.nsn.com>"
)
__email__ = "shasha.liu@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))


##RealEnb
# _real_enb_pdu = HBTE(addr="10.68.87.53", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.68.88.136", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    # pdu_port=_real_enb_pdu.pdu_ports[6],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(
    system_module=[_common_unit_2],
    airscale=_real_enb,
    oam_ip=NetworkAddress("10.68.88.135"),
    instance_id=2587,
    global_bts_id=2587,

)

_test_pc_enb = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.251.44", username="ute", password="uteUTE!"
    ),
    connections=[],
)

##5GRU for classicalBTS
_ru_pdu = HBTE(addr="10.68.87.55", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru = RU(
    ru_hw_group="below6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.56.2",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    lmp_connection=SshServiceDetails(
        addr="172.22.56.2",
        username="serviceuser",
        password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    pdu_port=_ru_pdu.pdu_ports[2],
    radio_type=RadioTypes.AQQL.value,
)

##DU for classicalBTS
_lmp_connection = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit = CapacityUnit(
    addr="192.168.253.22",
    hardware_type="ABIO",
    rus=[_ru],
)

_gnb_pdu = HBTE(addr="10.68.87.54", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru_cablinks = [
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=1),
        target=Endpoint(unit=_ru, label="SFP", port_id=1),
    ),
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=2),
        target=Endpoint(unit=_ru, label="SFP", port_id=2),
    ),
]

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection,
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[8],
    hardware_type="ASIB",
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(
    airscale=_airscale, rus=[_ru], f1_m_ip_addr="10.68.88.135", cablinks=_ru_cablinks
)

##CU #Auto TL Upgrading
_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.68.88.135",
        vlan_id=None,
        routing_v4=RoutingInformation(
            gateway="10.68.88.129", destIpAddr="10.68.88.135/27"
        ),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.68.88.135", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.68.88.135", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(
        v4="10.68.88.135",
        vlan_id=None,
        routing_v4=RoutingInformation(
            gateway="10.68.88.129", destIpAddr="10.68.88.135/27"
        ),
    ),
    x2u=NetworkAddress(
        v4="10.68.88.135",
        vlan_id=None,
        routing_v4=RoutingInformation(
            gateway="10.68.88.129", destIpAddr="10.68.88.135/27"
        ),
    ),
    s1u=NetworkAddress(
        v4="10.68.88.135",
        vlan_id=None,
        routing_v4=RoutingInformation(
            gateway="10.68.88.129", destIpAddr="10.68.88.135/27"
        ),
    ),
)

##cloud_topology #UTE Type
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ASIBR_ABIOB4_AQQL_ENB"

# classicalbts
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=2587, global_bts_id=2587)

##host #Local VM
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.251.44", username="ute", password="uteUTE!"
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_classical_bts.dus[0].airscale.common_units[0],
            interface_type="lmp",
        )
    ],
)

_test_pc_gnb = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.251.44", username="ute", password="uteUTE!"
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_classical_bts.dus[0].airscale.common_units[0],
            interface_type="lmp",
        )
    ],
)

# # netact  kongfu
_netact = Netact("10.106.161.25")

_appserver_ssh = SshServiceDetails(
    addr="10.57.191.247", username="vrf4_sg5", password="vrf4@sg5", port="55905"
)  # for UL
_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.191.247",
    iperf_path="/data/data/com.nokia.syve.uemanager.mobile/",
    port="55906",
)
_appserver = AppServer(_iperf)
# _appserver.iperf_details.port = 55905 #for DL

# CI_Detail_UE_Type='Huawei Mate 30 Pro 5G'

_ue1 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.68.86.179", username="mn5gran", password="nokia123@"
    ),
    serial_number="9YS0220110015254",  #'9YS0220103005528',##'L8K5T19919002146',
    server_dir="/cygdrive/c/pyro_server",
    python_path="/cygdrive/c/Python27/python.exe",
    iperf_details=_iperf,
    capabilities=["HUAWEI Mate 30 Pro", "cell_Mapping: [1]", "huawei"],
    # serial_com='12',
    # reset_interface='no',
    # enable_disable_cfun='yes',
    # processes_to_kill=['ttermpro', 'ATCom'],
    # ue_class = 'QualcommNoLicenseUe',
    # turn_off_on_firewall='yes',
    # diag_com='10',
    # iperf_directory ='adb shell /data/iperf'
)
# for FastMile CPE 3.2
_fastmile_appserver_1 = TafUeAppServer(
    app_server_name="APP_SERVER_1",
    address="10.57.191.247",
    user="vrf4_sg5",
    password="vrf4@sg5",
    bind_interface_ip="10.57.191.247",
    expected_prompt="[vrf4_sg5@appserver ~]$ ",
    binary_path="/home/vrf4_sg5/taf_debug/iperf",
    ports=[55905, 55907],
)

_fastmile_data_transfer_1 = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_fastmile_appserver_1,
    interval=1,
    binary_path="iperf",
    version=2,
)


_fastmile_1 = TafUeFastmile(
    com_port="8",
    ue_pc_address="10.68.86.179",
    root_password="542ae5228b73",
    ue_manage_ip="192.168.1.1",
    serial_number="LPL22140067F",
    data_transfer=[_fastmile_data_transfer_1],
    version="3.2",
    ue_pc_port=5555,
    capabilities=["REAL_FASTMILE_UE2", "nokia_fastmile"],
)
#_fastmile_1 = TafUeFastmile(
#    ue_pc_address="10.68.86.179",
#    root_password="Ndqb4mMH=tp_@gFc",
#    default_user_password="ZY9rjZ-w76t.oU,!",
#    ue_manage_ip="192.168.0.1",
#    serial_number="KLT232200B35",
#    version="Receiver 5G19-A",
#    data_transfer=[_fastmile_data_transfer_1],
#    ue_pc_port=5555,
#    capabilities=["REAL_FASTMILE_UE1", "nokia_fastmile"],
#    )


tl = TestLine(
    test_pc=_host,
    test_pcs=[_test_pc_gnb],
    gnbs=[_classical_bts],
    nms=_netact,
    enbs=[_lte_real_enb],
    ues=[_fastmile_1],
    appserver=_appserver,
    tl_cloud_topology=_tl_cloud_topology,
)

# old version keyword under robotws5g/resource compatibility workaround
# tl = TestlineWrapper(tl)
