import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import serial
import time
import re
import csv

# Initialize session state for messages
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Initialize serial connection
def init_serial():
    try:
        ser = serial.Serial("COM8", 115200, timeout=1)
        if not ser.is_open:
            st.session_state.messages.append("COM8 ACCESS DENIED")
            ser = serial.Serial("COM7", 115200, timeout=1)
            if not ser.is_open:
                st.session_state.messages.append("COM7 ACCESS DENIED")
                return None
        return ser
    except serial.SerialException as e:
        st.session_state.messages.append(f"Serial error: {e}")
        return None

ser = init_serial()

# Initialize data
x = np.arange(256)
y = np.zeros(256)

# Create a figure and axis
fig, ax = plt.subplots()
line, = ax.plot(x, y, lw=2)

def init():
    ax.set_title('Live CSI Animation')
    ax.set_xlabel('X')
    ax.set_ylabel('CSI')
    ax.set_xlim(0, 256)  # Adjust if needed
    ax.set_ylim(-100, 300)  # Adjust based on expected data range
    line.set_data(x, np.zeros_like(x))
    return line,

def update(frame):
    line.set_ydata(frame)
    return line,

def data_gen():
    while True:
        if ser and ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            print(line)
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            if re.match(r'^-?\d+(\s-?\d+)*$', line):
                data = [int(i) for i in line.split(' ')]
                with open("CSI.csv", "a", newline='') as csvfile:
                    csvwriter = csv.writer(csvfile)
                    csvwriter.writerow([timestamp] + data)
                st.session_state.messages.append(f"{timestamp}: {data}")
                yield np.array(data)

# Streamlit app
st.title("Live CSI Data Animation")

# Create a placeholder for the plot
plot_placeholder = st.empty()

# Function to update the plot
def animate():
    ani = animation.FuncAnimation(fig, update, frames=data_gen, init_func=init, blit=True, interval=40, cache_frame_data=False)
    plot_placeholder.pyplot(fig)

# Display messages
st.subheader("Message Console")
message_console = st.empty()

# Run the animation
animate()

# Update message console
for i in range(1000):  # Adjust the range as needed
    message_console.text_area("Serial Monitor", value="\n".join(st.session_state.messages), height=200, key=f"serial_monitor_{i}")
    time.sleep(1)
