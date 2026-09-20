<?php
include "config.php";
$name = $_POST['name'];
$score = $_POST['score'];//$_POST['score'];
$date = date('Y-m-d');//$_POST['date'];
$note = "";
// code to store the variables on the server

echo "Variables stored successfully.";

// check if the script received a new value for the variable via POST
if (isset($_POST['name'])) {
    $score = $_POST['score'];//$_POST['score'];
    $date = date('Y-m-d');//$_POST['date'];
    $note = "";


   // Step 1: Establish a connection to the database

    $conn = new mysqli($servername, $username, $password, $dbname);

    // Check connection
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
        echo 'connect failed';
    }
    echo 'connect successfully';
 

    // Step 2: Prepare the SQL statement
    $stmt = $conn->prepare("INSERT INTO leader_board (user_name, score, date_game, note) VALUES (?, ?, ?, ?)");
    
    if($stmt){
      echo 'end prepare';
    }else{
      echo $conn->error;
    }

 

    // Step 3: Bind the variables to the prepared statement
    $stmt->bind_param("sdss", $val1, $val2, $val3, $val4);
    echo 'end bind varables';
            
    // Set the values of the variables
    $val1 = $name;
    $val2 = $score;
    $val3 = $date;
    $val4 = $note;
 


    // Step 4: Execute the prepared statement
    $stmt->execute();
    echo 'end execute';

    // Close the connection
    $conn->close();

    echo 'DB updated successfully';








  } else {
    // return the current value of the variable to the Ajax request
    echo $variable;
  }
  if (isset($_POST['age'])) {
    // write the new value to the file
    $variable = $_POST['age'];
    file_put_contents('variable.txt', $variable);
    echo 'Variable updated successfully';
  } else {
    // return the current value of the variable to the Ajax request
    echo $variable;
  }
?>