import smtplib
from email.message import EmailMessage
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
import logging
import os
import re
from datetime import datetime
from selenium.webdriver.support.select import Select

def is_valid_contact(contact):
    return bool(re.fullmatch(r"\d+", str(contact)))

def is_valid_number(contact):
    contact = str(contact).strip() if pd.notna(contact) else ""  # Convert to string safely
    return bool(re.fullmatch(r"\d{10}", contact))

def is_valid_name(name):
    name = str(name).strip() if pd.notna(name) else ""  # Convert to string and remove extra spaces
    return bool(re.fullmatch(r"[A-Za-z ]+", name))

def is_valid_age(age):
    try:
        age = int(age)  # Convert to integer
        return 17 <= age <= 35  # Check if within range
    except ValueError:
        return False

def is_valid_email(mail):
    mail = str(mail).strip() if pd.notna(mail) else ""  # Convert to string and remove spaces
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"  # Email regex pattern
    return bool(re.fullmatch(pattern, mail))  # Check if email matches the pattern

current_date = datetime.now()
log_dir = 'logs'
os.makedirs(log_dir, exist_ok=True)
log_file_name = "logs - "+ current_date.strftime('%Y-%m-%d_%H-%M-%S.log')
log_file_path = os.path.join(log_dir, log_file_name)
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load the Excel data
file_path = "C:/Users/asus/OneDrive/Desktop/Project/dummy.xlsx"
df = pd.read_excel(file_path)
df["enrollment_date"] = pd.to_datetime(df["enrollment_date"]).dt.date

# Initialize counters
total_records = len(df)
success_count = 0
fail_count = 0

# Path to your WebDriver
driver_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe'

# Path to your local HTML file
html_file_path = 'http://localhost/draft HTML.html'

# Initialize the WebDriver (outside the loop)
driver = webdriver.Chrome()

try:
    for index, row in df.iterrows():
        try:
            logging.info("Starting to enter the  details of "+row["name"])
            Student_Id = row["student_id"]
            Name = row["name"]
            if is_valid_name(Name):
                print(f"Valid name - "+row["name"])
            else:
                print(f"Invalid name - "+row["name"])
                raise Exception("INVALID name " +row["name"]+ "given by student")
            Gender = row["gender"]
            Age = row["age"]
            if is_valid_age(Age):
                print(f" Valid age ")
            else:
                print(f"Invalid age")
                raise Exception("Invalid Age given by student :" + row["name"])
            ContactNumber = row["contact_number"]
            if is_valid_contact(ContactNumber):
                print(f"contact number has only numbers")
            else:
                print(f"INVALID contact number "+row["contact_number"] +"given by student :"+row["name"])
                raise Exception("INVALID contact number"+row["contact_number"] +"given by student :"+row["name"])
            if is_valid_number(ContactNumber):
                print(f"Valid 10-digit contact number")
            else:
                print(f"INVALID contact number given by student :" + row["name"])
                raise Exception("INVALID contact number - number do not have 10 digits given by student :" + row["name"])
            email = row["email"]
            if is_valid_email(email):
                print(f"Valid email ")
            else:
                print(f"Invalid email "+row["email"] + "given by student :"+row["name"])
                raise Exception("Invalid email " + row["email"] + "given by student :" + row["name"])

            Course_Id = row["course_id"]
            Course_Title = row["course_title"]
            Department = row["department_name"]
            TC_provided = row["tc_provided_status"]
            Marksheet_Provided = row["marksheet_provided_status"]
            Admission_date = str(row["enrollment_date"])  # Convert date to string

            # Open the web page
            driver.get(html_file_path)

            # Wait for the page to load
            time.sleep(2)

            # Locate form fields
            StudentId_field = driver.find_element(By.ID, 'student-id')
            Name_field = driver.find_element(By.ID, "student-name")
            Age_field = driver.find_element(By.ID, "age")
            gender_dropdown = driver.find_element(By.ID, "gender")
            gender_select = Select(gender_dropdown)
            ContactNumber_field = driver.find_element(By.ID, "contact-number")
            Email_field = driver.find_element(By.ID, "email")
            CourseId_field = driver.find_element(By.ID, "course-id")
            CourseTitle_field = driver.find_element(By.ID, "course-title")
            DepartmentName_field = driver.find_element(By.ID, "Department-Name")
            tc_provided_dropdown = driver.find_element(By.ID, "tc-provided")
            tc_provided_select = Select(tc_provided_dropdown)
            tc_provided_select.select_by_visible_text("Yes")
            tc_provided_select.select_by_visible_text("No")
            marksheet_provided_dropdown = driver.find_element(By.ID, "Marksheet-provided")
            marksheet_provided_select = Select(marksheet_provided_dropdown)
            admission_date_field = driver.find_element(By.ID, "enrollment-date")
            submit_button = driver.find_element(By.NAME, "Submit")


            # Fill out the form
            StudentId_field.send_keys(Student_Id)
            Name_field.send_keys(Name)
            Age_field.send_keys(Age)
            gender_select.select_by_visible_text(Gender)
            ContactNumber_field.send_keys(ContactNumber)
            Email_field.send_keys(email)
            CourseId_field.send_keys(Course_Id)
            CourseTitle_field.send_keys(Course_Title)
            DepartmentName_field.send_keys(Department)
            tc_provided_dropdown.send_keys(TC_provided)
            marksheet_provided_dropdown.send_keys(Marksheet_Provided)
            admission_date_field.send_keys(Admission_date)

            # Submit the form
            submit_button.click()

            success_count += 1

            # Wait before moving to the next record
            time.sleep(1)
            logging.info("Entered the details of Student name :"+row["name"]+" successfully")
        except Exception as e:
            print("Exception is:", e)
            logging.error("Exception occured "+str(e))
            fail_count += 1
