from datetime import datetime
import random
from flask import Blueprint, json, jsonify, request
from collabinnovate import db
from faker import Faker
from sqlalchemy.exc import SQLAlchemyError
from collabinnovate.manage_problems.model import Problem
from collabinnovate.manage_problems.utilities import updateParticipation
from collabinnovate.manage_solutions.model import Solution
from collabinnovate.manage_user_accounts.account.model import Account
from collabinnovate.manage_user_accounts.user.model import User


solutions = Blueprint('solutions', __name__)
fake = Faker()

def faker_solution():
    user_ids = list(range(1, 21))
    problems = list(range(1, 1001))
    users = User.query.filter_by(role_id = 1).all()

    solution = Solution(
        user_id=fake.random_element(elements=user_ids),
        problem_id=fake.random_element(elements=problems),
        title=fake.company(),
        author = random.choice(users).full_name,
        dateAdded=datetime.utcnow(),
        gpsposition={
            'latitude': float(fake.latitude()),
            'longitude': float(fake.longitude())
        },
        description=fake.paragraph(),
        product_offered=fake.word(),
        service_offered=fake.word(),
        customer_expectations=fake.paragraph(),
        what_company_sells=fake.word(),
        how_product_service_marketed=fake.paragraph(),
        customer_access_method=fake.word(),
        competitors=json.dumps([fake.company() for _ in range(random.randint(1, 5))]),
        direct_sales=fake.boolean(),
        retail_sales=fake.boolean(),
        direct_sales_details=fake.paragraph(),
        wholesale=fake.boolean(),
        informal=fake.boolean(),
        advertising=fake.boolean(),
        direct_marketing=fake.boolean(),
        sales_promotion=fake.boolean(),
        display=fake.boolean(),
        word_of_mouth=fake.boolean(),
        trade_show=fake.boolean(),
        mail_order=fake.boolean(),
        human_resources=json.dumps([
            {
                "position": fake.job(),
                "tasks_to_perform": fake.sentence(),
                "required_skills_experience": fake.sentence(),
                "ideal_profile": fake.sentence(),
                "monthly_salary": fake.random_int(1000, 5000)
            }
        ]),
        legal_form=fake.word(),
        financing_needed=fake.word(),
        investment_characteristics=fake.paragraph(),
        suppliers=json.dumps([fake.company() for _ in range(random.randint(1, 5))]),
        variable_cost=json.dumps({
            "variable_cost": fake.random_int(100, 1000)
        }),
        fixed_cost=json.dumps({
            "fixed_cost": fake.random_int(100, 1000)
        }),
        offers=json.dumps([
            {
                "Offer_Name": fake.word(),
                "Offer_Price": fake.random_int(10, 100),
                "Quantity_Sold": fake.random_int(1, 10),
                "Revenue_Generated": fake.random_int(100, 1000),
                "For_One_Month": fake.random_int(100, 1000),
                "For_Three_Months": fake.random_int(300, 3000),
                "For_Six_Months": fake.random_int(600, 6000),
                "For_One_Year": fake.random_int(1000, 10000),
                "For_Three_Years": fake.random_int(3000, 30000)
            }
        ]),
        quantity_sold=fake.random_int(1, 10),
        revenue_generated=json.dumps({
            "revenue_generated": fake.random_int(100, 1000)
        }),
        gross_margin=fake.random_int(100, 1000),
        net_profit=json.dumps({
            "net_profit": fake.random_int(100, 1000)
        }),
        cash_flow_plan=json.dumps({
            "cash_flow_plan": fake.random_int(100, 1000)
        }),
        financing_need=fake.random_int(100, 1000),
        financing_phase=fake.word(),
        financing_source=json.dumps([
            {
                "source": fake.company(),
                "amount": fake.random_int(1000, 10000)
            }
        ]),
        remuneration_type=fake.word(),
        impactful_introduction=fake.paragraph(),
        specific_problem_addressing=fake.paragraph(),
        innovative_solution_proposal=fake.paragraph(),
        team_presentation=fake.paragraph(),
        startup_costs_explanation=fake.paragraph(),
        necessary_capital_explanation=fake.paragraph(),
        expected_revenue_explanation=fake.paragraph(),
        investment_return_demonstration=fake.paragraph(),
        strategicpillar=fake.word()
    )

    db.session.add(solution)
    db.session.commit()


