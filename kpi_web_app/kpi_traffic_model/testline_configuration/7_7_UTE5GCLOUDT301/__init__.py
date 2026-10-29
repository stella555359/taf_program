__maintainer__ = "Lubomir Krzeminski"
__team__ = "MN_RAN_PZ_KRK_SG07"
__email__ = "lubomir.krzeminski@nokia.com"

import os
from taf.config.testline import RU
from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc
from taf.config.testline.gnb import CloudBts, CU
from taf.config.testline.gnb.du import DU
from taf.config.testline.pdu import FPFH, PduPort
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.nms import NMS, NOM
from taf.config.testline.connection_details import (
    SshServiceDetails,
    OpenStackConnectionDetails,
    BmcConnectionDetails,
    HttpConnectionDetails,
)
from taf.config.testline.cloud_hosting import (
    NCIR,
    ControlNode,
    CloudDeployment,
    DeploymentFlavorStack,
    DeploymentNetworkStack,
    DeploymentVnfStack,
    ComputeNode,
)


__all__ = ["tl"]

os.environ["INIT_PATH"] = os.path.dirname(os.path.abspath(__file__))

_CFG_DIR = os.path.dirname(os.path.abspath(__file__))

_vm_ute = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-ute5gcloudt301.sc5g.krk-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_ru_du = RU(
    ru_hw_group="",
    radio_type="AEUB",
    default_ssh_connection_details=SshServiceDetails(addr="", username=""),
)

_pdu = FPFH(
    addr="FPFH-GL06-1.sc5g-leg.krk-lab.nsn-rdnet.net",
    port_numbers=[1, 2, 3, 4, 5, 6],
    login="admin",
    password="admin",
    model="FPFH",
)

_pdus = [_pdu]

_du0_capacity_unit = CapacityUnit(addr="192.168.253.20")

_common_unit = CommonUnit(
    lmp_connection=SshServiceDetails(
        addr="192.168.255.129", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    capacity_units=[_du0_capacity_unit],
    hardware_type="ASIK",
    pdu_port=PduPort(pdu=_pdu, port_no=6),
)

_airscale = Airscale(common_units=[_common_unit])

_control_0 = ControlNode(
    open_stack_connection_details=OpenStackConnectionDetails(
        ip_addr="10.83.190.241",
        username="sb14user1",
        tenant="SB14tenant1",
        password="5Guser@9",
    ),
    default_ssh_connection_details=SshServiceDetails(
        addr="10.83.190.241", username="sb14user1", password="5Guser@9"
    ),
    bmc_connection_details=BmcConnectionDetails(addr="", username="", password=""),
)

_compute = ComputeNode(
    bmc_connection_details=BmcConnectionDetails(addr="", username="", password="")
)

_ncir = NCIR(compute_nodes=[_compute], control_nodes=[_control_0], version="ncir_19")

_cbts_flavor = DeploymentFlavorStack(
    name=None,
    env_files=[os.path.join(_CFG_DIR, "config_flavor.env")],
    yaml_file=os.path.join(_CFG_DIR, "5gbts_flavor.yaml"),
    default_vnf_prefix="5gbts-176-301",
)

_cbts_net = DeploymentNetworkStack(
    name=None,
    env_files=[os.path.join(_CFG_DIR, "config_ext_net.env")],
    yaml_file=os.path.join(_CFG_DIR, "5gbts_ext_net.yaml"),
)

_cbts_vnf = DeploymentVnfStack(
    name=None,
    env_files=[os.path.join(_CFG_DIR, "config_bts.env")],
    yaml_file=os.path.join(_CFG_DIR, "5gbts_heat.yaml"),
)

_cloud_deployment = CloudDeployment(
    default_cfg_dir=_CFG_DIR,
    flavors=[_cbts_flavor],
    networks=[_cbts_net],
    vnfs=[_cbts_vnf],
    cloud_hosting=_ncir,
)

_oam_ip = "10.83.251.12"

_du = DU(
    airscale=_airscale,
    oam_ip=_oam_ip,
    rus=[_ru_du],
)

_cu = CU(
    backhaul_site_oam_ip="10.83.183.51",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.83.183.51", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.83.183.51",
        username="Nemuadmin",
        password="nemuuser",
        port=80,
    ),
)

_cbts = CloudBts(
    cu=_cu, cloud_deployment=_cloud_deployment, vnf_name="5gbts-301", dus=[_du]
)

_nms = NMS(
    addr="",
    nom=NOM(
        https_main_info=HttpConnectionDetails(
            addr="https://user-mgmt.srncnms08.srnblr.nsn-rdnet.net",
            username="cnms01",
            password="Qwer@456",
            port=443,
        ),
        https_user_mgmt_info=HttpConnectionDetails(
            addr="https://user-mgmt.srncnms08.srnblr.nsn-rdnet.net",
            username="cnms01",
            password="Qwer@456",
            port=443,
        ),
        https_rest_info=HttpConnectionDetails(
            addr="https://apigw.srncnms08.srnblr.nsn-rdnet.net",
            username="neonetics",
            password="Nokia_150",
            port=443,
        ),
    ),
)

_tl_cloud_topology = "CLOUD_5G_ASIK_ABIL_AEUB_ENB_NOM"

tl = TestLine(
    test_pc=_vm_ute,
    gnbs=[_cbts],
    tl_cloud_topology=_tl_cloud_topology,
    nms=_nms,
    cloud_hostings=[_ncir],
    pdus=_pdus,
)

tl.ute_cplane_address = "172.16.5.3"
tl.ute_uplane_address = "172.16.5.3"
tl.ute_mplane_address = "172.16.6.3"

tl.gnb_cplane_address = "172.16.5.61"
tl.gnb_uplane_address = "172.16.5.71"
tl.gnb_uplane_address_2 = "172.16.5.71"
tl.gnb_mplane_address = "172.16.6.81"

tl.ip_address_version = "4"
tl.ip_address_prefix = "24"

tl.gnb_friendly_name = "7_7_UTE5GCLOUDT301"
tl.mrbts_name = "MRBTS-301"
tl.nrbts_name = "NRBTS-1"

tl.ip_913A_102r1 = ""
tl.ip_913A_103r1 = ""
tl.ip_913A_104r1 = ""
tl.ip_913A_104r4 = ""
tl.ip_913A_104r5 = ""
tl.ip_913A_104r6 = ""
tl.ip_913A_104r7 = ""
tl.ip_913A_104r8 = ""
tl.ip_913A_106r2 = ""
tl.ip_913A_106r3 = ""
tl.ip_913A_107r2 = ""
tl.ip_913A_107r3 = ""