except Exception as e:
        print("Exception is:", e)
        logging.error("Exception is:",e)
    # print("All records processed successfully!")

finally:

    results_file_path = "C:/xampp/htdocs/result.txt"

    # Save results to a text file
    with open(results_file_path, "w") as file:
        file.write(f"total_records={total_records}\n")
        file.write(f"success_count={success_count}\n")
        file.write(f"fail_count={fail_count}\n")
    time.sleep(5)
    driver.execute_script("window.open('http://localhost/report.php', '_blank');")
    print("Results saved to results.txt")
    time.sleep(30)


    # Send email notification after processing
    sender_email = "haarishkcb@gmail.com"
    sender_password = "dnkgammhqxdtjrza"
    recipient_email = "22ucs145@loyolacollege.edu"

    msg = EmailMessage()
    msg['Subject'] = "Automation Process Completed"
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg.set_content("Hello,\n\nThe Selenium automation process has successfully completed.\n\nRegards,\nYour Automation System")

    try:
        # Connect to Gmail SMTP server
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
            print("Email sent successfully!")

    except Exception as e:
        print("Failed to send email:", e)


def automation_process():
    try:
        logging.info("Automation process started.")

        # Simulating data extraction
        logging.info("Extracting data from Excel.")
        # (Your code for reading Excel)

        # Simulating database update
        logging.info("Updating MySQL database.")
        # (Your code for updating MySQL)

        # Simulating Selenium operations
        logging.info("Performing web automation using Selenium.")
        # (Your Selenium automation code)

        logging.info("Automation process completed successfully.")

        # Call the function after automation
        after_completion()

    except Exception as E:
        print("Failed to send email:", E)


def after_completion():
    logging.info("Post-processing task started.")
    # Example: Send an email notification
    send_email_notification()
    logging.info("Post-processing task completed.")

def send_email_notification():
    """Simulated function to send an email notification."""
    logging.info("Sending email notification...")
    # Your email sending logic here (e.g., using smtplib)
    logging.info("Email sent successfully.")

# Run the automation process
automation_process()