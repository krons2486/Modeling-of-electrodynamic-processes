import matplotlib.pyplot as plt

class Plotter:
    def plot_rcs_vs_frequency(self, data):
        frequencies = [entry['freq'] for entry in data]
        rcs_values = [entry['rcs'] for entry in data]

        plt.figure(figsize=(10, 6))
        plt.plot(frequencies, rcs_values, color='b', linestyle='-')
        plt.xlabel('Частота (Гц)')
        plt.ylabel('ЭПР (м^2)')
        plt.title('ЭПР vs. Частота')
        #plt.xscale('log')
        plt.grid(True)
        plt.show()
