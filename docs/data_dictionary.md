# MYOREHAB Dataset — Data Dictionary & Relational Schema

## 1. Overview & Dataset Architecture

The **MYOREHAB** dataset provides high-density surface electromyography (HD-sEMG) and synchronous 3D kinematic tracking for upper-limb gesture and posture analysis. The dataset follows a multi-center, relational architecture linking participant clinical demographics, hardware setups, experimental protocol tasks, and multidimensional signal time-series.

### Entity-Relationship Diagram (ERD Summary)
[centers] 1 ─── N [subjects] 1 ─── N [tasks] 1 ─── N [recordings]
│                   │
├────── N ──────────┤
▼                   ▼
[emg_signals]       [kinematics_3d]

---

## 0. Protocol & Naming Structure
Files are stored in `data-emg-raw/` and `data-kinetics-raw/` under the pattern `SNNN_PGA.csv`. During the ETL pipeline (`run_etl.py`), filename codes are parsed and extracted into relational primary keys and filter columns.

| Element | Variable Name | Data Type | Key Type | Description & Value Encoding |
|---|---|---|---|---|
| **SNNN** | `subject_id` | VARCHAR(15) | FK | Subject identifier formatted as `BR-CMP-SNNN` (e.g., `BR-CMP-S001`) |
| **P** | `arm_position` | INTEGER | Factor | Arm Position: `1` = Distal (AE), `2` = Proximal (AF) |
| **G** | `task_id` | INTEGER | FK / Factor | Grasp Type: `1` = One Finger Pinch (1FP), `2` = Two Finger Pinch (2FP), `3` = Full Grasp (FG) |
| **A** | `hand_angle` | INTEGER | Factor | Hand Angle: `1` = 0°, `2` = 45°, `3` = 90°, `4` = 135°, `5` = 180° |

---

## 2. Naming Conventions & Protocol Syntax

Raw and processed trial files follow a strict standardized naming convention:

$$\text{Syntax: } \mathbf{SNNN\_PGA.csv}$$

| Element | Component | Key Type | Values / Description |
| :--- | :--- | :---: | :--- |
| **Directory** | Folder path | - | `emg-raw-renamed/` |
| **S** | Prefix | - | Literal character `S` (Subject) |
| **NNN** | Subject ID | **FK** | 3-digit zero-padded integer (`001`–`999`), mapping to `subject_id` (`BR-CMP-SNNN`) |
| **P** | Arm Position | - | **1**: Distal (AE — Above Elbow / Distal)<br>**2**: Proximal (AF — Arm Flexed / Proximal) |
| **G** | Grasp Type | - | **1**: One Finger Pinch (1FP)<br>**2**: Two Finger Pinch (2FP)<br>**3**: Full Grasp (FG) |
| **A** | Angle | - | **1**: 0°<br>**2**: 45°<br>**3**: 90°<br>**4**: 135°<br>**5**: 180° |

*Example:* `S001_111.csv` corresponds to **Subject 001**, **Distal Position (1)**, **1-Finger Pinch (1)**, at **0° Angle (1)**.

---

## 3. Relational Database Tables

### 3.1. `0_Protocol_Naming`
Metadata defining the directory structure and trial encoding scheme.

| Element | Value / Pattern | Description & Categorization | Key Type |
| :--- | :--- | :--- | :---: |
| **Folder Structure** | `emg-raw-renamed/` | Directory containing raw/renamed sEMG and Kinematic CSV files | - |
| **File Pattern** | `SNNN_PGA.csv` | Standardized file naming syntax (e.g., `S001_111.csv`) | - |
| **S** | Subject Prefix | Literal letter 'S' indicating subject identifier | - |
| **NNN** | Subject Code | 3-digit numeric ID (`001`-`999`) corresponding to `subject_id` (`BR-CMP-SNNN`) | **FK** |
| **P** | Arm Position | 1 = Distal (AE: Above Elbow), 2 = Proximal (AF: Arm Flexed) | - |
| **G** | Grasp Type | 1 = One Finger Pinch (1FP), 2 = Two Finger Pinch (2FP), 3 = Full Grasp (FG) | - |
| **A** | Angle | 1 = 0°, 2 = 45°, 3 = 90°, 4 = 135°, 5 = 180° | - |

