import loader
import init

def main():
    data_loader = loader.Loader()
    employeesAndAvailability = init.EmployeesAndAvailability(data_loader.get_all_employeesloyees_data(), data_loader.get_employees_properties_data())
    sheduleProperties = init.ScheduleProperties(data_loader.get_schedule_properties_data())

    # print("Employee by id:")
    # print(employeesAndAvailability.get_employee_by_id(1))
    
    # print("Employee availability by id:")
    # print(employeesAndAvailability.get_employee_availability_by_id(1))

    # print("Employee availability by date:")
    # print(employeesAndAvailability.get_employee_availability_by_date(1, "2024-03-06"))

    # print("All employees availability by date:")
    # print(employeesAndAvailability.get_all_employees_availability_by_date("2024-03-06"))

    # print("All employees availability by date and department:")
    # print(employeesAndAvailability.get_all_employees_availability_by_date_department("2024-03-06", "HR"))

    # print("All employees availability by department:")
    # print(employeesAndAvailability.get_all_employees_availability_by_department("HR"))
    
    print("Shedule by department:")
    print(sheduleProperties.get_properties_for_department("HR"))
    print("Min employees by department:")
    print(sheduleProperties.get_minEmployees_for_department("HR"))
    print("Max employees by department:")
    print(sheduleProperties.get_maxEmployees_for_department("HR"))

if __name__ == "__main__":
    main()
