from taf.config.testline import RU
from taf.config.testline.connection_details import SshServiceDetails
from importlib.resources import files
import os


rus = {
    "AHLOA" : {
        "default_ssh_connection_details" : {
            "addr" : "172.16.37.129",
            "username" : "root",
            "password" : ""
        },
        "lmp_connection" : {
            "addr" : "5.5.5.5",
            "username" : "root",
            "password" : ""
        }
    },

    "AHFIB" : {
        "default_ssh_connection_details" : {
            "addr" : "172.16.37.128",
            "username" : "root",
            "password" : ""
        },
        "lmp_connection" : {
            "addr" : "5.5.5.5",
            "username" : "root",
            "password" : ""
        },
    },

    "AEHC" : {
        "default_ssh_connection_details" : {
            "addr" : "172.22.0.162",
            "username" : "rfsw",
            "password" : "HfBKgqIOogKY3BlGtiniuCI9bs76C8jYsAY6vw8f/Tw="
        },
        "lmp_connection" : {
            "addr" : "192.168.100.1",
            "username" : "root",
            "password" : "root"
        }
    },

    "AEQP" : {
        "default_ssh_connection_details" : {
            "addr" : "192.168.254.34",
            "username" : "serviceuser",
            "password" : "bobuWrUHk7Xq7WPpY9ZcjEi8zNdX3plZ+/y420RZ7W4="
        },
        "lmp_connection" : {
            "addr" : "192.168.254.34",
            "username" : "serviceuser",
            "password" : "bobuWrUHk7Xq7WPpY9ZcjEi8zNdX3plZ+/y420RZ7W4="
        }
    },

    "AEQE" : {
        "default_ssh_connection_details" : {
            "addr" : "172.22.48.162",
            "username" : "root",
            "password" : "w@=EIj7P6R0bVy85OjCVa^ho&8"
        },
        "lmp_connection" : {
            "addr" : "5.5.5.5",
            "username" : "root",
            "password" : "w@=EIj7P6R0bVy85OjCVa^ho&8"
        }
    },

   "AHCA" : {
        "default_ssh_connection_details" : {
            "addr" : "172.16.73.131",
            "username" : "root",
            "password" : ""
        },
        "lmp_connection" : {
            "addr" : "5.5.5.5",
            "username" : "root",
            "password" : ""
        }
    },

    "AEUD" : {
        "default_ssh_connection_details" : {
            "addr" : "172.22.48.162",
            "username" : "root",
            "password" : "umniedziala"
        },
        "lmp_connection" : {
            "addr" : "5.5.5.5",
            "username" : "root",
            "password" : "umniedziala"
        }
    },

    "AVQL" : {
        "default_ssh_connection_details" : {
            "addr" : "",
            "username" : "",
            "password" : ""
        },
        "lmp_connection" : {
            "addr" : "5.5.5.5",
            "username" : "root",
            "password" : ""
        }
    },

    "AHDB" : {
        "default_ssh_connection_details" : {
            "addr" : "172.16.33.128",
            "username" : "root",
            "password" : ""
        },
        "lmp_connection" : {
            "addr" : "5.5.5.5",
            "username" : "root",
            "password" : ""
        }
    },

    "FXJB" : {
        "default_ssh_connection_details" : {
            "addr" : "192.168.253.230",
            "username" : "root",
            "password" : ""
        },
        "lmp_connection" : {
            "addr" : "5.5.5.5",
            "username" : "root",
            "password" : ""
        }
    },
}


def get_rf_family(ru_type):
    ru_csv_path = files("taf") / "config" / "testline" / "info" / "data" / "ru_list.csv"
    with open(ru_csv_path, encoding="utf-8") as f:
        data = f.read().splitlines()
        headlines = data[0].split(";")

        records = [
            dict(zip(headlines, row.split(";")))
            for row in data[1:]
        ]

        for rus_dict in records:
            if rus_dict["RU name"] == ru_type:
                return (rus_dict["RF family"])


def QT_RU(ru_type, serial_nr, **kwargs):
    ru_conf = rus[str(ru_type)]

    ru_obj =  RU(
        radio_type=ru_type,
        ru_hw_group = get_rf_family(ru_type),
        default_ssh_connection_details=SshServiceDetails(
            addr=ru_conf["default_ssh_connection_details"]["addr"],
            username=ru_conf["default_ssh_connection_details"]["username"],
            password=ru_conf["default_ssh_connection_details"]["password"]
        ),
        lmp_connection=SshServiceDetails(
            addr=ru_conf["lmp_connection"]["addr"],
            username=ru_conf["lmp_connection"]["username"],
            password=ru_conf["lmp_connection"]["password"]
        ),
        serial_number=serial_nr,
        **kwargs
    )
    return ru_obj
