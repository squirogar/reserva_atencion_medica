$(document).ajaxStart(function(){
    console.log("muestra")
    document.getElementById("loadingEmail").style.display = "block"; //display:block
    document.getElementById("btnGuardarEmail").disabled = true;

});

$(document).ajaxStop(function(){
    console.log("oculta")
    document.getElementById("loadingEmail").style.display = "none";//$('#loadingEmail').hide(); //display:none
    document.getElementById("btnGuardarEmail").disabled = false;
});



//

$(document).ready(function () {
    
    // formulario cambio email
    $('#formCambiaEmail').submit(function (e) {
        e.preventDefault();
        const formData = $("#formCambiaEmail").serialize(); //para que pueda enviarse al servidor
        
        $.ajax({
            url: cambiaEmailUrl, //"{% url 'usr:cambia_email' %}"
            type: "post",
            data: formData,
            dataType: 'json',
            success: function (response) {
                console.log("success");
                

                
                const divMensaje = document.getElementById("divMensaje");
                const parrafo = document.createElement("p");
                let mensaje = null;

                if (response["cambio_efectivo"]) {
                    //insertar dentro de la modal el mensaje de exito
                    mensaje = document.createTextNode("Éxito"); 
                    
                    //reemplazar los datos por la nueva data
                    document.getElementById("email").textContent = response["datos"]["email"];


                } else {
                    //insertar dentro de la modal el mensaje de fracaso
                    mensaje = document.createTextNode(response["mensaje"]["email"][0]); 
                
                }
                
                divMensaje.textContent = ""; //limpia el contenido anterior

                parrafo.appendChild(mensaje);
                divMensaje.appendChild(parrafo);//agrega el mensaje al div dentro de la modal
                


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



function limpiaMensaje() {
    document.getElementById("divMensaje").textContent = "";
}