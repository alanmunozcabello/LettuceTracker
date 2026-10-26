import { api } from './api.js';

// Estado global
let proyectoActivo = {
    id: 'PRY001',
    nombre: 'Lettuce Tracker',
    descripcion: 'Gestión Documental de Proyectos — Universidad de Talca',
    estado: 'Activo'
};

let listaProyectos = [];
let usuarioSesion = null;

// Color de badge por rol
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

// Nombre de usuario por ID
function obtenerNombreUsuario(idUsuario) {
    if (idUsuario === 'USR001') return 'Nicolas Urbina';
    if (idUsuario === 'USR002') return 'Cristian Aliaga';
    if (idUsuario === 'USR003') return 'Alan Muñoz';
    return idUsuario;
}

// Renderizar tabla de miembros
async function cargarMiembrosProyecto(idPry) {
    const tbody = document.getElementById('miembros-tbody');
    if (!tbody) return;

    try {
        const miembros = await api.listarMiembros(idPry);
        tbody.innerHTML = '';

        if (!miembros || miembros.length === 0) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="4" style="text-align: center; color: var(--color-slate-400); padding: 2rem;">
                        No hay miembros asignados a este proyecto todavía.
                    </td>
                </tr>
            `;
            return;
        }

        miembros.forEach(m => {
            const nombre = obtenerNombreUsuario(m.id_usuario);
            const iniciales = nombre.split(' ').map(p => p[0]).slice(0, 2).join('').toUpperCase();

            const tr = document.createElement('tr');
            tr.setAttribute('data-user-row', m.id_usuario);
            tr.innerHTML = `
                <td><code>${m.id_usuario}</code></td>
                <td>
                    <div class="assignee-badge">
                        <span class="assignee-avatar">${iniciales}</span>
                        <span>${nombre}</span>
                    </div>
                </td>
                <td>
                    <span class="badge ${obtenerClaseBadge(m.rol)}" data-member-role="${m.id_usuario}">${m.rol}</span>
                </td>
                <td style="text-align: center;">
                    <button type="button" class="btn-secondary btn-sm" data-open-modal="modal-asignar-miembro" data-assign-user="${m.id_usuario}">
                        Modificar Rol
                    </button>
                </td>
            `;
            tbody.appendChild(tr);

            const taskRole = document.querySelector(`[data-assignee-role="${m.id_usuario}"]`);
            if (taskRole) {
                taskRole.textContent = `(${m.rol})`;
            }

            if (usuarioSesion && usuarioSesion.id === m.id_usuario) {
                const userRole = document.querySelector('.user-role');
                if (userRole) userRole.textContent = m.rol;
            }
        });

        tbody.querySelectorAll('[data-assign-user]').forEach(btn => {
            btn.addEventListener('click', () => {
                const idU = btn.getAttribute('data-assign-user');
                const selectUser = document.getElementById('asignar-id-usuario');
                if (selectUser) selectUser.value = idU;
                const modal = document.getElementById('modal-asignar-miembro');
                if (modal) modal.classList.add('active');
            });
        });

    } catch (e) {
        console.error('Error al listar miembros:', e);
    }
}

// Llenar selector de proyectos
async function cargarListaProyectos() {
    const selector = document.getElementById('selector-proyectos');
    if (!selector) return;

    try {
        listaProyectos = await api.listarProyectos();
        selector.innerHTML = '';

        if (!listaProyectos || listaProyectos.length === 0) {
            selector.innerHTML = `<option value="${proyectoActivo.id}">${proyectoActivo.id} — ${proyectoActivo.nombre}</option>`;
            return;
        }

        listaProyectos.forEach(p => {
            const opt = document.createElement('option');
            opt.value = p.id;
            opt.textContent = `${p.id} — ${p.nombre}`;
            if (p.id === proyectoActivo.id) opt.selected = true;
            selector.appendChild(opt);
        });

        selector.addEventListener('change', async (e) => {
            const nuevoId = e.target.value;
            await cargarProyecto(nuevoId);
        });

    } catch (e) {
        console.error('Error al listar proyectos:', e);
    }
}

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
    }, 4000);
}

// Sesión de usuario
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

// Consultar proyecto
async function cargarProyecto(idProyecto) {
    try {
        const p = await api.consultarProyecto(idProyecto);
        proyectoActivo = p;
        actualizarVistaProyecto();
        await cargarMiembrosProyecto(proyectoActivo.id);

        const selector = document.getElementById('selector-proyectos');
        if (selector) selector.value = p.id;

        mostrarToast(`Proyecto '${p.nombre}' cargado con éxito.`);
    } catch (e) {
        mostrarToast(e.message || 'Error al consultar proyecto', 'error');
    }
}

// Actualizar vista del proyecto
function actualizarVistaProyecto() {
    const elTitulo = document.getElementById('project-title');
    const elId = document.getElementById('project-id-badge');
    const elDesc = document.getElementById('project-desc');
    const elEstado = document.getElementById('project-status-badge');

    if (elTitulo) elTitulo.textContent = proyectoActivo.nombre || proyectoActivo.id;
    if (elId) elId.textContent = `ID: ${proyectoActivo.id}`;
    if (elDesc) elDesc.textContent = proyectoActivo.descripcion || 'Sin descripción';
    if (elEstado) elEstado.textContent = proyectoActivo.estado || 'Activo';

    document.querySelectorAll('[data-prefill-project]').forEach(input => {
        input.value = proyectoActivo.id;
    });
}

// Eventos de modales y formularios
function setupModals() {
    // Abrir modales
    document.querySelectorAll('[data-open-modal]').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const modalId = btn.getAttribute('data-open-modal');
            const modal = document.getElementById(modalId);
            if (modal) {
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

    // Crear proyecto
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
                await cargarListaProyectos();
                await cargarMiembrosProyecto(proyectoActivo.id);
            } catch (err) {
                mostrarToast(err.message, 'error');
            } finally {
                btnSubmit.disabled = false;
                btnSubmit.textContent = 'Guardar Proyecto';
            }
        });
    }

    // Buscar proyecto
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

    // Asignar miembro
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
                mostrarToast(`¡Rol actualizado! ${miembro.id_usuario} ahora es '${miembro.rol}'.`);
                formAsignarMiembro.reset();
                formAsignarMiembro.closest('.modal-backdrop').classList.remove('active');
                await cargarMiembrosProyecto(idPry);
            } catch (err) {
                mostrarToast(err.message, 'error');
            } finally {
                btnSubmit.disabled = false;
                btnSubmit.textContent = 'Asignar Miembro';
            }
        });
    }

    // Consultar miembro
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
                            <strong>Usuario:</strong> ${res.id_usuario} (${obtenerNombreUsuario(res.id_usuario)})<br>
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

    // Verificar permiso
    const formVerificarPermiso = document.getElementById('form-verificar-permiso');
    const resultadoPermiso = document.getElementById('resultado-verificar-permiso');
    if (formVerificarPermiso) {
        formVerificarPermiso.addEventListener('submit', async (e) => {
            e.preventDefault();
            const idPry = document.getElementById('verificar-permiso-proyecto').value.trim();
            const idUsuario = document.getElementById('verificar-permiso-usuario').value.trim();
            const rol = document.getElementById('verificar-permiso-rol').value;

            const btnSubmit = formVerificarPermiso.querySelector('button[type="submit"]');
            btnSubmit.disabled = true;
            btnSubmit.textContent = 'Comprobando...';

            try {
                const res = await api.verificarPermiso(idPry, idUsuario, rol);
                resultadoPermiso.style.display = 'block';

                if (res.tiene_permiso) {
                    resultadoPermiso.innerHTML = `
                        <div style="background-color: var(--color-emerald-50); border: 1px solid var(--color-emerald-200); border-radius: var(--radius-md); padding: 1rem; margin-top: 1rem; color: var(--color-emerald-700);">
                            <div style="font-weight: 700; font-size: 0.875rem;">✅ Permiso Concedido</div>
                            <div style="font-size: 0.8125rem; margin-top: 0.25rem;">
                                El usuario <strong>${res.id_usuario}</strong> (${obtenerNombreUsuario(res.id_usuario)}) <strong>SÍ posee</strong> el rol <strong>'${res.rol_solicitado}'</strong> en este proyecto.
                            </div>
                        </div>
                    `;
                } else {
                    resultadoPermiso.innerHTML = `
                        <div style="background-color: var(--color-amber-50); border: 1px solid var(--color-amber-200); border-radius: var(--radius-md); padding: 1rem; margin-top: 1rem; color: var(--color-amber-700);">
                            <div style="font-weight: 700; font-size: 0.875rem;">⚠️ Permiso No Asignado</div>
                            <div style="font-size: 0.8125rem; margin-top: 0.25rem;">
                                El usuario <strong>${res.id_usuario}</strong> (${obtenerNombreUsuario(res.id_usuario)}) <strong>NO posee</strong> el rol '${res.rol_solicitado}' en este proyecto.
                            </div>
                        </div>
                    `;
                }
            } catch (err) {
                resultadoPermiso.style.display = 'block';
                resultadoPermiso.innerHTML = `
                    <div style="background-color: var(--color-rose-50); border: 1px solid var(--color-rose-200); border-radius: var(--radius-md); padding: 1rem; margin-top: 1rem; color: var(--color-rose-700); font-size: 0.8125rem;">
                        ⚠️ ${err.message}
                    </div>
                `;
            } finally {
                btnSubmit.disabled = false;
                btnSubmit.textContent = 'Comprobar Permiso';
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
    setupModals();
    setupLogout();
    await cargarListaProyectos();

    try {
        const p = await api.consultarProyecto('PRY001');
        proyectoActivo = p;
        actualizarVistaProyecto();
    } catch (e) {
        actualizarVistaProyecto();
    }

    await cargarMiembrosProyecto(proyectoActivo.id);
});
