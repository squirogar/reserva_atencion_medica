$(document).ajaxStart(function(){
    document.getElementById("loadingEmail").style.display = "block"; //display:block
    document.getElementById("btnGuardarEmail").disabled = true;

});

$(document).ajaxStop(function(){
    document.getElementById("loadingEmail").style.display = "none";//$('#loadingEmail').hide(); //display:none
    document.getElementById("btnGuardarEmail").disabled = false;
});



//

$(document).ready(function () {
    
    // formulario cambio email
    $('#formCambiaEmail').submit(function (e) {
        e.preventDefault();
        const formData = $("#formCambiaEmail").serialize(); //para que pueda enviarse al servidor
        
        limpiaMensajeEmail();
        //document.getElementById("divMensajeEmail").textContent = "";
        
        $.ajax({
            url: cambiaEmailUrl, //"{% url 'usr:cambia_email' %}"
            type: "post",
            data: formData,
            dataType: 'json',
            success: function (response) {
                
                const divMensaje = document.getElementById("divMensajeEmail");
                const parrafo = document.createElement("p");
                let mensaje = null;
                let color = null;

                if (response["cambio_efectivo"]) {
                    //insertar dentro de la modal el mensaje de exito
                    mensaje = document.createTextNode("Éxito"); 
                    
                    //reemplazar los datos por la nueva data
                    document.getElementById("email").textContent = response["datos"]["email"];

                    color = "blue";


                } else {
                    //insertar dentro de la modal el mensaje de fracaso
                    mensaje = document.createTextNode(response["mensaje"]["email"][0]); 
                
                    color = "red";
                }
                

                parrafo.appendChild(mensaje);
                parrafo.style.color = color;
                divMensajeEmail.appendChild(parrafo);//agrega el mensaje al div dentro de la modal
                


                // Cerrar el modal
                //$("#emailModal").modal('hide');


            },
            error : function(jqXHR, status, error) {
                alert('Disculpe, ocurrió un problema');
            }, 
        });

    });

});



function limpiaMensajeEmail() {
    document.getElementById("divMensajeEmail").textContent = "";
}