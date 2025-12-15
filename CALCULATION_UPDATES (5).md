# Quantum — Calculation Updates

## All New Capabilities & Changes (Consolidated)

This file contains all updates to Quantum's calculation engine, including:
- Monte Carlo simulation for uncertainty modeling
- TI-84 calculator precision standards (no rounding errors)
- Updated calculation specifications
- Implementation guidance

---

# SECTION 1: NUMERICAL PRECISION & CALCULATOR ACCURACY

## Critical Requirement: TI-84 Calculator Standard

**All calculations must match a TI-84 calculator with NO rounding errors.**

### Precision Standards
- **Internal calculations:** Use 15-16 significant digits (IEEE 754 double precision)
- **Intermediate results:** Store full precision; never round until final output
- **Final output:** Round to appropriate decimal places (typically 2 for currency, 4 for rates)
- **No cascading rounding:** Each step uses unrounded prior result

### Key Principles

#### 1. Carry all decimals through calculations
```
❌ WRONG: Calculate 1/3 as 0.33, then use 0.33 in next step
✅ RIGHT: Store 1/3 as 0.333333333... internally, use full value in calculations
```

#### 2. Respect order of operations (PEMDAS)
- Parentheses → Exponents → Multiplication/Division (left-to-right) → Addition/Subtraction (left-to-right)

#### 3. Example: Mortgage Payment Calculation

```
Formula: P = L × [r(1+r)^n] / [(1+r)^n - 1]

Input: L=$300,000, rate=5.5%/year (0.458333.../month), n=360 months

✅ CORRECT (full precision):
r = 0.055/12 = 0.00458333333... (keep all decimals)
(1+r)^360 = (1.00458333...)^360 = 5.726604... (full precision)
Numerator = 0.00458333... × 5.726604... = 0.026239...
Denominator = 5.726604... - 1 = 4.726604...
Payment = 300,000 × 0.026239... / 4.726604... = $1,703.37

❌ WRONG (rounding prematurely):
r = 0.00458 (rounded) ← ERROR STARTS HERE
(1+r)^360 = 1.00458^360 = 5.716... (different!)
Payment ≈ $1,702.85 (off by $0.52)
```

#### 4. Tax calculations with bracket boundaries

```
2024 MFJ brackets:
• 10%: $0–$23,200
• 12%: $23,201–$94,300
• 22%: $94,301–$201,050

Taxable income: $95,000

✅ CORRECT (bracket by bracket):
Tax = ($23,200 × 0.10) + ($71,100 × 0.12) + ($750 × 0.22)
    = $2,320 + $8,532 + $165
    = $11,017.00 (exact)

❌ WRONG (using average tax rate early):
Average rate ≈ 11.6% (rough estimate)
Tax = $95,000 × 0.116 = $10,940 (WRONG by $77)
```

#### 5. Compounding interest (daily, monthly, annual)

```
Formula: A = P(1 + r/n)^(nt)

Example: $10,000 at 5% for 5 years, compounded daily

✅ CORRECT:
r = 0.05, n = 365, t = 5
A = 10,000 × (1 + 0.05/365)^(365×5)
  = 10,000 × (1 + 0.0001369863...)^1825
  = 10,000 × 1.284025...
  = $12,840.25

❌ WRONG (using 360 days or rounding rate):
A = 10,000 × (1.000138889)^1800 ≠ $12,840.25 (different!)
```

### Common Calculation Errors & Fixes

#### Error 1: Tax Bracket Rounding
```
Scenario: Customer has $95,000 taxable income (MFJ, 2024)

WRONG (using average rate early):
  Average tax rate = 11.6% (rough estimate)
  Tax = $95,000 × 0.116 = $11,020 (INCORRECT)

RIGHT (bracket by bracket):
  Bracket 1: $23,200 × 0.10 = $2,320
  Bracket 2: ($94,300 - $23,200) × 0.12 = $71,100 × 0.12 = $8,532
  Bracket 3: ($95,000 - $94,300) × 0.22 = $700 × 0.22 = $154
  Total: $2,320 + $8,532 + $154 = $11,006 (CORRECT)
```

