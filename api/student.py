from flask import Blueprint
from flask_restful import Api, Resource # used for REST API building

student_api = Blueprint('student_api', __name__,
                   url_prefix='/api')

# API docs https://flask-restful.readthedocs.io/en/latest/
api = Api(student_api)

class StudentAPI:        
    class _Maryam(Resource): 
        def get(self):
            # implement the get method 
            infoDB_maryam = [{
                "FirstName": "Maryam",
                "LastName": "Abdul-Aziz",
                "DOB": "November 23",
                "Residence": "The Bermuda Triangle",
                "Email": "maryama42841@stu.powayusd.com",
                "Favorite Books": ["The Outsiders", "Tex", "The Catcher in the Rye", "The Hunger Games", "Renegades"]
            }]
            return infoDB_maryam
    
    class _Katherine(Resource): 
        def get(self):
           # implement the get method 
           infoDB_katherine = [{
                "FirstName": "Katherine",
                "LastName": "Chen",
                "DOB": "July 30",
                "Residence": "San Diego",
                "Email": "katherine.yx.chen@gmail.com",
                "Favorite_Books": ["A Court of Thornes and Roses", "Talon", "49 Miles Alone", "They Both Die in the End", "The Silent Patient"]
            }]
           return infoDB_katherine

    class _Avika(Resource): 
        def get(self):
           # implement the get method 
           infoDB_avika = [{
            "FirstName": "Avika",
            "LastName": "Prasad",
            "DOB": "January 22",
            "Residence": "San Diego",
            "Email": "avikapd22@gmail.com",
            "Favorite_Books": ["The Inheritance Games", "Harry Potter 1-7", "Mystiwick School of Musicraft", "The Hunger Games"]
        }]
           return infoDB_avika

    class _Aditi(Resource): 
        def get(self):
           # implement the get method 
           infoDB_aditi = [{
            "FirstName": "Aditi",
            "LastName": "Bandaru",
            "DOB": "May 21",
            "Residence": "San Diego",
            "Email": "aditib03015@stu.powayusd.com",
            "Favorite_Books": ["A Feast for Crows", "Scythe", "A Game of Thrones", "Wings of Fires", "Frankenstein"]
        }]
           return infoDB_aditi

    class _Gabi(Resource): 
        def get(self):
           # implement the get method 
            infoDB_gabi = [{
                "FirstName": "Gabriela",
                "LastName": "Connelly",
                "DOB": "December 16",
                "Residence": "San Diego",
                "Email": "gabrielac@myyahoo.com",
                "Favorite_Books": ["Made You Up", "The Cruel Prince", "Diary of a Wimpy Kid 1-19", "Legend"]
        }]
            return infoDB_gabi

    class _Soumini(Resource): 
        def get(self):
           # implement the get method 
           infoDB_soumini = [{
            "FirstName": "Soumini",
            "LastName": "Kandula",
            "DOB": "December 21",
            "Residence": "Alaska",
            "Email": "souminik21@gmail.com",
            "Favorite_Books": ["Harry Potter 1-7", "The Silent Patient", "A Good Girl's Guide to Murder", "Legend", "The Fault in Our Stars"]
        }]
           return infoDB_soumini
           
    # building RESTapi endpoint
    api.add_resource(_Maryam, '/student/maryam')          
    api.add_resource(_Katherine, '/student/katherine')
    api.add_resource(_Avika, '/student/avika')
    api.add_resource(_Aditi, '/student/aditi')
    api.add_resource(_Gabi, '/student/gabi')   
    api.add_resource(_Soumini, '/student/soumini')     