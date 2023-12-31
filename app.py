import sys
import panel as pn
from quiz_ai import get_quiz_dict

quiz_dict = {}
current_question = 1
score = 0

async def acquire_write_lock():
    await pn.io.curdoc().add_next_tick_callback(lambda: None)

async def release_write_lock(lock):
    await pn.io.curdoc().add_next_tick_callback(lambda: None)

def update_question():
    print(quiz_dict[current_question])
    question.object = str(current_question) +". "+ quiz_dict[current_question]["question"]
    options_dict = quiz_dict[current_question]["options"]
    options_list = [f"{label}: {value}" for label, value in options_dict.items()]
    options.options = options_list

def next_question(event):
    global current_question, score
    selected_option = options.value.split(":")[0]
    quiz_dict[current_question]["user_selected"] = options.value
    correct_answer = quiz_dict[current_question]["answer"]

    if selected_option == correct_answer:
        result.object = "<b><font size='3' color='green'>Correct</font></b>"
        score += 1
    else:
        result.object = f"<b><font size='3' color='red'>Incorrect! Right Answer is '{correct_answer}'</font></b>"

    current_question += 1

    if current_question <= len(quiz_dict):
        update_question()
    else:
        result.object = f'''<br><b><font size='8' color='grey'> Quiz Completed - </font></b>
        <b><font size='7' color='Teal'>SCORE: {score / len(quiz_dict) * 100} %</font></b><br><br>
        <b><font size='6'> Review your assessment: Correct Answer(s) {score} out of {len(quiz_dict)} questions </font></b><br>
        <font size='3', color='red'> Warning: This questions are being processed by Google Gemini. 
        There could be error in the question/answer, since it is in experimental phase. Thanks for understanding! </font><br>
        '''

        # Display each question along with its options and user selection
        for q_num, q_data in quiz_dict.items():
            result.object += f"<br><b><font size='4'>Question {q_num}: {q_data['question']}</font></b><br>"
            result.object += f"<b><font size='3'>Options: {', '.join(f'{label}: {value}' for label, value in q_data['options'].items())}</font></b>"
            if q_data['user_selected'].split(':')[0] == q_data['answer'] :
                result.object += f"<br><b><font size='3' color='green'>User Selected: {q_data.get('user_selected', 'N/A')}</font></b><br>"
            else:
                result.object += f"<br><b><font size='3' color='red'>You Answered: {q_data.get('user_selected', 'N/A')}</font></b><br>"
            result.object += f"<b><font size='3' color='grey'>Correct Answer: {q_data['answer']}</font></b><br>\n"

        options.disabled = True
        next_button.disabled = True
        sys.exit()

def generate_quiz(event):
    global quiz_dict, current_question
    n = int(quiz_count_box.value)
    topic = title_box.value
    quiz_dict = get_quiz_dict(topic, n)
    current_question = 1
    update_question()

    # Enable the "Submit" button after generating the quiz
    next_button.disabled = False

    # Disable the "Generate" button once it's clicked
    submit_button.disabled = True

    # Create a layout with a bold headline for the quiz topic and a divider
    title_layout = pn.Row(pn.pane.Str(f"Exam Started on the Topic: {topic}", styles={"font-size": "50px"}))
    divider = pn.layout.Divider()

    # Combine the title layout, divider, and the existing layout
    app_layout[:] = [
        pn.Column(title_layout, divider),
        pn.Row(question, width=300),  # Adjust width if necessary
        options, next_button, result
    ]

    return quiz_dict

warning_label = pn.pane.Str()
title_box = pn.widgets.TextInput()
quiz_count_box = pn.widgets.TextInput()
title_label = pn.pane.Str()
quiz_count_label = pn.pane.Str()
submit_button = pn.widgets.Button(name="Generate", button_type="primary")

warning_label = "<font color='red'>Warning: Hit Generate button once and wait for sometime to create quiz page! (powered by Google Gemini)</font>"
title_label.object = "Enter the topic for quiz: "
quiz_count_label.object = "Enter the number of questions: "

submit_button.on_click(generate_quiz)

# Initial layout with only the input boxes and the "Generate" button
layout = pn.Row(
    pn.Column(title_label, title_box),
    pn.Column(quiz_count_label, quiz_count_box),
    pn.Column(submit_button),
    pn.Column(warning_label)
)

result = pn.pane.HTML()  # Use HTML pane to render HTML content
question = pn.pane.Str()
options = pn.widgets.RadioButtonGroup()
next_button = pn.widgets.Button(name='Submit', button_type='primary', disabled=True)
next_button.on_click(next_question)

# Create the app layout
app_layout = pn.Column(layout)

# Serve the Panel app
if __name__ == "__main__":
    pn.serve(app, title="Quiz Panel").show()