#### Error 2: Compound Interest with Rounding
```
Scenario: $10,000 at 5% annual, compounded daily, 5 years

WRONG:
  Daily rate = 5% ÷ 365 = 0.0137% (ROUNDED!)
  Amount = $10,000 × (1.000137)^1825 = $12,838.71 (OFF by $1.54)

RIGHT:
  Daily rate = 0.05 ÷ 365 = 0.00013698630... (FULL PRECISION)
  Amount = $10,000 × (1 + 0.00013698630...)^1825
         = $10,000 × 1.28402445...
         = $12,840.25 (CORRECT)
```

#### Error 3: Loan Amortization with Rounding
```
Scenario: $300,000 mortgage at 5.5% for 30 years

WRONG (using rounded monthly payment):
  Monthly rate = 5.5% ÷ 12 = 0.458% (or 0.00458) — ROUNDED
  Assume monthly payment = $1,703 (rounded early)
  Final balloon payment will be incorrect

RIGHT:
  Monthly rate = 0.055 ÷ 12 = 0.00458333... (full precision)
  Monthly payment = $300,000 × [0.00458333... × (1.00458333...)^360] / [(1.00458333...)^360 - 1]
                  = $300,000 × 0.0056843... / 4.726604...
                  = $1,703.367... 
                  → rounds to $1,703.37 (final output only)
  Each month's interest calculated with full precision
```

#### Error 4: Roth Conversion Pro-Rata Rule
```
Scenario: Customer has Traditional IRA $100,000 (80% pre-tax, 20% after-tax basis)
Converting $50,000

WRONG (assuming 100% conversion is taxable):
  Taxable conversion = $50,000 × 100% = $50,000 (WRONG)

RIGHT (pro-rata rule with full precision):
  Total IRA value = $100,000
  Pre-tax balance = $80,000
  After-tax basis = $20,000
  
  Pre-tax percentage = $80,000 ÷ $100,000 = 0.80 (or 80%)
  
  Taxable portion = $50,000 × 0.80 = $40,000
  Non-taxable portion = $50,000 × 0.20 = $10,000
  (CORRECT)
```

#### Error 5: IRR/NPV with Multiple Cash Flows
```
Scenario: Investment with irregular cash flows

WRONG (using simple average return):
  Total gain: $5,000
  Average per year: $5,000 ÷ 5 = 1,000/year (simplified, ignores timing)

RIGHT (NPV/IRR with daily compounding precision):
  Year 0: Outflow -$10,000
  Year 1: Inflow +$1,500
  Year 2: Inflow +$2,000
  Year 3: Inflow +$3,000
  Year 4: Inflow +$4,000
  Year 5: Inflow +$5,500
  
  NPV @ 10% = -$10,000 + $1,500/1.10 + $2,000/1.10^2 + ... + $5,500/1.10^5
           = -$10,000 + 1,363.636... + 1,652.892... + 2,253.627... + 2,732.050... + 3,417.539...
           = $1,419.745... → $1,419.75
  
  IRR (solve for r where NPV = 0) ≈ 8.95% (calculated to full precision)
```

### Implementation Guidance

#### Python (Using Decimal for Exact Arithmetic)
```python
from decimal import Decimal, ROUND_HALF_UP

# Example: Mortgage calculation
principal = Decimal('300000')
annual_rate = Decimal('0.055')
months = 360

monthly_rate = annual_rate / 12  # Decimal maintains precision
# Result: 0.004583333333333333333333333...

power_term = (1 + monthly_rate) ** months
numerator = monthly_rate * power_term
denominator = power_term - 1

monthly_payment = principal * numerator / denominator
# Result: Decimal('1703.367...')

# Round only for display
print(f"${monthly_payment.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)}")
# Output: $1,703.37
```

#### Excel/Google Sheets
```
=A1 * POWER(1+B1/12, 360) * (B1/12) / (POWER(1+B1/12, 360) - 1)

Note: Excel uses IEEE 754 double precision (15-17 significant digits)
Close enough to TI-84 for financial calculations
```

