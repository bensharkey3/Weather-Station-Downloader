# Weather-Station-Downloader
A program that downloads various images from the Rio Tinto Cape Lambert weather station, and saves as files in an s3 bucket every morning.
Weather station website: http://www.pilbarairon.com/DprCLWeather/Weather.aspx

Python script is executed within an AWS Lambda

Lambda Requirements:
* Added Cloudwatch Event to execute code based on a cron schedule 
* Added the python 'requests' package as a Lambda layer
* Added the gmail account password as a Lambda Environment variable so that its not hard entered in the code
