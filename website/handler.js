$( document ).ready(function() {
    $("form#teachform input").toggle();
    $("form#teachform label").toggle();
});


$(document).ready(function() {
    $("#inputform").submit(function(e) {
        $('#answer').text("loading");
        // Serialize the data in the form
        var serializedData = $("#inputform").serialize();
        //alert(serializedData);
        e.preventDefault();
        let urltxt = 'https://python-nlp-chatbot.herokuapp.com/api/'+$('form').serializeArray()[0].value;
        //alert(urltxt);
        $.ajax({                
            url: encodeURI(urltxt), 
            type: 'GET',
            cache: true,
            crossDomain: true,
            headers: {
                'Access-Control-Allow-Origin': '*'
            },
            success: function(data)
            {   
                //alert(data);
                $('#answer').text(JSON.stringify(data));
            },
            error: function(jqXHR, data, errorThrown ){
                //alert("jqXHR = "+JSON.stringify(jqXHR));
                //alert("data = "+JSON.stringify(data));
                //alert("errorThrown = "+JSON.stringify(errorThrown));

                //TEACHING BEGINS:
                $('#answer').text("Aku gak ngerti...");
                $.ajax({                
                    url: encodeURI('http://localhost:8000/index.php'), 
                    type: 'GET',
                    cache: true,
                    data: serializedData,
                    crossDomain: true,
                    headers: {
                        'Access-Control-Allow-Origin': '*'
                    },
                    success: function(data)
                    {   
                        $("form#teachform input").toggle();
                        $("form#teachform label").toggle();
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
        $("form#teachform input").toggle();
        $("form#teachform label").toggle();
        alert("Thanks udah ajarin aku <3");
    })
});