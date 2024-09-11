import argparse
import os
import matplotlib.pyplot as plt
import numpy as np

# Colors used in the plots
BLACK = 'k'
GREEN = '#2ca02c'
BLUE = '#1f77b4'
RED = '#d62728'
ORANGE = '#ff7f0e'
PURPLE = '#9467bd'
TURQUOIS = '#17becf'

# Function to compute average rewards
def compute_avg_reward(reward):
    avg_reward = np.zeros_like(reward)
    for i in range(len(reward)):
        avg_reward[i] = np.sum(reward[:(i + 1)]) / (i + 1)
    return avg_reward

# Function to get data, settings, and figure information based on figure_num
def get_results(figure_num, results_dir):
    # Default plot settings
    x_ticks = [0, 2000, 4000, 6000, 8000, 10000]
    x_tick_vals = x_ticks
    y_ticks = None
    marker = None
    x_label = "Steps"
    y_label = "Average rewards"

    # Figure 4
    if figure_num == 4:
        results = []
        legend = []
        fig_dir = f"{results_dir}/sum_rate_power"
        values = [8, 32]
        for val in values:
            results.append(np.load(f"{fig_dir}/{val}.npy").squeeze())
            legend.append(f"M = {val}, N = {val}, K = {val}")
        legend_loc = 'upper left'
        colors = [RED, BLUE]
        x_ticks = np.arange(-20, 35, 5)
        y_ticks = np.arange(0, 40, 5)
        marker = ['o', '<']
        x_label = "$P_{t}$ (dB)"
        y_label = "Sum rate (bps/Hz)"

    # Figure 5
    elif figure_num == 5:
        legend = []
        fig_dir = f"{results_dir}/sum_rate_ris"
        results = [np.load(f"{fig_dir}/result.npy")]
        legend.append("Proposed DRL Method")
        legend_loc = 'upper left'
        colors = [RED]
        x_ticks = np.arange(10, 210, 10)
        y_ticks = np.arange(12, 34, 2)
        x_label = "Number of elements in RIS"
        y_label = "Sum rate (bps/Hz)"

    # Add other figure settings (6, 7, etc.) here as needed...

    # Return the plot settings and data
    save_name = f"{figure_num}_reproduced.jpg"
    return results, legend, legend_loc, colors, x_ticks, x_tick_vals, y_ticks, marker, x_label, y_label, save_name

# Main function to parse arguments and plot the figure
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--figure_num', default=5, type=int, choices=[4, 5, 6, 7, 8, 9, 10, 11, 12],
                        help='Choose one of the figures to reproduce')
    args = parser.parse_args()

    results_dir = "./Learning Curves"
    fig_dir = f"./Learning Figures"

    if not os.path.exists(fig_dir):
        os.makedirs(fig_dir)

    results, legend, legend_loc, colors, x_ticks, x_tick_vals, y_ticks, marker, x_label, y_label, save_name = get_results(args.figure_num, results_dir)

    # Plot settings
    plt.rcParams['figure.figsize'] = [12, 10]
    linewidth = 3
    legend_size = 30
    font_size = 15 if args.figure_num == 5 else 25
    legend_font_size = 15 if args.figure_num in [6, 7, 10, 11] else 25

    # Plot data
    if marker is None:
        for res, color in zip(results, colors):
            plt.plot(x_ticks, res, linewidth=linewidth, color=color)
    else:
        for res, color in zip(results, colors):
            plt.plot(x_ticks, res, color=color, marker=marker, linewidth=linewidth)

    # Set x and y ticks
    plt.xticks(x_ticks, fontsize=font_size)

    if y_ticks is not None:
        plt.yticks(y_ticks, fontsize=font_size)

    # Set labels and title
    plt.xlabel(x_label, fontsize=font_size)
    plt.ylabel(y_label, fontsize=font_size)

    # Add legend
    plt.legend(legend, loc=legend_loc, fontsize=legend_font_size, ncol=1)

    # Enable grid and save/show
        # Enable grid
    plt.grid(True)

    # Save the figure
    plt.savefig(f"{fig_dir}/{save_name}", bbox_inches='tight')

    # Show the plot
    plt.show()