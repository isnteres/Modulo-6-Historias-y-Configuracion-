async function cargarHistorias() {
    const response = await fetch('/histories/');
    const data = await response.json();
    const tbody = document.getElementById('tabla-historias');
    tbody.innerHTML = '';
    data.forEach(historia => {
        tbody.innerHTML += `
            <tr>
                <td>${historia.id}</td>
                <td>${historia.nombre}</td>
                <td>${historia.documento}</td>
                <td>
                    <button onclick="editarHistoria(${historia.id})">Editar</button>
                    <button onclick="eliminarHistoria(${historia.id})">Eliminar</button>
                </td>
            </tr>`;
    });
}

async function crearHistoria() {
    const nombre = document.getElementById('nombre').value;
    const documento = document.getElementById('documento').value;
    await fetch('/histories/create/', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({nombre, documento})
    });
    cargarHistorias();
}

async function eliminarHistoria(id) {
    await fetch(`/histories/${id}/delete/`, {method: 'DELETE'});
    cargarHistorias();
}
