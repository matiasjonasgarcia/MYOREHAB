import pandas as pd

def generar_excel_diccionario():
    # 1. Centers
    centers = pd.DataFrame([
        ["center_id", "VARCHAR(10)", "Alphanumeric", "Unique code for the research center (e.g., 'BR-CMP')", "PK"],
        ["center_name", "VARCHAR(100)", "Text", "Full name of the institution/laboratory", "-"],
        ["country", "VARCHAR(50)", "Text", "Country of the research center", "-"]
    ], columns=["Variable", "Data Type", "Unit/Format", "Description", "Key Type"])

    # 2. Subjects
    subjects = pd.DataFrame([
        ["subject_id", "VARCHAR(15)", "Alphanumeric", "Unique identifier (e.g., 'BR-CMP-S001')", "PK"],
        ["center_id", "VARCHAR(10)", "Alphanumeric", "References the center", "FK"],
        ["age", "INTEGER", "Years", "Participant's age", "-"],
        ["gender", "VARCHAR(20)", "Text", "Participant's gender", "-"],
        ["weight", "NUMERIC(5,2)", "Kilograms (kg)", "Body weight", "-"],
        ["height", "NUMERIC(5,2)", "Centimeters (cm)", "Height", "-"],
        ["fa_circ", "NUMERIC(5,2)", "Centimeters (cm)", "Forearm circumference", "-"],
        ["lateral_dominance", "VARCHAR(20)", "Text", "Handedness (Right/Left)", "-"],
        ["laterality", "NUMERIC(5,2)", "Score", "Laterality index (e.g., Edinburgh Inventory)", "-"],
        ["nhpeg_dominant", "NUMERIC(6,2)", "Seconds (s)", "NHPT time for dominant hand", "-"],
        ["nhpeg_nondominant", "NUMERIC(6,2)", "Seconds (s)", "NHPT time for non-dominant hand", "-"],
        ["injuries", "TEXT", "Text", "Clinical history or relevant upper-limb injuries", "-"]
    ], columns=["Variable", "Data Type", "Unit/Format", "Description", "Key Type"])

    # 3. Equipment
    equipment = pd.DataFrame([
        ["equipment_id", "VARCHAR(15)", "Alphanumeric", "Unique code for the hardware setup", "PK"],
        ["signal_type", "VARCHAR(10)", "Text", "Signal modality ('EMG' or 'KINEMATICS')", "-"],
        ["brand", "VARCHAR(50)", "Text", "Manufacturer (e.g., 'In-house UNICAMP')", "-"],
        ["model", "VARCHAR(50)", "Text", "Hardware model", "-"],
        ["channel_layout", "VARCHAR(50)", "Text", "Physical distribution (e.g., '2x64 matrices', '4x32 bands')", "-"],
        ["total_channels", "INTEGER", "Count", "Total data channels", "-"]
    ], columns=["Variable", "Data Type", "Unit/Format", "Description", "Key Type"])

    # 4. Tasks
    tasks = pd.DataFrame([
        ["task_id", "VARCHAR(20)", "Alphanumeric", "Unique code combining subject and condition", "PK"],
        ["subject_id", "VARCHAR(15)", "Alphanumeric", "References the participant", "FK"],
        ["condition_code", "VARCHAR(5)", "Categorical", "Protocol condition (M111 to M235)", "-"],
        ["duration", "NUMERIC(5,2)", "Seconds (s)", "Standardized duration of the trial (e.g., 30.0 s)", "-"]
    ], columns=["Variable", "Data Type", "Unit/Format", "Description", "Key Type"])

    # 5. Recordings
    recordings = pd.DataFrame([
        ["recording_id", "UUID", "UUID v4", "Unique identifier for the recording file", "PK"],
        ["task_id", "VARCHAR(20)", "Alphanumeric", "References the mirrored task/condition", "FK"],
        ["equipment_id", "VARCHAR(15)", "Alphanumeric", "References the hardware used", "FK"],
        ["sampling_freq", "NUMERIC(8,2)", "Hertz (Hz)", "Actual sampling frequency", "-"],
        ["file_path", "VARCHAR(255)", "Path", "Relative path to the raw structure", "-"]
    ], columns=["Variable", "Data Type", "Unit/Format", "Description", "Key Type"])

    # Guardar en Excel con múltiples hojas
    excel_path = "MYOREHAB_Data_Dictionary.xlsx"
    with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
        centers.to_excel(writer, sheet_name="1_Centers", index=False)
        subjects.to_excel(writer, sheet_name="2_Subjects", index=False)
        equipment.to_excel(writer, sheet_name="3_Equipment", index=False)
        tasks.to_excel(writer, sheet_name="4_Tasks", index=False)
        recordings.to_excel(writer, sheet_name="5_Recordings", index=False)
    
    print(f"¡Éxito! El archivo '{excel_path}' ha sido creado en tu carpeta.")

if __name__ == "__main__":
    generar_excel_diccionario()