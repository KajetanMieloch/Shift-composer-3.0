import loader
import init

def main():
    data_loader = loader.Loader()
    employeesAdnAvailability = init.EmployeesAndAvailability(data_loader.get_all_employeesloyees_data(), data_loader.get_employees_properties_data())

    print("Employee by id:")
    print(employeesAdnAvailability.get_employee_by_id(1))
    
    print("Employee availability by id:")
    print(employeesAdnAvailability.get_employee_availability_by_id(1))

    print("Employee availability by date:")
    print(employeesAdnAvailability.get_employee_availability_by_date(1, "2024-03-06"))

    print("All employees availability by date:")
    print(employeesAdnAvailability.get_all_employees_availability_by_date("2024-03-06"))

    print("All employees availability by date and department:")
    print(employeesAdnAvailability.get_all_employees_availability_by_date_department("2024-03-06", "HR"))
    

if __name__ == "__main__":
    main()
