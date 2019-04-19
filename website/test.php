<?php
   function getRequest($userInput){
      // Get cURL resource
      $curl = curl_init();
      echo 'https://python-nlp-chatbot.herokuapp.com/api/'.$userInput;
      echo "<br>";
      // Set some options - we are passing in a useragent too here
      curl_setopt_array($curl, [
         CURLOPT_RETURNTRANSFER => 1,
         CURLOPT_URL => 'https://python-nlp-chatbot.herokuapp.com/api/'.urlencode($userInput), //urlencode to parse spaces in url
         CURLOPT_USERAGENT => 'Get request!'
      ]);
      // Send the request & save response to $resp
      $resp = curl_exec($curl);
      // Close request to clear up some resources
      curl_close($curl);
      return $resp;
   }

   if( $_GET["userInput"]) {
      echo nl2br("Bodoh!\r\n");
      /*echo nl2br("Request received!\r\n"); #nlbr: new line to break <br>
      $respond = getRequest($_GET["userInput"]);
      echo nl2br("RENITOBOT: $respond \r\n");
      */
      //exit();
   }
?>
<html>
   <body>
      <form action = "<?php $_PHP_SELF ?>" method = "GET">
         UserInput: <input type = "text" name = "userInput" /><br>
         <input type = "submit" id = "submitButton" />
      </form>
   </body>
</html>