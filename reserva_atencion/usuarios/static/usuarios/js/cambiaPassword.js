
$(document).ready(function () {
    
    // formulario cambio email
    $('#formCambiaPassword').submit(function (e) {
        e.preventDefault();
        let formData = $("#formCambiaPassword").serialize(); //para que pueda enviarse al servidor
    
        $.ajax({
            url: cambiaPasswordUrl, //"{% url 'usr:cambia_email' %}"
            type: "post",
            data: formData,
            dataType: 'json',
            success: function (response) {
                console.log("success");
                console.log(response, typeof response);

                if (!response["cambio_efectivo"]) {
                    //insertar dentro de la modal el mensaje de error
                    //response["mensaje"]
                } else {
                    //insertar dentro de la modal el mensaje de exito
                    //reemplazar los datos por la nueva data
                }
            


                // Cerrar el modal
                //$("#emailModal").modal('hide');


            },
            error : function(jqXHR, status, error) {
                alert('Disculpe, ocurrió un problema');
                console.error(status);
                console.error(error);
            }, 
        });

    });

});
