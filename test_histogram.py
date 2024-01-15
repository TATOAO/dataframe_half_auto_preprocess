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


