import loader
import init
import generator as gen

def generate(department):
    data_loader = loader.Loader()
    employeesAndAvailability = init.EmployeesAndAvailability(data_loader.get_all_employeesloyees_data(), data_loader.get_employees_properties_data())
    sheduleProperties = init.ScheduleProperties(data_loader.get_schedule_properties_data())

    generator = gen.Generator(employeesAndAvailability, sheduleProperties)

    harmonogram = generator.generate_harmonogram_phase_0(sheduleProperties.get_work_hours_for_department(department), department)
    print(harmonogram)

def main():
    generate("HR")
    generate("Security")

if __name__ == "__main__":
    main()