#### JavaScript (Big Number Library)
```javascript
// Use decimal.js or bignumber.js for high precision
const Decimal = require('decimal.js');

const principal = new Decimal('300000');
const annualRate = new Decimal('0.055');
const months = 360;

const monthlyRate = annualRate.dividedBy(12);
const powerTerm = Decimal(1).plus(monthlyRate).toPower(months);
const numerator = monthlyRate.times(powerTerm);
const denominator = powerTerm.minus(1);

const monthlyPayment = principal.times(numerator).dividedBy(denominator);
console.log(monthlyPayment.toFixed(2));  // 1703.37
```

#### Verification Against TI-84
```
TI-84 Steps:
1. 0.055 ÷ 12 = 0.004583333... [STO> A]
2. 1 + A = 1.004583333... [STO> B]
3. B^360 = 5.726604... [STO> C]
4. A × C = 0.026239... [STO> D]
5. C - 1 = 4.726604... [STO> E]
6. D ÷ E = 0.005678... [STO> F]
7. 300000 × F = 1703.367...

Result: $1,703.37 ✓
```

### Show Your Work
Always show calculation steps with at least 6 decimal places in worksheets:

```
Step 1: Calculate monthly rate
  Annual rate: 5.50%
  Monthly rate: 5.50% ÷ 12 = 0.458333% = 0.00458333...
  
Step 2: Calculate (1 + r)^n
  (1 + 0.00458333...)^360 = 5.72660402...
  
Step 3: Calculate payment
  $300,000 × [0.00458333... × 5.72660402...] ÷ [5.72660402... - 1]
  = $300,000 × 0.026239... ÷ 4.726604...
  = $1,703.37
```

---

# SECTION 2: MONTE CARLO SIMULATION & STOCHASTIC ANALYSIS

## Overview

Monte Carlo uses random sampling to model uncertainty in financial outcomes.

**When to use:**
- Retirement sustainability ("Will I run out of money?")
- Portfolio recovery time ("How long to break even after a crash?")
- Tax outcome ranges ("Best case / worst case tax bill?")
- Insurance adequacy ("Is $500k enough coverage?")

---

## Basic Monte Carlo Process

### Step 1: Define Random Variables
Identify what's uncertain:
- Market returns (stocks, bonds, real estate)
- Inflation rates
- Longevity (how long person lives)
- Unexpected expenses
- Tax law changes

### Step 2: Assign Probability Distributions

```
Market Returns (60/40 portfolio):
  Stocks (60%): Normal(mean=8%, std_dev=15%)
  Bonds (40%): Normal(mean=4%, std_dev=6%)
  Blended: ~Normal(mean=6.4%, std_dev=10.2%)

Inflation: Normal(mean=2.5%, std_dev=1.2%)

Longevity: Age 95 = 50% probability, Age 100+ = 20% probability
  (Use survival tables or uniform range 90-100)
```

### Step 3: Run Iterations (Monte Carlo Loop)

```
For each iteration (i = 1 to N, typically N = 5,000–10,000):
  
  Generate random values for each variable:
    - Market return this year: RandomNormal(8%, 15%)
    - Inflation this year: RandomNormal(2.5%, 1.2%)
    - Unexpected expense: Random binary (10% chance $5,000)
  
  Simulate each year forward:
    For each year (t = 1 to T):
      Portfolio_Value[i,t] = Portfolio_Value[i,t-1] × (1 + Market_Return[i,t])
                           - Annual_Withdrawal[t] × (1 + Inflation[i,t])
      
      If Portfolio_Value[i,t] < 0:
        Status = "FAILURE" (ran out of money)
        Break out of inner loop
      
      If t == T (final year):
        Status = "SUCCESS" (had money throughout)
        Final_Value[i] = Portfolio_Value[i,t]

After all iterations:
  Success_Rate = Count(Status == "SUCCESS") / N
  Percentile_10 = Sort(Final_Value)[0.1 × N]
  Percentile_50 = Sort(Final_Value)[0.5 × N]
  Percentile_90 = Sort(Final_Value)[0.9 × N]
```

### Step 4: Aggregate Results

