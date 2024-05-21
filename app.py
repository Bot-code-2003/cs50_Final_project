#app.py
import requests
from time import sleep
from tabulate import tabulate
import csv
import os
from datetime import date
import bcrypt

def main():
  salt = bcrypt.gensalt()
  keyflow("1. Register\n2. Login\n3. Logout\n")
  keyflow("Choose option: ")
  choice = input()
  match choice:
      
      case "1": 
          if register():
            username, password, city = login()
          if username is not None:
              keyflow("Login success!\n")
              keyflow(f"Hello {username}, I am Robin, your personal productivity manager.\n")
              fetch_weather(city)
              task_manager(username)
      case "2": 
          username, password, city = login()
          if username is not None:
              keyflow("Login success!\n")
              keyflow(f"Hello {username}, I am Robin, your personal productivity manager.\n")
              fetch_weather(city)
              task_manager(username)
      case "3":
          keyflow("Good Bye\n")
# Typing effect
def keyflow(Title):
  for char in Title:
    sleep(0.01)
    print(char, end="")

# Load the user info
def load_info_from_csv():
    personal_info = []
    try:
        with open('personal_info.csv', "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                personal_info.append(row)    
    except FileNotFoundError:
        pass
    return personal_info

# Save the first time user info.
def save_info_to_csv(personal_info):
    file_exists = os.path.isfile('personal_info.csv')
    with open('personal_info.csv', "a", newline="") as file:
        fieldnames = ['username', 'password', 'city']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not file_exists:  # Check if file exists and is empty
            writer.writeheader()
        writer.writerows(personal_info) 


personal_info = []
def register():
    print("REGISTER")
    keyflow("Welcome user! I am Robin, your personal productivity manager.\n")
    keyflow("Username: ")
    username = input()
    keyflow("Password: ")
    password = input()
    keyflow("City: ")
    city = input()
    personal_info.append({"username": username, "password": password, "city": city })
    save_info_to_csv(personal_info)
    return True

def login():
    personal_info = load_info_from_csv()  # Note the parenthesis to actually call the function
    print("LOGIN")
    print("Welcome user! I am Robin, your personal productivity manager.")
    username = input("Username: ")
    password = input("Password: ")
    for info in personal_info:
        if info['username'] == username and info['password'] == password:
            return info['username'], info['password'], info['city']
    print("Invalid username or password. Please try again.")
    return None, None, None

# Fetch weather and respond accordingly
def fetch_weather(city):
    api_key = "fed93326c16e64a95eae94565cc60a22"
    while True:
        weather_data = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city.lower()}&unit=imperial&APPID={api_key}")
        weather_json = weather_data.json()
        if "cod" in weather_json and weather_json["cod"] == 200:
            if "weather" in weather_json and len(weather_json["weather"]) > 0:
                weather_main = weather_json["weather"][0]["main"]
            else:
                weather_main = "Not available!"
            if "main" in weather_json and "temp" in weather_json["main"]:
                temp = round(weather_json["main"]["temp"])
            else:
                temp = "Not available!"
                
            if weather_main.lower() == "rain":
                keyflow(f"☔☔ The weather currently in {city} is {weather_main} and its {temp}°F. Carry an umbrella. ☔☔")
            elif weather_main.lower() == "thunderstorm":
                keyflow(f"⛈️⛈️ Be cautious There's a {weather_main} in {city}. The temperature is {temp}°F. Prefer staying indoor! ⛈️⛈️")
            elif weather_main.lower() == "drizzle":
                keyflow(f"🌧️ It's drizzling in {city}. The temperature is {temp}°F. You might need an umbrella. ☂️")
            elif weather_main.lower() == "snow":
                keyflow(f"🌨️🌨️ It's snowing in {city}! The temperature is {temp}°F. Enjoy the snow! ⛄⛄")
            elif weather_main.lower() == "mist":
                keyflow(f"🌫️🌫️ There's mist in {city}. The temperature is {temp}°F. Drive safely! 🌫️🌫️")
            elif weather_main.lower() == "smoke":
                keyflow(f"🚫 There's smoke in {city}. The temperature is {temp}°F. Be cautious of fire hazards. 🚫")
            elif weather_main.lower() == "haze":
                keyflow(f"😶‍🌫️ {city} is experiencing haze. The temperature is {temp}°F. Air quality may be affected. 😶‍🌫️")
            elif weather_main.lower() == "dust":
                keyflow(f"💨💨 Dusty conditions in {city}. The temperature is {temp}°F. Stay indoors if possible. 💨💨")
            elif weather_main.lower() == "fog":
                keyflow(f"🌁 Watch out for fog in {city}. The temperature is {temp}°F. Drive with caution. 🌫️🌫️")
            elif weather_main.lower() == "sand":
                keyflow(f"🟨🟨 There's sand in the air in {city}. The temperature is {temp}°F. Protect your eyes! 🟨🟨")
            elif weather_main.lower() == "tornado":
                keyflow(f"🌪️🌪️ A tornado warning in {city}! Seek shelter immediately. The temperature is {temp}°F. 🌪️🌪️")
            elif weather_main.lower() == "ash":
                keyflow(f"☁☁ Ash is falling in {city}. The temperature is {temp}°F. Protect yourself from ash inhalation. ☁☁")
            elif weather_main.lower() == "squall":
                keyflow(f"A squall is expected in {city}. The temperature is {temp}°F. Secure loose items!")
            elif weather_main.lower() == "clouds":
                keyflow(f"☁️☁️ It's cloudy in {city}. The temperature is {temp}°F. Hope for some sunshine soon! ☁️☁️")
            else:
                keyflow(f"The weather in {city} is {weather_main}. The temperature is {temp}°F.")
            return
        else:
            keyflow(f"Sorry, I'm unable to get weather info for {city}. Please try again.\n")
            city = input("Enter a different city: ")

