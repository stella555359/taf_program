__maintainer__ = "Chen Jian"
__team__ = (
    "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_05_GMS <I_NSB_MN_5GSC_MMW_SC_PZ_HZ_05@internal.nsn.com>"
)
__email__ = "jian.1.chen@nokia.com"

import os
import shutil

from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.testpc import TestPc, Connection
from taf.config.testline import DU, RU, RealEnb
from taf.config.testline.pdu import ATEN, PduPort, TopYoung
from taf.config.testline.gnb import ClassicalBts, CU
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.core import RealCore, PCF
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb.networkaddress import NetworkAddress  # add in taf.meta 5.4
from taf.config.testline.gnb.du import Cablink, Endpoint
from taf.config.testline.radio import (
    RadioTypes,
    SCRadioTypes,
    RU,
    SC5GRadio,
    SC4GRadio,
    RadioModule,
)
from taf.config.testline.ue import TafUeAndroid
from taf.config.testline.attenuator import HBTE as AHBTE
from taf.config.testline.appserver import TafUeAppServer
from taf.config.testline import TafUeDataTransferProtocol
from taf.config.testline.pdn import PDNTafUeAndroidDetails

from collections import OrderedDict

os.environ["INIT_CONFIG_FILE_PATH"] = os.path.dirname(os.path.abspath(__file__))

__all__ = ["tl"]

os.environ["ABSTRACT_LIB_CONFIG"] = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "ue_config.yaml"
)

# Enb
_common_unit_1 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
)

_real_enb = Airscale(common_units=[_common_unit_1])

_lte_real_enb = RealEnb(
    airscale=_real_enb, rms=None, instance_id=2032, global_bts_id=10444
)


_ru_pdu0 = TopYoung(addr="10.71.195.66", port_numbers=[1,3])
_ru_pdu1 = TopYoung(addr="10.71.195.69", port_numbers=[2])

_ru0 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52",
        username="serviceuser",
        password="oBrd1RgbOasUtYAeVfxrW9yGHb6ONl0w+MJUoKrBMGE="
    ),
    lmp_connection=SshServiceDetails(
        addr="172.21.1.21", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru_pdu0.pdu_ports[1],
    radio_type=RadioTypes.AWHQN.value,
    serial_number="1M254313949",
    product_code="476257A.101",
)

_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52",
        username="serviceuser",
        password="oBrd1RgbOasUtYAeVfxrW9yGHb6ONl0w+MJUoKrBMGE="
    ),
    lmp_connection=SshServiceDetails(
        addr="172.21.1.21", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru_pdu0.pdu_ports[3],
    radio_type=RadioTypes.AWHQN.value,
    serial_number="1M254313950",
    product_code="476257A.101",
)

_ru2 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="192.168.254.52",
        username="serviceuser",
        password="oBrd1RgbOasUtYAeVfxrW9yGHb6ONl0w+MJUoKrBMGE="
    ),
    lmp_connection=SshServiceDetails(
        addr="172.21.1.21", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru_pdu1.pdu_ports[2],
    radio_type=RadioTypes.AWHQN.value,
    serial_number="1M254313954",
    product_code="476257A.101",
)

_du0_pdu = TopYoung(addr="10.71.195.69", port_numbers=[4])

_common_unit_0_pdu_port = PduPort(pdu=_du0_pdu, port_no="4")

#_du0_capacity_unit_L_0 = CapacityUnit(addr="192.168.253.20")

#_du0_master_capacity_unit_L_0 = CapacityUnit(addr="fsp-1-1a")

#_du0_slave_capacity_unit_L_0 = CapacityUnit(addr="fsp-1-1b")

#_du0_fpga_capacity_unit_L_0 = CapacityUnit(addr="fsp-1-1c")

#_du0_capacity_unit_L_1 = CapacityUnit(addr="192.168.253.24")

#_du0_master_capacity_unit_L_1 = CapacityUnit(addr="fsp-1-2a")

