from __future__ import annotations

from pathlib import Path

from robotws_mcp.layer1.robot_ast_parser import RobotAstParser
from robotws_mcp.models import StyleProfile


def _profile() -> StyleProfile:
    return StyleProfile(
        name="Hangzhou_SG6_Common",
        description="test",
        path_scopes=[],
        preferred_keywords={},
        negative_patterns=[],
        style_rules=[],
        required_fields=[],
        confirmed_case_scopes=[],
        allowed_resource_scopes=["testsuite/Hangzhou/resources/RAN_PZ_HAZ_34/robot"],
        feature_allowlist={"RRM": ["CB010767"]},
    )


def test_robot_ast_parser_extracts_setup_logical_actions(tmp_path: Path) -> None:
    root = tmp_path
    robot_path = root / "testsuite" / "Hangzhou" / "RRM" / "RAN_PZ_HAZ_34" / "CB010767" / "case.robot"
    robot_path.parent.mkdir(parents=True)
    robot_path.write_text(
        "*** Test Cases ***\n"
        "Example Case\n"
        "    [Tags]    CRT\n"
        "    [Setup]    Run Keywords\n"
        "    ...    Run Keyword If    '${stream}'=='SBTS25R1'    Set Test Variable    ${update_params}    ${scf_update_params_9363_6}\n"
        "    ...    AND    9363_D_Case_SetUp    framestructure=1208\n"
        "    Do Verification    ${update_params}\n\n"
        "*** Keywords ***\n"
        "9363_D_Case_SetUp\n"
        "    [Arguments]    ${framestructure}=1208\n"
        "    ${cell_info}=    Get Cell Info    ${cell}\n"
        "    ${patternIdMax} =    Get Length    ${items}\n"
        "    Check CSV Contains Expected Counter    result.csv    pass\n",
        encoding="utf-8",
    )

    parsed = RobotAstParser().parse_file(robot_path, root=root, profile=_profile())

    assert len(parsed.testcases) == 1
    case = parsed.testcases[0]
    assert case.is_allowed is True
    assert case.domain == "RRM"
    assert case.setup_step_ids

    setup_steps = [step for step in parsed.steps if step.normalized_type == "setup"]
    assert [step.keyword for step in setup_steps] == ["Set Test Variable", "9363_D_Case_SetUp"]
    assert setup_steps[0].condition == "'${stream}'=='SBTS25R1'"
    assert setup_steps[0].variables_output == ["${update_params}"]
    assert setup_steps[0].variables_input == ["${scf_update_params_9363_6}", "${stream}"]
    assert setup_steps[1].arguments[0].kind == "named"
    assert setup_steps[1].arguments[0].name == "framestructure"
    assert setup_steps[1].arguments[0].value == "1208"

    keyword = next(item for item in parsed.keywords if item.name == "9363_D_Case_SetUp")
    assert keyword.arguments_schema[0].name == "framestructure"
    assert keyword.arguments_schema[0].default == "1208"
    assert keyword.keyword_sequence == ["Get Cell Info", "Get Length", "Check CSV Contains Expected Counter"]

    keyword_steps = [step for step in parsed.steps if step.owner_type == "keyword"]
    get_cell_step = next(step for step in keyword_steps if step.keyword == "Get Cell Info")
    assert get_cell_step.variables_output == ["${cell_info}"]
    assert get_cell_step.variables_input == ["${cell}"]
    get_length_step = next(step for step in keyword_steps if step.keyword == "Get Length")
    assert get_length_step.variables_output == ["${patternIdMax}"]
    assert get_length_step.variables_input == ["${items}"]
