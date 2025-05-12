class MemoryManager:
    def __init__(self):
        self.variables = {}  # Dictionary to store variables
        self.deleted_vars = set()  # Set to track deleted variables

    def allocate(self, name, value):
        """Allocate a new variable or update an existing one."""
        if name in self.deleted_vars:
            raise ValueError(f"Variable '{name}' has been deleted and cannot be reused.")
        self.variables[name] = value

    def deallocate(self, name):
        """Deallocate a variable and mark it as deleted."""
        if name in self.variables:
            del self.variables[name]
            self.deleted_vars.add(name)
        else:
            raise KeyError(f"Variable '{name}' is not defined and cannot be deallocated.")

    def get(self, name):
        """Retrieve the value of a variable."""
        if name in self.deleted_vars:
            raise ValueError(f"Variable '{name}' has been deleted.")
        if name not in self.variables:
            raise KeyError(f"Undefined variable: '{name}'")
        return self.variables[name]

    def update(self, name, value):
        """Update the value of an existing variable."""
        if name in self.deleted_vars:
            raise ValueError(f"Variable '{name}' has been deleted and cannot be updated.")
        if name not in self.variables:
            raise KeyError(f"Undefined variable: '{name}'")
        self.variables[name] = value

    def cleanup(self):
        """Clear all variables and reset the deleted variables tracker."""
        self.variables.clear()
        self.deleted_vars.clear()

    def exists(self, name):
        """Check if a variable exists and is not deleted."""
        return name in self.variables and name not in self.deleted_vars