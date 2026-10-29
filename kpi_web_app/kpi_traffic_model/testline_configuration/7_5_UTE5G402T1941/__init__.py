__maintainer__ = "Zhou Leiming"
__team__ = "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_05_GMS"
__email__ = "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_05@internal.nsn.com"
__owner_email__ = "leiming.zhou@nokia-sbell.com"

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
)
from taf.config.testline.testpc import TestPc
from taf.config.testline.core import EPCSim, RealCore
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb import ClassicalBts, CU
from taf.config.testline.enb import RealEnb
from taf.config.testline.ue import TM500, Android
from taf.config.testline import DU, RU, Cablink, Endpoint
from taf.config.testline.attenuator import (
    AttenuationPort,
    TopYoung,
)  # added in taf.meta 5.4
from taf.config.testline.attenuator import HBTE as hbte
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, HBTE, FPFH
from taf.config.testline.radio import RU, RadioTypes
from taf.config.testline import IperfDataTransferDetails
from taf.config.testline import Mitron
from taf.config.testline.appserver import AppServer
from taf.config.testline.pdu import ATEN, PduPort
from taf.config.testline.core import RealCore4G
from taf.config.testline.testline import TestLine
from taf.config.testline import NetworkAddress, RoutingInformation
from taf.config.testline.gnb.du import Cablink, Endpoint
from taf.config.testline.testpc import Connection
from taf.config.testline.dcap import DcapRnD
from taf.config.testline.appserver import TafUeAppServer
from taf.config.testline import TafUeDataTransferProtocol
from taf.config.testline.pdn import PDNTafUeAndroidDetails
from taf.config.testline.ue import TafUeAndroid

_cfg_dir = os.path.dirname(os.path.abspath(__file__))



_cu = CU(
    backhaul_site_oam_ip=NetworkAddress(
        v4="10.57.228.37",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.57.228.33", ip_prefix_length=24),
    ),
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.57.228.37", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.57.228.37", username="Nemuadmin", password="nemuuser", port=443
    ),
    x2c=NetworkAddress(
        v4="10.57.228.37",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.57.228.33", ip_prefix_length=24),
    ),
    x2u=NetworkAddress(
        v4="10.57.228.37",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.57.228.33", ip_prefix_length=24),
    ),
    s1u=NetworkAddress(
        v4="10.57.228.37",
        vlan_id=None,
        routing=RoutingInformation(gateway="10.57.228.33", ip_prefix_length=24),
    ),
)

# DU
_common_unit_pdu = FPFH(addr="10.57.176.6", port_numbers=[2])

_lmp_connection_0 = SshServiceDetails(
    addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_0 = CapacityUnit(
    addr="192.168.253.17",
    hardware_type="ASOE",
)

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection_0,
    capacity_units=[_capacity_unit_0],
    pdu_port=_common_unit_pdu.pdu_ports[2],
    hardware_type="ASOE",
)

# airscale
_airscale_0 = Airscale(common_units=[_common_unit_0])

# 5G RU

_du_pdu = FPFH(addr="10.57.176.6", port_numbers=[1, 2, 3, 4, 5, 6])


_ru_pdu = HBTE(addr="10.57.176.2", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])
_ru_pdu1 = FPFH(addr="10.57.241.196", port_numbers=[1, 2, 3, 4, 5, 6])

_ru = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.56.22.2", username="rfsw", password="f6gh0K2nXq0O8XqVFkUuMtJnzuKm0U3box0QcYgugn0="
    ),
    lmp_connection=SshServiceDetails(
        addr="172.21.1.21", username="root", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru_pdu.pdu_ports[4],
    radio_type="AVNB",
)

_ru1 = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.0.154", username="serviceuser", password="wcdjLlTpqEY3cAmOe11u6aELwGI3rDvpGJQvCkcyHZc="
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.77.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru_pdu1.pdu_ports[1],
    radio_type="AZQJ",
)

_ru_cablinks = [
    Cablink(
        source=Endpoint(unit=_capacity_unit_0, label="SFP", port_id=1),
        target=Endpoint(unit=_ru, label="SFP", port_id=1),
    ),
    Cablink(
        source=Endpoint(unit=_capacity_unit_0, label="SFP", port_id=2),
        target=Endpoint(unit=_ru, label="SFP", port_id=2),
    )    
]

_du_0 = DU(
    airscale=_airscale_0,
    rus=[_ru, _ru1],
    f1_m_ip_addr="10.57.228.37",
    cablinks=_ru_cablinks,
)

_dcap = DcapRnD(
    HttpConnectionDetails(
        addr="10.101.60.54", port="443", username="dcapuser", password="dcapadmin!"
    )
)

_gnb = ClassicalBts(cu=_cu, dus=[_du_0], instance_id="1941", global_bts_id="37406", dcap=_dcap)



_app_server_1 = TafUeAppServer(
    app_server_name="APP_5",
    address="10.57.191.249",
    user="vrf3_sg5",
    password="vrf3@sg5",
    ports=[45941,45041],
)



_data_transfer_iperf = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_app_server_1,
    interval=1,
#   interface_name="rmnet_data0",
    server_close_delay=50,
)


_pdn1 = PDNTafUeAndroidDetails(
    entryName="dxdata2", apnName="dxdata2", apnType=["DEFAULT"]
)


# CI_Detail_UE_Type='MTP8350'
_ue1 = TafUeAndroid(
    serial_number="bb9c8103", 
    capabilities=['REAL_UE', "qualcomm"],
    ue_pc_address="10.57.150.135",
    ssh_connection_details=SshServiceDetails(
        addr="10.57.150.135", username="mn5gran", password="nokia123@"
    ),
    data_transfer=[_data_transfer_iperf],
    pdns=[_pdn1],
    proxy_mngr_port="9955",    
)



#_eNB_capacity_unit = CapacityUnit(addr="192.168.253.36")
# _real_enb_pdu = HBTE(addr="10.71.195.69", port_numbers=[6])

# _enb_airscale = CommonUnit(
    # lmp_connection=SshServiceDetails(
        # addr="10.71.208.205", username="toor4nsn", password="oZPS0POrRieRtu"
    # ),
    # pdu_port=_real_enb_pdu.pdu_ports[5],
    # hardware_type="ASIA",
    # capacity_units=[],
# )


# _enb_0 = RealEnb(
    # airscale=Airscale(common_units=[_enb_airscale]),
    # x2_link_addr=NetworkAddress(
        # v4="10.71.208.205",
        # routing=RoutingInformation(gateway="10.71.208.1", ip_prefix_length=24),
    # ),
    # global_bts_id=10082,instance_id=1964
# )

# _enb_test_pc = TestPc(
    # default_ssh_connection_details=SshServiceDetails(
        # addr="10.57.251.31", username="ute", password="iW_K#8.ute%A10h0m0ra"
    # ),
    # connections=[_enb_0],
# )

_tl_cloud_topology = "CLOUD_5G_CLASSICAL_QC_SA_ASOE_AVNB"

# Testpc
_test_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.217.52", username="ute", password="ute"
    ),
    connections=[Connection(interface="eth1", device=_gnb.dus[0].airscale.common_units[0], interface_type="lmp")],
)

tl = TestLine(
    test_pc=_test_pc,
    test_pcs=[_test_pc],
    gnbs=[_gnb],
    #enbs=[_enb_0],
    core=RealCore(mcc=262, mnc=3),
    ues=[_ue1],
    #appserver=_appserver,
    tl_cloud_topology=_tl_cloud_topology,
    #pdus=[_du_pdu]
)


__all__ = ["tl"]
