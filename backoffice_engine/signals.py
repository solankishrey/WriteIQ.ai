from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import PlanDetails, Category, SubCategory


@receiver(post_migrate)
def create_default_data(sender, **kwargs):
    if sender.name != 'backoffice_engine':
        return

    # --- Default Plans ---
    default_plans = [
        {"name": "Free Plan", "description": "Basic access", "price": 0, "duration_days": 30, "credit": 20},
        {"name": "Silver Plan", "description": "Access to premium features", "price": 499, "duration_days": 30, "credit": 100},
        {"name": "Gold Plan", "description": "Extended features and support", "price": 999, "duration_days": 90, "credit": 200},
    ]

    for plan in default_plans:
        PlanDetails.objects.get_or_create(name=plan["name"], defaults=plan)

    # --- Default Categories & SubCategories ---
    category_data = {
        "Email": ["Welcome Emails", "Transactional Emails", "Newsletters", "Promotional Emails", "Follow-up Emails", "Cold Emails"],
        "Letter": ["Formal Letter", "Informal Letter", "Business Letter", "Recommendation Letter"],
        "Application": ["Job Application", "Leave Application", "College Admission Application"],
        "Resume/CV": ["Fresher Resume", "Experienced Resume", "Creative Resume", "Academic CV"],
        "Essay": ["Descriptive Essay", "Narrative Essay", "Expository Essay", "Argumentative Essay"],
        "Report": ["Progress Report", "Incident Report", "Lab Report", "Project Report"],
        "Proposal": ["Business Proposal", "Research Proposal", "Project Proposal"],
        "Other":  ["Dialogue","Newsletter","Research Paper","Thesis Summary","Invitation","Statement of Purpose","Other"]

    }

    for cat_name, subcats in category_data.items():
        category, created = Category.objects.get_or_create(name=cat_name, defaults={"description": f"{cat_name} documents"})
        for subcat in subcats:
            SubCategory.objects.get_or_create(
                name=subcat,
                category_id=category,
                defaults={"description": f"{subcat} type"}
            )