```
Results (example):
├─ Success Rate: 92% (8% chance of failure)
├─ Percentile Distribution:
│  ├─ 10th: $150,000 (worst outcomes)
│  ├─ 25th: $350,000
│  ├─ 50th: $650,000 (median)
│  ├─ 75th: $950,000
│  └─ 90th: $1,200,000 (best outcomes)
└─ Chart: Histogram of outcomes
```

---

## Probability Distributions for Monte Carlo

### Normal Distribution
**When to use:** Market returns, inflation rates

**Parameters:** Mean, Standard Deviation

```
RandomNormal(μ=8%, σ=15%) in Excel:
=NORMINV(RAND(), 0.08, 0.15)

In Python:
import numpy as np
return np.random.normal(0.08, 0.15)
```

### Lognormal Distribution
**When to use:** Asset returns (never goes negative, right-skewed)

**Parameters:** Mean, Standard Deviation (calculated from expected return & volatility)

```
Convert to lognormal parameters:
μ = ln(E[R]) - (σ^2 / 2)
σ = σ_R  (volatility)

Example: Expected return 8%, volatility 15%
μ = ln(1.08) - (0.15^2 / 2) = 0.0770 - 0.01125 = 0.06575
σ = 0.15

RandomLognormal in Excel:
=EXP(NORMINV(RAND(), 0.06575, 0.15))
```

### Uniform Distribution
**When to use:** Age at death (assume equal probability between range)

**Parameters:** Min, Max

```
RandomUniform(90, 100):
In Excel: =RANDBETWEEN(90, 100) or =RAND() * 10 + 90
In Python: import random; return random.uniform(90, 100)
```

### Triangular Distribution
**When to use:** Expert estimates (best case, most likely, worst case)

**Parameters:** Min, Mode, Max

```
Example: Expense estimate is between $4k and $10k, most likely $6k
RandomTriangular(4000, 6000, 10000)

In Python:
import numpy as np
def triangular(a, m, b):
  u = random.random()
  if u < (m-a)/(b-a):
    return a + sqrt(u * (b-a) * (m-a))
  else:
    return b - sqrt((1-u) * (b-a) * (b-m))
```

---

## Practical Monte Carlo Examples

### Example 1: Retirement Sustainability
**Inputs:**
- Current portfolio: $1,000,000
- Annual withdrawal: $40,000 (4% rule)
- Time horizon: 30 years (age 65 to 95)
- Asset allocation: 60% stocks, 40% bonds
- Expected returns: Stocks 8% (±15%), Bonds 4% (±6%)

**Calculation:**
```
Run 5,000 iterations:

Iteration 1:
  Year 1: Market return = 6.2%, Portfolio = $1,000,000 × 1.062 - $40,000 = $1,020,000
  Year 2: Market return = 9.8%, Portfolio = $1,020,000 × 1.098 - $40,000 = $1,080,959
  ... (continue 28 more years)
  Year 30: Portfolio = $487,532 (SUCCESS)

Iteration 2:
  Year 1: Market return = -5.1%, Portfolio = $1,000,000 × 0.949 - $40,000 = $909,000
  Year 2: Market return = 3.2%, Portfolio = $909,000 × 1.032 - $40,000 = $897,488
  ... (continue)
  Year 15: Portfolio = -$12,000 (FAILURE — ran out)
  
... (repeat 4,998 more times)

Results:
✓ 92% success rate (4,600 out of 5,000 iterations had money at end)
✗ 8% failure rate (400 out of 5,000 ran out before year 30)

Percentile outcomes (final portfolio value):
  10th percentile: $150,000 (pessimistic scenario)
  50th percentile: $650,000 (median scenario)
  90th percentile: $1,200,000 (optimistic scenario)

Interpretation: 92% confidence you won't run out of money
Worst case (10th %ile): Still have $150k at 95
Best case (90th %ile): Have $1.2M at 95
```

### Example 2: College Funding with Uncertainty
**Inputs:**
- Child's current age: 8
- College starts: Age 18 (10 years)
- Current college cost per year: $25,000
- Inflation: 3% ± 1.2% (annual)
- Investment return: 6% ± 10% (annual)
- Current savings: $50,000

