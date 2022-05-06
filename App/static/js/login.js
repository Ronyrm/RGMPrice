async function butConfirmarCadUsuario(){
    let formData = new FormData(document.querySelector('#formcadusuario'));
    url = '/add/usuario';
    console.log(url);
    var mybody = {method:'POST', body:formData };

    let response = await fetch(url,mybody);
    if (response.ok) {
        let compalert = '<button type="button" class="btn-close" data-bs-dismiss="alert"'+
                        ' aria-label="Close"></button>';
        json = await response.json();
        console.log(json);
        
        let spanalert = document.querySelector('#alertcadusuario');
        spanalert.classList.remove('d-none');
        spanalert.innerHTML = json.mensagem + compalert;
        if (json.sucesso){      
            console.log('Sucesso'); 
            spanalert.classList.remove('alert-danger');
            spanalert.classList.add('alert-primary');
            
            // atribui o email cadastrado
            let usernameemail = document.querySelector('#usernameemail');
            usernameemail.value = json.email;
            
            $('#spanalert').fadeOut();
            setTimeout(function(){
                spanalert.classList.add('alert-danger');
                spanalert.classList.remove('alert-primary');
                spanalert.classList.add('d-none');
                document.querySelector('#btnfecharcadusuario').click();
                document.querySelector('#password').focus();
            }, 5000);
        }
        else{
            $('#spanalert').fadeOut();
            setTimeout(function(){
                spanalert.classList.add('d-none');
            }, 5000);
        }

    }
}   