from core.config import DEFAULT_CONFIG
from forms.model import Field, FormSpec, Option


def first_present(*values):
    for value in values:
        if value is not None:
            return value
    return None


def bool_value(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() not in ('', '0', 'false', 'no', 'off')
    return bool(value)


def nested_get(data, *path):
    current = data
    for key in path:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current


def option_value(option, index):
    if isinstance(option, dict):
        return first_present(
            option.get('value'),
            option.get('id'),
            option.get('label'),
            option.get('title'),
            index,
        )
    return option


def option_label(option, index):
    if isinstance(option, dict):
        return str(first_present(
            option.get('label'),
            option.get('title'),
            option.get('name'),
            option.get('value'),
            index,
        ))
    return str(option)


def option_description(option):
    if isinstance(option, dict):
        return str(first_present(option.get('description'), ''))
    return ''


def extract_questions(data):
    questions = first_present(
        data.get('questions'),
        nested_get(data, 'request', 'questions'),
        nested_get(data, 'request', 'params', 'questions'),
        nested_get(data, 'params', 'questions'),
        nested_get(data, 'tool_input', 'questions'),
    )
    if isinstance(questions, list) and questions:
        return questions

    source = data.get('tool_input') if isinstance(data.get('tool_input'), dict) else data
    question = source.get('question') or source.get('message') or source.get('prompt')
    options = source.get('options') or source.get('choices') or []
    if question or options:
        return [{
            'question': question or '',
            'header': source.get('header') or source.get('title'),
            'options': options,
            'field_title': source.get('field_title'),
        }]

    return []


def question_field_name(item, index, total):
    if not isinstance(item, dict):
        item = {'question': str(item)}
    return str(first_present(
        item.get('id'),
        item.get('name'),
        'response' if total == 1 else f'response_{index + 1}',
    ))


def question_text(item, index):
    if not isinstance(item, dict):
        return str(item)
    return str(item.get('question') or item.get('message') or item.get('prompt') or f'问题 {index + 1}')


def schema_from_questions(data):
    questions = extract_questions(data)
    if not isinstance(questions, list) or not questions:
        return {}

    schema = {
        'type': 'object',
        'title': first_present(data.get('title'), 'Agent 需要您的选择'),
        'required': [],
        'properties': {},
    }

    for index, item in enumerate(questions):
        if not isinstance(item, dict):
            item = {'question': str(item)}

        field_name = question_field_name(item, index, len(questions))
        question = item.get('question') or item.get('message') or item.get('prompt') or ''
        header = first_present(item.get('header'), item.get('title'), item.get('field_title'), f'问题 {index + 1}')
        options = item.get('options') or item.get('choices') or []
        field = {'type': 'string', 'title': str(header), 'description': str(question)}

        if isinstance(options, list) and options:
            field['enum'] = [str(option_value(option, option_index)) for option_index, option in enumerate(options)]
            field['enumNames'] = [option_label(option, option_index) for option_index, option in enumerate(options)]
            field['enumDescriptions'] = [option_description(option) for option in options]
            field['allowCustom'] = first_present(
                item.get('allowCustom'),
                item.get('allow_custom'),
                item.get('allowOther'),
                item.get('allow_other'),
                True,
            )

        schema['properties'][field_name] = field
        schema['required'].append(field_name)

    return schema


def extract_schema(data):
    schema = first_present(
        data.get('requested_schema'),
        data.get('requestedSchema'),
        data.get('schema'),
        data.get('input_schema'),
        nested_get(data, 'tool_input', 'requested_schema'),
        nested_get(data, 'tool_input', 'requestedSchema'),
        nested_get(data, 'tool_input', 'schema'),
        nested_get(data, 'tool_input', 'input_schema'),
        nested_get(data, 'request', 'requested_schema'),
        nested_get(data, 'request', 'requestedSchema'),
        nested_get(data, 'request', 'schema'),
        nested_get(data, 'request', 'input_schema'),
        nested_get(data, 'request', 'params', 'requested_schema'),
        nested_get(data, 'request', 'params', 'requestedSchema'),
        nested_get(data, 'request', 'params', 'schema'),
        nested_get(data, 'request', 'params', 'input_schema'),
        nested_get(data, 'params', 'requested_schema'),
        nested_get(data, 'params', 'requestedSchema'),
        nested_get(data, 'params', 'schema'),
        nested_get(data, 'params', 'input_schema'),
    )
    if isinstance(schema, dict) and schema:
        return schema
    return schema_from_questions(data) or schema or {}


def extract_message(data):
    questions = extract_questions(data)
    first_question = questions[0] if isinstance(questions, list) and questions and isinstance(questions[0], dict) else {}
    return first_present(
        data.get('message'),
        data.get('prompt'),
        nested_get(data, 'tool_input', 'message'),
        nested_get(data, 'tool_input', 'prompt'),
        nested_get(data, 'request', 'message'),
        nested_get(data, 'request', 'prompt'),
        nested_get(data, 'request', 'params', 'message'),
        nested_get(data, 'request', 'params', 'prompt'),
        nested_get(data, 'params', 'message'),
        nested_get(data, 'params', 'prompt'),
        first_question.get('question'),
        first_question.get('message'),
        first_question.get('prompt'),
        'Agent 请求用户输入。',
    )


def extract_title(data, schema):
    questions = extract_questions(data)
    first_question = questions[0] if isinstance(questions, list) and questions and isinstance(questions[0], dict) else {}
    return first_present(
        data.get('title'),
        nested_get(data, 'tool_input', 'title'),
        nested_get(data, 'request', 'title'),
        nested_get(data, 'request', 'params', 'title'),
        schema.get('title') if isinstance(schema, dict) else None,
        first_question.get('header'),
        first_question.get('title'),
        '需要选择',
    )


def option_items(spec):
    if not isinstance(spec, dict):
        return []

    enum_values = spec.get('enum')
    if isinstance(enum_values, list):
        titles = spec.get('enumNames') or spec.get('enum_titles') or []
        descriptions = spec.get('enumDescriptions') or spec.get('enum_descriptions') or []
        return [
            Option(
                value=value,
                label=str(titles[index]) if index < len(titles) else str(value),
                description=str(descriptions[index]) if index < len(descriptions) else '',
            )
            for index, value in enumerate(enum_values)
        ]

    for key in ('oneOf', 'anyOf'):
        variants = spec.get(key)
        if isinstance(variants, list):
            items = []
            for variant in variants:
                if not isinstance(variant, dict):
                    continue
                value = first_present(
                    variant.get('const'),
                    variant.get('enum', [None])[0] if isinstance(variant.get('enum'), list) else None,
                )
                if value is None:
                    continue
                items.append(Option(
                    value=value,
                    label=str(first_present(variant.get('title'), value)),
                    description=str(first_present(variant.get('description'), '')),
                ))
            return items

    return []


def fields_from_schema(schema):
    if not isinstance(schema, dict):
        return []
    properties = schema.get('properties')
    if not isinstance(properties, dict):
        return []

    required = set(schema.get('required') if isinstance(schema.get('required'), list) else [])
    fields = []
    for name, spec in properties.items():
        if not isinstance(spec, dict):
            spec = {}
        fields.append(Field(
            name=name,
            title=str(first_present(spec.get('title'), name)),
            description=str(first_present(spec.get('description'), '')),
            required=name in required,
            type=str(first_present(spec.get('type'), 'string')),
            default=spec.get('default'),
            options=option_items(spec),
            allow_custom=bool_value(first_present(spec.get('allowCustom'), spec.get('allow_custom'), False)),
        ))
    return fields


def form_spec_from_event(data, config=None):
    schema = extract_schema(data)
    return FormSpec(
        title=str(extract_title(data, schema)),
        message=str(extract_message(data)),
        fields=fields_from_schema(schema),
    )


def form_event_from_questions(tool_data):
    tool_input = tool_data.get('tool_input', {})
    tool_name = tool_data.get('tool_name', '')
    message = ''
    questions = extract_questions(tool_input)
    for item in questions:
        if isinstance(item, dict):
            message = item.get('question') or item.get('message') or item.get('prompt') or ''
            if message:
                break

    schema = schema_from_questions({'tool_input': tool_input})
    if not schema:
        message = tool_input.get('question') or tool_input.get('message') or tool_input.get('prompt') or ''
        schema = {
            'type': 'object',
            'title': tool_input.get('title') or 'Agent 需要您的选择',
            'required': ['response'],
            'properties': {
                'response': {
                    'type': 'string',
                    'title': tool_input.get('field_title', '输入内容'),
                    'description': message,
                },
            },
        }

    return {
        'hook_event_name': 'Elicitation',
        'message': message or f'Agent 请求通过 {tool_name} 与您交互',
        'requested_schema': schema,
    }
