"""
Mock HR data.

Replace this module with real data access (a database, an HRIS API like
BambooHR/Workday, a document store, etc.) later -- the MCP server code in
hr_mcp_server.py doesn't need to change, only how POLICIES / BENEFITS / FAQS
are populated.
"""

POLICIES: dict[str, str] = {
    "Remote Work Policy": (
        "Employees may work remotely up to 3 days per week, subject to "
        "manager approval. Fully remote arrangements require VP-level "
        "sign-off. Remote employees must be reachable during core hours "
        "(10am-4pm in their local time zone) and attend all-hands meetings "
        "via video with camera on. Home office equipment stipend: $500/year, "
        "submit receipts via the Expenses portal."
    ),
    "Paid Time Off (PTO) Policy": (
        "Full-time employees accrue 15 days of PTO per year for the first "
        "2 years, increasing to 20 days after 2 years and 25 days after 5 "
        "years. PTO accrues monthly and can be carried over up to 5 days "
        "into the next calendar year; unused balances beyond that are "
        "forfeited (except where local law requires payout). Request PTO "
        "at least 5 business days in advance via the HR portal."
    ),
    "Sick Leave Policy": (
        "Employees receive 10 paid sick days per year, separate from PTO. "
        "Sick leave can be used for personal illness, medical appointments, "
        "or caring for an immediate family member. No doctor's note is "
        "required for absences under 3 consecutive days. Unused sick days "
        "do not carry over or pay out."
    ),
    "Parental Leave Policy": (
        "Birthing parents receive 16 weeks of paid leave; non-birthing "
        "parents and adoptive parents receive 8 weeks of paid leave. Leave "
        "can be taken continuously or split within the first 12 months "
        "after birth/adoption, with manager coordination. Job protection "
        "is guaranteed for the duration of leave."
    ),
    "Code of Conduct": (
        "All employees are expected to act with honesty, integrity, and "
        "respect toward colleagues, customers, and partners. Harassment, "
        "discrimination, and retaliation of any kind are strictly "
        "prohibited and should be reported to HR or via the anonymous "
        "ethics hotline. Conflicts of interest must be disclosed to your "
        "manager and HR."
    ),
    "Expense Reimbursement Policy": (
        "Business expenses under $75 do not require pre-approval; over $75 "
        "requires manager sign-off before purchase. Submit expense reports "
        "with itemized receipts within 30 days of the expense via the "
        "Expenses portal. Reimbursements are processed within 2 pay "
        "cycles."
    ),
    "Performance Review Policy": (
        "Formal performance reviews occur twice a year (April and October). "
        "Reviews include self-assessment, manager assessment, and peer "
        "feedback (360). Compensation changes tied to performance are "
        "communicated within 30 days of the review cycle closing."
    ),
    "Termination and Resignation Policy": (
        "Employees are asked to provide at least 2 weeks' written notice "
        "of resignation. Final paycheck, including accrued unused PTO, is "
        "issued per state/local law. Company property (laptop, badge, "
        "etc.) must be returned on or before the last day. Exit interviews "
        "are offered but optional."
    ),
}

BENEFITS: dict[str, str] = {
    "Health Insurance": (
        "The company offers three medical plan tiers (HDHP, PPO Standard, "
        "PPO Plus) through Aetna, plus dental and vision coverage. The "
        "company covers 80% of employee premiums and 60% of dependent "
        "premiums. Coverage begins on the 1st of the month following your "
        "start date. Open enrollment is held every November."
    ),
    "401(k)": (
        "Employees are eligible to contribute to the 401(k) plan "
        "(via Fidelity) starting on day one. The company matches 100% of "
        "the first 3% contributed and 50% of the next 2%, for a maximum "
        "match of 4%. Matching contributions vest immediately."
    ),
    "Stock Options / Equity": (
        "Eligible employees receive equity grants (RSUs or options "
        "depending on level) as part of their offer, vesting over 4 years "
        "with a 1-year cliff. Refresh grants are considered annually as "
        "part of the performance review cycle."
    ),
    "Wellness Stipend": (
        "Employees receive a $75/month wellness stipend that can be used "
        "for gym memberships, fitness classes, meditation apps, or "
        "therapy co-pays. Submit for reimbursement monthly via the "
        "Expenses portal; unused amounts do not roll over."
    ),
    "Learning & Development Budget": (
        "Each employee has an annual $1,500 L&D budget for courses, "
        "conferences, books, or certifications relevant to their role. "
        "Manager approval required for spends over $500. Unused budget "
        "does not carry over to the next year."
    ),
    "Commuter Benefits": (
        "Pre-tax commuter benefits are available for transit and parking "
        "up to the IRS monthly limit, administered through WageWorks. "
        "Enroll or change elections any time via the benefits portal; "
        "changes take effect the following month."
    ),
}

FAQS: list[dict] = [
    {
        "question": "How many vacation days do I get?",
        "answer": (
            "It depends on tenure: 15 days/year for your first 2 years, "
            "20 days after 2 years, and 25 days after 5 years. See the "
            "PTO Policy for accrual and carryover details."
        ),
    },
    {
        "question": "Can I work from home?",
        "answer": (
            "Yes -- up to 3 days/week with manager approval under the "
            "Remote Work Policy. Fully remote setups need VP sign-off."
        ),
    },
    {
        "question": "What's the parental leave policy?",
        "answer": (
            "Birthing parents get 16 weeks paid leave; non-birthing/"
            "adoptive parents get 8 weeks paid leave, usable within 12 "
            "months of the birth or adoption."
        ),
    },
    {
        "question": "Does the company match 401k contributions?",
        "answer": (
            "Yes -- 100% of the first 3% you contribute and 50% of the "
            "next 2%, up to a 4% match total, vesting immediately."
        ),
    },
    {
        "question": "How do I submit an expense report?",
        "answer": (
            "Submit itemized receipts through the Expenses portal within "
            "30 days of the purchase. Purchases over $75 need manager "
            "pre-approval."
        ),
    },
    {
        "question": "What happens to my unused PTO if I quit?",
        "answer": (
            "Accrued unused PTO is paid out with your final paycheck per "
            "state/local law. Sick leave does not pay out."
        ),
    },
    {
        "question": "How much notice do I need to give before resigning?",
        "answer": "At least 2 weeks' written notice, per company policy.",
    },
    {
        "question": "Is there a wellness or gym stipend?",
        "answer": (
            "Yes -- $75/month for gym, fitness classes, meditation apps, "
            "or therapy co-pays, reimbursed monthly."
        ),
    },
    {
        "question": "When is open enrollment for health insurance?",
        "answer": "Every November, for coverage effective the following January.",
    },
    {
        "question": "How often are performance reviews?",
        "answer": (
            "Twice a year, in April and October, including self, manager, "
            "and peer (360) feedback."
        ),
    },
]
