from __future__ import annotations

import json
from pathlib import Path

from robotws_mcp.layer7.service import ExecutionFeedbackService


def test_record_execution_feedback_and_query_hints(tmp_path: Path) -> None:
    service = ExecutionFeedbackService(tmp_path / "feedback.sqlite3")

    service.record_execution_feedback(
        {
            "source_type": "manual",
            "test_name": "BASIC_L3_Call",
            "keyword_name": "Make_L3_Call_With_MTK_UE",
            "status": "fail",
            "message": "connection timeout",
            "profile": "Hangzhou_RRM_SG6_Feature",
        }
    )

    feedback = service.get_execution_feedback("MTK", profile="Hangzhou_RRM_SG6_Feature")
    hints = service.get_feedback_hints("Make_L3_Call_With_MTK_UE", profile="Hangzhou_RRM_SG6_Feature")

    assert feedback["feedback"][0]["failure_class"] == "timeout"
    assert hints["has_failures"] is True
    assert hints["failure_count"] == 1


def test_import_robot_output_xml(tmp_path: Path) -> None:
    output = tmp_path / "output.xml"
    output.write_text(
        """<robot>
  <suite name="Suite">
    <test name="BASIC_L3_Call">
      <kw name="Attach Ue"><status status="PASS" elapsedtime="10"/></kw>
      <kw name="Check Tput"><status status="FAIL" elapsedtime="20">timeout while collecting tput</status></kw>
      <status status="FAIL" elapsedtime="100">timeout while collecting tput</status>
    </test>
  </suite>
</robot>""",
        encoding="utf-8",
    )
    service = ExecutionFeedbackService(tmp_path / "feedback.sqlite3")

    result = service.import_robot_output_xml(str(output), profile="Hangzhou_RRM_SG6_Feature", testline="T813")
    hints = service.get_feedback_hints("Check Tput", profile="Hangzhou_RRM_SG6_Feature")

    assert result["imported"] == 2
    assert hints["has_failures"] is True
    assert hints["recent_failures"][0]["failure_class"] == "timeout"


def test_import_jenkins_result_json(tmp_path: Path) -> None:
    path = tmp_path / "jenkins.json"
    path.write_text(
        json.dumps(
            {
                "profile": "Hangzhou_RRM_SG6_Feature",
                "testline": "T813",
                "tests": [
                    {
                        "test_name": "BASIC_L3_Call",
                        "failed_keyword": "Detach Ue",
                        "status": "FAIL",
                        "message": "unknown keyword",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    service = ExecutionFeedbackService(tmp_path / "feedback.sqlite3")

    result = service.import_jenkins_result_json(str(path))

    assert result["imported"] == 1
    assert result["records"][0]["failure_class"] == "keyword_resolution"

