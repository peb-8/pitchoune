class Aggregation:

    def __init__(self, op: str, on: str):
        self.op = op
        self.on = on

    def process(self, values):
        if self.op == "count":
            return len(values)
        if self.op == "unique_count":
            return len(set(values))
        if self.op == "sum":
            return sum(values)
        if self.op == "mean":
            return sum(float(value) for value in values) / len(values)
        if self.op == "collect_set":
            return list(set(values))
        if self.op == "collect":
            return values

    def __str__(self):
        return f"{self.op} on {self.on}"

    def __repr__(self):
        return f"Aggregation operation '{self.op}' on '{self.on}'"
