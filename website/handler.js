$( document ).ready(function() {
    $("form#teachform input").hide();
    $("form#teachform label").hide();
});


$(document).ready(function() {
    $("#inputform").submit(function(e) {
        $('#answer').text("loading");
        // Algorithm type:
        var algotype = document.getElementById('algopick').value;
        //alert(algotype);
        // Serialize the data in the form
        var serializedData = $("#inputform").serialize();
        //alert(serializedData);
        e.preventDefault();
        let base_url = 'https://python-nlp-chatbot.herokuapp.com/api/'
        //alert(encodeURIComponent($('form').serializeArray()[0].value))
        $.ajax({                
            url: base_url+algotype+'/'+encodeURIComponent($('form').serializeArray()[0].value), 
            type: 'GET',
            cache: true,
            crossDomain: true,
            headers: {
                'Access-Control-Allow-Origin': '*'
            },
            success: function(data)
            {   
                //alert(data);
                $("form#teachform input").hide();
                $("form#teachform label").hide();
                $('#answer').text(JSON.stringify(data));
            },
            error: function(jqXHR, data, errorThrown ){
                //alert("jqXHR = "+JSON.stringify(jqXHR));
                //alert("data = "+JSON.stringify(data));
                //alert("errorThrown = "+JSON.stringify(errorThrown));

                //TEACHING BEGINS:
                $('#answer').text("Aku gak ngerti...");
                $.ajax({                
                    url: 'http://localhost:8000/index.php', 
                    type: 'GET',
                    cache: true,
                    data: serializedData,
                    crossDomain: true,
                    headers: {
                        'Access-Control-Allow-Origin': '*'
                    },
                    success: function(data)
                    {   
                        $("form#teachform input").show();
                        $("form#teachform label").show();
                        if(algotype == "regex"){
                            $("#patterns").hide();
                            $("#patternlabel").hide();
                        }
                        else{
                            $("#regexes").hide();
                            $("#regexlabel").hide();
                        }
                    },
                    error: function(jqXHR, data, errorThrown ){
                        //alert("jqXHR = "+JSON.stringify(jqXHR));
                        //alert("data = "+JSON.stringify(data));
                        //alert("errorThrown = "+JSON.stringify(errorThrown)); 
                        alert("failure calling teachNLP");       
                    }
                })      
            }
        });
    })
});

$(document).ready(function() {
    $("#teachform").submit(function(e) {
        $("form#teachform input").hide();
        $("form#teachform label").hide();
        alert("Thanks udah ajarin aku <3");
    })
});