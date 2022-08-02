import tkinter as tk
from tkinter import font
from tkinter.filedialog import askopenfile
from PictureLocation import PictureLocation
from pathlib import Path
from PIL import ImageTk, Image


class GUI:
    def __init__(self) -> None:
        """_summary_"""
        self.padding_x = 0
        self.padding_y = 5
        self.pic_width = 600
        self.open_file = False
        self.root = tk.Tk()
        self.root.title("PictureLokation")
        self.backgroundColor = "white"
        self.lable = tk.Label(self.root, background=self.backgroundColor)
        self.init()

    def init(self) -> None:
        """_summary_"""
        #  ----------------- open image -----------------
        image_open = Image.open("icon.png")
        # resize image
        new_height = int(self.pic_width * image_open.size[1] / image_open.size[0])
        image_resize = image_open.resize((self.pic_width, new_height), Image.ANTIALIAS)
        image_loaction = ImageTk.PhotoImage(image_resize)
        self.image = tk.Label(self.lable, image=image_loaction, bg="white")
        # -----------------  header font -----------------
        font_headline = font.Font(size=30, weight="bold", family="Roboto")
        font_standard = font.Font(size=14, family="Roboto")
        # ----------------- header -----------------
        headline = tk.Label(self.lable, text="PictureLocation", font=font_headline, background=self.backgroundColor, foreground="#6F6F6F")
        upload_pic = tk.Label(self.lable, text="Upload Picture", font=font_standard, background=self.backgroundColor)
        # ----------------- button -----------------
        self.button_ask_file = tk.Button(self.lable, text="Load Picture", command=self.ask_open_file, height=2, bg="#fcba03")
        self.button_get_coordinaten = tk.Button(self.lable, text="Get Coordinats", command=self.pic_coordinaten, height=2, bg="#fcba03")
        self.button_get_address = tk.Button(self.lable, text="Get Address", command=self.pic_address, height=2, bg="#fcba03")
        self.button_get_map = tk.Button(self.lable, text="Open Map", command=self.get_map, height=2, bg="#fcba03")
        # ----------------- text -----------------
        self.text_coordinaten_long = tk.Label(self.lable, text="", bg="white", width=50, font=font.Font(size=12, family="Roboto"))
        self.text_coordinaten_grad = tk.Label(self.lable, text="", bg="white", width=50, font=font.Font(size=12, family="Roboto"))
        self.text_address_part1 = tk.Label(self.lable, text="", bg="white", width=50, font=font.Font(size=12, family="Roboto"))
        self.text_address_part2 = tk.Label(self.lable, text="", bg="white", width=50, font=font.Font(size=12, family="Roboto"))
        self.emty = tk.Label(self.lable, text="", bg="white", width=50)
        #  ----------------- grid -----------------
        self.lable.grid()
        # position header 01
        headline.grid(column=0, row=0, sticky=tk.EW, padx=self.padding_x, pady=self.padding_y)
        # position header 02
        upload_pic.grid(column=0, row=1, sticky=tk.EW, padx=self.padding_x, pady=self.padding_y)
        # position button "Load Picture"
        self.button_ask_file.grid(column=0, row=2, sticky=tk.EW, padx=self.padding_x, pady=self.padding_y)
        # position button of the image
        self.image.grid(column=0, row=3, sticky=tk.W, padx=self.padding_x, pady=self.padding_y)
        # position button "Get Coordinats"
        self.button_get_coordinaten.grid(column=0, row=4, sticky=tk.EW, padx=self.padding_x, pady=self.padding_y)
        # position button "Get Address"
        self.button_get_address.grid(column=0, row=5, sticky=tk.EW, padx=self.padding_x, pady=self.padding_y)
        # position button "Open Mape"
        self.button_get_map.grid(column=0, row=6, sticky=tk.EW, padx=self.padding_x, pady=self.padding_y)
        # position text "coordinats long"
        self.text_coordinaten_long.grid(column=0, row=7, sticky=tk.EW, padx=self.padding_x)
        # position text "coordinats grad"
        self.text_coordinaten_grad.grid(column=0, row=8, sticky=tk.EW, padx=self.padding_x)
        # emty space
        self.emty.grid(column=0, row=9, sticky=tk.EW, padx=self.padding_x)
        # position text "address" part 01
        self.text_address_part1.grid(column=0, row=10, sticky=tk.EW, padx=self.padding_x)
        # position text "address" part 02
        self.text_address_part2.grid(column=0, row=11, sticky=tk.EW, padx=self.padding_x)
        # building mainloop
        self.root.mainloop()

    def ask_open_file(self) -> None:
        """_summary_"""
        self.open_file = True
        file = askopenfile(
            mode="r", filetypes=[("Picture, *.jpg"), ("Picture, *.jpeg"), ("Picture, *.png"), ("Picture, *.gif"), ("All files", "*.*")]
        ).name
        self.button_ask_file.configure(bg="#55de00", text=Path(file).name)
        self.pic_location = PictureLocation(file)
        if not self.pic_location.gps:
            print("No GPS Infomation")
            self.button_ask_file.configure(bg="red", text=f"No GPS Infomation from {Path(file).name}")
            return

    def pic_coordinaten(self) -> None:
        """_summary_"""
        if not self.open_file:
            print("Please Load the Pic")
            self.button_ask_file.configure(bg="red", text="Please Load the Pic")
            return
        if not self.pic_location.gps:
            print("Try a other Pic")
            self.button_ask_file.configure(bg="red")
            return
        dg, grad = self.pic_location.get_coordinaten()
        print("the coordinats in [deg] are:")
        print(dg)
        print("the coordinats in [grad] are:")
        print(grad)
        self.text_coordinaten_long.configure(text=f"{dg[0]}: {dg[1]:.2f}°   and   {dg[2]}: {dg[3]:.2f}°   or")
        self.text_coordinaten_grad.configure(
            text=f"({grad[0][0]}°  {grad[0][1]}min  {grad[0][2]}s)   and   ({grad[1][0]}°  {grad[1][1]}min  {grad[1][2]}s)"
        )

    def pic_address(self) -> None:
        """_summary_"""
        if not self.open_file:
            print("Please Load the Pic")
            self.button_ask_file.configure(bg="red", text="Please Load the Pic")
            return
        if not self.pic_location.gps:
            print("Try a other Pic")
            self.button_ask_file.configure(bg="red")
            return
        address = self.pic_location.get_address()
        split_address = address.split(",")
        self.emty.configure(text="-" * 100)
        if len(split_address) > 6:
            address_part_01 = "".join(address.split(",")[:5])
            address_part_02 = "".join(address.split(",")[5:])
            self.text_address_part1.configure(text=address_part_01)
            self.text_address_part2.configure(text=address_part_02)
        else:
            self.text_address_part1.configure(text=address)

    def get_map(self) -> None:
        """_summary_"""
        if not self.open_file:
            print("Please Load the Pic")
            self.button_ask_file.configure(bg="red", text="Please Load the Pic")
            return
        if not self.pic_location.gps:
            print("Try a other Pic")
            self.button_ask_file.configure(bg="red")
            return
        self.pic_location.creat_map()


if __name__ == "__main__":
    gui = GUI()
