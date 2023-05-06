import getpass
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--headless')

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.facebook.com/")

wait = WebDriverWait(driver, 20)


def login():
  email_xpath = "//input[@id='email']"
  USERNAME = input("Enter facebook ID: ")
  wait.until(EC.presence_of_element_located((By.XPATH, email_xpath)))
  driver.find_element(By.XPATH, email_xpath).clear()
  driver.find_element(By.XPATH, email_xpath).send_keys(USERNAME)

  PASSWORD = getpass.getpass("Enter password: ")
  password_xpath = "//input[@id='pass']"
  driver.find_element(By.XPATH, password_xpath).clear()
  driver.find_element(By.XPATH, password_xpath).send_keys(PASSWORD)

  wait.until(EC.element_to_be_clickable((By.NAME, "login")))
  driver.find_element(By.NAME, "login").click()
  print("Logging in...........")
  wait.until(
    EC.presence_of_element_located(
      (By.XPATH, "(//div[@class='x78zum5 x1n2onr6'])[1]")))
  print(f"Log in successful as {USERNAME}")


def get_birthday_lists():
  driver.get("https://www.facebook.com/events/birthdays/")
  print("Getting list of friends having birthday today......")
  todays_birthday_xpath = (
    "(//div[contains(@class,'x1oo3vh0 xexx8yu x1pi30zi x18d9i69 x1swvt13')])[1]"
  )
  wait.until(EC.presence_of_element_located((By.XPATH, todays_birthday_xpath)))

  # Parent element with list of friends birthday available for the current date.
  todays_birthday_element = driver.find_element(By.XPATH,
                                                todays_birthday_xpath)

  # Sometimes some friends having birthday timeline are not available. So, firstly the timeline has to be checked.
  # Getting the timeline field for posting message on the friends timeline.
  global friends_timeline
  friends_timeline = todays_birthday_element.find_elements(
    By.XPATH, ".//p[@class='xdj266r x11i5rnm xat24cr x1mh8g0r x16tdsg8']")

  # Finding the parent element where both friends name and timeline are available.
  parent_elements = [
    child_element.find_element(
      By.XPATH,
      "ancestor::div[@class='xamitd3 x1r8uery x1iyjqo2 xs83m0k xeuugli']",
    ) for child_element in friends_timeline
  ]

  # Appending friend's name as a list from the parent elements.
  # List comprehension method.
  global friend_lists
  friend_lists = [
    (parent_element.find_element(By.XPATH,
                                 ".//div[@class='x78zum5 xdt5ytf']")).text
    for parent_element in parent_elements
  ]
  # print(friend_lists)
  return friend_lists


def msg_selected_friends():
  # For posting birthday message on selected friends timeline.
  birthday_msg = "May all your wishes come true today and always! Happy birthday!"
  selection_list = input(
    "Provide the list of numbers whom you want to send birthday message. Eg. 1,2,3:\n"
  ).split(",")

  if selection_list.lower() != "q":
    for i in selection_list:
      friends_timeline[int(i) - 1].send_keys(birthday_msg)
      friends_timeline[int(i) - 1].send_keys(Keys.ENTER)
      print(f"Birthday post posted on {friend_lists[int(i)-1]} timeline.")


def msg_all_friends():
  # Posting birthday messages on all friends timeline.
  birthday_msg = "May all your wishes come true today and always! Happy birthday!"
  for i in range(len(friends_timeline)):
    friends_timeline[i].send_keys(birthday_msg)
    friends_timeline[i].send_keys(Keys.ENTER)
    print(f"Birthday post posted on {friend_lists[i]} timeline.")


def logout():
  login_title = driver.title

  # Click on the profile icon
  driver.find_element(By.XPATH,
                      "(//div[@class='x78zum5 x1n2onr6'])[1]").click()

  # Wait for the dropdown menu to appear
  wait.until(
    EC.presence_of_element_located(
      (By.XPATH, "//span[normalize-space()='Log Out']")))

  # Click on the log out button
  driver.find_element(By.XPATH, "//span[normalize-space()='Log Out']").click()

  # Logout Confirmation
  while True:
    logout_title = driver.title
    if login_title != logout_title:
      msg = "Log out successful..."
      return msg


try:
  login()
  print(get_birthday_lists())

  user_input = input("Do you want to send msg to all your friends: ")

  while True:
    if user_input.lower() == "y":
      msg_all_friends()
      break
    elif user_input == "n":
      msg_selected_friends()
      break
    elif user_input == "q":
      break
    else:
      print("Invalid input. Ans (y/n) or q to quit.")
      user_input = input("Do you want to send msg to all your friends: ")
finally:
  print(logout())
  driver.quit()
