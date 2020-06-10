import urllib.request
import datetime
import os
import logging
import smtplib


class ImageNameUrl:
    def __init__(self, name, url):
        '''creates an object for each image containing its url and giving it a name'''
        self.name = name
        self.url = url

        
def download_image(url, directory, name):
    '''Retrieves an image from the provided url, and saves to the directory provided.
    Args:
        url (str): the image address
        directory (str): the file directory for the image to be saved
        name (str): the name of the image
    Returns:
        none
    '''
    path = directory + '/' + datetime.datetime.today().strftime('%Y-%m-%d') + '-' + name +'.jpg'
    urllib.request.urlretrieve(url, path)
    

def send_basic_gmail(to_email, subject, message_body):
    '''this function sends an email from bensharkeyreporting@gmail.com'''
    gmail_sender = 'bensharkeyreporting@gmail.com'
    gmail_pwd = 'reporting123'

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(gmail_sender, gmail_passwd)

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


def main():  
    '''Runs the program'''
    # create and configure logger 
    logging.basicConfig(filename="logs.log", 
        format='%(asctime)s - %(levelname)s - %(message)s', 
        datefmt='%Y-%m-%d %H:%M:%S',
        filemode='a') 

    logger=logging.getLogger() 
    logger.setLevel(20) 

    # define variables
    success_count = 0
    fail_count = 0
    directory = str(os.getcwd())

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

    # download images
    for i in image_list:
        try:
            download_image(i.url, directory, i.name)
            success_count+=1
        except Exception as ex:
            fail_count+=1
            print(i.name + ': ' + str(ex))
            logger.error(i.name + ': ' + str(ex))
    
    # write completion messages to logs and email
    if fail_count == 0:
        message = 'Successful - {} images downloaded'.format(success_count)
    else:
        message = 'ERROR - {} images downloaded, {} failed'.format(success_count, fail_count)
        
    print(message)
    logger.error(message)
    send_basic_gmail('ben.sharkey@gmail.com', message, '')

    
if __name__ == '__main__':
    main()