#_du0_slave_capacity_unit_L_1 = CapacityUnit(addr="fsp-1-2b")

#_du0_fpga_capacity_unit_L_1 = CapacityUnit(addr="fsp-1-2c")

#_du0_capacity_unit_L_2 = CapacityUnit(addr="192.168.253.28")

#_du0_master_capacity_unit_L_2 = CapacityUnit(addr="fsp-1-3a")

#_du0_slave_capacity_unit_L_2 = CapacityUnit(addr="fsp-1-3b")

#_du0_fpga_capacity_unit_L_2 = CapacityUnit(addr="fsp-1-3c")

_app_server_1 = TafUeAppServer(
    app_server_name="APP_SG5",
    address="10.57.191.249",
    user="vrf3_sg5",
    password="vrf3@sg5",
    ports=[45001,45023,45024],
)

_data_transfer_iperf = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_app_server_1,
    interval=1,
    server_close_delay=50,
)

_pdn1 = PDNTafUeAndroidDetails(
    entryName="dxdata2", apnName="dxdata2", apnType=["DEFAULT"]
)

_android = TafUeAndroid(
    ssh_connection_details=SshServiceDetails(
        addr="10.71.217.41", username="nokia5G", password="noki@123"
    ),
    ue_pc_address="10.71.217.41",
    proxy_mngr_port="9955",
    serial_number="1ed5da5d",  # f1318050
    data_transfer=[_data_transfer_iperf],
    pdns=[_pdn1],
    capabilities=["REAL_UE", "qualcomm"],
)

_capacity_unit = CapacityUnit(addr="192.168.253.20", hardware_type="ASOH", rus=[_ru0, _ru1, _ru2])

_common_unit_0_L = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_capacity_unit],
    pdu_port=_common_unit_0_pdu_port,
    hardware_type="ASOH",
    hardware_version="A101",
    serial_number="L1241401977",
)

_airscale = Airscale(common_units=[_common_unit_0_L])

# Cablinks should be defined in the bottom of DU section
_ru_cablinks = [
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=1),
        target=Endpoint(unit=_ru0, label="SFP", port_id=1),
    ),
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=2),
        target=Endpoint(unit=_ru1, label="SFP", port_id=1),
    ),
    Cablink(
        source=Endpoint(unit=_capacity_unit, label="SFP", port_id=3),
        target=Endpoint(unit=_ru2, label="SFP", port_id=1),
    ),
]

_du = DU(airscale=_airscale, rus=[_ru0,_ru1,_ru2], f1_m_ip_addr="10.71.208.199", cablinks=_ru_cablinks)

_cu = CU(
    backhaul_site_oam_ip="10.71.208.199",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.208.199", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.208.199", username="Nemuadmin", password="nemuuser", port=443
    ),
)

_cbts = ClassicalBts(cu=_cu, dus=[_du], instance_id=2001, global_bts_id=10899)

# Test VM
_test_vm = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.251.39", username="ute", password="uteUTE!"
    ),
    connections=[
        Connection(
            interface="eth1",
            device=_cbts.dus[0].airscale.common_units[0],
            interface_type="lmp",
        )
    ],
)

# RealCore
_pcf = PCF(
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.217.23", username="feat1", password="Nokia@123"
    )
)
_realcore = RealCore(pcf=_pcf)

_tl_cloud_topology = "CLOUD_5G_CLASSICAL_MINI_ASIBL_ABIO1_AEUD"

_attenuator = AHBTE(
    ip_addr="10.101.51.50",
    port=5000,
    attenuation_port_numbers=[1, 2, 3, 4],
    model="PA-16-16-6-127-0.5-B-S",
)

tl = TestLine(
    test_pc=_test_vm,
    gnbs=[_cbts],
    tl_cloud_topology=_tl_cloud_topology,
    core=_realcore,
    enbs=[_lte_real_enb],
    ues=[_android],
    #test_pcs=[_test_vm],
    attenuator=_attenuator,
)