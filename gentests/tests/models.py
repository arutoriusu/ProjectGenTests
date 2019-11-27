from django.db import models

class Tag(models.Model):
    name_tag = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.name_tag}'

class Task(models.Model):
    question = models.CharField(max_length=30)
    answer = models.CharField(max_length=30)
    img = models.ImageField(blank=True, null=True)
    tip = models.CharField(max_length=30, blank=True, null=True)
    tag = models.ForeignKey(to=Tag, on_delete=models.CASCADE, related_name='tasks', blank=True, null=True)
    
    def __str__(self):
        return f'{self.question}'

class Test(models.Model):
    theme_of_test = models.CharField(max_length=30)
    task = models.ForeignKey(to=Task, on_delete=models.CASCADE, related_name='tasks')

    def __str__(self):
        return f'{self.theme_of_test}'
