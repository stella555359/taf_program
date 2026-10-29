"""MCP server exposing read-only RobotWS context tools."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from robotws_mcp.profiles.store import ProfileStore
from robotws_mcp.layer2.query import Layer2QueryService
from robotws_mcp.layer3.service import GovernanceService
from robotws_mcp.layer4.service import SemanticRetrievalService
from robotws_mcp.layer5.service import TemplateExtractionService
from robotws_mcp.layer6.service import ValidationEngineService
from robotws_mcp.layer7.import_feedback import DEFAULT_FEEDBACK_DB_PATH
from robotws_mcp.layer7.service import ExecutionFeedbackService
from robotws_mcp.retrieval.context_builder import ContextBuilder, GenerationContextRequest
from robotws_mcp.validation.style_validator import StyleValidator


DEFAULT_DB_PATH = "data/indexes/robotws.sqlite3"
DEFAULT_LAYER2_DB_PATH = "data/indexes/robotws_layer2_graph.sqlite3"
DEFAULT_LAYER7_DB_PATH = DEFAULT_FEEDBACK_DB_PATH


class RobotWsMcpService:
    """Tool implementation layer independent from the MCP transport."""

    def __init__(
        self,
        db_path: str | Path = DEFAULT_DB_PATH,
        layer2_db_path: str | Path = DEFAULT_LAYER2_DB_PATH,
        layer7_db_path: str | Path = DEFAULT_LAYER7_DB_PATH,
    ) -> None:
        self.profile_store = ProfileStore()
        self.context_builder = ContextBuilder(db_path=db_path, profile_store=self.profile_store)
        self.layer2_query = Layer2QueryService(layer2_db_path)
        self.governance = GovernanceService(layer2_db_path=layer2_db_path, profile_store=self.profile_store)
        self.feedback = ExecutionFeedbackService(layer7_db_path)
        self.layer4 = SemanticRetrievalService(
            db_path=db_path,
            layer2_db_path=layer2_db_path,
            profile_store=self.profile_store,
            feedback_service=self.feedback,
        )
        self.layer5 = TemplateExtractionService(
            db_path=db_path,
            layer2_db_path=layer2_db_path,
            profile_store=self.profile_store,
            retrieval_service=self.layer4,
        )
        self.layer6 = ValidationEngineService(
            layer2_db_path=layer2_db_path,
            profile_store=self.profile_store,
            feedback_service=self.feedback,
        )
        self.validator = StyleValidator()

    def identify_robotws_profile(self, path_hint: str = "", requirement: str = "") -> dict[str, Any]:
        profile = self.profile_store.identify(path_hint=path_hint, requirement=requirement)
        return {"profile": profile.to_dict() if profile else None}

    def search_robot_cases(
        self,
        query: str,
        profile: str = "",
        tags: list[str] | None = None,
        limit: int = 10,
    ) -> dict[str, Any]:
        cases = self.context_builder.search_cases(query=query, profile=profile, limit=limit)
        if tags:
            tag_set = set(tags)
            cases = [case for case in cases if tag_set.intersection(set(case.get("tags", [])))]
        return {"cases": cases}

    def search_robot_keywords(self, query: str, profile: str = "", limit: int = 10) -> dict[str, Any]:
        return {"keywords": self.context_builder.search_keywords(query=query, profile=profile, limit=limit)}

    def get_case_pattern(self, case_name_or_path: str) -> dict[str, Any]:
        return {"case": self.context_builder.get_case_pattern(case_name_or_path)}

    def trace_keyword_usage(self, keyword_name: str, profile: str = "", depth: int = 2) -> dict[str, Any]:
        # Profile is accepted for API symmetry. Current trace is exact-name based.
        return {"keyword": keyword_name, "profile": profile, "edges": self.context_builder.trace_keyword_usage(keyword_name, depth)}

    def find_taf_library_usage(self, library_name: str, profile: str = "") -> dict[str, Any]:
        return {"library": library_name, "usage": self.context_builder.find_taf_library_usage(library_name, profile)}

    def get_style_profile(self, profile: str) -> dict[str, Any]:
        return {"profile": self.context_builder.get_style_profile(profile)}

    def get_sg6_discovery_report(self) -> dict[str, Any]:
        return self.context_builder.get_sg6_discovery_report()

    def discover_sg6_features(self, area: str = "", print_detail: bool = True) -> dict[str, Any]:
        report = self.context_builder.get_sg6_discovery_report()
        if area:
            area_upper = area.upper()
            report = {
                **report,
                "features": [
                    feature for feature in report.get("features", []) if feature.get("area", "").upper() == area_upper
                ],
            }
        if not print_detail:
            return {"summary": report.get("summary", {})}
        return report

    def get_generation_context(
        self,
        requirement: str,
        path_hint: str = "",
        profile_hint: str = "",
        limit: int = 5,
    ) -> dict[str, Any]:
        request = GenerationContextRequest(
            requirement=requirement,
            path_hint=path_hint,
            profile_hint=profile_hint,
            limit=limit,
        )
        return self.context_builder.build_generation_context(request)

    def validate_generated_case_style(self, robot_text: str, profile: str = "") -> dict[str, Any]:
        style_profile = self.profile_store.effective(profile) if profile else None
        return self.validator.validate(robot_text, style_profile).to_dict()

    def get_testcase_graph(self, testcase_name_or_id: str, depth: int = 2) -> dict[str, Any]:
        return self.layer2_query.get_testcase_graph(testcase_name_or_id, depth)

    def get_keyword_graph(self, keyword_name_or_id: str, direction: str = "downstream", depth: int = 2) -> dict[str, Any]:
        return self.layer2_query.get_keyword_graph(keyword_name_or_id, direction, depth)

    def resolve_keyword_call(self, owner_id: str, step_id: str) -> dict[str, Any]:
        return self.layer2_query.resolve_keyword_call(owner_id, step_id)

    def explain_taf_dependency(self, record_id: str) -> dict[str, Any]:
        return self.layer2_query.explain_taf_dependency(record_id)

    def find_keyword_callers(self, keyword_name: str, domain: str = "", feature: str = "", limit: int = 20) -> dict[str, Any]:
        return self.layer2_query.find_keyword_callers(keyword_name, domain, feature, limit)

    def get_unresolved_calls(self, domain: str = "", feature: str = "", status: str = "unresolved", limit: int = 50) -> dict[str, Any]:
        return self.layer2_query.get_unresolved_calls(domain, feature, status, limit)

    def evaluate_taf_usage(self, evidence: dict[str, Any]) -> dict[str, Any]:
        return self.governance.evaluate_taf_usage(evidence)

    def explain_allowed_boundary(self, record_id_or_path: str, profile: str = "Hangzhou_SG6_Common") -> dict[str, Any]:
        return self.governance.explain_allowed_boundary(record_id_or_path, profile)

    def filter_generation_context(self, candidate_ids: list[str], profile: str = "Hangzhou_SG6_Common") -> dict[str, Any]:
        return self.governance.filter_generation_context(candidate_ids, profile)

    def validate_generated_robot(self, robot_text: str, profile: str = "Hangzhou_SG6_Common") -> dict[str, Any]:
        return self.governance.validate_generated_robot(robot_text, profile)

    def retrieve_generation_context(
        self,
        requirement: str,
        profile: str = "",
        path_hint: str = "",
        limit: int = 5,
    ) -> dict[str, Any]:
        return self.layer4.retrieve_generation_context(requirement, profile, path_hint, limit)

    def search_evidence(
        self,
        query: str,
        profile: str = "",
        evidence_types: list[str] | None = None,
        limit: int = 10,
    ) -> dict[str, Any]:
        return self.layer4.search_evidence(query, profile, evidence_types, limit)

    def rank_keyword_candidates(
        self,
        query: str,
        profile: str = "",
        domain: str = "",
        feature: str = "",
        limit: int = 10,
    ) -> dict[str, Any]:
        return self.layer4.rank_keyword_candidates(query, profile, domain, feature, limit)

    def get_workflow_template(
        self,
        operation: str,
        profile: str = "",
        domain: str = "",
        requirement: str = "",
        limit: int = 3,
    ) -> dict[str, Any]:
        return self.layer5.get_workflow_template(operation, profile, domain, requirement, limit)

    def extract_template_from_requirement(
        self,
        requirement: str,
        profile: str = "",
        domain: str = "",
        limit: int = 3,
    ) -> dict[str, Any]:
        return self.layer5.extract_template_from_requirement(requirement, profile, domain, limit)

    def recommend_template_steps(
        self,
        requirement: str,
        profile: str = "",
        domain: str = "",
        limit: int = 3,
    ) -> dict[str, Any]:
        return self.layer5.recommend_template_steps(requirement, profile, domain, limit)

    def validate_generated_robot_static(
        self,
        robot_text: str,
        profile: str = "Hangzhou_SG6_Common",
        requirement: str = "",
    ) -> dict[str, Any]:
        return self.layer6.validate_generated_robot(robot_text, profile, requirement)

    def explain_validation_issue(
        self,
        robot_text: str,
        profile: str = "Hangzhou_SG6_Common",
        requirement: str = "",
    ) -> dict[str, Any]:
        return self.layer6.explain_validation_issue(robot_text, profile, requirement)

    def record_execution_feedback(self, feedback: dict[str, Any]) -> dict[str, Any]:
        return self.feedback.record_execution_feedback(feedback)

    def import_robot_output_xml(self, path: str, profile: str = "", testline: str = "") -> dict[str, Any]:
        return self.feedback.import_robot_output_xml(path, profile, testline)

    def import_jenkins_result_json(self, path: str) -> dict[str, Any]:
        return self.feedback.import_jenkins_result_json(path)

    def get_execution_feedback(self, query: str = "", profile: str = "", limit: int = 50) -> dict[str, Any]:
        return self.feedback.get_execution_feedback(query, profile, limit)

    def get_feedback_hints(self, record_id_or_name: str, profile: str = "") -> dict[str, Any]:
        return self.feedback.get_feedback_hints(record_id_or_name, profile)


def create_mcp_server(
    db_path: str | Path = DEFAULT_DB_PATH,
    layer2_db_path: str | Path = DEFAULT_LAYER2_DB_PATH,
    layer7_db_path: str | Path = DEFAULT_LAYER7_DB_PATH,
):
    try:
        from mcp.server.fastmcp import FastMCP
    except ImportError as error:
        raise RuntimeError("The 'mcp' package is required to run the MCP server.") from error

    service = RobotWsMcpService(db_path=db_path, layer2_db_path=layer2_db_path, layer7_db_path=layer7_db_path)
    mcp = FastMCP("RobotWS Knowledge Base")

    @mcp.tool()
    def identify_robotws_profile(path_hint: str = "", requirement: str = "") -> dict[str, Any]:
        return service.identify_robotws_profile(path_hint=path_hint, requirement=requirement)

    @mcp.tool()
    def search_robot_cases(query: str, profile: str = "", tags: list[str] | None = None, limit: int = 10) -> dict[str, Any]:
        return service.search_robot_cases(query=query, profile=profile, tags=tags, limit=limit)

    @mcp.tool()
    def search_robot_keywords(query: str, profile: str = "", limit: int = 10) -> dict[str, Any]:
        return service.search_robot_keywords(query=query, profile=profile, limit=limit)

    @mcp.tool()
    def get_case_pattern(case_name_or_path: str) -> dict[str, Any]:
        return service.get_case_pattern(case_name_or_path=case_name_or_path)

    @mcp.tool()
    def trace_keyword_usage(keyword_name: str, profile: str = "", depth: int = 2) -> dict[str, Any]:
        return service.trace_keyword_usage(keyword_name=keyword_name, profile=profile, depth=depth)

    @mcp.tool()
    def find_taf_library_usage(library_name: str, profile: str = "") -> dict[str, Any]:
        return service.find_taf_library_usage(library_name=library_name, profile=profile)

    @mcp.tool()
    def get_style_profile(profile: str) -> dict[str, Any]:
        return service.get_style_profile(profile=profile)

    @mcp.tool()
    def get_sg6_discovery_report() -> dict[str, Any]:
        return service.get_sg6_discovery_report()

    @mcp.tool()
    def discover_sg6_features(area: str = "", print_detail: bool = True) -> dict[str, Any]:
        return service.discover_sg6_features(area=area, print_detail=print_detail)

    @mcp.tool()
    def get_generation_context(requirement: str, path_hint: str = "", profile_hint: str = "", limit: int = 5) -> dict[str, Any]:
        return service.get_generation_context(
            requirement=requirement,
            path_hint=path_hint,
            profile_hint=profile_hint,
            limit=limit,
        )

    @mcp.tool()
    def validate_generated_case_style(robot_text: str, profile: str = "") -> dict[str, Any]:
        return service.validate_generated_case_style(robot_text=robot_text, profile=profile)

    @mcp.tool()
    def get_testcase_graph(testcase_name_or_id: str, depth: int = 2) -> dict[str, Any]:
        return service.get_testcase_graph(testcase_name_or_id=testcase_name_or_id, depth=depth)

    @mcp.tool()
    def get_keyword_graph(keyword_name_or_id: str, direction: str = "downstream", depth: int = 2) -> dict[str, Any]:
        return service.get_keyword_graph(keyword_name_or_id=keyword_name_or_id, direction=direction, depth=depth)

    @mcp.tool()
    def resolve_keyword_call(owner_id: str, step_id: str) -> dict[str, Any]:
        return service.resolve_keyword_call(owner_id=owner_id, step_id=step_id)

    @mcp.tool()
    def explain_taf_dependency(record_id: str) -> dict[str, Any]:
        return service.explain_taf_dependency(record_id=record_id)

    @mcp.tool()
    def find_keyword_callers(keyword_name: str, domain: str = "", feature: str = "", limit: int = 20) -> dict[str, Any]:
        return service.find_keyword_callers(keyword_name=keyword_name, domain=domain, feature=feature, limit=limit)

    @mcp.tool()
    def get_unresolved_calls(domain: str = "", feature: str = "", status: str = "unresolved", limit: int = 50) -> dict[str, Any]:
        return service.get_unresolved_calls(domain=domain, feature=feature, status=status, limit=limit)

    @mcp.tool()
    def evaluate_taf_usage(evidence: dict[str, Any]) -> dict[str, Any]:
        return service.evaluate_taf_usage(evidence=evidence)

    @mcp.tool()
    def explain_allowed_boundary(record_id_or_path: str, profile: str = "Hangzhou_SG6_Common") -> dict[str, Any]:
        return service.explain_allowed_boundary(record_id_or_path=record_id_or_path, profile=profile)

    @mcp.tool()
    def filter_generation_context(candidate_ids: list[str], profile: str = "Hangzhou_SG6_Common") -> dict[str, Any]:
        return service.filter_generation_context(candidate_ids=candidate_ids, profile=profile)

    @mcp.tool()
    def validate_generated_robot(robot_text: str, profile: str = "Hangzhou_SG6_Common") -> dict[str, Any]:
        return service.validate_generated_robot(robot_text=robot_text, profile=profile)

    @mcp.tool()
    def retrieve_generation_context(requirement: str, profile: str = "", path_hint: str = "", limit: int = 5) -> dict[str, Any]:
        return service.retrieve_generation_context(requirement=requirement, profile=profile, path_hint=path_hint, limit=limit)

    @mcp.tool()
    def search_evidence(query: str, profile: str = "", evidence_types: list[str] | None = None, limit: int = 10) -> dict[str, Any]:
        return service.search_evidence(query=query, profile=profile, evidence_types=evidence_types, limit=limit)

    @mcp.tool()
    def rank_keyword_candidates(query: str, profile: str = "", domain: str = "", feature: str = "", limit: int = 10) -> dict[str, Any]:
        return service.rank_keyword_candidates(query=query, profile=profile, domain=domain, feature=feature, limit=limit)

    @mcp.tool()
    def get_workflow_template(operation: str, profile: str = "", domain: str = "", requirement: str = "", limit: int = 3) -> dict[str, Any]:
        return service.get_workflow_template(operation=operation, profile=profile, domain=domain, requirement=requirement, limit=limit)

    @mcp.tool()
    def extract_template_from_requirement(requirement: str, profile: str = "", domain: str = "", limit: int = 3) -> dict[str, Any]:
        return service.extract_template_from_requirement(requirement=requirement, profile=profile, domain=domain, limit=limit)

    @mcp.tool()
    def recommend_template_steps(requirement: str, profile: str = "", domain: str = "", limit: int = 3) -> dict[str, Any]:
        return service.recommend_template_steps(requirement=requirement, profile=profile, domain=domain, limit=limit)

    @mcp.tool()
    def validate_generated_robot_static(robot_text: str, profile: str = "Hangzhou_SG6_Common", requirement: str = "") -> dict[str, Any]:
        return service.validate_generated_robot_static(robot_text=robot_text, profile=profile, requirement=requirement)

    @mcp.tool()
    def explain_validation_issue(robot_text: str, profile: str = "Hangzhou_SG6_Common", requirement: str = "") -> dict[str, Any]:
        return service.explain_validation_issue(robot_text=robot_text, profile=profile, requirement=requirement)

    @mcp.tool()
    def record_execution_feedback(feedback: dict[str, Any]) -> dict[str, Any]:
        return service.record_execution_feedback(feedback=feedback)

    @mcp.tool()
    def import_robot_output_xml(path: str, profile: str = "", testline: str = "") -> dict[str, Any]:
        return service.import_robot_output_xml(path=path, profile=profile, testline=testline)

    @mcp.tool()
    def import_jenkins_result_json(path: str) -> dict[str, Any]:
        return service.import_jenkins_result_json(path=path)

    @mcp.tool()
    def get_execution_feedback(query: str = "", profile: str = "", limit: int = 50) -> dict[str, Any]:
        return service.get_execution_feedback(query=query, profile=profile, limit=limit)

    @mcp.tool()
    def get_feedback_hints(record_id_or_name: str, profile: str = "") -> dict[str, Any]:
        return service.get_feedback_hints(record_id_or_name=record_id_or_name, profile=profile)

    return mcp


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run RobotWS MCP server.")
    parser.add_argument("--db-path", default=DEFAULT_DB_PATH, help="SQLite index path.")
    parser.add_argument("--layer2-db-path", default=DEFAULT_LAYER2_DB_PATH, help="Layer 2 graph SQLite index path.")
    parser.add_argument("--layer7-db-path", default=DEFAULT_LAYER7_DB_PATH, help="Layer 7 feedback SQLite index path.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    mcp = create_mcp_server(db_path=args.db_path, layer2_db_path=args.layer2_db_path, layer7_db_path=args.layer7_db_path)
    mcp.run()


if __name__ == "__main__":
    main()
