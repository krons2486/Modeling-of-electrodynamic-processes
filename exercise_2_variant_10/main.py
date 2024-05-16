from dataLoader import DataLoader
from RCS import RCS
from resultWriter import ResultWriter
from plotter import Plotter
import numpy as np

def main():
    url = "https://jenyay.net/uploads/Student/Modelling/task_rcs.xml"
    variant_number = 10
    
    loader = DataLoader(url)
    D, fmin, fmax = loader.parse_xml(variant_number)

    frequencies = np.linspace(fmin, fmax, num=100)
    rcs_calculator = RCS(D / 2)
    results = []
    for freq in frequencies:
        rcs = rcs_calculator.calculate_rcs(freq)
        results.append({"freq": freq, "lambda": 3e8 / freq, "rcs": rcs})

    writer = ResultWriter("rcs_results.json")
    writer.write_to_json({"data": results})

    plotter = Plotter()
    plotter.plot_rcs_vs_frequency(results)

if __name__ == "__main__":
    main()
