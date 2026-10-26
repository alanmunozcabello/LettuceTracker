/**
 * LettuceTracker - Capa de comunicación con el Backend mediante Fetch API
 * 
 * Conecta los endpoints REST existentes de Autenticación y Administración.
 */

const API_BASE = '/api/v1';

export const api = {
    /**
     * Valida la sesión actual del usuario autenticado.
     */
    async getSesion() {
        const res = await fetch(`${API_BASE}/auth/me`, {
            credentials: 'same-origin',
            cache: 'no-store'
        });
        if (!res.ok) {
            throw new Error('No autenticado');
        }
        return await res.json();
    },

    /**
     * Cierra la sesión activa en el servidor y elimina la cookie.
     */
    async logout() {
        return await fetch(`${API_BASE}/auth/logout`, {
            method: 'POST',
            credentials: 'same-origin'
        });
    },

    /**
     * Crea un nuevo proyecto en el backend (POST /api/v1/administracion/proyectos).
     * @param {{ id: string, nombre: string, descripcion: string }} datos
     */
    async crearProyecto(datos) {
        const res = await fetch(`${API_BASE}/administracion/proyectos`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'same-origin',
            body: JSON.stringify(datos)
        });
        const json = await res.json().catch(() => ({}));
        if (!res.ok) {
            throw new Error(json.detail || 'Error al crear el proyecto');
        }
        return json;
    },

    /**
     * Consulta un proyecto por su identificador (GET /api/v1/administracion/proyectos/{id}).
     * @param {string} idProyecto
     */
    async consultarProyecto(idProyecto) {
        const res = await fetch(`${API_BASE}/administracion/proyectos/${encodeURIComponent(idProyecto.trim())}`, {
            credentials: 'same-origin'
        });
        const json = await res.json().catch(() => ({}));
        if (!res.ok) {
            throw new Error(json.detail || `Proyecto '${idProyecto}' no encontrado`);
        }
        return json;
    },

    /**
     * Asigna o actualiza el rol de un miembro en un proyecto (POST /api/v1/administracion/proyectos/{id}/miembros).
     * @param {string} idProyecto
     * @param {{ id_usuario: string, rol: string }} datos
     */
    async asignarMiembro(idProyecto, datos) {
        const res = await fetch(`${API_BASE}/administracion/proyectos/${encodeURIComponent(idProyecto.trim())}/miembros`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'same-origin',
            body: JSON.stringify(datos)
        });
        const json = await res.json().catch(() => ({}));
        if (!res.ok) {
            throw new Error(json.detail || 'Error al asignar miembro');
        }
        return json;
    },

    /**
     * Consulta la pertenencia y rol de un miembro (GET /api/v1/administracion/proyectos/{id}/miembros/{id_usuario}).
     * @param {string} idProyecto
     * @param {string} idUsuario
     */
    async consultarMiembro(idProyecto, idUsuario) {
        const res = await fetch(
            `${API_BASE}/administracion/proyectos/${encodeURIComponent(idProyecto.trim())}/miembros/${encodeURIComponent(idUsuario.trim())}`,
            { credentials: 'same-origin' }
        );
        const json = await res.json().catch(() => ({}));
        if (!res.ok) {
            throw new Error(json.detail || `Miembro '${idUsuario}' no encontrado en el proyecto '${idProyecto}'`);
        }
        return json;
    },

    /**
     * Consulta los permisos específicos de un miembro (GET /api/v1/administracion/proyectos/{id}/miembros/{id_usuario}/permisos).
     * @param {string} idProyecto
     * @param {string} idUsuario
     */
    async consultarPermisos(idProyecto, idUsuario) {
        const res = await fetch(
            `${API_BASE}/administracion/proyectos/${encodeURIComponent(idProyecto.trim())}/miembros/${encodeURIComponent(idUsuario.trim())}/permisos`,
            { credentials: 'same-origin' }
        );
        const json = await res.json().catch(() => ({}));
        if (!res.ok) {
            throw new Error(json.detail || 'Error al consultar permisos');
        }
        return json;
    },

    /**
     * Registra la matrícula de un estudiante en un curso (POST /api/v1/administracion/matriculas).
     * @param {{ id_usuario: string, id_curso: string }} datos
     */
    async matricularEstudiante(datos) {
        const res = await fetch(`${API_BASE}/administracion/matriculas`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'same-origin',
            body: JSON.stringify(datos)
        });
        const json = await res.json().catch(() => ({}));
        if (!res.ok) {
            throw new Error(json.detail || 'Error al registrar la matrícula');
        }
        return json;
    }
};
