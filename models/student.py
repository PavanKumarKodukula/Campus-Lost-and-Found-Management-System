from .user import User


class Student(User):

    def __init__(self, user_id, name, college_id, email, phone, password):
        super().__init__(user_id,name,college_id,email,phone,password,"student")