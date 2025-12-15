"""
╔═══════════════════════════════════════════════════════════════════════╗
║                                                                       ║
║              QUANTUM FIVE-BUCKET PORTFOLIO BUILDER                    ║
║              Slide 29 - Complete Instructions for GPT                 ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝

INSTRUCTIONS FOR GPT: HOW TO BUILD SLIDE 29 - FIVE-BUCKET PORTFOLIO DESIGN

This code teaches Quantum EXACTLY how to:
1. Design a modern five-bucket portfolio strategy
2. Assign assets to appropriate buckets based on purpose
3. Calculate weighted average portfolio returns
4. Explain why five buckets beats 60/40 or three-bucket systems
5. Build the visual presentation for clients

PURPOSE OF SLIDE 29:
Present the client's portfolio structure using a modern five-bucket strategy 
designed to improve diversification, clarify purpose, and replace outdated 
systems like traditional 60/40 or three-bucket approaches.

OFFICIAL NJM RETURN ASSUMPTIONS:
- Bucket 1 (Preserve): 7%
- Bucket 2 (Provide - Income): 11%
- Bucket 3 (Provide - Flexible Income): 15%
- Bucket 4 (Performance): 15%
- Bucket 5 (Cash): 2%

"""

from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
from enum import Enum


# ═══════════════════════════════════════════════════════════════════════════
# BUCKET DEFINITIONS
# ═══════════════════════════════════════════════════════════════════════════

class BucketType(Enum):
    """Five bucket types in order from safest to most aggressive"""
    BUCKET_1_PRESERVE = "preserve"
    BUCKET_2_PROVIDE_INCOME = "provide_income"
    BUCKET_3_PROVIDE_FLEXIBLE = "provide_flexible"
    BUCKET_4_PERFORMANCE = "performance"
    BUCKET_5_CASH = "cash"


# Official NJM Expected Return Assumptions
BUCKET_EXPECTED_RETURNS = {
    BucketType.BUCKET_1_PRESERVE: 0.07,         # 7%
    BucketType.BUCKET_2_PROVIDE_INCOME: 0.11,   # 11%
    BucketType.BUCKET_3_PROVIDE_FLEXIBLE: 0.15, # 15%
    BucketType.BUCKET_4_PERFORMANCE: 0.15,      # 15%
    BucketType.BUCKET_5_CASH: 0.02              # 2%
}


@dataclass
class BucketDefinition:
    """
    Complete definition of each bucket in the five-bucket system
    """
    bucket_type: BucketType
    name: str
    purpose: str
    risk_level: str
    typical_holdings: List[str]
    role_in_planning: str
    expected_return: float
    time_horizon: str


# Complete Five-Bucket System Definition
FIVE_BUCKET_SYSTEM = {
    BucketType.BUCKET_1_PRESERVE: BucketDefinition(
        bucket_type=BucketType.BUCKET_1_PRESERVE,
        name="Bucket 1 - Preserve",
        purpose="Protect principal",
        risk_level="Lowest (other than cash) - Super Conservative",
        typical_holdings=[
            "Fixed index annuities (FIAs)",
            "Multi-Year Guaranteed Annuities (MYGAs)",
            "Protected income sources",
            "CD alternatives",
            "Principal-protected vehicles"
        ],
        role_in_planning=(
            "Provides stability, protects against market downturns, "
            "supports longevity risk management"
        ),
        expected_return=BUCKET_EXPECTED_RETURNS[BucketType.BUCKET_1_PRESERVE],
        time_horizon="Long-term stability"
    ),
    
    BucketType.BUCKET_2_PROVIDE_INCOME: BucketDefinition(
        bucket_type=BucketType.BUCKET_2_PROVIDE_INCOME,
        name="Bucket 2 - Provide (Stable Income)",
        purpose="Income generation",
        risk_level="Low to Moderate Risk",
        typical_holdings=[
            "Conservative dividend equities",
            "Buffered ETFs",
            "Fixed income alternatives",
            "Covered call strategies",
            "High-quality bonds"
        ],
        role_in_planning=(
            "Generates income, supports partial Roth conversion tax payments, "
            "provides COLA support"
        ),
        expected_return=BUCKET_EXPECTED_RETURNS[BucketType.BUCKET_2_PROVIDE_INCOME],
        time_horizon="Intermediate (3-10 years)"
    ),
    
    BucketType.BUCKET_3_PROVIDE_FLEXIBLE: BucketDefinition(
        bucket_type=BucketType.BUCKET_3_PROVIDE_FLEXIBLE,
        name="Bucket 3 - Provide (Flexible Income)",
        purpose="Fill income gaps + support Roth conversion costs",
        risk_level="Moderate Risk",
        typical_holdings=[
            "Balanced strategies",
            "Defensive equities",
            "Alternative income solutions",
            "Tactical allocation funds",
            "Multi-asset strategies"
        ],
        role_in_planning=(
            "Supports liquidity for tax strategies, fills income gaps, "
            "provides flexible access"
        ),
        expected_return=BUCKET_EXPECTED_RETURNS[BucketType.BUCKET_3_PROVIDE_FLEXIBLE],
        time_horizon="Intermediate (5-15 years)"
    ),
    
    BucketType.BUCKET_4_PERFORMANCE: BucketDefinition(
        bucket_type=BucketType.BUCKET_4_PERFORMANCE,
        name="Bucket 4 - Performance",
        purpose="Long-term growth and performance",
        risk_level="Higher Risk",
        typical_holdings=[
            "Equities",
            "Growth funds",
            "Alternatives",
            "Thematic portfolios",
            "Managed equity portfolios",
            "High beta sectors",
            "International growth"
        ],
        role_in_planning=(
            "Drives long-term return potential, offsets inflation over decades, "
            "maximizes growth for future needs"
        ),
        expected_return=BUCKET_EXPECTED_RETURNS[BucketType.BUCKET_4_PERFORMANCE],
        time_horizon="Long-term (10+ years)"
    ),
    
    BucketType.BUCKET_5_CASH: BucketDefinition(
        bucket_type=BucketType.BUCKET_5_CASH,
        name="Bucket 5 - Cash",
        purpose="Immediate liquidity",
        risk_level="No Market Risk",
        typical_holdings=[
            "Cash",
            "Money market funds",
            "Treasury bills",
            "Ultra-short duration bonds"
        ],
        role_in_planning=(
            "Emergency use, short-term expenses, short-term opportunities, "
            "tactical positioning"
        ),
        expected_return=BUCKET_EXPECTED_RETURNS[BucketType.BUCKET_5_CASH],
        time_horizon="Short-term (0-1 year)"
    )
}


