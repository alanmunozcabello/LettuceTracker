import { api } from './api.js';

// Estado global de la vista
let proyectoActivo = {
    id: 'PRY001',
    nombre: 'Lettuce Tracker',
    descripcion: 'Gestión Documental de Proyectos — Universidad de Talca',
    estado: 'Activo'
};

let usuarioSesion = null;

// Clases de color para roles
function obtenerClaseBadge(rol) {
    switch (rol) {
        case 'Líder de Proyecto':
            return 'badge-amber';
        case 'Desarrollador':
            return 'badge-blue';
        case 'Tester':
            return 'badge-indigo';
        case 'Arquitecto':
            return 'badge-emerald';
        case 'Documentador':
            return 'badge-purple';
        default:
            return 'badge-blue';
    }
}

// Actualiza el rol en la interfaz (tabla de miembros y tabla de tareas)
function actualizarRolEnInterfaz(idUsuario, rol) {
    // 1. Actualizar badge en la tabla de miembros
    const badge = document.querySelector(`[data-member-role="${idUsuario}"]`);
    if (badge) {
        badge.textContent = rol;
        badge.className = `badge ${obtenerClaseBadge(rol)}`;
    }

    // 2. Actualizar texto de rol en la tabla de tareas
    const taskRole = document.querySelector(`[data-assignee-role="${idUsuario}"]`);
    if (taskRole) {
        taskRole.textContent = `(${rol})`;
    }

    // 3. Si el usuario actual es el logueado, actualizar el navbar
    if (usuarioSesion && usuarioSesion.id === idUsuario) {
        const userRole = document.querySelector('.user-role');
        if (userRole) {
            userRole.textContent = rol;
        }
    }
}

// Sincroniza los roles reales de los miembros consultando al backend
async function sincronizarMiembrosProyecto(idPry) {
    const usuarios = ['USR001', 'USR002', 'USR003'];
    for (const idUsuario of usuarios) {
        try {
            const m = await api.consultarMiembro(idPry, idUsuario);
            if (m && m.rol) {
                actualizarRolEnInterfaz(m.id_usuario, m.rol);
            }
        } catch (e) {
            // No asignado a este proyecto
        }
    }
}

// Utilidad para notificaciones Toast
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
    }, 4000);
}

// Inicializar y validar sesión
async function inicializarSesion() {
    try {
        const sesion = await api.getSesion();
        if (sesion && sesion.usuario) {
            usuarioSesion = sesion.usuario;
            const nombre = usuarioSesion.nombre || 'Usuario';
            const iniciales = nombre.split(' ').map(p => p[0]).slice(0, 2).join('').toUpperCase() || 'U';
            
            const userAvatar = document.querySelector('.user-avatar');
            const userName = document.querySelector('.user-name');
            const userRole = document.querySelector('.user-role');

            if (userAvatar) userAvatar.textContent = iniciales;
            if (userName) userName.textContent = nombre;
            if (userRole) userRole.textContent = usuarioSesion.email || 'Miembro';
        }
    } catch (e) {
        window.location.replace('/static/html/login.html');
    }
}

// Cargar datos de un proyecto
async function cargarProyecto(idProyecto) {
    try {
        const p = await api.consultarProyecto(idProyecto);
        proyectoActivo = p;
        actualizarVistaProyecto();
        await sincronizarMiembrosProyecto(proyectoActivo.id);
        mostrarToast(`Proyecto '${p.nombre}' cargado con éxito.`);
    } catch (e) {
        mostrarToast(e.message || 'Error al consultar proyecto', 'error');
    }
}

function actualizarVistaProyecto() {
    const elTitulo = document.getElementById('project-title');
    const elId = document.getElementById('project-id-badge');
    const elDesc = document.getElementById('project-desc');
    const elEstado = document.getElementById('project-status-badge');

    if (elTitulo) elTitulo.textContent = proyectoActivo.nombre || proyectoActivo.id;
    if (elId) elId.textContent = `ID: ${proyectoActivo.id}`;
    if (elDesc) elDesc.textContent = proyectoActivo.descripcion || 'Sin descripción';
    if (elEstado) elEstado.textContent = proyectoActivo.estado || 'Activo';
}

