from system.core.model import Model

import re
NAME_REGEX = re.compile(r'^[^\W_]+(-[^\W_]+)?$')
PASSWORD_REGEX = re.compile(r'[A-Za-z0-9@#$%^&+=]{8,}')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')


class User(Model):

    def registerUser(self, userData):
        errors = []

        if not userData['name']:
            errors.append(("Name cannot be left blank", "regname"))
            
        if not userData['alias']:
            errors.append(("One must have an alias", "regalias"))

        elif not NAME_REGEX.match(userData['alias']):
            errors.append(("Letters only please", "regalias"))

        if not userData['email']:
            errors.append(("One must have an email", "regemail"))

        elif not EMAIL_REGEX.match(userData['email']):
            errors.append(("Letters only please", "regemail"))

        if not userData['password']:
            errors.append(("One must create a password", "regpassword")) 
  
        elif not PASSWORD_REGEX.match(userData['password']):
            errors.append(("must be 8 charactors, letters and numbers, upper and lowercase accepted", "regpassword"))  

        if not userData['passwordconfirmation']:
            errors.append(("One must confirm a password", "regconfirm"))
 
        elif not (userData['password']) == (userData['passwordconfirmation']):
            errors.append(("Passwords must match", "regconfirm"))

        if errors:
            return {"status": False, "errors": errors}
        else:
            password = userData['password']
            pw_hash = self.bcrypt.generate_password_hash(password)

            sql = """INSERT INTO user (name, alias, email, password, created_at, updated_at) 
                     VALUES (:name, :alias, :email, :password, NOW(), NOW())""" 
            data = {
                'name': userData['name'],
                'alias': userData['alias'],
                'email': userData['email'],
                'password': pw_hash,
            }
            self.db.query_db(sql, data)

            get_user_query = "SELECT * FROM user WHERE email = :email"
            user_data = {
                'email': userData['email'],
            }
            userArray = self.db.query_db(get_user_query, user_data)

            if userArray:
                user = userArray[0]

                return { "status": True,  "user": user }

       

    def loginUser(self, userData):
        errors = []
        password = userData["password"]

        sql = "SELECT * FROM user WHERE email = :email"
        data = {
            'email': userData['email'],
        }
        userArray = self.db.query_db(sql, data)

        if userArray:
            user = userArray[0]

            if self.bcrypt.check_password_hash(user["password"], password):
                return { "status": True, "user": user }

        errors.append('Email and password do not match.')
        return {"status": False, "errors": errors}
