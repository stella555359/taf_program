# Generated with TL configuration generator at 2026-02-04_12:36:42

# Repository  -> https://wrgitlab.int.net.nokia.com/ran_pz_krk/config_generator
# Jenkins job -> http://krk-pz-jenkins.krk-lab.nsn-rdnet.net:5990/view/Tools/job/Config_Generator/build?delay=0sec

__maintainer__ = "KRKAUTO5GPZ"
__team__ = "I_MN_RAN_PZ_KRK_TAG"
__email__ = "I_MN_RAN_PZ_KRK_TAG@internal.nsn.com"

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
import os
import yaml
from taf.config.testline import TafUeAppServer, TafUeDataTransferProtocol, TafUeAndroid
from taf.config.testline.attenuator import RadioRack
from taf.config.testline.pdn import PDNTafUeAndroidDetails
from taf.config.testline.lmi import SerialOverTcp, Remote

# ------------------------PDU_CONFIGURATION------------------------

_bts_pdu = FPFH(
    port_numbers=[1],         # update port_no
    addr="FPFH-PB09-46-D01.D01-leg.krk-lab.nsn-rdnet.net",   # update address
    login="admin",
    password="admin",
)

_hpe_snmp_user = {
    "userName": "administrator",
    "authKey": "password",
    "privKey": "password",
    "authProtocol": "MD5",
    "privProtocol": "AES",      # HPE v2.0.0.K DES, HPE v2.0.0.Q/v2.0.0.T AES, ATEN should be AES
}

_ru_pdu = FPFH(
    port_numbers=[1, 2, 3, 4, 5, 6],         # update port_no
    addr="fpfh-pb07-39-d01.d01-leg.krk-lab.nsn-rdnet.net",   # update address
    login="admin",
    password="admin",
)

_ru_pdu_2 = FPFH(
    port_numbers=[1, 2, 3, 4, 5, 6],         # update port_no
    addr="fpfh-pb08-39-d01.d01-leg.krk-lab.nsn-rdnet.net",   # update address
    login="admin",
    password="admin",
)


# ------------------------GNB0_CONFIGURATION------------------------

_test_pc_gnb_0 = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="7-7-T01PY002.d01.krk-lab.nsn-rdnet.net",
        username="ute",
        password="ute",
    )
)

_gnb_0_instance_id = 85002
_gnb_0_global_bts_id = 85002

_gnb_0_primary_ssh_lmp_connection = SshServiceDetails(
    addr="192.168.255.129",
    username="toor4nsn",
    password="oZPS0POrRieRtu",
    proxy=_test_pc_gnb_0.default_ssh_connection_details,
)

_gnb_0_oam_ip = NetworkAddress(
    v4="10.89.3.2/24",
    routing_v4=RoutingInformation(gateway="10.89.3.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
) 

_gnb_0_f1m_ip = NetworkAddress(
    v4="10.89.3.2/24",
    routing_v4=RoutingInformation(gateway="10.89.3.254", destIpAddr="0.0.0.0"),
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
    v4="10.89.4.2/24",
    routing_v4=RoutingInformation(gateway="10.89.3.254", destIpAddr="0.0.0.0"),
    vlan_id=507,
) 

_gnb_0_x2u_ip = NetworkAddress(
    v4="10.254.5.2/24",
    routing_v4=RoutingInformation(gateway="10.89.3.254", destIpAddr="0.0.0.0"),
    vlan_id=506,
) 

_gnb_0_s1c_ip = NetworkAddress(
    v4="/0",
    routing_v4=RoutingInformation(gateway="", destIpAddr=""),
    vlan_id=0,
) 

_gnb_0_s1u_ip = NetworkAddress(
    v4="10.89.3.2/24",
    routing_v4=RoutingInformation(gateway="10.89.3.254", destIpAddr="0.0.0.0"),
    vlan_id=504,
) 

_gnb_0_xnc_ip = NetworkAddress(
    v4="10.89.4.2/24",
    routing_v4=RoutingInformation(gateway="10.89.3.254", destIpAddr="0.0.0.0"),
    vlan_id=507,
) 

_gnb_0_xnu_ip = NetworkAddress(
    v4="10.254.5.2/24",
    routing_v4=RoutingInformation(gateway="10.89.3.254", destIpAddr="0.0.0.0"),
    vlan_id=506,
) 

_gnb_0_ngc_ip = NetworkAddress(
    v4="10.89.4.2/24",
    routing_v4=RoutingInformation(gateway="10.89.3.254", destIpAddr="0.0.0.0"),
    vlan_id=507,
) 

_gnb_0_ngu_ip = NetworkAddress(
    v4="10.254.5.2/24",
    routing_v4=RoutingInformation(gateway="10.89.3.254", destIpAddr="0.0.0.0"),
    vlan_id=506,
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
    ru_hw_group="AHHB",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHHB",
    serial_number="DH205061549",
    product_code="474252A.102",
    pdu_port=PduPort(pdu=_ru_pdu, port_no=2), # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr="10.255.60.92", port=5001)]
    # )
)

_gnb_0_radio_unit_1 = RU(
    ru_hw_group="AHPMDB",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHPMDB",
    serial_number="LR250500462",
    product_code="475000A.101",
    pdu_port=PduPort(pdu=_ru_pdu, port_no=6),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr="10.255.60.91", port=5001)]
    # )
)

