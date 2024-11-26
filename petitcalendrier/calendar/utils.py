from petitcalendrier.models import Answer

def create_answer(form, question, user):
    character = form.answer_character.data
    time = form.answer_time.data
    object = form.answer_object.data 
    place = form.answer_place.data
    sound = form.answer_sound.data
    color = form.answer_color.data
    return Answer(answer_character=character, answer_time=time, answer_object=object, answer_place=place, answer_sound=sound, answer_color=color, question=question, author=user)