from datetime import date

from django.core.management.base import BaseCommand
from django.utils import timezone

from accounts.models import User
from blog.models import Post
from core.models import SiteSettings
from projects.models import Category, Project, Tag as ProjectTag
from qna.models import Question, Tag as QuestionTag
from skills.models import Certification, Education, Experience, Skill, SkillCategory


class Command(BaseCommand):
    help = "Create polished starter content for the portfolio."

    def handle(self, *args, **options):
        site, _ = SiteSettings.objects.get_or_create(pk=1)
        site.site_name = "IANO / systems portfolio"
        site.role = "Developer, data enthusiast, cybersecurity practitioner, researcher, entrepreneur, and teacher"
        site.hero_text = "I connect mathematics, software, data, and security to solve real problems."
        site.about_text = "I am Ian Muiruri Waiganjo, a technology-focused professional who builds systems, studies evidence, and keeps learning across disciplines."
        site.location = "Kenya"
        site.save()

        user, created = User.objects.get_or_create(username="iano", defaults={"email": "hello@example.com", "first_name": "Iano"})
        if created:
            user.set_password("portfolio-demo")
            user.save()

        categories = {}
        for name, slug in [("Machine learning", "machine-learning"), ("Product systems", "product-systems"), ("Developer tools", "developer-tools")]:
            categories[name], _ = Category.objects.get_or_create(slug=slug, defaults={"name": name})

        tags = {}
        for name in ["Python", "Django", "ML", "Data", "Systems"]:
            tags[name], _ = ProjectTag.objects.get_or_create(name=name)
        project_data = [
            ("Signal / anomaly detection", "A calm interface for finding the one unusual thing in a noisy stream.", "A production-minded anomaly detection workflow that combines feature engineering, explainable models, and an operator-first review loop.", categories["Machine learning"], ["Python", "ML", "Data"], "3.2× faster investigations"),
            ("Field notes / knowledge graph", "Turning scattered technical notes into a searchable map of ideas.", "A lightweight knowledge system for connecting research, decisions, and context without hiding the source material behind a black box.", categories["Product systems"], ["Python", "Django", "Data"], "1 place to think clearly"),
            ("Deploy / the boring parts", "Small developer tools that make shipping feel predictable.", "A set of internal tools for repeatable previews, health checks, and deployment diagnostics across a growing Python surface area.", categories["Developer tools"], ["Python", "Django", "Systems"], "less ceremony, more signal"),
        ]
        for title, summary, description, category, tag_names, metric in project_data:
            project, _ = Project.objects.get_or_create(title=title, defaults={"summary": summary, "description": description, "category": category, "featured": True, "tech_stack": tag_names, "impact_metric": metric, "status": "completed"})
            project.tags.set([tags[name] for name in tag_names])

        for category_name, slug, skills in [
            ("Languages", "languages", [("Python", 98, 8), ("SQL", 92, 7), ("Bash", 84, 6)]),
            ("ML / data", "ml-data", [("scikit-learn", 92, 6), ("PyTorch", 82, 4), ("Pandas", 95, 7)]),
            ("Systems", "systems", [("Django", 94, 6), ("Postgres", 88, 6), ("Docker", 85, 5)]),
        ]:
            skill_category, _ = SkillCategory.objects.get_or_create(slug=slug, defaults={"name": category_name})
            for name, level, years in skills:
                Skill.objects.update_or_create(category=skill_category, name=name, defaults={"level": level, "years": years})

        Experience.objects.update_or_create(role="Independent engineer", company="IANO / LABS", defaults={"start_date": date(2020, 1, 1), "location": "Kenya", "description": "Building software, data workflows, and security-minded systems from first principles. I connect technical depth with useful product decisions and teach what I learn.", "stack": ["Python", "Django", "Data", "Cybersecurity"]})
        Education.objects.update_or_create(institution="University studies", degree="Bachelor's degree", defaults={"field": "Mathematics and Chemistry, major in Statistics", "start_date": date(2016, 1, 1), "end_date": date(2020, 12, 31), "details": "Graduated with honors, developing a foundation in analytical thinking, research, problem solving, and evidence-based decisions."})
        for name, issuer, issued_date in [("Python and web development", "Independent learning", date(2022, 6, 1)), ("Cybersecurity foundations", "Professional development", date(2023, 4, 1)), ("Data analysis and research", "Professional development", date(2024, 2, 1))]:
            Certification.objects.update_or_create(name=name, issuer=issuer, defaults={"issued_date": issued_date})
        Post.objects.get_or_create(title="The best ML system is usually a product decision", defaults={"author": user, "excerpt": "Models matter. The workflow around the model matters more.", "body": "A model can be technically excellent and still fail to create value.\\n\\nThe real work is deciding what signal is useful, who needs it, and what happens after the prediction. That is where the system becomes a product.", "status": "published", "published_at": timezone.now()})
        question_tag, _ = QuestionTag.objects.get_or_create(name="python")
        question, _ = Question.objects.get_or_create(title="How do you decide whether a data pipeline needs a queue?", defaults={"author": user, "body": "I am designing a small ML workflow and want to keep the first version simple without painting the system into a corner. What signals tell you it is time to introduce a queue?", "status": "open"})
        question.tags.add(question_tag)
        self.stdout.write(self.style.SUCCESS("Starter portfolio content is ready."))
