"""
╔═══════════════════════════════════════════════════════════════════════╗
║                                                                       ║
║              QUANTUM ROTH CONVERSION SLIDE BUILDER                    ║
║              Slide 21 - Complete Instructions for GPT                 ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝

INSTRUCTIONS FOR GPT: HOW TO BUILD SLIDE 21 - ROTH CONVERSION OPTIONS

This code teaches Quantum EXACTLY how to:
1. Analyze client income and tax position
2. Calculate conversion scenarios (22%, 24%, 32% brackets)
3. Factor in portfolio growth (8% annually)
4. Calculate total cost and timeline for each scenario
5. Build the comparison slide showing all options

PURPOSE OF SLIDE 21:
Demonstrate client's Roth conversion options by analyzing income, tax brackets,
portfolio growth, and total cost/timeline to move IRA dollars into Roth accounts.

"""

from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
from enum import Enum


# ═══════════════════════════════════════════════════════════════════════════
# TAX BRACKET DEFINITIONS (2024 Federal Tax Brackets)
# ═══════════════════════════════════════════════════════════════════════════

class FilingStatus(Enum):
    """Client's tax filing status"""
    MARRIED = "married_filing_jointly"
    SINGLE = "single"
    HEAD_OF_HOUSEHOLD = "head_of_household"


# 2024 Federal Tax Brackets
TAX_BRACKETS_2024 = {
    FilingStatus.MARRIED: {
        10: (0, 22_000),
        12: (22_000, 89_075),
        22: (89_075, 190_750),
        24: (190_750, 364_200),
        32: (364_200, 462_500),
        35: (462_500, 693_750),
        37: (693_750, float('inf'))
    },
    FilingStatus.SINGLE: {
        10: (0, 11_000),
        12: (11_000, 44_725),
        22: (44_725, 95_375),
        24: (95_375, 182_100),
        32: (182_100, 231_250),
        35: (231_250, 578_125),
        37: (578_125, float('inf'))
    }
}

# Standard Deductions (2024)
STANDARD_DEDUCTION_2024 = {
    FilingStatus.MARRIED: 29_200,
    FilingStatus.SINGLE: 14_600,
    FilingStatus.HEAD_OF_HOUSEHOLD: 21_900
}


# ═══════════════════════════════════════════════════════════════════════════
# CLIENT DATA STRUCTURE
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class ClientProfile:
    """
    STEP 1: Gather Client Information
    
    All information needed to analyze Roth conversion options
    """
    # Required Information
    name: str
    filing_status: FilingStatus
    gross_income: float                  # Total income from all sources
    ira_balance: float                   # Current IRA balance to convert
    
    # Optional (defaults provided)
    standard_deduction: Optional[float] = None
    other_deductions: float = 0          # Itemized deductions beyond standard
    portfolio_growth_rate: float = 0.08  # Default 8% annual growth
    
    def __post_init__(self):
        """Calculate taxable income and current bracket"""
        # Use standard deduction if not provided
        if self.standard_deduction is None:
            self.standard_deduction = STANDARD_DEDUCTION_2024[self.filing_status]
        
        # Calculate taxable income
        self.taxable_income = max(0, 
            self.gross_income - self.standard_deduction - self.other_deductions
        )
        
        # Determine current tax bracket
        self.current_bracket = self._determine_bracket(self.taxable_income)
    
    def _determine_bracket(self, taxable_income: float) -> int:
        """Determine which tax bracket the income falls into"""
        brackets = TAX_BRACKETS_2024[self.filing_status]
        
        for rate, (min_income, max_income) in brackets.items():
            if min_income <= taxable_income < max_income:
                return rate
        
        return 37  # Highest bracket


# ═══════════════════════════════════════════════════════════════════════════
# ROTH CONVERSION CALCULATIONS
# ═══════════════════════════════════════════════════════════════════════════

