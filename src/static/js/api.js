// Cliente API REST con Fetch
const API_BASE = '/api/v1';

export const api = {
    // Sesión actual
    async getSesion() {
        const res = await fetch(`${API_BASE}/auth/me`, {
            credentials: 'same-origin',
            cache: 'no-store'
        });
        if (!res.ok) throw new Error('No autenticado');
        return await res.json();
    },

    // Cerrar sesión
    async logout() {
        return await fetch(`${API_BASE}/auth/logout`, {
            method: 'POST',
            credentials: 'same-origin'
        });
    },

    // Listar proyectos
    async listarProyectos() {
        const res = await fetch(`${API_BASE}/administracion/proyectos`, {
            credentials: 'same-origin',
            cache: 'no-store'
        });
        const json = await res.json().catch(() => ([]));
        if (!res.ok) throw new Error(json.detail || 'Error al listar los proyectos');
        return json;
    },

    // Crear proyecto
    async crearProyecto(datos) {
        const res = await fetch(`${API_BASE}/administracion/proyectos`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'same-origin',
            body: JSON.stringify(datos)
        });
        const json = await res.json().catch(() => ({}));
        if (!res.ok) throw new Error(json.detail || 'Error al crear el proyecto');
        return json;
    },

    // Consultar proyecto por ID
    async consultarProyecto(idProyecto) {
        const res = await fetch(`${API_BASE}/administracion/proyectos/${encodeURIComponent(idProyecto.trim())}`, {
            credentials: 'same-origin'
        });
        const json = await res.json().catch(() => ({}));
        if (!res.ok) throw new Error(json.detail || `Proyecto '${idProyecto}' no encontrado`);
        return json;
    },

    // Listar miembros de un proyecto
    async listarMiembros(idProyecto) {
        const res = await fetch(`${API_BASE}/administracion/proyectos/${encodeURIComponent(idProyecto.trim())}/miembros`, {
            credentials: 'same-origin',
            cache: 'no-store'
        });
        const json = await res.json().catch(() => ([]));
        if (!res.ok) throw new Error(json.detail || `Error al listar miembros del proyecto '${idProyecto}'`);
        return json;
    },

    // Asignar o actualizar rol de miembro
    async asignarMiembro(idProyecto, datos) {
        const res = await fetch(`${API_BASE}/administracion/proyectos/${encodeURIComponent(idProyecto.trim())}/miembros`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'same-origin',
            body: JSON.stringify(datos)
        });
        const json = await res.json().catch(() => ({}));
        if (!res.ok) throw new Error(json.detail || 'Error al asignar miembro');
        return json;
    },

    // Consultar miembro
    async consultarMiembro(idProyecto, idUsuario) {
        const res = await fetch(
            `${API_BASE}/administracion/proyectos/${encodeURIComponent(idProyecto.trim())}/miembros/${encodeURIComponent(idUsuario.trim())}`,
            { credentials: 'same-origin' }
        );
        const json = await res.json().catch(() => ({}));
        if (!res.ok) throw new Error(json.detail || `Miembro '${idUsuario}' no encontrado en el proyecto '${idProyecto}'`);
        return json;
    },

    // Consultar permisos
    async consultarPermisos(idProyecto, idUsuario) {
        const res = await fetch(
            `${API_BASE}/administracion/proyectos/${encodeURIComponent(idProyecto.trim())}/miembros/${encodeURIComponent(idUsuario.trim())}/permisos`,
            { credentials: 'same-origin' }
        );
        const json = await res.json().catch(() => ({}));
        if (!res.ok) throw new Error(json.detail || 'Error al consultar permisos');
        return json;
    },

    // Verificar permiso
    async verificarPermiso(idProyecto, idUsuario, rol) {
        const res = await fetch(
            `${API_BASE}/administracion/proyectos/${encodeURIComponent(idProyecto.trim())}/miembros/${encodeURIComponent(idUsuario.trim())}/verificar-permiso`,
            {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                credentials: 'same-origin',
                body: JSON.stringify({ rol })
            }
        );
        const json = await res.json().catch(() => ({}));
        if (!res.ok) throw new Error(json.detail || 'Error al verificar permiso');
        return json;
    },

    // Registrar matrícula
    async matricularEstudiante(datos) {
        const res = await fetch(`${API_BASE}/administracion/matriculas`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'same-origin',
            body: JSON.stringify(datos)
        });
        const json = await res.json().catch(() => ({}));
        if (!res.ok) throw new Error(json.detail || 'Error al registrar la matrícula');
        return json;
    },

    // Listar matrículas
    async listarMatriculas(filtros = {}) {
        const params = new URLSearchParams();
        if (filtros.id_usuario) params.append('id_usuario', filtros.id_usuario);
        if (filtros.id_curso) params.append('id_curso', filtros.id_curso);

        const url = `${API_BASE}/administracion/matriculas${params.toString() ? '?' + params.toString() : ''}`;
        const res = await fetch(url, {
            credentials: 'same-origin',
            cache: 'no-store'
        });
        const json = await res.json().catch(() => ([]));
        if (!res.ok) throw new Error(json.detail || 'Error al listar las matrículas');
        return json;
    },

    // Consultar matrícula por ID
    async consultarMatricula(idMatricula) {
        const res = await fetch(`${API_BASE}/administracion/matriculas/${encodeURIComponent(idMatricula.trim())}`, {
            credentials: 'same-origin'
        });
        const json = await res.json().catch(() => ({}));
        if (!res.ok) throw new Error(json.detail || `Matrícula '${idMatricula}' no encontrada`);
        return json;
    }
};
