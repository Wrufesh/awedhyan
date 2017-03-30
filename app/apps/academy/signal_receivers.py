def delete_question_choice(sender, instance, **kwargs):
    instance.choices.all().delete()

