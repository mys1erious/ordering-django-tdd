import re


url = "http://127.0.0.1:8000/users/profile/43"


print(re.findall(r"/view/(\d*?).htm", "/view/123.htm /view/456.htm"))



id = re.findall(r'/profile/([0-9]*)', url)

print(id)