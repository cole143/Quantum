# Quantum Beta Portfolio Analytics — Capabilities & Calculation Specs

## Core Capabilities Catalog

### 1. Document Extraction & Classification
**Supported Document Types:**
- Bank statements (checking, savings, money market)
- Investment account statements (brokerage, 401k, IRA, HSA)
- Tax returns (1040, Schedule C, Schedule D, K-1)
- Loan statements (mortgage, auto, student, personal)
- Insurance policies & statements
- Contracts & agreements
- Pay stubs & W-2 forms
- Property tax assessments
- Credit card statements

**Extraction Pipeline:**
```
Ingest → Normalize → OCR → Layout Analysis → Parse → Template Match 
→ Heuristics/ML → Table Build → Post-Process → Validate → Redact → Artifact
```

**Output: Extraction Artifact (JSON)**
```json
{
  "document_id": "doc_uuid",
  "classification": "Bank Statement",
  "confidence": 0.92,
  "metadata": {
    "source": "file_name.pdf",
    "page_count": 3,
    "extracted_date": "2024-11-10",
    "date_range": ["2024-08-01", "2024-10-31"]
  },
  "extracted_data": {
    "institution": "Chase Bank",
    "account_type": "Checking",
    "account_number": "****1234",
    "beginning_balance": { "value": 5000, "provenance": "page 1, line 3" },
    "transactions": [
      {
        "date": "2024-08-05",
        "description": "Direct deposit",
        "amount": 3500,
        "type": "deposit",
        "page": 1,
        "confidence": 0.99
      }
    ]
  },
  "validation_flags": [
    { "level": "warning", "text": "NSF charge detected on 2024-09-15 — verify intent?" },
    { "level": "info", "text": "Sum of withdrawals exceeds deposits — account drew down" }
  ]
}
```

---

### 2. Tax Planning & Projections

#### Roth Conversion Optimization
**Input:** Filing status, current income, IRA balance, conversion amount (variable)
**Calculation:**
1. Calculate current tax bracket (federal + state)
2. Estimate tax impact of conversion (ordinary income inclusion)
3. Consider FICA consequences (if self-employed)
4. Model multi-year conversions to spread tax burden
5. Sensitivity: vary conversion amounts ±25%, ±50%
6. Output: tax-efficient ladder schedule

**Key Rules:**
- Roth conversions taxed as ordinary income in conversion year
- Pro-rata rule: mixture of pre-tax & after-tax IRA balances
- State tax varies (CA 9.3%, NY 6.85%, TX 0%, etc.)
- FICA: conversions DO NOT trigger FICA if retired

**Formula:**
```
Taxable Income = W-2 + Self-Employment + Roth Conversion + Other Income
Tax = Tax(Taxable Income) - Tax(Taxable Income - Conversion)
```

#### Federal 1040 Projection
**Input:** Income sources, deductions, filing status, state, prior year carryovers
**Calculation:**
1. Aggregate income: wages + interest + dividends + capital gains + self-employment
2. Apply standard or itemized deduction
3. Calculate tax using 2024 brackets
4. Apply credits (EITC, CTC, education, etc.)
5. Model state income tax (if applicable)
6. Compare filing statuses (MFJ vs. MFS vs. HoH)

**Output:** Form 1040 projection with estimated tax liability + refund/payment due

#### RMD Planning (SECURE Act 2.0)
**Rules:**
- Starting age: 73 (born 2023+), 72 (born 2022), 72 (born 1951-2021), 70.5 (born pre-1951)
- Calculation: account balance ÷ IRS life expectancy factor
- Aggregation rule: IRAs can be aggregated; 401k plans separate
- Penalty: 25% of shortfall (reduced to 10% if corrected timely)

**Calculation:**
```
RMD = Prior Year December 31 Balance ÷ IRS Life Expectancy Factor
Penalty = 0.25 × (Required Distribution - Actual Distribution)
```

---

### 3. Retirement Income Analysis

#### Time-Weighted Return (TWR)
**Use:** Portfolio performance independent of cash flows
**Formula:**
```
TWR = [(1 + R1) × (1 + R2) × ... × (1 + Rn)] - 1

Where R_i = (Ending Value_i − Beginning Value_i − Net Flow_i) / (Beginning Value_i + Net Flow_i)
```

#### Money-Weighted Return (MWR) / Internal Rate of Return
**Use:** Overall account performance including timing of deposits/withdrawals
**Method:** Solve for discount rate where NPV = 0
```
0 = Initial Balance + Sum(Flows / (1 + r)^t) − Ending Value
```

#### Cash-Flow Waterfall
**Input:** Deposits, withdrawals, dividends, fees, tax withholdings
**Output:** Period-by-period account progression
```
Beginning Balance
+ Deposits
+ Earnings (dividends + capital gains)
- Withdrawals
- Fees
- Taxes
= Ending Balance
```

