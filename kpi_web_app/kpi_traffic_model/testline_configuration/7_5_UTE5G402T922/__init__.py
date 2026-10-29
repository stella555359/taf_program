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
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, ATEN, RRB, APC, Gude
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
    HBTE,
    Hytem,
    RadioRack,
)
from taf.compatibility.configuration import TestlineWrapper

__maintainer__ = "y6lu"
__team__ = "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_03@internal.nsn.com"
__email__ = "lu.yu@nokia-sbell.com"


PARAMS_TO_MODIFY_TL = [
    dict(
        value="10.68.88.135",
        dist_name="MRBTS-10048/TNLSVC-1/TNL-1/IPNO-1/IPIF-1/IPADDRESSV4-1",
        p_name="localIpAddr",
    ),
]

LIST_ITEM_TO_ADD_TL = [
    dict(
        dist_name="MRBTS-10048/MNL-1/MNLENT-1/SYNC-1/CLOCK-1/TOP-1/TOPP-1",
        list_name="topMasterList",
        elements={
            "localPriority": "128",
            "masterIpAddr": "10.97.126.186",
            "phaseErrorComp": "0",
            "phaseErrorComp": "0",
        },
    ),
    dict(
        dist_name="MRBTS-10048/TNLSVC-1/TNL-1/IPNO-1/IPRT-1",
        list_name="staticRoutes",
        elements={
            "destIpAddr": "0.0.0.0",
            "destinationIpPrefixLength": "0",
            "gateway": "10.68.88.225",
        },
    ),
    #    dict(
    #        dist_name="MRBTS-925/TNLSVC-1/TNL-1/IPNO-1/IPRT-1",
    #        list_name="staticRoutes",
    #        elements={
    #            "destIpAddr": "10.68.90.131",
    #            "destinationIpPrefixLength": "32",
    #            "gateway": "10.57.159.129",
    #            "preference": "1"}),
    #    dict(
    #        dist_name="MRBTS-1900/TNLSVC-1/TNL-4/IPNO-1/IPRT-1",
    #        list_name="staticRoutes",
    #        elements={
    #            "destIpAddr": "0.0.0.0",
    #            "destinationIpPrefixLength": "0",
    #            "gateway": "10.68.90.129",
    #            "preference": "1"})
]

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# #host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.107", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)


# RealEnb
_real_enb_pdu = FACOM(addr="10.101.45.228", port_numbers=[2])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.101.51.137", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[2],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, instance_id="922")

# attenuator
_attenuator = HBTE(
    ip_addr="10.101.51.136",
    port=5000,
    attenuation_port_numbers=[1, 9, 2, 10, 3, 11, 4, 12],
    model="PA-16-16-6-127-0.5-B-S",
)

# #5GRU_0 for classicalBTS
_ru1_pdu = FACOM(addr="10.101.45.230", port_numbers=[4])
_ru2_pdu = FACOM(addr="10.101.45.230", port_numbers=[5])
_ru3_pdu = FACOM(addr="10.101.45.230", port_numbers=[6])
_ru4_pdu = FACOM(addr="10.101.45.226", port_numbers=[5])

##
_ru1 = RU(
    ru_hw_group="Above6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.73.129", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.73.129", username="root", password="umniedziala"
    ),
    pdu_port=_ru1_pdu.pdu_ports[4],
    radio_type="AHLOA",
    attenuation_ports=[
        _attenuator.attenuator_ports[1],
        _attenuator.attenuator_ports[9],
    ],
)

_ru2 = RU(
    ru_hw_group="Above6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.73.128", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.73.128", username="root", password="umniedziala"
    ),
    pdu_port=_ru2_pdu.pdu_ports[5],
    radio_type="AHLOA",
    attenuation_ports=[
        _attenuator.attenuator_ports[2],
        _attenuator.attenuator_ports[10],
    ],
)

_ru3 = RU(
    ru_hw_group="Above6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.73.130", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.73.130", username="root", password="umniedziala"
    ),
    pdu_port=_ru3_pdu.pdu_ports[6],
    radio_type="AHLOA",
    attenuation_ports=[
        _attenuator.attenuator_ports[3],
        _attenuator.attenuator_ports[11],
    ],
)

_ru4 = RU(
    ru_hw_group="Above6GHz",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.73.130", username="root", password="umniedziala"
    ),
    lmp_connection=SshServiceDetails(
        addr="172.16.73.130", username="root", password="umniedziala"
    ),
    pdu_port=_ru3_pdu.pdu_ports[6],
    radio_type="AHLOA",
    attenuation_ports=[
        _attenuator.attenuator_ports[4],
        _attenuator.attenuator_ports[12],
    ],
)

# #######Iperf########
_appserver_ssh = SshServiceDetails(
    addr="10.70.222.51", username="mmw_sg3", password="mm@3", port="43121"
)

