from collabinnovate.manage_problems.model import Problem
from collabinnovate import db

def updateParticipation(id):
    problem = Problem.query.filter_by(id = id).first()
    problem.participations += 1
    db.session.add(problem) 