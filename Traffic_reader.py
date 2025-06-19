#Author: W. Vihanga Visalka
#Date: 12/24/2024
#Student ID: W2120519/20232519

import csv
from datetime import datetime
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Task A: Input Validation
def validate_date_input():
    """
    Prompts the user for a date in DD MM YYYY format, validates the input for:
    - Correct data type
    - Correct range for day, month, and year
    """
    while True:
        try:
            day = int(input("Please enter the day of the survey in the format dd: "))
            if day < 1 or day > 31:
                print("Out of range - values must be in the range 1 and 31.")
                continue

            month = int(input("Please enter the month of the survey in the format MM: "))
            if month < 1 or month > 12:
                print("Out of range - values must be in the range 1 to 12.")
                continue

            year = int(input("Please enter the year of the survey in the format YYYY: "))
            if year < 2000 or year > 2024:
                print("Out of range - values must range from 2000 and 2024..")
                continue

            selected_date = f"{day:02d}{month:02d}{year}"
            file_name = f"traffic_data{selected_date}.csv"

            if file_name not in ["traffic_data16062024.csv", "traffic_data15062024.csv", "traffic_data21062024.csv"]:
                print(f"No data available for the date {day:02d}/{month:02d}/{year}. Please try another date.")
                continue

            return file_name
        except ValueError:  
            print("Integer required")

def validate_continue_input():
    """
    Prompts the user to decide whether to load another dataset:
    - Validates "Y" or "N" input
    """
    while True:
        user_input = input("Do you want to select another dataset? (Y/N or Yes or no): ").strip().upper()
        if user_input in ["Y", "N", "YES", "NO"]:
            return user_input
        else:
            print("Invalid input. Please enter Y/N or Yes/No.")

# Task B: Processed Outcomes
def process_csv_data(file_path):
    """
    Processes the CSV data for the selected date and extracts:
    - Total vehicles
    - Total trucks
    - Total electric vehicles
    - Two-wheeled vehicles, and other requested metrics
    """
    outcomes = {
        "File Name": file_path,
        "Total Vehicles": 0,
        "Total Trucks": 0,
        "Total Electric Vehicles": 0,
        "Two-Wheeled Vehicles": 0,
        "Elm North Buses": 0,
        "No Turn Vehicles": 0,
        "Vehicles Over Speed Limit": 0,
        "Elm Total": 0,
        "Hanley Total": 0,
        "Hanley Peak Traffic Hour Count": 0,
        "Hanley Peak Traffic Hour": "",
        "Total Rain Hours": 0,
        "Scooters in Elm": 0,
        "Bicycles Per Hour": {},
    }

    hourly_traffic_hanley = {}

    try:
        with open(file_path, 'r') as csv_file:
            reader = csv.DictReader(csv_file)

            for row in reader:
                outcomes["Total Vehicles"] += 1
                if row.get("VehicleType") == "Truck":
                    outcomes["Total Trucks"] += 1
                if row.get("elctricHybrid", "").strip().lower() == "true":
                    outcomes["Total Electric Vehicles"] += 1
                if row.get("VehicleType") in ["Bicycle", "Motorcycle", "Scooter"]:
                    outcomes["Two-Wheeled Vehicles"] += 1
                if row.get("JunctionName") == "Elm Avenue/Rabbit Road" and row.get(
                        "travel_Direction_out") == "N" and row.get("VehicleType") == "Buss":
                    outcomes["Elm North Buses"] += 1
                if row.get("travel_Direction_in") == row.get("travel_Direction_out"):
                    outcomes["No Turn Vehicles"] += 1
                try:
                    if int(row.get("VehicleSpeed", 0)) > int(row.get("JunctionSpeedLimit", 0)):
                        outcomes["Vehicles Over Speed Limit"] += 1
                except ValueError:
                    pass
                if row.get("JunctionName") == "Elm Avenue/Rabbit Road":
                    outcomes["Elm Total"] += 1
                    if row.get("VehicleType") == "Scooter":
                        outcomes["Scooters in Elm"] += 1
                if row.get("JunctionName") == "Hanley Highway/Westway":
                    outcomes["Hanley Total"] += 1
                    try:
                        time_string = row.get("timeOfDay", "00:00:00").strip()
                        hour = int(time_string.split(":")[0])  # Extract hour from time
                        hourly_traffic_hanley[hour] = hourly_traffic_hanley.get(hour, 0) + 1
                    except (ValueError, IndexError):
                        pass  # Skip rows with invalid or missing time data
                if row.get("Weather_Conditions") == "Rain":
                    outcomes["Total Rain Hours"] += 1
                if row.get("VehicleType") == "Bicycle":
                    hour = row.get("Time", "00:00")[:2]
                    outcomes["Bicycles Per Hour"][hour] = outcomes["Bicycles Per Hour"].get(hour, 0) + 1

            if hourly_traffic_hanley:
                max_traffic = max(hourly_traffic_hanley.values())
                peak_hour = max(hourly_traffic_hanley, key=hourly_traffic_hanley.get)
                outcomes["Hanley Peak Traffic Hour Count"] = max_traffic
                outcomes["Hanley Peak Traffic Hour"] = f"Between {peak_hour:02}:00 and {peak_hour + 1:02}:00"

    except FileNotFoundError:
        print("File not found. Please ensure the file name is correct.")

    return outcomes

