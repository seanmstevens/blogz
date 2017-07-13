#### SIGNUP INPUT VERIFICATION UTILITIES ####

def check_username_signup(username, user):
    errors = []
    if user:
        errors.append("That user already exists.")
    
    if not username:
        errors.append("You cannot leave this field blank.")

    if len(username) > 20:
        errors.append("Your username needs to be shorter than 20 characters.")
    elif len(username) < 3:
        errors.append("Your username needs to be at least 3 characters long.")

    if not username[0].isalpha():
        errors.append("Your username must start with a letter.")

    return errors

def check_password_signup(password):
    errors = []
    if not password:
        errors.append("You cannot leave this field blank.")

    if len(password) > 20:
        errors.append("Your username needs to be shorter than 20 characters.")
    elif len(password) < 3:
        errors.append("Your username needs to be at least 3 characters long.")

    return errors

def check_verify_signup(verify, password):
    errors = []
    if not verify:
        errors.append("You cannot leave this field blank.")

    if verify != password:
        errors.append("Your passwords do not match.")

    return errors

#### LOGIN INPUT VERIFICATION UTILITIES ####

def check_username_login(user):
    errors = []
    if not user:
        errors.append("That user doesn't exist yet.")

    return errors
