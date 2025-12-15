# Quantum Beta Portfolio Analytics — ChatGPT Custom GPT Implementation Guide

## Overview

Quantum is a deterministic financial document processor and calculation engine designed to turn messy financial data into audit-ready reports. This guide shows you how to implement Quantum as a custom GPT in ChatGPT.

---

## Files Included

You have 5 core files to upload/reference when creating your custom GPT:

### 1. **quantum_system_prompt.md**
- **Purpose:** The "personality" and operational rules for your GPT
- **Use:** Copy the entire contents into the "System Prompt" or "Instructions" field in ChatGPT's GPT Builder
- **Key Sections:**
  - Identity & purpose
  - How to operate (extraction, calculation, output)
  - Data handling & security principles
  - Tone & interaction style

### 2. **quantum_capabilities.md**
- **Purpose:** Detailed specification of what Quantum can calculate
- **Use:** Reference document to paste into GPT context, or attach as knowledge file
- **Key Sections:**
  - Document extraction pipeline
  - Tax calculations (Roth, 1040, RMD)
  - Retirement analysis (TWR, MWR, IRR)
  - Lending metrics (DTI, LTV, amortization)
  - Insurance needs analysis
  - Validation rules & citations

### 3. **quantum_data_model.md**
- **Purpose:** Data schema definitions for inputs/outputs
- **Use:** Reference for understanding data structures; optional to include in GPT
- **Key Sections:**
  - Extraction artifact schema (with provenance)
  - Client profile JSON structure
  - Calculation request/output schemas
  - Validation & reconciliation rules

### 4. **quantum_portal_guide.md**
- **Purpose:** User workflows and portal features
- **Use:** For your user-facing documentation; optional for GPT context
- **Key Sections:**
  - 3 essential workflows
  - Client/Advisor/Admin portal features
  - Calculation menu & best practices
  - Support & troubleshooting

### 5. **quantum_system_prompt.md** (same as #1)
- Already listed above

---

## Step-by-Step: Setting Up in ChatGPT

### Step 1: Access GPT Builder
1. Log into ChatGPT (requires ChatGPT Plus or Team)
2. Click "Explore" → "Create a GPT"
3. Or go directly to https://chatgpt.com/gpts/editor

### Step 2: Fill in Basic Info
- **Name:** "Quantum Beta Portfolio Analytics"
- **Description:** "Deterministic financial document processor & calculation engine. Extract audit-ready data from PDFs, calculate tax/retirement/lending metrics with full audit trails."
- **Instructions (System Prompt):** [Copy entire contents of `quantum_system_prompt.md`]

### Step 3: Configure Capabilities
In the GPT Builder, ensure these are enabled:
- ✅ Web browsing (optional; for looking up current tax brackets)
- ✅ Code interpreter (useful for complex calculations)
- ❌ DALL-E (not needed)

### Step 4: Upload Knowledge Files
Attach these as knowledge files:
1. `quantum_capabilities.md` – Full calculation specs
2. `quantum_data_model.md` – Data schemas
3. `quantum_portal_guide.md` – User workflows (optional)

**How to upload in GPT Builder:**
- Scroll down to "Knowledge"
- Click "Upload files"
- Select your .md files
- Files will be indexed automatically

### Step 5: Configure Actions (Optional)
If you want Quantum to integrate with external tools:
- **Tax Software Integration:** Connect to TurboTax API (if available)
- **Accounting Platform:** Connect to QuickBooks Online API
- **Data Aggregator:** Connect to Yodlee or Plaid API

(For now, skip this unless you have API keys ready)

### Step 6: Set Conversation Starters
Add helpful prompts users can click to get started:
- "I have a bank statement to extract"
- "Calculate my Roth conversion tax impact"
- "Analyze my debt-to-income ratio for a mortgage"
- "Generate a multi-year retirement projection"
- "Run an IRR analysis on this investment deal"

### Step 7: Test & Save
1. Click the "Preview" pane on the right
2. Test a simple request: "Extract data from a bank statement" or "What can you calculate?"
3. Verify it responds with Quantum personality & offers key capabilities
4. Click "Save" when satisfied

---

## Implementation Checklist

- [ ] Create new custom GPT in ChatGPT
- [ ] Copy `quantum_system_prompt.md` into "Instructions"
- [ ] Upload `quantum_capabilities.md` as knowledge file
- [ ] Upload `quantum_data_model.md` as knowledge file (optional)
- [ ] Upload `quantum_portal_guide.md` as knowledge file (optional)
- [ ] Set conversation starters (5-6 examples)
- [ ] Enable Code Interpreter (recommended)
- [ ] Enable Web Browsing (recommended for tax rule lookups)
- [ ] Test with sample request (e.g., "Extract a bank statement")
- [ ] Test with calculation (e.g., "Calculate Roth conversion")
- [ ] Save & publish GPT
- [ ] Share link with team/clients

