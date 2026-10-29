
import pathlib
import json
import collections
import mock  # pylint: disable=locally-disabled, E0401

from testsuite.Ulm.ET.Performance_Test.resources.test.testmock.ute_wtssim import UteWtsSimMock
from testsuite.Ulm.ET.Performance_Test.resources.python import wts_manager


def test_total_command_should_match_expected():
    utemock = UteWtsSimMock()
    with mock.patch('testsuite.Ulm.ET.Performance_Test.resources.python.wts_manager.get_egate_obj',
                    return_value=utemock):
        start = 20
        num_cells = 9
        testcase_arguments = {
            'active_cells': ["1", "3"], 'ue_count': "10"
        }
        ue_group1_args = {
            "ue_register": [{
                "id": "<ue>", "nwslice": 1, "pass_regexp": "Registered state.", "command_delay": 0
            }],
            "test_cmd": [{
                "id": "test string <ue>"
            }]
        }
        wts_manager.send_ue_commands(
            start=start, num_cells=num_cells, **testcase_arguments, **ue_group1_args)
        assert (10 * 2) == len(utemock.registered_ue_ids)


def test_json_command_should_match_expected():
    utemock = UteWtsSimMock()
    with mock.patch('testsuite.Ulm.ET.Performance_Test.resources.python.wts_manager.get_egate_obj',
                    return_value=utemock):
        wts_manager.send_ue_commands_from_json(
            pathlib.Path(__file__).parent.resolve().joinpath("test_files", "wts_manager.json"),
            start=20,
            num_cells=9,
            active_cells=[1, 3],
            ue_count=10
        )
        assert (10 * 2) == len(utemock.registered_ue_ids)


def test_read_cmd_should_match_expected():
    utemock = UteWtsSimMock()
    with mock.patch('testsuite.Ulm.ET.Performance_Test.resources.python.wts_manager.get_egate_obj',
                    return_value=utemock):
        with open(pathlib.Path(__file__).parent.resolve().joinpath("test_files", "wts_manager.json"),
                  "r", encoding="utf-8") as rstream:
            jdata = json.load(
                rstream, object_pairs_hook=collections.OrderedDict)
        wts_manager.send_ue_commands(
            start=20,
            num_cells=9,
            active_cells=[1, 3],
            ue_count=10,
            **jdata
        )
        assert (10 * 2) == len(utemock.registered_ue_ids)


def test_get_cell_id_for_ue():
    assert wts_manager.is_ue_included(1, 6, [1, 2, 3, 4, 5, 6]) is True
    assert wts_manager.is_ue_included(1, 9, [1, 3]) is True
    assert wts_manager.is_ue_included(2, 9, [1, 3]) is False
