import cv2
import os
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import numpy as np

# Define the save path for the encrypted image
SAVE_PATH = r"C:\Users\nanch\Downloads\Stenography-main\encryptedImage.png"
PASSWORD_FILE = "password.txt"

# Function to save the password
def save_password(password):
    with open(PASSWORD_FILE, "w") as file:
        file.write(password)

# Function to load the saved password
def load_password():
    if os.path.exists(PASSWORD_FILE):
        with open(PASSWORD_FILE, "r") as file:
            return file.read().strip()
    return ""

def encrypt():
    img_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image Files", "*.jpg *.png *.bmp")])
    if not img_path:
        messagebox.showerror("Error", "No image selected!")
        return

    img = cv2.imread(img_path)
    if img is None:
        messagebox.showerror("Error", "Could not load image. Check the file path.")
        return

    msg = simpledialog.askstring("Input", "Enter secret message:", parent=root)
    password = simpledialog.askstring("Input", "Enter a passcode:", show="*", parent=root)

    if not msg or not password:
        messagebox.showerror("Error", "Message or password cannot be empty!")
        return

    save_password(password)  

    msg_bytes = msg.encode('utf-8')  
    msg_len = len(msg_bytes)

    # Ensure message fits inside the image
    max_bytes = img.shape[0] * img.shape[1] * 3
    if msg_len > max_bytes - 3:
        messagebox.showerror("Error", "Message is too large to be hidden in the selected image!")
        return

    # Store message length in first two pixels
    img[0, 0, 0] = msg_len % 256  
    img[0, 0, 1] = (msg_len // 256) % 256  

    flat_img = img.flatten()
    for i in range(msg_len):
        flat_img[i + 3] = msg_bytes[i]  # Store message bytes in image pixels
    
    img = flat_img.reshape(img.shape)
    cv2.imwrite(SAVE_PATH, img)

    os.system(f"start {SAVE_PATH}")
    messagebox.showinfo("Success", f"Message encrypted and saved at:\n{SAVE_PATH}")

def decrypt():
    img_path = filedialog.askopenfilename(title="Select Encrypted Image", filetypes=[("Image Files", "*.jpg *.png *.bmp")])
    if not img_path:
        messagebox.showerror("Error", "No image selected!")
        return

    img = cv2.imread(img_path)
    if img is None:
        messagebox.showerror("Error", "Could not load image. Check the file path.")
        return

    saved_password = load_password()
    pas = simpledialog.askstring("Input", "Enter passcode for decryption:", show="*", parent=root)
    
    if pas != saved_password:
        messagebox.showerror("Error", "Incorrect password!")
        return

    # Convert uint8 to int to avoid OverflowError
    msg_len = int(img[0, 0, 0]) + int(img[0, 0, 1]) * 256

    flat_img = img.flatten()

    try:
        msg_bytes = bytes(flat_img[3:3 + msg_len])  
        decrypted_message = msg_bytes.decode('utf-8')
    except UnicodeDecodeError:
        messagebox.showerror("Error", "Decryption failed. Data may be corrupted.")
        return

    messagebox.showinfo("Decrypted Message", decrypted_message)

# GUI Setup
root = tk.Tk()
root.title("Image Steganography")
root.geometry("600x600")

label = tk.Label(root, text="Image Steganography", font=("Arial", 18, "bold"))
label.pack(pady=20)

encrypt_btn = tk.Button(root, text="Encrypt Message", command=encrypt, font=("Arial", 14), bg="lightblue", width=30, height=3)
encrypt_btn.pack(pady=20)

decrypt_btn = tk.Button(root, text="Decrypt Message", command=decrypt, font=("Arial", 14), bg="lightgreen", width=30, height=3)
decrypt_btn.pack(pady=20)

exit_btn = tk.Button(root, text="Exit", command=root.quit, font=("Arial", 14), bg="red", width=30, height=3)
exit_btn.pack(pady=20)

root.mainloop()
