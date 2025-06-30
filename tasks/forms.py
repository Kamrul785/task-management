from django import forms
from tasks.models import Task

# Django Form 
class TaskForm(forms.Form):
    title = forms.CharField(max_length=250,label="Task Title")
    description = forms.CharField(widget=forms.Textarea,label="Task Description")
    due_date = forms.DateField(widget=forms.SelectDateWidget,label="Due Date") 
    assigned_to = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=[],label="Assign To")
    
    def __init__(self, *args, **kwargs):
        # print(args,kwargs)
        employees = kwargs.pop('employees',[])
        super().__init__(*args,**kwargs)
        self.fields['assigned_to'].choices =[(emp.id,emp.name) for emp in employees]  


class StyledFormMixin:
    """ Mixing to apply styles to form fields"""
    default_classes = "border-2 border-gray-300 shadow-md w-full rounded-lg focus:border-rose-300 focus:ring-rose-500 px-3"
    
    def apply_styled_widgets(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'placeholder': f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget,forms.Textarea):
                field.widget.attrs.update({
                    'class': f"{self.default_classes}",
                    'placeholder': f"Enter {field.label.lower()}",
                    'rows': 5
                })
            elif isinstance(field.widget,forms.SelectDateWidget):
                field.widget.attrs.update({
                    'class' : "border-2 border-gray-300 shadow-md rounded-lg focus:border-rose-300 focus:ring-rose-500 px-3 h-10"
                })
            elif isinstance(field.widget,forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    'class' : "space-y-2"  
                })
    

# Django Model Form 
class TaskModelForm(StyledFormMixin,forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title','description','due_date', 'assigned_to']
        # exclude = ['project','is_completed','created_at','updated_at']  # ae file gula bad diye dekhano 
        widgets ={
            'due_date': forms.SelectDateWidget,
            'assigned_to':forms.CheckboxSelectMultiple
        }
        
        
        """ Style mixing use korle ae vabe widgets ar use korte hobe na. redundancy kombe"""
        '''" Manual widget styling ''' 
        # widgets = {
        #     'title':forms.TextInput(attrs={
        #         'class':"border-2 border-gray-300 shadow-md w-full rounded-lg focus:border-rose-300 focus:ring-rose-500 px-3 h-10",
        #         'placeholder':"Enter Task Title"
        #     }),
        #     'description':forms.Textarea(attrs={
        #         'class':"border-2 border-gray-300 shadow-md w-full rounded-lg focus:border-rose-300 focus:ring-rose-500 px-3 h-20",
        #         'placeholder':"Descrip the tast",
        #         'rows' : 5
        #     }),
        #     'due_date':forms.SelectDateWidget(attrs={
        #         'class':"border-2 border-gray-300 shadow-md rounded-lg focus:border-rose-300 focus:ring-rose-500",
        #     }),
        #     'assigned_to':forms.CheckboxSelectMultiple(attrs={
        #         'class': "space-y-2",
        #     })
        # }
    
    """ Widget using mixing """
    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()
        