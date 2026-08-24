-- 1. Tabla de Centros (Evita redundancia de nombres y países)
CREATE TABLE centers (
    center_id VARCHAR(10) PRIMARY KEY,
    center_name VARCHAR(100) NOT NULL,
    country VARCHAR(50) NOT NULL
);

-- 2. Tabla de Sujetos (Datos demográficos y clínicos)
CREATE TABLE subjects (
    subject_id VARCHAR(15) PRIMARY KEY,
    center_id VARCHAR(10) REFERENCES centers(center_id) ON DELETE RESTRICT,
    age INTEGER CHECK (age > 0 AND age < 120),
    gender VARCHAR(20),
    weight NUMERIC(5,2),
    height NUMERIC(5,2),
    fa_circ NUMERIC(5,2),
    lateral_dominance VARCHAR(20),
    laterality NUMERIC(5,2),
    nhpeg_dominant NUMERIC(6,2),
    nhpeg_nondominant NUMERIC(6,2),
    injuries TEXT
);

-- 3. Tabla de Equipamiento (Resolviendo el problema multicéntrico de marcas/canales)
CREATE TABLE equipment (
    equipment_id VARCHAR(15) PRIMARY KEY,
    signal_type VARCHAR(10) CHECK (signal_type IN ('EMG', 'KINEMATICS')),
    brand VARCHAR(50) NOT NULL,
    model VARCHAR(50),
    channel_layout VARCHAR(50),
    total_channels INTEGER
);

-- 4. Tabla de Tareas (El "Espejo" entre cinemática y EMG)
CREATE TABLE tasks (
    task_id VARCHAR(20) PRIMARY KEY,
    subject_id VARCHAR(15) REFERENCES subjects(subject_id) ON DELETE CASCADE,
    condition_code VARCHAR(5) NOT NULL, -- Ej: M111, M235
    duration_seconds NUMERIC(5,2) DEFAULT 30.00
);

-- 5. Tabla de Registros (Archivos físicos)
CREATE TABLE recordings (
    recording_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    task_id VARCHAR(20) REFERENCES tasks(task_id) ON DELETE CASCADE,
    equipment_id VARCHAR(15) REFERENCES equipment(equipment_id) ON DELETE RESTRICT,
    sampling_freq NUMERIC(8,2) NOT NULL,
    file_path VARCHAR(255) UNIQUE NOT NULL,
    has_notch_filter BOOLEAN DEFAULT FALSE
);

-- 6. Tabla de Métricas Extraídas (Aborda Tareas 3 y 4 del Sprint)
-- Aquí guardaremos los resultados post-procesamiento (amplitudes resumen, velocidades)
CREATE TABLE signal_metrics (
    metric_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    recording_id UUID REFERENCES recordings(recording_id) ON DELETE CASCADE,
    feature_category VARCHAR(50) NOT NULL, -- Ej: 'Cinemática', 'EMG'
    feature_name VARCHAR(50) NOT NULL,     -- Ej: 'max_angular_velocity', 'rms_amplitude'
    feature_value NUMERIC(10,4) NOT NULL,
    unit VARCHAR(20)                       -- Ej: 'deg/s', 'mV'
);