---

### 3.2. `1_Centers`
Primary location registry for research centers involved in data acquisition.

| Variable | Data Type | Unit / Format | Description | Key Type |
| :--- | :--- | :--- | :--- | :---: |
| **center_id** | VARCHAR(10) | Alphanumeric | Unique code for the research center (e.g., `'BR-CMP'`) | **PK** |
| **center_name** | VARCHAR(100) | Text | Full name of the institution or laboratory | - |
| **country** | VARCHAR(50) | Text | Country where the research center is located | - |

---

### 3.3. `2_Subjects`
Clinical demographics, physical characteristics, and baseline motor test metrics.

| Variable | Data Type | Unit / Format | Description | Key Type |
| :--- | :--- | :--- | :--- | :---: |
| **subject_id** | VARCHAR(15) | Alphanumeric | Unique subject code (e.g., `'BR-CMP-S001'`) | **PK** |
| **center_id** | VARCHAR(10) | Alphanumeric | Research center key | **FK** |
| **age** | INTEGER | Years | Participant's age at acquisition time | - |
| **gender** | VARCHAR(20) | Text | Participant's self-reported gender | - |
| **weight** | NUMERIC(5,2) | Kilograms (kg) | Body weight | - |
| **height** | NUMERIC(5,2) | Centimeters (cm) | Height | - |
| **fa_circ** | NUMERIC(5,2) | Centimeters (cm) | Forearm circumference measured at maximum girth | - |
| **lateral_dominance** | VARCHAR(20) | Text | Handedness (`Right` / `Left`) | - |
| **laterality** | NUMERIC(5,2) | Score | Laterality quotient (e.g., Edinburgh Handedness Inventory) | - |
| **nhpeg_dominant** | NUMERIC(6,2) | Seconds (s) | Nine-Hole Peg Test performance (Dominant hand) | - |
| **nhpeg_nondominant** | NUMERIC(6,2) | Seconds (s) | Nine-Hole Peg Test performance (Non-dominant hand) | - |
| **injuries** | TEXT | Text | Relevant upper-limb injuries or neuromuscular conditions | - |

---

### 3.4. `3_Equipment`
Hardware configurations for electrophysiological and optical sensor arrays.

| Variable | Data Type | Unit / Format | Description | Key Type |
| :--- | :--- | :--- | :--- | :---: |
| **equipment_id** | VARCHAR(15) | Alphanumeric | Unique code for the hardware setup | **PK** |
| **signal_type** | VARCHAR(10) | Text | Signal modality (`EMG` or `KINEMATICS`) | - |
| **brand** | VARCHAR(50) | Text | Hardware manufacturer | - |
| **model** | VARCHAR(50) | Text | Device model / acquisition system | - |
| **channel_layout** | VARCHAR(50) | Text | Physical sensor topology (e.g., `'2x64 matrices'`) | - |
| **total_channels** | INTEGER | Count | Number of operational channels | - |

---

### 3.5. `4_Tasks`
Task/trial specification mapping subject executions to protocol posture combinations.

| Variable | Data Type | Unit / Format | Description | Key Type |
| :--- | :--- | :--- | :--- | :---: |
| **task_id** | VARCHAR(20) | Alphanumeric | Composite identifier (e.g., `'BR-CMP-S001_M111'`) | **PK** |
| **subject_id** | VARCHAR(15) | Alphanumeric | References participant ID | **FK** |
| **condition_code** | VARCHAR(5) | Categorical | Protocol condition (`M111` to `M235`) encoding $PGA$ | - |
| **duration** | NUMERIC(5,2) | Seconds (s) | Nominal trial duration (e.g., `30.0` s) | - |

---

### 3.6. `5_Recordings`
File-level metadata linking trial tasks to raw data stores on disk.

