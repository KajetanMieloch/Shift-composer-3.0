import loader
import init
import generator as gen

def generate(department):
    data_loader = loader.Loader()
    employeesAndAvailability = init.EmployeesAndAvailability(data_loader.get_all_employeesloyees_data(), data_loader.get_employees_properties_data(), data_loader.get_schedule_properties_data())
    sheduleProperties = init.ScheduleProperties(data_loader.get_schedule_properties_data())

    generator = gen.Generator(employeesAndAvailability, sheduleProperties)

    harmonogram = generator.generate_harmonogram_phase_0(sheduleProperties.get_work_hours_for_department(department), department)
    
    ## Debug ###
    for h in harmonogram:
        print(h.start_date, h.end_date, h.start_hour, h.end_hour, h.matched_employees)
        for emp in h.matched_employees:
            print(emp.get_employee_avability_for_department())
            pass
    ## Debug ###
        
    return {"department": department, "harmonogram": harmonogram}

def get_schedule_to_combine(schedules):
    shared_employees = []
    schedules_to_combine = []
    for s in schedules:
        for h in s["harmonogram"]:
            for emp in h.matched_employees:
                #THIS IS THE EASY WAY TO DO IT
                #I PROGRAMED ALL METHOS BEFORE NOW I IT SO EASY
                #emp.get_employee_avability_for_department() is a dictionary with the hours of availability for each department
                if len(emp.get_employee_avability_for_department().keys()) > 1:
                    if emp not in shared_employees and emp.get_id() not in [e.get_id() for e in shared_employees]:
                        shared_employees.append(emp)
    
    for emp in shared_employees:
        schedules_to_combine.append(list(emp.get_employee_avability_for_department().keys()))

    return schedules_to_combine

def combine(schedules, schedules_to_combine):

    temp_schedules_to_combine = []

    for s in schedules:
        #ESSA
        #THAT WAS HARD LINE
        if s.get("department") in [x for y in schedules_to_combine for x in y]:
            temp_schedules_to_combine.append(s)
    
    return temp_schedules_to_combine
    



def main():

    schedules_multiple_departments = []
    schedules_single_department = []

    schedules = []
    schedules.append(generate("HR"))
    schedules.append(generate("IT"))
    schedules.append(generate("Security"))

    schedules_to_combine = get_schedule_to_combine(schedules)
    combined = combine(schedules, schedules_to_combine)
    
    for s in schedules:
        if s in combined:
            schedules_multiple_departments.append(s)
        else:
            schedules_single_department.append(s)

if __name__ == "__main__":
    main()
