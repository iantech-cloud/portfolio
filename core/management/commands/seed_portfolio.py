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
        site.site_name = "IAN MUIRURI WAIGANJO / portfolio"
        site.role = "Statistician, software engineer, cybersecurity practitioner, researcher, and entrepreneur"
        site.hero_text = "I build serious systems at the intersection of analytical thinking, practical software, and security."
        site.about_text = "I am Ian Muiruri Waiganjo — a statistician by academic foundation, developer and system builder by practice, cybersecurity enthusiast by direction, researcher by mindset, entrepreneur by ambition, and lifelong learner by choice."
        site.location = "Nairobi, Kenya"
        site.email = "hello@ianmuiruri.com"
        site.save()

        user, created = User.objects.get_or_create(username="iano", defaults={"email": "hello@example.com", "first_name": "Iano"})
        if created:
            user.set_password("portfolio-demo")
            user.save()

        categories = {}
        for name, slug in [("Machine learning", "machine-learning"), ("Product systems", "product-systems"), ("Developer tools", "developer-tools")]:
            categories[name], _ = Category.objects.get_or_create(slug=slug, defaults={"name": name})

        tags = {}
        for name in ["Python", "Django", "ML", "Data", "Systems", "Cybersecurity", "PostgreSQL", "JavaScript", "TypeScript", "WordPress", "M-Pesa"]:
            tags[name], _ = ProjectTag.objects.get_or_create(name=name)
        project_data = [
            ("HustleHub Africa", "A multi-opportunity digital earning platform built around real users and real transactions.", "A product ecosystem spanning profiles, referrals, wallets, withdrawals, M-Pesa payments, surveys, gaming, foreigner chat, notifications, support, reporting, blogs, and administrative tools. The work has been a practical education in business logic, payment callbacks, permissions, reliability, and secure production systems.", categories["Product systems"], ["Python", "Django", "PostgreSQL", "M-Pesa"], "real users, real business logic"),
            ("EUR/USD market analysis", "A statistical and machine learning workflow for understanding market data.", "An exploratory project using time, open, high, low, close, and volume data to practice feature engineering, regression, classification, visualization, model evaluation, and rigorous interpretation rather than treating model output as a black box.", categories["Machine learning"], ["Python", "ML", "Data"], "evidence before confidence"),
            ("IANO / systems portfolio", "A living technical portfolio and CV for work across software, data, security, and research.", "A Django-powered publishing system with structured projects, skills, experience, education, certifications, articles, Q&A, contact messages, and downloadable CV generation. It is designed to turn a broad technical direction into a clear, useful public record.", categories["Developer tools"], ["Python", "Django", "Systems"], "one place to understand the work"),
        ]
        for title, summary, description, category, tag_names, metric in project_data:
            project, _ = Project.objects.get_or_create(title=title, defaults={"summary": summary, "description": description, "category": category, "featured": True, "tech_stack": tag_names, "impact_metric": metric, "status": "completed"})
            project.tags.set([tags[name] for name in tag_names])

        for category_name, slug, skills in [
            ("Languages", "languages", [("Python", 92, 5), ("SQL", 84, 4), ("JavaScript / TypeScript", 78, 3), ("PHP", 76, 4), ("Bash", 75, 4)]),
            ("Backend / web", "backend-web", [("Django", 88, 5), ("Next.js", 72, 2), ("WordPress / WooCommerce", 86, 5), ("APIs and integrations", 84, 4)]),
            ("Data / ML", "data-ml", [("Pandas / NumPy", 88, 4), ("Matplotlib", 82, 4), ("scikit-learn", 76, 3), ("Statistics", 90, 7)]),
            ("Systems / security", "systems-security", [("PostgreSQL", 82, 4), ("MongoDB", 72, 3), ("Linux / Git", 84, 5), ("Cybersecurity", 68, 2), ("Deployment / Nginx", 72, 3)]),
        ]:
            skill_category, _ = SkillCategory.objects.get_or_create(slug=slug, defaults={"name": category_name})
            for name, level, years in skills:
                Skill.objects.update_or_create(category=skill_category, name=name, defaults={"level": level, "years": years})

        Experience.objects.update_or_create(role="Co-founder & CEO", company="OneSocialStack", defaults={"start_date": date(2022, 1, 1), "location": "Kenya", "description": "Leading product direction for a technology venture focused on digital platforms, online services, automation, and systems that create practical value for people and businesses.", "stack": ["Product strategy", "Software", "Automation", "Entrepreneurship"]})
        Experience.objects.update_or_create(role="Managing Director", company="Goldmine Agencies Limited", defaults={"start_date": date(2021, 1, 1), "location": "Kenya", "description": "Working at the intersection of business operations, digital services, technology, and sustainable commercial opportunity.", "stack": ["Business", "Digital services", "Operations"]})
        Experience.objects.update_or_create(role="Independent software engineer", company="IANO / LABS", defaults={"start_date": date(2020, 1, 1), "location": "Kenya", "description": "Building web applications, APIs, data workflows, and security-minded systems. Working across Python, Django, PHP, WordPress, JavaScript, TypeScript, databases, Linux, deployment, and third-party integrations.", "stack": ["Python", "Django", "PostgreSQL", "Cybersecurity", "Deployment"]})
        Education.objects.update_or_create(institution="University studies", degree="Bachelor's degree", defaults={"field": "Mathematics and Chemistry, major in Statistics", "start_date": date(2016, 1, 1), "end_date": date(2020, 12, 31), "details": "Graduated with honors. Developed a foundation in analytical thinking, research, statistical reasoning, problem solving, and evidence-based decisions."})
        certifications = [
            ("Python and web development", "Independent learning", date(2022, 6, 1), ""),
            ("Cybersecurity foundations", "Professional development", date(2023, 4, 1), "https://www.credly.com/badges/0c40ea8e-867a-418b-8ce8-6688fd0870f2/public_url"),
            ("Data analysis and research", "Professional development", date(2024, 2, 1), ""),
        ]
        for name, issuer, issued_date, credential_url in certifications:
            Certification.objects.update_or_create(
                name=name,
                issuer=issuer,
                defaults={"issued_date": issued_date, "credential_url": credential_url},
            )
        Post.objects.get_or_create(title="The best ML system is usually a product decision", defaults={"author": user, "excerpt": "Models matter. The workflow around the model matters more.", "body": "A model can be technically excellent and still fail to create value.\\n\\nThe real work is deciding what signal is useful, who needs it, and what happens after the prediction. That is where the system becomes a product.", "status": "published", "published_at": timezone.now()})
        question_tag, _ = QuestionTag.objects.get_or_create(name="python")
        question, _ = Question.objects.get_or_create(title="When does a data pipeline need a queue?", defaults={"author": user, "body": "I am designing a small ML workflow and want to keep the first version simple without painting the system into a corner. What signals tell you it is time to introduce a queue?", "status": "open"})
        question.tags.add(question_tag)
        self.stdout.write(self.style.SUCCESS("Starter portfolio content is ready."))
