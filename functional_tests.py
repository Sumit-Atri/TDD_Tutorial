from selenium import webdriver

browser = webdriver.Chrome()
browser.get("http://localhost:8000/admin")

assert "Log in | Django site admin" in browser.title
print("OK")