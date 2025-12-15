# Quantum Beta Portfolio Analytics — Quick Start & Portal Guide

## Getting Started: 3 Essential Workflows

### Workflow 1: Document Upload & Extract
1. **User uploads document** (PDF, spreadsheet, image of bank statement)
2. **Quantum classifies** (e.g., "Bank Statement — 3 months, personal • 92%")
3. **Extraction artifact generated** with all values + provenance
4. **Validation flags displayed** as clickable chips ("NSF charge detected — verify?" / "Unusual transfer — confirm?")
5. **User reviews & confirms** or requests corrections
6. **Profile updated** (if new account, new template, etc.)
7. **Extraction fingerprinted** for future reuse

---

### Workflow 2: Request a Calculation
**Example: Roth Conversion Analysis**

1. **User inputs trigger**
   - "I want to analyze a Roth conversion for tax year 2024"
   - OR uploads documents + requests "calculate my tax liability"

2. **Quantum confirms inputs**
   - Filing status? (pulls from Client Profile if available)
   - Current income? (matches to recent W-2/1099)
   - IRA balances? (from prior extractions or manual entry)
   - Proposed conversion amount? (from user)

3. **Calculation runs**
   - Apply federal tax brackets (2024)
   - Calculate FICA impact (if applicable)
   - Add state income tax (if applicable)
   - Model multi-year scenarios

4. **Output generated**
   - Markdown worksheet (human-readable)
   - JSON artifact (machine-readable, traceable)
   - CSV export (for tax software)
   - Sensitivity analysis ("What if income increases by $10k?")

5. **User downloads & submits to tax professional** or stores in Client Portal

---

### Workflow 3: Multi-Document Analysis
**Example: Loan Approval (DTI/LTV Calculation)**

1. **User uploads:** Pay stub + bank statement + mortgage pre-qual + asset statement
2. **Quantum extracts:** Monthly income, debts, assets, property value
3. **Quantum calculates:**
   - Debt-to-Income ratio (DTI = total monthly debt ÷ gross income)
   - Loan-to-Value (LTV = loan amount ÷ property value)
   - Residual income (gross income − debts − taxes − living expenses)
4. **Output:** One-page lending report with clear pass/fail indicators
5. **User shares** with lender or keeps for records

---

## Client Portal Features

### Dashboard
- **Recent Documents:** Last 5 uploads with status (extracted, validated, ready)
- **Pending Actions:** Validation flags requiring user confirmation
- **Saved Calculations:** Links to prior tax projections, analyses, etc.
- **Quick Actions:** "Upload New Document" / "Request Calculation" / "Download Reports"

### Document Management
- **View Extractions:** Click any document to see extracted values + provenance
- **Review & Edit:** Correct any misparsed values; Quantum updates artifact
- **Download:** Get extraction artifact (JSON), original file, or formatted worksheet
- **Flag for Review:** Tag for advisor review if uncertain

### Calculations
- **My Calculations:** Searchable list (by type, date, result)
- **Reuse & Modify:** Load prior calculation, adjust assumptions, re-run
- **Export:** Download as PDF, CSV, JSON for tax pro / advisor

### Settings
- **Profile:** Name, filing status, state, dependents, contact
- **Preferences:** Tax year, calculation defaults (discount rate, etc.)
- **Consent:** Enable/disable profile persistence & auto-reuse
- **Data Retention:** Set how long extractions are kept (default 365 days)

### Notifications
- **Extraction Ready:** "Your bank statement has been extracted & validated"
- **Calculation Complete:** "Your Roth conversion analysis is ready"
- **Advisor Comment:** "Your tax advisor left a note on your extraction"

---

## Advisor Portal Features

### Client Management
- **Client List:** All clients with last-upload date, outstanding items
- **Bulk Actions:** Schedule calculations for multiple clients at year-end

### Document Review
- **Raw Extraction Preview:** See raw OCR + parsed values
- **Validation Flags:** Review all warnings & errors flagged by Quantum
- **Manual Corrections:** Edit misparsed values; Quantum re-validates
- **Approval Workflow:** Mark as "reviewed" and send to client

### Scenario & Assumptions
- **Modify Assumptions:** Override default tax brackets, rates, etc.
- **Run Scenarios:** "What if we convert $50k instead of $75k?"
- **Save Assumptions:** Store as templates for future clients with similar profiles

### Audit Log
- **Full History:** Every extraction, calculation, correction, approval
- **Versioning:** Access prior versions of calculations
- **Export:** Download audit log as CSV for compliance

### Reporting
- **Aggregate Reports:** "How many clients had Roth conversions this year?"
- **Risk Dashboard:** Clients with unusual transactions flagged
- **Performance Metrics:** Average time to process, error rates, etc.

---

## Admin Portal Features

### User Management
- **RBAC:** Assign roles (Client, Advisor, Admin)
- **Access Control:** Define what each user can see/do
- **Audit Trail:** Track all admin actions

### Compliance & Legal
- **Data Retention Policies:** Set global defaults
- **Legal Holds:** Flag specific client data for retention
- **HIPAA/SOX Prep:** Generate compliance reports