class RothConversionCalculator:
    """
    STEP 2-5: Calculate Roth Conversion Scenarios
    
    This class performs ALL calculations needed for Slide 21
    """
    
    def __init__(self, client: ClientProfile):
        self.client = client
        self.brackets = TAX_BRACKETS_2024[client.filing_status]
    
    def calculate_room_in_bracket(self, target_bracket: int) -> float:
        """
        Calculate how much income can be added before entering next bracket
        
        Formula: Top of target bracket - Current taxable income
        
        Example: 
        - Married couple, $100,000 income
        - After deductions: $70,800 taxable
        - Top of 12% bracket: $89,075
        - Room in 12% bracket: $89,075 - $70,800 = $18,275
        - Can convert $18,275 more at 12% rate
        """
        _, bracket_max = self.brackets[target_bracket]
        room = bracket_max - self.client.taxable_income
        return max(0, room)
    
    def calculate_conversion_to_bracket(self, target_bracket: int) -> float:
        """
        Calculate how much can be converted up to top of target bracket
        
        This is the "conversion space" available
        """
        _, bracket_max = self.brackets[target_bracket]
        conversion_amount = bracket_max - self.client.taxable_income
        return max(0, conversion_amount)
    
    def calculate_conversion_tax(self, conversion_amount: float, target_bracket: int) -> float:
        """
        Calculate tax owed on a Roth conversion
        
        KEY CONCEPT: Roth conversion is treated as ordinary income
        Tax is calculated using marginal rates from current bracket up to target bracket
        
        Example:
        - Converting $50,000
        - Current bracket: 12%
        - Target bracket: 22%
        - First portion taxed at 12%, remainder at 22%
        """
        if conversion_amount <= 0:
            return 0
        
        current_income = self.client.taxable_income
        total_tax = 0
        remaining_conversion = conversion_amount
        
        # Calculate tax for each bracket the conversion passes through
        for rate in sorted(self.brackets.keys()):
            if remaining_conversion <= 0:
                break
            
            min_bracket, max_bracket = self.brackets[rate]
            
            # Skip brackets below current income
            if max_bracket <= current_income:
                continue
            
            # Calculate how much of conversion falls in this bracket
            bracket_start = max(current_income, min_bracket)
            bracket_end = max_bracket
            
            amount_in_bracket = min(
                remaining_conversion,
                bracket_end - bracket_start
            )
            
            if amount_in_bracket > 0:
                tax_in_bracket = amount_in_bracket * (rate / 100)
                total_tax += tax_in_bracket
                remaining_conversion -= amount_in_bracket
                current_income += amount_in_bracket
            
            # Stop when we reach target bracket
            if rate >= target_bracket:
                break
        
        return total_tax
    
    def project_conversion_timeline(
        self, 
        annual_conversion: float,
        target_bracket: int
    ) -> Dict[str, any]:
        """
        STEP 4-5: Project timeline to complete IRA to Roth conversion
        
        KEY FACTORS:
        1. IRA grows at portfolio_growth_rate each year
        2. Annual conversion reduces IRA balance
        3. Continue until IRA is fully converted
        
        Returns detailed year-by-year projection
        """
        ira_balance = self.client.ira_balance
        growth_rate = self.client.portfolio_growth_rate
        
        year = 0
        total_taxes_paid = 0
        total_converted = 0
        
        yearly_details = []
        
        while ira_balance > 0 and year < 100:  # Safety limit
            year += 1
            
            # Beginning of year
            starting_balance = ira_balance
            
            # Apply growth to IRA
            growth = ira_balance * growth_rate
            ira_balance += growth
            
            # Convert for this year (limited to remaining IRA balance)
            conversion_this_year = min(annual_conversion, ira_balance)
            
            # Calculate tax on conversion
            tax_this_year = self.calculate_conversion_tax(
                conversion_this_year, 
                target_bracket
            )
            
            # Reduce IRA by conversion
            ira_balance -= conversion_this_year
            
            # Track totals
            total_converted += conversion_this_year
            total_taxes_paid += tax_this_year
            
            # Record this year's details
            yearly_details.append({
                'year': year,
                'starting_balance': starting_balance,
                'growth': growth,
                'conversion': conversion_this_year,
                'tax_paid': tax_this_year,
                'ending_balance': ira_balance
            })
            
            # Stop if IRA is depleted
            if ira_balance < 1:
                break
        
        return {
            'years_to_complete': year,
            'total_taxes_paid': total_taxes_paid,
            'total_converted': total_converted,
            'final_ira_balance': ira_balance,
            'yearly_breakdown': yearly_details
        }
    
    def calculate_three_scenarios(self) -> Dict[str, Dict]:
        """
        STEP 2: Run Three Conversion Scenarios
        
        Calculate conversions to:
        1. 22% bracket - Smaller conversions, slower timeline
        2. 24% bracket - Medium conversions, balanced approach
        3. 32% bracket - Larger conversions, faster completion
        
        Returns complete analysis for all three scenarios
        """
        scenarios = {}
        target_brackets = [22, 24, 32]
        
        for bracket in target_brackets:
            # Calculate annual conversion amount
            annual_conversion = self.calculate_conversion_to_bracket(bracket)
            
            # Project timeline with growth
            projection = self.project_conversion_timeline(
                annual_conversion,
                bracket
            )
            
            # Calculate effective tax rate
            effective_rate = (projection['total_taxes_paid'] / 
                            projection['total_converted'] * 100 
                            if projection['total_converted'] > 0 else 0)
            
            scenarios[f"{bracket}%_bracket"] = {
                'target_bracket': bracket,
                'annual_conversion': annual_conversion,
                'years_to_complete': projection['years_to_complete'],
                'total_taxes': projection['total_taxes_paid'],
                'total_converted': projection['total_converted'],
                'effective_tax_rate': effective_rate,
                'final_ira_balance': projection['final_ira_balance'],
                'yearly_breakdown': projection['yearly_breakdown']
            }
        
        return scenarios


