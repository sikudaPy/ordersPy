from django.db import models

class Feedback(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    comment = models.TextField(max_length=1024) 

class FeedbackComment(models.Model):
    feedback = models.ForeignKey(Feedback,on_delete = models.CASCADE,blank=False)
    comment = models.TextField(max_length=1024) 


