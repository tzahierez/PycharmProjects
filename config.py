# config.py
import os

# prompt config:
# I wrote a python/flask/mysql project that will be used to teachers to create and check tests
# regarding a known subject.
# the enterance page (http://127.0.0.1:5000/exam/create_exam_template) will let the teacher to fill in fields of the test material (course name, course subject, and number of questions to be generated)
# once the teacher filled these fields, and pressed "start generate test", then ai generated questions will show (the requested number of questions) and the answers that the ai engine found.
# the teacher is capable of editing theanswers, and also to fill text of how to rate the mark of the answer that students will fill in later on.
# then the techer can press the "create test template", and move on to the test-templates-page, where he cen see all test templates.
#
# here are the basic building blocks:
#
# schema:
#
# there is exam that describes the title of specific test, there is question_template that describes question, its answer, and how to validate the answer
#
# CREATE TABLE `exam_template` (
#   `id` int NOT NULL AUTO_INCREMENT,
#   `course` varchar(128) NOT NULL,
#   `subject` varchar(128) NOT NULL,
#   `chapter` varchar(128) DEFAULT NULL,
#   `question_count` int NOT NULL,
#   PRIMARY KEY (`id`)
# ) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
#
#
# CREATE TABLE `question_template` (
#   `id` int NOT NULL AUTO_INCREMENT,
#   `exam_template_id` int NOT NULL,
#   `question_text` text NOT NULL,
#   `perfect_answer` text NOT NULL,
#   `evaluation_criteria` text,
#   PRIMARY KEY (`id`),
#   KEY `exam_template_id` (`exam_template_id`),
#   CONSTRAINT `question_template_ibfk_1` FOREIGN KEY (`exam_template_id`) REFERENCES `exam_template` (`id`)
# ) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci

class Config:
    #production
    #SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://todo_user:pass@localhost/todo_list_db'
    SQLALCHEMY_DATABASE_URI_WORK_LOCAL = 'mysql+mysqlconnector://admin:admin123@ai-mysqldev.c8gl0mqk3fwz.us-west-2.rds.amazonaws.com:3306/exam-ai' #os.getenv('DATABASE_URL', 'mysql+mysqlconnector://admin:admin123@ai-mysqldev.c8gl0mqk3fwz.us-west-2.rds.amazonaws.com:3306/exam-ai')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'NO DATABASE DEFINED')
    #local not working fro some reason...
    #SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://todo_list:pass@localhost/todo_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Other configuration settings...