// Manejo de Modales
function setupModals() {
    // Abrir modales
    document.querySelectorAll('[data-open-modal]').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const modalId = btn.getAttribute('data-open-modal');
            const modal = document.getElementById(modalId);
            if (modal) {
                // Pre-rellenar id de proyecto si aplica
                const inputPry = modal.querySelector('[data-prefill-project]');
                if (inputPry) inputPry.value = proyectoActivo.id;
                modal.classList.add('active');
            }
        });
    });

    // Cerrar modales
    document.querySelectorAll('.modal-backdrop, .modal-close-btn, [data-close-modal]').forEach(el => {
        el.addEventListener('click', (e) => {
            if (e.target === el || el.classList.contains('modal-close-btn') || el.hasAttribute('data-close-modal')) {
                const modal = el.closest('.modal-backdrop');
                if (modal) modal.classList.remove('active');
            }
        });
    });

    // Formulario Crear Proyecto
    const formCrearPry = document.getElementById('form-crear-proyecto');
    if (formCrearPry) {
        formCrearPry.addEventListener('submit', async (e) => {
            e.preventDefault();
            const id = document.getElementById('crear-pry-id').value.trim();
            const nombre = document.getElementById('crear-pry-nombre').value.trim();
            const descripcion = document.getElementById('crear-pry-desc').value.trim();

            const btnSubmit = formCrearPry.querySelector('button[type="submit"]');
            btnSubmit.disabled = true;
            btnSubmit.textContent = 'Creando...';

            try {
                const nuevoPry = await api.crearProyecto({ id, nombre, descripcion });
                mostrarToast(`¡Proyecto '${nuevoPry.nombre}' creado exitosamente!`);
                formCrearPry.reset();
                formCrearPry.closest('.modal-backdrop').classList.remove('active');
                proyectoActivo = nuevoPry;
                actualizarVistaProyecto();
                await sincronizarMiembrosProyecto(proyectoActivo.id);
            } catch (err) {
                mostrarToast(err.message, 'error');
            } finally {
                btnSubmit.disabled = false;
                btnSubmit.textContent = 'Guardar Proyecto';
            }
        });
    }

    // Formulario Buscar Proyecto
    const formBuscarPry = document.getElementById('form-buscar-proyecto');
    if (formBuscarPry) {
        formBuscarPry.addEventListener('submit', async (e) => {
            e.preventDefault();
            const id = document.getElementById('buscar-pry-id').value.trim();
            const btnSubmit = formBuscarPry.querySelector('button[type="submit"]');
            btnSubmit.disabled = true;
            btnSubmit.textContent = 'Buscando...';

            try {
                await cargarProyecto(id);
                formBuscarPry.closest('.modal-backdrop').classList.remove('active');
            } catch (err) {
                mostrarToast(err.message, 'error');
            } finally {
                btnSubmit.disabled = false;
                btnSubmit.textContent = 'Consultar';
            }
        });
    }

    // Formulario Asignar Miembro
    const formAsignarMiembro = document.getElementById('form-asignar-miembro');
    if (formAsignarMiembro) {
        formAsignarMiembro.addEventListener('submit', async (e) => {
            e.preventDefault();
            const idPry = document.getElementById('asignar-id-proyecto').value.trim();
            const idUsuario = document.getElementById('asignar-id-usuario').value.trim();
            const rol = document.getElementById('asignar-rol').value;

            const btnSubmit = formAsignarMiembro.querySelector('button[type="submit"]');
            btnSubmit.disabled = true;
            btnSubmit.textContent = 'Guardando...';

            try {
                const miembro = await api.asignarMiembro(idPry, { id_usuario: idUsuario, rol });
                // Actualizar inmediatamente la fila en la tabla y en las tareas
                actualizarRolEnInterfaz(miembro.id_usuario, miembro.rol);
                mostrarToast(`¡Rol actualizado! ${miembro.id_usuario} es ahora '${miembro.rol}'.`);
                formAsignarMiembro.reset();
                formAsignarMiembro.closest('.modal-backdrop').classList.remove('active');
            } catch (err) {
                mostrarToast(err.message, 'error');
            } finally {
                btnSubmit.disabled = false;
                btnSubmit.textContent = 'Asignar Miembro';
            }
        });
    }

    // Formulario Consultar Miembro
    const formConsultarMiembro = document.getElementById('form-consultar-miembro');
    const resultadoMiembro = document.getElementById('resultado-consultar-miembro');
    if (formConsultarMiembro) {
        formConsultarMiembro.addEventListener('submit', async (e) => {
            e.preventDefault();
            const idPry = document.getElementById('consultar-mbr-proyecto').value.trim();
            const idUsuario = document.getElementById('consultar-mbr-usuario').value.trim();

            const btnSubmit = formConsultarMiembro.querySelector('button[type="submit"]');
            btnSubmit.disabled = true;
            btnSubmit.textContent = 'Consultando...';

            try {
                const res = await api.consultarMiembro(idPry, idUsuario);
                resultadoMiembro.style.display = 'block';
                resultadoMiembro.innerHTML = `
                    <div style="background-color: var(--color-slate-50); border: 1px solid var(--color-slate-200); border-radius: var(--radius-md); padding: 1rem; margin-top: 1rem;">
                        <div style="font-weight: 700; color: var(--color-slate-900); font-size: 0.875rem;">Miembro Encontrado</div>
                        <div style="font-size: 0.8125rem; color: var(--color-slate-600); margin-top: 0.35rem;">
                            <strong>ID Miembro:</strong> ${res.id_miembro}<br>
                            <strong>Usuario:</strong> ${res.id_usuario}<br>
                            <strong>Proyecto:</strong> ${res.id_proyecto}<br>
                            <strong>Rol Asignado:</strong> <span class="badge ${obtenerClaseBadge(res.rol)}" style="margin-left: 0.25rem;">${res.rol}</span>
                        </div>
                    </div>
                `;
            } catch (err) {
                resultadoMiembro.style.display = 'block';
                resultadoMiembro.innerHTML = `
                    <div style="background-color: var(--color-rose-50); border: 1px solid var(--color-rose-200); border-radius: var(--radius-md); padding: 1rem; margin-top: 1rem; color: var(--color-rose-700); font-size: 0.8125rem;">
                        ⚠️ ${err.message}
                    </div>
                `;
            } finally {
                btnSubmit.disabled = false;
                btnSubmit.textContent = 'Verificar';
            }
        });
    }
}

// Evento de Logout
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

// Inicialización general al cargar el DOM
window.addEventListener('DOMContentLoaded', async () => {
    await inicializarSesion();
    setupModals();
    setupLogout();
    
    // Consultar el proyecto inicial y sincronizar roles guardados en el backend
    try {
        const p = await api.consultarProyecto('PRY001');
        proyectoActivo = p;
        actualizarVistaProyecto();
    } catch (e) {
        actualizarVistaProyecto();
    }

    // Sincronizar los roles reales guardados en miembros.json
    await sincronizarMiembrosProyecto(proyectoActivo.id);
});