# ═══════════════════════════════════════════════════════════════════════════
# SLIDE 21 BUILDER
# ═══════════════════════════════════════════════════════════════════════════

class Slide21Builder:
    """
    COMPLETE INSTRUCTIONS FOR BUILDING SLIDE 21
    
    This class contains the EXACT structure and content for Slide 21
    """
    
    @staticmethod
    def build_slide_21_instructions(client: ClientProfile) -> Dict[str, any]:
        """
        Generate complete instructions for building Slide 21
        
        Returns structured data that Quantum uses to build the slide
        """
        
        # Initialize calculator
        calculator = RothConversionCalculator(client)
        
        # Calculate all three scenarios
        scenarios = calculator.calculate_three_scenarios()
        
        # Build slide structure
        slide_data = {
            'slide_number': 21,
            'slide_title': f'Roth Conversion Options - {client.name}',
            'slide_type': 'roth_conversion_analysis',
            
            # SECTION 1: Client Current Position
            'client_position': {
                'title': 'Current Tax Position',
                'data': {
                    'gross_income': f'${client.gross_income:,.0f}',
                    'filing_status': client.filing_status.value.replace('_', ' ').title(),
                    'standard_deduction': f'${client.standard_deduction:,.0f}',
                    'taxable_income': f'${client.taxable_income:,.0f}',
                    'current_bracket': f'{client.current_bracket}%',
                    'ira_balance': f'${client.ira_balance:,.0f}',
                    'portfolio_growth': f'{client.portfolio_growth_rate * 100:.0f}%'
                },
                'layout': 'metrics_grid'
            },
            
            # SECTION 2: Room in Current Bracket
            'bracket_room': {
                'title': 'Available Conversion Space',
                'data': {
                    'current_bracket': f'{client.current_bracket}%',
                    'room_in_bracket': f'${calculator.calculate_room_in_bracket(client.current_bracket):,.0f}',
                    'explanation': f'You can convert ${calculator.calculate_room_in_bracket(client.current_bracket):,.0f} more at your current {client.current_bracket}% rate before entering the next bracket'
                },
                'layout': 'highlight_box'
            },
            
            # SECTION 3: Three Conversion Scenarios
            'scenarios': {
                'title': 'Conversion Scenarios Comparison',
                'subtitle': 'Compare cost vs. speed for different conversion strategies',
                'data': scenarios,
                'layout': 'comparison_table'
            },
            
            # SECTION 4: Key Insights
            'key_insights': Slide21Builder._generate_insights(client, scenarios),
            
            # SECTION 5: Recommendations
            'recommendations': Slide21Builder._generate_recommendations(client, scenarios),
            
            # SECTION 6: Visual Elements
            'charts': {
                'timeline_chart': {
                    'type': 'bar_chart',
                    'data': {
                        '22% Bracket': scenarios['22%_bracket']['years_to_complete'],
                        '24% Bracket': scenarios['24%_bracket']['years_to_complete'],
                        '32% Bracket': scenarios['32%_bracket']['years_to_complete']
                    },
                    'title': 'Years to Complete Conversion',
                    'xlabel': 'Conversion Strategy',
                    'ylabel': 'Years'
                },
                'cost_chart': {
                    'type': 'bar_chart',
                    'data': {
                        '22% Bracket': scenarios['22%_bracket']['total_taxes'],
                        '24% Bracket': scenarios['24%_bracket']['total_taxes'],
                        '32% Bracket': scenarios['32%_bracket']['total_taxes']
                    },
                    'title': 'Total Tax Cost',
                    'xlabel': 'Conversion Strategy',
                    'ylabel': 'Total Taxes ($)'
                }
            }
        }
        
        return slide_data
    
    @staticmethod
    def _generate_insights(client: ClientProfile, scenarios: Dict) -> List[str]:
        """
        STEP 6: Generate key insights about the scenarios
        
        These insights help clients understand trade-offs
        """
        insights = []
        
        s22 = scenarios['22%_bracket']
        s24 = scenarios['24%_bracket']
        s32 = scenarios['32%_bracket']
        
        # Insight 1: Timeline comparison
        if s22['years_to_complete'] > s32['years_to_complete'] * 1.5:
            insights.append(
                f"Converting only to the 22% bracket takes {s22['years_to_complete']} years, "
                f"while the 32% strategy completes in {s32['years_to_complete']} years—"
                f"{s22['years_to_complete'] - s32['years_to_complete']} years faster"
            )
        
        # Insight 2: Growth impact
        if client.ira_balance > 500_000:
            annual_growth = client.ira_balance * client.portfolio_growth_rate
            insights.append(
                f"With ${client.ira_balance:,.0f} growing at {client.portfolio_growth_rate*100:.0f}% annually, "
                f"your IRA grows by approximately ${annual_growth:,.0f} per year. "
                f"Slower conversions may not keep pace with growth."
            )
        
        # Insight 3: Tax cost comparison
        tax_difference = s32['total_taxes'] - s22['total_taxes']
        insights.append(
            f"The 32% strategy costs ${tax_difference:,.0f} more in total taxes "
            f"but completes {s22['years_to_complete'] - s32['years_to_complete']} years faster"
        )
        
        # Insight 4: Effective rates
        insights.append(
            f"Effective tax rates: 22% strategy = {s22['effective_tax_rate']:.1f}%, "
            f"24% strategy = {s24['effective_tax_rate']:.1f}%, "
            f"32% strategy = {s32['effective_tax_rate']:.1f}%"
        )
        
        return insights
    
    @staticmethod
    def _generate_recommendations(client: ClientProfile, scenarios: Dict) -> List[str]:
        """
        Generate personalized recommendations based on scenarios
        """
        recommendations = []
        
        s22 = scenarios['22%_bracket']
        s24 = scenarios['24%_bracket']
        s32 = scenarios['32%_bracket']
        
        # Recommendation based on timeline
        if s22['years_to_complete'] > 15:
            recommendations.append(
                "Consider the 24% or 32% strategy: "
                f"The 22% approach takes {s22['years_to_complete']} years, "
                "which may extend beyond your planning horizon"
            )
        
        # Recommendation based on IRA size
        if client.ira_balance > 1_000_000:
            recommendations.append(
                "With a substantial IRA balance, faster conversion strategies "
                "may be advantageous to minimize future RMD requirements"
            )
        
        # Recommendation based on age (if we had it)
        recommendations.append(
            "Balance conversion speed with annual tax impact based on your "
            "cash flow capacity and retirement timeline"
        )
        
        # Strategic recommendation
        recommendations.append(
            "Consider splitting the difference: Start with 24% bracket conversions, "
            "then adjust annually based on market conditions and income changes"
        )
        
        return recommendations


