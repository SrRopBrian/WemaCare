import bisect

class HospitalQueue:
    def __init__(self):
        self.queue = []
        self.counter = 0  # To maintain order in case of age ties

    def add(self, name, age):
        # Create a patient entry and insert it into the sorted queue
        patient = (-age, self.counter, {"name": name, "age": age})
        bisect.insort(self.queue, patient)
        self.counter += 1

    def update(self, name, new_age=None):
        # Find the patient by name, remove them, and reinsert with updated age
        for i, (_, _, patient) in enumerate(self.queue):
            if patient['name'].lower() == name.lower():
                # Remove the patient
                self.queue.pop(i)
                if new_age is not None:
                    # Re-add the patient with the updated age
                    self.add(name, new_age)
                return True
        return False

    def admit(self):
        if self.queue:
            # Remove and return the highest-priority patient
            return self.queue.pop(0)[2]
        return None

    def remove(self, name):
        for i, (_, _, patient) in enumerate(self.queue):
            if patient['name'].lower() == name.lower():
                self.queue.pop(i)
                return True
        return False

    def get_highest_priority(self):
        if self.queue:
            return self.queue[0][2]  # Return the patient with the highest priority
        return None

    def length(self):
        return len(self.queue)

    def is_empty(self):
        return len(self.queue) == 0
