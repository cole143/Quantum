"""
Quantum Financial Assistant - All-in-One Deployment
Created by: Cole Sorokolit and Nic McLeod

This single file contains everything needed to deploy to Render.
Just upload this file + the requirements.txt to GitHub and deploy!

Version: 2.0.0 - Single File Edition
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
from dataclasses import dataclass, asdict
import json
import os
import uvicorn


# ============================================================================
# TAX ENGINE - All calculation logic
# ============================================================================

class FilingStatus(Enum):
    """Federal tax filing statuses"""
    SINGLE = "Single"
    MARRIED_FILING_JOINTLY = "Married Filing Jointly"
    MARRIED_FILING_SEPARATELY = "Married Filing Separately"
    HEAD_OF_HOUSEHOLD = "Head of Household"


@dataclass
class TaxBracket:
    """Tax bracket definition"""
    rate: float
    range_start: int
    range_end: Optional[int]


@dataclass
class TaxCalculationResult:
    """Result of a tax calculation"""
    total_tax: float
    effective_rate: float
    marginal_rate: float
    breakdown: List[Dict[str, Any]]
    filing_status: str
    year: int
    taxable_income: float
    summary: str
    disclaimer: str
    
    def to_dict(self):
        return asdict(self)


class QuantumEngine:
    """Main Quantum calculation engine"""
    
    def __init__(self):
        self.tax_brackets_2025 = self._load_2025_brackets()
        self.tax_brackets_2024 = self._load_2024_brackets()
        self.standard_deductions = self._load_standard_deductions()
        self.disclaimers = self._load_disclaimers()
        self.fdic_info = self._load_fdic_info()
    
    def _load_2025_brackets(self):
        return {
            FilingStatus.SINGLE: [
                TaxBracket(0.10, 0, 11925),
                TaxBracket(0.12, 11925, 48475),
                TaxBracket(0.22, 48475, 103350),
                TaxBracket(0.24, 103350, 197300),
                TaxBracket(0.32, 197300, 250525),
                TaxBracket(0.35, 250525, 626350),
                TaxBracket(0.37, 626350, None)
            ],
            FilingStatus.MARRIED_FILING_JOINTLY: [
                TaxBracket(0.10, 0, 23850),
                TaxBracket(0.12, 23850, 96950),
                TaxBracket(0.22, 96950, 206700),
                TaxBracket(0.24, 206700, 394600),
                TaxBracket(0.32, 394600, 501050),
                TaxBracket(0.35, 501050, 751600),
                TaxBracket(0.37, 751600, None)
            ],
            FilingStatus.MARRIED_FILING_SEPARATELY: [
                TaxBracket(0.10, 0, 11925),
                TaxBracket(0.12, 11925, 48475),
                TaxBracket(0.22, 48475, 103350),
                TaxBracket(0.24, 103350, 197300),
                TaxBracket(0.32, 197300, 250525),
                TaxBracket(0.35, 250525, 375800),
                TaxBracket(0.37, 375800, None)
            ],
            FilingStatus.HEAD_OF_HOUSEHOLD: [
                TaxBracket(0.10, 0, 17000),
                TaxBracket(0.12, 17000, 64850),
                TaxBracket(0.22, 64850, 103350),
                TaxBracket(0.24, 103350, 197300),
                TaxBracket(0.32, 197300, 250500),
                TaxBracket(0.35, 250500, 626350),
                TaxBracket(0.37, 626350, None)
            ]
        }
    
    def _load_2024_brackets(self):
        return {
            FilingStatus.SINGLE: [
                TaxBracket(0.10, 0, 11600),
                TaxBracket(0.12, 11600, 47150),
                TaxBracket(0.22, 47150, 100525),
                TaxBracket(0.24, 100525, 191950),
                TaxBracket(0.32, 191950, 243725),
                TaxBracket(0.35, 243725, 609350),
                TaxBracket(0.37, 609350, None)
            ],
            FilingStatus.MARRIED_FILING_JOINTLY: [
                TaxBracket(0.10, 0, 23200),
                TaxBracket(0.12, 23200, 94300),
                TaxBracket(0.22, 94300, 201050),
                TaxBracket(0.24, 201050, 383900),
                TaxBracket(0.32, 383900, 487450),
                TaxBracket(0.35, 487450, 731200),
                TaxBracket(0.37, 731200, None)
            ]
        }
    
    def _load_standard_deductions(self):
        return {
            2025: {
                FilingStatus.SINGLE: 15000,
                FilingStatus.MARRIED_FILING_JOINTLY: 30000,
                FilingStatus.MARRIED_FILING_SEPARATELY: 15000,
                FilingStatus.HEAD_OF_HOUSEHOLD: 22500
            },
            2024: {
                FilingStatus.SINGLE: 14600,
                FilingStatus.MARRIED_FILING_JOINTLY: 29200,
                FilingStatus.MARRIED_FILING_SEPARATELY: 14600,
                FilingStatus.HEAD_OF_HOUSEHOLD: 21900
            }
        }
    
    def _load_disclaimers(self):
        return {
            'tax_calculation': (
                "⚠️ TAX CALCULATION DISCLAIMER: This calculation is for educational and "
                "informational purposes only. Tax laws are complex and subject to change. "
                "Consult a licensed tax professional or CPA for personalized tax advice."
            ),
            'fdic_insurance': (
                "⚠️ FDIC INSURANCE DISCLOSURE: This information is educational only. "
                "For specific questions about your accounts, contact your bank or visit FDIC.gov."
            )
        }
    
    def _load_fdic_info(self):
        return {
            'coverage_limit': 250000,
            'coverage_per': 'per depositor, per insured bank, per ownership category',
            'covered_accounts': [
                'Checking accounts',
                'Savings accounts',
                'Money market deposit accounts',
                'Certificates of deposit (CDs)'
            ],
            'not_covered': [
                'Stocks',
                'Bonds',
                'Mutual funds',
                'Cryptocurrency'
            ],
            'key_points': [
                'Each ownership category is insured separately up to $250,000',
                'Joint accounts: Each co-owner gets $250,000 coverage',
                'Coverage is automatic - no need to apply'
            ],
            'summary': 'FDIC insurance protects deposits up to $250,000 per depositor, per bank, per ownership category.'
        }
    
    def calculate_tax(self, income: float, filing_status: str, year: int = 2025, is_gross: bool = False):
        """Calculate federal income tax"""
        
        # Parse filing status
        fs = self._parse_filing_status(filing_status)
        
        # Apply standard deduction if gross
        taxable_income = income
        if is_gross:
            std_ded = self.standard_deductions[year][fs]
            taxable_income = max(0, income - std_ded)
        
        # Get brackets
        brackets = self.tax_brackets_2025[fs] if year == 2025 else self.tax_brackets_2024.get(fs, self.tax_brackets_2025[fs])
        
        # Calculate tax
        total_tax = 0
        breakdown = []
        
        for bracket in brackets:
            start = bracket.range_start
            end = bracket.range_end if bracket.range_end else float('inf')
            
            if taxable_income <= start:
                break
            
            taxable_in_bracket = min(taxable_income - start, end - start)
            
            if taxable_in_bracket > 0:
                tax = taxable_in_bracket * bracket.rate
                total_tax += tax
                
                breakdown.append({
                    'bracket': f"{bracket.rate * 100:.0f}%",
                    'range_start': start,
                    'range_end': end if end != float('inf') else taxable_income,
                    'taxable_amount': taxable_in_bracket,
                    'tax': tax,
                    'description': f"${taxable_in_bracket:,.2f} at {bracket.rate * 100:.0f}% = ${tax:,.2f}"
                })
        
        effective_rate = (total_tax / taxable_income * 100) if taxable_income > 0 else 0
        marginal_rate = float(breakdown[-1]['bracket'].rstrip('%')) if breakdown else 0
        
        summary = f"For ${taxable_income:,.2f} taxable income ({fs.value}, {year}), your federal income tax is ${total_tax:,.2f}."
        
        return TaxCalculationResult(
            total_tax=total_tax,
            effective_rate=effective_rate,
            marginal_rate=marginal_rate,
            breakdown=breakdown,
            filing_status=fs.value,
            year=year,
            taxable_income=taxable_income,
            summary=summary,
            disclaimer=self.disclaimers['tax_calculation']
        )
    
    def get_fdic_info(self):
        """Get FDIC information"""
        info = self.fdic_info.copy()
        info['disclaimer'] = self.disclaimers['fdic_insurance']
        return info
    
    def _parse_filing_status(self, status: str) -> FilingStatus:
        """Parse filing status string"""
        status_map = {
            'SINGLE': FilingStatus.SINGLE,
            'S': FilingStatus.SINGLE,
            'MARRIED': FilingStatus.MARRIED_FILING_JOINTLY,
            'MARRIED_FILING_JOINTLY': FilingStatus.MARRIED_FILING_JOINTLY,
            'MFJ': FilingStatus.MARRIED_FILING_JOINTLY,
            'MARRIED_FILING_SEPARATELY': FilingStatus.MARRIED_FILING_SEPARATELY,
            'MFS': FilingStatus.MARRIED_FILING_SEPARATELY,
            'HEAD_OF_HOUSEHOLD': FilingStatus.HEAD_OF_HOUSEHOLD,
            'HOH': FilingStatus.HEAD_OF_HOUSEHOLD
        }
        
        key = status.upper().replace(' ', '_').replace('-', '_')
        
        if key in status_map:
            return status_map[key]
        
        raise ValueError(f"Invalid filing status: '{status}'")


# ============================================================================
# FASTAPI APP
# ============================================================================

app = FastAPI(
    title="Quantum Financial Assistant",
    description="Created by Cole Sorokolit and Nic McLeod",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

quantum = QuantumEngine()


# Pydantic Models
class TaxCalculationRequest(BaseModel):
    income: float = Field(..., gt=0)
    filing_status: str
    year: int = Field(2025, ge=2024, le=2025)
    is_gross_income: bool = False


class TaxCalculationResponse(BaseModel):
    total_tax: float
    effective_rate: float
    marginal_rate: float
    breakdown: List[Dict[str, Any]]
    filing_status: str
    year: int
    taxable_income: float
    summary: str
    disclaimer: str


# ============================================================================
# HTML FRONTEND (EMBEDDED)
# ============================================================================

HTML_CONTENT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quantum Financial Assistant</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            line-height: 1.6;
            color: #212121;
            background: #fafafa;
        }
        .container { max-width: 1200px; margin: 0 auto; padding: 0 20px; }
        .header {
            background: white;
            border-bottom: 1px solid #e0e0e0;
            padding: 20px 0;
            box-shadow: 0 1px 3px rgba(0,0,0,0.12);
        }
        .logo {
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 24px;
            font-weight: 700;
            color: #1976d2;
        }
        .hero {
            background: linear-gradient(135deg, #1976d2 0%, #115293 100%);
            color: white;
            padding: 60px 0;
            text-align: center;
        }
        .hero h1 { font-size: 36px; margin-bottom: 10px; }
        .hero p { font-size: 18px; opacity: 0.9; }
        .main { padding: 40px 0; }
        .section { margin-bottom: 40px; }
        .section-title { font-size: 28px; margin-bottom: 20px; }
        .card {
            background: white;
            border-radius: 12px;
            padding: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .form-group { margin-bottom: 20px; }
        .form-label { display: block; font-weight: 600; margin-bottom: 8px; }
        .form-input, .form-select {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 16px;
        }
        .form-input:focus, .form-select:focus {
            outline: none;
            border-color: #1976d2;
        }
        .btn {
            padding: 12px 32px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
        }
        .btn-primary {
            background: #1976d2;
            color: white;
        }
        .btn-primary:hover {
            background: #115293;
            transform: translateY(-2px);
        }
        .results {
            margin-top: 30px;
            padding-top: 30px;
            border-top: 2px solid #e0e0e0;
        }
        .result-cards {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            margin: 20px 0;
        }
        .result-card {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 20px;
            border-radius: 12px;
            text-align: center;
        }
        .result-label {
            font-size: 12px;
            color: #757575;
            text-transform: uppercase;
            margin-bottom: 8px;
        }
        .result-value {
            font-size: 28px;
            font-weight: 700;
            color: #1976d2;
        }
        .disclaimer {
            background: #fff3e0;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #ff9800;
            margin-top: 20px;
        }
        .footer {
            background: #424242;
            color: white;
            padding: 30px 0;
            text-align: center;
            margin-top: 60px;
        }
        @media (max-width: 768px) {
            .result-cards { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <header class="header">
        <div class="container">
            <div class="logo">
                <span>🤖</span>
                <span>Quantum</span>
            </div>
        </div>
    </header>

    <section class="hero">
        <div class="container">
            <h1>Quantum Financial Assistant</h1>
            <p>Professional tax calculations and financial education</p>
            <p style="margin-top: 10px;">Created by <strong>Cole Sorokolit</strong> and <strong>Nic McLeod</strong></p>
        </div>
    </section>

    <main class="main">
        <div class="container">
            <section class="section">
                <h2 class="section-title">💰 Federal Income Tax Calculator</h2>
                
                <div class="card">
                    <form id="taxForm">
                        <div class="form-group">
                            <label class="form-label">Income Amount ($)</label>
                            <input type="number" id="income" class="form-input" placeholder="75000" required>
                        </div>
                        
                        <div class="form-group">
                            <label class="form-label">Filing Status</label>
                            <select id="filingStatus" class="form-select" required>
                                <option value="">Select...</option>
                                <option value="Single">Single</option>
                                <option value="Married Filing Jointly">Married Filing Jointly</option>
                                <option value="Married Filing Separately">Married Filing Separately</option>
                                <option value="Head of Household">Head of Household</option>
                            </select>
                        </div>
                        
                        <div class="form-group">
                            <label class="form-label">Tax Year</label>
                            <select id="taxYear" class="form-select">
                                <option value="2025">2025</option>
                                <option value="2024">2024</option>
                            </select>
                        </div>
                        
                        <button type="submit" class="btn btn-primary">Calculate Tax</button>
                    </form>
                    
                    <div id="results" style="display: none;" class="results">
                        <h3>Results</h3>
                        <div class="result-cards">
                            <div class="result-card">
                                <div class="result-label">Total Tax</div>
                                <div id="totalTax" class="result-value">$0</div>
                            </div>
                            <div class="result-card">
                                <div class="result-label">Effective Rate</div>
                                <div id="effectiveRate" class="result-value">0%</div>
                            </div>
                            <div class="result-card">
                                <div class="result-label">Marginal Rate</div>
                                <div id="marginalRate" class="result-value">0%</div>
                            </div>
                        </div>
                        <div id="summary"></div>
                        <div id="disclaimer" class="disclaimer"></div>
                    </div>
                </div>
            </section>
        </div>
    </main>

    <footer class="footer">
        <div class="container">
            <p>© 2025 Quantum Financial Assistant</p>
            <p>Created by <strong>Cole Sorokolit</strong> and <strong>Nic McLeod</strong></p>
            <p style="margin-top: 10px; font-size: 14px;">For educational purposes only</p>
        </div>
    </footer>

    <!-- Q Chat Widget -->
    <div id="q-chat-widget" style="position: fixed; bottom: 20px; right: 20px; z-index: 9999;">
        <button id="q-chat-button" style="width: 60px; height: 60px; border-radius: 50%; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border: none; cursor: pointer; box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4); display: flex; align-items: center; justify-content: center; position: relative; transition: all 0.3s ease; font-size: 28px; font-weight: 700; color: white;">
            Q
        </button>
        
        <div id="q-chat-window" style="display: none; position: absolute; bottom: 80px; right: 0; width: 380px; height: 600px; background: white; border-radius: 16px; box-shadow: 0 12px 48px rgba(0, 0, 0, 0.15); flex-direction: column; overflow: hidden;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 16px; display: flex; justify-content: space-between; align-items: center;">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <div style="width: 40px; height: 40px; border-radius: 50%; background: white; color: #667eea; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 18px;">Q</div>
                    <div>
                        <div style="font-weight: 600; font-size: 16px;">Quantum Assistant</div>
                        <div style="font-size: 12px; opacity: 0.9;">Online</div>
                    </div>
                </div>
                <button id="q-close" style="background: rgba(255, 255, 255, 0.2); border: none; color: white; width: 32px; height: 32px; border-radius: 50%; cursor: pointer; font-size: 20px;">×</button>
            </div>
            
            <div id="q-messages" style="flex: 1; overflow-y: auto; padding: 16px; background: #f8f9fa;"></div>
            
            <div style="display: flex; gap: 8px; padding: 16px; background: white; border-top: 1px solid #e0e0e0; align-items: center;">
                <input type="text" id="q-input" placeholder="Ask about taxes or FDIC..." style="flex: 1; border: 1px solid #e0e0e0; border-radius: 20px; padding: 10px 16px; font-size: 14px; outline: none;">
                <button id="q-send" style="width: 40px; height: 40px; border-radius: 50%; background: #667eea; border: none; color: white; cursor: pointer; display: flex; align-items: center; justify-content: center;">➤</button>
            </div>
        </div>
    </div>

    <script>
        // Tax Calculator
        document.getElementById('taxForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const income = parseFloat(document.getElementById('income').value);
            const filingStatus = document.getElementById('filingStatus').value;
            const taxYear = parseInt(document.getElementById('taxYear').value);
            
            try {
                const response = await fetch('/api/calculate-tax', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        income: income,
                        filing_status: filingStatus,
                        year: taxYear
                    })
                });
                
                const data = await response.json();
                
                document.getElementById('totalTax').textContent = '$' + data.total_tax.toLocaleString('en-US', {minimumFractionDigits: 2});
                document.getElementById('effectiveRate').textContent = data.effective_rate.toFixed(2) + '%';
                document.getElementById('marginalRate').textContent = data.marginal_rate.toFixed(0) + '%';
                document.getElementById('summary').innerHTML = '<p style="margin: 20px 0;">' + data.summary + '</p>';
                document.getElementById('disclaimer').innerHTML = '<strong>⚠️ Disclaimer:</strong><p style="margin-top: 8px;">' + data.disclaimer + '</p>';
                
                document.getElementById('results').style.display = 'block';
                document.getElementById('results').scrollIntoView({ behavior: 'smooth' });
                
            } catch (error) {
                alert('Error calculating tax. Please try again.');
            }
        });

        // Q Chat Widget
        const chatButton = document.getElementById('q-chat-button');
        const chatWindow = document.getElementById('q-chat-window');
        const closeBtn = document.getElementById('q-close');
        const messagesDiv = document.getElementById('q-messages');
        const input = document.getElementById('q-input');
        const sendBtn = document.getElementById('q-send');
        
        let isOpen = false;
        
        // Welcome message
        addMessage("👋 Hi! I'm <strong>Q</strong>, your Quantum assistant created by Cole Sorokolit and Nic McLeod.<br><br>I can help with:<br>• Tax calculations<br>• FDIC insurance<br>• Financial questions<br><br>Try asking: 'Calculate tax on $75,000' or 'What is FDIC?'", 'bot');
        
        chatButton.addEventListener('click', () => {
            isOpen = !isOpen;
            chatWindow.style.display = isOpen ? 'flex' : 'none';
            if (isOpen) input.focus();
        });
        
        closeBtn.addEventListener('click', () => {
            isOpen = false;
            chatWindow.style.display = 'none';
        });
        
        sendBtn.addEventListener('click', () => sendMessage());
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') sendMessage();
        });
        
        function sendMessage() {
            const text = input.value.trim();
            if (!text) return;
            
            addMessage(text, 'user');
            input.value = '';
            
            setTimeout(() => {
                const response = getResponse(text);
                addMessage(response, 'bot');
            }, 500);
        }
        
        function getResponse(text) {
            const lower = text.toLowerCase();
            
            if (lower.includes('tax') && (lower.includes('calculate') || lower.match(/\d+/))) {
                return "I can help calculate taxes! 💰<br><br>Use the tax calculator above, or tell me:<br>• Your income amount<br>• Filing status<br>• Tax year<br><br>Example: 'Calculate tax for $75,000, single, 2025'";
            }
            
            if (lower.includes('fdic') || lower.includes('insurance')) {
                return "🏦 <strong>FDIC Insurance</strong><br><br>FDIC insures deposits up to <strong>$250,000</strong> per depositor, per bank, per ownership category.<br><br><strong>Covered:</strong> Checking, savings, CDs<br><strong>Not covered:</strong> Stocks, bonds, crypto<br><br>Want more details? Scroll down to the FDIC section!";
            }
            
            if (lower.includes('help') || lower.includes('what can')) {
                return "I'm Q, your Quantum financial assistant! 👋<br><br><strong>I can help with:</strong><br>• Federal tax calculations<br>• FDIC insurance info<br>• Filing status questions<br>• Financial education<br><br>Try: 'Calculate tax on $50,000' or 'Explain FDIC'";
            }
            
            if (lower.includes('who made') || lower.includes('creator')) {
                return "I was created by <strong>Cole Sorokolit</strong> and <strong>Nic McLeod</strong>! 👥<br><br>They built Quantum to make financial calculations accessible to everyone.";
            }
            
            const incomeMatch = text.match(/\$?([\d,]+)/);
            if (incomeMatch) {
                const amount = incomeMatch[1].replace(/,/g, '');
                return `Great! I can calculate tax on $${parseInt(amount).toLocaleString()}.<br><br>What's your filing status?<br>• Single<br>• Married Filing Jointly<br>• Married Filing Separately<br>• Head of Household<br><br>Or use the calculator above for instant results!`;
            }
            
            return "That's a great question! For calculations, please use the tools above:<br><br>• <strong>Tax Calculator</strong> for income tax<br>• <strong>FDIC Section</strong> (coming soon)<br><br>Or ask me about:<br>• How taxes work<br>• FDIC insurance basics<br>• Filing statuses";
        }
        
        function addMessage(text, sender) {
            const msgDiv = document.createElement('div');
            msgDiv.style.cssText = 'display: flex; gap: 8px; margin-bottom: 16px; ' + (sender === 'user' ? 'flex-direction: row-reverse;' : '');
            
            const time = new Date().toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' });
            
            if (sender === 'bot') {
                msgDiv.innerHTML = `
                    <div style="width: 32px; height: 32px; border-radius: 50%; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 14px; flex-shrink: 0;">Q</div>
                    <div style="max-width: 70%; background: white; color: #333; border-radius: 16px 16px 16px 4px; padding: 12px 16px; box-shadow: 0 2px 4px rgba(0,0,0,0.08);">
                        <div style="font-size: 14px; line-height: 1.5;">${text}</div>
                        <div style="font-size: 11px; opacity: 0.6; margin-top: 4px;">${time}</div>
                    </div>
                `;
            } else {
                msgDiv.innerHTML = `
                    <div style="max-width: 70%; background: #667eea; color: white; border-radius: 16px 16px 4px 16px; padding: 12px 16px;">
                        <div style="font-size: 14px; line-height: 1.5;">${text}</div>
                        <div style="font-size: 11px; opacity: 0.8; margin-top: 4px;">${time}</div>
                    </div>
                `;
            }
            
            messagesDiv.appendChild(msgDiv);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }
    </script>
</body>
</html>
"""


# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve main page"""
    return HTML_CONTENT


@app.get("/health")
async def health():
    """Health check"""
    return {
        "status": "healthy",
        "version": "2.0.0",
        "creators": "Cole Sorokolit and Nic McLeod"
    }


@app.post("/api/calculate-tax", response_model=TaxCalculationResponse)
async def calculate_tax(request: TaxCalculationRequest):
    """Calculate federal income tax"""
    try:
        result = quantum.calculate_tax(
            income=request.income,
            filing_status=request.filing_status,
            year=request.year,
            is_gross=request.is_gross_income
        )
        return TaxCalculationResponse(**result.to_dict())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/fdic-info")
async def get_fdic_info():
    """Get FDIC information"""
    return quantum.get_fdic_info()


@app.get("/api/creators")
async def get_creators():
    """Get creator information"""
    return {
        "creators": "Cole Sorokolit and Nic McLeod",
        "version": "2.0.0"
    }


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port)
