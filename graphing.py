import pandas as pd
import matplotlib.pyplot as plt
import re  # Regular expression module

def read_and_plot_fitness_data(filename):
    # Initialize lists to store the data
    generations = []
    best_fitness = []
    average_fitness = []

    # Open the file and read line by line
    with open(filename, 'r') as file:
        for line in file:
            try:
                # Use regular expressions to find all numbers in the line
                numbers = re.findall(r'\d+\.?\d*', line)
                if len(numbers) == 3:  # We expect exactly 3 numbers per line
                    # Extract generation number, best fitness, and average fitness
                    generation = int(numbers[0])
                    best_fit = int(numbers[1])
                    avg_fit = float(numbers[2])

                    # Append the parsed data to the lists
                    generations.append(generation)
                    best_fitness.append(best_fit)
                    average_fitness.append(avg_fit)
                else:
                    raise ValueError("Unexpected number of numeric values found in line.")
            except Exception as e:
                # Print error and problematic line for debugging
                print(f"Error parsing line: {line}. Error: {e}")

    # Create a DataFrame from the lists
    data = pd.DataFrame({
        'Generation': generations,
        'Best Fitness': best_fitness,
        'Average Fitness': average_fitness
    })

    # Plotting the data
    plt.figure(figsize=(10, 5))
    plt.plot(data['Generation'], data['Best Fitness'], label='Best Fitness', marker='o')
    plt.plot(data['Generation'], data['Average Fitness'], label='Average Fitness', marker='x')
    plt.title('Fitness Trends Over Generations')
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.legend()
    plt.grid(True)
    plt.show()

# Usage example
read_and_plot_fitness_data('training.txt')
