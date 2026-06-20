import tkinter as tk

# ---------------- WINDOW ----------------
root = tk.Tk()
root.title("Secure Password Analyzer")
root.geometry("600x600")

# ---------------- INPUT FIELDS ----------------
tk.Label(root, text="Full Name").pack()
name_entry = tk.Entry(root)
name_entry.pack()

tk.Label(root, text="Username").pack()
username_entry = tk.Entry(root)
username_entry.pack()

tk.Label(root, text="Email").pack()
email_entry = tk.Entry(root)
email_entry.pack()

tk.Label(root, text="DOB (DDMMYYYY)").pack()
dob_entry = tk.Entry(root)
dob_entry.pack()

tk.Label(root, text="Password").pack()
password_entry = tk.Entry(root, show="*")
password_entry.pack()

# ---------------- OUTPUT BOX ----------------
output = tk.Text(root, height=25, width=70)
output.pack()

# ---------------- CHECK PASSWORD ----------------
def check_password():
    password = password_entry.get()
    name = name_entry.get().lower()
    username = username_entry.get().lower()
    email = email_entry.get().lower()
    dob = dob_entry.get()

    score = 0
    output.delete("1.0", tk.END)

    output.insert(tk.END, "🔐 PASSWORD SECURITY REPORT\n")
    output.insert(tk.END, "================================\n")

    # ---------------- BASIC CHECKS ----------------
    if len(password) >= 8:
        score += 1
        output.insert(tk.END, "✔ Length OK\n")
    else:
        output.insert(tk.END, "✘ Too short (min 8)\n")

    if any(c.isupper() for c in password):
        score += 1
        output.insert(tk.END, "✔ Uppercase found\n")
    else:
        output.insert(tk.END, "✘ Missing uppercase\n")

    if any(c.islower() for c in password):
        score += 1
        output.insert(tk.END, "✔ Lowercase found\n")
    else:
        output.insert(tk.END, "✘ Missing lowercase\n")

    if any(c.isdigit() for c in password):
        score += 1
        output.insert(tk.END, "✔ Digit found\n")
    else:
        output.insert(tk.END, "✘ Missing digit\n")

    special = "!@#$%^&*()-_=+[]{}|\\:;\"'<>,.?/"
    if any(c in special for c in password):
        score += 1
        output.insert(tk.END, "✔ Special character found\n")
    else:
        output.insert(tk.END, "✘ Missing special character\n")

    # ---------------- COMMON PASSWORD CHECK ----------------
    output.insert(tk.END, "\n--- Common Password Check ---\n")

    try:
        with open("common_passwords.txt", "r") as file:
            common_passwords = set(file.read().splitlines())

        if password.lower() in common_passwords:
            output.insert(tk.END, "✘ This is a COMMON password\n")
            score -= 2
        else:
            output.insert(tk.END, "✔ Not in common password list\n")

    except FileNotFoundError:
        output.insert(tk.END, "⚠ common_passwords.txt not found\n")

    # ---------------- PERSONAL INFO CHECK ----------------
    output.insert(tk.END, "\n--- Personal Info Check ---\n")

    email_prefix = email.split("@")[0] if "@" in email else email

    found_issue = False
    name_found = False

    if username and username in password.lower():
        output.insert(tk.END, "✘ Contains username\n")
        found_issue = True
    else:
        output.insert(tk.END, "✔ Username NOT found\n")

    for part in name.split():
        if part and part in password.lower():
            output.insert(tk.END, f"✘ Contains name part: {part}\n")
            found_issue = True
            name_found = True

    if not name_found:
        output.insert(tk.END, "✔ Name NOT found\n")

    if email_prefix and email_prefix in password.lower():
        output.insert(tk.END, "✘ Contains email prefix\n")
        found_issue = True
    else:
        output.insert(tk.END, "✔ Email prefix NOT found\n")

    if dob and dob in password:
        output.insert(tk.END, "✘ Contains DOB\n")
        found_issue = True
    else:
        output.insert(tk.END, "✔ DOB NOT found\n")

    output.insert(tk.END, "================================\n")

    if found_issue:
        score -= 2
        output.insert(tk.END, "⚠ Personal Info Risk Detected\n")
    else:
        output.insert(tk.END, "✔ No Personal Info Found (Safe)\n")

    # ---------------- FINAL SCORE ----------------
    output.insert(tk.END, "\n================================\n")
    output.insert(tk.END, f"Score: {score}/5\n")

    if score <= 2:
        output.insert(tk.END, "Strength: WEAK\n")
    elif score <= 4:
        output.insert(tk.END, "Strength: MEDIUM\n")
    else:
        output.insert(tk.END, "Strength: STRONG\n")

# ---------------- RESET FUNCTION ----------------
def reset():
    password_entry.delete(0, tk.END)
    output.delete("1.0", tk.END)
    password_entry.focus()

# ---------------- BUTTONS ----------------
tk.Button(root, text="Check Password", command=check_password).pack(pady=5)
tk.Button(root, text="Check Again", command=reset).pack(pady=5)
tk.Button(root, text="Quit", command=root.quit).pack(pady=5)

# ---------------- RUN ----------------
root.mainloop()