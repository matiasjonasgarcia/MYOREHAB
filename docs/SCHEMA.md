````mermaid
erDiagram
    CENTERS {
        string center_id PK
        string center_name
        string country
    }
    SUBJECTS {
        string subject_id PK
        string center_id FK
        string acronyms
        int age
        string gender
        float weight
        float height
        float fa_circ
        string injuries
        string injuries_description
        string sport
        string sport_type
        int sport_frequency
        string lateral_dominancy
        float laterality
        float nhpt_dominante_s
        float nhpt_no_dominante_s
    }
    EQUIPMENT {
        string equipment_id PK
        string center_id FK
        string signal_type
        string brand
        string model
        string channel_layout
    }
    TASKS {
        string task_id PK
        string subject_id FK
        string condition_code
        float duration
    }
    RECORDINGS {
        string recording_id PK
        string task_id FK
        string equipment_id FK
        float sampling_freq
        string file_path
    }
    EMG_SIGNALS {
        string emg_id PK
        string recording_id FK
        string equipment_id FK
        string ruta_archivo
    }
    KINEMATICS_3D {
        string kin_id PK
        string recording_id FK
        string equipment_id FK
        string ruta_archivo
    }
    VIDEOS_3D {
        string video_id PK
        string recording_id FK
        string ruta_archivo
    }

    CENTERS ||--o{ SUBJECTS : "houses"
    CENTERS ||--o{ EQUIPMENT : "owns"
    SUBJECTS ||--o{ TASKS : "performs"
    TASKS ||--o{ RECORDINGS : "generates"
    RECORDINGS ||--o| EMG_SIGNALS : "links"
    RECORDINGS ||--o| KINEMATICS_3D : "links"
    RECORDINGS ||--o| VIDEOS_3D : "links"
    EQUIPMENT ||--o{ EMG_SIGNALS : "records"
    EQUIPMENT ||--o{ KINEMATICS_3D : "records"