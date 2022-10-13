import tkinter as tk
import tkinter.filedialog
import tkinter.font
from tkinter import ttk
import os, subprocess, shutil

class Windows(tk.Tk):
    WIDTH = 600
    HEIGHT = 400
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # Adding title to the window
        self.wm_title("WinUSB")
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")

        # creating a frame and assigning it to container
        container = tk.Frame(self, height=self.HEIGHT, width=self.WIDTH)
        # specifying the region where the frame is packed in root
        container.pack(side="top", expand=True)

        # We will now create a dictionary of frames
        self.frames = {}
        # we'll create the frames themselves later but let's add the components to the dictionary.
        for F in [MainPage]:
            frame = F(container, self)

            # the windows class acts as the root window for the frames.
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Using a method to switch frames
        self.show_frame(MainPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        # raises the current frame to the top
        frame.tkraise()

class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.iso_file = ""
        self.usb_path = ""

        iso_input = tk.Label(
            self,
            text="Windows ISO File",
            font="Times 12"
        )
        # iso_input.pack(side="top")
        iso_input.grid(row=0, column=0)

        self.iso_selector = tk.Button(
            self,
            text="Select Windows ISO File",
            command=self.get_iso_path
        )
        self.iso_selector.grid(row=0, column=1)
        print("Font check:", tk.font.families())

        usb_input = tk.Label(
            self,
            text="Path to USB drive",
            font="Arial 12"
        )
        # usb_input.pack(side="top")
        usb_input.grid(row=1, column=0)
        self.usb_selector = tk.Button(
            self,
            text="Select USB path",
            command=self.get_usb_path
        )
        self.usb_selector.grid(row=1, column=1)

        # We use the switch_window_button in order to call the show_frame() method as a lambda function
        switch_window_button = tk.Button(
            self,
            text="Create installation media",
            command=self.create_installation_media,
        )
        switch_window_button.grid(row=2, column=0)

    def get_iso_path(self):
        self.iso_file = tk.filedialog.askopenfilename(
            initialdir = "~",
            title = "Select a File",
            filetypes = (
                ("ISO files", "*.iso*"),
                ("all files", "*.*")
            )
        )
        self.iso_selector.config(text=self.iso_file)
        print("ISO entry:", self.iso_file)
    
    def get_usb_path(self):
        self.usb_path = tk.filedialog.askdirectory(
            initialdir="~",
            title="Select a folder"
        )
        self.usb_selector.config(text=self.usb_path)
        print("USB entry:", self.usb_path)
    
    def create_installation_media(self):
        self.dependency_install()
        self.mount_iso()
        self.copy_installation_file()
        self.cleanup()

    def dependency_install(self):
        package_name = "wimtools"
        subprocess.run(["sudo", "apt", "install", "-y", package_name], check=True)
    
    def mount_iso(self):
        os.mkdir("/media/iso")
        subprocess.run(["sudo", "mount", "-o", "loop", self.iso_file, "/media/iso"], check=True)
    
    def copy_installation_file(self):
        shutil.copyfile("/media/iso/sources/install.wim", "/tmp")
        subprocess.run(["wimlib-imagex", "split", "/tmp/install.wim", "/tmp/install.swm", 4000], check=True)
        shutil.copytree("/media/iso/", self.usb_path, ignore="/media/iso/sources/install.wim")
        subprocess.run(["scp", "-v", "/tmp/install*swm", os.path.join(self.usb_path, "sources", "")], check=True)
        files = [f for f in os.listdir("/tmp") if ".swm" in f]
        [shutil.copyfile(f, os.path.join(self.usb_path, "sources")) for f in files]
    
    def cleanup(self):
        subprocess.run(["sudo", "umount", "/media/iso"], check=True)
        subprocess.run(["sudo", "rmdir", "/media/iso"], check=True)
        subprocess.run(["rm", "-f", "/tmp/install.wim", "/tmp/install*swm"], check=True)


if __name__ == "__main__":
    testObj = Windows()
    testObj.mainloop()
