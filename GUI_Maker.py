#https://www.youtube.com/watch?v=iM3kjbbKHQU


#this is the setup class needed to make a GUI
import customtkinter as tkint




def init():
    tkint.set_appearance_mode("dark")
    tkint.set_default_color_theme("dark-blue")
    root = tkint.CTk() 
    root.geometry("500x300")

    frame = tkint.CTkFrame(master=root)
    frame.pack(pady=20,padx=60,fill="both",expand = True)

    label = tkint.CTkLabel(master=frame, text = "APP")
    label.pack(pady = 12, padx = 10 )

    button = tkint.CTkButton(master=frame,text="start", command = button_press )
    button.pack(padx = 12, pady=10)

    root.mainloop()


def button_press():
        print("test")


if __name__ == "__main__":
    init()
