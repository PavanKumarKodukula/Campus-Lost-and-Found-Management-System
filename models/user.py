class User:

    def __init__(self, user_id, name, college_id, email, phone, password, role):
        self.__user_id = user_id
        self.__name = name
        self.__college_id = college_id
        self.__email = email
        self.__phone = phone
        self.__password = password
        self.__role = role

    def get_user_id(self):
        return self.__user_id

    def get_name(self):
        return self.__name

    def get_college_id(self):
        return self.__college_id

    def get_email(self):
        return self.__email

    def get_phone(self):
        return self.__phone

    def get_password(self):
        return self.__password

    def get_role(self):
        return self.__role