# ═══════════════════════════════════════════════════════════════════════════
# CLIENT PORTFOLIO STRUCTURE
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class ClientPortfolio:
    """
    Client's complete portfolio with five-bucket allocation
    """
    client_name: str
    total_portfolio_value: float
    
    # Bucket allocations (as decimals, e.g., 0.25 = 25%)
    bucket_1_allocation: float  # Preserve
    bucket_2_allocation: float  # Provide - Income
    bucket_3_allocation: float  # Provide - Flexible
    bucket_4_allocation: float  # Performance
    bucket_5_allocation: float  # Cash
    
    # Optional: Specific dollar amounts (calculated if not provided)
    bucket_1_amount: Optional[float] = None
    bucket_2_amount: Optional[float] = None
    bucket_3_amount: Optional[float] = None
    bucket_4_amount: Optional[float] = None
    bucket_5_amount: Optional[float] = None
    
    # Client planning factors
    annual_income_need: Optional[float] = None
    roth_conversion_annual_cost: Optional[float] = None
    risk_tolerance: str = "moderate"
    time_horizon_years: int = 20
    
    def __post_init__(self):
        """Calculate dollar amounts and validate allocations"""
        # Validate allocations sum to 100%
        total_allocation = (
            self.bucket_1_allocation +
            self.bucket_2_allocation +
            self.bucket_3_allocation +
            self.bucket_4_allocation +
            self.bucket_5_allocation
        )
        
        if abs(total_allocation - 1.0) > 0.001:  # Allow small rounding errors
            raise ValueError(
                f"Bucket allocations must sum to 100%. Current sum: {total_allocation*100:.1f}%"
            )
        
        # Calculate dollar amounts if not provided
        if self.bucket_1_amount is None:
            self.bucket_1_amount = self.total_portfolio_value * self.bucket_1_allocation
        if self.bucket_2_amount is None:
            self.bucket_2_amount = self.total_portfolio_value * self.bucket_2_allocation
        if self.bucket_3_amount is None:
            self.bucket_3_amount = self.total_portfolio_value * self.bucket_3_allocation
        if self.bucket_4_amount is None:
            self.bucket_4_amount = self.total_portfolio_value * self.bucket_4_allocation
        if self.bucket_5_amount is None:
            self.bucket_5_amount = self.total_portfolio_value * self.bucket_5_allocation


# ═══════════════════════════════════════════════════════════════════════════
# PORTFOLIO RETURN CALCULATOR
# ═══════════════════════════════════════════════════════════════════════════

