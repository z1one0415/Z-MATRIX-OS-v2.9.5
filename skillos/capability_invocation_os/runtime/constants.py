"""Runtime action constants and forbidden module names."""
DENY = "DENY"
DENY_NOOP = "DENY_NOOP"
CONTINUE = "CONTINUE"
DEGRADE_DOCS_ONLY = "DEGRADE_DOCS_ONLY"
DEGRADE_MANUAL_REVIEW = "DEGRADE_MANUAL_REVIEW"
NEEDS_HUMAN_REVIEW = "NEEDS_HUMAN_REVIEW"
FORBIDDEN_MODULES = {"z2","z8","z9","v3","worldblocks","dealcompass","broker","real_trade","production","order","trading"}
CAPABILITY_TAGS = {"execution","call","invoke","adapter","run"}
