# Quantum Beta Portfolio Analytics — Data Model & Schema

## Core Data Structures

### 1. Extraction Artifact Schema
**Purpose:** Immutable record of extracted data with full provenance

```json
{
  "extraction_id": "uuid",
  "document_id": "doc_uuid",
  "timestamp": "2024-11-10T15:30:00Z",
  "document_metadata": {
    "filename": "chase_stmt_sep2024.pdf",
    "document_type": "Bank Statement",
    "classification_confidence": 0.92,
    "page_count": 3,
    "extraction_method": "OCR + Template Match + Heuristics"
  },
  "extracted_entities": {
    "institution": {
      "value": "Chase Bank",
      "provenance": "page 1, header",
      "confidence": 0.99
    },
    "account_number": {
      "value": "****1234",
      "provenance": "page 1, line 2",
      "confidence": 0.95,
      "redacted": true
    },
    "period_start": {
      "value": "2024-09-01",
      "provenance": "page 1, statement header",
      "confidence": 0.99
    },
    "period_end": {
      "value": "2024-09-30",
      "provenance": "page 1, statement header",
      "confidence": 0.99
    },
    "beginning_balance": {
      "value": 5000.00,
      "currency": "USD",
      "provenance": "page 1, opening balance line",
      "confidence": 0.98
    }
  },
  "extracted_tables": [
    {
      "table_id": "tbl_0001",
      "table_type": "Transactions",
      "rows": [
        {
          "row_id": 1,
          "date": {
            "value": "2024-09-05",
            "provenance": "page 1, row 1, col 1",
            "confidence": 0.98
          },
          "description": {
            "value": "Direct Deposit",
            "provenance": "page 1, row 1, col 2",
            "confidence": 0.99
          },
          "amount": {
            "value": 3500.00,
            "type": "deposit",
            "provenance": "page 1, row 1, col 3",
            "confidence": 0.99
          }
        }
      ]
    }
  ],
  "validation_results": {
    "status": "warnings",
    "checks": [
      {
        "check": "date_logic",
        "status": "pass",
        "message": "All transaction dates within statement period"
      },
      {
        "check": "balance_reconciliation",
        "status": "warning",
        "message": "Beginning + deposits - withdrawals = 5500 (expected 4800). Variance: $700 unexplained."
      },
      {
        "check": "outlier_detection",
        "status": "warning",
        "message": "NSF charge on 2024-09-15 ($35) — verify intent"
      }
    ]
  },
  "redaction_log": [
    {
      "field": "account_number",
      "original_chars": 16,
      "redacted_chars": 12,
      "method": "last-4-visible"
    }
  ],
  "audit_trail": {
    "created_by": "user_uuid",
    "created_at": "2024-11-10T15:30:00Z",
    "modified_at": null,
    "reviewed_by": null
  }
}
```

---

### 2. Client Profile JSON
**Purpose:** Persistent context for reuse across uploads (with consent)