_gnb_0_radio_unit_2 = RU(
    ru_hw_group="AHPMDB",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHPMDB",
    serial_number="LR250500463",
    product_code="475000A.101",
    pdu_port=PduPort(pdu=_ru_pdu, port_no=5),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr="10.255.60.90", port=5001)]
    # )
)

_gnb_0_radio_unit_3 = RU(
    ru_hw_group="AHPMDB",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHPMDB",
    serial_number="LR234504186",
    product_code="475000A.101",
    pdu_port=PduPort(pdu=_ru_pdu, port_no=1),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr="10.255.60.89", port=5001)]
    # )
)

_gnb_0_radio_unit_4 = RU(
    ru_hw_group="AHHB",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHHB",
    serial_number="DH205061552",
    product_code="474252A.102",
    pdu_port=PduPort(pdu=_ru_pdu, port_no=3),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr="10.255.60.94", port=5001)]
    # )
)

_gnb_0_radio_unit_5 = RU(
    ru_hw_group="AHHB",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHHB",
    serial_number="DH205061557",
    product_code="474252A.102",
    pdu_port=PduPort(pdu=_ru_pdu, port_no=4),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr="10.255.60.110", port=5001)]
    # )
)

_gnb_0_radio_unit_6 = RU(
    ru_hw_group="AEQC",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AEQC",
    serial_number="1M202227580",
    product_code="475431A.101",
    pdu_port=PduPort(pdu=_ru_pdu_2, port_no=2),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr="10.255.60.114", port=5001)]
    # )
)

_gnb_0_radio_unit_7 = RU(
    ru_hw_group="AEQC",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AEQC",
    serial_number="1M202227579",
    product_code="475431A.101",
    pdu_port=PduPort(pdu=_ru_pdu_2, port_no=1),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr="10.255.60.113", port=5001)]
    # )
)

_gnb_0_radio_unit_8 = RU(
    ru_hw_group="AEQC",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AEQC",
    serial_number="1M222643819",
    product_code="475431A.M02",
    pdu_port=PduPort(pdu=_ru_pdu_2, port_no=3),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr="10.255.60.88", port=5001)]
    # )
)

_gnb_0_radio_unit_9 = RU(
    ru_hw_group="AHEGB",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHEGB",
    serial_number="EA214550850",
    product_code="474090A.101",
    pdu_port=PduPort(pdu=_ru_pdu_2, port_no=4),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr="10.255.60.111", port=5001)]
    # )
)

_gnb_0_radio_unit_10 = RU(
    ru_hw_group="AHEGB",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHEGB",
    serial_number="EA214550851",
    product_code="474090A.101",
    pdu_port=PduPort(pdu=_ru_pdu_2, port_no=5),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr="10.255.60.112", port=5001)]
    # )
)

_gnb_0_radio_unit_11 = RU(
    ru_hw_group="AHEGB",
    default_ssh_connection_details=SshServiceDetails(
        addr="",
        username="root",
        password="umniedziala",
    ),
    radio_type="AHEGB",
    serial_number="EA222453211",
    product_code="474090A.101",
    pdu_port=PduPort(pdu=_ru_pdu_2, port_no=6),  # uncomment & update port_no for gNB - for eNB you can delete
    # lmi=SerialOverTcp(
    #    uart_mapping=[Remote(addr="10.255.60.93", port=5001)]
    # )
)

_gnb_0_capacity_unit_0 = CapacityUnit(
    addr="",
    hardware_type="ABIA",
    hardware_version="A.104",
    serial_number="EA201952194",
    product_code="473096A.104",
    slot_id=SlotId.B3,
    rus=[_gnb_0_radio_unit_1, _gnb_0_radio_unit_2, _gnb_0_radio_unit_3],
)

