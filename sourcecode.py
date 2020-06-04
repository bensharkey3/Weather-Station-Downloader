import urllib.request

code = 'https://raw.githubusercontent.com/bensharkey3/Weather-Station-Downloader/master/weather_station_downloader.py'
response = urllib.request.urlopen(code)
data = response.read()
exec(data)
