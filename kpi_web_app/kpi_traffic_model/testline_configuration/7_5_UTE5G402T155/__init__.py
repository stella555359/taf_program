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
)  # added in taf.meta.5.4
from taf.config.testline.core import (
    EPCSim,
    RealCore4G,
    RealCore,
    RealCore5GDetails,
    AMF,
)
from taf.config.testline.gnb.du import DU
from taf.config.testline.pdu import FACOM, PduPort, Pdu, EPC, ATEN, RRB, APC, Gude
from taf.config.testline.pdu import HBTE
from taf.config.testline.testline import TestLine
from taf.config.testline.ue import MediaTek
from taf.config.testline.pdn import PDN, PDPTypes
from taf.config.testline.connection_details import (
    SshServiceDetails,
    IperfDataTransferDetails,
)
from taf.config.testline.appserver import AppServer
from taf.config.testline.testpc import TestPc
from taf.config.testline.gnb.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
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
from taf.config.testline.enb import (
    Enb,
    SimEnb,
    RealEnb,
    LTEEmuEnb,
    PrismaEnb,
    DocomoEnb,
)


__maintainer__ = "Deng Qingqing"
__team__ = "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_02@internal.nsn.com"
__email__ = "qingqing.deng@nokia-sbell.com"


# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# #host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.155.211", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)
_docker_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.46", username="dcapuser", password="dcapuser123"
    )
)
_tce_pc = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.167.46", username="dcapuser", port=1234
    )
)

# PB INFO of ENB IS NOT CORRECT #
# 4GRU for RealEnb
_ru_enb_pdu = HBTE(addr="10.57.246.62", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru_enb = RadioModule(
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.10.49", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    pdu_port=_ru_enb_pdu.pdu_ports[2],
)

# #RealEnb
_real_enb_pdu = HBTE(addr="10.57.246.195", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_common_unit_2 = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="10.57.251.140", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[],
    pdu_port=_real_enb_pdu.pdu_ports[4],
)

_real_enb = Airscale(common_units=[_common_unit_2])

_lte_real_enb = RealEnb(airscale=_real_enb, rms=_ru_enb)

# #5GRU_0 for cloudBTS
_ru_pdu = HBTE(addr="10.71.196.18", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_ru = RU(
    ru_hw_group="hw_group",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.48.162",
        username="serviceuser",
        password="bobuWrUHk7Xq7WPpY9ZcjEi8zNdX3plZ+/y420RZ7W4=",
    ),
    lmp_connection=SshServiceDetails(
        addr="192.168.100.1", username="root", password="a2%FgSz3$fHmdusap354xujw7a"
    ),
    pdu_port=_ru_pdu.pdu_ports[1],
    radio_type=RadioTypes.AEQU,
)

# #######Iperf########
_appserver_ssh = SshServiceDetails(
    addr="10.57.178.20", username="mmw_sg2_3", password="mm@2@3"
)

_mtk_host_ssh = SshServiceDetails(
    addr="10.57.150.167", username="nokia5G", password="noki@123"
)

_iperf_details_on_mtk = IperfDataTransferDetails(
    ssh_connection_details=_mtk_host_ssh,
    network_interface_address="",
    iperf_path="C:/Tool/iperf-2.0.9-win64/iperf",
    port="47127",
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.178.20",
    iperf_path="/usr/bin/iperf",
    port="46127",
)
_appserver = AppServer(_iperf_details_on_appserver)

# Huawei
_mtk = MediaTek(
    ssh_connection_details=_mtk_host_ssh,
    server_dir="c:/pyro_server",
    server_port=8080,
    edb_file_path="C:\MTK\Item.3 - NR16.R2.MP.W21.46.p11_MT6298_DONGLE(NLWCG_SAP_R16)_bin\MDDB_MT6298_S00_NR16_R2_MP_W21_46_P11.EDB",
    imei="12345678901234",
    imsi="310260100008735",
    apn_url="wap1.nokia.com",
    iperf_details=_iperf_details_on_mtk,
    capabilities=["REAL_MEDIATEK_UE"],
)

# #DU_0 for cloudlBTS
_lmp_connection_0 = SshServiceDetails(
    addr="10.71.211.133", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_0 = CapacityUnit(addr="192.168.253.22")

_du_pdu = HBTE(addr="10.71.196.21", port_numbers=[1, 2, 3, 4, 5, 6, 7, 8])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection_0,
    capacity_units=[_capacity_unit_0],
    pdu_port=_du_pdu.pdu_ports[1],
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(airscale=_airscale, rus=[_ru], f1_m_ip_addr="10.71.211.133")


# #CU
_cu = CU(
    backhaul_site_oam_ip="10.71.211.133",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.211.133", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.211.133", username="Nemuadmin", password="nemuuser"
    ),
)

# classicalbts------------------------------------------------
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=332, global_bts_id=332)

_pdns = [
    PDN(pdp_type=PDPTypes.IP.value, apn="wap2.nokia.com"),
    PDN(pdp_type=PDPTypes.IP.value, apn="wap2.nokia.com"),
]
_core = RealCore(pdns=_pdns)


# #cloud_topology------------------------------------------------
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ASIL_ABIL_AEQU_eCPRI"

tl = TestLine(
    test_pc=_host,
    test_pcs=[_docker_pc, _tce_pc],
    ues=[_mtk],
    gnbs=[_classical_bts],
    enbs=[_lte_real_enb],
    appserver=_appserver,
    core=_core,
    tl_cloud_topology=_tl_cloud_topology,
)