# ═══════════════════════════════════════════════════════════════════════════
# EXAMPLE USAGE & OUTPUT FORMAT
# ═══════════════════════════════════════════════════════════════════════════

def generate_slide_21_example():
    """
    EXAMPLE: How GPT should use this code to build Slide 21
    
    This demonstrates the complete workflow
    """
    
    # STEP 1: Create client profile from input data
    client = ClientProfile(
        name="Johnson Family",
        filing_status=FilingStatus.MARRIED,
        gross_income=100_000,
        ira_balance=1_000_000,
        portfolio_growth_rate=0.08  # 8% annual growth
    )
    
    print("="*80)
    print("SLIDE 21 INSTRUCTIONS - ROTH CONVERSION OPTIONS")
    print("="*80)
    print(f"\nClient: {client.name}")
    print(f"Gross Income: ${client.gross_income:,.0f}")
    print(f"IRA Balance: ${client.ira_balance:,.0f}")
    print(f"Filing Status: {client.filing_status.value.replace('_', ' ').title()}")
    print(f"Current Tax Bracket: {client.current_bracket}%")
    print(f"Taxable Income: ${client.taxable_income:,.0f}")
    
    # STEP 2: Build slide instructions
    slide_instructions = Slide21Builder.build_slide_21_instructions(client)
    
    # STEP 3: Display scenario comparisons
    print("\n" + "="*80)
    print("THREE CONVERSION SCENARIOS")
    print("="*80)
    
    scenarios = slide_instructions['scenarios']['data']
    
    # Print comparison table
    print(f"\n{'Strategy':<20} {'Annual Conv.':<15} {'Years':<10} {'Total Taxes':<15} {'Eff. Rate':<12}")
    print("-" * 80)
    
    for scenario_name, data in scenarios.items():
        bracket = data['target_bracket']
        annual = data['annual_conversion']
        years = data['years_to_complete']
        taxes = data['total_taxes']
        rate = data['effective_tax_rate']
        
        print(f"{bracket}% Bracket{'':<10} ${annual:>12,.0f}  {years:>8}    ${taxes:>12,.0f}  {rate:>10.1f}%")
    
    # STEP 4: Display key insights
    print("\n" + "="*80)
    print("KEY INSIGHTS")
    print("="*80)
    
    for i, insight in enumerate(slide_instructions['key_insights'], 1):
        print(f"\n{i}. {insight}")
    
    # STEP 5: Display recommendations
    print("\n" + "="*80)
    print("RECOMMENDATIONS")
    print("="*80)
    
    for i, rec in enumerate(slide_instructions['recommendations'], 1):
        print(f"\n{i}. {rec}")
    
    # STEP 6: Show year-by-year breakdown for one scenario
    print("\n" + "="*80)
    print("YEAR-BY-YEAR BREAKDOWN (24% Bracket Strategy)")
    print("="*80)
    
    scenario_24 = scenarios['24%_bracket']
    yearly = scenario_24['yearly_breakdown'][:10]  # First 10 years
    
    print(f"\n{'Year':<6} {'Start Bal':<15} {'Growth':<15} {'Conversion':<15} {'Tax':<12} {'End Bal':<15}")
    print("-" * 90)
    
    for year_data in yearly:
        print(
            f"{year_data['year']:<6} "
            f"${year_data['starting_balance']:>12,.0f}  "
            f"${year_data['growth']:>12,.0f}  "
            f"${year_data['conversion']:>12,.0f}  "
            f"${year_data['tax_paid']:>10,.0f}  "
            f"${year_data['ending_balance']:>12,.0f}"
        )
    
    print("\n" + "="*80)
    print(f"✓ Slide 21 complete! Ready to present to {client.name}")
    print("="*80)
    
    return slide_instructions