# Load the tasks of user from tasks.csv if exists
def load_tasks_from_csv(name):
    tasks = []
    try:
        with open('tasks.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['User'] == name:
                    tasks.append(row)
    except FileNotFoundError:
        pass
    return tasks

# Save the user tasks to tasks.csv
def save_tasks_to_csv(tasks):
    file_exists = os.path.isfile('tasks.csv')
    with open('tasks.csv', 'a', newline='') as file: 
        fieldnames = ['Task', 'Progress', 'User']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerows(tasks)

# All the task manager working
def task_manager(name):
    today = date.today()
    print("\n--------------------")
    print("Productivity Manager")
    print("--------------------")
    while True:
        print(f"{name}! These are some ways I can assist you with.\n")
        print("1. Task manager\n2. Goal setting\n3. Exit\n")
        choice = input("Enter your choice: ")
        if choice == "1":
            tasks = load_tasks_from_csv(name)
            newTasks = []
            while True:
                print("\nMENU\n1. Add task\n2. Delete task\n3. Display\n4. Exit\n")
                todoChoice = input("Enter your choice: ")
                if todoChoice == "1":
                    task = input("Task: ")
                    progress = today.strftime("%B %d, %Y")  # Default progress
                    newTasks.append({'Task': task, 'Progress': progress, 'User': name})
                    print("Task added successfully.\n")
                elif todoChoice == "2":
                    if len(tasks) == 0:
                        print("No tasks to delete.\n")
                    else:
                        print("DELETE TASK\n")
                        headers = ["S.no", "Task", "Progress"]
                        all_tasks = tasks + newTasks
                        table = [(i, task['Task'], task['Progress']) for i, task in enumerate(all_tasks, start=1)]
                        print(tabulate(table, headers, tablefmt="grid"))
                        choice = int(input("\nChoose the task number to delete: "))
                        if choice in range(1, len(all_tasks) + 1):
                            del all_tasks[choice - 1]
                            print("Task deleted successfully.\n")
                        else:
                            print("Invalid task number.")
                elif todoChoice == "3":
                    # print(newTasks)
                    if len(tasks)==0 and len(newTasks) == 0:
                        print("No tasks to display.\n")
                    else:
                        all_tasks = newTasks + tasks
                        headers = ["S.no", "Task", "Date"]
                        table = [(i, task['Task'], task['Progress']) for i, task in enumerate(all_tasks, start=1)]
                        print("\n")
                        print(tabulate(table, headers, tablefmt="pretty"))
                        print("\n")
                elif todoChoice == "4":
                    save_tasks_to_csv(newTasks)
                    print(f"Goodbye, {name}. Have a great day!\n")
                    break
                else:
                    print("Invalid Choice")
        elif choice == "3":
            print(f"Goodbye, {name}. Have a great day!\n")
            break
        else:
            print("Invalid choice")    
              
if __name__ == "__main__":
    main()