def display_outcomes(outcomes):
    """
    Displays the calculated outcomes in a clear and formatted way.
    """
    print("************************************************************")
    print(f"data file selected is {outcomes['File Name']}")
    print("************************************************************")
    print(f"The total number of vehicles recorded for this date is {outcomes['Total Vehicles']}")
    print(f"The total number of trucks recorded for this date is {outcomes['Total Trucks']}")
    print(f"The total number of electric vehicles for this date is {outcomes['Total Electric Vehicles']}")
    print(f"The total number of two-wheeled vehicles for this date is {outcomes['Two-Wheeled Vehicles']}")
    print(f"The total number of Busses leaving Elm Avenue/Rabbit Road heading North is {outcomes['Elm North Buses']}")
    print(f"The total number of Vehicles through both junctions not turning left or right is {outcomes['No Turn Vehicles']}")
    print(f"The percentage of total vehicles recorded that are trucks for this date is {round((outcomes['Total Trucks'] / outcomes['Total Vehicles']) * 100) if outcomes['Total Vehicles'] else 0}%")
    
    bicycles_total = sum(outcomes["Bicycles Per Hour"].values())
    bicycles_hours = len(outcomes["Bicycles Per Hour"])
    avg_bicycles = round(bicycles_total / 24) if bicycles_total else 0
    print(f"the average number of Bikes per hour for this date is {avg_bicycles}")

    print(f"The total number of Vehicles recorded as over the speed limit for this date is {outcomes['Vehicles Over Speed Limit']}")
    print(f"The total number of vehicles recorded through Elm Avenue/Rabbit Road junction is {outcomes['Elm Total']}")
    print(f"The total number of vehicles recorded through Hanley Highway/Westway junction is {outcomes['Hanley Total']}")
    print(f"{round((outcomes['Scooters in Elm'] / outcomes['Elm Total']) * 100) if outcomes['Elm Total'] else 0}% of vehicles recorded through Elm Avenue/Rabbit Road are scooters.")
    print(f"The highest number of vehicles in an hour on Hanley Highway/Westway is {outcomes['Hanley Peak Traffic Hour Count']}")
    print(f"The most vehicles through Hanley Highway/Westway were recorded {outcomes['Hanley Peak Traffic Hour']}")
    print(f"The number of hours of rain for this date is {outcomes['Total Rain Hours']}")

# Task C: Save Results to Text File
def save_results_to_file(outcomes, file_name="results.txt"):
    """
    Saves the processed outcomes to a text file and appends if the program loops.
    """
    try:
        with open(file_name, "a") as file:
            for key, value in outcomes.items():
                file.write(f"{key}: {value}\n")
            file.write("\n")
    except Exception as e:
        print(f"Error saving results: {e}")


