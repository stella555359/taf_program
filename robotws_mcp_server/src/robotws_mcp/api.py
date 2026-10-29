"""HTTP API for centralized RobotWS knowledge queries."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel, Field

from robotws_mcp import __version__
from robotws_mcp.server import DEFAULT_DB_PATH, DEFAULT_LAYER2_DB_PATH, DEFAULT_LAYER7_DB_PATH, RobotWsMcpService


class GenerationContextBody(BaseModel):
    requirement: str
    profile: str = ""
    path_hint: str = ""
    limit: int = Field(default=5, ge=1, le=50)


class SearchBody(BaseModel):
    query: str
    profile: str = ""
    limit: int = Field(default=10, ge=1, le=100)


class ValidateStyleBody(BaseModel):
    robot_text: str
    profile: str = ""


class TestcaseGraphBody(BaseModel):
    testcase_name_or_id: str
    depth: int = Field(default=2, ge=1, le=10)


class KeywordGraphBody(BaseModel):
    keyword_name_or_id: str
    direction: str = "downstream"
    depth: int = Field(default=2, ge=1, le=10)


class ResolveKeywordCallBody(BaseModel):
    owner_id: str
    step_id: str


class TafDependencyBody(BaseModel):
    record_id: str


class KeywordCallersBody(BaseModel):
    keyword_name: str
    domain: str = ""
    feature: str = ""
    limit: int = Field(default=20, ge=1, le=100)


class UnresolvedCallsBody(BaseModel):
    domain: str = ""
    feature: str = ""
    status: str = "unresolved"
    limit: int = Field(default=50, ge=1, le=200)


class TafUsageBody(BaseModel):
    evidence: dict[str, Any]


class BoundaryBody(BaseModel):
    record_id_or_path: str
    profile: str = "Hangzhou_SG6_Common"


class FilterGenerationContextBody(BaseModel):
    candidate_ids: list[str]
    profile: str = "Hangzhou_SG6_Common"


class GovernanceValidateRobotBody(BaseModel):
    robot_text: str
    profile: str = "Hangzhou_SG6_Common"


class Layer4RetrievalBody(BaseModel):
    requirement: str
    profile: str = ""
    path_hint: str = ""
    limit: int = Field(default=5, ge=1, le=50)


class EvidenceSearchBody(BaseModel):
    query: str
    profile: str = ""
    evidence_types: list[str] | None = None
    limit: int = Field(default=10, ge=1, le=100)


class KeywordRankBody(BaseModel):
    query: str
    profile: str = ""
    domain: str = ""
    feature: str = ""
    limit: int = Field(default=10, ge=1, le=100)


class TemplateBody(BaseModel):
    operation: str = ""
    requirement: str = ""
    profile: str = ""
    domain: str = ""
    limit: int = Field(default=3, ge=1, le=20)


class StaticValidationBody(BaseModel):
    robot_text: str
    profile: str = "Hangzhou_SG6_Common"
    requirement: str = ""


class FeedbackBody(BaseModel):
    feedback: dict[str, Any]


class RobotOutputImportBody(BaseModel):
    path: str
    profile: str = ""
    testline: str = ""


class JenkinsImportBody(BaseModel):
    path: str


class FeedbackQueryBody(BaseModel):
    query: str = ""
    profile: str = ""
    limit: int = Field(default=50, ge=1, le=200)


class FeedbackHintsBody(BaseModel):
    record_id_or_name: str
    profile: str = ""


def create_api_app(
    db_path: str | Path = DEFAULT_DB_PATH,
    layer2_db_path: str | Path = DEFAULT_LAYER2_DB_PATH,
    layer7_db_path: str | Path = DEFAULT_LAYER7_DB_PATH,
) -> FastAPI:
    """Create a RobotWS Knowledge API app."""

    service = RobotWsMcpService(db_path=db_path, layer2_db_path=layer2_db_path, layer7_db_path=layer7_db_path)
    app = FastAPI(title="RobotWS Knowledge API", version=__version__)

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/version")
    def version() -> dict[str, Any]:
        return {
            "name": "robotws-knowledge-api",
            "version": __version__,
            "db_path": str(db_path),
        }

    @app.get("/profiles")
    def profiles() -> dict[str, list[dict[str, Any]]]:
        return {"profiles": [profile.to_dict() for profile in service.profile_store.all()]}

    @app.get("/discovery/sg6")
    def sg6_discovery() -> dict[str, Any]:
        return service.get_sg6_discovery_report()

    @app.post("/query/generation-context")
    def generation_context(body: GenerationContextBody) -> dict[str, Any]:
        return service.get_generation_context(
            requirement=body.requirement,
            path_hint=body.path_hint,
            profile_hint=body.profile,
            limit=body.limit,
        )

    @app.post("/query/search-cases")
    def search_cases(body: SearchBody) -> dict[str, Any]:
        return service.search_robot_cases(query=body.query, profile=body.profile, limit=body.limit)

    @app.post("/query/search-keywords")
    def search_keywords(body: SearchBody) -> dict[str, Any]:
        return service.search_robot_keywords(query=body.query, profile=body.profile, limit=body.limit)

    @app.post("/query/validate-style")
    def validate_style(body: ValidateStyleBody) -> dict[str, Any]:
        return service.validate_generated_case_style(robot_text=body.robot_text, profile=body.profile)

    @app.post("/query/layer2/testcase-graph")
    def testcase_graph(body: TestcaseGraphBody) -> dict[str, Any]:
        return service.get_testcase_graph(testcase_name_or_id=body.testcase_name_or_id, depth=body.depth)

    @app.post("/query/layer2/keyword-graph")
    def keyword_graph(body: KeywordGraphBody) -> dict[str, Any]:
        return service.get_keyword_graph(
            keyword_name_or_id=body.keyword_name_or_id,
            direction=body.direction,
            depth=body.depth,
        )

    @app.post("/query/layer2/resolve-keyword-call")
    def resolve_keyword_call(body: ResolveKeywordCallBody) -> dict[str, Any]:
        return service.resolve_keyword_call(owner_id=body.owner_id, step_id=body.step_id)

    @app.post("/query/layer2/explain-taf-dependency")
    def explain_taf_dependency(body: TafDependencyBody) -> dict[str, Any]:
        return service.explain_taf_dependency(record_id=body.record_id)

    @app.post("/query/layer2/find-keyword-callers")
    def find_keyword_callers(body: KeywordCallersBody) -> dict[str, Any]:
        return service.find_keyword_callers(
            keyword_name=body.keyword_name,
            domain=body.domain,
            feature=body.feature,
            limit=body.limit,
        )

    @app.post("/query/layer2/unresolved-calls")
    def unresolved_calls(body: UnresolvedCallsBody) -> dict[str, Any]:
        return service.get_unresolved_calls(
            domain=body.domain,
            feature=body.feature,
            status=body.status,
            limit=body.limit,
        )

    @app.post("/query/layer3/evaluate-taf-usage")
    def evaluate_taf_usage(body: TafUsageBody) -> dict[str, Any]:
        return service.evaluate_taf_usage(evidence=body.evidence)

    @app.post("/query/layer3/explain-allowed-boundary")
    def explain_allowed_boundary(body: BoundaryBody) -> dict[str, Any]:
        return service.explain_allowed_boundary(record_id_or_path=body.record_id_or_path, profile=body.profile)

    @app.post("/query/layer3/filter-generation-context")
    def filter_generation_context(body: FilterGenerationContextBody) -> dict[str, Any]:
        return service.filter_generation_context(candidate_ids=body.candidate_ids, profile=body.profile)

    @app.post("/query/layer3/validate-generated-robot")
    def validate_generated_robot(body: GovernanceValidateRobotBody) -> dict[str, Any]:
        return service.validate_generated_robot(robot_text=body.robot_text, profile=body.profile)

    @app.post("/query/layer4/retrieve-generation-context")
    def retrieve_generation_context(body: Layer4RetrievalBody) -> dict[str, Any]:
        return service.retrieve_generation_context(
            requirement=body.requirement,
            profile=body.profile,
            path_hint=body.path_hint,
            limit=body.limit,
        )

    @app.post("/query/layer4/search-evidence")
    def search_evidence(body: EvidenceSearchBody) -> dict[str, Any]:
        return service.search_evidence(
            query=body.query,
            profile=body.profile,
            evidence_types=body.evidence_types,
            limit=body.limit,
        )

    @app.post("/query/layer4/rank-keyword-candidates")
    def rank_keyword_candidates(body: KeywordRankBody) -> dict[str, Any]:
        return service.rank_keyword_candidates(
            query=body.query,
            profile=body.profile,
            domain=body.domain,
            feature=body.feature,
            limit=body.limit,
        )

    @app.post("/query/layer5/workflow-template")
    def workflow_template(body: TemplateBody) -> dict[str, Any]:
        return service.get_workflow_template(
            operation=body.operation,
            profile=body.profile,
            domain=body.domain,
            requirement=body.requirement,
            limit=body.limit,
        )

    @app.post("/query/layer5/extract-template")
    def extract_template(body: TemplateBody) -> dict[str, Any]:
        return service.extract_template_from_requirement(
            requirement=body.requirement,
            profile=body.profile,
            domain=body.domain,
            limit=body.limit,
        )

    @app.post("/query/layer5/recommend-template-steps")
    def recommend_template_steps(body: TemplateBody) -> dict[str, Any]:
        return service.recommend_template_steps(
            requirement=body.requirement,
            profile=body.profile,
            domain=body.domain,
            limit=body.limit,
        )

    @app.post("/query/layer6/validate-generated-robot")
    def validate_generated_robot_static(body: StaticValidationBody) -> dict[str, Any]:
        return service.validate_generated_robot_static(
            robot_text=body.robot_text,
            profile=body.profile,
            requirement=body.requirement,
        )

    @app.post("/query/layer6/explain-validation-issue")
    def explain_validation_issue(body: StaticValidationBody) -> dict[str, Any]:
        return service.explain_validation_issue(
            robot_text=body.robot_text,
            profile=body.profile,
            requirement=body.requirement,
        )

    @app.post("/query/layer7/record-execution-feedback")
    def record_execution_feedback(body: FeedbackBody) -> dict[str, Any]:
        return service.record_execution_feedback(feedback=body.feedback)

    @app.post("/query/layer7/import-robot-output-xml")
    def import_robot_output_xml(body: RobotOutputImportBody) -> dict[str, Any]:
        return service.import_robot_output_xml(path=body.path, profile=body.profile, testline=body.testline)

    @app.post("/query/layer7/import-jenkins-result-json")
    def import_jenkins_result_json(body: JenkinsImportBody) -> dict[str, Any]:
        return service.import_jenkins_result_json(path=body.path)

    @app.post("/query/layer7/execution-feedback")
    def get_execution_feedback(body: FeedbackQueryBody) -> dict[str, Any]:
        return service.get_execution_feedback(query=body.query, profile=body.profile, limit=body.limit)

    @app.post("/query/layer7/feedback-hints")
    def get_feedback_hints(body: FeedbackHintsBody) -> dict[str, Any]:
        return service.get_feedback_hints(record_id_or_name=body.record_id_or_name, profile=body.profile)

    return app


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run RobotWS Knowledge API.")
    parser.add_argument("--db-path", default=DEFAULT_DB_PATH, help="SQLite index path.")
    parser.add_argument("--layer2-db-path", default=DEFAULT_LAYER2_DB_PATH, help="Layer 2 graph SQLite index path.")
    parser.add_argument("--layer7-db-path", default=DEFAULT_LAYER7_DB_PATH, help="Layer 7 feedback SQLite index path.")
    parser.add_argument("--host", default="127.0.0.1", help="API bind host.")
    parser.add_argument("--port", type=int, default=8051, help="API bind port.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        import uvicorn
    except ImportError as error:
        raise RuntimeError("The 'uvicorn' package is required to run the HTTP API.") from error

    uvicorn.run(
        create_api_app(db_path=args.db_path, layer2_db_path=args.layer2_db_path, layer7_db_path=args.layer7_db_path),
        host=args.host,
        port=args.port,
    )


if __name__ == "__main__":
    main()
