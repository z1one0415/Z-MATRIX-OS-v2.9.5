"""R3: Workflow Template — standard research workflow definition."""
DEFAULT_TEMPLATE = {"name":"Standard Research Workflow","stages":["IDEA","RESEARCH","VALIDATION","COUNCIL","APPROVED","MONITOR","RETIRED"],
    "required_stages":["RESEARCH","VALIDATION","COUNCIL"],"skippable_stages":["MONITOR"],
    "production_allowed": False}

class WorkflowTemplate:
    @staticmethod
    def get_template(template_id: str = "DEFAULT") -> dict: return DEFAULT_TEMPLATE if template_id=="DEFAULT" else {}
    @staticmethod
    def validate_stage_order(stages: list[str]) -> bool: return stages == DEFAULT_TEMPLATE["stages"] or all(s in DEFAULT_TEMPLATE["stages"] for s in stages)
