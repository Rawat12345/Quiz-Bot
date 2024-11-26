from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        session["final_score"] = 0
        bot_responses.append(BOT_WELCOME_MESSAGE)
        current_question_id = 0

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    """
    Validates and stores the answer for the current question to django session.
    """
    if current_question_id:
        question_details = PYTHON_QUESTION_LIST[current_question_id - 1]

        final_score = session.get("final_score")

        if question_details["answer"] == answer:
            final_score += 1

        session["final_score"] = final_score
        session.save()

    return True, ""


def get_next_question(current_question_id):
    """
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    """
    next_question_id = current_question_id + 1
    if len(PYTHON_QUESTION_LIST) > current_question_id:
        next_question_details = PYTHON_QUESTION_LIST[current_question_id]

        options = next_question_details["options"]
        question_details = f"{next_question_details['question_text']} <br>"

        index = 1
        for data in options:
            question_details = f"{question_details} {index}. {data} <br>"
            index += 1

        return question_details, next_question_id

    return None, -1


def generate_final_response(session):
    """
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    """

    final_score = session.get("final_score")
    
    final_score = (final_score/len(PYTHON_QUESTION_LIST))*100

    return f"Your final test result is: {final_score}%"
