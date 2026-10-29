# Generated with TL configuration generator at 2025-02-26_13:41:15

# Repository  -> https://wrgitlab.int.net.nokia.com/ran_pz_krk/config_generator
# Jenkins job -> http://krk-pz-jenkins.krk-lab.nsn-rdnet.net:5990/view/Tools/job/Config_Generator/build?delay=0sec

__maintainer__ = "Maciej Russek"
__team__ = "I_MN_RAN_PZ_KRK_2"
__email__ = "maciej.russek@nokia.com"

from taf.config.testline.testline import TestLine
from taf.config.testline.testpc import TestPc, Connection
from taf.config.testline.connection_details import (
    SshServiceDetails,
    HttpConnectionDetails,
)
from taf.config.testline.gnb import ClassicalBts, CU, DU
from taf.config.testline.gnb.networkaddress import NetworkAddress, RoutingInformation
from taf.config.testline.radio import RU, RUExtension
from taf.config.testline.enb import RealEnb
from taf.config.testline.airscale import (
    Airscale,
    CommonUnit,
    CoreUnit,
    CapacityUnit,
    SlotId,
    TRSInterfaces,
)
from taf.config.testline.pdu import PduPort, FPFH, HPE
from taf.config.testline.lmi import SerialOverTcp, Remote
from taf.config.testline.ue import TafUeAndroid
from taf.config.testline.appserver import TafUeAppServer
from taf.config.testline.taf_ue_data_transfer_protocol import TafUeDataTransferProtocol
import os
import yaml

# ------------------------PDU_CONFIGURATION------------------------

_bts_pdu_1 = FPFH(
    port_numbers=[1,5,6],         # update port_no
    addr="10.255.41.41",   # update address
    login="admin",
    password="admin",
)

# _hpe_snmp_user = {
#     "userName": "administrator",
#     "authKey": "password",
#     "privKey": "password",
#     "authProtocol": "MD5",
#     "privProtocol": "AES",      # HPE v2.0.0.K DES, HPE v2.0.0.Q/v2.0.0.T AES, ATEN should be AES
# }

_ru_pdu_1 = FPFH(
    port_numbers=[1,2,3],         # update port_no
    addr="fpfh-hf08-46-p11.p11-leg.ska-lab.nsn-rdnet.net",    # update address
    login="admin",
    password="admin",
)

# _ru_pdu_2 = HPE(
#     port_numbers=[2],         # update port_no
#     addr="hf09.mgt.ska-lab.nsn-rdnet.net",    # update address
#     snmp_user=_hpe_snmp_user,
# )

# ------------------------GNB0_CONFIGURATION------------------------

_test_pc_gnb_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-UTE5GCLOUDT11SK100.p11.ska-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_gnb_0_instance_id = 81100
_gnb_0_global_bts_id = 81100

_gnb_0_primary_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_gnb_0.default_ssh_connection_details,
)

_gnb_0_oam_ip = NetworkAddress(
    v4="10.82.28.100/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_0_f1m_ip = NetworkAddress(
    v4="10.82.28.100/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
)

_gnb_0_f1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_0_f1u_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_0_x2c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_0_x2u_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_0_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_0_s1u_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
)

_gnb_0_xnc_ip = NetworkAddress(
    v4="10.82.30.100/24",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=507,
)

_gnb_0_xnu_ip = NetworkAddress(
    v4="10.255.48.100/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=505,
)

_gnb_0_ngc_ip = NetworkAddress(
    v4="10.82.30.100/24",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=507,
)

_gnb_0_ngu_ip = NetworkAddress(
    v4="10.255.48.100/23",
    routing_v4=RoutingInformation(gateway="10.82.29.254", destIpAddr="0.0.0.0"),
    vlan_id=505,
)

_gnb_0_oam_http_connection = HttpConnectionDetails(
    addr=_gnb_0_oam_ip.v4.split("/")[0],
    username="Nemuadmin",
    password="nemuuser",
    port=443,
)

_cu_gnb_0 = CU(
    backhaul_site_oam_ip=_gnb_0_oam_ip,
    oam_ssh_connection_details=_gnb_0_primary_ssh_lmp_connection,
    oam_http_connection_details=_gnb_0_oam_http_connection,
    f1m=_gnb_0_f1m_ip,
    f1c=_gnb_0_f1c_ip,
    f1u=_gnb_0_f1u_ip,
    x2c=_gnb_0_x2c_ip,
    x2u=_gnb_0_x2u_ip,
    s1c=_gnb_0_s1c_ip,
    s1u=_gnb_0_s1u_ip,
    xnc=_gnb_0_xnc_ip,
    xnu=_gnb_0_xnu_ip,
    ngc=_gnb_0_ngc_ip,
    ngu=_gnb_0_ngu_ip,
    instance_id=_gnb_0_instance_id,
    global_bts_id=_gnb_0_global_bts_id,
)

