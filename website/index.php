<!doctype html>
<html>
<head>
    <title>RenitoBot</title>
    <script src="jquery.js"></script> <!--include this first! or jquery won't work!-->
    <script src="handler.js"></script>
</head>
<body>
    <form name = "inputform" id="inputform" action = "<?php $_PHP_SELF ?>" method = "GET">
        UserInput: <input type = "text" name = "userInput" /><br>
        <input type = "submit" id = "submitButton" />
    </form>
    Renito ANSWER: <label id ="answer">-</label>
    <br>
    <form name = "teachform" id="teachform" action = "<?php $_PHP_SELF ?>" method = "POST">
        <label>Intent:</label><input id="intent" type="text" name="intent"><br><br>
        <label>Regexes:</label><input id="regexes" type="text" name="regexes"><br><br>
        <label>Replies:</label><input id="replies" type="text" name="replies"> 
        <input type = "submit" id = "submitButton" /><br>
    </form>
</body>
</html>

<?php
    $base_url = 'https://python-nlp-chatbot.herokuapp.com/';

/*
   if( $_GET["userInput"]) {
    //echo nl2br("\r\nBodoh!\r\n");
   }*/

    if( $_POST["intent"] && $_POST["regexes"] && $_POST["replies"] ) {
        //intent:
        //echo $_POST["intent"];

        //for regexes:
        $data = $_POST["regexes"];
        $data_arr = explode(',', $data); // <----- explode the string here from commas
        // Now you can store these values into the database
        //echo '<pre>'; print_r($data_arr); echo '</pre>';

        //for replies:
        $data = $_POST["replies"];
        $data_arr2 = explode(',', $data); // <----- explode the string here from commas
        // Now you can store these values into the database
        //echo '<pre>'; print_r($data_arr2); echo '</pre>';
        
        $intentQueryURL = $base_url.'query/'.urlencode($_POST["intent"]);
        //echo nl2br("$intentQueryURL\r\n");
        $intentFound = file_get_contents($intentQueryURL);
        //echo $intentFound;

        if ($intentFound == "true\n"){
            echo nl2br("Menambah ke existing diction! DONE!");
            $finalData["newRegexes"] = $data_arr;
            $finalData["newReplies"] = $data_arr2;
            $jsonData = json_encode($finalData);
            //echo nl2br("$jsonData\r\n");

            //sending put request:
            //The URL that we want to send a PUT request to.
            //$url = $base_url.'api/'.urlencode($_POST["intent"]);
            
            //Initiate cURL   
            $ch = curl_init();
            curl_setopt($ch, CURLOPT_URL, $base_url.'api/'.urlencode($_POST["intent"]));
            curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/json','Content-Length: ' . strlen($jsonData)));
            curl_setopt($ch, CURLOPT_CUSTOMREQUEST, 'PUT');
            curl_setopt($ch, CURLOPT_POSTFIELDS,$jsonData);
            curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
            $response  = curl_exec($ch);
            curl_close($ch);
            //echo $response;
        }
        else{
            echo nl2br("\r\nNew diksi! LEARNED!\r\n");
            $newIntentStrat["intent"] = $_POST["intent"];
            $newIntentStrat["regexes"] = $data_arr;
            $jsonIntentStrat= json_encode($newIntentStrat);
            $newReplyStrat["intent"] = $_POST["intent"];
            $newReplyStrat["replies"] = $data_arr2;
            $jsonReplyStrat= json_encode($newReplyStrat);
            //echo nl2br("$jsonIntentStrat\r\n");
            //echo nl2br("$jsonReplyStrat\r\n");

            //post intent strat:
            $ch = curl_init();
            curl_setopt($ch, CURLOPT_URL, $base_url.'api/intentStrategy');
            curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/json'));
            curl_setopt($ch, CURLOPT_POST, 1);
            curl_setopt($ch, CURLOPT_POSTFIELDS,$jsonIntentStrat);
            curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
            $response  = curl_exec($ch);
            curl_close($ch);

            //post reply strat: 
            $ch = curl_init();
            curl_setopt($ch, CURLOPT_URL, $base_url.'api/replyStrategy');
            curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/json'));
            curl_setopt($ch, CURLOPT_POST, 1);
            curl_setopt($ch, CURLOPT_POSTFIELDS,$jsonReplyStrat);
            curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
            $response  = curl_exec($ch);
            curl_close($ch);

        }
    }
?>

