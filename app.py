#app.py
import requests
from time import sleep
from tabulate import tabulate
import csv
def main():
  name, city = Intro()
  keyflow(f"{name}...")
  # fetch_weather(city)
  task_manager(name)

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
    with open('personal_info.csv', "w", newline="") as file:
        fieldnames = ['name', 'city']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(personal_info)  # Write a single row with the personal_info dictionary


# Introduction Chat
def Intro():
    personal_info = load_info_from_csv()
    if len(personal_info) == 0:
        Title = "Hello user! I am Robin, your personal productivity manager.\nBy the way let me know a bit about u so i can give u personalised experience!!\n"
        keyflow(Title)
        keyflow("Your name :")
        name = input()
        keyflow("The city that u currently live in? ")
        city = input()
        personal_info.append({'name': name, "city": city})
        save_info_to_csv(personal_info)
    else:
        name = personal_info[0]['name']  # Retrieve name from personal_info dictionary
        city = personal_info[0]['city']  # Retrieve city from personal_info dictionary
        keyflow(f"Welcome Back {name}\n")
    return name, city

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

def load_tasks_from_csv():
    tasks = []
    try:
        with open('tasks.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                tasks.append(row)
    except FileNotFoundError:
        pass
    return tasks

def save_tasks_to_csv(tasks):
    with open('tasks.csv', 'w', newline='') as file:  # Change mode to 'w' to overwrite existing file and write headers
        fieldnames = ['Task', 'Progress', 'User']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(tasks)  # Use writerows to write multiple rows at once

def task_manager(name):
    print("\n--------------------")
    print("Productivity Manager")
    print("--------------------")
    while True:
        print(f"{name}! These are some ways I can assist you with.\n")
        print("1. Task manager\n2. Goal setting\n3. Exit\n")
        choice = input("Enter your choice: ")
        if choice == "1":
            tasks = load_tasks_from_csv()
            print(tasks)
            while True:
                print("\nMENU\n1. Add task\n2. Delete task\n3. Edit task\n4. Display\n5. Exit\n")
                todoChoice = input("Enter your choice: ")
                if todoChoice == "1":
                    task = input("Task: ")
                    progress = "Not started"  # Default progress
                    tasks.append({'Task': task, 'Progress': progress, 'User': name})
                    print("Task added successfully.\n")
                elif todoChoice == "2":
                    if len(tasks) == 0:
                        print("No tasks to delete.\n")
                    else:
                        print("DELETE TASK\n")
                        headers = ["S.no", "Task", "Progress"]
                        table = [(i, task['Task'], task['Progress']) for i, task in enumerate(tasks, start=1)]
                        print(tabulate(table, headers, tablefmt="grid"))
                        choice = int(input("\nChoose the task number to delete: "))
                        if choice in range(1, len(tasks) + 1):
                            del tasks[choice - 1]
                            print("Task deleted successfully.\n")
                        else:
                            print("Invalid task number.")
                elif todoChoice == "3":
                    if len(tasks) == 0:
                        print("No tasks to edit\n")
                    else:
                        print("EDIT TASK\n")
                        headers = ["S.no", "Task", "Progress"]
                        table = [(i, task['Task'], task['Progress']) for i, task in enumerate(tasks, start=1)]
                        print(tabulate(table, headers, tablefmt="grid"))
                        choice = int(input("\nChoose the task number to edit: "))
                        if choice in range(1, len(tasks) + 1):
                            task_to_edit = tasks[choice - 1]
                            print(f"Editing task '{task_to_edit['Task']}':\n")
                            print("1. Edit task name\n2. Edit progress status\n")
                            edit_choice = input("Enter your choice: ")
                            if edit_choice == "1":
                                new_task_name = input("Enter new task name: ")
                                task_to_edit['Task'] = new_task_name
                                print("Task name edited successfully.\n")
                            elif edit_choice == "2":
                                new_progress = input("Enter new progress status: ")
                                task_to_edit['Progress'] = new_progress
                                print("Progress status edited successfully.\n")
                            else:
                                print("Invalid choice.")
                        else:
                            print("Invalid task number.")
                elif todoChoice == "4":
                    if len(tasks) == 0:
                        print("No tasks to display.\n")
                    else:
                        headers = ["S.no", "Task", "Progress"]
                        table = [(i, task['Task'], task['Progress']) for i, task in enumerate(tasks, start=1)]
                        print("\n")
                        print(tabulate(table, headers, tablefmt="grid"))
                        print("\n")
                elif todoChoice == "5":
                    save_tasks_to_csv(tasks)
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