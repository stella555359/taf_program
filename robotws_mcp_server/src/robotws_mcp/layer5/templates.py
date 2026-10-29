"""Built-in workflow template definitions."""

from __future__ import annotations

from robotws_mcp.layer5.models import TemplateStep


L3_CALL_STEPS = [
    TemplateStep(
        role="setup",
        description="Prepare SG6/RRM case environment with feature-local setup.",
        search_terms=["case setup", "9198 case setup", "8015 case setup", "8247 case setup"],
        rationale="Setup must come from the active domain/feature boundary.",
    ),
    TemplateStep(
        role="attach",
        description="Prepare and attach UE before traffic.",
        search_terms=["MTK attach", "UE Attach", "Start UE Attach With MTK", "Make_L3_Call_With_MTK_UE"],
        rationale="Attach establishes the UE state required for L3 traffic.",
    ),
    TemplateStep(
        role="start_dl_traffic",
        description="Start DL traffic with requested throughput.",
        search_terms=["Start Traffic For MTK UE", "Start Data Transfer DL", "L3 Call Data Transfer"],
        rationale="DL traffic should start before throughput validation.",
    ),
    TemplateStep(
        role="start_ul_traffic",
        description="Start UL traffic with requested throughput.",
        search_terms=["Start Traffic For MTK UE", "Start Data Transfer UL", "L3 Call Data Transfer"],
        rationale="UL traffic should start before throughput validation.",
    ),
    TemplateStep(
        role="check_tput",
        description="Collect and check DL/UL throughput.",
        search_terms=["Check L3 Call Tput", "Check Tput For CA Group", "Check Bi Tput", "Check peak throughput"],
        rationale="Throughput check validates that the L3 call reached the requested traffic target.",
    ),
    TemplateStep(
        role="stop_traffic",
        description="Stop DL/UL traffic before detach.",
        search_terms=["Stop Traffic For MTK UE", "Stop Data Transfer", "Stop Traffic"],
        rationale="Stopping traffic prevents leaking iperf processes into later cases.",
    ),
    TemplateStep(
        role="detach",
        description="Detach UE after traffic is stopped.",
        search_terms=["Detach Ue", "Stop Traffic And Detach", "power_ue.UE Detach"],
        rationale="Detach is required cleanup for UE state.",
    ),
    TemplateStep(
        role="teardown",
        description="Run feature-local teardown.",
        search_terms=["case teardown", "9198 case teardown", "8015 case teardown", "8247 case teardown"],
        rationale="Teardown restores environment and checks alarms/log cleanup.",
    ),
]


GENERIC_ROBOT_STEPS = [
    TemplateStep("documentation", "Write testcase documentation.", search_terms=["documentation"]),
    TemplateStep("tags", "Set target testline and profile tags.", search_terms=["tags"]),
    TemplateStep("setup", "Use allowed setup keyword.", search_terms=["setup"]),
    TemplateStep("body", "Add generated Robot steps.", search_terms=["keyword"]),
    TemplateStep("teardown", "Use allowed teardown keyword.", search_terms=["teardown"]),
]

