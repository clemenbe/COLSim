import tkinter as tk

class RuleApplicationWindow:

    def __init__(self, rules):
        self.window = tk.Tk()
        self.window.geometry("500x500") # Specify the size of the window
        self.rules = rules
        self.labels = []

        # Create a label for each rule and store it in self.labels
        for rule in rules:
            label = tk.Label(self.window, text=rule, fg="black", bg="white", font=("Helvetica", 15))
            label.pack(fill='both', padx=5, pady=5)
            self.labels.append(label)

    def apply_rule(self, rule, color):
        # Change the color of the rule's label to green when it's applied
        for i in range(len(self.rules)):
            if self.rules[i] == rule:
                self.labels[i]['bg'] = color

    # def unapply_rule(self, rule):
    #     # Change the color of the rule's label to white when it's not applied
    #     for i in range(len(self.rules)):
    #         if self.rules[i] == rule:
    #             self.labels[i]['bg'] = "white"

    def reset_rules(self):
        for label in self.labels:
            label['bg'] = 'white'

    def run(self):
        self.window.mainloop()

