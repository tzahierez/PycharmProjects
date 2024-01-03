import os
import re

import openai
from openai import OpenAI


class OpenAiClient:

    #TODO - notice that chapter is context. it should be changed all the way including the database
    def generate_question_to_answer_pairs(_self, course, subject, context, question_count, pdf_text):
        try:

            # Extract text from the incoming JSON request
            # data = request.json
            #user_input = f"provide {question_count} questions and perfect answers for the course {course} and the subject {subject}. {chapter}.your  expected reply  should have the following structure: \"<question X>:.....<answerX>....\""

            prompt_parts = ["Based on the following text from the course material:"]

            if course:
                prompt_parts.append(f"for the course '{course}'")
            if context:
                prompt_parts.append(f"which is part of a '{context}'")

            prompt_parts.append(
                f"\n\n{pdf_text}\n\nPlease provide {question_count} questions and perfect answers")

            if subject:
                prompt_parts.append(f"on the subject '{subject}'.")

            prompt_parts.append(
                "Your expected reply should have the following structure: '<question X>:.....<answer X>....'")

            # Combining all parts into the final prompt
            user_input = " ".join(prompt_parts)
            # user_input = (
            #     f"Based on the following text from the course material, which is part of a '{context}':\n\n"
            #     f"{pdf_text}\n\n"
            #     f"Please provide {question_count} questions and perfect answers for the course '{course}' and the subject '{subject}'. "
            #     f"Your expected reply should have the following structure: '<question X>:.....<answer X>....'"
            # )
            # user_id = data.get('user_id', 'default_user')  # You should pass a unique user_id with each request

            # Retrieve the existing conversation context if it exists
            conversation_history = ''  # session_contexts.get(user_id, [])

            # OPENAI_API_KEY=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   ( replaced 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)
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

            print('sending req to gpt ', conversation_history)
            # Call OpenAI GPT-3.5-turbo API using the updated API
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",  # Specify the GPT-3.5-turbo model
                messages=[{"role": "system", "content": "You are a helpful assistant."},
                          {"role": "user", "content": user_input}]
            )
            print('got response from gpt')
            # Extract the response text
            response_text = response.choices[0].message.content  # Accessing the 'content' attribute directly


            # response_text = """Question 1: What is a heap in the context of data structures?
            # Answer 1: A heap is a specialized tree-based data structure that satisfies the heap property. It is commonly used to implement priority queues, as it allows efficient retrieval of the maximum or minimum element.
            # Question 2: How does a binary heap differ from other types of heaps?
            # Answer 2: A binary heap is a complete binary tree that satisfies the heap property. The heap property states that for every node in the heap, the value of that node is greater than or equal to (in a max heap) or less than or equal to (in a min heap) the values of its child nodes.
            # Question 3: What are the main operations performed on a heap?
            # Answer 3: The main operations performed on a heap are insertion, deletion, and retrieval of the maximum or minimum element. Insertion involves placing a new element in the heap while maintaining the heap property. Deletion removes the maximum or minimum element from the heap and restores the heap property. Retrieval returns the maximum or minimum element without modifying the heap.
            # """



#             response_text = """Question 1: dummy question1?
# Answer 1: dummy ans1
# Question 2: dummy question2?
# Answer 2: dummy ans2.
# Question 3: dummy question2?
# Answer 3: dummy ans3."""

            print(response_text)
            # Return the response text as JSON
            result = parse_qa_pairs(response_text)
            return result  # jsonify({'response': response_text})
        except Exception as e:
            print("Error during API call:", e)
            return str(e)  # or handle the error appropriately


def parse_qa_pairs(raw_text):
    # Initialize an empty list to hold the question-answer pairs
    qa_pairs = []

    # Split the text by "Question" to separate each Q&A pair
    questions = split_text = re.split("question ", raw_text, flags=re.IGNORECASE)[1:]  # Skip the first split as it will be empty

    for q in questions:
        # Split each Q&A pair by "Answer"
        parts = re.split("answer ", q, flags=re.IGNORECASE)

        # Extract the question and answer texts
        question_text = parts[0].split(":")[1].strip()
        answer_text = parts[1].split(":")[1].strip()

        # Create a dictionary for the Q&A pair and append to the list
        qa_pairs.append({
            'question': question_text,
            'answer': answer_text
        })

    return qa_pairs

'''
# Sample usage:
raw_text = """
Question 1: What is a linked list in the context of data structures?
Answer 1: A linked list is a linear data structure used to store a collection of elements. ...

Question 2: What are the advantages of using linked lists over arrays in certain scenarios?
Answer 2: Linked lists have a number of advantages over arrays. ...

Question 3: What are the different types of linked lists that can be used in programming?
Answer 3: There are several types of linked lists, including singly linked lists, ...
"""

parsed_pairs = parse_qa_pairs(raw_text)
print(parsed_pairs)

# data = """Question 1: dummy question1 blabla
# Answer 1: dummy answer1 blabla
# Question 2: dummy question2 blabla
# Answer 2: dummy answer2 blabla"""
#
# # Convert the data string to the desired structure
# qa_structure = convert_to_qa_structure(data)
'''