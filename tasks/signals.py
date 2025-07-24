from django.db.models.signals import post_save,pre_save,m2m_changed, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from tasks.models import Task



@receiver(m2m_changed, sender=Task.assigned_to.through)
def notify_employee_on_task_creation(sender, instance, action , **kwargs):
    if action == 'post_add':
        print(instance, instance.assigned_to.all())
        assigned_email = [emp.email for emp in instance.assigned_to.all()]
        send_mail(
            "New Task Assigned",
            f"You have been assignto to the task: {instance.title}",
            "kamrulkhan526785@gmail.com",
            assigned_email,
            fail_silently=False,
        )

@receiver(post_delete, sender= Task)
def delete_associated_details(sender, instance, **kwargs):
    if instance.details:
        print(isinstance)
        instance.details.delete()
        
        print('Deleted Successfully')