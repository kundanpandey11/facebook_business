from django.db import models
from django.contrib.auth.models import User 

# usermodel will be responsible for taking out links of 
# the own pages and store it in a json file
class UserModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    page_url_json = models.FileField()
    


# save all the json file in a seperate table 
class UserJsonFiles(models.Model):
    usermodel = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_json_file = models.FileField()
    page_url = models.CharField(max_length=300, null=False, blank=False)
    page_name = models.CharField(max_length=100, null=True, blank=True)




class CreateRequest(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    url = models.CharField(max_length=500, unique=True, null=False, blank=False)
    # email = models.EmailField(null=False, blank=False)
    post_count = models.IntegerField()

    def __str__(self):
        return self.name
    

