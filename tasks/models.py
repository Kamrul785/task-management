from django.db import models
from django.conf import settings

class Task(models.Model):   
    STATUS_CHOICES =(
        ('PENDING','Pending'),
        ('IN_PROGRESS','In Progress'),
        ('COMPLETED','Completed'),
    )
    project = models.ForeignKey(           
        "Project",
        on_delete=models.CASCADE, 
        default=1
    )
    assigned_to = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='tasks'
    )
    
    title = models.CharField(max_length=250)
    description = models.TextField()
    due_date = models.DateField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now= True)
    
    def __str__(self):
        return self.title
    
    # one to one 
    # many to one
    # many to many


# one to one relationship
class TaskDetail(models.Model):
    HIGH = 'H'
    MEDIUM = 'M'
    LOW = 'L'
    PRIORITY_OPTIONS = (
        (HIGH, 'High'),
        (MEDIUM,'Medium'),
        (LOW,'Low')
    )
    
    task = models.OneToOneField(
        Task,
        on_delete=models.CASCADE,
        related_name="details"
    )
    asset = models.ImageField(upload_to='task_asset', blank=True, null=True, default='task_asset/default_img.jpg')
    priority = models.CharField(max_length=1,choices=PRIORITY_OPTIONS,default=LOW)
    notes = models.TextField(blank = True, null = True)
    
    def __str__(self):
        return f'Details from task {self.task.title}'

# many to many relationship
# task = onkgula employee ekta task
# employee = onk gula task er jonno assign ase
class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True,null=True)
    start_date = models.DateField()
    
    def __str__(self):
        return self.name
    

        