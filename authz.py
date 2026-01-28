# authz.py

from roles import ROLE_HIERARCHY
from permissions import PERMISSIONS

def get_role(current_user):
    if current_user is None:
        return "GUEST"
    return current_user.get("role_name", "GUEST")

def can(current_user, permission):
    user_role = get_role(current_user)
    required_role = PERMISSIONS.get(permission)

    if required_role is None:
        return False

    return ROLE_HIERARCHY[user_role] >= ROLE_HIERARCHY[required_role]
