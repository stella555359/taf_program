__maintainer__ = "UTE team"
__team__ = "UTE team"
__email__ = "ute@nokia.com"
__owner_email__ = "UTE Lab Team"


import os
import yaml
from taf.config.testline.testline import TestLine
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.testpc import TestPc
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline.gnb.networkaddress import NetworkAddress
from taf.config.testline.gnb.du import Cablink, Endpoint
from taf.config.testline import Airphone
from taf.config.testline.pdu import FACOM
from taf.config.testline.appserver import AppServer
from taf.config.testline.attenuator import HBTE, JFW
from taf.config.testline.core import RealCore
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)
from taf.config.testline.enb import (
    RealEnb,
)
from taf.config.testline.ue import (
    AirphoneCloud,
    Airphone,
    Prisma,
    Android,
    Qualcomm,
    QualcommUeType,
)
_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

## attenuator
_attenuator = JFW(
    ip_addr="10.69.70.47",
    port=3001,
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8],
    model="50PA-574",
)

# Iperf
_appserver_ssh = SshServiceDetails(
    addr="10.69.69.213", username="ute", password="iW_K#8.ute%A10h0m0ra", port="54015"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.69.9.10",
    iperf_path="iperf",
    port="54015",
)

_appserver = AppServer(_iperf)

## DU for classicalBTS
_gnb_pdu = FACOM(addr="10.69.71.48", port_numbers=[5])

_capacity_unit = CapacityUnit(
    addr="192.168.253.20",
    hardware_type="ABIO",
)

_common_unit = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.1",
        # addr="10.69.70.46",
        username="toor4nsn",
        password="oZPS0POrRieRtu"
    ),
    capacity_units=[_capacity_unit],
    pdu_port=_gnb_pdu.pdu_ports[5],
    hardware_type="ASIB",
)

_airscale = Airscale([_common_unit])

# 5GRU for classicalBTS
_ru_0_pdu = FACOM(addr="10.69.69.226", port_numbers=[5])

_ru_0 = RU(
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52", username="root", password="root"
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.254.52", username="root", password="root"
    ),
    ru_hw_group="AZQP",
    radio_type="AZQP",
    pdu_port=_ru_0_pdu.pdu_ports[5],
    serial_number=None,
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

_ru_cablinks = [
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=1),
        target=Endpoint(unit=_ru_0, label="SFP", port_id=1),
    )
]
_cu = CU(
    backhaul_site_oam_ip="10.69.70.46",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.69.70.46", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.69.70.46", username="Nemuadmin", password="nemuuser"
    ),
    x2c=NetworkAddress(v4="10.108.233.27", vlan_id=None),
    x2u=NetworkAddress(v4="10.108.233.27", vlan_id=None),
    s1u=NetworkAddress(v4="10.108.233.27", vlan_id=None),
)

_du = DU(airscale=_airscale, rus=[_ru_0], f1_m_ip_addr="10.69.70.46", cablinks=_ru_cablinks)

_classical_bts = ClassicalBts(cu=_cu, dus=[_du], instance_id=10674, global_bts_id=10674)

# Beginning -- set enb with enb format
_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.1", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_capacity_unit],
    # pdu_port=_real_enb_pdu.pdu_ports[3],
)

_real_enb1 = Airscale(common_units=[_common_unit_2])

_lte_real_enb1 = RealEnb(
    airscale=_real_enb1,
    rms=None,
    instance_id=10674,
    global_bts_id=10674,
    oam_ip=NetworkAddress(
        v4="10.69.70.46",
    ),
)
# End -- set enb with enb format

_xiaomi11 = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.69.68.199", username="csv1-tester", password="Nokia123!"
    ),
    serial_number="75ce19a3",
    server_dir="/cygdrive/c/pyro_server",
    python_path="/cygdrive/c/Python27/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/qcat.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["Commercial", "xiaomi12"],
)

_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.69.69.213", username="ute", password="iW_K#8.ute%A10h0m0ra"
    ),
    connections=[_classical_bts.dus[0].airscale.common_units[0], _xiaomi11],
)

tl = TestLine(
    test_pc=_test_pc,
    # gnbs=[_classical_bts],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_Xiaomi_ASIB_ABIO_AZQP",
    ues=[_xiaomi11],
    enbs=[_lte_real_enb1],
    appserver=_appserver,
    core=RealCore(mcc=460, mnc=0),
    attenuator=_attenuator,
)

__all__ = ["tl"]