---

### 4. Lending & Credit Analysis

#### Debt-to-Income (DTI) Ratio
**Formula:**
```
DTI = Total Monthly Debt Payments / Gross Monthly Income
```
**Components:**
- Housing (mortgage/rent + taxes + insurance + HOA)
- Auto loans
- Student loans
- Credit card minimum payments
- Child support

**Thresholds:**
- FHA: <43% (standard), up to 50% with compensating factors
- Conventional: <43% (most lenders)
- VA: No set limit, but typically <40%

#### Loan-to-Value (LTV)
**Formula:**
```
LTV = Loan Amount / Property Value
CLTV = (First Mortgage + Second Mortgage + HELOC) / Property Value
```

#### Amortization Schedule
**Input:** Principal, rate, term, start date
**Calculation (monthly):**
```
Monthly Payment = P × [r(1+r)^n] / [(1+r)^n - 1]
Where P = principal, r = monthly rate, n = number of payments

For each period:
Interest Payment = Remaining Balance × Monthly Rate
Principal Payment = Total Payment − Interest Payment
Remaining Balance = Previous Balance − Principal Payment
```

---

### 5. Investment Analysis

#### IRR / NPV for Contracts & Deals
**Use:** Evaluate investment attractiveness
**Formula (NPV):**
```
NPV = Sum(Cash Flow_t / (1 + discount_rate)^t) − Initial Investment
```

**Formula (IRR):** Solve for r where NPV = 0
```
0 = Initial Outlay + Sum(Inflows_t / (1 + IRR)^t)
```

---

### 6. Insurance Needs Analysis

#### Income Replacement Ratio
**Input:** Current income, dependents, years to retirement
**Calculation:**
```
Annual Benefit Needed = Annual Income × Replacement Ratio (60-80%)
Life Insurance Death Benefit = Annual Benefit × Years Until Retirement / Discount Factor
```

#### Education Funding
**Input:** Current age of child, college start year, cost per year, inflation rate
**Formula:**
```
Future Cost = Current Cost × (1 + Inflation)^Years Until College
PV of Needs = Sum(Future Cost / (1 + Growth Rate)^years funded)
```

---

### 7. Banking & Cash Flow Analysis

#### NSF Detection
- Flag transactions where available balance goes negative
- Alert if overdraft fees are charged
- Identify patterns (recurring NSF charges)

#### Reconciliation
- Match deposits to known income sources
- Match withdrawals to known expenses
- Identify unexplained transfers
- Calculate true cash flow (net deposits − withdrawals − fees)

---

## Validation Rules

**All extractions checked against:**
1. Date logic (dates within reasonable range, no future dates unless expected)
2. Numerical consistency (totals reconcile, balances make sense)
3. Format conformance (account numbers, SSN patterns, etc.)
4. Outlier detection (unusual transactions flagged for review)
5. Reconciliation (deposits ↔ statements ↔ tax forms alignment)

---

## Assumptions & Limitations

### Assumptions (flagged for confirmation)
- 2024 tax brackets & rules (unless year specified)
- Single filer (unless noted)
- U.S. tax treatment (federal + state; not international)
- Compound monthly (unless specified)
- No extraordinary life events (marriage, disability, etc.)

### Limitations
- No modeling of edge cases without explicit input (e.g., Roth conversion for high-income filers subject to backdoor Roth rules)
- State-specific rules vary; some states not fully modeled
- Insurance needs analysis uses industry-standard ratios, not actuarial modeling
- Does NOT model cryptocurrency, alternative investments, or complex derivatives
- Does NOT provide investment advice

---

## Output Formats

**For Every Calculation, Provide:**
1. **Markdown Worksheet** (human-readable)
   - Inputs summary
   - Calculation rules/citations
   - Step-by-step math
   - Results + key metrics
   - Sensitivity table

2. **JSON Artifact** (machine-readable)
   - All inputs + assumptions
   - All intermediate calculations
   - Final results
   - Audit trail

3. **CSV Export** (for external tools)
   - Waterfall tables
   - Amortization schedules
   - Multi-year projections
   - Sensitivity grids

---

## Citation Standards

**For every tax/retirement rule, cite:**
- IRS Publication number (e.g., "Pub 17")
- Tax code section (e.g., "IRC §408(m)")
- SECURE Act rule (if applicable, with year: "SECURE 2.0, 2023")
- Year of rule applicability (e.g., "2024 rule; check current year")

**Example:**
> RMD age 73 (SECURE 2.0, 2023; applies to individuals born in 1951 and later). Calculation per IRC §408(a)(6) and IRS Pub 590-B.
