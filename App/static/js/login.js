async function butConfirmarCadUsuario(){
    let formData = new FormData(document.querySelector('#formcadusuario'));
    url = '/add/usuario';
    console.log(url);
    var mybody = {method:'POST', body:formData };

    let response = await fetch(url,mybody);
    if (response.ok) {

    }
}