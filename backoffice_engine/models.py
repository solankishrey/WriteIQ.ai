from django.db import models
from django.utils import timezone

# Create your models here.

class BaseModel(models.Model):
    id=models.AutoField(primary_key=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class User(BaseModel):
    name=models.CharField(max_length=20)
    email=models.EmailField(max_length=100,unique=True)
    password=models.CharField(max_length=50) 
    otp=models.CharField(max_length=6)
    otp_used=models.IntegerField() 
        
    class Meta:
        db_table="user"

    def __str__(self):
        return f" {self.id} - {self.name}"

class Category(BaseModel):
    name=models.CharField(max_length=50)        
    description=models.CharField(max_length=50)

    class Meta:
        db_table="category"

    def __str__(self):
        return f"{self.name} - {self.description}"

class SubCategory(BaseModel):
    name=models.CharField(max_length=20)
    description=models.CharField(max_length=20)
    category_id=models.ForeignKey(Category,null=True,on_delete=models.CASCADE)

    class Meta:
        db_table="sub_category"

    def __str__(self):
        return f"{self.name} - {self.description}-{self.category_id}"
        
class GeneratedContent(BaseModel):
    prompt=models.CharField(max_length=200)
    content=models.TextField()
    category_id=models.ForeignKey(Category,null=True,on_delete=models.CASCADE)
    sub_category_id=models.ForeignKey(SubCategory,null=True,on_delete=models.CASCADE)
    user_id=models.IntegerField(max_length=10)

    class Meta:
        db_table="content_generator"

    def __str__(self):
        return f"{self.user_id}  -  {self.prompt}  -  {self.category_id}"

        
        
class PlanDetails(BaseModel):
    name=models.CharField(max_length=255)
    description=models.TextField(null=True,blank=True)
    price=models.IntegerField(null=False,blank=False)
    duration_days=models.IntegerField(default=30)
    credit=models.IntegerField(null=False,blank=False)
    is_active = models.BooleanField(default=True)


    
    def __str__(self):
        return f"{self.name}-{self.description}"
        
    class Meta:
        db_table="Plan_Details"   

class Subscription(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(PlanDetails, on_delete=models.CASCADE, null=True)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True, blank=True)
    status=models.CharField(max_length=20,default='active')
    pending_credit=models.IntegerField(default=5)
    total_credit = models.IntegerField(default=0)


    def __str__(self):
        return f"{self.user} - {self.plan}"

    class Meta:
        db_table="Subscription"

class Feedback(BaseModel):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    message = models.TextField()
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name} - {self.rating}"
    
    class Meta:
        db_table="Feedback"

        
