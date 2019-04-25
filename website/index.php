<!doctype html>
<html>
<head>
    <title>RenitoBot</title>
    <script src="jquery.js"></script> <!--include this first! or jquery won't work!-->
    <script src="handler.js"></script>
    <link href="style.css" rel="stylesheet" />
</head>
<body>
    <form name = "inputform" id="inputform" action = "<?php $_PHP_SELF ?>" method = "GET">
        <div class = "Bot">
			<img class = "square" src="resource/renito.png" />
		</div>
		
		<div class = "Chatbox" >
			<div class = "Dialog" id ="Dialog">
                <span style="float: left">You:</span><br>
                <span style="float: left">Where am I?</span><br>
                <span style="float: right">RenitoBot:</span><br>
                <span style="float: right">HEY LO, I'm Renito yo! Salam kenal yo, sini sama aku yo!</span><br>
                
            </div>
            <label class = "inputLabel">UserInput: </label><input class= "inputBox" style="width:325px;height:50px" type = "text" name = "userInput" /><br>
            <input class = "submitButton" type = "submit" id = "submitButton" />
        </div>
		
	<div class = "wrapper">
	    <label>Which Algorithm:</label>
	    <input list="algo" type="text" id="algopick">
	    <datalist id="algo">
	        <option value="regex"> </option>
	        <option value="kmp"> </option>
	        <option value="bm"> </option>
	    </datalist>

        <br><br>
	    
	       
	        
	    </form>
	    Renito ANSWER: <label id ="answer">-</label>
	    <br>
        <form name = "teachform" id="teachform" action = "<?php $_PHP_SELF ?>" method = "POST">
            <label><h2 id ="answer" style="font-size : 50px>" > RENITO'S TEACHING SESSION <br> BEGINS:</h1><br> </label>
	        <label>Intent:</label><input id="intent" type="text" name="intent" value=""><br><br>
	        <label id ="regexlabel">Regexes:</label><input id="regexes" type="text" name="regexes"><br><br>
	        <label id ="patternlabel">Patterns:</label><input id="patterns" type="text" name="patterns" value=""><br><br>
	        <label>Replies:</label><input id="replies" type="text" name="replies"> 
	        <input type = "submit" id = "submitButton" /><br>
	    </form>
	</div>
</body>
</html>

<?php
    $base_url = 'https://python-nlp-chatbot.herokuapp.com/';

/*
   if( $_GET["userInput"]) {
    //echo nl2br("\r\nBodoh!\r\n");
   }*/

    if( $_POST["intent"] && $_POST["regexes"] || $_POST["patterns"]  && $_POST["replies"] ) {
        //intent:
        //echo $_POST["intent"];
        if($_POST["patterns"] == "")
            $isRegex = 1;
        else
            $isRegex = 0;
        //for patterns:
        $data = $_POST["patterns"];
        $data_arr0 = explode(',', $data); // explode the string from commas

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
        echo nl2br("$intentQueryURL\r\n");
        $intentFound = file_get_contents($intentQueryURL);
        //echo $intentFound;
        
        

        if ($intentFound == "true\n"){
            echo nl2br("Menambah ke existing diction! DONE!");
            if($isRegex == 1){
                //untuk dict1:
                $finalData["newRegexes"] = $data_arr;
                $finalData["newReplies"] = $data_arr2;
                $jsonData = json_encode($finalData);
                //which url to update:
                $putURL = $base_url.'api/regex/'.urlencode($_POST["intent"]);
            }
            else{
                //untuk dict2:
                $finalData["newPatterns"] = $data_arr0;
                $finalData["newReplies"] = $data_arr2;
                $jsonData = json_encode($finalData);
                //echo nl2br("$jsonData\r\n");
                //which url to update:
                $putURL = $base_url.'api/pattern/'.urlencode($_POST["intent"]);
            }

            //sending put request:
            //The URL that we want to send a PUT request to.
            //$url = $base_url.'api/'.urlencode($_POST["intent"]);
            
            //Initiate cURL   
            $ch = curl_init();
            curl_setopt($ch, CURLOPT_URL, $putURL);
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
            //echo '<pre>'; print_r($data_arr0); echo '</pre>';
            //echo empty($data_arr0);
            //echo empty($data_arr0) == true;
            if($isRegex == 1){
                //echo nl2br("entered here: REGEX");
                $newIntentStrat["intent"] = $_POST["intent"];
                $newIntentStrat["regexes"] = $data_arr;
                $jsonIntentStrat= json_encode($newIntentStrat);
                $post_URL='api/post/intentStrategy';
            }
            else{
                //echo nl2br("entered here: BM/KMP");
                $newIntentStrat["intent"] = $_POST["intent"];
                $newIntentStrat["patterns"] = $data_arr0;
                $jsonIntentStrat= json_encode($newIntentStrat);
                $post_URL='api/post/intentStrategy2';
            }
            $newReplyStrat["intent"] = $_POST["intent"];
            $newReplyStrat["replies"] = $data_arr2;
            $jsonReplyStrat= json_encode($newReplyStrat);
            //echo nl2br("$jsonIntentStrat\r\n");
            //echo nl2br("$jsonReplyStrat\r\n");

            //post intent strat:
            $ch = curl_init();
            curl_setopt($ch, CURLOPT_URL, $base_url.$post_URL);
            curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/json'));
            curl_setopt($ch, CURLOPT_POST, 1);
            curl_setopt($ch, CURLOPT_POSTFIELDS,$jsonIntentStrat);
            curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
            $response  = curl_exec($ch);
            curl_close($ch);

            //post reply strat: 
            $ch = curl_init();
            curl_setopt($ch, CURLOPT_URL, $base_url.'api/post/replyStrategy');
            curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/json'));
            curl_setopt($ch, CURLOPT_POST, 1);
            curl_setopt($ch, CURLOPT_POSTFIELDS,$jsonReplyStrat);
            curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
            $response  = curl_exec($ch);
            curl_close($ch);

        }
    }
?>

