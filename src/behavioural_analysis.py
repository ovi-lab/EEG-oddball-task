import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Data for all participants
data = {
    'P1': {
        'sessions': ['Session 1', 'Session 2', 'Session 3'],
        'actual': [[4, 11, 17], [14, 13, 9], [10, 11, 9]],
        'perceived': [[4, 11, 17], [14, 13, 9], [10, 11, 9]],
    },
    'P2': {
        'sessions': ['Session 1', 'Session 2', 'Session 3'],
        'actual': [[12, 7, 16], [14, 6, 14], [12, 10, 8]],
        'perceived': [[12, 7, 16], [13, 6, 14], [12, 10, 8]],
    },
    'P3': {
        'sessions': ['Session 1', 'Session 2', 'Session 3'],
        'actual': [[15, 8, 6], [12, 11, 16], [10, 17, 16]],
        'perceived': [[15, 8, 6], [12, 11, 16], [10, 17, 16]],
    },
    'P4': {
        'sessions': ['Session 1', 'Session 2', 'Session 3'],
        'actual': [[6, 7, 12], [8, 7, 9], [9, 10, 13]],
        'perceived': [[6, 7, 12], [8, 7, 9], [9, 10, 13]],
    },
    'P5': {
        'sessions': ['Session 1', 'Session 2', 'Session 3'],
        'actual': [[8, 10, 8], [11, 13, 12], [8, 10, 18]],
        'perceived': [[7, 10, 8], [11, 13, 12], [8, 10, 17]],
    },
    'P6': {
        'sessions': ['Session 1', 'Session 2', 'Session 3'],
        'actual': [[12, 14, 14], [13, 13, 11], [12, 8, 14]],
        'perceived': [[12, 14, 14], [13, 13, 11], [12, 7, 14]],
    },
    'P7': {
        'sessions': ['Session 1', 'Session 2', 'Session 3'],
        'actual': [[13, 11, 10], [16, 11, 8], [12, 11, 9]],
        'perceived': [[13, 11, 10], [16, 11, 8], [12, 11, 9]],
    },
    'P8': {
        'sessions': ['Session 1', 'Session 2', 'Session 3'],
        'actual': [[9, 10, 12], [13, 13, 7], [10, 11, 11]],
        'perceived': [[9, 10, 12], [13, 13, 7], [10, 11, 11]],
    },
    'P9': {
        'sessions': ['Session 1', 'Session 2', 'Session 3'],
        'actual': [[13, 11, 11], [6, 12, 6], [11, 10, 9]],
        'perceived': [[13, 11, 11], [6, 12, 6], [11, 10, 9]],
    }
}

# Function to calculate accuracy
def calculate_accuracy(actual, perceived):
    return np.mean(np.array(actual) == np.array(perceived)) * 100

# Prepare data for plotting
participants = []
accuracies = []

for participant, details in data.items():
    all_actuals = [item for sublist in details['actual'] for item in sublist]
    all_perceived = [item for sublist in details['perceived'] for item in sublist]
    accuracy = calculate_accuracy(all_actuals, all_perceived)
    participants.append(participant)
    accuracies.append(accuracy)

# Create a DataFrame
df = pd.DataFrame({
    'Participant': participants,
    'Accuracy': accuracies
})

# Plotting
plt.figure(figsize=(12, 6))
bar_width = 0.35
x = np.arange(len(df['Participant']))

plt.bar(x, df['Accuracy'], bar_width, color='b', label='Accuracy')

plt.xlabel('Participants')
plt.ylabel('Accuracy (%)')
plt.title('Combined Accuracy of Actual vs. Perceived Counts')
plt.xticks(x, df['Participant'])
plt.legend(title='Metric')
plt.grid(axis='y')
plt.ylim(0, 110)
plt.show()
