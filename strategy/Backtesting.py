class Backtester:
    def __init__(self, algorithms):
        self.algorithms = algorithms

    def run(self):
        results = {}
        for algo in self.algorithms:
            try:
                data_with_signals = algo.apply_strategy()
                performance = algo.evaluate(data_with_signals)
                results[algo.name] = performance
            except Exception as e:
                print(f"Error in {algo.name}: {str(e)}")
                results[algo.name] = None
        return results