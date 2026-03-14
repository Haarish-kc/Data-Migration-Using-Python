<?php
// Database connection details
$host = "localhost";
$username = "root";  // Your MySQL username
$password = "1234";      // Your MySQL password
$dbname = "student_data"; // The database name

// Create a connection
$conn = new mysqli($host, $username, $password, $dbname);

// Check for connection errors
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
																													
// Retrieve data from the HTML form
$student_id = $_POST['student_id'];
$name = $_POST['name'];
$age = $_POST['age'];
$gender = $_POST['gender'];
$contact_number = $_POST['contact_number'];
$email = $_POST['email'];

$course_id = $_POST['course_id'];
$course_title = $_POST['course_title'];
$department_name = $_POST['Department-Name'];

$tc_provided = $_POST['tc_provided'];
$marksheet_provided = $_POST['Marksheet_provided'];
$enrollment_date = $_POST['enrollment_date'];

// Convert date to correct format
$enrollment_date = date('Y-m-d', strtotime($enrollment_date));

// Insert data into the students table
$sql_student = "INSERT INTO students (student_id, name, age, gender, contact_number, email) 
                VALUES ('$student_id', '$name', '$age', '$gender', '$contact_number', '$email')";
if ($conn->query($sql_student) === TRUE) {
    echo "New student record created successfully.";
} else {
    echo "Error: " . $sql_student . "<br>" . $conn->error;
}

// Insert data into the courses table
$sql_course = "INSERT INTO courses (course_id,student_id, course_title, department_name) 
               VALUES ('$course_id','$student_id', '$course_title', '$department_name')";
if ($conn->query($sql_course) === TRUE) {
    echo "New course record created successfully.";
} else {
    echo "Error: " . $sql_course . "<br>" . $conn->error;
}

// Insert data into the enrollments table
$sql_enrollment = "INSERT INTO enrollments (student_id, course_id, tc_provided, marksheet_provided, enrollment_date) 
                   VALUES ('$student_id', '$course_id', '$tc_provided', '$marksheet_provided', '$enrollment_date')";
if ($conn->query($sql_enrollment) === TRUE) {
    echo "Enrollment record created successfully.";
} else {
    echo "Error: " . $sql_enrollment . "<br>" . $conn->error;
}

// Close the connection
$conn->close();
?>
