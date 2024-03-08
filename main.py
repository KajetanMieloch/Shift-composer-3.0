import loader
import init

def main():
    data_loader = loader.Loader()

    # Create an instance of the Employee class
    employees = []
    for emp in data_loader.get_all_employeesloyees_data():
        employees.append(init.Employee(emp["id"], emp["name"], emp["surname"], emp["department"]))
    
    for emp in employees:
        print(emp.get_all_info())
    
    

if __name__ == "__main__":
    main()
