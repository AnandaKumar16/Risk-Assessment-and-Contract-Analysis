# Quick Start Guide
# Legal Contract Analysis Assistant

## Installation (5 minutes)

### Step 1: Open PowerShell in the project folder
```powershell
cd "c:\Users\nnand\Desktop\GUVI\contract-analyzer"
```

### Step 2: Create virtual environment
```powershell
python -m venv venv
```

### Step 3: Activate virtual environment
```powershell
.\venv\Scripts\Activate.ps1
```

If you get an error about execution policy, run this first:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Step 4: Install dependencies
```powershell
pip install -r requirements.txt
```

### Step 5: Launch the application
```powershell
streamlit run app.py
```

## Using the Application

1. **Browser will open automatically** at http://localhost:8501
2. **Upload a contract** using the file uploader in the sidebar
3. **Click "Analyze Contract"** button
4. **Wait 10-30 seconds** for analysis to complete
5. **Review results** across different tabs:
   - Summary: Executive overview
   - Risk Assessment: Overall risk analysis
   - Unfavorable Clauses: Problem areas
   - Clause Analysis: Detailed breakdown
   - Entities: Extracted information
   - Export: Download reports

## Testing with Sample Contract

To test the application:
1. Upload the file: `templates/sample_contract.txt`
2. This sample has intentionally unfavorable clauses
3. Demonstrates all analysis features

## Common Commands

**Start the app:**
```powershell
streamlit run app.py
```

**Stop the app:**
- Press `Ctrl + C` in the terminal

**Reactivate virtual environment** (if you closed PowerShell):
```powershell
cd "c:\Users\nnand\Desktop\GUVI\contract-analyzer"
.\venv\Scripts\Activate.ps1
streamlit run app.py
```

**Deactivate virtual environment:**
```powershell
deactivate
```

## Troubleshooting

**Problem: "streamlit: command not found"**
Solution: Make sure virtual environment is activated (you should see `(venv)` in your prompt)

**Problem: Port 8501 already in use**
Solution: 
```powershell
streamlit run app.py --server.port 8502
```

**Problem: PDF parsing not working**
Solution: Ensure PyPDF2 is installed:
```powershell
pip install PyPDF2
```

## Next Steps

- Read the full README.md for detailed documentation
- Review templates/sme_contract_templates.md for balanced clause examples
- Analyze your own contracts
- Export reports for your records

## Support

- Check README.md for comprehensive documentation
- Review inline code documentation
- Examine the sample contract for testing

---

Happy analyzing! 🚀
