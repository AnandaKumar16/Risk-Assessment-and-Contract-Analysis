# Legal Contract Analysis Assistant for Indian SMEs

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

A GenAI-powered contract analysis tool designed specifically for Small and Medium Enterprise (SME) owners in India to understand, evaluate, and manage complex legal contracts.

---

## 🎯 Overview

This application helps SME owners in India:

- ✅ **Understand** complex legal language in plain business English
- ✅ **Identify** risks, unfavorable clauses, and hidden liabilities
- ✅ **Evaluate** contracts with AI-powered risk scoring
- ✅ **Negotiate** better terms with specific renegotiation suggestions
- ✅ **Make informed** business decisions with comprehensive analysis

---

## ⚠️ Important Disclaimer

**This tool is for informational and analytical purposes only and does NOT constitute legal advice.** All interpretations are based solely on the contract text provided. Always consult with a qualified legal professional before making any contractual decisions.

---

## 🚀 Features

### Core Analysis Capabilities

1. **Document Processing**
   - Supports PDF, DOCX, and TXT formats
   - Automatic text extraction and preprocessing
   - Multi-language detection (English/Hindi)

2. **Contract Classification**
   - Identifies contract types (Employment, Vendor, Service, Lease, etc.)
   - Confidence scoring for classifications

3. **Clause Extraction & Analysis**
   - Automatic clause segmentation
   - Plain language summaries
   - Obligation, rights, and prohibition detection

4. **Named Entity Recognition**
   - Extracts parties, dates, amounts, durations
   - Identifies key terms and conditions

5. **Risk Assessment**
   - Clause-level risk scoring (0-100)
   - Contract-level composite risk rating
   - Identifies unfavorable terms for SMEs

6. **Ambiguity Detection**
   - Flags vague or undefined terms
   - Highlights subjective language
   - Points out missing safeguards

7. **Renegotiation Support**
   - Specific alternative clause suggestions
   - Explains why alternatives are better
   - Prioritizes changes by impact

8. **SME-Friendly Reporting**
   - Executive summaries in business language
   - Key takeaways and action items
   - Export to Markdown and JSON

---

## 📋 Supported Contract Types

- Employment Agreements
- Vendor / Supplier Contracts
- Service Agreements
- Lease / Rental Agreements
- Partnership Deeds
- Licensing Agreements
- NDAs / Confidentiality Agreements
- Other commercial contracts

---

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Step 1: Clone or Download

```bash
# If using Git
git clone <repository-url>
cd contract-analyzer

# Or download and extract the ZIP file
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🎮 Usage

### Running the Application

1. **Start the Streamlit app:**

```bash
streamlit run app.py
```

2. **Open your browser:**
   - The app will automatically open at `http://localhost:8501`
   - If not, manually navigate to the URL shown in the terminal

3. **Upload and analyze:**
   - Click "Browse files" in the sidebar
   - Select your contract (PDF, DOCX, or TXT)
   - Click "Analyze Contract"
   - Wait for the analysis to complete (typically 10-30 seconds)

4. **Review results:**
   - Navigate through tabs to see different analysis sections
   - Export reports as needed

---

## 📁 Project Structure

```
contract-analyzer/
│
├── app.py                          # Main Streamlit application
│
├── modules/                        # Core analysis modules
│   ├── __init__.py
│   ├── parser.py                   # Document parsing (PDF, DOCX, TXT)
│   ├── analyzer.py                 # Contract analysis & NLP
│   ├── risk_scorer.py              # Risk assessment engine
│   └── report_generator.py         # Report generation
│
├── config/                         # Configuration files
│   └── settings.json               # Application settings
│
├── templates/                      # Templates and samples
│   ├── sme_contract_templates.md   # SME-friendly clause templates
│   └── sample_contract.txt         # Sample contract for testing
│
├── outputs/                        # Generated reports (created at runtime)
│
├── requirements.txt                # Python dependencies
│
└── README.md                       # This file
```

---

## 🧪 Testing the Application

We've included a sample contract for testing:

1. Start the application: `streamlit run app.py`
2. Upload the file: `templates/sample_contract.txt`
3. Click "Analyze Contract"
4. Review the analysis results

The sample contract contains several intentionally unfavorable clauses to demonstrate the tool's capabilities.

---

## 📊 Understanding the Analysis

### Risk Levels

- **🟢 Low Risk (0-29):** Clause appears balanced and standard
- **🟡 Medium Risk (30-59):** Some concerns; review and consider modifications
- **🔴 High Risk (60-100):** Significant risks; renegotiation strongly recommended

### Key Sections in Reports

1. **Executive Summary:** Business-friendly overview of the contract
2. **Risk Assessment:** Overall risk score and distribution
3. **Unfavorable Clauses:** Specific problematic clauses with recommendations
4. **Clause Analysis:** Detailed breakdown of each clause
5. **Entities:** Key information extracted (parties, dates, amounts)
6. **Export:** Download comprehensive reports

---

## 🎯 Use Cases

### For SME Owners

- Review vendor contracts before signing
- Understand employment agreements
- Evaluate service provider terms
- Assess lease agreements
- Analyze partnership proposals

### For Startup Founders