class PortfolioReturnCalculator:
    """
    Calculate weighted average returns and project portfolio growth
    """
    
    @staticmethod
    def calculate_weighted_return(portfolio: ClientPortfolio) -> float:
        """
        Calculate weighted average expected return across all buckets
        
        Formula: Σ(Bucket Weight × Bucket Expected Return)
        
        Example:
        Bucket 1: 25% × 7% = 1.75%
        Bucket 2: 20% × 11% = 2.20%
        Bucket 3: 20% × 15% = 3.00%
        Bucket 4: 30% × 15% = 4.50%
        Bucket 5: 5% × 2% = 0.10%
        Total: 11.55%
        """
        weighted_return = (
            portfolio.bucket_1_allocation * BUCKET_EXPECTED_RETURNS[BucketType.BUCKET_1_PRESERVE] +
            portfolio.bucket_2_allocation * BUCKET_EXPECTED_RETURNS[BucketType.BUCKET_2_PROVIDE_INCOME] +
            portfolio.bucket_3_allocation * BUCKET_EXPECTED_RETURNS[BucketType.BUCKET_3_PROVIDE_FLEXIBLE] +
            portfolio.bucket_4_allocation * BUCKET_EXPECTED_RETURNS[BucketType.BUCKET_4_PERFORMANCE] +
            portfolio.bucket_5_allocation * BUCKET_EXPECTED_RETURNS[BucketType.BUCKET_5_CASH]
        )
        
        return weighted_return
    
    @staticmethod
    def calculate_bucket_contributions(portfolio: ClientPortfolio) -> Dict[str, float]:
        """
        Calculate how much each bucket contributes to total return
        
        Returns dictionary with contribution percentages
        """
        contributions = {
            'Bucket 1 (Preserve)': portfolio.bucket_1_allocation * BUCKET_EXPECTED_RETURNS[BucketType.BUCKET_1_PRESERVE],
            'Bucket 2 (Provide - Income)': portfolio.bucket_2_allocation * BUCKET_EXPECTED_RETURNS[BucketType.BUCKET_2_PROVIDE_INCOME],
            'Bucket 3 (Provide - Flexible)': portfolio.bucket_3_allocation * BUCKET_EXPECTED_RETURNS[BucketType.BUCKET_3_PROVIDE_FLEXIBLE],
            'Bucket 4 (Performance)': portfolio.bucket_4_allocation * BUCKET_EXPECTED_RETURNS[BucketType.BUCKET_4_PERFORMANCE],
            'Bucket 5 (Cash)': portfolio.bucket_5_allocation * BUCKET_EXPECTED_RETURNS[BucketType.BUCKET_5_CASH]
        }
        
        return contributions
    
    @staticmethod
    def project_portfolio_growth(
        portfolio: ClientPortfolio,
        years: int
    ) -> List[Dict[str, float]]:
        """
        Project portfolio growth over time with each bucket growing at its rate
        
        Returns year-by-year projections
        """
        projections = []
        
        # Starting values
        current_values = {
            'bucket_1': portfolio.bucket_1_amount,
            'bucket_2': portfolio.bucket_2_amount,
            'bucket_3': portfolio.bucket_3_amount,
            'bucket_4': portfolio.bucket_4_amount,
            'bucket_5': portfolio.bucket_5_amount
        }
        
        for year in range(1, years + 1):
            # Grow each bucket at its expected rate
            current_values['bucket_1'] *= (1 + BUCKET_EXPECTED_RETURNS[BucketType.BUCKET_1_PRESERVE])
            current_values['bucket_2'] *= (1 + BUCKET_EXPECTED_RETURNS[BucketType.BUCKET_2_PROVIDE_INCOME])
            current_values['bucket_3'] *= (1 + BUCKET_EXPECTED_RETURNS[BucketType.BUCKET_3_PROVIDE_FLEXIBLE])
            current_values['bucket_4'] *= (1 + BUCKET_EXPECTED_RETURNS[BucketType.BUCKET_4_PERFORMANCE])
            current_values['bucket_5'] *= (1 + BUCKET_EXPECTED_RETURNS[BucketType.BUCKET_5_CASH])
            
            total_value = sum(current_values.values())
            
            projections.append({
                'year': year,
                'bucket_1': current_values['bucket_1'],
                'bucket_2': current_values['bucket_2'],
                'bucket_3': current_values['bucket_3'],
                'bucket_4': current_values['bucket_4'],
                'bucket_5': current_values['bucket_5'],
                'total_portfolio': total_value
            })
        
        return projections
    
    @staticmethod
    def compare_to_60_40(portfolio: ClientPortfolio) -> Dict[str, float]:
        """
        Compare five-bucket strategy to traditional 60/40 portfolio
        
        Traditional 60/40 assumption: 8% average return
        """
        five_bucket_return = PortfolioReturnCalculator.calculate_weighted_return(portfolio)
        traditional_60_40_return = 0.08  # 8% assumed for 60/40
        
        return {
            'five_bucket_return': five_bucket_return,
            'traditional_60_40_return': traditional_60_40_return,
            'difference': five_bucket_return - traditional_60_40_return,
            'outperformance_percentage': ((five_bucket_return / traditional_60_40_return) - 1) * 100
        }


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 29 BUILDER
# ═══════════════════════════════════════════════════════════════════════════

