function test(){
    alert('hola mundo')
}

function jsAjax() {
    var urlHref = "/ajax";

    $.ajax({
        url: urlHref,
        type: 'POST',                         // Método HTTP: GET, POST, PUT, DELETE, etc.
        dataType: 'json',                     // Formato de datos esperado
        cache: false,
        processData: false, 
        contentType: false,
        success: function (cJSON){
            alert(cJSON.result);
        },
        error: function (obj, tipeError, Error){

        }
    });

}