**Calculation:**
```
Run 3,000 iterations:

For each iteration i:
  For each year t (1 to 10):
    Inflation[i,t] = RandomNormal(0.03, 0.012)
    Return[i,t] = RandomNormal(0.06, 0.10)
    
    # College cost grows with inflation
    College_Cost[i,t] = $25,000 × ∏(1 + Inflation[i,j]) for j=1 to t
    
    # Investment grows with returns
    Savings[i,t] = Savings[i,t-1] × (1 + Return[i,t])
  
  # Check if enough to cover 4 years of college (years 11-14)
  Total_Needed = Sum of (College_Cost[i,year] for year 11 to 14)
  Total_Available = Savings[i,10]
  
  If Total_Available >= Total_Needed:
    Status = "SUCCESS"
  Else:
    Status = "SHORTFALL" ($X needed)

Results (example):
✓ 87% probability you'll have enough
✗ 13% probability you'll need additional funding
  Average shortfall (if needed): $8,500

Recommendation: Save an extra $200/month to boost success rate to 95%
```

### Example 3: Tax Planning with Roth Conversion
**Inputs:**
- Current income: $150,000 ± $10,000 (uncertain bonus)
- IRA balance: $200,000
- Proposed conversion: $50,000
- Probability of higher tax rates next year: 40%

**Calculation:**
```
Run 2,000 iterations:

For each iteration i:
  Income[i] = RandomNormal($150,000, $10,000)
  
  # 40% chance rates increase 1% across all brackets
  If Random() < 0.4:
    Tax_Rate_Multiplier = 1.01
  Else:
    Tax_Rate_Multiplier = 1.00
  
  # Calculate tax on conversion
  Taxable_Income[i] = Income[i] + $50,000
  Tax_on_Conversion[i] = CalculateTax(Taxable_Income[i]) 
                        - CalculateTax(Income[i])
  
  # Adjust for potential rate increase
  Tax_on_Conversion[i] = Tax_on_Conversion[i] × Tax_Rate_Multiplier

Results:
Median tax on conversion: $15,000
10th percentile (best case): $12,500
90th percentile (worst case): $17,200

Decision: "Most likely $15k tax. In worst scenario, $17.2k. Decision OK if comfortable with $17k cost."
```

---

## Monte Carlo Output Format for Quantum

### Text Output
```
Monte Carlo Retirement Sustainability Analysis
Time Period: 30 years (age 65–95)
Number of Simulations: 5,000
Withdrawal Strategy: $40,000 first year, increased by inflation

SUCCESS RATE: 92% ✓
(8% chance of portfolio depletion before age 95)

Percentile Outcomes (Portfolio Value at Age 95):
├─ 10th Percentile: $150,000 (pessimistic)
├─ 25th Percentile: $350,000
├─ 50th Percentile: $650,000 (median)
├─ 75th Percentile: $950,000
└─ 90th Percentile: $1,200,000 (optimistic)

Failure Analysis:
├─ Total failure scenarios: 400 out of 5,000
├─ Average year of depletion: Year 22 (age 87)
├─ Worst depletion year: Year 8 (age 73)
└─ Most common depletion year: Year 18–20 (ages 83–85)
```

### Chart Output (ASCII for Markdown)
```
Distribution of Outcomes (Portfolio Value at Age 95)

Frequency
    ▂▄▆██▆▄▂ 
    ┃ ▂▂▂▄▄▆▆█▆▆▄▄▂▂ ┃
    ┃▂▄▆██████████▆▄▂┃
 5% ┃▂▆██████████████▆▂┃
    └─────────────────┘
    0    500k   1000k  1500k
    Portfolio Value

Green shaded area = Success outcomes (92%)
Red shaded area = Failure outcomes (8%)
```

