from .rules import (
    airphone_mandatory_params,
    rpi_mandatory_params,
    prisma_mandatory_params,
    appserver_mandatory_params,
    gnbs_mandatory_params,
)


class Rules(object):
    CLOUD_5G_CLASSICAL_AP = [
        airphone_mandatory_params,
    ]

    CLOUD_5G_RPI_ASIKA101L_ABILA101B1_AEUA = [
        rpi_mandatory_params,
    ]

    CLOUD_5G_CLASSICAL_PRISMA_ASIKL_ABILB1_AHLOA_ENB = [
        prisma_mandatory_params,
        appserver_mandatory_params,
        gnbs_mandatory_params,
    ]
