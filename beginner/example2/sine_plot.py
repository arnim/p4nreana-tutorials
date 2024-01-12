import numpy as np
import matplotlib.pyplot as plt

# Generate x values from 0 to 2*pi with 100 points
x_values = np.linspace(0, 2 * np.pi, 100)

# Generate y values using the sine function
y_values = np.sin(x_values)

# Create a plot for the sine function
plt.plot(x_values, y_values, label='sin(x)')

# Add labels and title
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Sine Plot')

# Add a legend
plt.legend()

# Save the plot as a PNG file
plt.savefig('sine_plot.png')

