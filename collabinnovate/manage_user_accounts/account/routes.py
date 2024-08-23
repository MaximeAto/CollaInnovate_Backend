from faker import Faker
from flask import Blueprint, jsonify, request
from collabinnovate import db,Group,Role
from collabinnovate.manage_user_accounts.account.model import Account
from collabinnovate.manage_user_accounts.account.mashmallow import MashmallowAccount


accounts = Blueprint('accounts', __name__)
ma = MashmallowAccount()
fake = Faker()


@accounts.route("/hundred_accounts", methods=['POST'])
def hundred_candidates():
    users_id = list(range(1, 21))
    
    for _ in range(20):
        
        account = Account(
            user_id=fake.random_element(elements=users_id),
            type_account=fake.random_element(elements=("SO","PP","CO")),
            role=fake.random_element(elements=("SO","PP","CO"))
        )
        
        db.session.add(account)
        db.session.commit()
    return jsonify(message = "les 20 accounts ont été enregistré")

# Route pour créer un compte
@accounts.route('/account/create', methods=['POST'])
def create_account():
    try:
        data = request.json
        account = Account(
            user_id=data.get('user_id'),
            type_account=data.get('type_account'),
            account_details=data.get('account_details'),
            role=data.get('role')
        )
        db.session.add(account)
        db.session.commit()
        return ma.jsonify(account), 201
    except Exception as e:
        return jsonify({'message': 'Failed to create account.', 'error': str(e)}), 500



# Route pour récupérer un compte par ID
@accounts.route('/account/<int:account_id>', methods=['GET'])
def get_account(account_id):
    try:
        account = Account.query.get(account_id)
        if not account:
            return jsonify({'message': 'Account not found.'}), 404
        return ma.jsonify(account), 200
    except Exception as e:
        return jsonify({'message': 'Failed to get account.', 'error': str(e)}), 500



# Route pour mettre à jour un compte par ID
@accounts.route('/account/<int:account_id>', methods=['PUT'])
def update_account(account_id):
    try:
        data = request.json
        account = Account.query.get(account_id)
        if not account:
            return jsonify({'message': 'Account not found.'}), 404
        
        account.user_id = data.get('user_id', account.user_id)
        account.type_account = data.get('type_account', account.type_account)
        account.account_details = data.get('account_details', account.account_details)
        account.role = data.get('role', account.role)
        
        db.session.commit()
        return jsonify({'message': 'Account updated successfully.'}), 200
    except Exception as e:
        return jsonify({'message': 'Failed to update account.', 'error': str(e)}), 500



# Route pour supprimer un compte par ID
@accounts.route('/account/<int:account_id>', methods=['DELETE'])
def delete_account(account_id):
    try:
        account = Account.query.get(account_id)
        if not account:
            return jsonify({'message': 'Account not found.'}), 404
        
        db.session.delete(account)
        db.session.commit()
        return jsonify({'message': 'Account deleted successfully.'}), 200
    except Exception as e:
        return jsonify({'message': 'Failed to delete account.', 'error': str(e)}), 500



# Route pour récupérer les détails d'un compte par ID
@accounts.route('/account/<int:account_id>/details', methods=['GET'])
def get_account_details(account_id):
    try:
        account = Account.query.get(account_id)
        if not account:
            return jsonify({'message': 'Account not found.'}), 404
        return ma.jsonify(account), 200
    except Exception as e:
        return jsonify({'message': 'Failed to get account details.', 'error': str(e)}), 500



# Route pour mettre à jour les détails d'un compte par ID
@accounts.route('/account/<int:account_id>/details', methods=['PUT'])
def update_account_details(account_id):
    try:
        data = request.json
        account = Account.query.get(account_id)
        if not account:
            return jsonify({'message': 'Account not found.'}), 404
        
        account.account_details = data.get('account_details', account.account_details)
        
        db.session.commit()
        return jsonify({'message': 'Account details updated successfully.'}), 200
    except Exception as e:
        return jsonify({'message': 'Failed to update account details.', 'error': str(e)}), 500



# Route pour mettre à jour le mot de passe d'un compte par ID
@accounts.route('/account/<int:account_id>/password', methods=['PUT'])
def update_account_password(account_id):
    try:
        data = request.json
        new_password = data.get('password')
        if not new_password:
            return jsonify({'message': 'New password is required.'}), 400
        
        account = Account.query.get(account_id)
        if not account:
            return jsonify({'message': 'Account not found.'}), 404
        
        account.password = new_password
        db.session.commit()
        return jsonify({'message': 'Account password updated successfully.'}), 200
    except Exception as e:
        return jsonify({'message': 'Failed to update account password.', 'error': str(e)}), 500



