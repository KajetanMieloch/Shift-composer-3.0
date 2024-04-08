import loader
import init
import generator as gen

def generate(department, priority = 0):
    #priority is used when one employee is available for multiple departments
    #priority 0 means that none of the departments is prioritized, so employee will be randomly selected, try to avoid this
    data_loader = loader.Loader()
    employeesAndAvailability = init.EmployeesAndAvailability(data_loader.get_all_employeesloyees_data(), data_loader.get_employees_properties_data(), data_loader.get_schedule_properties_data())
    sheduleProperties = init.ScheduleProperties(data_loader.get_schedule_properties_data())

    generator = gen.Generator(employeesAndAvailability, sheduleProperties)

    harmonogram = generator.generate_harmonogram_phase_0(sheduleProperties.get_work_hours_for_department(department), department)
    
    ## Debug ###
    for h in harmonogram:
        #print(h.start_date, h.end_date, h.start_hour, h.end_hour, h.matched_employees)
        for emp in h.matched_employees:
            #print(emp.get_id(), emp.get_name(), emp.get_hours_of_availability(department))
            pass
    ## Debug ###
        
    #This return is marked to delete
    #Instead of returning the harmonogram, we should process it and return optimized harmonogram
    optimazed_harmonogram = generator.generate_harmonogram_phase_1(harmonogram, department, sheduleProperties)

    return {"department": department, "harmonogram": optimazed_harmonogram}


def get_schedule_to_combine(schedules):
    """
    Retrieves the schedules that need to be combined based on the shared employees' availability for multiple departments.

    Args:
        schedules (list): A list of schedules.

    Returns:
        list: A list of schedules to be combined, where each schedule is represented as a list of department names.
    """
    shared_employees = []
    schedules_to_combine = []
    for s in schedules:
        for h in s["harmonogram"]:
            for emp in h.matched_employees:
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

    schedules_single_department = []
    schedules_multiple_departments = []

    schedules = []
    #schedules.append(generate("HR"))
    #schedules.append(generate("IT"))
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