### System Settings
- **Calculation Engine:** Version control, rule updates
- **Supported Documents:** Add/remove document types
- **Integration:** Connect to tax software, accounting platforms

---

## Integration Points (Future)

**Tax Software:**
- Export calculation to TurboTax / TaxAct / ProConnect format

**Accounting Platforms:**
- Push extracted transactions to QuickBooks / Xero

**Data Aggregates:**
- Sync with Morningstar, Facteus, or custom data sources

**Advisor Tech:**
- Connect to MoneyGuidePro, NaviPlan, Black Diamond, etc.

---

## Security & Compliance

### Data Security
- **Encryption:** AES-256 at rest, TLS 1.3 in transit
- **Access Control:** Role-based (RBAC), IP whitelisting optional
- **Audit Trail:** Immutable log of all reads, writes, exports
- **Redaction:** PII masked by default (account numbers, SSN)

### Compliance
- **GLBA:** Financial privacy safeguards
- **SOX:** If serving public company finance teams
- **State Regulations:** Varies by state (some require specific data handling)

### Backup & Disaster Recovery
- **Frequency:** Daily incremental, weekly full backups
- **Retention:** 30 days (configurable)
- **Recovery Time:** <2 hours for full restoration
- **Testing:** Monthly backup restore drills

---

## Calculation Menu (Quick Reference)

| Calculation Type | Input | Output | Use Case |
|---|---|---|---|
| **Roth Conversion** | Income, IRA balance, conversion amount | Tax impact, multi-year scenarios | Tax planning |
| **1040 Projection** | Income sources, deductions, credits | Estimated tax, refund/payment due | Tax planning |
| **RMD Planning** | Age, IRA balance, SECURE Act rules | Annual RMD amount, penalty if missed | Retirement planning |
| **DTI/LTV Analysis** | Income, debts, assets, property value | DTI %, LTV %, lending eligibility | Loan underwriting |
| **Amortization** | Loan amount, rate, term | Payment schedule, interest/principal breakdown | Loan analysis |
| **Portfolio TWR/MWR** | Deposits, withdrawals, earnings, dates | Performance metrics, GIPS-compliant returns | Performance reporting |
| **Cash-Flow Waterfall** | Deposits, withdrawals, fees, gains | Period-by-period balance progression | Account analysis |
| **Insurance Needs** | Income, dependents, years to retirement | Life insurance death benefit needed | Insurance analysis |
| **IRR/NPV** | Investment inflows, outflows, discount rate | Internal rate of return, present value | Investment evaluation |
| **NSF & Reconciliation** | Bank statements, expenses | Unexplained items, balance gaps | Cash management |

---

## Troubleshooting & Support

### Common Issues

**"My extraction is showing wrong values"**
1. Check document quality (clear? straight? readable?)
2. Review validation flags
3. Use "Edit" feature to correct, or re-upload with better quality image

**"I'm seeing a validation warning — what does it mean?"**
- Click the chip to expand
- Review the rule that triggered it
- Confirm it's accurate, or correct the data

**"Can I reuse a prior calculation?"**
- Yes! Click "Calculations" → find prior one → "Reuse & Modify"
- Change assumptions, re-run

**"How do I export for my tax software?"**
- Open calculation → "Download" → Select format (CSV, JSON, or Markdown)
- Import into TurboTax / TaxAct / ProConnect

### Support Channels
- **In-app Help:** Click ? icon for context-specific guides
- **Email:** support@quantumanalytics.io
- **Portal:** Submit ticket from "Support" menu
- **Advisor Hotline:** Dedicated phone line for tax pros & advisors

---

## Best Practices

### For Clients
1. **Keep documents organized** – Use clear naming (e.g., "2024_Sep_Chase_Statement")
2. **Upload regularly** – Monthly if possible, at least quarterly
3. **Review extractions** – Confirm values before calculations
4. **Save calculations** – Export worksheets for your records
5. **Enable profile consent** – Allows Quantum to reuse templates & assumptions

### For Advisors
1. **Batch process** – Upload multiple clients' docs at once
2. **Customize assumptions** – Override defaults for client-specific rules
3. **Flag for review** – Mark uncertain extractions for manual review
4. **Document corrections** – Leave notes when you edit extracted values
5. **Use templates** – Save recurring calculation assumptions

### For Admins
1. **Audit regularly** – Review access logs monthly
2. **Test backups** – Monthly restore drills
3. **Update rules** – Keep tax brackets, SECURE Act rules current
4. **Monitor performance** – Track extraction accuracy, calculation time

---

## Roadmap & Future Features

**Phase 2 (Q1 2025):**
- Multi-year projection dashboards
- Alternative investment support (crypto, real estate)
- International tax rules (Canadian, UK, etc.)

**Phase 3 (Q2 2025):**
- Machine learning confidence scoring for extractions
- Real-time data feeds (market data, tax law updates)
- API for third-party integrations

**Phase 4 (Q3+ 2025):**
- Mobile app (iOS/Android)
- Voice-controlled extraction ("Scan this bank statement")
- Blockchain-backed audit trail for high-compliance customers
