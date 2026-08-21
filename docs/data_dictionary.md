# MYOREHAB: Preliminary Comprehensive Data Dictionary

This document defines the relational schema and metadata structure for the MYOREHAB multi-center database.

## 1. Centers (Research Sites)
Tracks the origin of the data to handle multi-center international protocols.

| Variable | Data Type | Unit/Format | Description | Key Type |
| :--- | :--- | :--- | :--- | :--- |
| `center_id` | VARCHAR(10) | Alphanumeric | Unique code for the research center (e.g., 'BR-CMP' for Campinas, 'ES-MAD' for Madrid). | **PK** |
| `center_name`| VARCHAR(100)| Text | Full name of the institution/laboratory. | - |
| `country` | VARCHAR(50) | Text | Country of the research center. | - |

## 2. Subjects (Participant Information)
Contains detailed demographic, anthropometric, and clinical data.

| Variable | Data Type | Unit/Format | Description | Key Type |
| :--- | :--- | :--- | :--- | :--- |
| `subject_id` | VARCHAR(15) | Alphanumeric | Unique and anonymized identifier (e.g., 'BR-CMP-S001'). | **PK** |
| `center_id` | VARCHAR(10) | Alphanumeric | References the center where the data was collected. | **FK** |
| `age` | INTEGER | Years | Participant's age. | - |
| `gender` | VARCHAR(20) | Text | Participant's gender. | - |
| `weight` | NUMERIC(5,2)| Kilograms (kg)| Body weight. | - |
| `height` | NUMERIC(5,2)| Centimeters (cm)| Height. | - |
| `fa_circ` | NUMERIC(5,2)| Centimeters (cm)| Forearm circumference (FA_Circ). | - |
| `lateral_dominance`| VARCHAR(20) | Text | Self-reported handedness (Right/Left). | - |
| `laterality` | NUMERIC(5,2)| Score | Laterality index (e.g., Edinburgh Handedness Inventory). | - |
| `nhpeg_dominant` | NUMERIC(6,2)| Seconds (s) | Nine-Hole Peg Test completion time for dominant hand. | - |
| `nhpeg_nondominant`| NUMERIC(6,2)| Seconds (s) | Nine-Hole Peg Test completion time for non-dominant hand. | - |
| `injuries` | TEXT | Text | Clinical history or relevant upper-limb injuries. | - |

## 3. Equipment (Hardware Specifications)
Catalogs the specific hardware used, allowing interoperability across different recording setups.

| Variable | Data Type | Unit/Format | Description | Key Type |
| :--- | :--- | :--- | :--- | :--- |
| `equipment_id` | VARCHAR(15) | Alphanumeric | Unique code for the hardware setup. | **PK** |
| `signal_type` | VARCHAR(10) | Text | Signal modality ('EMG' or 'KINEMATICS'). | - |
| `brand` | VARCHAR(50) | Text | Manufacturer (e.g., 'In-house UNICAMP', 'OT Bioelettronica'). | - |
| `model` | VARCHAR(50) | Text | Hardware model (e.g., 'Quattrocento', 'DFK 37BUX287'). | - |
| `channel_layout`| VARCHAR(50) | Text | Physical distribution (e.g., '2x64 matrices', '4x32 bands'). | - |
| `total_channels`| INTEGER | Count | Total data channels (e.g., 128 for EMG, 63 for 3D Kinematics). | - |

## 4. Tasks (Experimental Conditions)
Acts as the central pivot. Each task mirrors exactly one execution of a movement, linking both Kinematics and EMG data.

| Variable | Data Type | Unit/Format | Description | Key Type |
| :--- | :--- | :--- | :--- | :--- |
| `task_id` | VARCHAR(20) | Alphanumeric | Unique code combining subject and condition (e.g., 'BR-CMP-S001_M111'). | **PK** |
| `subject_id` | VARCHAR(15) | Alphanumeric | References the participant. | **FK** |
| `condition_code`| VARCHAR(5) | Categorical | Protocol condition (M111 to M235). Encodes Arm Position, Grasp Type, and Angle. | - |
| `duration` | NUMERIC(5,2)| Seconds (s) | Standardized duration of the trial (e.g., 30.0 s). | - |

## 5. Recordings (Signal Files)
Indexes the physical files, storing specific metadata for the actual recording.

| Variable | Data Type | Unit/Format | Description | Key Type |
| :--- | :--- | :--- | :--- | :--- |
| `recording_id` | UUID | UUID v4 | Unique identifier for the recording file. | **PK** |
| `task_id` | VARCHAR(20) | Alphanumeric | References the mirrored task/condition. | **FK** |
| `equipment_id` | VARCHAR(15) | Alphanumeric | References the hardware used. | **FK** |
| `sampling_freq` | NUMERIC(8,2)| Hertz (Hz) | Actual sampling frequency (e.g., ~2052 Hz for EMG, 100 Hz for Kin). | - |
| `file_path` | VARCHAR(255)| Path | Relative path to the raw structure (e.g., `data/raw/emg/S001_M111.csv`). | - |