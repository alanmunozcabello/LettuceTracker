import { api } from './api.js';

// Notificación Toast
function mostrarToast(mensaje, tipo = 'success') {
    const container = document.getElementById('toast-container');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = `toast toast-${tipo}`;
    toast.innerHTML = `
        <span style="font-size: 1.1rem;">${tipo === 'success' ? '✅' : '⚠️'}</span>
        <span>${mensaje}</span>
    `;
    container.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(8px)';
        toast.style.transition = 'all 0.25s ease';
        setTimeout(() => toast.remove(), 250);
    }, 4500);
}

// Sesión de usuario
async function inicializarSesion() {
    try {
        const sesion = await api.getSesion();
        if (sesion && sesion.usuario) {
            const u = sesion.usuario;
            const nombre = u.nombre || 'Usuario';
            const iniciales = nombre.split(' ').map(p => p[0]).slice(0, 2).join('').toUpperCase() || 'U';

            const userAvatar = document.querySelector('.user-avatar');
            const userName = document.querySelector('.user-name');
            const userRole = document.querySelector('.user-role');

            if (userAvatar) userAvatar.textContent = iniciales;
            if (userName) userName.textContent = nombre;
            if (userRole) userRole.textContent = u.email || 'Estudiante / Miembro';
        }
    } catch (e) {
        window.location.replace('/static/html/login.html');
    }
}

// Nombre de estudiante por ID
function obtenerNombreEstudiante(idUsuario) {
    if (idUsuario === 'USR001') return 'Nicolas Urbina';
    if (idUsuario === 'USR002') return 'Cristian Aliaga';
    if (idUsuario === 'USR003') return 'Alan Muñoz';
    return idUsuario;
}

// Nombre de curso por ID
function obtenerNombreCurso(idCurso) {
    if (idCurso === 'CUR001') return 'Diseño de Software (2026-2)';
    if (idCurso === 'CUR002') return 'Ingeniería de Software (2026-2)';
    return idCurso;
}

