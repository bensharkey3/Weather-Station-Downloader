import json
import boto3
import smtplib
import datetime
import requests
import os


class ImageNameUrl:
    def __init__(self, name, url):
        '''creates an object for each image containing its url and giving it a name'''
        self.name = name
        self.url = url
        
        
def download_image(url, name, bucket_name):
    '''Retrieves an image from the provided url, and saves to the directory provided.
    Args:
        url (str): the image address
        directory (str): the file directory for the image to be saved
        name (str): the name of the image
    Returns:
        none
    '''
    object_key = datetime.datetime.today().strftime('%Y-%m-%d') + '-' + name +'.png'
    s3_object = boto3.resource('s3').Object(bucket_name, object_key)
    
    with requests.get(url, stream=True) as r:
        s3_object.put(Body=r.content)
    

def send_basic_gmail(to_email, subject, message_body):
    '''this function sends an email from bensharkeyreporting@gmail.com'''
    gmail_sender = 'bensharkeyreporting@gmail.com'
    gmail_pwd = os.environ['gmail_pwd']

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(gmail_sender, gmail_pwd)

    email_string = '\r\n'.join(['To: %s' % to_email,
        'From: %s' % gmail_sender,
        'Subject: %s' % subject,
        '', message_body])

    try:
        server.sendmail(gmail_sender, [to_email], email_string)
        print ('email sent')
    except:
        print ('error sending mail')

    server.quit()


def lambda_handler(event, context):
    '''runs program
    '''
    bucket_name = 'cape-lambert-weather-station-images'
    success_count = 0
    fail_count = 0
    
    meterologystation = ImageNameUrl('meterologystation', r'http://www.pilbarairon.com/DprCLWeather/GraphInfo/CLW_Met.Gif')
    capelambertdolphin34 = ImageNameUrl('capelambertdolphin34', r'http://www.pilbarairon.com/DprCLWeather/GraphInfo/D34_Wave.Gif')
    capelambertbeacon28 = ImageNameUrl('capelambertbeacon28', r'http://www.pilbarairon.com/DprCLWeather/GraphInfo/M28_Met.Gif')
    beacon14wavesignificant = ImageNameUrl('beacon14wavesignificant', r'http://www.pilbarairon.com/DprCLWeather/GraphInfo/B14_Wave.Gif')
    beacon14wavemax = ImageNameUrl('beacon14wavemax', r'http://www.pilbarairon.com/DprCLWeather/GraphInfo/B14_MAX.Gif')

    image_list = [meterologystation,
                  capelambertdolphin34,
                  capelambertbeacon28,
                  beacon14wavesignificant,
                  beacon14wavemax]
                  
    email_recipient_list = ['bensharkey3@gmail.com',
                            'brenton.savio@australconstruction.com.au']
    
    # download images
    for i in image_list:
        try:
            download_image(i.url, i.name, bucket_name)
            success_count+=1
        except Exception as ex:
            fail_count+=1
            print(i.name + ': ' + str(ex))
    
    message = '{} images downloaded, {} errors encountered'.format(success_count, fail_count)
    
    for i in email_recipient_list:
        send_basic_gmail(i, message, "downloaded images to s3 bucket 'cape-lambert-weather-station-images'")
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
