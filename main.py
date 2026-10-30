import pymysql

# Initialize MariaDB connection
conn = pymysql.connect(
    host='localhost', user='root', password='', database='student_db'
)
cursor = conn.cursor()

# Create table with AUTO_INCREMENT ID and unique name constraint
cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) UNIQUE,
        preliminary_grade DECIMAL(5,2),
        midterm_grade DECIMAL(5,2),
        final_grade DECIMAL(5,2)
    )
""")
conn.commit()


def get_db_students():
  cursor.execute(
      "SELECT name, preliminary_grade, midterm_grade, final_grade FROM students"
  )
  return [
      {
          "name": row[0],
          "preliminary grade": row[1],
          "midterm grade": row[2],
          "final grade": row[3],
      }
      for row in cursor.fetchall()
  ]


def calculate_grades(student):
  total = (
      student["preliminary grade"]
      + student["midterm grade"]
      + student["final grade"]
  )
  avg = total / 3
  if avg >= 90:
    status = "Outstanding"
  elif avg >= 85:
    status = "Very Satisfactory"
  elif avg >= 80:
    status = "Satisfactory"
  elif avg >= 75:
    status = "Passed"
  else:
    status = "Failed"
  return avg, status


def get_valid_grade(prompt_text):
  attempts = 0
  while attempts < 3:
    val = input(prompt_text)
    try:
      num = float(val)
      if 0 <= num <= 100:
        return num
      print("\nNOTE: Number must be between 0 and 100.\n")
    except ValueError:
      print("\nNOTE: Numbers only.\n")
    attempts += 1
  print("NOTE: Too many attempts. Returning to menu.\n")
  return None


while True:
  print("\n" + "=" * 65)
  print("STUDENT PERFORMANCE SYSTEM (MariaDB)")
  print("=" * 65)
  print(
      "\n[1] Add Students\n[2] View Students Record\n[3] View Class"
      " Summary\n[4] Search Student\n[5] Edit Student\n[6] Delete Student\n[7]"
      " Exit"
  )
  print("\n" + "=" * 65)
  select = input("Enter choice: ")
  print("=" * 65)

  students = get_db_students()

  if select == "1":
    try:
      enter = int(input("\nHow many students will be entered?\nEnter: "))
    except ValueError:
      print("\nNOTE: Type the number only.\n")
      continue

    for i in range(enter):
      print(f"\nSTUDENT[{i + 1}]")
      attempts = 0
      while attempts < 3:
        name = input("Enter name: ")
        if not all(w.isalpha() for w in name.split()):
          print("\nNOTE: Letters only and nothing else.\n")
        elif len(name.split()) < 2:
          print(
              "\nNOTE: Name must have 2 or more words: [Kenneth Pacanza,"
              " Christine Logroño]\n"
          )
        elif not name.istitle():
          print(
              "\nNOTE: Each word must start with a capital letter and lowercase"
              " rest.\n"
          )
        elif any(s["name"].lower() == name.lower() for s in get_db_students()):
          print("\nNOTE: This name is already in use.\n")
        else:
          break
        attempts += 1
      else:
        print("NOTE: Too many attempts. Returning to menu.\n")
        continue

      prelim = get_valid_grade("Enter preliminary grade: ")
      if prelim is None:
        continue
      mid = get_valid_grade("Enter midterm grade: ")
      if mid is None:
        continue
      fin = get_valid_grade("Enter final grade: ")
      if fin is None:
        continue

      try:
        cursor.execute(
            "INSERT INTO students (name, preliminary_grade, midterm_grade,"
            " final_grade) VALUES (%s, %s, %s, %s)",
            (name, prelim, mid, fin),
        )
        conn.commit()
        print("=" * 65 + "\nSTUDENT ADDED SUCCESSFULLY. ✅\n" + "=" * 65)
      except pymysql.err.IntegrityError:
        print("\nNOTE: Student already exists in database.\n")

  elif select == "2":
    if not students:
      print(
          "\n\n"
          + "=" * 65
          + "\nNOTE: NO STUDENT/S DATA RECORD TO BE VIEWED YET.\n"
          + "=" * 65
          + "\n\n"
      )
      continue

    print("\n" + "=" * 65 + "\nSTUDENT RECORDS\n" + "=" * 65 + "\n")
    print(f"{'Name':<25}{'Average':<15}{'Status':<25}\n" + "=" * 65)
    for s in students:
      avg, status = calculate_grades(s)
      print(f"{s['name']:<25}{avg:<15.2f}{status:<25}\n" + "=" * 65)

  elif select == "3":
    if not students:
      print(
          "\n\n"
          + "=" * 65
          + "\nNOTE: NO STUDENT/S DATA TO BE SUMMARIZE YET.\n"
          + "=" * 65
          + "\n\n"
      )
      continue

    averages = [calculate_grades(s)[0] for s in students]
    highest_avg, lowest_avg = max(averages), min(averages)
    high_s = students[averages.index(highest_avg)]
    low_s = students[averages.index(lowest_avg)]
    class_avg = sum(averages) / len(students)
    passed = sum(1 for a in averages if a >= 75)
    failed = len(students) - passed
    passing_rate = (passed / len(students)) * 100

    print("\n" + "=" * 65 + "\nCLASS PERFORMANCE SUMMARY\n" + "=" * 65)
    print(f"Highest Average : {high_s['name']} - {highest_avg:.2f}")
    print(f"Lowest Average  : {low_s['name']} - {lowest_avg:.2f}")
    print(f"\nClass Average    : {class_avg:.2f}")
    print(
        f"\nPassed Students  : {passed}\nFailed Students  :"
        f" {failed}\nPassing Rate     : {passing_rate:.2f}%\n"
        + "=" * 65
    )

  elif select in ["4", "5", "6"]:
    if not students:
      print(
          "\n\n"
          + "=" * 65
          + "\nNOTE: NO STUDENT DATA AVAILABLE YET.\n"
          + "=" * 65
          + "\n\n"
      )
      continue

    attempts = 0
    while attempts < 3:
      search_name = input("\nEnter student name: ")
      found = next(
          (s for s in students if s["name"].lower() == search_name.lower()),
          None,
      )

      if found:
        avg, status = calculate_grades(found)
        if select == "4":
          print(
              f"\n[STUDENT FOUND]\nName:[{found['name']}]\nPreliminary:["
              f"{found['preliminary grade']:.2f}]\nMidterm:["
              f"{found['midterm grade']:.2f}]\nFinal:["
              f"{found['final grade']:.2f}]\nAverage:[{avg:.2f}]\nStatus:["
              f"{status}]"
          )
        elif select == "5":
          print(f"\n[EDITING STUDENT: {found['name']}]")
          new_prelim = get_valid_grade("Enter new preliminary grade: ")
          new_mid = get_valid_grade("Enter new midterm grade: ")
          new_fin = get_valid_grade("Enter new final grade: ")
          if None in (new_prelim, new_mid, new_fin):
            break
          cursor.execute(
              "UPDATE students SET preliminary_grade=%s, midterm_grade=%s,"
              " final_grade=%s WHERE name=%s",
              (new_prelim, new_mid, new_fin, found["name"]),
          )
          conn.commit()
          print("=" * 65 + "\nSTUDENT UPDATED SUCCESSFULLY. 🔄\n" + "=" * 65)
        elif select == "6":
          cursor.execute("DELETE FROM students WHERE name=%s", (found["name"],))
          conn.commit()
          print("=" * 65 + "\nSTUDENT DELETED SUCCESSFULLY. 🗑️\n" + "=" * 65)
        break
      else:
        print("\n" + "=" * 65 + "\nNOTE: STUDENT NOT FOUND.\n" + "=" * 65)
        attempts += 1
    else:
      print("NOTE: Too many attempts. Returning to menu.\n")

  elif select == "7":
    print("\n\nEXITING MENU COMPLETE.\n\n")
    conn.close()
    break
  else:
    print(
        "\n\n"
        + "=" * 65
        + "\nNOTE: NOTHING IN THE OPTION. CHOOSE AGAIN.\n"
        + "=" * 65
        + "\n\n"
    )
