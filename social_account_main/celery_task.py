import os
import json
import urllib.request
from celery import Celery, shared_task
from django.conf import settings 
from django.core.mail import EmailMessage, get_connection, send_mail, send_mass_mail
import time
from access_token import LONGLIVED_ACCESS_TOKEN, USER_LONGLIVED_ACCESS_TOKEN




# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_account_main.settings')

app = Celery('social_account_main')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# LONGLIVED_ACCESS_TOKEN = "EAAHUhP0dyaEBAIgIVZBE6AMX5W7OHtf4goo1jK9mZCddy3lgEhFKZBkp622uUT8rhtnYOl1dC9rZC24rtK5GuU5JTREJ3cAvVOHenrV81ieQTmZAtIVoP5KMhPwlnomXhuuX9KhjXZCVu99HD62qHElU2V89ZB8v17hPCTxPGYGNDBklTvdayYJzkZC8bVk6mmgeG1aFbyLAcwZDZD"


@app.task(bind=True)
def do_stuff(self):
    print(f'Request: {self.request!r}')


@shared_task()
def add():
    print("2")
    return 1+1


# @shared_task()
def send_email():  
    with get_connection(  
        host=settings.EMAIL_HOST, 
    port=settings.EMAIL_PORT,  
    username=settings.EMAIL_HOST_USER, 
    password=settings.EMAIL_HOST_PASSWORD, 
    use_tls=settings.EMAIL_USE_TLS  
    ) as connection:  
        subject = "Welcome to our community! 🍚 Your 10 Delicious Rice Recipes are attached below!"
        email_from = settings.EMAIL_HOST_USER  
        # recipient_list = json.load(open('JSON/emails.json', 'r'))['new_email']
        recipient_list = ["kundanpandey.dev@gmail.com", "kundan.k.pandey03@gmail.com","kundan.k.pandey02@gmail.com" ]   
        if len(recipient_list) != 0:

            html_content = open("template/email.html").read()
            pdf_file = open("template/GER Document.pdf", 'rb').read()
            mass_email_message = [] 
            for recipient in recipient_list:
                email = EmailMessage(subject, html_content, email_from, [recipient], connection=connection)
                email.content_subtype = "html"
                email.attach("GER Document.pdf", pdf_file) 
                mass_email_message.append(email)

            connection.send_messages(mass_email_message)
            print(recipient_list)
            print('Mail sent to above list of mails.')

        else:
            print("NO NEW LEADS FOUND!")
        


        # email.send()

# make a call every 5 minutes and see if there are any new users
def get_all_leads(file_path='JSON/data.json'):
    ads_id = "723940182548849"
    all_leads = f"https://graph.facebook.com/{ads_id}/leads?access_token={LONGLIVED_ACCESS_TOKEN}"
    leads_object = json.loads(urllib.request.urlopen(all_leads).read())    
    json_object = json.dumps(leads_object)
    json_file = open('JSON/data.json', 'w', encoding='utf-8')
    json_file.write(json_object)
    json_file.close() 
    time.sleep(3)  
    # <==============================>


def intersection(test_list, remove_list):
    res = [i for i in test_list if i not in remove_list]
    return res



def store_email_to_json(file_path="JSON/data.json"):
    email_dir = {}
    email_list = []
    with open(file_path, 'r', encoding='utf-8') as json_file:
        file_data = json.load(json_file)
    print(len(file_data['data']))
    for d in file_data['data']:
        for n in d['field_data']:
            if n['name'] == 'email':
                # print(n['values'])
                email = n['values']
                email_list.extend(email)
    print(len(email_list))
    email_dir["email"] = email_list # store the email from the current leads 
    old_email_json = open("JSON/emails.json", "r+", encoding='utf-8') # read the existing email.json
    old_email_data = json.load(old_email_json)
    new_email = intersection(email_dir['email'], old_email_data['email'])
    print(new_email)
    print(len(new_email))
    email_dir['new_email'] = new_email

    email_json = open('JSON/emails.json', 'w', encoding='utf-8')
    json_obejct = json.dumps(email_dir, indent=4)
    email_json.write(json_obejct)
    email_json.close()




@app.task()
def create_json_and_send_email():
    get_all_leads()
    store_email_to_json()
    send_email()



   