class Slide29Builder:
    """
    COMPLETE INSTRUCTIONS FOR BUILDING SLIDE 29
    
    This class contains the EXACT structure and content for Slide 29
    """
    
    @staticmethod
    def build_slide_29_instructions(portfolio: ClientPortfolio) -> Dict[str, any]:
        """
        Generate complete instructions for building Slide 29
        
        Returns structured data that Quantum uses to build the slide
        """
        
        calculator = PortfolioReturnCalculator()
        
        # Calculate returns
        weighted_return = calculator.calculate_weighted_return(portfolio)
        bucket_contributions = calculator.calculate_bucket_contributions(portfolio)
        comparison_60_40 = calculator.compare_to_60_40(portfolio)
        
        # Build slide structure
        slide_data = {
            'slide_number': 29,
            'slide_title': f'Five-Bucket Portfolio Design - {portfolio.client_name}',
            'slide_type': 'five_bucket_portfolio',
            
            # SECTION 1: Introduction / Why Five Buckets
            'introduction': {
                'title': 'Modern Five-Bucket Strategy',
                'why_five_buckets': [
                    "Replaces outdated 60/40 portfolios (increasingly ineffective in volatile or rising-rate environments)",
                    "Improves on three-bucket systems (too broad, not specific enough)",
                    "Gives each asset type a specific purpose and time horizon",
                    "Keeps structure simple and intuitive for clients",
                    "Provides flexibility and clarity traditional models lack"
                ],
                'layout': 'bullet_points'
            },
            
            # SECTION 2: The Five Buckets (Left to Right)
            'bucket_structure': {
                'title': 'Your Five-Bucket Portfolio Structure',
                'subtitle': 'From Safest (Left) to Most Aggressive (Right)',
                'buckets': Slide29Builder._format_bucket_details(portfolio),
                'layout': 'five_column_layout'
            },
            
            # SECTION 3: Portfolio Allocation Summary
            'allocation_summary': {
                'title': 'Your Portfolio Allocation',
                'data': {
                    'Bucket 1 (Preserve)': {
                        'percentage': f'{portfolio.bucket_1_allocation * 100:.1f}%',
                        'amount': f'${portfolio.bucket_1_amount:,.0f}',
                        'return': '7%'
                    },
                    'Bucket 2 (Provide - Income)': {
                        'percentage': f'{portfolio.bucket_2_allocation * 100:.1f}%',
                        'amount': f'${portfolio.bucket_2_amount:,.0f}',
                        'return': '11%'
                    },
                    'Bucket 3 (Provide - Flexible)': {
                        'percentage': f'{portfolio.bucket_3_allocation * 100:.1f}%',
                        'amount': f'${portfolio.bucket_3_amount:,.0f}',
                        'return': '15%'
                    },
                    'Bucket 4 (Performance)': {
                        'percentage': f'{portfolio.bucket_4_allocation * 100:.1f}%',
                        'amount': f'${portfolio.bucket_4_amount:,.0f}',
                        'return': '15%'
                    },
                    'Bucket 5 (Cash)': {
                        'percentage': f'{portfolio.bucket_5_allocation * 100:.1f}%',
                        'amount': f'${portfolio.bucket_5_amount:,.0f}',
                        'return': '2%'
                    },
                    'Total Portfolio': {
                        'percentage': '100%',
                        'amount': f'${portfolio.total_portfolio_value:,.0f}',
                        'return': f'{weighted_return * 100:.2f}%'
                    }
                },
                'layout': 'allocation_table'
            },
            
            # SECTION 4: Weighted Average Return Calculation
            'return_calculation': {
                'title': 'Blended Expected Portfolio Return',
                'formula': 'Weighted Average Return = Σ(Bucket Weight × Bucket Expected Return)',
                'calculation_breakdown': Slide29Builder._format_return_calculation(portfolio, bucket_contributions),
                'weighted_return': f'{weighted_return * 100:.2f}%',
                'layout': 'calculation_display'
            },
            
            # SECTION 5: Comparison to Traditional Strategies
            'comparison': {
                'title': 'Five-Bucket Strategy vs. Traditional 60/40',
                'data': {
                    'Your Five-Bucket Strategy': f'{weighted_return * 100:.2f}%',
                    'Traditional 60/40 Portfolio': f'{comparison_60_40["traditional_60_40_return"] * 100:.2f}%',
                    'Difference': f'{comparison_60_40["difference"] * 100:+.2f}%',
                    'Outperformance': f'{comparison_60_40["outperformance_percentage"]:+.1f}%'
                },
                'insight': Slide29Builder._generate_comparison_insight(comparison_60_40),
                'layout': 'comparison_chart'
            },
            
            # SECTION 6: How This Supports Your Plan
            'plan_integration': Slide29Builder._generate_plan_integration(portfolio),
            
            # SECTION 7: Visual Elements
            'charts': {
                'allocation_pie': {
                    'type': 'pie_chart',
                    'data': {
                        'Preserve (7%)': portfolio.bucket_1_allocation * 100,
                        'Provide-Income (11%)': portfolio.bucket_2_allocation * 100,
                        'Provide-Flexible (15%)': portfolio.bucket_3_allocation * 100,
                        'Performance (15%)': portfolio.bucket_4_allocation * 100,
                        'Cash (2%)': portfolio.bucket_5_allocation * 100
                    },
                    'title': 'Portfolio Allocation'
                },
                'bucket_bars': {
                    'type': 'horizontal_bar_chart',
                    'data': {
                        'Bucket 1\nPreserve\n7%': portfolio.bucket_1_amount,
                        'Bucket 2\nProvide-Income\n11%': portfolio.bucket_2_amount,
                        'Bucket 3\nProvide-Flexible\n15%': portfolio.bucket_3_amount,
                        'Bucket 4\nPerformance\n15%': portfolio.bucket_4_amount,
                        'Bucket 5\nCash\n2%': portfolio.bucket_5_amount
                    },
                    'title': 'Dollar Allocation by Bucket',
                    'xlabel': 'Amount ($)'
                }
            }
        }
        
        return slide_data
    
    @staticmethod
    def _format_bucket_details(portfolio: ClientPortfolio) -> List[Dict]:
        """Format detailed information for each bucket"""
        buckets = []
        
        allocations = {
            BucketType.BUCKET_1_PRESERVE: (portfolio.bucket_1_allocation, portfolio.bucket_1_amount),
            BucketType.BUCKET_2_PROVIDE_INCOME: (portfolio.bucket_2_allocation, portfolio.bucket_2_amount),
            BucketType.BUCKET_3_PROVIDE_FLEXIBLE: (portfolio.bucket_3_allocation, portfolio.bucket_3_amount),
            BucketType.BUCKET_4_PERFORMANCE: (portfolio.bucket_4_allocation, portfolio.bucket_4_amount),
            BucketType.BUCKET_5_CASH: (portfolio.bucket_5_allocation, portfolio.bucket_5_amount)
        }
        
        for bucket_type, bucket_def in FIVE_BUCKET_SYSTEM.items():
            allocation, amount = allocations[bucket_type]
            
            buckets.append({
                'name': bucket_def.name,
                'purpose': bucket_def.purpose,
                'risk_level': bucket_def.risk_level,
                'allocation': f'{allocation * 100:.1f}%',
                'amount': f'${amount:,.0f}',
                'expected_return': f'{bucket_def.expected_return * 100:.0f}%',
                'typical_holdings': bucket_def.typical_holdings,
                'role': bucket_def.role_in_planning,
                'time_horizon': bucket_def.time_horizon
            })
        
        return buckets
    
    @staticmethod
    def _format_return_calculation(
        portfolio: ClientPortfolio,
        contributions: Dict[str, float]
    ) -> List[str]:
        """Format the step-by-step return calculation"""
        calculation_steps = []
        
        # Show each bucket's contribution
        calculation_steps.append(
            f"Bucket 1: {portfolio.bucket_1_allocation*100:.1f}% × 7% = {contributions['Bucket 1 (Preserve)']*100:.2f}%"
        )
        calculation_steps.append(
            f"Bucket 2: {portfolio.bucket_2_allocation*100:.1f}% × 11% = {contributions['Bucket 2 (Provide - Income)']*100:.2f}%"
        )
        calculation_steps.append(
            f"Bucket 3: {portfolio.bucket_3_allocation*100:.1f}% × 15% = {contributions['Bucket 3 (Provide - Flexible)']*100:.2f}%"
        )
        calculation_steps.append(
            f"Bucket 4: {portfolio.bucket_4_allocation*100:.1f}% × 15% = {contributions['Bucket 4 (Performance)']*100:.2f}%"
        )
        calculation_steps.append(
            f"Bucket 5: {portfolio.bucket_5_allocation*100:.1f}% × 2% = {contributions['Bucket 5 (Cash)']*100:.2f}%"
        )
        
        # Show total
        total = sum(contributions.values())
        calculation_steps.append(f"\nTotal Blended Return: {total*100:.2f}%")
        
        return calculation_steps
    
    @staticmethod
    def _generate_comparison_insight(comparison: Dict[str, float]) -> str:
        """Generate insight about five-bucket vs 60/40"""
        difference = comparison['difference'] * 100
        
        if difference > 0:
            return (
                f"Your five-bucket strategy is projected to outperform a traditional "
                f"60/40 portfolio by {difference:.2f} percentage points annually. "
                f"This enhanced return comes from strategic allocation across five "
                f"distinct buckets, each serving a specific purpose in your plan."
            )
        else:
            return (
                f"Your five-bucket strategy is more conservative than a traditional "
                f"60/40 portfolio, providing {abs(difference):.2f}% less return but "
                f"with significantly more principal protection and clarity of purpose."
            )
    
    @staticmethod
    def _generate_plan_integration(portfolio: ClientPortfolio) -> Dict[str, any]:
        """Show how bucket design supports client's plan"""
        
        # Calculate provide buckets total (2 + 3)
        provide_total = portfolio.bucket_2_allocation + portfolio.bucket_3_allocation
        provide_amount = portfolio.bucket_2_amount + portfolio.bucket_3_amount
        
        integration = {
            'title': 'How This Design Supports Your Plan',
            'points': []
        }
        
        # Income support
        if portfolio.annual_income_need:
            integration['points'].append(
                f"Your Provide buckets (Buckets 2 & 3) total {provide_total*100:.0f}% "
                f"(${provide_amount:,.0f}), designed to support your "
                f"${portfolio.annual_income_need:,.0f} annual income need"
            )
        
        # Roth conversion support
        if portfolio.roth_conversion_annual_cost:
            integration['points'].append(
                f"Provide buckets also cover your ${portfolio.roth_conversion_annual_cost:,.0f} "
                f"annual Roth conversion tax costs while maintaining growth"
            )
        
        # Stability
        if portfolio.bucket_1_allocation > 0:
            integration['points'].append(
                f"Your Preserve bucket ({portfolio.bucket_1_allocation*100:.0f}% / "
                f"${portfolio.bucket_1_amount:,.0f}) provides stability and protects "
                f"against market downturns while earning 7% annually"
            )
        
        # Growth
        if portfolio.bucket_4_allocation > 0:
            integration['points'].append(
                f"Your Performance bucket ({portfolio.bucket_4_allocation*100:.0f}% / "
                f"${portfolio.bucket_4_amount:,.0f}) drives long-term growth at 15% "
                f"annually to offset inflation over decades"
            )
        
        # Liquidity
        if portfolio.bucket_5_allocation > 0:
            integration['points'].append(
                f"Your Cash bucket ({portfolio.bucket_5_allocation*100:.0f}% / "
                f"${portfolio.bucket_5_amount:,.0f}) provides immediate liquidity "
                f"for emergencies and opportunities"
            )
        
        return integration


