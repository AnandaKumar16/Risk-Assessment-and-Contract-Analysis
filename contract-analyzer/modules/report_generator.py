"""
Report Generator Module
Generates structured, export-ready contract analysis reports
"""

from typing import Dict, Any, List
from datetime import datetime
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ReportGenerator:
    """
    Generates comprehensive analysis reports in various formats.
    """
    
    DISCLAIMER = (
        "⚠️ DISCLAIMER: This analysis is for informational and analytical purposes only "
        "and does not constitute legal advice. All interpretations are based solely on "
        "the provided contract text. Please consult with a qualified legal professional "
        "before making any decisions based on this analysis."
    )
    
    def __init__(self):
        self.report_data = {}
    
    def generate_full_report(self, 
                            parsed_data: Dict[str, Any],
                            analysis_results: Dict[str, Any],
                            risk_assessment: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate complete analysis report combining all components.
        
        Args:
            parsed_data: Output from DocumentParser
            analysis_results: Output from ContractAnalyzer
            risk_assessment: Output from RiskScorer
        
        Returns:
            Complete report dictionary
        """
        # Pass language detection info to analysis results for clause analysis
        if 'language_detected' not in analysis_results:
            analysis_results['language_detected'] = parsed_data.get('language_detected', 'English')
        
        report = {
            'metadata': self._generate_metadata(parsed_data),
            'contract_overview': self._generate_overview(analysis_results),
            'contract_classification': self._generate_classification(analysis_results),
            'entities': self._generate_entities_section(analysis_results),
            'clause_analysis': self._generate_clause_analysis(analysis_results, risk_assessment),
            'risk_assessment': self._generate_risk_section(risk_assessment),
            'unfavorable_clauses': self._generate_unfavorable_section(risk_assessment),
            'renegotiation_guide': self._generate_renegotiation_guide(risk_assessment),
            'sme_summary': self._generate_sme_summary(analysis_results, risk_assessment),
            'disclaimer': self.DISCLAIMER
        }
        
        self.report_data = report
        return report
    
    def _generate_metadata(self, parsed_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate report metadata."""
        metadata = parsed_data.get('metadata', {})
        return {
            'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'document_name': metadata.get('filename', 'Unknown'),
            'document_format': metadata.get('format', 'Unknown'),
            'document_size': metadata.get('size_bytes', 0),
            'pages': metadata.get('pages', metadata.get('paragraphs', 'N/A'))
        }
    
    def _generate_overview(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate contract overview section."""
        summary = analysis_results.get('summary', {})
        
        return {
            'total_clauses': summary.get('total_clauses', 0),
            'total_obligations': summary.get('total_obligations', 0),
            'total_rights': summary.get('total_rights', 0),
            'total_prohibitions': summary.get('total_prohibitions', 0),
            'ambiguous_clauses': summary.get('ambiguous_clauses_count', 0),
            'risky_clauses': summary.get('risky_clauses_count', 0)
        }
    
    def _generate_classification(self, analysis_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate contract type classification."""
        contract_types = analysis_results.get('contract_types', [])
        
        classifications = []
        for contract_type, confidence in contract_types:
            classifications.append({
                'type': contract_type,
                'confidence': f"{int(confidence * 100)}%",
                'confidence_score': confidence
            })
        
        return classifications
    
    def _generate_entities_section(self, analysis_results: Dict[str, Any]) -> Dict[str, List[str]]:
        """Generate extracted entities section."""
        entities = analysis_results.get('entities', {})
        
        # Clean and format entities
        formatted_entities = {}
        for entity_type, entity_list in entities.items():
            if entity_list:
                formatted_entities[entity_type.title()] = entity_list[:10]  # Limit to top 10
        
        return formatted_entities
    
    def _generate_clause_analysis(self, 
                                  analysis_results: Dict[str, Any],
                                  risk_assessment: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate detailed clause-by-clause analysis."""
        clauses = analysis_results.get('clauses', [])
        clause_risks = risk_assessment.get('clause_risks', [])
        language_detected = analysis_results.get('language_detected', 'English')
        
        # Merge clause data with risk scores
        detailed_clauses = []
        
        for i, clause in enumerate(clauses):
            risk_data = clause_risks[i] if i < len(clause_risks) else {}
            
            clause_dict = {
                'number': clause.get('number', str(i + 1)),
                'heading': clause.get('heading', ''),
                'text': clause.get('text', ''),
                'plain_language_summary': self._generate_plain_summary(clause),
                'obligations': clause.get('obligations', []),
                'rights': clause.get('rights', []),
                'prohibitions': clause.get('prohibitions', []),
                'ambiguities': clause.get('ambiguities', []),
                'risk_score': risk_data.get('risk_score', 0),
                'risk_level': risk_data.get('risk_level', 'Low'),
                'risk_factors': risk_data.get('risk_factors', []),
                'impact_on_sme': self._assess_sme_impact(clause, risk_data),
                'language_detected': language_detected
            }
            detailed_clauses.append(clause_dict)
        
        return detailed_clauses
    
    def _generate_plain_summary(self, clause: Dict[str, Any]) -> str:
        """Generate plain language summary of a clause."""
        text = clause.get('text', '')
        obligations = clause.get('obligations', [])
        rights = clause.get('rights', [])
        
        # Simple heuristic summary
        summary_parts = []
        
        if obligations:
            summary_parts.append(f"This clause requires you to {len(obligations)} specific action(s).")
        
        if rights:
            summary_parts.append(f"You have {len(rights)} right(s) under this clause.")
        
        if not summary_parts:
            # Fallback: use first sentence
            sentences = text.split('.')
            if sentences:
                summary_parts.append(sentences[0].strip() + '.')
        
        return ' '.join(summary_parts) if summary_parts else "General contractual provision."
    
    def _assess_sme_impact(self, clause: Dict[str, Any], risk_data: Dict[str, Any]) -> str:
        """Assess how this clause impacts an SME."""
        risk_level = risk_data.get('risk_level', 'Low')
        risk_factors = risk_data.get('risk_factors', [])
        
        if risk_level == 'High':
            return (
                "⚠️ HIGH IMPACT: This clause poses significant risk to your business. "
                "It may result in financial liability, operational constraints, or loss of rights. "
                "Strongly recommend renegotiation or legal review."
            )
        elif risk_level == 'Medium':
            return (
                "⚡ MODERATE IMPACT: This clause has some risks or imbalances. "
                "Review carefully and consider requesting modifications for better protection."
            )
        else:
            return (
                "✓ LOW IMPACT: This clause appears relatively balanced and standard. "
                "Still review to ensure it aligns with your business needs."
            )
    
    def _generate_risk_section(self, risk_assessment: Dict[str, Any]) -> Dict[str, Any]:
        """Generate risk assessment summary."""
        return {
            'overall_score': risk_assessment.get('overall_risk_score', 0),
            'overall_level': risk_assessment.get('overall_risk_level', 'Unknown'),
            'statistics': risk_assessment.get('statistics', {}),
            'key_concerns': risk_assessment.get('key_concerns', [])[:10],
            'mitigation_strategies': risk_assessment.get('mitigation_strategies', [])
        }
    
    def _generate_unfavorable_section(self, risk_assessment: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate section highlighting unfavorable clauses."""
        unfavorable = risk_assessment.get('unfavorable_clauses', [])
        
        # Sort by risk score (highest first)
        sorted_unfavorable = sorted(
            unfavorable,
            key=lambda x: x.get('risk_score', 0),
            reverse=True
        )
        
        highlighted = []
        for clause in sorted_unfavorable:
            highlighted.append({
                'clause_number': clause.get('clause_number', 'N/A'),
                'clause_heading': clause.get('clause_heading', 'Untitled'),
                'risk_score': clause.get('risk_score', 0),
                'risk_level': clause.get('risk_level', 'Unknown'),
                'why_unfavorable': ', '.join(clause.get('risk_factors', [])),
                'recommendations': clause.get('recommendations', [])
            })
        
        return highlighted
    
    def _generate_renegotiation_guide(self, risk_assessment: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate renegotiation guidance."""
        unfavorable = risk_assessment.get('unfavorable_clauses', [])
        
        renegotiation_items = []
        
        for clause in unfavorable:
            if clause.get('risk_score', 0) >= 30:  # Medium or high risk
                renegotiation_items.append({
                    'clause_reference': f"Clause {clause.get('clause_number', 'N/A')}",
                    'issue': clause.get('clause_heading', 'Untitled'),
                    'current_problems': clause.get('risk_factors', []),
                    'suggested_alternatives': clause.get('recommendations', []),
                    'priority': 'HIGH' if clause.get('risk_score', 0) >= 60 else 'MEDIUM'
                })
        
        # Sort by priority
        renegotiation_items.sort(key=lambda x: x['priority'], reverse=True)
        
        return renegotiation_items
    
    def _generate_sme_summary(self, 
                             analysis_results: Dict[str, Any],
                             risk_assessment: Dict[str, Any]) -> Dict[str, Any]:
        """Generate SME-friendly executive summary."""
        contract_types = analysis_results.get('contract_types', [])
        primary_type = contract_types[0][0] if contract_types else "Unknown Contract Type"
        
        overall_risk = risk_assessment.get('overall_risk_level', 'Unknown')
        stats = risk_assessment.get('statistics', {})
        
        # Generate business-friendly summary
        summary_text = self._create_business_summary(
            primary_type,
            overall_risk,
            stats,
            risk_assessment.get('key_concerns', [])
        )
        
        # Key takeaways
        takeaways = self._generate_key_takeaways(risk_assessment)
        
        # Action items
        action_items = self._generate_action_items(risk_assessment)
        
        return {
            'contract_type': primary_type,
            'overall_risk': overall_risk,
            'summary': summary_text,
            'key_takeaways': takeaways,
            'recommended_actions': action_items
        }
    
    def _create_business_summary(self, 
                                contract_type: str,
                                risk_level: str,
                                stats: Dict[str, Any],
                                concerns: List[str]) -> str:
        """Create business-friendly summary text."""
        total_clauses = stats.get('total_clauses', 0)
        high_risk = stats.get('high_risk_clauses', 0)
        medium_risk = stats.get('medium_risk_clauses', 0)
        
        summary = f"This appears to be a {contract_type} with {total_clauses} main clauses. "
        
        if risk_level == 'High':
            summary += (
                f"⚠️ WARNING: This contract carries HIGH RISK for your business. "
                f"We identified {high_risk} high-risk and {medium_risk} medium-risk clauses "
                f"that could expose you to significant liabilities or unfavorable terms. "
                f"We strongly recommend legal review before signing."
            )
        elif risk_level == 'Medium':
            summary += (
                f"⚡ CAUTION: This contract has MEDIUM RISK. "
                f"There are {medium_risk} clauses that need attention and possibly renegotiation. "
                f"Review the highlighted issues carefully."
            )
        else:
            summary += (
                f"✓ This contract appears relatively balanced with LOW overall risk. "
                f"However, always review all terms to ensure they meet your business needs."
            )
        
        return summary
    
    def _generate_key_takeaways(self, risk_assessment: Dict[str, Any]) -> List[str]:
        """Generate key business takeaways."""
        takeaways = []
        
        concerns = risk_assessment.get('key_concerns', [])[:5]
        stats = risk_assessment.get('statistics', {})
        
        # Risk distribution
        high_risk = stats.get('high_risk_clauses', 0)
        medium_risk = stats.get('medium_risk_clauses', 0)
        
        if high_risk > 0:
            takeaways.append(
                f"🔴 {high_risk} clause(s) pose serious risk - immediate attention required"
            )
        
        if medium_risk > 0:
            takeaways.append(
                f"🟡 {medium_risk} clause(s) have moderate concerns - review recommended"
            )
        
        # Specific concerns
        for concern in concerns[:3]:
            takeaways.append(f"• {concern}")
        
        return takeaways
    
    def _generate_action_items(self, risk_assessment: Dict[str, Any]) -> List[str]:
        """Generate recommended action items for SME."""
        actions = []
        
        unfavorable = risk_assessment.get('unfavorable_clauses', [])
        high_risk_clauses = [c for c in unfavorable if c.get('risk_score', 0) >= 60]
        
        if high_risk_clauses:
            actions.append(
                f"1. URGENT: Renegotiate {len(high_risk_clauses)} high-risk clause(s) before signing"
            )
            actions.append("2. Consult with a lawyer specializing in contract law")
        
        actions.append("3. Request written clarification for all ambiguous terms")
        actions.append("4. Negotiate liability caps and payment terms that suit your cash flow")
        actions.append("5. Ensure you have adequate insurance coverage for contractual liabilities")
        actions.append("6. Document all verbal agreements as written amendments")
        actions.append("7. Set up internal reminders for key dates (renewal, termination notice, etc.)")
        
        return actions[:7]  # Limit to 7 actions
    
    def export_to_markdown(self) -> str:
        """Export report to markdown format."""
        if not self.report_data:
            return "No report data available"
        
        md = []
        
        # Title
        md.append("# Contract Analysis Report")
        md.append("")
        
        # Metadata
        metadata = self.report_data.get('metadata', {})
        md.append("## Document Information")
        md.append(f"- **Analysis Date:** {metadata.get('analysis_date', 'N/A')}")
        md.append(f"- **Document:** {metadata.get('document_name', 'N/A')}")
        md.append(f"- **Format:** {metadata.get('document_format', 'N/A')}")
        md.append("")
        
        # SME Summary
        sme_summary = self.report_data.get('sme_summary', {})
        md.append("## Executive Summary for Business Owners")
        md.append("")
        md.append(f"**Contract Type:** {sme_summary.get('contract_type', 'Unknown')}")
        md.append(f"**Overall Risk Level:** {sme_summary.get('overall_risk', 'Unknown')}")
        md.append("")
        md.append(sme_summary.get('summary', ''))
        md.append("")
        
        # Key Takeaways
        md.append("### Key Takeaways")
        for takeaway in sme_summary.get('key_takeaways', []):
            md.append(f"- {takeaway}")
        md.append("")
        
        # Recommended Actions
        md.append("### Recommended Actions")
        for action in sme_summary.get('recommended_actions', []):
            md.append(f"{action}")
        md.append("")
        
        # Contract Classification
        classification = self.report_data.get('contract_classification', [])
        if classification:
            md.append("## Contract Type Classification")
            for item in classification:
                md.append(f"- **{item['type']}** - Confidence: {item['confidence']}")
            md.append("")
        
        # Risk Assessment
        risk = self.report_data.get('risk_assessment', {})
        md.append("## Overall Risk Assessment")
        md.append(f"- **Risk Score:** {risk.get('overall_score', 0)}/100")
        md.append(f"- **Risk Level:** {risk.get('overall_level', 'Unknown')}")
        md.append("")
        
        stats = risk.get('statistics', {})
        md.append("### Risk Distribution")
        md.append(f"- High Risk Clauses: {stats.get('high_risk_clauses', 0)}")
        md.append(f"- Medium Risk Clauses: {stats.get('medium_risk_clauses', 0)}")
        md.append(f"- Low Risk Clauses: {stats.get('low_risk_clauses', 0)}")
        md.append("")
        
        # Key Concerns
        md.append("### Top Concerns")
        for concern in risk.get('key_concerns', [])[:5]:
            md.append(f"- {concern}")
        md.append("")
        
        # Unfavorable Clauses
        unfavorable = self.report_data.get('unfavorable_clauses', [])
        if unfavorable:
            md.append("## Unfavorable Clauses Requiring Attention")
            md.append("")
            for clause in unfavorable:
                md.append(f"### Clause {clause.get('clause_number', 'N/A')}: {clause.get('clause_heading', 'Untitled')}")
                md.append(f"**Risk Level:** {clause.get('risk_level', 'Unknown')} ({clause.get('risk_score', 0)}/100)")
                md.append("")
                md.append(f"**Why This Is Unfavorable:**")
                md.append(clause.get('why_unfavorable', 'N/A'))
                md.append("")
                md.append(f"**Recommendations:**")
                for rec in clause.get('recommendations', []):
                    md.append(f"- {rec}")
                md.append("")
        
        # Renegotiation Guide
        renego = self.report_data.get('renegotiation_guide', [])
        if renego:
            md.append("## Renegotiation Guide")
            md.append("")
            for item in renego:
                md.append(f"### {item.get('clause_reference', 'N/A')} - Priority: {item.get('priority', 'N/A')}")
                md.append(f"**Issue:** {item.get('issue', 'N/A')}")
                md.append("")
                md.append("**Current Problems:**")
                for problem in item.get('current_problems', []):
                    md.append(f"- {problem}")
                md.append("")
                md.append("**Suggested Alternatives:**")
                for alt in item.get('suggested_alternatives', []):
                    md.append(f"- {alt}")
                md.append("")
        
        # Disclaimer
        md.append("---")
        md.append("")
        md.append(f"## {self.DISCLAIMER}")
        md.append("")
        
        return '\n'.join(md)
    
    def export_to_json(self) -> str:
        """Export report to JSON format."""
        return json.dumps(self.report_data, indent=2, ensure_ascii=False)
