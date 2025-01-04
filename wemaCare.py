import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
from hospitalQ import HospitalQueue

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class WemaCare(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("850x600")
        self.title("Wema Care")
        self.resizable(False, False)

        self.patient_queue = HospitalQueue()

        self.setup_ui()

    def setup_ui(self):
        # App Title & Icon
        ctk.CTkLabel(self, text="WemaCare Reception", font=("Arial", 20)).pack(pady=10)

        self.hospital_icon = ctk.CTkImage(light_image=Image.open('resources/medicine.png'),
                                          dark_image=Image.open('resources/medicine.png'), size=(30, 30))
        ctk.CTkLabel(self, image=self.hospital_icon, text="").place(relx=0.5, rely=0.1, anchor="center")

        # Add Patient Section
        ctk.CTkLabel(self, text="Add Patient to Queue").place(x=85, y=80)
        self.name_entry = ctk.CTkEntry(self, placeholder_text="Name")
        self.name_entry.place(x=80, y=110)
        self.age_entry = ctk.CTkEntry(self, placeholder_text="Age")
        self.age_entry.place(x=80, y=150)
        ctk.CTkButton(self, text="Add Patient", command=self.add_patient).place(x=80, y=190)

        # Admit Oldest Patient
        ctk.CTkButton(self, text="Admit Next Patient", command=self.admit_oldest).place(x=80, y=230)

        # Update Patient Section
        ctk.CTkLabel(self, text="Update Patient Details").place(x=350, y=80)
        self.update_name_entry = ctk.CTkEntry(self, placeholder_text="Name to Update")
        self.update_name_entry.place(x=350, y=110)
        self.new_age_entry = ctk.CTkEntry(self, placeholder_text="New Age")
        self.new_age_entry.place(x=350, y=150)
        ctk.CTkButton(self, text="Update Patient", command=self.update_patient).place(x=350, y=190)

        # Is Queue Empty
        ctk.CTkButton(self, text="Is Queue Empty?", command=self.check_is_empty).place(x=350, y=230)

        # Remove Patient by Name
        ctk.CTkLabel(self, text="Remove Patient by Name").place(x=600, y=80)
        self.index_entry = ctk.CTkEntry(self, placeholder_text="Name")
        self.index_entry.place(x=600, y=110)
        ctk.CTkButton(self, text="Remove Patient", command=self.remove_patient).place(x=600, y=150)

        # Get Highest Priority Patient
        ctk.CTkButton(self, text="View Oldest Patient", command=self.get_highest_priority).place(x=600, y=190)

        # Queue length
        ctk.CTkButton(self, text="Queue Length", command=self.get_length).place(x=600, y=230)

        # Display Queue Section
        ctk.CTkLabel(self, text="Patient Queue").place(x=80, y=300)
        self.queue_frame = ctk.CTkFrame(self, width=500, height=200, corner_radius=10)
        self.queue_frame.place(x=80, y=330)

    # Queue managemement functions
    def add_patient(self):
        name = self.name_entry.get()
        age = self.age_entry.get()

        if not name or not age.isdigit():
            messagebox.showerror("Error", "Please enter a valid name and age.")
            return

        self.patient_queue.add(name, int(age))
        messagebox.showinfo("Success", f"Patient {name} added successfully.")
        self.update_visual_queue()
        self.clear_entries()

    def admit_oldest(self):
        patient = self.patient_queue.admit()
        if patient:
            messagebox.showinfo("Admitted Patient", f"Admitted: {patient['name']}, Age: {patient['age']}")
            self.update_visual_queue()
        else:
            messagebox.showinfo("Queue Empty", "No patients in the queue.")

    def remove_patient(self):
        name = self.index_entry.get()

        if not name:
            messagebox.showerror("Error", "Please enter the name of the patient to remove.")
            return

        success = self.patient_queue.remove(name)
        if success:
            messagebox.showinfo("Success", f"Removed patient '{name}'.")
            self.clear_entries()
            self.update_visual_queue()
        else:
            messagebox.showerror("Error", f"Patient '{name}' not found.")

    def get_length(self):
        length = self.patient_queue.length()
        messagebox.showinfo("Queue Length", f"The queue has {length} patient(s).")

    def get_highest_priority(self):
        patient = self.patient_queue.get_highest_priority()
        if patient:
            messagebox.showinfo("Highest Priority", f"{patient['name']}, Age: {patient['age']}")
        else:
            messagebox.showinfo("Queue Empty", "No patients in the queue.")

    def check_is_empty(self):
        if self.patient_queue.is_empty():
            messagebox.showinfo("Queue Status", "The queue is empty.")
        else:
            messagebox.showinfo("Queue Status", "The queue is not empty.")

    def update_patient(self):
        name = self.update_name_entry.get()
        new_age = self.new_age_entry.get()

        if not name:
            messagebox.showerror("Error", "Please enter the name of the patient to update.")
            return

        new_age = int(new_age) if new_age.isdigit() else None
        success = self.patient_queue.update(name, new_age)

        if success:
            messagebox.showinfo("Success", f"Patient '{name}' updated successfully.")
            self.update_name_entry.delete(0, "end")
            self.new_age_entry.delete(0, "end")
            self.update_visual_queue()
        else:
            messagebox.showerror("Error", f"Patient '{name}' not found.")
            self.clear_entries()

    # Visual Queue 
    def update_visual_queue(self):
        # Clear the current visual queue
        for widget in self.queue_frame.winfo_children():
            widget.destroy()

        # Display each patient in the queue according to the order in the PQ
        for _, _, patient in self.patient_queue.queue:
            frame = ctk.CTkFrame(self.queue_frame, height=50, width=380, corner_radius=10)
            frame.pack(pady=5, padx=10, fill="x")

            # Patient Image
            patient_image = ctk.CTkImage(light_image=Image.open('resources/patient.png'),
                                     dark_image=Image.open('resources/patient.png'), size=(30, 30))
            ctk.CTkLabel(frame, image=patient_image, text="").pack(side="left", padx=10)

            # Patient Details
            ctk.CTkLabel(frame, text=f"{patient['name']} (Age: {patient['age']})").pack(side="left", padx=10)

    def clear_entries(self):
        self.name_entry.delete(0, "end")
        self.age_entry.delete(0, "end")
        self.index_entry.delete(0, "end")

if __name__ == "__main__":
    app = WemaCare()
    app.mainloop()
