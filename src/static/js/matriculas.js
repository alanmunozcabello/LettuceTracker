import { api } from './api.js';

// Historial local de matrículas realizadas en esta sesión
const historialMatriculas = [];

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

function renderizarTablaMatriculas() {
    const tbody = document.getElementById('matriculas-tbody');
    const emptyState = document.getElementById('matriculas-empty');
    if (!tbody) return;

    tbody.innerHTML = '';

    if (historialMatriculas.length === 0) {
        if (emptyState) emptyState.style.display = 'block';
        return;
    }

    if (emptyState) emptyState.style.display = 'none';

    historialMatriculas.forEach(m => {
        const tr = document.createElement('tr');
        
        let nombreEstudiante = m.id_usuario;
        if (m.id_usuario === 'USR001') nombreEstudiante = 'Nicolas Urbina';
        else if (m.id_usuario === 'USR002') nombreEstudiante = 'Cristian Aliaga';
        else if (m.id_usuario === 'USR003') nombreEstudiante = 'Alan Muñoz';

        let nombreCurso = m.id_curso;
        if (m.id_curso === 'CUR001') nombreCurso = 'Diseño de Software (2026-2)';
        else if (m.id_curso === 'CUR002') nombreCurso = 'Ingeniería de Software (2026-2)';

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
            <td>${new Date(m.fecha).toLocaleString()}</td>
            <td style="text-align: center;">
                <span class="status-pill status-completed">Inscrito</span>
            </td>
        `;
        tbody.appendChild(tr);
    });

    const contador = document.getElementById('matriculas-contador');
    if (contador) {
        contador.textContent = `Mostrando ${historialMatriculas.length} matrícula(s) registradas`;
    }
}

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
            historialMatriculas.unshift(matricula);
            renderizarTablaMatriculas();
            form.reset();
        } catch (err) {
            mostrarToast(err.message || 'Error al matricular estudiante', 'error');
        } finally {
            btnSubmit.disabled = false;
            btnSubmit.textContent = 'Registrar Matrícula';
        }
    });
}

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

window.addEventListener('DOMContentLoaded', () => {
    inicializarSesion();
    setupFormularioMatricula();
    setupLogout();
    renderizarTablaMatriculas();
});