# ═══════════════════════════════════════════════════════════════════════════
# GPT TRAINING SUMMARY
# ═══════════════════════════════════════════════════════════════════════════

"""
TRAINING SUMMARY FOR GPT - HOW TO BUILD SLIDE 21

WHEN USER ASKS FOR ROTH CONVERSION ANALYSIS:

1. GATHER CLIENT DATA:
   - Name
   - Filing status (married/single)
   - Gross income
   - IRA balance
   - Portfolio growth rate (default 8%)

2. CREATE CLIENT PROFILE:
   client = ClientProfile(
       name="Client Name",
       filing_status=FilingStatus.MARRIED,
       gross_income=100000,
       ira_balance=1000000
   )

3. BUILD SLIDE 21:
   slide_data = Slide21Builder.build_slide_21_instructions(client)

4. PRESENT THREE SCENARIOS:
   - 22% bracket: Lower tax, slower completion
   - 24% bracket: Balanced approach
   - 32% bracket: Higher tax, faster completion

5. EXPLAIN KEY CONCEPTS:
   - Room in current bracket
   - Annual conversion amounts
   - Portfolio growth impact (8% default)
   - Total tax cost vs. timeline trade-off
   - Effective tax rates

6. SHOW COMPARISONS:
   - Years to complete
   - Total taxes paid
   - Annual conversion amounts
   - Impact of growth on timeline

7. PROVIDE INSIGHTS:
   - Which strategy completes fastest
   - How growth affects slower strategies
   - Tax cost differences
   - Effective rates for each scenario

8. MAKE RECOMMENDATIONS:
   - Based on IRA size
   - Based on timeline
   - Based on client's situation
   - Suggest balanced approach

OUTPUT STRUCTURE:
- Current tax position (income, bracket, deductions)
- Room in current bracket
- Three scenario comparison table
- Timeline visualization
- Tax cost visualization
- Key insights
- Personalized recommendations
- Year-by-year breakdown

CALCULATIONS TO PERFORM:
✓ Taxable income calculation
✓ Current bracket determination
✓ Room in bracket calculation
✓ Annual conversion amounts
✓ Tax on conversions (marginal rates)
✓ Portfolio growth projections
✓ Year-by-year balances
✓ Total costs and timelines
✓ Effective tax rates

IMPORTANT REMINDERS:
- Portfolio grows at 8% annually (default)
- Growth increases IRA balance each year
- Slower conversions may not keep pace with growth
- Faster conversions cost more but complete sooner
- Show trade-offs clearly
- Use client's actual tax brackets
- Factor in standard deduction
- Calculate marginal tax rates correctly
"""


# ═══════════════════════════════════════════════════════════════════════════
# RUN EXAMPLE
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # Generate example Slide 21
    slide_instructions = generate_slide_21_example()
    
    print("\n\n" + "="*80)
    print("CODE COMPLETE - QUANTUM CAN NOW BUILD SLIDE 21!")
    print("="*80)
    print("\nThis code teaches Quantum:")
    print("✓ How to analyze client income and tax position")
    print("✓ How to calculate three conversion scenarios")
    print("✓ How to factor in portfolio growth")
    print("✓ How to calculate total cost and timeline")
    print("✓ How to generate insights and recommendations")
    print("✓ How to structure Slide 21 with all required elements")
    print("\nGPT can now build complete Roth conversion analysis slides!")
    print("="*80)
