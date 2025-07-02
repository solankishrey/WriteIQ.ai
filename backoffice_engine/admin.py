from django.contrib import admin
from backoffice_engine.models import User,PlanDetails,Category,SubCategory,Subscription,GeneratedContent,Feedback
# Register your models here.

admin.site.register(User)
admin.site.register(PlanDetails)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Subscription)
admin.site.register(GeneratedContent)
admin.site.register(Feedback)
