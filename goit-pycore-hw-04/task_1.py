def total_salary(path: str) -> tuple[float, float]:
    """
        Calculates the total and average salary of developers from a text file.

        Args:
            path (str): The path to a text file that contains records
                        in the format "Name,Salary". Each line corresponds
                        to one developer.

        Returns:
            tuple[float, float]: A tuple containing:
                - The total sum of all salaries (float)
                - The average salary (float)

        Raises:
            FileNotFoundError: If the specified file does not exist.
        """"""
    Calculates the total and average salary of developers from a text file.

    Args:
        path (str): The path to a text file that contains records 
                    in the format "Name,Salary". Each line corresponds
                    to one developer.

    Returns:
        tuple[float, float]: A tuple containing:
            - The total sum of all salaries (float)
            - The average salary (float)

    Raises:
        FileNotFoundError: If the specified file does not exist.
    """
    try:
        with open(path, "r", encoding="utf-8") as file:
            lines = file.readlines()

        salaries = []
        for line in lines:
            if line.strip():
                name, salary = line.strip().split(",")
                salaries.append(float(salary))

        total_salary_sum  = sum(salaries)
        average_salaries = total_salary_sum / len(salaries) if salaries else 0
        return total_salary_sum, average_salaries

    except FileNotFoundError:
        print("File not found")
        return 0, 0


total, average = total_salary("salary_file.txt")
print(f"Загальна сума заробітної плати: {total}, Середня заробітна плата: {average}")