| Variable | Data Type | Unit / Format | Description | Key Type |
| :--- | :--- | :--- | :--- | :---: |
| **recording_id** | UUID | UUID v4 | Unique identifier for the raw file execution | **PK** |
| **task_id** | VARCHAR(20) | Alphanumeric | References protocol task | **FK** |
| **equipment_id** | VARCHAR(15) | Alphanumeric | Hardware system key | **FK** |
| **sampling_freq** | NUMERIC(8,2) | Hertz (Hz) | Acquisition sampling rate | - |
| **file_path** | VARCHAR(255) | Path | Relative path (`emg-raw-renamed/SNNN_PGA.csv`) | - |

---

### 3.7. `6_EMG_Signals`
High-Density Surface Electromyography matrix data (128 total channels).

| Variable Range | Data Type | Unit / Format | Description | Key Type |
| :--- | :--- | :--- | :--- | :---: |
| **task_id** | VARCHAR(20) | Alphanumeric | Protocol task identifier | **FK** |
| **subject_id** | VARCHAR(15) | Alphanumeric | Subject identifier | **FK** |
| **flex_ch1** – **flex_ch64** | FLOAT64 | $\mu\text{V}$ / Digital | 64 HD-sEMG channels placed over forearm flexor muscles | - |
| **exte_ch1** – **exte_ch64** | FLOAT64 | $\mu\text{V}$ / Digital | 64 HD-sEMG channels placed over forearm extensor muscles | - |

---

### 3.8. `7_Kinematics_3D`
Synchronous 3D kinematic keypoint tracking, confidence scores, and transformation matrices.

#### Identifiers & Frame Index
| Variable | Data Type | Unit / Format | Description | Key Type |
| :--- | :--- | :--- | :--- | :---: |
| **task_id** | VARCHAR(20) | Alphanumeric | Protocol task key | **FK** |
| **subject_id** | VARCHAR(15) | Alphanumeric | Subject key | **FK** |
| **fnum** | INT64 | Frame Index | Sequential frame counter | - |

#### Joint Keypoint Quadruplets & Quality Metrics (21 Keypoints $\times$ 6 Attributes = 126 Columns)
*Tracked Keypoints:* `wrist`, `thumb_cmc`, `thumb_mcp`, `thumb_ip`, `thumb_tip`, `index_finger_mcp`, `index_finger_pip`, `index_finger_dip`, `index_finger_tip`, `middle_finger_mcp`, `middle_finger_pip`, `middle_finger_dip`, `middle_finger_tip`, `ring_finger_mcp`, `ring_finger_pip`, `ring_finger_dip`, `ring_finger_tip`, `pinky_mcp`, `pinky_pip`, `pinky_dip`, `pinky_tip`.

Anatomical abbreviations:
- `CMC`: Carpometacarpal joint
- `MCP`: Metacarpophalangeal joint
- `PIP`: Proximal interphalangeal joint
- `DIP`: Distal interphalangeal joint
- `IP`: Interphalangeal joint
- `TIP`: Distal extremity of the finger

#### Per-Keypoint Position and Quality Variables
Each of the 21 keypoints generates 5 standardized columns:
For each keypoint `[joint]`:
| Variable Syntax | Data Type | Unit / Format | Description |
| :--- | :--- | :--- | :--- |
| `[joint]_x` | FLOAT64 | mm / px | Spatial 3D Coordinate $X$ |
| `[joint]_y` | FLOAT64 | mm / px | Spatial 3D Coordinate $Y$ |
| `[joint]_z` | FLOAT64 | mm / px | Spatial 3D Coordinate $Z$ |
| `[joint]_error` | FLOAT64 | Pixels (px) | Reprojection error in 2D pixels |
| `[joint]_ncams` | INT64 | Count (0–5) | Number of cameras contributing to 3D triangulation |
| `[joint]_score` | FLOAT64 | Score (0.0–1.0) | Minimum 2D detection confidence score |

#### Calibration Reference System
| Variable | Data Type | Unit / Format | Description |
| :--- | :--- | :--- | :--- |
| **m_00** – **m_22** | FLOAT64 | Matrix Element | 9 elements of the $3 \times 3$ coordinate rotation matrix $\mathbf{M}$ |
| **center_0** – **center_2** | FLOAT64 | Spatial Coords | 3D origin center coordinates $(x_0, y_0, z_0)$ |
