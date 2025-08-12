import os
from colorama import Fore
def number_to_month_conversion(n:int)->str:
    """Function return months"""
    months=["january","febuarary","march",
            "april","may","june","july","august",
            "september","october","november","december"]
    return months[n-1]

class ReportGeneration:
    """Class For Report Generation"""

    def get_files(self,year:int,directorypath:str):
        """Get Related Data files from the directory """
        try:
            folder_path = os.path.join(directorypath)
            files = [
                os.path.join(folder_path, f)
                for f in os.listdir(folder_path)
                if f.endswith(".txt") and str(year) in f
            ]
            return sorted(files)
        except Exception as e:
            print(f"Error reading directory: {e}")
            return []
    def str_to_int(self,value:str):
        try:
            return int(value)
        except (ValueError, TypeError):
            print ("File values are not correct")


    def yearly_report(self, file_list: list,date_col,max_col,min_col,humid_col):
        """Combine multiple monthly files into one yearly report."""
        max_temp = None
        min_temp = None
        humidity = None
        max_temp_date = []
        min_temp_date = []
        humidity_date = []

        for filename in file_list:
            try:
                with open(filename, "r") as f:
                    f.readline()
                    for line in f:
                        parts = line.strip().split(",")
                        t_max = self.str_to_int(parts[max_col]) if parts[max_col] else None
                        t_min = self.str_to_int(parts[min_col]) if parts[min_col] else None
                        hum = self.str_to_int(parts[humid_col]) if parts[humid_col] else None
                        date = parts[date_col]
                        if t_max is not None:
                            if max_temp is None or t_max > max_temp:
                                max_temp = t_max
                                max_temp_date = [date]
                            elif t_max == max_temp:
                                max_temp_date.append(date)
                        if t_min is not None:
                            if min_temp is None or t_min < min_temp:
                                min_temp = t_min
                                min_temp_date = [date]
                            elif t_min == min_temp:
                                min_temp_date.append(date)
                        if hum is not None:
                            if humidity is None or hum > humidity:
                                humidity = hum
                                humidity_date = [date]
                            elif hum == humidity:
                                humidity_date.append(date)
            except FileNotFoundError:
                print(f"File not found: {filename}")
            except Exception as e:
                print(f"Error reading {filename}: {e}")
        self.display_yearly_report(max_temp,min_temp,humidity,max_temp_date,min_temp_date,humidity_date)

    def display_yearly_report(self, max_temp, min_temp, humidity, max_date, min_date, humid_date):
        """Printing results"""
        print(f"Highest: {max_temp}C on {', '.join(f'{number_to_month_conversion(int(m))} {d}' for y, m, d in (date.split('-') for date in max_date))}")
        print(f"Lowest: {min_temp}C on {', '.join(f'{number_to_month_conversion(int(m))} {d}' for y, m, d in (date.split('-') for date in min_date))}")
        print(f"Humid: {humidity}% on {', '.join(f'{number_to_month_conversion(int(m))} {d}' for y, m, d in (date.split('-') for date in humid_date))}")
    
    def monthly_report(self,file_path:str,max_col,min_col,humid_col):
        """Creating monthly report by showing average temparature and humidity"""
        try:
            max_temp=[]
            min_temp=[]
            humid_temp=[]
            with open(file_path,"r") as f :
                f.readline()
                for line in f:
                    parts = line.strip().split(",")
                    t_max = int(parts[max_col]) if parts[max_col] else None
                    t_min = int(parts[min_col]) if parts[min_col] else None
                    hum = int(parts[humid_col]) if parts[humid_col] else None
                    if t_max is not None:
                        max_temp.append(t_max)
                    if t_min is not None:
                        min_temp.append(t_min)
                    if hum is not None:
                        humid_temp.append(hum)
                    
            print(f"Highest Average : {sum([t for t in max_temp]) // len(max_temp) if max_temp else 0}C") 
            print(f"Lowest Average  : {sum([t for t in min_temp]) // len(min_temp) if min_temp else 0}C")
            print(f"Humidity Average: {sum([t for t in humid_temp]) // len(humid_temp) if humid_temp else 0}%")
        except Exception as e:
            print(f"Error reading file: {e}")
            return []


    def monthly_bar_graph(self,file_path:str,max_col,min_col,date_col):
        formatted_date_state=False
        try:
            with open(file_path,"r") as f :
                f.readline()
                for line in f:
                    parts = line.strip().split(",")
                    t_max = self.str_to_int(parts[max_col]) if parts[max_col] else None
                    t_min = self.str_to_int(parts[min_col]) if parts[min_col] else None
                    y, m, d = parts[date_col].split("-")
                    formatted_date = f"{number_to_month_conversion(int(m))} {y}"
                    if formatted_date is not None and formatted_date_state is False :
                        print(formatted_date)
                        formatted_date_state=True
                    if t_max is not None:
                        bar="+"*t_max
                        print(f"{d} {Fore.RED }{bar} {Fore.WHITE} {t_max}C")
                    if t_min is not None:
                        bar2="+"*t_min
                        print(f"{d} {Fore.BLUE }{bar2} {Fore.WHITE} {t_min}C")
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
    def combine_monthly_bar_graph(self,file_path:str,max_col,min_col,date_col):
        formatted_date_state=False
        try:
            with open(file_path,"r") as f :
                f.readline()
                for line in f:
                    parts = line.strip().split(",")
                    t_max = self.str_to_int(parts[max_col]) if parts[max_col] else None
                    t_min = self.str_to_int(parts[min_col]) if parts[min_col] else None
                    y, m, d = parts[date_col].split("-")
                    formatted_date = f"{number_to_month_conversion(int(m))} {y}"
                    if formatted_date is not None and formatted_date_state is False :
                        print(formatted_date)
                        formatted_date_state=True
                    if t_max is not None and t_min is not None:
                        bar="+"*t_max
                        bar2="+"*t_min
                        print(f"{d} {Fore.BLUE }{bar2}{Fore.RED }{bar} {Fore.WHITE} {t_min}C-{t_max}C")
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except Exception as e:
            print(f"Error reading {file_path}: {e}")



if __name__ == "__main__":

    r = ReportGeneration()
    while True :
        print("=====================================================")
        print("1.Annual Report")
        print("2.Monthly Report (Avg. Basis)")
        print("3.Monthly Temparature Based Barchart")
        print("4.Combined Monthly Temparature Based Barchart")
        print("0.Exit")
        print("=====================================================")
        op=input ("Choose an option : ")

        match op:
            case "1":
                directory_path=input("Enter Directory path for annual report :")
                files=r.get_files(2004,directory_path)
                r.yearly_report(files,0,1,3,7)
            case "2": 
                filepath=input("Enter file path for monthlly report :")
                r.monthly_report(filepath,1,3,7)
            case "3":
                filepath=input("Enter file path for monthlly report :")
                r.monthly_bar_graph(filepath,1,3,0)
            case "4":
                filepath=input("Enter file path for monthlly report :")
                r.combine_monthly_bar_graph(filepath,1,3,0)
            case _:
                print("=====================================================")
                break
        