```json
{
  "client_id": "client_uuid",
  "created_at": "2024-01-15T10:00:00Z",
  "last_updated": "2024-11-10T15:30:00Z",
  "consent": {
    "store_profile": true,
    "reuse_templates": true,
    "reuse_extractions": true,
    "auto_categorize": true,
    "data_retention_days": 365
  },
  "personal": {
    "name": "John Doe",
    "age": 45,
    "filing_status": "Married Filing Jointly",
    "state_of_residence": "CA",
    "dependents": [
      { "name": "Jane Doe", "age": 18, "relationship": "child", "claimed_yes_no": true }
    ]
  },
  "income": {
    "w2_income": {
      "value": 150000,
      "source": "W-2 from Acme Corp",
      "year": 2024
    },
    "self_employment": {
      "value": 25000,
      "source": "1099-NEC consulting",
      "year": 2024
    },
    "taxable_interest": 500,
    "qualified_dividends": 2000
  },
  "accounts": [
    {
      "account_id": "acc_uuid",
      "institution": "Chase Bank",
      "account_type": "Checking",
      "account_number": "****1234",
      "known_templates": [
        {
          "template_id": "tpl_001",
          "name": "Chase Personal Checking (3-month)",
          "matched_documents": 3,
          "last_match": "2024-11-10"
        }
      ]
    },
    {
      "account_id": "acc_uuid_2",
      "institution": "Vanguard",
      "account_type": "Brokerage",
      "account_number": "****5678",
      "known_templates": [
        {
          "template_id": "tpl_002",
          "name": "Vanguard Monthly Statement",
          "matched_documents": 12,
          "last_match": "2024-10-31"
        }
      ]
    }
  ],
  "known_iras": [
    {
      "account_id": "ira_uuid",
      "institution": "Fidelity",
      "type": "Traditional IRA",
      "current_balance": 250000,
      "contribution_history": [
        { "year": 2023, "amount": 6500 },
        { "year": 2024, "amount": 7000 }
      ]
    }
  ],
  "tax_preferences": {
    "filing_method": "joint",
    "standard_deduction_preference": true,
    "estimated_tax_due_dates": ["Q1", "Q2", "Q3", "Q4"]
  },
  "calculation_defaults": {
    "tax_year": 2024,
    "discount_rate": 0.05,
    "inflation_rate": 0.03,
    "state_tax_rate": 0.093
  },
  "extraction_fingerprints": [
    {
      "fingerprint": "sha256_hash_of_doc",
      "extraction_id": "ext_uuid_123",
      "date": "2024-09-15",
      "reused_on": ["2024-10-15", "2024-11-10"]
    }
  ],
  "audit_log": [
    {
      "action": "profile_created",
      "timestamp": "2024-01-15T10:00:00Z",
      "user": "client_uuid"
    },
    {
      "action": "extraction_linked",
      "timestamp": "2024-11-10T15:30:00Z",
      "extraction_id": "ext_uuid_123"
    }
  ]
}
```

---

### 3. Calculation Request Schema
**Purpose:** Standardized input for all Quantum calculations

```json
{
  "calculation_id": "calc_uuid",
  "calculation_type": "roth_conversion_optimization",
  "timestamp": "2024-11-10T15:45:00Z",
  "client_id": "client_uuid",
  "inputs": {
    "filing_status": "Married Filing Jointly",
    "current_income": {
      "w2": 150000,
      "self_employment": 25000,
      "taxable_interest": 500,
      "qualified_dividends": 2000,
      "total": 177500
    },
    "ira_balances": {
      "traditional_ira": 250000,
      "sept_ira": 0,
      "rollover_ira": 0
    },
    "proposed_conversion_amounts": [50000, 75000, 100000],
    "tax_year": 2024,
    "state": "CA"
  },
  "assumptions": {
    "federal_tax_brackets_2024": true,
    "state_tax_rate": 0.093,
    "fica_applicable": false,
    "conversion_year": 2024,
    "inflation_rate": 0.03
  },
  "calculation_steps": [
    {
      "step": 1,
      "description": "Aggregate current income",
      "formula": "W-2 + SE + Interest + Dividends",
      "result": 177500
    },
    {
      "step": 2,
      "description": "Apply pro-rata rule (Traditional + SEP + ROLLOVER IRAs)",
      "formula": "Pre-tax IRA / Total IRA × Conversion Amount",
      "result": "100% pre-tax (no basis)"
    },
    {
      "step": 3,
      "description": "Calculate taxable income + conversion",
      "formula": "177500 + Conversion Amount",
      "results": {
        "conversion_50k": 227500,
        "conversion_75k": 252500,
        "conversion_100k": 277500
      }
    },
    {
      "step": 4,
      "description": "Determine tax bracket & calculate federal tax",
      "formula": "Tax(AGI + Conversion) - Tax(AGI)",
      "results": {
        "conversion_50k": 12000,
        "conversion_75k": 18000,
        "conversion_100k": 24000
      }
    },
    {
      "step": 5,
      "description": "Add California state income tax (9.3%)",
      "formula": "Conversion × 0.093",
      "results": {
        "conversion_50k": 4650,
        "conversion_75k": 6975,
        "conversion_100k": 9300
      }
    }
  ],
  "results": {
    "scenarios": [
      {
        "scenario_name": "Conservative ($50k conversion)",
        "conversion_amount": 50000,
        "federal_tax": 12000,
        "state_tax": 4650,
        "total_tax": 16650,
        "effective_tax_rate": 0.333,
        "net_roth_contribution": 33350
      },
      {
        "scenario_name": "Moderate ($75k conversion)",
        "conversion_amount": 75000,
        "federal_tax": 18000,
        "state_tax": 6975,
        "total_tax": 24975,
        "effective_tax_rate": 0.333,
        "net_roth_contribution": 50025
      },
      {
        "scenario_name": "Aggressive ($100k conversion)",
        "conversion_amount": 100000,
        "federal_tax": 24000,
        "state_tax": 9300,
        "total_tax": 33300,
        "effective_tax_rate": 0.333,
        "net_roth_contribution": 66700
      }
    ]
  },
  "sensitivity_analysis": {
    "if_income_increases_10k": "Tax on conversion increases by $2,300 federal + $930 CA",
    "if_tax_rates_increase_1pct": "Federal tax increases by $500-1000 depending on bracket"
  },
  "audit_trail": {
    "created_by": "user_uuid",
    "created_at": "2024-11-10T15:45:00Z",
    "reviewed_by": null,
    "modified_at": null
  }
}
```

