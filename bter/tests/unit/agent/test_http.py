from bter.http import http_util

httpclient = http_util.HttpClient()
response = httpclient.download("http://data.bter.com/api2/1/ticker/btc_cny")
print(response.content)