_iperf = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.70.222.51",
    iperf_path="/usr/bin/iperf",
    port=43021,
)

# Qualcomm
_Android = Android(
    ssh_connection_details=SshServiceDetails(
        addr="10.101.47.8", username="nokia5G", password="noki@123"
    ),
    serial_number="e4320026",
    server_dir="/cygdrive/c/pyro_server",
    python_path="C:/Python38/python.exe",
    qcat_path="C:/Program Files (x86)/Qualcomm/QCAT 6.x/Bin/QCAT.exe",
    diag_cfg_path="C:/pyro_server/DIAG.cfg",
    iperf_details=_iperf,
    capabilities=["qct_dx50", "REAL_UE"],
)


# askey
_ue_config_path = os.path.join(_cfg_dir, "AskeyData/askey.yml")
if os.path.isfile(_ue_config_path):
    with open(_ue_config_path) as f:
        _ue_askey = f.read()
        qci_port = re.findall("(_iperf.*?port)", _ue_askey)
        for item in qci_port:
            _ue_askey = _ue_askey.replace(item, str(eval(item)))
        _ue_config = yaml.safe_load(_ue_askey)
else:
    _ue_config = ""

# #DU_0 for classicalBTS
_lmp_connection_0 = SshServiceDetails(
    addr="10.101.51.135", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_0 = CapacityUnit(addr="1.1.1.1")

_gnb_pdu = FACOM(addr="10.101.45.228", port_numbers=[5])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection_0,
    capacity_units=[_capacity_unit_0],
    pdu_port=_gnb_pdu.pdu_ports[5],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru1, _ru2, _ru3, _ru4], f1_m_ip_addr="10.101.51.135")

##CU
_cu = CU(
    backhaul_site_oam_ip="10.101.51.135",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.101.51.135", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.101.51.135", username="Nemuadmin", password="nemuuser"
    ),
)

# cloud
_control = ControlNode(
    open_stack_connection_details=OpenStackConnectionDetails(
        ip_addr="10.57.137.34",
        username="admin",
        tenant="admin",
        password="HZnokia123!",
        port=5000,
        protocol="https",
        version="v3",
    ),
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.137.34", username="sqg09", password="Nokia09!"
    ),
    bmc_connection_details=BmcConnectionDetails(
        addr="5.5.5.5", username="admin", password="admin"
    ),
)

_ncir = NCIR(
    compute_nodes=[],
    control_nodes=[_control],
    version="ncir_19",
    cloud_deployments=None,
)

# classicalbts
_classical_bts = ClassicalBts(
    dus=[_du], cu=_cu, instance_id="10048", global_bts_id="10048"
)


# #cloudbts
_cbts_flavor = DeploymentFlavorStack(
    name="tl923_cbtsflavor",
    env_files=[
        os.path.join(_cfg_dir, "5gbts_flavor.env"),
        os.path.join(_cfg_dir, "config_flavor_ci.env"),
    ],
    yaml_file=os.path.join(_cfg_dir, "5gbts_flavor.yaml"),
    default_vnf_prefix="cbts_prefix",
)

_cbts_net = DeploymentNetworkStack(
    name="tl923_ext_net",
    env_files=[
        os.path.join(_cfg_dir, "5gbts_ext_net.env"),
        os.path.join(_cfg_dir, "config_ext_net_ci.env"),
    ],
    yaml_file=os.path.join(_cfg_dir, "5gbts_ext_net.yaml"),
)

_cbts_vnf = DeploymentVnfStack(
    name="tl923_cbts_deploy",
    env_files=[
        os.path.join(_cfg_dir, "5gbts_heat.env"),
        os.path.join(_cfg_dir, "config_bts_ci.env"),
    ],
    yaml_file=os.path.join(_cfg_dir, "5gbts_heat.yaml"),
)

_cloud_deployment = CloudDeployment(
    default_cfg_dir=_cfg_dir,
    flavors=[_cbts_flavor],
    networks=[_cbts_net],
    vnfs=[_cbts_vnf],
    cloud_hosting=_ncir,
)

_cbts = CloudBts(dus=[_du], cu=_cu, cloud_deployment=_cloud_deployment)

_iperf_details_on_appserver2 = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.70.222.51",
    iperf_path="iperf",
    port="43021",
)

_appserver = AppServer(_iperf_details_on_appserver2)

# #cloud_topology
_tl_cloud_topology = "CLOUD_5G_BB3"

tl = TestLine(
    test_pc=_host,
    ues=[_ue_config],
    gnbs=[_classical_bts],
    # cloud_hostings=[_ncir],
    enbs=[_lte_real_enb],
    # tl_cloud_topology=_tl_cloud_topology,
    appserver=_appserver,
    attenuator=_attenuator,
)