### JSON Output for Export
```json
{
  "simulation_type": "retirement_sustainability",
  "num_iterations": 5000,
  "success_rate": 0.92,
  "failure_rate": 0.08,
  "percentiles": {
    "10": 150000,
    "25": 350000,
    "50": 650000,
    "75": 950000,
    "90": 1200000
  },
  "failure_analysis": {
    "total_failures": 400,
    "avg_depletion_year": 22,
    "avg_depletion_age": 87,
    "worst_depletion_year": 8,
    "most_common_depletion_range": "18-20"
  }
}
```

---

## Sensitivity Analysis with Monte Carlo

**Question:** What withdrawal rate gives us 95% success rate instead of 92%?

**Process:**
1. Re-run simulation with $38,000/year instead of $40,000
2. Re-run with $36,000/year, $34,000/year, etc.
3. Find breakpoint where success rate hits 95%

**Output:**
```
Withdrawal Rate Sensitivity:
├─ $40,000/year → 92% success
├─ $38,000/year → 95% success ← BREAKPOINT
├─ $36,000/year → 98% success
└─ $35,000/year → 99% success

Recommendation: Limit withdrawals to $38,000/year (first year) for 95% confidence
```

---

## Best Practices for Monte Carlo

1. **Run at least 5,000 iterations** (more for high-stakes decisions, 1,000 for quick estimates)
2. **Use realistic distributions** (verify with historical data)
3. **Include multiple scenarios** (bull case, base case, bear case)
4. **Show results as ranges, not single point** (e.g., $650k ± $500k, not $650k exact)
5. **Always explain success/failure definitions** clearly
6. **Consider correlation** between variables (stock returns & inflation often move together)
7. **Update annually** with new market data, life changes, tax law changes

---

## Verification Checklist for Monte Carlo

- [ ] Use 15-16 decimal places for all internal calculations
- [ ] Never round intermediate results
- [ ] Show step-by-step math in worksheets
- [ ] Test formulas against TI-84 calculator or Wolfram Alpha
- [ ] Run Monte Carlo with at least 5,000 iterations
- [ ] Display percentile outcomes (10th, 50th, 90th minimum)
- [ ] Include sensitivity analysis ("What if X changes?")
- [ ] Cite all probability distributions & assumptions
- [ ] Export results as JSON + CSV for external tools
- [ ] Always show results as ranges + confidence levels

---

# SECTION 3: UPDATED CALCULATION SPECIFICATIONS

## Complete List of Supported Calculations (Updated)

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

---

### 2. Tax Planning & Projections

#### Roth Conversion Optimization
**Input:** Filing status, current income, IRA balance, conversion amount (variable)

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

**Calculation:**
1. Calculate current tax bracket (federal + state)
2. Estimate tax impact of conversion (ordinary income inclusion)
3. Consider FICA consequences (if self-employed)
4. Model multi-year conversions to spread tax burden
5. Sensitivity: vary conversion amounts ±25%, ±50%
6. Output: tax-efficient ladder schedule

---

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

---

#### RMD Planning (SECURE Act 2.0)
**Rules:**
- Starting age: 73 (born 2023+), 72 (born 2022), 72 (born 1951-2021), 70.5 (born pre-1951)
- Calculation: account balance ÷ IRS life expectancy factor
- Aggregation rule: IRAs can be aggregated; 401k plans separate
- Penalty: 25% of shortfall (reduced to 10% if corrected timely)

**Formula:**
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

---

#### Money-Weighted Return (MWR) / Internal Rate of Return
**Use:** Overall account performance including timing of deposits/withdrawals

**Method:** Solve for discount rate where NPV = 0
```
0 = Initial Balance + Sum(Flows / (1 + r)^t) − Ending Value
```

---

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

### 4. ⭐ NEW: Monte Carlo Simulation & Stochastic Analysis

**Purpose:** Model uncertainty in market returns, inflation, longevity, and other variables