@solutions.route("/thousand_solution", methods=["POST"])
def thousand_solution():
    for _ in range(1000):
        faker_solution()
    return jsonify(message = "les 1000 solutions ont été enregistré")


# Route pour créer une nouvelle solution

@solutions.route('/add/<email>/<problemId>', methods=['POST'])
def create_solution(email, problemId):
    # try:
        data = request.get_json()
        user = User.query.filter_by(email=email).first()

        # Extract competitors, humans, suppliers, fixedcosts, variablecosts, offers from FormData
        competitors = data.get('competitors')
        humans = data.get('humans')
        suppliers = data.get('investment[suppliers]')
        fixedcosts = data.get('fixedcosts')
        variablecosts = data.get('variablecosts')
        offers = data.get('financialforecast[offers]')


        # Create new solution instance
        new_solution = Solution(
            title=data.get('solutionTitle'),
            problem_id=problemId,
            user_id=user.id,
            author = user.full_name,

            # Solution information fields
            description=data.get('aboutSolution'),
            product_offered=data.get('productsOnOffer'),
            service_offered=data.get('servicesOnOffer'),
            customer_expectations=data.get('customerExpectations'),
            what_company_sells=data.get('companySales'),
            how_product_service_marketed=data.get('how_product_service_marketed'),
            customer_access_method=data.get('customer_access_method'),
            
            # Distribution channels fields
            direct_sales=data.get('directSales'),
            wholesale=data.get('wholesale'),
            informal=data.get('informalSales'),
            retail_sales=data.get('retailSales'),
            
            # Promotion means fields
            advertising=data.get('advertising'),
            direct_marketing=data.get('directMarketing'),
            sales_promotion=data.get('salesPromotion'),
            display=data.get('display'),
            word_of_mouth=data.get('wordOfMouth'),
            trade_show=data.get('tradeShow'),
            mail_order=data.get('mailOrder'),
            
            # Competitors and human resources fields
            competitors=competitors,
            human_resources=humans,
            
            # Legal form field
            legal_form=data.get('legalForm'),
            
            # Required investment fields
            financing_needed=data.get('investment')["needs"],
            investment_characteristics=data.get('investment')["characteristics"],
            suppliers=suppliers,
            
            # Working capital fields
            variable_cost=variablecosts,
            fixed_cost=fixedcosts,
            
            # Financial forecast fields
            offers=offers,
            quantity_sold= data.get('financialforecast')["quantitysold"],
            revenue_generated={
                'firstmonth': data.get('financialforecast')["salesgenerated"]["firstmonth"],
                'thirdmonth': data.get('financialforecast')["salesgenerated"]["thirdmonth"],
                'sixthmonth': data.get('financialforecast')["salesgenerated"]["sixthmonth"],
                'firstyear': data.get('financialforecast')["salesgenerated"]["firstyear"],
                'thirdyear': data.get('financialforecast')["salesgenerated"]["thirdyear"],
            },
            
            # Cash flow plan fields
            cash_flow_plan={
                'firstmonth': data.get('cashflowfirstmonth'),
                'thirdmonth': data.get('cashflowthirdmonth'),
                'sixthmonth': data.get('cashflowsixthmonth'),
                'firstyear': data.get('cashflowfirstyear'),
                'thirdyear': data.get('cashflowthirdyear'),
            },
            
            # Financing need field
            financing_need=data.get('financingNeed'),
            
            # Financing phase fields
            financing_phase=data.get('financingPhase'),
            
            # Financing source fields
            financing_source={
                'equitycapital': {
                    'privatesavings': data.get('financingSource')["equitycapital"]["privatesavings"],
                    'privatesphere': data.get('financingSource')["equitycapital"]["privatesphere"],
                    'privateshareholders': data.get('financingSource')["equitycapital"]["privateshareholders"],
                    'startupsponsors': data.get('financingSource')["equitycapital"]["startupsponsors"],
                    'businessagents': data.get('financingSource')["equitycapital"]["businessagents"],
                    'incubatorandbusinessincubator': data.get('financingSource')["equitycapital"]["incubatorandbusinessincubator"],
                    'mixedcapital': data.get('financingSource')["equitycapital"]["mixedcapital"],
                },
                'creditsource': {
                    'bankCredit': data.get('financingSource')["creditsource"]["bankCredit"],
                    'startupLaunchCredit': data.get('financingSource')["creditsource"]["startupLaunchCredit"],
                    'mezzanineFinancing': data.get('financingSource')["creditsource"]["mezzanineFinancing"],
                    'other': data.get('financingSource')["creditsource"]["other"],
                },
                'publicSubsidyforBusinessCreation': {
                    'businessstartupprogram': data.get('financingSource')["publicSubsidyforBusinessCreation"]["businessstartupprogram"],
                    'startupCompetition': data.get('financingSource')["publicSubsidyforBusinessCreation"]["startupCompetition"],
                    'other': data.get('financingSource')["publicSubsidyforBusinessCreation"]["other"],
                },
                'crowdfundingSources': {
                    'crowdfunding': data.get('financingSource')["crowdfundingSources"]["crowdfunding"],
                    'crowdInvesting': data.get('financingSource')["crowdfundingSources"]["crowdInvesting"],
                    'crowdLending': data.get('financingSource')["crowdfundingSources"]["crowdLending"],
                    'other': data.get('financingSource')["crowdfundingSources"]["other"],
                },
            },
            
            # Capital provider remuneration strategy field
            remuneration_type=data.get('remunerationType'),
            
            # Strategy mobilized pillars fields
            strategicpillar=data.get('pillar'),
        )
        updateParticipation(problemId)

        db.session.add(new_solution)
        db.session.commit()
        return jsonify({'message': 'The solution has been added with success'}), 201
    # except SQLAlchemyError as e:
    #     db.session.rollback()
    #     return jsonify({'message': 'Registration error'}), 400
    # except Exception as e:

    #     return jsonify({'message': 'Registration error'}), 500
    