# Task D: Histogram Display
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class HistogramApp:
    def __init__(self, traffic_data, date):
        """
        Initializes the histogram application with the traffic data and selected date.
        """
        self.traffic_data = traffic_data
        self.date = date
        self.root = tk.Tk()
        self.root.title(f"Traffic Histogram for {self.date}")
        self.canvas = None  # Will hold the canvas for drawing

    def setup_window(self):
        """
        Sets up the Tkinter window and canvas for the histogram.
        """
        self.root.geometry("800x600")  # Set the size of the window

    def draw_histogram(self):
        """
        Draws the histogram with axes, labels, and bars.
        """
        # Data Preparation
        hours = list(range(24))
        elm_data = [self.traffic_data.get("Elm", {}).get(hour, 0) for hour in hours]
        hanley_data = [self.traffic_data.get("Hanley", {}).get(hour, 0) for hour in hours]

        # Create the figure and axis
        fig, ax = plt.subplots(figsize=(10, 5))

        # Adjust bar positions
        x = range(len(hours))
        bar_width = 0.4  # Adjusted bar width to avoid overlap
        elm_positions = [pos - bar_width / 2 for pos in x]  # Shift Elm bars to the left
        hanley_positions = [pos + bar_width / 2 for pos in x]  # Shift Hanley bars to the right

        # Plot bars
        elm_bars = ax.bar(elm_positions, elm_data, width=bar_width, label="Elm Avenue/Rabbit Road", color="green")
        hanley_bars = ax.bar(hanley_positions, hanley_data, width=bar_width, label="Hanley Highway/Westway", color="red")

        # Add labels on top of the bars with matching colors
        for bar in elm_bars:
            height = bar.get_height()
            if height > 0:
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    height + 1,
                    f"{int(height)}",
                    ha="center",
                    va="bottom",
                    fontsize=9,
                    color="green",  # Match the bar color
                )

        for bar in hanley_bars:
            height = bar.get_height()
            if height > 0:
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    height + 1,
                    f"{int(height)}",
                    ha="center",
                    va="bottom",
                    fontsize=9,
                    color="red",  # Match the bar color
                )

        # Set labels and title
        ax.set_xlabel("Hour of the Day")
        ax.set_ylabel("Number of Vehicles")
        ax.set_title(f"Traffic Volume by Hour ({self.date})")
        ax.set_xticks(x)
        ax.set_xticklabels([f"{hour:02}:00" for hour in hours], rotation=45)

        self.add_legend(ax)

        # Embed the plot in the Tkinter window
        self.canvas = FigureCanvasTkAgg(fig, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()

    def add_legend(self, ax):
        """
        Adds a legend to the histogram to indicate which bar corresponds to which junction.
        """
        ax.legend()

    def run(self):
        """
        Displays the histogram and closes the window after a short delay.
        """
        self.draw_histogram()

        # Close the window after a delay
        self.root.after(5000, self.root.destroy)  # Automatically close after 5 seconds
        self.root.update()  # Update the Tkinter window non-blocking





class MultiCSVProcessor:
    def __init__(self):
        """
        Initializes the application for processing multiple CSV files.
        """
        self.current_data = None

    def load_csv_file(self, file_path):
        """
        Loads a CSV file and processes its data.
        """
        hourly_traffic = {"Elm": {}, "Hanley": {}}
        try:
            with open(file_path, 'r') as csv_file:
                reader = csv.DictReader(csv_file)

                for row in reader:
                    time_string = row.get("timeOfDay", "00:00:00").strip()
                    try:
                        hour = datetime.strptime(time_string, "%H:%M:%S").hour
                    except ValueError:
                        continue

                    junction = "Elm" if row.get("JunctionName") == "Elm Avenue/Rabbit Road" else "Hanley"
                    hourly_traffic[junction][hour] = hourly_traffic[junction].get(hour, 0) + 1

            return hourly_traffic

        except FileNotFoundError:
            print(f"File {file_path} not found.")
            return None

    def clear_previous_data(self):
        """
        Clears data from the previous run to process a new dataset.
        """
        self.current_data = None

    def handle_user_interaction(self):
        """
        Handles user input for processing multiple files.
        """
        while True:
            # Step 1: Validate and get the file name
            file_name = validate_date_input()  # Use Task A's validation function

            # Step 2: Process the selected file
            outcomes = process_csv_data(file_name)
            if not outcomes["Total Vehicles"]:  # Check if data was processed correctly
                print("No valid data found in the selected file. Try again.")
                continue

            # Step 3: Display outcomes in the console
            display_outcomes(outcomes)

            # Step 4: Save the outcomes to a text file
            save_results_to_file(outcomes)

            # Step 5: Load the file for histogram and display it
            traffic_data = self.load_csv_file(file_name)
            if traffic_data:
                histogram_app = HistogramApp(traffic_data, file_name)
                histogram_app.run()

            # Step 6: Always ask the user if they want to continue
            while True:  # Ensure valid input for continuation
                user_choice = validate_continue_input()
                if user_choice in ["Y", "YES"]:
                    print("Starting a new dataset...")
                    print("******************************************************************************************************")
                    break  # Exit inner loop to start processing a new dataset
                elif user_choice in ["N", "NO"]:
                    print("Exiting program. Goodbye!")
                    return  # Exit the outer loop and terminate the program

    def process_files(self):
        """
        Main loop for handling multiple CSV files until the user decides to quit.
        """
        self.handle_user_interaction()


# Main Program Execution
if __name__ == "__main__":
    processor = MultiCSVProcessor()
    processor.process_files()
