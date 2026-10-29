import os
from taf.config.testline.connection_details import (
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
from taf.config.testline.core import EPCSim, LTEEmuCore, PrismaCore
from taf.config.testline.gnb.du import DU
from taf.config.testline.pdu import (
    HBTE,
    TopYoung,
    PduPort,
    Pdu,
    EPC,
    ATEN,
    RRB,
    APC,
    Gude,
)
from taf.config.testline.testline import TestLine
from taf.config.testline.gnb.gnb import CloudBts, CU, ClassicalBts
from taf.config.testline.airscale import Airscale, CommonUnit, CapacityUnit
from taf.config.testline.ue import AirphoneCloud, Airphone, Prisma, TM500
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
from taf.config.testline.pdu import TopYoung, HBTE, FPFH
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

from taf.config.testline import NetworkAddress, RoutingInformation, LicenseKeeper




__maintainer__ = "Zhang Lusha"
__team__ = (
    "I_NSB_MN_5GSC_MMW_SC_PZ_HZ_02_GMS <I_NSB_MN_5GSC_MMW_SC_PZ_HZ_02@internal.nsn.com>"
)
__email__ = "lusha.zhang@nokia-sbell.com"

# common
__all__ = ["tl"]

_cfg_dir = os.path.dirname(os.path.abspath(__file__))

# Real EPC is used. epcsim is here only as a backup solution.
_epc_sim = EPCSim(
    mme_ip="10.110.133.68",
    mcc="262",
    mnc="2",
    tac="20200",
    default_ssh_connection_details=SshServiceDetails(
        addr="10.110.133.23", username="nokia", password="Nokia_54321"
    ),
    edaemon_port=10000,
    egate_port=20000,
    dir_path="/opt/iphy/latest",
    cfg_filename="LRC.cfg",
)


##PB info
# _ru_pdu_DBIG20_PB1 = TopYoung(addr="10.71.196.78", port_numbers=[2, 3, 4, 6])
# _ru_pdu_DBIG17_PB2 = NOKIA(addr="10.71.196.83", port_numbers=[5, 6])


_ru_1_pdu = FPFH(addr="10.71.196.73", port_numbers=[1, 2, 3, 4,  5, 6])

_ru_2_pdu = FPFH(addr="10.71.196.74", port_numbers=[3])

_ru_3_pdu = HBTE(addr="10.71.196.75", port_numbers=[1, 2, 3, 4,  5, 6])


##5GRU_1
##SN:1M214208678 - AQQA1
_ru1 = RU(
    ru_hw_group="Rel6.2_MAA_32T32R",
    default_ssh_connection_details=SshServiceDetails(
        #addr="172.22.0.158",
        addr="172.22.8.2",
        username="rfsw",
        password="3Is6ezFJ7dFlB29cgs0yp3RCM3fUF1zNO1+6Z08tlAc=",
        #username="serviceuser",
        #password="v160rWp/6qpX/RQjmnaupqP+FBV2/f7bgiwMI8+cpEY=",
    ),
    pdu_port=_ru_1_pdu.pdu_ports[5],
    radio_type=RadioTypes.AQQA,
)

##SN:1M214208705 - AQQA2
_ru2 = RU(
    ru_hw_group="Rel6.2_MAA_32T32R",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.8.10",
        username="rfsw",
        password="3Is6ezFJ7dFlB29cgs0yp3RCM3fUF1zNO1+6Z08tlAc=",
    ),
    pdu_port=_ru_1_pdu.pdu_ports[6],
    radio_type=RadioTypes.AQQA,
)


##5GRU_3
##SN: AWPQZ4 EB2313R0122
_ru3 = RU(
    ru_hw_group="Rel6.2 IDRU_4T4R",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.8.30",
        username="rfsw",
        password="KRG3dFggxxHw+s0z64U0AR22VyjfnXdHrAVdSv5jpc4=",
    ),
    pdu_port=_ru_3_pdu.pdu_ports[6],
    radio_type=RadioTypes.AWPQZ,
)

##5GRU_4
##SN:1M180417867 - FXED1
_ru4 = RU(
    ru_hw_group="obsai",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.10.129",
        username="root", 
        password=""
    ),
    pdu_port=_ru_1_pdu.pdu_ports[3],
    radio_type=RadioTypes.FXED,
    serial_number="1M180417867"
)


