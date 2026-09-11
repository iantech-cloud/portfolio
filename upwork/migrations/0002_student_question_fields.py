from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("upwork", "0001_initial")]

    operations = [
        migrations.AddField(model_name="brief", name="is_student_question", field=models.BooleanField(default=False)),
        migrations.AddField(model_name="brief", name="math_content", field=models.TextField(blank=True, help_text="Optional LaTeX-friendly working or formula content.")),
        migrations.AddField(model_name="brief", name="attachment", field=models.FileField(blank=True, upload_to="upwork/questions/%Y/%m/")),
        migrations.AddField(model_name="brief", name="answer", field=models.TextField(blank=True)),
        migrations.AddField(model_name="brief", name="answer_preview", field=models.TextField(blank=True)),
        migrations.AddField(model_name="brief", name="answered_at", field=models.DateTimeField(blank=True, null=True)),
    ]