// Cargar lista de matrículas
async function cargarMatriculas(filtros = {}) {
    const tbody = document.getElementById('matriculas-tbody');
    const emptyState = document.getElementById('matriculas-empty');
    const contador = document.getElementById('matriculas-contador');
    if (!tbody) return;

    try {
        const matriculas = await api.listarMatriculas(filtros);
        tbody.innerHTML = '';

        if (!matriculas || matriculas.length === 0) {
            if (emptyState) emptyState.style.display = 'block';
            if (contador) contador.textContent = '0 matrículas encontradas';
            return;
        }

        if (emptyState) emptyState.style.display = 'none';
        if (contador) contador.textContent = `${matriculas.length} matrícula(s) registradas`;

        matriculas.forEach(m => {
            const nombreEstudiante = obtenerNombreEstudiante(m.id_usuario);
            const nombreCurso = obtenerNombreCurso(m.id_curso);
            const fechaStr = m.fecha ? new Date(m.fecha).toLocaleString() : 'Reciente';

            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td><code>${m.id_matricula}</code></td>
                <td>
                    <div class="assignee-badge">
                        <span class="assignee-avatar">${m.id_usuario.substring(0, 3)}</span>
                        <span>${nombreEstudiante} <span class="assignee-role">(${m.id_usuario})</span></span>
                    </div>
                </td>
                <td>
                    <span class="badge badge-blue">${nombreCurso}</span>
                </td>
                <td>${fechaStr}</td>
                <td style="text-align: center;">
                    <span class="status-pill status-completed">Inscrito</span>
                </td>
            `;
            tbody.appendChild(tr);
        });

    } catch (err) {
        console.error('Error al listar matrículas:', err);
        mostrarToast(err.message, 'error');
    }
}

// Formulario de matrícula
function setupFormularioMatricula() {
    const form = document.getElementById('form-matricular');
    if (!form) return;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const idUsuario = document.getElementById('matricula-usuario').value;
        const idCurso = document.getElementById('matricula-curso').value;

        if (!idUsuario || !idCurso) {
            mostrarToast('Por favor selecciona tanto el estudiante como el curso.', 'error');
            return;
        }

        const btnSubmit = form.querySelector('button[type="submit"]');
        btnSubmit.disabled = true;
        btnSubmit.textContent = 'Procesando Matrícula...';

        try {
            const matricula = await api.matricularEstudiante({
                id_usuario: idUsuario,
                id_curso: idCurso
            });

            mostrarToast(`¡Matrícula exitosa! Código generado: ${matricula.id_matricula}`);
            form.reset();
            await cargarMatriculas();
        } catch (err) {
            mostrarToast(err.message || 'Error al matricular estudiante', 'error');
        } finally {
            btnSubmit.disabled = false;
            btnSubmit.textContent = 'Registrar Matrícula';
        }
    });
}

// Filtros y búsqueda
function setupFiltros() {
    const filtroEstudiante = document.getElementById('filtro-estudiante');
    const filtroCurso = document.getElementById('filtro-curso');
    const btnLimpiar = document.getElementById('btn-limpiar-filtros');

    const aplicarFiltros = () => {
        const id_usuario = filtroEstudiante.value || undefined;
        const id_curso = filtroCurso.value || undefined;
        cargarMatriculas({ id_usuario, id_curso });
    };

    if (filtroEstudiante) filtroEstudiante.addEventListener('change', aplicarFiltros);
    if (filtroCurso) filtroCurso.addEventListener('change', aplicarFiltros);

    if (btnLimpiar) {
        btnLimpiar.addEventListener('click', () => {
            if (filtroEstudiante) filtroEstudiante.value = '';
            if (filtroCurso) filtroCurso.value = '';
            cargarMatriculas();
        });
    }

    // Buscar por código
    const formBuscar = document.getElementById('form-buscar-matricula');
    if (formBuscar) {
        formBuscar.addEventListener('submit', async (e) => {
            e.preventDefault();
            const inputId = document.getElementById('buscar-matricula-id');
            const idMatricula = inputId ? inputId.value.trim() : '';

            if (!idMatricula) {
                await cargarMatriculas();
                return;
            }

            try {
                const res = await api.consultarMatricula(idMatricula);
                mostrarToast(`Matrícula encontrada: ${res.id_matricula}`);

                const tbody = document.getElementById('matriculas-tbody');
                const emptyState = document.getElementById('matriculas-empty');
                const contador = document.getElementById('matriculas-contador');

                if (emptyState) emptyState.style.display = 'none';
                if (contador) contador.textContent = '1 matrícula encontrada';
                if (tbody) {
                    tbody.innerHTML = `
                        <tr>
                            <td><code>${res.id_matricula}</code></td>
                            <td>
                                <div class="assignee-badge">
                                    <span class="assignee-avatar">${res.id_usuario.substring(0, 3)}</span>
                                    <span>${obtenerNombreEstudiante(res.id_usuario)} <span class="assignee-role">(${res.id_usuario})</span></span>
                                </div>
                            </td>
                            <td>
                                <span class="badge badge-blue">${obtenerNombreCurso(res.id_curso)}</span>
                            </td>
                            <td>${res.fecha ? new Date(res.fecha).toLocaleString() : 'Reciente'}</td>
                            <td style="text-align: center;">
                                <span class="status-pill status-completed">Inscrito</span>
                            </td>
                        </tr>
                    `;
                }
            } catch (err) {
                mostrarToast(err.message, 'error');
            }
        });
    }
}

// Cerrar sesión
function setupLogout() {
    const logoutBtn = document.getElementById('logout-link');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', async (e) => {
            e.preventDefault();
            await api.logout();
            window.location.replace('/static/html/login.html');
        });
    }
}

// Inicio
window.addEventListener('DOMContentLoaded', async () => {
    await inicializarSesion();
    setupFormularioMatricula();
    setupFiltros();
    setupLogout();
    await cargarMatriculas();
});
