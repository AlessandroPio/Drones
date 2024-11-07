class Prolog:

    def json_to_prolog(self, data):
        prolog_facts = []
        for key, value in data.items():
            if isinstance(value, dict):
                fact = f"{key}("
                fact += ", ".join([f"{k}({self.json_to_prolog_value(v)})" for k, v in value.items()])
                fact += ")."
                prolog_facts.append(fact)
            else:
                prolog_facts.append(f"{key}({self.json_to_prolog_value(value)}).")
        return "\n".join(prolog_facts)

    def json_to_prolog_value(self, value):
        if isinstance(value, str):
            return f'"{value}"'
        elif isinstance(value, list):
            return "[" + ", ".join([self.json_to_prolog_value(v) for v in value]) + "]"
        else:
            return str(value)

