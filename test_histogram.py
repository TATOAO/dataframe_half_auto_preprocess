import plotext as plt
import time

for i in range(10):
    pizzas = ["Sausage", "Pepperoni", "Mushrooms", "Cheese", "Chicken", "Beef"]
    percentages = [14, 36*i, 11, 8, 7, i]
    plt.simple_bar(pizzas, percentages, width = 100, title = 'Most Favored Pizzas in the World')
    plt.show()
    time.sleep(0.1)
    if i < 9:
        plt.clear_terminal()


# import time
#
# def print_progress_bar(iteration, total, prefix='', suffix='', length=30, fill='█', print_end='\r'):
#     percent = ("{0:.1f}").format(100 * (iteration / float(total)))
#     filled_length = int(length * iteration // total)
#     bar = fill * filled_length + '-' * (length - filled_length)
#     print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=print_end, flush=True)
#
# # Example usage
# total_iterations = 100
# for i in range(1, total_iterations + 1):
#     time.sleep(0.1)  # Simulating some task that takes time
#     print_progress_bar(i, total_iterations, prefix='Progress:', suffix='Complete', length=50)
#
# print("\nTask completed!")
#
