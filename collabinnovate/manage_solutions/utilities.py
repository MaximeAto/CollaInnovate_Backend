from collabinnovate.manage_problems.model import Problem
from collabinnovate import db


class Competitor:
  def __init__(self, name, strengths, weaknesses, competitive_advantage):
    self.name = name
    self.strengths = strengths
    self.weaknesses = weaknesses
    self.competitive_advantage = competitive_advantage

  
class HumanResource:
  def __init__(self, position, tasks_to_perform, required_skills_experience, ideal_profile, monthly_salary):
    self.position = position
    self.tasks_to_perform = tasks_to_perform
    self.required_skills_experience = required_skills_experience
    self.ideal_profile = ideal_profile
    self.monthly_salary = monthly_salary
    
class GeneratedRevenue:
    def __init__(self, month, three_months, six_months, one_year, three_years):
        self.month = month
        self.three_months = three_months
        self.six_months = six_months
        self.one_year = one_year
        self.three_years = three_years