_gnb_0_capacity_unit_1 = CapacityUnit(
    addr="",
    hardware_type="ABIO",
    hardware_version="A.104",
    serial_number="DH222540547",
    product_code="475266A.104",
    slot_id=SlotId.B1,
    rus=[_gnb_0_radio_unit_0, _gnb_0_radio_unit_1, _gnb_0_radio_unit_10, _gnb_0_radio_unit_11, _gnb_0_radio_unit_2, _gnb_0_radio_unit_3, _gnb_0_radio_unit_4, _gnb_0_radio_unit_5, _gnb_0_radio_unit_9],
)

_gnb_0_capacity_unit_2 = CapacityUnit(
    addr="",
    hardware_type="ABIO",
    hardware_version="A.104",
    serial_number="L1213108378",
    product_code="475266A.104",
    slot_id=SlotId.B2,
    rus=[_gnb_0_radio_unit_6, _gnb_0_radio_unit_7, _gnb_0_radio_unit_8],
)

_gnb_0_common_unit_0 = CommonUnit(
    lmp_connection=_gnb_0_primary_ssh_lmp_connection,
    capacity_units=[_gnb_0_capacity_unit_0, _gnb_0_capacity_unit_1, _gnb_0_capacity_unit_2],
    hardware_type="ASIB",
    hardware_version="A.102",
    serial_number="DH214144756",
    mac_addr="60:8f:a4:31:2d:18",
    # trs_connections=[TRSInterfaces.EIF1],
    slot_id=SlotId.C1,
    pdu_port=PduPort(pdu=_bts_pdu, port_no=1),  # uncomment & update port_no for gNB - for eNB you can delete
)

_gnb_0_airscale = Airscale(
    common_units=[_gnb_0_common_unit_0],
    product_code="475773A",
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
        device=_gnb_0.dus[0].airscale.common_units[0],
        interface="eth1",
        interface_type="lmp",
    )
]

# _appsrv = TafUeAppServer(
#     app_server_name="KRK-SB18s16-App2",
#     address="10.83.249.132",
#     bind_interface_ip="10.83.249.162",
#     user="5g",
#     password="5g"
# )

_appsrv = TafUeAppServer(
    app_server_name="SRN-Appserver-Krakow",
    # app_server_name="KRK-SB18s16-App2",
    address="10.83.249.130",
    # address="10.83.249.132",
    bind_interface_ip="10.83.249.189",
    # bind_interface_ip="10.83.249.162",
    user="5g",
    password="5g"
)

_iperf = TafUeDataTransferProtocol(
    protocol_name='iperf',
    app_server=_appsrv,
    binary_path='/data/data/com.nokia.android.application/',
    # interface_name='5gkrk/rmnet_data0',
    # interface_name='5gkrkpych2/rmnet_data0',
    interval=1,
)

# ------------------------UE_CONFIGURATION------------------------

_samsung = TafUeAndroid(
    ssh_connection_details=SshServiceDetails(
        #addr="PLKR-TP-UE09.sc5g.krk-lab.nsn-rdnet.net",
        addr="PLKR-SC5G-PC125.d01.krk-lab.nsn-rdnet.net",
        # username="PLKR-SC5G+pzkrk",
        username="pzkrk",
        password="NokiaBts2003",
    ),
    #ue_pc_address="PLKR-TP-UE09.sc5g.krk-lab.nsn-rdnet.net",
    ue_pc_address="PLKR-SC5G-PC125.d01.krk-lab.nsn-rdnet.net",
    ue_pc_port="80",
    # serial_number="RFCX20VQXYD",
    # serial_number="R3CT20BA69M",
    # serial_number="3ac3124c",
    # serial_number="8c9ab6ab",
    # serial_number="RFCWC0YVALD",
    # serial_number="RFCX11N6MFD",
    serial_number="RFCX20VQXYD",
    capabilities=["REAL_UE", "REAL_ANDROID_UE"],
    data_transfer=[_iperf],
)

# ------------------------Attenuator------------------------------

_attenuator = RadioRack(
    ip_addr="10.255.60.23",
    port=50000,
    attenuation_port_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
    model='16-220')

# ------------------------TL_CONFIGURATION------------------------

tl = TestLine(
    test_pc=_test_pc_gnb_0,
    gnbs=[_gnb_0],
    attenuator=_attenuator,
    test_pcs=[_test_pc_gnb_0],
    tl_cloud_topology="CLOUD_7_7_T01PY002",
    ues=[_samsung]
)

__all__ = ["tl"]