_gnb_0_radio_unit_0 = RU(
    ru_hw_group="AVQL",
    default_ssh_connection_details=SshServiceDetails(
       addr="",
       username="root",
       password="umniedziala",
    ),
    radio_type="AVQL",
    serial_number="L1250203764",
    product_code="476203A.203",
    pdu_port=PduPort(pdu=_ru_pdu_1, port_no=3),    # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_1 = RU(
    ru_hw_group="AVQC",
    default_ssh_connection_details=SshServiceDetails(
       addr="",
       username="root",
       password="umniedziala",
    ),
    radio_type="AVQC",
    serial_number="1M244107262",
    product_code="476401A.101",
    pdu_port=PduPort(pdu=_ru_pdu_1, port_no=2),    # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_2 = RU(
    ru_hw_group="AVQC",
    default_ssh_connection_details=SshServiceDetails(
       addr="",
       username="root",
       password="umniedziala",
    ),
    radio_type="AVQC",
    serial_number="1M244107261",
    product_code="476401A.101",
    pdu_port=PduPort(pdu=_ru_pdu_1, port_no=1),    # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_3 = RU(
    ru_hw_group="AEQB",
    default_ssh_connection_details=SshServiceDetails(
       addr="",
       username="root",
       password="umniedziala",
    ),
    radio_type="AEQB",
    serial_number="1M201109059",
    product_code="474413A.101",
    pdu_port=PduPort(pdu=_bts_pdu_1, port_no=6),    # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

_gnb_0_radio_unit_4 = RU(
    ru_hw_group="AWHQX",
    default_ssh_connection_details=SshServiceDetails(
       addr="",
       username="root",
       password="umniedziala",
    ),
    radio_type="AWHQX",
    serial_number="EB2306R0036",
    product_code="475927A.101",
    pdu_port=PduPort(pdu=_bts_pdu_1, port_no=5),    # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
    # )
)

# _gnb_0_radio_unit_5 = RU(
#     ru_hw_group="APHG",
#     default_ssh_connection_details=SshServiceDetails(
#        addr="",
#        username="root",
#        password="umniedziala",
#     ),
#     radio_type="APHG",
#     serial_number="NH221300853",
#     product_code="475295A.101",
#     pdu_port=PduPort(pdu=_ru_pdu_2, port_no=2),    # uncomment & update port_no for gNB - for eNB you can delete
#     # lmi=SerialOverTcp(
#     #    uart_mapping=[Remote(addr=NetworkAddress(v4="MUMIN-LMI_FQDN"), port=5001)]
#     # )
# )

_gnb_0_core_unit_0 = CoreUnit(
    lmp_connection=_gnb_0_primary_ssh_lmp_connection,
    hardware_type="ASOG",
    hardware_version="A.101",
    serial_number="L1241503051",
    mac_addr="28:74:f5:25:06:e6",
    # trs_connections=[TRSInterfaces.EIF1],
    rus=[_gnb_0_radio_unit_0, _gnb_0_radio_unit_1, _gnb_0_radio_unit_2, _gnb_0_radio_unit_3, _gnb_0_radio_unit_4],
    pdu_port=PduPort(pdu=_bts_pdu_1, port_no=1),    # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_0_airscale = Airscale(
    core_units=[_gnb_0_core_unit_0],
    product_code="N/A",
    )

_du_gnb_0 = DU(
    airscale=_gnb_0_airscale,
    oam_ip=_gnb_0_oam_ip,
    f1_m_ip_addr=_gnb_0_f1m_ip,
    f1_c_ip_addr=_gnb_0_f1c_ip,
    f1_u_ip_addr=_gnb_0_f1u_ip,
    f1_m_cu=_gnb_0_f1m_ip,
    f1_c_cu=_gnb_0_f1c_ip,
    f1_u_cu=_gnb_0_f1u_ip,
    instance_id=_gnb_0_instance_id,
    global_bts_id=_gnb_0_global_bts_id,
    )

_gnb_0 = ClassicalBts(
    cu=_cu_gnb_0,
    dus=[_du_gnb_0],
    instance_id=_gnb_0_instance_id,
    global_bts_id=_gnb_0_global_bts_id,
)

_test_pc_gnb_0.connections = [
    Connection(
        device=_gnb_0.dus[0].airscale.core_units[0],
        interface="eth1",
        interface_type="lmp",
    )
]

_appserver_ssh = TafUeAppServer(
    app_server_name="APP_1",
    address="10.84.168.70",
    user="5g",
    password="5g",
    bind_interface_ip="10.84.169.54",
    expected_prompt="5g@SKA-HC14s17-1:~"

)

_qc_iperf = TafUeDataTransferProtocol(
    protocol_name="iperf",
    app_server=_appserver_ssh,
    binary_path="/data/data/com.nokia.android.application/"
)

_qc = TafUeAndroid(
    serial_number="f90cbdc6",
    ue_pc_address="plkr-sg02-100.intra.noklab.net",
    ue_pc_port="80",
    ssh_connection_details=SshServiceDetails(
        addr="plkr-sg02-100.intra.noklab.net", username="user-lab0", password="Bts2003"
    ),
    capabilities=["REAL_UE", "REAL_ANDROID_UE", "QC"],
    qualcomm_prototype=False,
    data_transfer=[_qc_iperf],
)

# ------------------------TL_CONFIGURATION------------------------


tl = TestLine(
    test_pc=_test_pc_gnb_0,
    gnbs=[_gnb_0],
    test_pcs=[_test_pc_gnb_0],
    tl_cloud_topology="CLOUD_5G_CLASSICAL_ANDROID_ASOG_2xAVQC_AVQL_AEQB_AWHQX_APHG_AWHGEQK",
    ues=[_qc]
)

__all__ = ["tl"]
