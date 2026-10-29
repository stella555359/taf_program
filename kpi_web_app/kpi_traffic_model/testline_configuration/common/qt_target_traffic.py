ASIB_ABIO_5G_NSA_4G_FDD_traffic_4G = [70, 200, 50]      #[iperf_duration, MAX_DL, MAX_UL, optional:min_percentage=0.8]
ASIB_ABIO_5G_NSA_4G_FDD_traffic_5G = [70, 80, 20]       #[iperf_duration, MAX_DL, MAX_UL, optional:min_percentage=0.8]
ASIB_FSMF_ABIA_4G_3G_2G_traffic_2G = [70, 0.05, 0.025]  #[iperf_duration, MAX_DL, MAX_UL, optional:min_percentage=0.8]
ASIB_FSMF_ABIA_4G_3G_2G_traffic_3G = [70, 0.4, 0.2]     #[iperf_duration, MAX_DL, MAX_UL, optional:min_percentage=0.8]
ASIB_FSMF_ABIA_4G_3G_2G_traffic_4G = [70, 15, 10]       #[iperf_duration, MAX_DL, MAX_UL, optional:min_percentage=0.8]
ASIK_ABIL_5G_SA_FDD_traffic_5G     = [70, 100, 50]      #[iperf_duration, MAX_DL, MAX_UL, optional:min_percentage=0.8]
ASIK_ABIL_5G_SA_TDD_traffic_5G     = [180, 400, 40]     #[iperf_duration, MAX_DL, MAX_UL, optional:min_percentage=0.8]
ASIM_ABIP_5G_NSA_TDD_traffic_5G    = [180, 300, 30]     #[iperf_duration, MAX_DL, MAX_UL, optional:min_percentage=0.8]
ASOE_5G_NSA_TDD_traffic_5G         = [180, 400, 50]     #[iperf_duration, MAX_DL, MAX_UL, optional:min_percentage=0.8]
ASOG_5G_NSA_TDD_traffic_5G         = [180, 150, 40]     #[iperf_duration, MAX_DL, MAX_UL, optional:min_percentage=0.8]
ASOG_5G_NSA_TDD_traffic_5G         = [180, 150, 40]     #[iperf_duration, MAX_DL, MAX_UL, optional:min_percentage=0.8]
CPRI_FDD_NSA_Thor_traffic_5G       = [70, 80, 20]       #[iperf_duration, MAX_DL, MAX_UL, optional:min_percentage=0.8]
eCPRI_TDD_SA_Thor_traffic_5G       = [180, 300, 30]     #[iperf_duration, MAX_DL, MAX_UL, optional:min_percentage=0.8]


def create_dict_with_target_traffic(iperf_duration, max_dl, max_ul, min_percentage, **kwargs):
    if type(max_dl) == int:
        min_dl = int(max_dl * min_percentage)
    else:
        min_dl = round(max_dl * min_percentage, 2)

    if type(max_ul) == int:
        min_ul = int(max_ul * min_percentage)
    else:
        min_ul = round((max_ul * min_percentage), 2)

    return {
        "IPERF_DURATION" : iperf_duration,  # seconds
        "MIN_DL": min_dl,  # Mbits/sec
        "MAX_DL": max_dl,  # Mbits/sec
        "MIN_UL": min_ul,  # Mbits/sec
        "MAX_UL": max_ul,  # Mbits/sec
        **kwargs
        }


def get_target_traffic(product_name, _2G_3G_4G_5G="", min_percentage=0.8, **kwargs):
    try:
        product = product_name.split("-")
        product = str(product[1]) + "_traffic_" + _2G_3G_4G_5G
    except IndexError:
        product = product_name
    create_dict_with_target_traffic(*globals()[product], min_percentage, **kwargs)