# Route pour obtenir toutes les solutions d'un problem
@solutions.route('/all/<problemID>', methods=['GET'])
def get_all_solutions(problemID):
    try:
        solutions_query = Solution.query.filter_by(problem_id=problemID).all()
        if not solutions_query:
            return jsonify({"error": "No solutions found for the given problem ID"}), 404
        
        solutions_list = [solution.to_dict() for solution in solutions_query]
        return jsonify(solutions_list), 200
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500

    except Exception as e:
        return jsonify({"error": "An unexpected error occurred: "}), 500
    
@solutions.route('/getall/<id>', methods=['GET'])
def get_all_usersolution(id):
    allsolution = []
    try:
        user  = User.query.filter_by(email = id).first()
        if user:
            
        
            problems_query = Problem.query.filter_by(user_id = user.id).all() 
            problems_list = [problem.to_dict() for problem in problems_query]
            if problems_query :
                for problem in problems_query:
                    solutionByProblem_query = Solution.query.filter_by(problem_id = problem.id).all()
                    if solutionByProblem_query:
                        solutions = [solution.to_dict() for solution in solutionByProblem_query]
                        for solution in solutions:
                            allsolution.append(solution)
                return jsonify({'problems': problems_list, 'solutions' : list(allsolution), 'user_id': user.id}), 200
        else:
            return jsonify({'message': "user not found"}), 404
    except SQLAlchemyError as e:
        return jsonify({"error": "error"}), 500

    except Exception as e:
        return jsonify({"error": "An unexpected error occurred: "}), 500


@solutions.route('/get/<int:solution_id>', methods=['GET'])
def get_solution(solution_id):
    try:
        solution = Solution.query.get(solution_id)
        if solution:
            user = User.query.filter_by(id = solution.user_id).first()
            return jsonify({"message": solution.to_dict(), "user": user.email}), 200
        else:
            return jsonify({"error": "Solution not found"}), 404
    except Exception as e:
        return jsonify({"error": "An error occurred while retrieving the solution"}), 500

# Route pour mettre à jour une solution existante
@solutions.route('/update/<int:solution_id>', methods=['PUT'])
def update_solution(solution_id):
    solution = Solution.query.get(solution_id)
    if not solution:
        return jsonify({'message': 'Solution non trouvée'}), 404
    data = request.json
    solution.title = data.get('title', solution.title)
    solution.description = data.get('description', solution.description)
    # Mettez à jour les autres champs au besoin
    db.session.commit()
    return jsonify({'message': 'Solution mise à jour avec succès'}), 200

# Route pour supprimer une solution existante
@solutions.route('/delete/<int:solution_id>', methods=['DELETE'])
def delete_solution(solution_id):
    solution = Solution.query.get(solution_id)
    if not solution:
        return jsonify({'message': 'Solution non trouvée'}), 404
    db.session.delete(solution)
    db.session.commit()
    return jsonify({'message': 'Solution supprimée avec succès'}), 200