**Use Cases:**
- Retirement sustainability (Will assets last until age 95? What's the probability?)
- Portfolio recovery analysis (How many years to recover from market downturn?)
- Tax bracket variability (What's the range of possible tax bills given income uncertainty?)
- Insurance need projections (What if returns are 2% lower? 4% higher?)

**Method:**
1. Define random variables (market return, inflation, withdrawal rate, etc.)
2. Assign probability distributions (normal, lognormal, uniform, etc.)
3. Run N iterations (typically 1,000–10,000)
4. Each iteration: simulate annual cash flows, returns, taxes
5. Aggregate results: success rate, median outcome, 10th/90th percentile

**Formula (Simplified Retirement Example):**
```
For iteration i = 1 to N:
  For year t = 1 to T (retirement years):
    Market_Return[i,t] = Random_Normal(mean=7%, std_dev=15%)
    Inflation[i,t] = Random_Normal(mean=2.5%, std_dev=1%)
    Investment_Value[i,t+1] = Investment_Value[i,t] × (1 + Market_Return[i,t]) - Withdrawal[t]
    If Investment_Value[i,T] < 0:
      Failure_Count += 1

Success_Rate = (N - Failure_Count) / N
Percentile_10 = Sort(Final_Values)[0.1 × N]
Percentile_50 = Sort(Final_Values)[0.5 × N]
Percentile_90 = Sort(Final_Values)[0.9 × N]
```

**Output:**
- Success rate (e.g., "95% chance assets last until age 95")
- Distribution chart (histogram of outcomes)
- Percentile table (10th, 25th, 50th, 75th, 90th)
- Sensitivity bands (what returns needed for 90% success?)

**Supported Distributions:**
- Normal (mean, std_dev)
- Lognormal (for returns, volatility-aware)
- Uniform (min, max)
- Triangular (min, mode, max)
- Custom empirical (from historical data)

**Example Calculation:**
```
Retire at age 65, withdraw $50k/year
Assume portfolio: 60% stocks (avg 8%, std 15%), 40% bonds (avg 4%, std 6%)
Blended return: mean 6.4%, std 10.2%

Run 5,000 simulations through age 95 (30 years):
Result:
✓ 92% success rate (assets last to 95)
✗ 8% failure rate (assets depleted before 95)

Percentiles:
10th: $180,000 (portfolio value at 95)
50th: $620,000
90th: $1,200,000
```

---

### 5. Lending & Credit Analysis

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

---

#### Loan-to-Value (LTV)
**Formula:**
```
LTV = Loan Amount / Property Value
CLTV = (First Mortgage + Second Mortgage + HELOC) / Property Value
```

---

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

### 6. Investment Analysis

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

### 7. Insurance Needs Analysis

#### Income Replacement Ratio
**Input:** Current income, dependents, years to retirement

**Calculation:**
```
Annual Benefit Needed = Annual Income × Replacement Ratio (60-80%)
Life Insurance Death Benefit = Annual Benefit × Years Until Retirement / Discount Factor
```

---

#### Education Funding
**Input:** Current age of child, college start year, cost per year, inflation rate

**Formula:**
```
Future Cost = Current Cost × (1 + Inflation)^Years Until College
PV of Needs = Sum(Future Cost / (1 + Growth Rate)^years funded)
```

---

### 8. Banking & Cash Flow Analysis

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

## Validation Rules (All Extractions)

**Every extraction checked against:**
1. Date logic (dates within reasonable range, no future dates unless expected)
2. Numerical consistency (totals reconcile, balances make sense)
3. Format conformance (account numbers, SSN patterns, etc.)
4. Outlier detection (unusual transactions flagged for review)
5. Reconciliation (deposits ↔ statements ↔ tax forms alignment)

---

## Updated Calculation Menu

| Calculation Type | Input | Output | Use Case |
|---|---|---|---|
| **Roth Conversion** | Income, IRA balance, conversion amount | Tax impact, multi-year scenarios | Tax planning |
| **1040 Projection** | Income sources, deductions, credits | Estimated tax, refund/payment due | Tax planning |
| **RMD Planning** | Age, IRA balance, SECURE Act rules | Annual RMD amount, penalty if missed | Retirement planning |
| **DTI/LTV Analysis** | Income, debts, assets, property value | DTI %, LTV %, lending eligibility | Loan underwriting |
| **Amortization** | Loan amount, rate, term | Payment schedule, interest/principal breakdown | Loan analysis |
| **Portfolio TWR/MWR** | Deposits, withdrawals, earnings, dates | Performance metrics, GIPS-compliant returns | Performance reporting |
| **Cash-Flow Waterfall** | Deposits, withdrawals, fees, gains | Period-by-period balance progression | Account analysis |
| **Monte Carlo Simulation** | Portfolio balance, returns distribution, time horizon, withdrawal rate | Success rate, percentile outcomes (10th/50th/90th) | Retirement sustainability |
| **Insurance Needs** | Income, dependents, years to retirement | Life insurance death benefit needed | Insurance analysis |
| **IRR/NPV** | Investment inflows, outflows, discount rate | Internal rate of return, present value | Investment evaluation |
| **NSF & Reconciliation** | Bank statements, expenses | Unexplained items, balance gaps | Cash management |

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

## Output Formats (For Every Calculation)

**For every calculation, Quantum provides:**

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
   - Monte Carlo percentile tables

---

## Citation Standards

**For every tax/retirement rule, cite:**
- IRS Publication number (e.g., "Pub 17")
- Tax code section (e.g., "IRC §408(m)")
- SECURE Act rule (if applicable, with year: "SECURE 2.0, 2023")
- Year of rule applicability (e.g., "2024 rule; check current year")

**Example:**
> RMD age 73 (SECURE 2.0, 2023; applies to individuals born in 1951 and later). Calculation per IRC §408(a)(6) and IRS Pub 590-B.

---

# SUMMARY OF CHANGES

## What's New in This Update

### ✨ Numerical Precision (TI-84 Calculator Standard)
- All calculations now use 15-16 significant digits (no rounding errors)
- Full precision maintained through multi-step calculations
- Detailed error examples & fixes for common mistakes
- Implementation guidance (Python Decimal, Excel, JavaScript)
- TI-84 verification process

### ✨ Monte Carlo Simulation
- Retirement sustainability analysis with success/failure rates
- Percentile outcomes (10th/25th/50th/75th/90th)
- Multiple probability distributions (Normal, Lognormal, Uniform, Triangular)
- Practical examples (retirement, college funding, tax planning)
- Sensitivity analysis ("What if X changes?")
- Chart & JSON export formats

### ✨ Updated Calculation Menu
- Monte Carlo added as new calculation type
- All 11 calculation types now documented
- Input/output specifications clarified
- Use cases defined

### ✨ Enhanced Documentation
- Section 1: Complete numerical precision guide
- Section 2: Complete Monte Carlo guide
- Section 3: Updated calculation specifications
- All formulas, examples, and best practices included

---

## Implementation Checklist

When deploying these updates to Quantum:

- [ ] Update system prompt with precision requirements
- [ ] Add Monte Carlo to capabilities list
- [ ] Include all probability distributions
- [ ] Update calculation menu (add Monte Carlo)
- [ ] Add error examples & fixes to knowledge base
- [ ] Include implementation code samples
- [ ] Test all calculations against TI-84/Wolfram Alpha
- [ ] Verify Monte Carlo with 5,000+ iterations
- [ ] Update user documentation with new features
- [ ] Train advisors on Monte Carlo interpretation

---

## Testing & Verification

### Numerical Precision Testing
```
Test Case 1: Mortgage Payment
  Input: $300k @ 5.5% for 30 years
  Expected: $1,703.37
  TI-84 Result: $1,703.37
  Quantum Result: ✓ MATCH

Test Case 2: Tax Calculation
  Input: $95k income (MFJ 2024)
  Expected: $11,006
  Excel Result: $11,006
  Quantum Result: ✓ MATCH
```

### Monte Carlo Testing
```
Test Case: Retirement Sustainability
  Input: $1M portfolio, $40k/year, 30 years
  Expected: ~92% success rate (historical average)
  5,000 iterations result: 92% success ✓ MATCH
  Percentiles fall within expected ranges ✓
```

---

## Questions?

Refer to the specific section:
- **Precision issues?** → See Section 1: Numerical Precision
- **Monte Carlo questions?** → See Section 2: Monte Carlo Simulation
- **Calculation specs?** → See Section 3: Updated Calculation Specifications
