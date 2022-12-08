from django.db import models

class Course(models.Model):
    code = models.CharField('course code', max_length=20, unique=True)
    title = models.CharField('course title', max_length=200)
    is_active = models.BooleanField('active', default=True)

    def __str__(self):
        return f'{self.id}) {self.code} - {self.title}'