from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("upwork", "0002_student_question_fields")]

    operations = [
        migrations.AddField(
            model_name="brief",
            name="answer_unlocked",
            field=models.BooleanField(default=False),
        ),
    ]
