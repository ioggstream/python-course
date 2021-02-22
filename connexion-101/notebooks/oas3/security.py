"""
A file implementing securitySchemes
"""


def my_auth(username, password, required_scopes=None):
    """An dummy authentication function.
       :params: username, the username
       :params: password, the password
       :params: scopes, the scope
       :returns: `{"sub": username, "scope": ""}` on success, 
                 None on failure
    """
    if username == password:
        return {"sub": username, "scope": ""}
    return None