# ═══════════════════════════════════════════════════════════════════════════
# CLIENT EXPLANATION SCRIPT
# ═══════════════════════════════════════════════════════════════════════════

class ClientExplanationScript:
    """
    Exact script for explaining Slide 29 to clients
    """
    
    @staticmethod
    def generate_explanation(portfolio: ClientPortfolio) -> str:
        """
        Generate the exact explanation script for Slide 29
        
        This is what advisors should say to clients
        """
        weighted_return = PortfolioReturnCalculator.calculate_weighted_return(portfolio)
        
        script = f"""
This slide shows how we intentionally design your entire portfolio using five 
distinct buckets. Each bucket has a specific purpose.

On the far left is your most conservative bucket—your Preserve bucket—designed 
to protect principal and provide stability. You have {portfolio.bucket_1_allocation*100:.0f}% 
(${portfolio.bucket_1_amount:,.0f}) allocated here, earning 7% annually.

The middle two buckets are your Provide buckets. These handle your income needs, 
Roth conversion tax costs, and cost-of-living adjustments. They are designed to 
be accessible and dependable. Together, they represent {(portfolio.bucket_2_allocation + portfolio.bucket_3_allocation)*100:.0f}% 
of your portfolio (${(portfolio.bucket_2_amount + portfolio.bucket_3_amount):,.0f}).

Bucket four is your Performance bucket—your long-term engine for growth. This is 
{portfolio.bucket_4_allocation*100:.0f}% (${portfolio.bucket_4_amount:,.0f}) allocated to 
higher-return strategies earning 15% annually to offset inflation over decades.

Finally, bucket five is simply cash for short-term liquidity—{portfolio.bucket_5_allocation*100:.0f}% 
(${portfolio.bucket_5_amount:,.0f}) for emergencies and opportunities.

By blending these five buckets, we create a balanced, purpose-driven portfolio 
with a blended expected return of {weighted_return*100:.2f}% annually—tailored to 
your plan rather than relying on outdated 60/40 models or overly simplified 
three-bucket strategies.

Each bucket serves a distinct purpose in your financial plan, giving us 
flexibility and clarity that traditional approaches simply cannot provide.
        """
        
        return script.strip()


