from forms.schema import extract_questions, question_field_name, question_text


def build_updated_input(tool_input, content):
    updated = dict(tool_input or {})
    questions = extract_questions(tool_input or {})
    answers = dict(tool_input.get('answers')) if isinstance((tool_input or {}).get('answers'), dict) else {}

    for index, item in enumerate(questions):
        field_name = question_field_name(item, index, len(questions))
        if field_name in content:
            answers[question_text(item, index)] = content[field_name]

    if answers:
        updated['answers'] = answers
    return updated