##5GRU_5
##SN:1M170335367 - FXED2
_ru5 = RU(
    ru_hw_group="obsai",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.10.128",
        username="root", 
        #password="umniedziala"
        password=""
    ),
    pdu_port=_ru_1_pdu.pdu_ports[4],
    radio_type=RadioTypes.FXED,
    serial_number="1M170335367"
)


##5GRU_6
##SN:AS212919727 - AHCA1
_ru6 = RU(
    ru_hw_group="Rel3.2_FRMr_6T6R",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.37.129",
        username="root", 
        password="umniedziala"
    ),
    pdu_port=_ru_1_pdu.pdu_ports[2],
    radio_type=RadioTypes.AHCA,
)


##5GRU_7
##SN:AS213009766 - AHCA2
_ru7 = RU(
    ru_hw_group="Rel3.2_FRMr_6T6R",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.37.128",
        username="root", 
        password="umniedziala"
    ),
    pdu_port=_ru_1_pdu.pdu_ports[1],
    radio_type=RadioTypes.AHCA,
)


##5GRU_8
##SN:AS213009764 - AHCA3
_ru8 = RU(
    ru_hw_group="Rel3.2_FRMr_6T6R",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.16.37.130",
        username="root", 
        password="umniedziala"
    ),
    pdu_port=_ru_2_pdu.pdu_ports[3],
    radio_type=RadioTypes.AHCA,
)



##5GRU_9
##SN:EB2329R0384 - AWPQZ1
_ru9 = RU(
    ru_hw_group="Rel6.2 IDRU_4T4R",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.8.34",
        username="rfsw",
        password="KRG3dFggxxHw+s0z64U0AR22VyjfnXdHrAVdSv5jpc4=",
    ),
    pdu_port=_ru_3_pdu.pdu_ports[1],
    radio_type=RadioTypes.AWPQZ,
)

##5GRU_10
##SN:EB2314R0337 - AWPQZ2
_ru10 = RU(
    ru_hw_group="Rel6.2 IDRU_4T4R",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.8.38",
        username="rfsw",
        password="KRG3dFggxxHw+s0z64U0AR22VyjfnXdHrAVdSv5jpc4=",
    ),
    pdu_port=_ru_3_pdu.pdu_ports[2],
    radio_type=RadioTypes.AWPQZ,
)

##5GRU_11
##SN:EB2314R0319 - AWPQZ3
_ru11 = RU(
    ru_hw_group="Rel6.2 IDRU_4T4R",
    default_ssh_connection_details=SshServiceDetails(
        addr="172.22.8.42",
        username="rfsw",
        password="KRG3dFggxxHw+s0z64U0AR22VyjfnXdHrAVdSv5jpc4=",
    ),
    pdu_port=_ru_3_pdu.pdu_ports[3],
    radio_type=RadioTypes.AWPQZ,
)


# #######Iperf########
_appserver_ssh = SshServiceDetails(
    addr="10.57.162.2", username="mmw_sg2", password="mm@2", port="42128"
)

_iperf_details = IperfDataTransferDetails(
    ssh_connection_details=_appserver_ssh,
    network_interface_address="10.57.162.2",
    iperf_path="iperf",
    port="43128",
)


_appserver = AppServer(_iperf_details)



# SIGSPARK 128
_ue_host1_ssh = SshServiceDetails(
    addr="10.71.205.19", username="spark", password="spark"
)



_spark_appserver_ssh = SshServiceDetails(
    addr="10.71.219.22", 
    username="mmw_sg2", 
    password="mm@2",
)

_iperf_details_on_appserver = IperfDataTransferDetails(
    ssh_connection_details=_spark_appserver_ssh,
    network_interface_address="10.71.219.22",
    iperf_path="/usr/bin/iperf",
    port=43128,
)


# SIGSPARK
_appserver_ip_addr1 = "10.71.219.22"

_spark_appserver_ssh1 = SshServiceDetails(
    addr=_appserver_ip_addr1, username="mmw_sg2", password="mm@2"
)