# ═══════════════════════════════════════════════════════════════════════════
# EXAMPLE USAGE & OUTPUT
# ═══════════════════════════════════════════════════════════════════════════

def generate_slide_29_example():
    """
    EXAMPLE: How GPT should use this code to build Slide 29
    
    This demonstrates the complete workflow
    """
    
    # STEP 1: Create client portfolio
    portfolio = ClientPortfolio(
        client_name="Johnson Family",
        total_portfolio_value=2_500_000,
        
        # Five-bucket allocation (must sum to 1.0 / 100%)
        bucket_1_allocation=0.25,  # 25% Preserve
        bucket_2_allocation=0.20,  # 20% Provide - Income
        bucket_3_allocation=0.20,  # 20% Provide - Flexible
        bucket_4_allocation=0.30,  # 30% Performance
        bucket_5_allocation=0.05,  # 5% Cash
        
        # Planning factors
        annual_income_need=120_000,
        roth_conversion_annual_cost=50_000,
        risk_tolerance="moderate",
        time_horizon_years=25
    )
    
    print("="*80)
    print("SLIDE 29 INSTRUCTIONS - FIVE-BUCKET PORTFOLIO DESIGN")
    print("="*80)
    print(f"\nClient: {portfolio.client_name}")
    print(f"Total Portfolio: ${portfolio.total_portfolio_value:,.0f}")
    print(f"Annual Income Need: ${portfolio.annual_income_need:,.0f}")
    print(f"Roth Conversion Cost: ${portfolio.roth_conversion_annual_cost:,.0f}")
    
    # STEP 2: Calculate weighted return
    calculator = PortfolioReturnCalculator()
    weighted_return = calculator.calculate_weighted_return(portfolio)
    
    print("\n" + "="*80)
    print("WEIGHTED AVERAGE RETURN CALCULATION")
    print("="*80)
    
    contributions = calculator.calculate_bucket_contributions(portfolio)
    
    print(f"\nBucket 1 (Preserve):        {portfolio.bucket_1_allocation*100:5.1f}% × 7%  = {contributions['Bucket 1 (Preserve)']*100:5.2f}%")
    print(f"Bucket 2 (Provide-Income):  {portfolio.bucket_2_allocation*100:5.1f}% × 11% = {contributions['Bucket 2 (Provide - Income)']*100:5.2f}%")
    print(f"Bucket 3 (Provide-Flexible):{portfolio.bucket_3_allocation*100:5.1f}% × 15% = {contributions['Bucket 3 (Provide - Flexible)']*100:5.2f}%")
    print(f"Bucket 4 (Performance):     {portfolio.bucket_4_allocation*100:5.1f}% × 15% = {contributions['Bucket 4 (Performance)']*100:5.2f}%")
    print(f"Bucket 5 (Cash):            {portfolio.bucket_5_allocation*100:5.1f}% × 2%  = {contributions['Bucket 5 (Cash)']*100:5.2f}%")
    print("-" * 80)
    print(f"Total Blended Expected Return:              {weighted_return*100:5.2f}%")
    
    # STEP 3: Show allocation summary
    print("\n" + "="*80)
    print("PORTFOLIO ALLOCATION SUMMARY")
    print("="*80)
    
    print(f"\n{'Bucket':<30} {'Allocation':<12} {'Amount':<18} {'Return':<10}")
    print("-" * 80)
    print(f"{'Bucket 1 - Preserve':<30} {portfolio.bucket_1_allocation*100:>10.1f}%  ${portfolio.bucket_1_amount:>14,.0f}  {7:>8}%")
    print(f"{'Bucket 2 - Provide (Income)':<30} {portfolio.bucket_2_allocation*100:>10.1f}%  ${portfolio.bucket_2_amount:>14,.0f}  {11:>8}%")
    print(f"{'Bucket 3 - Provide (Flexible)':<30} {portfolio.bucket_3_allocation*100:>10.1f}%  ${portfolio.bucket_3_amount:>14,.0f}  {15:>8}%")
    print(f"{'Bucket 4 - Performance':<30} {portfolio.bucket_4_allocation*100:>10.1f}%  ${portfolio.bucket_4_amount:>14,.0f}  {15:>8}%")
    print(f"{'Bucket 5 - Cash':<30} {portfolio.bucket_5_allocation*100:>10.1f}%  ${portfolio.bucket_5_amount:>14,.0f}  {2:>8}%")
    print("-" * 80)
    print(f"{'TOTAL':<30} {100:>10.0f}%  ${portfolio.total_portfolio_value:>14,.0f}  {weighted_return*100:>7.2f}%")
    
    # STEP 4: Compare to 60/40
    print("\n" + "="*80)
    print("COMPARISON TO TRADITIONAL 60/40 PORTFOLIO")
    print("="*80)
    
    comparison = calculator.compare_to_60_40(portfolio)
    
    print(f"\nYour Five-Bucket Strategy:      {comparison['five_bucket_return']*100:.2f}%")
    print(f"Traditional 60/40 Portfolio:    {comparison['traditional_60_40_return']*100:.2f}%")
    print(f"Difference:                     {comparison['difference']*100:+.2f}%")
    print(f"Outperformance:                 {comparison['outperformance_percentage']:+.1f}%")
    
    # STEP 5: Build full slide
    print("\n" + "="*80)
    print("BUILDING COMPLETE SLIDE 29")
    print("="*80)
    
    slide_instructions = Slide29Builder.build_slide_29_instructions(portfolio)
    
    # STEP 6: Generate client explanation
    print("\n" + "="*80)
    print("CLIENT EXPLANATION SCRIPT")
    print("="*80)
    
    explanation = ClientExplanationScript.generate_explanation(portfolio)
    print(f"\n{explanation}")
    
    print("\n" + "="*80)
    print("✓ Slide 29 Complete!")
    print("="*80)
    
    return slide_instructions


