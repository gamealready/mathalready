<?php
  include "php/config.php";
  // Step 1: Establish a connection to the database

  $conn = new mysqli($servername, $username, $password, $dbname);

  // Check connection
  if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
  }

    // retrieve data from the database
    $sql = "SELECT * FROM leader_board ORDER BY score DESC LIMIT 10";
    $result = mysqli_query($conn, $sql);



    // encode the data as a JSON object
    $data = array();
    while ($row = mysqli_fetch_assoc($result)) {
        $data[] = $row;
    }
    echo json_encode($data);

    
?>