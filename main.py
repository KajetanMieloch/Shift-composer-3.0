import loader
import init

def main():
    data_loader = loader.Loader()
    employeesAdnAvailability = init.EmployeesAndAvailability(data_loader.get_all_employeesloyees_data(), data_loader.get_employees_properties_data())

    print(employeesAdnAvailability.employees[0].get_all_info())
    print(employeesAdnAvailability.get_name_by_id(1))

    

if __name__ == "__main__":
    main()
