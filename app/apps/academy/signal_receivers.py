def delete_question_choice(sender, instance, **kwargs):
    instance.choices.all().delete()


def delete_non_chapter_question(sender, instance, **kwargs):
    if not instance.chapter:
        instance.question.delete()