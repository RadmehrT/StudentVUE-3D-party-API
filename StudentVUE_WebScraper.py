import json
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

class StudentVUE_WebScraper:
    
    
    
    def __init__(self, studentVUE_URL, STUDENT_VUE_COURSE_HISTORY_URL):
        self.studentVUE_URL = studentVUE_URL
        self.studentVUE_course_history_URL = STUDENT_VUE_COURSE_HISTORY_URL
        
    def set_json_file_name(self, filename):
        self.json_file_name = filename + ".json"   
        
    def get_json_file_name(self):
        return self.json_file_name
        
    def store_data_in_json(self, filename):
        try:
            json_file = open(filename, "w")
        
            json.dump(self.courses_data, json_file, indent=4)
        except json.JSONDecodeError:
            print("There was an issue parsing the JSON")
            
            
            
    def delete_json_file(self, filename):
        
        if os.path.exists(filename):
            os.remove(filename)
            print(f"{filename} has been deleted.")
        
        
        
    def set_username(self, username):
        self.username = username
        
    def set_password(self, password):
        self.password = password
            
    def get_username(self):
        return self.username        
    
    def get_password(self):
        return self.password      
    
    
      
            
    def run(self):

        #Course_History URL will have to be updated based on district as well.
       
        LOGIN_URL = self.studentVUE_URL
        try:
            USERNAME = self.username
            PASSWORD = self.password
            
        except Exception as error:
            print("something went wrong please try again")

        chrome_options = Options()
        chrome_options.add_argument("--headless") 
        chrome_options.add_argument("--disable-gpu")

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)


        driver.get(LOGIN_URL)

        wait = WebDriverWait(driver, 20)
        username_input = wait.until(EC.presence_of_element_located((By.NAME, "ctl00$MainContent$username")))
        password_input = driver.find_element(By.NAME, "ctl00$MainContent$password")

        username_input.send_keys(USERNAME)
        password_input.send_keys(PASSWORD)

        login_button = driver.find_element(By.NAME, "ctl00$MainContent$Submit1")
        login_button.click()

        print("Current URL after login:", driver.current_url)


        driver.get(self.studentVUE_course_history_URL)


        label = wait.until(EC.element_to_be_clickable((By.XPATH, "(//label[@class='pxp-switch'])[last()]")))
        label.click()




        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='chs-data']/table")))

        course_rows = driver.find_elements(By.XPATH, "//div[@class='chs-data']/table/tbody/tr")

        self.courses_data = []

        for row in course_rows:
            try:
                course_title = row.find_element(By.XPATH, ".//span[@data-bind='text: CourseTitle']").text
                course_id = row.find_element(By.XPATH, ".//span[@data-bind='text: CourseID']").text
                mark = row.find_element(By.XPATH, ".//span[@data-bind='text: Mark']").text
                credits_attempted = row.find_element(By.XPATH, ".//span[@data-bind='text: CreditsAttempted']").text
                credits_completed = row.find_element(By.XPATH, ".//span[@data-bind='text: CreditsCompleted']").text
                chs_type = row.find_element(By.XPATH, ".//span[@data-bind='text: CHSType']").text

                print(f"Course: {course_title} ({course_id}) | Mark: {mark} | Credits: {credits_attempted}/{credits_completed} | Type: {chs_type}")
                
                course_info = {
                    "CourseTitle": course_title,
                    "CourseID": course_id,
                    "Mark": mark,
                    "CreditsAttempted": credits_attempted,
                    "CreditsCompleted": credits_completed,
                    "CHSType": chs_type
                }
                
                self.courses_data.append(course_info)
            
            except Exception as e:
                print(f"Error processing row: {e}")

        self.store_data_in_json(self.get_json_file_name())

        driver.quit()
        