---

## Key Features Once Deployed

### Document Extraction
- User uploads PDF, spreadsheet, or image
- Quantum classifies document type & extracts data
- Provides extraction artifact with full provenance (every value traceable to source)
- Surfaces validation flags for user confirmation

### Tax Calculations
- Roth conversion optimization (federal + state, multi-year scenarios)
- 1040 projections with estimated tax & refund/payment
- RMD planning under SECURE Act rules

### Retirement Analysis
- Time-weighted return (TWR) & money-weighted return (MWR)
- Cash-flow waterfalls showing deposits, withdrawals, earnings, fees
- Rebalancing impact analysis

### Lending Metrics
- Debt-to-Income (DTI) ratio calculation
- Loan-to-Value (LTV) analysis
- Amortization schedules with prepayment scenarios

### Investment Analysis
- IRR & NPV calculations for deals/contracts
- Sensitivity analysis (what-if scenarios)

### All Outputs Include
- Step-by-step math (no black boxes)
- Citations to tax code, IRS publications, or SECURE Act rules
- Markdown worksheets (human-readable) + JSON artifacts (machine-readable)
- CSV exports for tax software

---

## Customization Options

### Option A: Minimal (GPT Only)
- Use only the system prompt + knowledge files
- Users interact via chat
- No persistent storage or multi-user portal
- **Good for:** Individual users, tax pros wanting a smart calculator

### Option B: Integrated (GPT + Your Backend)
- GPT as front-end conversational interface
- Your backend stores calculations, client profiles, audit logs
- GPT can call your API to save/retrieve data
- **Good for:** Financial advisory firms wanting client portal + calculations

### Option C: Enterprise (GPT + Full Platform)
- GPT as one interface (chat)
- Full web portal for clients (upload, review, download)
- Admin dashboard for advisors
- Database for persistent storage, audit trails, compliance
- **Good for:** Large advisory firms, financial institutions, compliance-heavy use cases

For now, Option A (GPT only) is recommended to get started quickly.

---

## Usage Examples

### Example 1: Extract Bank Statement
```
User: I have a Chase bank statement (3 months). Can you extract the key figures?
[User uploads PDF]

Quantum: "Bank Statement detected — Chase Checking, 3 months (Aug-Oct 2024) • 95% confidence.

Extracted:
• Beginning balance: $5,000
• Total deposits: $10,500
• Total withdrawals: $8,200
• Ending balance: $7,300
• Fees: $35 (NSF charge on 9/15)

Validation flags:
⚠️ NSF charge detected (9/15/2024) — verify intent?
✅ Balances reconcile correctly

Ready to proceed? I can:
1. Refine any values
2. Run cash-flow analysis
3. Check for fraud patterns
4. Export as JSON/CSV"
```

### Example 2: Roth Conversion Analysis
```
User: I earned $150k this year (W-2 + $25k self-employment). I have $250k in a Traditional IRA. 
Can you analyze a Roth conversion?

Quantum: "Roth Conversion Analysis — 2024
Confirming inputs:
✓ Filing status: Single (assumed — correct?)
✓ State: Unknown (affects state tax — where do you live?)
✓ Current income: $177,500 (W-2 + SE + interest + dividends)
✓ Traditional IRA: $250,000 (100% pre-tax)

Proposed scenarios: $50k, $75k, $100k conversion

Results (preliminary):
• $50k conversion → $16,650 tax → $33,350 net to Roth
• $75k conversion → $24,975 tax → $50,025 net to Roth
• $100k conversion → $33,300 tax → $66,700 net to Roth

[Shows step-by-step math]
[Offers sensitivity analysis: 'What if income increases?']
[Provides citations: IRC §408(d)(3), IRS Pub 590-A]
[Offers download: Markdown worksheet, JSON, CSV]"
```

### Example 3: DTI Analysis
```
User: I'm applying for a mortgage. Can you calculate my debt-to-income ratio?
[User uploads: Pay stub, bank statement, mortgage pre-qual]

Quantum: "Mortgage DTI Analysis
Income:
• Gross monthly income: $12,500 (from pay stub)

Debts:
• Student loans: $450/mo
• Car loan: $300/mo
• Credit cards: $200/mo (minimum payments)
• Proposed mortgage payment: $2,800/mo
• Total monthly debt: $3,750

DTI Calculation:
$3,750 ÷ $12,500 = 30%

Result: ✅ ACCEPTABLE
Most lenders require <43% DTI. You're at 30%, well within range.
Lender guidelines: FHA typically allows up to 43%, conventional up to 43%.

[Shows details & exports to PDF]"
```

---

## Troubleshooting

