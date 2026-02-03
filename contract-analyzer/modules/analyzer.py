"""
Contract Analyzer Module
Performs NLP-based analysis on contract text:
- Clause extraction
- Named Entity Recognition (NER)
- Obligation/Right/Prohibition detection
- Ambiguity detection
- Contract type classification
"""

import re
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class Clause:
    """Represents a contract clause."""
    number: str
    heading: str
    text: str
    obligations: List[str] = field(default_factory=list)
    rights: List[str] = field(default_factory=list)
    prohibitions: List[str] = field(default_factory=list)
    entities: Dict[str, List[str]] = field(default_factory=dict)
    ambiguities: List[str] = field(default_factory=list)
    risk_indicators: List[str] = field(default_factory=list)


class ContractAnalyzer:
    """
    Analyzes contract text using NLP techniques.
    """
    
    # Contract type keywords
    CONTRACT_TYPES = {
        'Employment Agreement': [
            'employee', 'employer', 'employment', 'salary', 'wage', 'probation',
            'termination of employment', 'working hours', 'leave', 'benefits'
        ],
        'Vendor / Supplier Contract': [
            'vendor', 'supplier', 'supply', 'purchase order', 'delivery', 'goods',
            'procurement', 'invoice', 'payment terms'
        ],
        'Service Agreement': [
            'service provider', 'client', 'services', 'scope of work', 'deliverables',
            'service level', 'sla', 'milestone'
        ],
        'Lease / Rental Agreement': [
            'landlord', 'tenant', 'lease', 'rent', 'premises', 'property',
            'security deposit', 'tenancy', 'eviction'
        ],
        'Partnership Deed': [
            'partner', 'partnership', 'firm', 'profit sharing', 'capital contribution',
            'partnership business', 'dissolution'
        ],
        'Licensing Agreement': [
            'licensor', 'licensee', 'license', 'intellectual property', 'royalty',
            'licensed product', 'grant of license'
        ],
        'NDA / Confidentiality Agreement': [
            'confidential information', 'disclosing party', 'receiving party',
            'non-disclosure', 'proprietary', 'trade secret'
        ]
    }
    
    # Obligation indicators
    OBLIGATION_KEYWORDS = [
        'shall', 'must', 'will', 'required to', 'obligated to', 'agrees to',
        'undertakes to', 'responsible for', 'bound to', 'covenant to'
    ]
    
    # Rights indicators
    RIGHTS_KEYWORDS = [
        'may', 'entitled to', 'has the right to', 'permitted to', 'allowed to',
        'can', 'authorized to', 'discretion to'
    ]
    
    # Prohibition indicators
    PROHIBITION_KEYWORDS = [
        'shall not', 'must not', 'will not', 'prohibited from', 'restricted from',
        'may not', 'cannot', 'forbidden to', 'barred from'
    ]
    
    # Ambiguous terms
    AMBIGUOUS_TERMS = [
        'reasonable', 'appropriate', 'sufficient', 'necessary', 'material',
        'substantial', 'significant', 'promptly', 'as soon as possible',
        'best efforts', 'good faith', 'satisfactory', 'adequate'
    ]
    
    # Risk indicator terms
    RISK_INDICATORS = {
        'financial': [
            'penalty', 'liquidated damages', 'unlimited liability', 'indemnify',
            'forfeit', 'fine', 'damages', 'compensation'
        ],
        'termination': [
            'unilateral termination', 'immediate termination', 'terminate at will',
            'without cause', 'sole discretion'
        ],
        'lock-in': [
            'lock-in period', 'minimum term', 'auto-renewal', 'evergreen',
            'binding for', 'irrevocable'
        ],
        'ip': [
            'transfer of ip', 'assignment of rights', 'waive all rights',
            'exclusive ownership', 'surrender'
        ],
        'non-compete': [
            'non-compete', 'non-solicitation', 'restraint of trade',
            'covenant not to compete'
        ]
    }
    
    def __init__(self):
        self.clauses: List[Clause] = []
    
    def analyze_contract(self, text: str) -> Dict[str, Any]:
        """
        Perform comprehensive contract analysis.
        
        Args:
            text: Contract text to analyze
        
        Returns:
            Dictionary containing all analysis results
        """
        if not text or len(text.strip()) < 50:
            return {
                'error': 'Contract text is too short or empty for analysis',
                'contract_types': [],
                'clauses': [],
                'entities': {},
                'summary': {}
            }
        
        # Extract clauses
        self.clauses = self._extract_clauses(text)
        
        # Analyze each clause
        for clause in self.clauses:
            self._analyze_clause(clause)
        
        # Extract global entities
        global_entities = self._extract_entities(text)
        
        # Classify contract type
        contract_types = self._classify_contract_type(text)
        
        # Generate summary statistics
        summary = self._generate_summary()
        
        return {
            'contract_types': contract_types,
            'clauses': [self._clause_to_dict(c) for c in self.clauses],
            'entities': global_entities,
            'summary': summary,
            'error': None
        }
    
    def _extract_clauses(self, text: str) -> List[Clause]:
        """
        Extract clauses and sub-clauses from contract text.
        Attempts to preserve numbering and structure.
        """
        clauses = []
        
        # Split by common clause patterns
        # Pattern 1: Numbered clauses (1., 1.1, 1.1.1, etc.)
        # Pattern 2: Lettered clauses (a), (i), etc.
        # Pattern 3: Headings in CAPS or Title Case
        
        # Split into paragraphs first
        paragraphs = text.split('\n\n')
        
        current_clause_num = ""
        current_heading = ""
        current_text = []
        
        # Regex for clause numbers
        clause_pattern = re.compile(r'^(\d+\.[\d\.]*|\([a-z]\)|\([ivx]+\))\s*', re.IGNORECASE)
        heading_pattern = re.compile(r'^([A-Z][A-Z\s]{3,}):?\s*$|^([A-Z][a-z\s]+):$')
        
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
            
            # Check if this is a clause number
            clause_match = clause_pattern.match(para)
            heading_match = heading_pattern.match(para)
            
            if clause_match:
                # Save previous clause if exists
                if current_text:
                    clauses.append(Clause(
                        number=current_clause_num or str(len(clauses) + 1),
                        heading=current_heading,
                        text=' '.join(current_text)
                    ))
                
                current_clause_num = clause_match.group(1).strip()
                current_heading = ""
                current_text = [para]
                
            elif heading_match and len(para) < 100:
                # This is likely a heading
                if current_text:
                    clauses.append(Clause(
                        number=current_clause_num or str(len(clauses) + 1),
                        heading=current_heading,
                        text=' '.join(current_text)
                    ))
                
                current_clause_num = str(len(clauses) + 1)
                current_heading = para.strip(':')
                current_text = []
                
            else:
                # Continue current clause
                current_text.append(para)
        
        # Add final clause
        if current_text:
            clauses.append(Clause(
                number=current_clause_num or str(len(clauses) + 1),
                heading=current_heading,
                text=' '.join(current_text)
            ))
        
        # If no clauses were detected, split into logical chunks
        if len(clauses) == 0:
            chunks = self._split_into_chunks(text)
            for i, chunk in enumerate(chunks):
                clauses.append(Clause(
                    number=str(i + 1),
                    heading="",
                    text=chunk
                ))
        
        return clauses
    
    def _split_into_chunks(self, text: str, max_chunk_size: int = 1000) -> List[str]:
        """Split text into logical chunks for analysis."""
        sentences = re.split(r'(?<=[.!?])\s+', text)
        chunks = []
        current_chunk = []
        current_size = 0
        
        for sentence in sentences:
            sentence_len = len(sentence)
            if current_size + sentence_len > max_chunk_size and current_chunk:
                chunks.append(' '.join(current_chunk))
                current_chunk = [sentence]
                current_size = sentence_len
            else:
                current_chunk.append(sentence)
                current_size += sentence_len
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return chunks
    
    def _analyze_clause(self, clause: Clause):
        """Analyze a single clause for obligations, rights, prohibitions, and ambiguities."""
        text_lower = clause.text.lower()
        
        # Extract obligations
        for keyword in self.OBLIGATION_KEYWORDS:
            if keyword in text_lower:
                # Find sentences containing this keyword
                sentences = self._extract_sentences_with_keyword(clause.text, keyword)
                clause.obligations.extend(sentences)
        
        # Extract rights
        for keyword in self.RIGHTS_KEYWORDS:
            if keyword in text_lower:
                sentences = self._extract_sentences_with_keyword(clause.text, keyword)
                clause.rights.extend(sentences)
        
        # Extract prohibitions
        for keyword in self.PROHIBITION_KEYWORDS:
            if keyword in text_lower:
                sentences = self._extract_sentences_with_keyword(clause.text, keyword)
                clause.prohibitions.extend(sentences)
        
        # Detect ambiguities
        for term in self.AMBIGUOUS_TERMS:
            if term in text_lower:
                clause.ambiguities.append(f"Contains ambiguous term: '{term}'")
        
        # Detect risk indicators
        for risk_type, keywords in self.RISK_INDICATORS.items():
            for keyword in keywords:
                if keyword in text_lower:
                    clause.risk_indicators.append(f"{risk_type.upper()}: {keyword}")
        
        # Extract entities from clause
        clause.entities = self._extract_entities(clause.text)
        
        # Remove duplicates
        clause.obligations = list(set(clause.obligations))
        clause.rights = list(set(clause.rights))
        clause.prohibitions = list(set(clause.prohibitions))
        clause.ambiguities = list(set(clause.ambiguities))
        clause.risk_indicators = list(set(clause.risk_indicators))
    
    def _extract_sentences_with_keyword(self, text: str, keyword: str) -> List[str]:
        """Extract sentences containing a specific keyword."""
        sentences = re.split(r'(?<=[.!?])\s+', text)
        matching = []
        keyword_lower = keyword.lower()
        
        for sentence in sentences:
            if keyword_lower in sentence.lower():
                matching.append(sentence.strip())
        
        return matching
    
    def _extract_entities(self, text: str) -> Dict[str, List[str]]:
        """
        Extract named entities from text.
        Uses pattern matching for: parties, dates, amounts, etc.
        """
        entities = {
            'parties': [],
            'dates': [],
            'amounts': [],
            'durations': [],
            'locations': [],
            'percentages': []
        }
        
        # Extract parties (simple heuristic: capitalized names/companies)
        # Look for patterns like "Mr./Mrs./Ms. Name" or "Company Name Pvt Ltd"
        party_patterns = [
            r'\b(?:Mr\.?|Mrs\.?|Ms\.?|Dr\.?)\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*',
            r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+(?:Pvt\.?\s+Ltd\.?|Limited|LLC|Inc\.?|Corporation|Corp\.?)',
            r'\b[A-Z][A-Z\s&]+(?:Pvt\.?\s+Ltd\.?|Limited|LLC)'
        ]
        
        for pattern in party_patterns:
            matches = re.findall(pattern, text)
            entities['parties'].extend(matches)
        
        # Extract dates
        date_patterns = [
            r'\b\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\b',
            r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b',
            r'\b\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}\b'
        ]
        
        for pattern in date_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            entities['dates'].extend(matches)
        
        # Extract monetary amounts
        amount_patterns = [
            r'(?:Rs\.?|INR|₹)\s*[\d,]+(?:\.\d{2})?',
            r'[\d,]+(?:\.\d{2})?\s*(?:rupees|lakhs?|crores?)',
            r'\$\s*[\d,]+(?:\.\d{2})?',
            r'USD\s*[\d,]+(?:\.\d{2})?'
        ]
        
        for pattern in amount_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            entities['amounts'].extend(matches)
        
        # Extract durations/periods
        duration_patterns = [
            r'\b\d+\s*(?:days?|weeks?|months?|years?)\b',
            r'\b(?:one|two|three|four|five|six|seven|eight|nine|ten)\s+(?:days?|weeks?|months?|years?)\b'
        ]
        
        for pattern in duration_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            entities['durations'].extend(matches)
        
        # Extract percentages
        percentage_pattern = r'\b\d+(?:\.\d+)?%'
        entities['percentages'] = re.findall(percentage_pattern, text)
        
        # Remove duplicates and clean
        for key in entities:
            entities[key] = list(set([e.strip() for e in entities[key]]))
        
        return entities
    
    def _classify_contract_type(self, text: str) -> List[Tuple[str, float]]:
        """
        Classify contract type based on keyword matching.
        Returns list of (type, confidence_score) tuples.
        """
        text_lower = text.lower()
        scores = {}
        
        for contract_type, keywords in self.CONTRACT_TYPES.items():
            matches = sum(1 for keyword in keywords if keyword in text_lower)
            if matches > 0:
                # Simple confidence score based on keyword matches
                confidence = min(matches / len(keywords), 1.0)
                scores[contract_type] = confidence
        
        # Sort by confidence
        sorted_types = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        # Return types with confidence > 0.1
        return [(t, round(s, 2)) for t, s in sorted_types if s > 0.1]
    
    def _generate_summary(self) -> Dict[str, Any]:
        """Generate summary statistics of the analysis."""
        total_obligations = sum(len(c.obligations) for c in self.clauses)
        total_rights = sum(len(c.rights) for c in self.clauses)
        total_prohibitions = sum(len(c.prohibitions) for c in self.clauses)
        total_ambiguities = sum(len(c.ambiguities) for c in self.clauses)
        total_risks = sum(len(c.risk_indicators) for c in self.clauses)
        
        # Count clauses with risks
        risky_clauses = sum(1 for c in self.clauses if c.risk_indicators)
        ambiguous_clauses = sum(1 for c in self.clauses if c.ambiguities)
        
        return {
            'total_clauses': len(self.clauses),
            'total_obligations': total_obligations,
            'total_rights': total_rights,
            'total_prohibitions': total_prohibitions,
            'total_ambiguities': total_ambiguities,
            'total_risk_indicators': total_risks,
            'risky_clauses_count': risky_clauses,
            'ambiguous_clauses_count': ambiguous_clauses,
            'risk_percentage': round((risky_clauses / len(self.clauses) * 100) if self.clauses else 0, 1)
        }
    
    def _clause_to_dict(self, clause: Clause) -> Dict[str, Any]:
        """Convert Clause object to dictionary."""
        return {
            'number': clause.number,
            'heading': clause.heading,
            'text': clause.text,
            'obligations': clause.obligations,
            'rights': clause.rights,
            'prohibitions': clause.prohibitions,
            'entities': clause.entities,
            'ambiguities': clause.ambiguities,
            'risk_indicators': clause.risk_indicators
        }
