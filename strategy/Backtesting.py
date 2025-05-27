class Backtester:
    def __init__(self, data, algorithms):
        self.data = data
        self.algorithms = algorithms
        # self.stock = stock

    def run(self):
        results = {}
        for algo in self.algorithms:
            try:
                data_copy = self.data.copy()
                data_with_signals = algo.apply_strategy(data_copy)
                performance = algo.evaluate(data_with_signals)
                results[algo.name] = performance
            except Exception as e:
                results[algo.name] = None
        return results