---

### 4. Calculation Output Schema
**Purpose:** Standardized output format (Markdown, JSON, CSV)

```json
{
  "calculation_result_id": "result_uuid",
  "calculation_id": "calc_uuid",
  "generated_at": "2024-11-10T16:00:00Z",
  "markdown_output": "# Roth Conversion Analysis — 2024\n\n**Client:** John Doe (MFJ, CA)\n**Year:** 2024\n\n## Inputs\n- **Current Income:** $177,500 (W-2 $150k + SE $25k + Interest $500 + Dividends $2k)\n- **Traditional IRA Balance:** $250,000 (100% pre-tax)\n- **Conversion Scenarios:** $50k, $75k, $100k\n- **Tax Year Rules:** 2024 brackets\n\n## Calculation Rules\n\n### Pro-Rata Rule (IRC §408(d)(2))\nSince you have only Traditional IRAs (no Roth basis), 100% of the conversion is taxable.\n\n### Federal Tax Brackets (2024, MFJ)\n- 24% bracket: $110,601–$189,750\n- 32% bracket: $189,751–$243,725\n\n### California State Tax\n9.3% on conversion income (CA Revenue & Taxation Code §17041)\n\n## Step-by-Step Calculation (Conservative Scenario: $50k Conversion)\n\n1. **Taxable Income Without Conversion:** $177,500\n2. **Add Roth Conversion:** $177,500 + $50,000 = $227,500\n3. **Federal Tax Impact:**\n   - Tax on $227,500 = $34,335 (estimated)\n   - Tax on $177,500 = $22,335 (estimated)\n   - **Incremental Federal Tax = $12,000**\n4. **California State Tax:**\n   - $50,000 × 9.3% = $4,650\n5. **Total Tax on Conversion = $16,650**\n\n## Results\n\n| Scenario | Conversion Amount | Federal Tax | CA Tax | Total Tax | Effective Rate | Net to Roth |\n|----------|-----------------|------------|--------|-----------|----------------|-------------|\n| Conservative | $50,000 | $12,000 | $4,650 | $16,650 | 33.3% | $33,350 |\n| Moderate | $75,000 | $18,000 | $6,975 | $24,975 | 33.3% | $50,025 |\n| Aggressive | $100,000 | $24,000 | $9,300 | $33,300 | 33.3% | $66,700 |\n\n## Sensitivity Analysis\n\nIf your W-2 income increases by $10,000 (to $160k), the tax on each conversion scenario would increase by approximately:\n- $50k conversion: +$2,400 total tax\n- $75k conversion: +$2,400 total tax\n- $100k conversion: +$2,400 total tax (same rate applies)\n\n## Assumptions & Limitations\n- Uses 2024 federal & California tax brackets\n- Assumes no extraordinary deductions beyond standard deduction\n- No FICA impact (not self-employed or already retired)\n- Multi-year conversion strategy not modeled here\n- No state reciprocity or local tax considerations\n\n## Citations\n- **Roth Conversion Rules:** IRC §408(d)(3)\n- **Pro-Rata Rule:** IRC §408(d)(2); IRS Pub 590-A\n- **2024 Tax Brackets:** IRS Pub 17\n- **California Tax:** Revenue & Taxation Code §17041\n\n**Next Steps:**\n1. Confirm income projections for 2024\n2. Determine cash source for taxes (bank account, taxable brokerage)\n3. Verify no other tax events (capital gains, AMT, ACA subsidy impact)\n4. File Form 8606 with tax return to report conversion\n",
  "json_output": {
    "summary": {
      "calculation_type": "roth_conversion_optimization",
      "client_id": "client_uuid",
      "tax_year": 2024,
      "state": "CA",
      "filing_status": "MFJ"
    },
    "inputs": {
      "current_income": 177500,
      "traditional_ira_balance": 250000,
      "scenarios": [50000, 75000, 100000]
    },
    "results": [
      {
        "scenario": "Conservative",
        "conversion": 50000,
        "federal_tax": 12000,
        "state_tax": 4650,
        "total_tax": 16650,
        "net_to_roth": 33350
      }
    ],
    "citations": [
      "IRC §408(d)(3) — Roth Conversion Rules",
      "IRC §408(d)(2) — Pro-Rata Rule",
      "IRS Pub 590-A — Traditional IRAs",
      "IRS Pub 17 — 2024 Tax Brackets"
    ]
  },
  "csv_output": "Scenario,Conversion Amount,Federal Tax,State Tax,Total Tax,Effective Rate,Net to Roth\nConservative,$50000,$12000,$4650,$16650,33.3%,$33350\nModerate,$75000,$18000,$6975,$24975,33.3%,$50025\nAggressive,$100000,$24000,$9300,$33300,33.3%,$66700",
  "audit_trail": {
    "calculation_id": "calc_uuid",
    "generated_by": "quantum_engine",
    "timestamp": "2024-11-10T16:00:00Z",
    "input_validation": "passed",
    "math_verification": "passed"
  }
}
```

