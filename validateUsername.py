from tkinter import messagebox

def validateUsername(username: str, parent) -> bool:
    if not username:
        messagebox.showerror("Error", "You must provide a username to connect.", parent=parent)
        return False
    if not username.isalnum():
        messagebox.showerror("Error", "Usernames must only contain letters and numbers.", parent=parent)
        return False
    if len(username) < 3 or len(username) > 15:
        messagebox.showerror("Error", "Usernames must be between 3 and 15 characters.", parent=parent)
        return False
    if username == "System":
        messagebox.showerror("Error", "System is a reserved username. Please select another name.", parent=parent)
        return False
    return True
