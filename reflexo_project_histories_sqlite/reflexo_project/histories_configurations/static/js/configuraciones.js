async function cargarConfiguraciones() {
    await cargarDocumentos();
    await cargarPagos();
}

async function cargarDocumentos() {
    const response = await fetch('/document_types/');
    const data = await response.json();
    const lista = document.getElementById('lista-documentos');
    lista.innerHTML = '';
    data.forEach(doc => {
        lista.innerHTML += `<li>${doc.nombre} 
            <button onclick="eliminarDocumento(${doc.id})">X</button></li>`;
    });
}

async function agregarDocumento() {
    const valor = document.getElementById('nuevo-documento').value;
    await fetch('/document_types/create/', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({nombre: valor})
    });
    cargarDocumentos();
}
