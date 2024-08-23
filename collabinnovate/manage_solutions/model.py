from datetime import datetime
from collabinnovate import db
from sqlalchemy import JSON

class Solution(db.Model):
    __tablename__ = "solutions"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    problem_id = db.Column(db.Integer, db.ForeignKey('problems.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    dateAdded = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    gpsposition = db.Column(JSON)
    
    # Solution information fields
    description = db.Column(db.Text, nullable=False)
    product_offered = db.Column(db.String(100))
    service_offered = db.Column(db.String(100))
    customer_expectations = db.Column(db.Text)
    what_company_sells = db.Column(db.String(100))
    how_product_service_marketed = db.Column(db.Text)
    customer_access_method = db.Column(db.String(100))

    competitors = db.Column(JSON)

    # Distribution channels fields
    direct_sales = db.Column(db.Boolean)
    retail_sales = db.Column(db.Boolean)  # changed to snake_case
    direct_sales_details = db.Column(db.Text)
    wholesale = db.Column(db.Boolean)
    informal = db.Column(db.Boolean)

    # Promotion means fields
    advertising = db.Column(db.Boolean)
    direct_marketing = db.Column(db.Boolean)
    sales_promotion = db.Column(db.Boolean)
    display = db.Column(db.Boolean)
    word_of_mouth = db.Column(db.Boolean)
    trade_show = db.Column(db.Boolean)
    mail_order = db.Column(db.Boolean)

    # Human resources fields
    human_resources = db.Column(JSON)

    # Legal form field
    legal_form = db.Column(db.String(100))

    # Required investment fields
    financing_needed = db.Column(db.String(100))
    investment_characteristics = db.Column(db.Text)
    suppliers = db.Column(JSON)

    # Working capital fields
    variable_cost = db.Column(JSON)
    fixed_cost = db.Column(JSON)

    # Financial forecast fields
    offers = db.Column(JSON)
    quantity_sold = db.Column(db.Float, default=0.0)
    revenue_generated = db.Column(JSON)

    # Profit generation fields
    gross_margin = db.Column(db.Float, default=0.0)
    net_profit = db.Column(JSON)

    # Cash flow plan fields
    cash_flow_plan = db.Column(JSON)  # changed to snake_case

    # Financing need field
    financing_need = db.Column(db.Float, default=0.0)

    # Financing phase fields
    financing_phase = db.Column(db.String(100))

    # Financing source fields
    financing_source  = db.Column(JSON)

    # Capital provider remuneration strategy field
    remuneration_type = db.Column(db.String(100))

    # Executive summary production fields
    impactful_introduction = db.Column(db.Text)
    specific_problem_addressing = db.Column(db.Text)
    innovative_solution_proposal = db.Column(db.Text)
    team_presentation = db.Column(db.Text)
    startup_costs_explanation = db.Column(db.Text)
    necessary_capital_explanation = db.Column(db.Text)
    expected_revenue_explanation = db.Column(db.Text)
    investment_return_demonstration = db.Column(db.Text)

    # Strategy mobilized pillars fields
    strategicpillar = db.Column(db.String(100))

    comments = db.relationship('Comment', backref='solution')
    mention = db.relationship('Mention', backref='solution', uselist=False)



    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'problem_id': self.problem_id,
            'author': self.author,
            'user_id': self.user_id,
            'description': self.description,
            'gpsposition': self.gpsposition,
            'dateAdded': self.dateAdded,
            'product_offered': self.product_offered,
            'service_offered': self.service_offered,
            'customer_expectations': self.customer_expectations,
            'what_company_sells': self.what_company_sells,
            'how_product_service_marketed': self.how_product_service_marketed,
            'customer_access_method': self.customer_access_method,
            'competitors': self.competitors,
            'direct_sales': self.direct_sales,
            'retail_sales': self.retail_sales,
            'direct_sales_details': self.direct_sales_details,
            'wholesale': self.wholesale,
            'informal': self.informal,
            'advertising': self.advertising,
            'direct_marketing': self.direct_marketing,
            'sales_promotion': self.sales_promotion,
            'display': self.display,
            'word_of_mouth': self.word_of_mouth,
            'trade_show': self.trade_show,
            'mail_order': self.mail_order,
            'human_resources': self.human_resources,
            'legal_form': self.legal_form,
            'financing_needed': self.financing_needed,
            'investment_characteristics': self.investment_characteristics,
            'suppliers': self.suppliers,
            'variable_cost': self.variable_cost,
            'fixed_cost': self.fixed_cost,
            'offers': self.offers,
            'quantity_sold': self.quantity_sold,
            'revenue_generated': self.revenue_generated,
            'gross_margin': self.gross_margin,
            'net_profit': self.net_profit,
            'cash_flow_plan': self.cash_flow_plan,
            'financing_need': self.financing_need,
            'financing_phase': self.financing_phase,
            'financing_source': self.financing_source,
            'remuneration_type': self.remuneration_type,
            'impactful_introduction': self.impactful_introduction,
            'specific_problem_addressing': self.specific_problem_addressing,
            'innovative_solution_proposal': self.innovative_solution_proposal,
            'team_presentation': self.team_presentation,
            'startup_costs_explanation': self.startup_costs_explanation,
            'necessary_capital_explanation': self.necessary_capital_explanation,
            'expected_revenue_explanation': self.expected_revenue_explanation,
            'investment_return_demonstration': self.investment_return_demonstration,
            'strategicpillar': self.strategicpillar
        }