- Review investor agreements
- Evaluate SaaS contracts
- Understand licensing terms
- Assess co-founder agreements

### For Freelancers

- Review client contracts
- Understand NDA terms
- Evaluate project agreements

---

## 🔒 Privacy & Security

- **No data storage:** Contracts are processed in memory only
- **No external API calls:** All analysis is performed locally
- **Confidential:** Your contract data never leaves your machine
- **Open source:** Full transparency in processing logic

---

## ⚙️ Technical Details

### NLP Techniques Used

1. **Pattern Matching:** Keyword-based detection for obligations, rights, prohibitions
2. **Named Entity Recognition:** Regex-based extraction of entities
3. **Clause Segmentation:** Heuristic-based clause boundary detection
4. **Risk Scoring:** Rule-based scoring with weighted factors
5. **Classification:** Keyword frequency analysis for contract types

### Limitations

- **Not a replacement for legal counsel:** Always consult a lawyer for important contracts
- **Pattern-based:** May miss context-specific nuances
- **English-focused:** Best results with English contracts
- **India-centric:** Optimized for Indian contract contexts
- **No case law:** Does not reference legal precedents or statutes

---

## 🛠️ Troubleshooting

### Common Issues

**Problem:** "PyPDF2 library not installed" error
```bash
Solution: pip install PyPDF2
```

**Problem:** "python-docx library not installed" error
```bash
Solution: pip install python-docx
```

**Problem:** Streamlit won't start
```bash
Solution: 
1. Ensure virtual environment is activated
2. Reinstall streamlit: pip install --upgrade streamlit
3. Check Python version: python --version (should be 3.8+)
```

**Problem:** PDF extraction returns empty text
```bash
Solution: 
1. Ensure PDF is not scanned/image-based
2. Try converting to DOCX or TXT first
3. Check if PDF is password-protected
```

**Problem:** Analysis taking too long
```bash
Solution:
1. Check contract file size (should be < 10MB)
2. For very large contracts, consider splitting into sections
```

---

## 🔄 Future Enhancements

Potential future features:

- [ ] Integration with Indian legal databases
- [ ] Advanced NLP with transformer models
- [ ] Comparative contract analysis
- [ ] Contract drafting assistant
- [ ] Mobile application
- [ ] Multi-party contract analysis
- [ ] Version comparison
- [ ] Email integration

---

## 📝 Contributing

Contributions are welcome! Areas where you can help:

1. **Improve NLP accuracy:** Better clause extraction algorithms
2. **Add contract types:** Support for more contract categories
3. **Enhance risk scoring:** More sophisticated risk models
4. **Better templates:** Additional SME-friendly clause templates
5. **Documentation:** Improve guides and examples
6. **Testing:** Add test cases and edge case handling

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Document parsing powered by [PyPDF2](https://pypdf2.readthedocs.io/) and [python-docx](https://python-docx.readthedocs.io/)
- Designed for Indian SME community

---

## 📞 Support

For questions, issues, or suggestions:

1. Check the Troubleshooting section above
2. Review the sample contract and templates
3. Consult the inline documentation in the code

---

## 🎓 Educational Purpose

This tool is designed to:

- **Educate** SME owners about contract terms
- **Empower** better negotiation discussions
- **Highlight** potential risks proactively
- **Guide** toward legal consultation when needed

It is **NOT** designed to:

- Replace legal professionals
- Provide legally binding advice
- Guarantee accuracy of analysis
- Make decisions on your behalf

---

## 📚 Additional Resources

### Recommended Reading

- **Indian Contract Law Basics:** Understanding the Indian Contract Act, 1872
- **SME Legal Protection:** Common pitfalls in business contracts
- **Negotiation Skills:** How to negotiate better contract terms
- **Legal Due Diligence:** Checklist for contract review

### When to Consult a Lawyer

Always seek legal advice for:

- High-value contracts (> ₹10 lakhs)
- Long-term commitments (> 2 years)
- Contracts with complex IP provisions
- International contracts
- Contracts with significant liability exposure
- Employment contracts for key personnel
- Merger/acquisition agreements
- Any contract you don't fully understand

---

## 🌟 Getting the Most Out of This Tool

### Best Practices

1. **Upload complete contracts:** Ensure all pages are included
2. **Review all tabs:** Don't just rely on the summary
3. **Focus on high-risk clauses:** Prioritize your negotiation points
4. **Use templates as guides:** Refer to provided clause alternatives
5. **Document everything:** Export reports for your records
6. **Consult professionals:** Use this as preparation for legal consultation
7. **Track changes:** Re-analyze after negotiation to see improvements

### Workflow Suggestion

1. **Initial Upload:** Get quick risk assessment
2. **Detailed Review:** Go through unfavorable clauses
3. **Prepare Questions:** Note concerns for lawyer discussion
4. **Negotiate:** Use alternative suggestions as negotiation starting points
5. **Re-analyze:** Upload revised contract to verify improvements
6. **Final Review:** Professional legal review before signing

---

**Version:** 1.0.0  
**Last Updated:** February 2026  
**Maintained for:** Indian SME Community

---

🚀 **Ready to analyze your first contract? Run `streamlit run app.py` to get started!**
