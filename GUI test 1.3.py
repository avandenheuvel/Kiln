import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import random
import time

class TemperatureControllerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Temperature Controller")
        self.geometry("800x600")

        self.time_period = 20  # Default time period for graph (adjustable with slider)
        self.graph_data_limit = 2000  # Maximum number of data points

        self.time_values = []
        self.temperature_values = []
        self.output_values = []
        self.setpoint_values = []

        self.create_main_screen()
        self.create_setup_screen()
        
        # Initialize heater states (0 for OFF, 1 for ON)
        self.heater_1_state = tk.IntVar(value=0)
        self.heater_2_state = tk.IntVar(value=0)
        
        # Initialize the graph
        self.init_graph()
        
        # Simulate data update
        self.animation = None
        self.start_data_simulation()

    def create_main_screen(self):
        self.main_screen = ttk.Frame(self)
        self.main_screen.pack(fill="both", expand=True)

        # Labels and Input boxes for temperature setpoints
        self.label_setpoint_1 = ttk.Label(self.main_screen, text="Setpoint 1:")
        self.label_setpoint_1.grid(row=0, column=0, padx=10, pady=5)
        self.setpoint_1 = tk.DoubleVar()
        self.entry_setpoint_1 = ttk.Entry(self.main_screen, textvariable=self.setpoint_1)
        self.entry_setpoint_1.grid(row=0, column=1, padx=10, pady=5)

        self.label_setpoint_2 = ttk.Label(self.main_screen, text="Setpoint 2:")
        self.label_setpoint_2.grid(row=1, column=0, padx=10, pady=5)
        self.setpoint_2 = tk.DoubleVar()
        self.entry_setpoint_2 = ttk.Entry(self.main_screen, textvariable=self.setpoint_2)
        self.entry_setpoint_2.grid(row=1, column=1, padx=10, pady=5)

        # Heaters Control
        self.heater_output_1 = tk.DoubleVar()
        self.heater_output_2 = tk.DoubleVar()

        self.label_heater_output_1 = ttk.Label(self.main_screen, text="Heater Output 1:")
        self.label_heater_output_1.grid(row=2, column=0, padx=10, pady=5)
        self.label_heater_output_1_value = ttk.Label(self.main_screen, textvariable=self.heater_output_1)
        self.label_heater_output_1_value.grid(row=2, column=1, padx=10, pady=5)

        self.label_heater_output_2 = ttk.Label(self.main_screen, text="Heater Output 2:")
        self.label_heater_output_2.grid(row=3, column=0, padx=10, pady=5)
        self.label_heater_output_2_value = ttk.Label(self.main_screen, textvariable=self.heater_output_2)
        self.label_heater_output_2_value.grid(row=3, column=1, padx=10, pady=5)

        # code for the buttons with the modified code
        self.button_toggle_heater_1 = ttk.Button(self.main_screen, text="Heater 1: OFF", style="Off.TButton", command=self.toggle_heater_1)
        self.button_toggle_heater_1.grid(row=4, column=0, padx=10, pady=5)

        self.button_toggle_heater_2 = ttk.Button(self.main_screen, text="Heater 2: OFF", style="Off.TButton", command=self.toggle_heater_2)
        self.button_toggle_heater_2.grid(row=4, column=1, padx=10, pady=5)

        # Graph trend
        self.figure = plt.Figure(figsize=(6, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_xlabel("Time (seconds)")
        self.ax.set_ylabel("Temperature / Setpoint / Heater Output (%)")
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.main_screen)
        self.canvas.get_tk_widget().grid(row=6, column=0, columnspan=2, padx=10, pady=5)

        # Slider to adjust time period
        self.label_time_period = ttk.Label(self.main_screen, text="Time Period (seconds):")
        self.label_time_period.grid(row=7, column=0, padx=10, pady=5)
        self.time_period = tk.IntVar(value=20)
        self.slider_time_period = ttk.Scale(self.main_screen, from_=60, to=2000, length=200, variable=self.time_period, command=self.on_slider_change)
        self.slider_time_period.grid(row=7, column=1, padx=10, pady=5)

        # Button to switch to the setup screen
        self.button_setup_screen = ttk.Button(self.main_screen, text="Go to Setup Screen", command=self.show_setup_screen)
        self.button_setup_screen.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

    def create_setup_screen(self):
        self.setup_screen = ttk.Frame(self)
        self.setup_screen.pack(fill="both", expand=True)

        # Labels and Input boxes for PID controller parameters
        self.label_kp = ttk.Label(self.setup_screen, text="KP:")
        self.label_kp.grid(row=0, column=0, padx=10, pady=5)
        self.kp = tk.DoubleVar()
        self.entry_kp = ttk.Entry(self.setup_screen, textvariable=self.kp)
        self.entry_kp.grid(row=0, column=1, padx=10, pady=5)

        self.label_ki = ttk.Label(self.setup_screen, text="KI:")
        self.label_ki.grid(row=1, column=0, padx=10, pady=5)
        self.ki = tk.DoubleVar()
        self.entry_ki = ttk.Entry(self.setup_screen, textvariable=self.ki)
        self.entry_ki.grid(row=1, column=1, padx=10, pady=5)

        self.label_kd = ttk.Label(self.setup_screen, text="KD:")
        self.label_kd.grid(row=2, column=0, padx=10, pady=5)
        self.kd = tk.DoubleVar()
        self.entry_kd = ttk.Entry(self.setup_screen, textvariable=self.kd)
        self.entry_kd.grid(row=2, column=1, padx=10, pady=5)

        # Stepper Motors Control
        self.stepper_1_position = tk.DoubleVar()
        self.stepper_2_position = tk.DoubleVar()

        self.label_stepper_1_position = ttk.Label(self.setup_screen, text="Stepper 1 Position:")
        self.label_stepper_1_position.grid(row=3, column=0, padx=10, pady=5)
        self.label_stepper_1_position_value = ttk.Label(self.setup_screen, textvariable=self.stepper_1_position)
        self.label_stepper_1_position_value.grid(row=3, column=1, padx=10, pady=5)

        self.label_stepper_2_position = ttk.Label(self.setup_screen, text="Stepper 2 Position:")
        self.label_stepper_2_position.grid(row=4, column=0, padx=10, pady=5)
        self.label_stepper_2_position_value = ttk.Label(self.setup_screen, textvariable=self.stepper_2_position)
        self.label_stepper_2_position_value.grid(row=4, column=1, padx=10, pady=5)

        self.button_manual_enable_1 = ttk.Button(self.setup_screen, text="Manual Enable 1", command=self.manual_enable_1)
        self.button_manual_enable_1.grid(row=5, column=0, padx=10, pady=5)

        self.button_forward_1 = ttk.Button(self.setup_screen, text="Forward 1", command=self.forward_1)
        self.button_forward_1.grid(row=5, column=1, padx=10, pady=5)

        self.button_reverse_1 = ttk.Button(self.setup_screen, text="Reverse 1", command=self.reverse_1)
        self.button_reverse_1.grid(row=5, column=2, padx=10, pady=5)

        self.button_manual_enable_2 = ttk.Button(self.setup_screen, text="Manual Enable 2", command=self.manual_enable_2)
        self.button_manual_enable_2.grid(row=6, column=0, padx=10, pady=5)

        self.button_forward_2 = ttk.Button(self.setup_screen, text="Forward 2", command=self.forward_2)
        self.button_forward_2.grid(row=6, column=1, padx=10, pady=5)

        self.button_reverse_2 = ttk.Button(self.setup_screen, text="Reverse 2", command=self.reverse_2)
        self.button_reverse_2.grid(row=6, column=2, padx=10, pady=5)

        # Button to switch back to the main screen
        self.button_main_screen = ttk.Button(self.setup_screen, text="Go to Main Screen", command=self.show_main_screen)
        self.button_main_screen.grid(row=7, column=0, columnspan=3, padx=10, pady=5)

    def start_data_simulation(self):
        self.animation = self.after(1000, self.update_data_simulation)

    def update_data_simulation(self):
        # Simulate data
        current_time = time.strftime("%H:%M:%S")
        temperature = random.uniform(25, 30)
        output = random.uniform(0, 100)
        setpoint = random.uniform(25, 30)

        # Add data to arrays
        self.time_values.append(current_time)
        self.temperature_values.append(temperature)
        self.output_values.append(output)
        self.setpoint_values.append(setpoint)

        # Trim arrays if exceeding limit
        if len(self.time_values) > self.graph_data_limit:
            self.time_values.pop(0)
            self.temperature_values.pop(0)
            self.output_values.pop(0)
            self.setpoint_values.pop(0)

        # Update graph
        self.update_graph()

        # Schedule next data update
        self.animation = self.after(1000, self.update_data_simulation)

    def init_graph(self):
        self.graph_fig = Figure(figsize=(6, 4), dpi=100)
        self.graph_ax = self.graph_fig.add_subplot(111)
        self.graph_ax.set_xlabel('Time')
        self.graph_ax.set_ylabel('Value')
        self.graph_ax.set_title('Temperature Controller Data')
        self.graph_canvas = FigureCanvasTkAgg(self.graph_fig, master=self)
        self.graph_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def update_graph(self):
        self.graph_ax.clear()

        self.graph_ax.plot(self.time_values[-self.time_period.get():], self.temperature_values[-self.time_period.get():], label='Temperature')
        self.graph_ax.plot(self.time_values[-self.time_period.get():], self.output_values[-self.time_period.get():], label='Heater Output')
        self.graph_ax.plot(self.time_values[-self.time_period.get():], self.setpoint_values[-self.time_period.get():], label='Setpoint')

        self.graph_ax.set_xlabel('Time')
        self.graph_ax.set_ylabel('Value')
        self.graph_ax.legend()

        self.graph_canvas.draw()

    def on_slider_change(self, value):
        self.time_period = int(value)
        self.update_graph()

    def manual_enable_1(self):
        # Function to manually enable Stepper 1
        pass

    def toggle_heater_1(self):
        # Function to toggle Heater 1 on/off
        self.heater_1_state = not self.heater_1_state
        if self.heater_1_state:
            self.button_toggle_heater_1.config(text="Heater 1: ON", style="On.TButton")
        else:
            self.button_toggle_heater_1.config(text="Heater 1: OFF", style="Off.TButton")

    def toggle_heater_2(self):
        # Function to toggle Heater 2 on/off
        self.heater_2_state = not self.heater_2_state
        if self.heater_2_state:
            self.button_toggle_heater_2.config(text="Heater 2: ON", style="On.TButton")
        else:
            self.button_toggle_heater_2.config(text="Heater 2: OFF", style="Off.TButton")

    def forward_1(self):
        # Function to move Stepper 1 forward
        pass

    def reverse_1(self):
        # Function to move Stepper 1 in reverse
        pass

    def manual_enable_2(self):
        # Function to manually enable Stepper 2
        pass

    def forward_2(self):
        # Function to move Stepper 2 forward
        pass

    def reverse_2(self):
        # Function to move Stepper 2 in reverse
        pass

    def show_main_screen(self):
        self.setup_screen.pack_forget()
        self.main_screen.pack(fill="both", expand=True)
        self.current_screen = "main"

    def show_setup_screen(self):
        self.main_screen.pack_forget()
        self.setup_screen.pack(fill="both", expand=True)
        self.current_screen = "setup"

if __name__ == "__main__":
    app = TemperatureControllerApp()

    # Custom styles for buttons (On.TButton for ON state, Off.TButton for OFF state)
    app.style = ttk.Style()
    app.style.configure("On.TButton", foreground="white", background="green")
    app.style.configure("Off.TButton", foreground="white", background="red")

    app.mainloop()
