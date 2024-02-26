import requests
import math
from datetime import datetime
import customtkinter
import tkinter as tk


def clock():
    time_live = datetime.now()
    time_live = time_live.strftime('%H:%M:%S')
    time_str.set(time_live)
    clock_label.after(100, clock)


def date():
    date_live = datetime.now()
    date_live = date_live.strftime('%A\n%d/%m/%Y')
    date_str.set(date_live)


def kelvin_to_celsius(temp):
    celsius = temp - 273.15
    return celsius


def cardinal_direction(wind_deg):
    val = math.floor((wind_deg / 22.5) + 0.5)
    arr = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    return arr[(val % 16)]


def return_button(event):
    collect_data()


def collect_data():
    global icon
    base_url = 'http://api.openweathermap.org/data/2.5/weather?'
    api_key = 'register and get own key ;)'
    city = enter_city.get()
    url = base_url + 'appid=' + api_key + '&q=' + city
    response = requests.get(url).json()

    country = response['sys']['country']
    description = response['weather'][0]['description']
    description_icon = response['weather'][0]['icon']
    temp_celsius = response['main']['temp']     # temp in kelvin to celsius
    time_zone_location = response['timezone']
    time_zone_location = datetime.timestamp(datetime.utcnow()) + time_zone_location
    time_zone_location = datetime.fromtimestamp(time_zone_location)
    time_zone_location = time_zone_location.strftime('%H:%M:%S')
    output.after(100, collect_data)
    temp_feels_like = response['main']['feels_like']
    pressure = response['main']['pressure']
    humidity = response['main']['humidity']
    wind_speed = response['wind']['speed']
    wind_deg = response['wind']['deg']
    visibility = response['visibility']

    output_temp_str.set(f'{kelvin_to_celsius(temp_celsius):.1f} °C')
    output_str.set(f'\n{city.upper()}, {country} | {time_zone_location}\n'
                   f'Feels like {kelvin_to_celsius(temp_feels_like):.1f} °C | {description.capitalize()}\n'
                   f'Pressure: {pressure} hPa\n'
                   f'Humidity: {humidity} % \n'
                   f'Wind Speed: {wind_speed}m/s {cardinal_direction(wind_deg)}\n'
                   f'Visibility: {visibility / 1000} km\n')

    # https://openweathermap.org/weather-conditions#Weather-Condition-Codes-2
    if description_icon == '01d':
        icon = 'icons/01d.png'
    elif description_icon == '01n':
        icon = 'icons/01n.png'
    elif description_icon == '02d':
        icon = 'icons/02d.png'
    elif description_icon == '02n':
        icon = 'icons/02n.png'
    elif description_icon == '03d' or '03n':
        icon = 'icons/03.png'
    elif description_icon == '04d' or '04n':
        icon = 'icons/04.png'
    elif description_icon == '10d':
        icon = 'icons/06d.png'
    elif description_icon == '09d':
        icon = 'icons/06n.png'
    elif description_icon == '11d':
        icon = 'icons/07.png'
    elif description_icon == '13d':
        icon = 'icons/08.png'
    elif description_icon == '50d':
        icon = 'icons/09.png'
    else:
        icon = 'icons/10.png'

    icon = tk.PhotoImage(file=f'{icon}')
    root.img = icon
    canvas.itemconfig('change_icon', image=icon)


root = customtkinter.CTk()
root.title('Weather')
root.geometry('550x800')
root.resizable(False, False)
root.config(background='#007777')

time_str = customtkinter.StringVar()
clock_label = customtkinter.CTkLabel(root, font=('Calibri', 60), text='', textvariable=time_str, bg_color='#007777')
clock_label.pack(pady=10)

date_str = customtkinter.StringVar()
date_label = customtkinter.CTkLabel(root, font=('Calibri', 32), text='', textvariable=date_str, bg_color='#007777')
date_label.pack(pady=10)

search_label_frame = customtkinter.CTkFrame(root, fg_color='#007777', bg_color='#007777', corner_radius=0)
search_label_frame.pack(pady=10)

enter_city = customtkinter.CTkEntry(search_label_frame, font=('Calibri', 32), bg_color='#007777', fg_color='#003333',
                                    border_color='#003333', corner_radius=5, width=300)
enter_city.grid(row=0, column=0, padx=10, pady=15)


search_button = customtkinter.CTkButton(search_label_frame, font=('Calibri', 32), text='🔍', bg_color='#007777',
                                        fg_color='#003333', border_color='#003333', corner_radius=5, width=10,
                                        command=collect_data)
search_button.grid(row=0, column=1, pady=15)
root.bind('<Return>', return_button)

canvas = tk.Canvas(root, width=200, height=200, background='#007777', bd=0, highlightthickness=0, relief='ridge')
canvas.pack()

img_placeholder = 'icons/10.png'
img = tk.PhotoImage(file=f'{img_placeholder}')
root.img = img
canvas.create_image(0, 0, image=img, anchor='nw', tag='change_icon')

output_temp_str = customtkinter.StringVar()
output_temp = customtkinter.CTkLabel(root, font=('Calibri', 60), text='', bg_color='#007777',
                                     textvariable=output_temp_str)
output_temp.pack()

output_str = customtkinter.StringVar()
output = customtkinter.CTkLabel(root, font=('Calibri', 32), text='', bg_color='#007777', textvariable=output_str)
output.pack()

clock()
date()
root.mainloop()
