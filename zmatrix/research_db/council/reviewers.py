"""Batch-D: 12-Seat Research Council — structured, independent reviewers."""
from .base_reviewer import ReviewContext, ReviewResult, BaseReviewer, ReviewVerdict
from dataclasses import dataclass

def _check_verdict(score, min_pass=0.6, min_cond=0.4): 
    return ReviewVerdict.PASS.value if score>=min_pass else (ReviewVerdict.CONDITIONAL_PASS.value if score>=min_cond else ReviewVerdict.FAIL.value)

def _data_review(ctx): 
    s=0.7 if ctx.metrics.get("coverage",0)>=0.5 else 0.3; return ReviewResult(reviewer_id="R01",reviewer_name="Data",verdict=_check_verdict(s),score=s)
def _factor_review(ctx): 
    ic=ctx.metrics.get("ic",0); s=0.8 if abs(ic)>=0.03 else (0.5 if abs(ic)>=0.01 else 0.2); return ReviewResult(reviewer_id="R02",reviewer_name="Factor",verdict=_check_verdict(s),score=s)
def _attribution_review(ctx): 
    a=ctx.attribution.get("selection_alpha",0); s=0.7 if a>0.01 else (0.5 if a>-0.01 else 0.3); return ReviewResult(reviewer_id="R03",reviewer_name="Attribution",verdict=_check_verdict(s),score=s)
def _replay_review(ctx): 
    s=0.9 if ctx.replay_hash else 0.2; return ReviewResult(reviewer_id="R04",reviewer_name="Replay",verdict=_check_verdict(s),score=s)
def _risk_review(ctx): 
    f=len(ctx.risk_flags); s=0.8 if f==0 else (0.5 if f<=2 else 0.2); return ReviewResult(reviewer_id="R05",reviewer_name="Risk",verdict=_check_verdict(s),score=s,concerns=ctx.risk_flags)
def _sector_review(ctx): 
    s=0.6; return ReviewResult(reviewer_id="R06",reviewer_name="Sector",verdict=_check_verdict(s),score=s)
def _industry_review(ctx): 
    s=0.6; return ReviewResult(reviewer_id="R07",reviewer_name="Industry",verdict=_check_verdict(s),score=s)
def _catalyst_review(ctx): 
    s=0.5; return ReviewResult(reviewer_id="R08",reviewer_name="Catalyst",verdict=_check_verdict(s),score=s)
def _execution_review(ctx): 
    s=0.7; return ReviewResult(reviewer_id="R09",reviewer_name="Execution",verdict=_check_verdict(s),score=s)
def _portfolio_review(ctx): 
    s=0.6; return ReviewResult(reviewer_id="R10",reviewer_name="Portfolio",verdict=_check_verdict(s),score=s)
def _governance_review(ctx): 
    s=0.8 if not ctx.risk_flags else 0.4; return ReviewResult(reviewer_id="R11",reviewer_name="Governance",verdict=_check_verdict(s),score=s,concerns=ctx.risk_flags)
def _devil_review(ctx): 
    c=[]; s=0.3
    if abs(ctx.metrics.get("ic",0))<0.02: c.append("Low IC → possible noise"); s=0.2
    if ctx.metrics.get("coverage",1)<0.5: c.append("Low coverage → survivorship bias risk")
    return ReviewResult(reviewer_id="R12",reviewer_name="Devil",verdict=_check_verdict(s),score=s,concerns=c,minority_note="Always question the thesis")

DATA_REVIEWER=BaseReviewer("R01","Data",_data_review)
FACTOR_REVIEWER=BaseReviewer("R02","Factor",_factor_review)
ATTRIBUTION_REVIEWER=BaseReviewer("R03","Attribution",_attribution_review)
REPLAY_REVIEWER=BaseReviewer("R04","Replay",_replay_review)
RISK_REVIEWER=BaseReviewer("R05","Risk",_risk_review)
SECTOR_REVIEWER=BaseReviewer("R06","Sector",_sector_review)
INDUSTRY_REVIEWER=BaseReviewer("R07","Industry",_industry_review)
CATALYST_REVIEWER=BaseReviewer("R08","Catalyst",_catalyst_review)
EXECUTION_REVIEWER=BaseReviewer("R09","Execution",_execution_review)
PORTFOLIO_REVIEWER=BaseReviewer("R10","Portfolio",_portfolio_review)
GOVERNANCE_REVIEWER=BaseReviewer("R11","Governance",_governance_review)
DEVIL_REVIEWER=BaseReviewer("R12","Devil",_devil_review)
ALL_REVIEWERS=[DATA_REVIEWER,FACTOR_REVIEWER,ATTRIBUTION_REVIEWER,REPLAY_REVIEWER,RISK_REVIEWER,SECTOR_REVIEWER,INDUSTRY_REVIEWER,CATALYST_REVIEWER,EXECUTION_REVIEWER,PORTFOLIO_REVIEWER,GOVERNANCE_REVIEWER,DEVIL_REVIEWER]