# ═══════════════════════════════════════════════════════════════════════════
# GPT TRAINING SUMMARY
# ═══════════════════════════════════════════════════════════════════════════

"""
TRAINING SUMMARY FOR GPT - HOW TO BUILD SLIDE 29

WHEN USER ASKS FOR FIVE-BUCKET PORTFOLIO DESIGN:

1. GATHER PORTFOLIO DATA:
   - Client name
   - Total portfolio value
   - Five bucket allocations (must sum to 100%)
   - Annual income need (optional)
   - Roth conversion annual cost (optional)

2. CREATE PORTFOLIO:
   portfolio = ClientPortfolio(
       client_name="Client Name",
       total_portfolio_value=2_500_000,
       bucket_1_allocation=0.25,  # 25%
       bucket_2_allocation=0.20,  # 20%
       bucket_3_allocation=0.20,  # 20%
       bucket_4_allocation=0.30,  # 30%
       bucket_5_allocation=0.05   # 5%
   )

3. CALCULATE WEIGHTED RETURN:
   calculator = PortfolioReturnCalculator()
   weighted_return = calculator.calculate_weighted_return(portfolio)

4. BUILD SLIDE 29:
   slide_data = Slide29Builder.build_slide_29_instructions(portfolio)

5. OFFICIAL RETURN ASSUMPTIONS (NJM):
   - Bucket 1 (Preserve): 7%
   - Bucket 2 (Provide - Income): 11%
   - Bucket 3 (Provide - Flexible): 15%
   - Bucket 4 (Performance): 15%
   - Bucket 5 (Cash): 2%

6. EXPLAIN FIVE BUCKETS:
   - Bucket 1: Preserve - Principal protection, lowest risk (7%)
   - Bucket 2: Provide (Income) - Stable income, low-moderate risk (11%)
   - Bucket 3: Provide (Flexible) - Income gaps, moderate risk (15%)
   - Bucket 4: Performance - Long-term growth, higher risk (15%)
   - Bucket 5: Cash - Immediate liquidity, no market risk (2%)

7. SHOW ADVANTAGES OVER 60/40:
   - More specific asset purposes
   - Better clarity for clients
   - Improved diversification
   - Flexibility traditional models lack

8. CALCULATE WEIGHTED RETURN:
   Formula: Σ(Bucket Weight × Bucket Expected Return)
   Example: (0.25×7%) + (0.20×11%) + (0.20×15%) + (0.30×15%) + (0.05×2%)

OUTPUT STRUCTURE:
- Why five buckets (vs 60/40 or 3-bucket)
- Five-bucket structure details
- Portfolio allocation summary
- Weighted return calculation
- Comparison to 60/40
- How design supports client's plan
- Visual charts (pie, bars)
- Client explanation script

IMPORTANT REMINDERS:
- Allocations must sum to exactly 100%
- Use official NJM return assumptions
- Show step-by-step calculation
- Compare to traditional 60/40
- Explain how each bucket supports the plan
- Provide client-facing explanation script
- Include visual elements

"""


# ═══════════════════════════════════════════════════════════════════════════
# RUN EXAMPLE
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # Generate example Slide 29
    slide_instructions = generate_slide_29_example()
    
    print("\n\n" + "="*80)
    print("CODE COMPLETE - QUANTUM CAN NOW BUILD SLIDE 29!")
    print("="*80)
    print("\nThis code teaches Quantum:")
    print("✓ How to design five-bucket portfolios")
    print("✓ How to calculate weighted average returns")
    print("✓ How to compare to traditional 60/40")
    print("✓ How to explain each bucket's purpose")
    print("✓ How to show plan integration")
    print("✓ How to structure Slide 29 with all required elements")
    print("✓ How to generate client explanation scripts")
    print("\nGPT can now build complete five-bucket portfolio slides!")
    print("="*80)