### Issue: GPT doesn't extract data accurately
- **Solution:** Provide clearer document guidance. Example: "This is a Chase bank statement for Sep 2024. Please extract the transactions table only."
- Retrain with better examples if possible

### Issue: Calculations seem off
- **Solution:** Ask Quantum to show step-by-step math. Verify each assumption (tax year, filing status, state).
- Example: "Show me the federal tax bracket you're using for 2024, MFJ"

### Issue: GPT doesn't remember prior context
- **Solution:** ChatGPT loses context after ~20 exchanges. Provide inputs directly (or use your own backend to persist).
- Workaround: Copy/paste prior calculation results as context for follow-up calculations

### Issue: Knowledge files not being used
- **Solution:** Make sure files are uploaded as .md (not .pdf). Check that GPT builder shows "1 file" under Knowledge section.
- Test by asking: "What tax rules do you use for Roth conversions?" — should cite sources

---

## Advanced: Connecting Your Backend

If you want Quantum to save calculations, maintain client profiles, and generate audit logs:

### API Integration (Option B)
1. Create a simple REST API on your backend (Node, Python, etc.)
2. In ChatGPT GPT Builder, add "Actions" → "Custom Integration"
3. Define endpoints:
   - `POST /extractions` – Save extraction artifact
   - `POST /calculations` – Save calculation result
   - `GET /client/{id}/profile` – Retrieve client profile
   - `POST /client/{id}/profile` – Update profile

4. Example:
```json
{
  "openapi": "3.0.0",
  "info": { "title": "Quantum API", "version": "1.0" },
  "servers": [{ "url": "https://your-api.com/api" }],
  "paths": {
    "/extractions": {
      "post": {
        "operationId": "saveExtraction",
        "requestBody": { "content": { "application/json": { "$ref": "#/components/schemas/ExtractionArtifact" } } },
        "responses": { "200": { "description": "Extraction saved" } }
      }
    }
  }
}
```

### Database Schema (Recommended)
```sql
CREATE TABLE qd_extractions (
  id UUID PRIMARY KEY,
  client_id UUID REFERENCES qd_clients(id),
  document_id UUID,
  extracted_data JSONB,
  provenance JSONB,
  created_at TIMESTAMP,
  created_by UUID
);

CREATE TABLE qd_calculations (
  id UUID PRIMARY KEY,
  client_id UUID REFERENCES qd_clients(id),
  calculation_type VARCHAR,
  inputs JSONB,
  results JSONB,
  audit_trail JSONB,
  created_at TIMESTAMP
);

CREATE TABLE qd_client_profiles (
  client_id UUID PRIMARY KEY,
  personal_data JSONB,
  accounts JSONB,
  tax_preferences JSONB,
  consent JSONB,
  updated_at TIMESTAMP
);
```

---

## Compliance & Security Notes

- **Data Privacy:** If handling PII (SSN, account numbers), ensure you comply with GLBA, HIPAA, or SOX as applicable
- **Audit Trail:** Log all calculations & modifications for compliance
- **Encryption:** Use TLS for API calls, AES-256 for stored data
- **Retention:** Set data retention policies (default 365 days, configurable per client)
- **Redaction:** Mask PII in user-facing outputs (show ****1234 instead of full account number)

---

## Deployment Checklist

### Pre-Launch
- [ ] GPT tested with 10+ sample requests
- [ ] Knowledge files indexed & searchable
- [ ] Conversation starters working
- [ ] Tone & personality matches Quantum brand
- [ ] All calculations verified against source data
- [ ] Tax rules current for 2024

### Launch
- [ ] Share GPT link with beta users / team
- [ ] Collect feedback on accuracy & usability
- [ ] Document common issues & solutions
- [ ] Train users on best practices (clear docs, specific requests)

### Post-Launch (Ongoing)
- [ ] Monitor calculation accuracy (sample-check results)
- [ ] Update tax rules annually (new brackets, SECURE Act changes, etc.)
- [ ] Collect user feedback & improve
- [ ] Expand supported calculations based on demand

---

## Next Steps

1. **Immediately:** Set up GPT in ChatGPT using steps above
2. **This week:** Test with 5-10 sample calculations
3. **Next week:** Share with 2-3 trusted advisors for feedback
4. **Month 2:** Iterate on accuracy & UX; add features based on feedback
5. **Month 3:** Consider Option B (API integration) if demand warrants
6. **Q2 2025:** Evaluate full platform (Option C) based on user volume

---

## Support & Questions

For questions about Quantum:
- Review the full documentation (all 5 files)
- Test in the GPT Preview pane
- Iteratively improve based on real usage

For technical questions about ChatGPT GPT Builder:
- See ChatGPT's GPT Builder documentation: https://platform.openai.com/docs/assistants
- Visit OpenAI forums or support

Good luck! 🚀