_iperf_details_on_appserver1 = IperfDataTransferDetails(
    ssh_connection_details=_spark_appserver_ssh1,
    network_interface_address=_appserver_ip_addr1,
    iperf_path="iperf",
    port=43128,
)


_sigspark1 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="5fd4a06c",
    server_dir="C:\Program Files (x86)\Spark1.1.2008.60\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033100015388",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
    #capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark2 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="8927fd2d",
    server_dir="C:\Program Files (x86)\Spark1.1.2008.60\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033100012777",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
    #capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark3 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="ad750721",
    server_dir="C:\Program Files (x86)\Spark1.1.2008.60\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033100012780",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
    #capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark4 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="cdaf5c71",
    server_dir="C:\Program Files (x86)\Spark1.1.2008.60\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033100012779",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
    #capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark5 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="f02a3224",
    server_dir="C:\Program Files (x86)\Spark1.1.2008.60\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033100015389",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
    #capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark6 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="f7941d67",
    server_dir="C:\Program Files (x86)\Spark1.1.2008.60\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033100012781",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
    #capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

_sigspark7 = Android(
    ssh_connection_details=_ue_host1_ssh,
    serial_number="f911bda9",
    server_dir="C:\Program Files (x86)\Spark1.1.2008.60\Bin\Spark.exe",
    python_path="C:/Python27",
    iperf_details=_iperf_details_on_appserver,
    imsi="262033100012782",
    capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
    #capabilities=["REAL_ANDROID_UE", "huawei_sigspark"],
)

#_sigspark8 = Android(
    #ssh_connection_details=_ue_host1_ssh,
    #serial_number="021091002111001",
    #server_dir="C:\Program Files (x86)\Spark1.1.2008.60\Bin\Spark.exe",
    #python_path="C:/Python27",
    #iperf_details=_iperf_details_on_appserver,
    #imsi="262033100012783",
   # capabilities=["REAL_UE", "REAL_ANDROID_UE", "huawei_sigspark"],
#)



##DU_0 for cloudlBTS
_lmp_connection_0 = SshServiceDetails(
    addr="10.71.212.37", username="toor4nsn", password="oZPS0POrRieRtu"
)

_capacity_unit_0 = CapacityUnit(
    addr="10.71.212.37",
    hardware_type="ASIM",
)

_du_pdu = HBTE(addr="10.71.196.72", port_numbers=[2])

_common_unit_0 = CommonUnit(
    lmp_connection=_lmp_connection_0,
    capacity_units=[_capacity_unit_0],
    pdu_port=_du_pdu.pdu_ports[2],
    hardware_type="ABIP",
)

_airscale = Airscale(common_units=[_common_unit_0])

_du = DU(
    airscale=_airscale, rus=[_ru1, _ru2, _ru3, _ru4, _ru5, _ru6, _ru7, _ru8, _ru9, _ru10, _ru11], f1_m_ip_addr="10.71.212.37"
)


##CU

_cu = CU(
    backhaul_site_oam_ip="10.71.212.37",
    oam_ssh_connection_details=SshServiceDetails(
        addr="10.71.212.37", username="toor4nsn", password="oZPS0POrRieRtu"
    ),
    oam_http_connection_details=HttpConnectionDetails(
        addr="10.71.212.37", username="Nemuadmin", password="nemuuser"
    ),
)


##classicalbts------------------------------------------------
_classical_bts = ClassicalBts(dus=[_du], cu=_cu, instance_id=37154, global_bts_id=37154)

##host
_host = TestPc(
    default_ssh_connection_details=SshServiceDetails(
        addr="10.57.177.102", username="ute", password="iW_K#8.ute%A10h0m0ra"
    )
)

##cloud_topology------------------------------------------------
_tl_cloud_topology = "CLOUD_5G_CLASSICAL_ASIM_ABIP_2XFXED_2xAWPQZ_AQQA"

tl = TestLine(
    test_pc=_host,
    gnbs=[_classical_bts],
    tl_cloud_topology=_tl_cloud_topology,
    ues=[_sigspark1,_sigspark2,_sigspark3,_sigspark4,_sigspark5,_sigspark6,_sigspark7,],    
    appserver=_appserver,
    core=_epc_sim
)

# print (tl.core.default_ssh_connection_details.addr)