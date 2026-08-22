# Padel Pro - Torneos & Gestos

Aplicación de gestión de torneos de pádel con control de partidos en vivo, motor de puntuación oficial y reconocimiento de gestos por cámara.

## Características

- Gestión de torneos, parejas, jugadores y pistas
- Motor de puntuación oficial de pádel (con tie-break y punto de oro)
- Control de partidos en vivo con cronómetro
- Reconocimiento de gestos por cámara para controlar el marcador sin tocar la pantalla
- Historial de eventos y auditoría
- Rankings y estadísticas

## Stack

### Frontend
- React 19 + Vite + TypeScript
- Tailwind CSS 4
- Lucide React icons
- Motion (Framer Motion)

### Backend
- FastAPI + Uvicorn
- SQLAlchemy 2.0
- PostgreSQL 16
- Pydantic 2

## Setup Local

### Prerequisitos
- Node.js 18+
- Python 3.12+
- PostgreSQL 16 (o Docker)

### 1. Clonar el repositorio

```bash
git clone <repo-url>
cd padel-pro---torneos-&-gestos
```

### 2. Configurar variables de entorno

Frontend (`.env`):
```bash
VITE_API_BASE=http://localhost:8000
```

Backend (`backend/.env`):
```bash
DATABASE_URL=postgresql://padel_user:padel_pass@localhost:5432/padel_pro
```

### 3. Configurar base de datos

```bash
# Crear la base de datos PostgreSQL
createdb padel_pro

# Ejecutar schema inicial
psql -U padel_user -d padel_pro -f backend/init_db.sql
```

### 4. Instalar dependencias

```bash
# Frontend
npm install

# Backend
cd backend
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

### 5. Ejecutar la aplicación

```bash
# Terminal 1 - Backend
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2 - Frontend
npm run dev
```

La app estará disponible en `http://localhost:3000`.

## Scripts Disponibles

### Frontend
- `npm run dev` - Inicia el servidor de desarrollo en puerto 3000
- `npm run build` - Construye la app para producción
- `npm run preview` - Previsualiza la build de producción
- `npm run lint` - Verifica tipos de TypeScript
- `npm run clean` - Limpia archivos generados

### Backend
- `uvicorn main:app --reload` - Inicia API con recarga automática
- Acceder a documentación interactiva en `http://localhost:8000/docs`

## Producción

La aplicación está desplegada en Render:
- Frontend + Backend: https://padel-pro-1iny.onrender.com

## Estructura del Proyecto

```
├── src/
│   ├── api.ts                 # Cliente HTTP para la API
│   ├── types.ts               # Tipos TypeScript
│   ├── App.tsx                # Componente principal
│   ├── components/            # Componentes de UI
│   ├── domain/
│   │   └── scoringEngine.ts   # Motor de puntuación de pádel
│   ├── camera/                # Reconocimiento de gestos (MediaPipe)
│   └── data/
│       └── mockData.ts        # Datos iniciales de ejemplo
├── backend/
│   ├── main.py                # API FastAPI
│   ├── database.py            # Configuración SQLAlchemy
│   ├── init_db.sql            # Schema inicial de PostgreSQL
│   ├── requirements.txt       # Dependencias Python
│   └── Dockerfile             # Imagen Docker del backend
├── docker-compose.yml         # Orquestación local (DB + Backend)
├── vite.config.ts             # Configuración de Vite
└── package.json               # Dependencias y scripts del frontend
```

## API Endpoints

- `GET /api/users` - Listar jugadores
- `GET /api/pairs` - Listar parejas
- `GET /api/tournaments` - Listar torneos
- `GET /api/matches` - Listar partidos
- `GET /api/courts` - Listar pistas
- `GET /api/stats` - Estadísticas generales
- `POST /api/users` - Crear usuario
- `PUT /api/matches/{id}` - Actualizar partido
- `POST /api/matches/{id}/events` - Registrar evento de partido
- `POST /api/audit-logs` - Crear log de auditoría

Documentación completa disponible en `/docs` cuando el backend está corriendo.
