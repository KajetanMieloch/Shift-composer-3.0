import loader
import init
import generator as gen

def generate(department):
    data_loader = loader.Loader()
    employeesAndAvailability = init.EmployeesAndAvailability(data_loader.get_all_employeesloyees_data(), data_loader.get_employees_properties_data(), data_loader.get_schedule_properties_data())
    sheduleProperties = init.ScheduleProperties(data_loader.get_schedule_properties_data())

    generator = gen.Generator(employeesAndAvailability, sheduleProperties)

    harmonogram = generator.generate_harmonogram_phase_0(sheduleProperties.get_work_hours_for_department(department), department)
    
    ### Debug ###
    # for h in harmonogram:
    #     print(h.start_date, h.end_date, h.start_hour, h.end_hour, h.matched_employees)
    #     for emp in h.matched_employees:
    #         print(emp.get_employee_avability_for_department())
    #         pass
    ### Debug ###
        
    return {"department": department, "harmonogram": harmonogram}

def combine(schedules):
    shared_employees = []
    schedules_to_combine = []
    for s in schedules:
        for h in s["harmonogram"]:
            for emp in h.matched_employees:
                #THIS IS THE EASY WAY TO DO IT
                #I PROGRAMED ALL METHOS BEFORE NOW I IT SO EASY
                #emp.get_employee_avability_for_department() is a dictionary with the hours of availability for each department
                if len(emp.get_employee_avability_for_department().keys()) > 1:
                    if emp not in shared_employees:
                        shared_employees.append(emp)
    
    for emp in shared_employees:
        print(emp.get_name(), emp.get_surname() , emp.get_employee_avability_for_department())

def main():
    schedules = []
    schedules.append(generate("HR"))
    schedules.append(generate("IT"))
    schedules.append(generate("Security"))

    combine(schedules)


if __name__ == "__main__":
    main()
