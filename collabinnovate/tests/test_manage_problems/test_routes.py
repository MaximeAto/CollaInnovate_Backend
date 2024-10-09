import pytest
from collabinnovate.manage_problems.model import Problem
from collabinnovate.manage_user_accounts.user.model import User
from datetime import datetime

# Test de la création d'un problème
def test_create_problem(test_client, init_database):

    # Créer des données JSON valides pour la création d'un problème
    problem_data = {
        'user_id': 1,  # Assurez-vous que cet ID utilisateur existe dans votre base de données
        'problemTitle': 'Test Problem',  # Correspond à 'problemTitle'
        'aboutProblem': 'This is a test problem description.',  # Correspond à 'aboutProblem'
        'category': 'Technology',  # Correspond à 'category'
        'country': 'Test Country',  # Ajouté pour correspondre au champ 'country'
        'city': 'Test City',  # Ajouté pour correspondre au champ 'city'
        'deadline': '2024-12-31',  # Format ISO 8601 pour la date
        'business_needs_improvement': 'Test business needs improvement',  # Correspond à 'business_needs_improvement'
        'population_affected': 'Test population',  # Correspond à 'population_affected'
        'concern_population_affected': 'Test concern',  # Correspond à 'concern_population_affected'
        'impacts_on_these_populations': 'Test impact',  # Correspond à 'impacts_on_these_populations'
        'population_volume': 500  # Correspond à 'population_volume'
    }


    response = test_client.post(f'problems/add/test_user@example.com', json=problem_data)
    assert response.status_code == 201
    assert 'The problem has been added with success' in response.get_json()['message']


# Test pour obtenir tous les problèmes
def test_get_all_problems(test_client, init_database):


    response = test_client.get(f'problems/all/test_user@example.com')
    assert response.status_code == 200
    assert 'problems' in response.get_json()


# Test pour obtenir un problème spécifique
def test_get_problem_by_id(test_client, init_database):

    # Créer un problème de test
    problem = Problem(
        user_id=1, author="Test Author", title="Test Problem",
        about_problem="Test description", category="Technology",
        deadline=datetime(2024, 12, 31),
        activity_requiring_improvement="Improvement needed"
    )
    init_database.session.add(problem)
    init_database.session.commit()

    # Tester la récupération du problème
    response = test_client.get(f'problems/get/{problem.id}')
    assert response.status_code == 200
    assert 'Test Problem' in response.get_json()['message']['title']


# Test de la mise à jour d'un problème
def test_update_problem(test_client, init_database):


    # Créer un problème de test
    problem = Problem(
        user_id=1, author="Test Author", title="Problem to Update",
        about_problem="Test description", category="Technology",
        deadline=datetime(2024, 12, 31),
        activity_requiring_improvement="Needs improvement"
    )
    init_database.session.add(problem)
    init_database.session.commit()

    # Mise à jour des données du problème
    updated_data = {
        'title': 'Updated Problem',
        'activity_requiring_improvement': 'Updated improvement',
        'about_problem': 'Updated description',  
        'category': 'Technology',  
        'deadline': '2025-01-01' 
    }

    # Mettre à jour le problème
    response = test_client.put(f'problems/update/{problem.id}', json=updated_data)
    assert response.status_code == 201
    


# Test de la suppression d'un problème
def test_delete_problem(test_client, init_database):

    # Créer un problème de test
    problem = Problem(
        user_id=1, author="Test Author", title="Problem to Delete",
        about_problem="Test description", category="Technology",
        deadline=datetime(2024, 12, 31),
        activity_requiring_improvement="Needs improvement"
    )
    init_database.session.add(problem)
    init_database.session.commit()

    # Supprimer le problème
    response = test_client.delete(f'problems/delete/{problem.id}')
    assert response.status_code == 200
    assert 'Le problème a été supprimé avec succès' in response.get_json()['message']