---

### 5. Portfolio Aggregation Schema
**For multi-account analysis**

```json
{
  "portfolio_id": "port_uuid",
  "client_id": "client_uuid",
  "as_of_date": "2024-11-10",
  "accounts": [
    {
      "account_id": "acc_001",
      "institution": "Vanguard Brokerage",
      "balance": 500000,
      "asset_class": "Stocks (80%), Bonds (20%)",
      "cost_basis": 350000,
      "unrealized_gain": 150000,
      "annual_dividends": 5000
    },
    {
      "account_id": "acc_002",
      "institution": "Fidelity Traditional IRA",
      "balance": 250000,
      "asset_class": "Balanced Fund",
      "tax_status": "Pre-tax"
    }
  ],
  "portfolio_totals": {
    "total_balance": 750000,
    "total_cost_basis": 350000,
    "total_unrealized_gain": 150000,
    "total_annual_income": 5000
  },
  "performance_metrics": {
    "time_weighted_return_ytd": 0.082,
    "money_weighted_return_ytd": 0.075,
    "alpha": 0.015,
    "sharpe_ratio": 0.85
  }
}
```

---

## Validation & Reconciliation Rules

**Every extraction checked against:**
1. **Row/column alignment:** Totals must reconcile
2. **Date logic:** No future dates unless explicitly expected
3. **Amount logic:** Decimals correct, thousands separators consistent
4. **Cross-document:** Deposits in checking ↔ withdrawals from savings
5. **Tax reconciliation:** 1099 interest ↔ bank statement interest + reported

---

## Data Retention & Security

- **Retention:** Per client consent (default 365 days)
- **Encryption:** At rest (AES-256) & in transit (TLS 1.3)
- **Audit Trail:** Immutable, timestamped log of all access/modifications
- **Redaction:** PII masked by default (account numbers, SSN, etc.)
- **RBAC:** Role-based access (client, advisor, admin)

---

## Import/Export Formats

**Supported Imports:**
- PDF (scanned + native)
- CSV, XLSX
- JSON (extraction artifacts)
- Images (PNG, JPG)

**Supported Exports:**
- PDF (report)
- CSV (tables, waterfalls)
- JSON (full calculation artifact)
- Markdown (human-readable worksheet)
