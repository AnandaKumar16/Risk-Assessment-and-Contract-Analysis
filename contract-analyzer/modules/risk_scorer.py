"""
Risk Scoring Module
Assigns risk scores to individual clauses and overall contract
Identifies unfavorable terms for SMEs
"""

from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class RiskScore:
    """Risk score for a clause or contract."""
    score: float  # 0-100
    level: str  # 'Low', 'Medium', 'High'
    factors: List[str]  # Contributing risk factors
    recommendations: List[str]  # Mitigation recommendations


class RiskScorer:
    """
    Evaluates risk levels in contract clauses.
    """
    
    # Risk weights for different factors
    RISK_WEIGHTS = {
        'financial_penalty': 25,
        'unlimited_liability': 30,
        'unilateral_termination': 20,
        'ip_transfer': 20,
        'non_compete': 15,
        'lock_in': 15,
        'auto_renewal': 10,
        'ambiguous_terms': 10,
        'missing_safeguards': 15,
        'one_sided_obligation': 12,
        'jurisdiction_disadvantage': 10,
        'indemnity_broad': 20,
        'no_liability_cap': 25,
        'immediate_termination': 15,
        'confidentiality_overly_broad': 12
    }
    
    # SME-unfavorable patterns
    UNFAVORABLE_PATTERNS = {
        'unlimited': ['unlimited liability', 'unlimited damages', 'unlimited indemnification'],
        'unilateral': ['unilateral', 'sole discretion', 'at will', 'without cause'],
        'penalties': ['penalty', 'liquidated damages', 'forfeit', 'fine'],
        'no_cap': ['without limit', 'no cap', 'not limited to'],
        'immediate': ['immediate termination', 'terminate immediately', 'forthwith'],
        'irrevocable': ['irrevocable', 'unconditional', 'non-refundable'],
        'perpetual': ['perpetual', 'indefinite', 'in perpetuity'],
        'waiver': ['waive', 'surrender', 'relinquish all'],
        'exclusive': ['exclusive rights', 'sole ownership', 'complete transfer']
    }
    
    # Balanced alternatives for unfavorable clauses
    RENEGOTIATION_SUGGESTIONS = {
        'unlimited_liability': {
            'alternative': 'Liability shall be capped at [X amount or percentage of contract value]',
            'explanation': 'Limits financial exposure to a predictable amount'
        },
        'unilateral_termination': {
            'alternative': 'Either party may terminate with [X days] written notice for convenience, or immediately for material breach with opportunity to cure',
            'explanation': 'Provides mutual rights and reasonable notice period'
        },
        'penalty_clause': {
            'alternative': 'Liquidated damages shall not exceed [X%] of contract value and shall be the exclusive remedy',
            'explanation': 'Sets reasonable cap and prevents multiple penalties'
        },
        'broad_indemnity': {
            'alternative': 'Each party shall indemnify the other only for claims arising from their own negligence or willful misconduct',
            'explanation': 'Limits indemnity to party\'s own actions'
        },
        'auto_renewal': {
            'alternative': 'Contract renews automatically unless either party provides [X days] written notice of non-renewal',
            'explanation': 'Allows easy exit with reasonable notice'
        },
        'ip_transfer': {
            'alternative': 'Client receives a perpetual, non-exclusive license to use deliverables; provider retains IP rights',
            'explanation': 'Balances usage rights without full IP transfer'
        },
        'non_compete_broad': {
            'alternative': 'Non-compete limited to [specific geography] for [reasonable duration] and only for direct competing services',
            'explanation': 'Narrows scope to reasonable competitive protection'
        },
        'ambiguous_timeline': {
            'alternative': 'Specify exact number of days/months instead of "reasonable time" or "promptly"',
            'explanation': 'Creates clear, measurable deadlines'
        },
        'no_cure_period': {
            'alternative': 'Add: "provided that the non-breaching party has given written notice and [X days] to cure"',
            'explanation': 'Allows opportunity to fix issues before termination'
        },
        'one_sided_confidentiality': {
            'alternative': 'Make confidentiality obligations mutual and reciprocal',
            'explanation': 'Protects both parties equally'
        }
    }
    
    def score_clause(self, clause_data: Dict[str, Any]) -> RiskScore:
        """
        Calculate risk score for a single clause.
        
        Args:
            clause_data: Dictionary with clause information from analyzer
        
        Returns:
            RiskScore object
        """
        risk_points = 0
        risk_factors = []
        
        text_lower = clause_data.get('text', '').lower()
        risk_indicators = clause_data.get('risk_indicators', [])
        ambiguities = clause_data.get('ambiguities', [])
        obligations = clause_data.get('obligations', [])
        rights = clause_data.get('rights', [])
        prohibitions = clause_data.get('prohibitions', [])
        
        # 1. Check for risk indicators from analyzer
        for indicator in risk_indicators:
            if 'FINANCIAL' in indicator:
                risk_points += self.RISK_WEIGHTS.get('financial_penalty', 10)
                risk_factors.append(f"Financial risk: {indicator}")
            elif 'TERMINATION' in indicator:
                risk_points += self.RISK_WEIGHTS.get('unilateral_termination', 15)
                risk_factors.append(f"Termination risk: {indicator}")
            elif 'IP' in indicator:
                risk_points += self.RISK_WEIGHTS.get('ip_transfer', 15)
                risk_factors.append(f"IP risk: {indicator}")
            elif 'NON-COMPETE' in indicator:
                risk_points += self.RISK_WEIGHTS.get('non_compete', 12)
                risk_factors.append(f"Non-compete risk: {indicator}")
            elif 'LOCK-IN' in indicator:
                risk_points += self.RISK_WEIGHTS.get('lock_in', 10)
                risk_factors.append(f"Lock-in risk: {indicator}")
        
        # 2. Check for unfavorable patterns
        for pattern_type, patterns in self.UNFAVORABLE_PATTERNS.items():
            for pattern in patterns:
                if pattern in text_lower:
                    weight = 15  # default
                    if pattern_type == 'unlimited':
                        weight = self.RISK_WEIGHTS.get('unlimited_liability', 30)
                    elif pattern_type == 'unilateral':
                        weight = self.RISK_WEIGHTS.get('unilateral_termination', 20)
                    elif pattern_type == 'penalties':
                        weight = self.RISK_WEIGHTS.get('financial_penalty', 25)
                    
                    risk_points += weight
                    risk_factors.append(f"Unfavorable term: '{pattern}'")
        
        # 3. Check for ambiguities
        if ambiguities:
            risk_points += len(ambiguities) * self.RISK_WEIGHTS.get('ambiguous_terms', 10)
            risk_factors.append(f"Contains {len(ambiguities)} ambiguous term(s)")
        
        # 4. Check obligation balance
        obligation_count = len(obligations)
        rights_count = len(rights)
        
        if obligation_count > 0 and rights_count == 0:
            risk_points += self.RISK_WEIGHTS.get('one_sided_obligation', 12)
            risk_factors.append("One-sided obligations (no rights for SME)")
        elif obligation_count > rights_count * 2:
            risk_points += 8
            risk_factors.append("Imbalanced obligations vs rights")
        
        # 5. Check for missing safeguards
        if obligation_count > 0:
            # Check if there's a cure period mentioned
            if 'cure' not in text_lower and 'remedy' not in text_lower:
                if any(term in text_lower for term in ['breach', 'violation', 'default']):
                    risk_points += self.RISK_WEIGHTS.get('missing_safeguards', 15)
                    risk_factors.append("No cure period for breach")
        
        # 6. Check for liability caps
        if 'liability' in text_lower or 'indemnify' in text_lower:
            has_cap = any(term in text_lower for term in ['limited to', 'capped at', 'maximum of', 'not exceed'])
            if not has_cap:
                risk_points += self.RISK_WEIGHTS.get('no_liability_cap', 25)
                risk_factors.append("No cap on liability/indemnification")
        
        # Normalize score to 0-100
        risk_score = min(risk_points, 100)
        
        # Determine risk level
        if risk_score >= 60:
            risk_level = "High"
        elif risk_score >= 30:
            risk_level = "Medium"
        else:
            risk_level = "Low"
        
        # Generate recommendations
        recommendations = self._generate_recommendations(risk_factors, clause_data)
        
        return RiskScore(
            score=round(risk_score, 1),
            level=risk_level,
            factors=risk_factors,
            recommendations=recommendations
        )
    
    def score_contract(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate overall contract risk score and identify unfavorable clauses.
        
        Args:
            analysis_results: Complete analysis from ContractAnalyzer
        
        Returns:
            Dictionary with contract-level risk assessment
        """
        clauses = analysis_results.get('clauses', [])
        
        if not clauses:
            return {
                'overall_risk_score': 0,
                'overall_risk_level': 'Unknown',
                'clause_risks': [],
                'unfavorable_clauses': [],
                'key_concerns': [],
                'mitigation_strategies': []
            }
        
        # Score each clause
        clause_risks = []
        for clause in clauses:
            risk = self.score_clause(clause)
            clause_risks.append({
                'clause_number': clause.get('number'),
                'clause_heading': clause.get('heading'),
                'risk_score': risk.score,
                'risk_level': risk.level,
                'risk_factors': risk.factors,
                'recommendations': risk.recommendations
            })
        
        # Calculate overall risk (weighted average, emphasizing high-risk clauses)
        risk_scores = [cr['risk_score'] for cr in clause_risks]
        
        # Weight high-risk clauses more heavily
        weighted_scores = []
        for score in risk_scores:
            if score >= 60:
                weighted_scores.extend([score] * 3)  # Count high-risk clauses 3x
            elif score >= 30:
                weighted_scores.extend([score] * 2)  # Count medium-risk clauses 2x
            else:
                weighted_scores.append(score)
        
        overall_risk_score = round(sum(weighted_scores) / len(weighted_scores), 1) if weighted_scores else 0
        
        # Determine overall risk level
        if overall_risk_score >= 60:
            overall_risk_level = "High"
        elif overall_risk_score >= 30:
            overall_risk_level = "Medium"
        else:
            overall_risk_level = "Low"
        
        # Identify unfavorable clauses (medium or high risk)
        unfavorable_clauses = [
            cr for cr in clause_risks if cr['risk_score'] >= 30
        ]
        
        # Extract key concerns
        all_factors = []
        for cr in clause_risks:
            all_factors.extend(cr['risk_factors'])
        
        # Count and rank concerns
        concern_counts = {}
        for factor in all_factors:
            concern_counts[factor] = concern_counts.get(factor, 0) + 1
        
        key_concerns = sorted(
            [(concern, count) for concern, count in concern_counts.items()],
            key=lambda x: x[1],
            reverse=True
        )[:10]  # Top 10 concerns
        
        # Generate contract-level mitigation strategies
        mitigation_strategies = self._generate_contract_mitigation(clause_risks, key_concerns)
        
        return {
            'overall_risk_score': overall_risk_score,
            'overall_risk_level': overall_risk_level,
            'clause_risks': clause_risks,
            'unfavorable_clauses': unfavorable_clauses,
            'key_concerns': [c[0] for c in key_concerns],
            'mitigation_strategies': mitigation_strategies,
            'statistics': {
                'total_clauses': len(clause_risks),
                'high_risk_clauses': sum(1 for cr in clause_risks if cr['risk_score'] >= 60),
                'medium_risk_clauses': sum(1 for cr in clause_risks if 30 <= cr['risk_score'] < 60),
                'low_risk_clauses': sum(1 for cr in clause_risks if cr['risk_score'] < 30)
            }
        }
    
    def _generate_recommendations(self, risk_factors: List[str], clause_data: Dict[str, Any]) -> List[str]:
        """Generate specific recommendations for a clause based on identified risks."""
        recommendations = []
        text_lower = clause_data.get('text', '').lower()
        
        # Match risk factors to renegotiation suggestions
        for factor in risk_factors:
            if 'unlimited liability' in factor.lower() or 'no cap on liability' in factor.lower():
                sugg = self.RENEGOTIATION_SUGGESTIONS['unlimited_liability']
                recommendations.append(f"{sugg['alternative']} - {sugg['explanation']}")
            
            elif 'unilateral' in factor.lower() or 'termination risk' in factor.lower():
                sugg = self.RENEGOTIATION_SUGGESTIONS['unilateral_termination']
                recommendations.append(f"{sugg['alternative']} - {sugg['explanation']}")
            
            elif 'financial risk' in factor.lower() or 'penalty' in factor.lower():
                sugg = self.RENEGOTIATION_SUGGESTIONS['penalty_clause']
                recommendations.append(f"{sugg['alternative']} - {sugg['explanation']}")
            
            elif 'ip' in factor.lower():
                sugg = self.RENEGOTIATION_SUGGESTIONS['ip_transfer']
                recommendations.append(f"{sugg['alternative']} - {sugg['explanation']}")
            
            elif 'non-compete' in factor.lower():
                sugg = self.RENEGOTIATION_SUGGESTIONS['non_compete_broad']
                recommendations.append(f"{sugg['alternative']} - {sugg['explanation']}")
            
            elif 'lock-in' in factor.lower() or 'auto-renewal' in factor.lower():
                sugg = self.RENEGOTIATION_SUGGESTIONS['auto_renewal']
                recommendations.append(f"{sugg['alternative']} - {sugg['explanation']}")
            
            elif 'ambiguous' in factor.lower():
                sugg = self.RENEGOTIATION_SUGGESTIONS['ambiguous_timeline']
                recommendations.append(f"{sugg['alternative']} - {sugg['explanation']}")
            
            elif 'one-sided' in factor.lower():
                recommendations.append("Request reciprocal obligations or balanced rights")
            
            elif 'no cure period' in factor.lower():
                sugg = self.RENEGOTIATION_SUGGESTIONS['no_cure_period']
                recommendations.append(f"{sugg['alternative']} - {sugg['explanation']}")
        
        # Add general recommendation if clause is high risk
        if not recommendations:
            recommendations.append("Review this clause with legal counsel before signing")
        
        return list(set(recommendations))  # Remove duplicates
    
    def _generate_contract_mitigation(self, clause_risks: List[Dict], 
                                      key_concerns: List[Tuple[str, int]]) -> List[str]:
        """Generate contract-level mitigation strategies."""
        strategies = []
        
        # Count high and medium risk clauses
        high_risk_count = sum(1 for cr in clause_risks if cr['risk_score'] >= 60)
        medium_risk_count = sum(1 for cr in clause_risks if 30 <= cr['risk_score'] < 60)
        
        if high_risk_count > 0:
            strategies.append(
                f"PRIORITY: Renegotiate {high_risk_count} high-risk clause(s) before signing. "
                "These pose significant financial or operational risks to your business."
            )
        
        if medium_risk_count > 3:
            strategies.append(
                f"Request modifications to {medium_risk_count} medium-risk clauses to balance obligations."
            )
        
        # Specific strategies based on common concerns
        concern_texts = [c[0].lower() for c in key_concerns[:5]]
        
        if any('liability' in c for c in concern_texts):
            strategies.append(
                "Negotiate liability caps and obtain adequate insurance coverage. "
                "Consider limiting liability to contract value or a specific amount."
            )
        
        if any('termination' in c for c in concern_texts):
            strategies.append(
                "Request mutual termination rights with reasonable notice periods. "
                "Ensure you have exit options if business conditions change."
            )
        
        if any('ambiguous' in c for c in concern_texts):
            strategies.append(
                "Request clarification of all ambiguous terms in writing. "
                "Define 'reasonable', 'promptly', and other subjective terms with specific timeframes."
            )
        
        if any('penalty' in c or 'financial' in c for c in concern_texts):
            strategies.append(
                "Negotiate caps on penalties and liquidated damages. "
                "Ensure payment terms are realistic for your cash flow."
            )
        
        # General SME protection strategies
        strategies.append(
            "Consult with a legal professional before signing, especially for high-value or long-term contracts."
        )
        
        strategies.append(
            "Document all verbal promises and clarifications in writing as amendments to the contract."
        )
        
        return strategies