# Route pour récupérer les invitations d'un compte par ID
@accounts.route('/account/<int:account_id>/invitations', methods=['GET'])
def get_account_invitations(account_id):
    try:
        account = Account.query.get(account_id)
        if not account:
            return jsonify({'message': 'Account not found.'}), 404
        
        invitations = [invitation.to_dict() for invitation in account.invitations]
        return jsonify({'message': 'Get account invitations by ID.', 'invitations': invitations}), 200
    except Exception as e:
        return jsonify({'message': 'Failed to get account invitations.', 'error': str(e)}), 500



# Route pour mettre à jour les rôles d'un compte par ID
@accounts.route('/account/<int:account_id>/roles', methods=['PUT'])
def update_account_roles(account_id):
    try:
        data = request.json
        role_names = data.get('roles')
        if not role_names:
            return jsonify({'message': 'Role names are required.'}), 400
        
        account = Account.query.get(account_id)
        if not account:
            return jsonify({'message': 'Account not found.'}), 404
        
        # Vérifier si les rôles existent, sinon les créer
        roles = []
        for role_name in role_names:
            role = Role.query.filter_by(name=role_name).first()
            if not role:
                role = Role(name=role_name)
                db.session.add(role)
                db.session.commit()
            roles.append(role)
        
        # Mettre à jour les rôles du compte
        account.roles = roles
        db.session.commit()
        return jsonify({'message': 'Account roles updated successfully.'}), 200
    except Exception as e:
        return jsonify({'message': 'Failed to update account roles.', 'error': str(e)}), 500



# Route pour récupérer les groupes d'un compte par ID
@accounts.route('/account/<int:account_id>/groups', methods=['GET'])
def get_account_groups(account_id):
    try:
        account = Account.query.get(account_id)
        if not account:
            return jsonify({'message': 'Account not found.'}), 404
        
        groups = [group.name for group in account.groups]
        return jsonify({'message': 'Get account groups by ID.', 'groups': groups}), 200
    except Exception as e:
        return jsonify({'message': 'Failed to get account groups.', 'error': str(e)}), 500



# Route pour mettre à jour les groupes d'un compte par ID
@accounts.route('/account/<int:account_id>/groups', methods=['PUT'])
def update_account_groups(account_id):
    try:
        data = request.json
        group_names = data.get('groups')
        if not group_names:
            return jsonify({'message': 'Group names are required.'}), 400
        
        account = Account.query.get(account_id)
        if not account:
            return jsonify({'message': 'Account not found.'}), 404
        
        # Vérifier si les groupes existent, sinon les créer
        groups = []
        for group_name in group_names:
            group = Group.query.filter_by(name=group_name).first()
            if not group:
                group = Group(name=group_name)
                db.session.add(group)
                db.session.commit()
            groups.append(group)
        
        # Mettre à jour les groupes du compte
        account.groups = groups
        db.session.commit()
        return jsonify({'message': 'Account groups updated successfully.'}), 200
    except Exception as e:
        return jsonify({'message': 'Failed to update account groups.', 'error': str(e)}), 500



# # Route pour envoyer une invitation pour un compte par ID
# @accounts.route('/account/<int:account_id>/invitations', methods=['POST'])
# def send_account_invitation(account_id):
#     try:
#         data = request.json
#         if 'recipient_email' not in data:
#             return jsonify({'message': 'Recipient email is required.'}), 400
        
#         # Vérifier si le compte existe
#         account = Account.query.get(account_id)
#         if not account:
#             return jsonify({'message': 'Account not found.'}), 404
        
#         # Implémenter la logique pour envoyer une invitation pour un compte
#         invitation = Invitation(sender_id=account.user_id, recipient_email=data['recipient_email'], account_id=account_id)
#         db.session.add(invitation)
#         db.session.commit()
        
#         return jsonify({'message': 'Invitation sent successfully.'}), 200
#     except Exception as e:
#         return jsonify({'message': 'Failed to send account invitation.', 'error': str(e)}), 500




# # Route pour annuler une invitation pour un compte par ID et ID d'invitation
# @accounts.route('/account/<int:account_id>/invitations/<int:invitation_id>', methods=['DELETE'])
# def cancel_account_invitation(account_id, invitation_id):
#     try:
#         # Vérifier si l'invitation et le compte associé existent
#         invitation = Invitation.query.filter_by(id=invitation_id, account_id=account_id).first()
#         if not invitation:
#             return jsonify({'message': 'Invitation not found.'}), 404
        
#         # Implémenter la logique pour annuler une invitation pour un compte
#         db.session.delete(invitation)
#         db.session.commit()
        
#         return jsonify({'message': 'Invitation canceled successfully.'}), 200
#     except Exception as e:
#         return jsonify({'message': 'Failed to cancel account invitation.', 'error': str(e)}), 500