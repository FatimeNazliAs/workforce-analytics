# FABENODE REPORT MAPPING

## Purpose

This document maps each report page to:
- required metrics
- required columns
- visualization types
- reusable calculation logic
- output artifacts

The goal is to keep report requirements separated from implementation details.

---

# PAGE 3 — REPORT DEFINITIONS

## Purpose

Defines:
- valid data rules
- stress categories
- fatigue categories
- critical event definitions
- high load definitions

## Required Logic

### Valid Row Rule

Conditions:
- message == "SUCCESS"
- is_ekg_quality == True

### Critical Stress Rule

Conditions:
- stress_score >= 8
- valid row

### Critical Event Rule

Conditions:
- stress_score >= 8
- hr >= 100
- valid row

### High Load Rule

Conditions:
- stress_score >= 6
OR
- hr >= 100
- valid row

## Required Modules

- validation.py
- risk_rules.py

## Output

No chart output.

This page defines reusable analysis rules.

---

# PAGE 4 — EXECUTIVE SUMMARY

## Graph 1 — Shift-Based Average Stress

### Chart Type
Bar Chart

### Required Columns
- timestamp
- stress_score
- message
- is_ekg_quality

### Required Processing
- valid row filtering
- shift assignment

### Metric Definition

Average Stress by Shift:

mean(stress_score)

using valid rows only.

### Expected Output DataFrame

| shift | avg_stress | valid_count |

### Output Figure

outputs/figures/page_04_shift_avg_stress.png

---

## Graph 2 — Shift-Based Critical Stress Ratio

### Chart Type
Bar Chart

### Required Columns
- timestamp
- stress_score
- message
- is_ekg_quality

### Required Processing
- valid row filtering
- shift assignment
- critical stress masking

### Metric Definition

critical_stress_ratio =
critical_stress_count / valid_count * 100

Critical stress:
- stress_score >= 8

### Expected Output DataFrame

| shift | critical_stress_count | valid_count | critical_stress_ratio |

### Output Figure

outputs/figures/page_04_critical_stress_ratio.png

---

## Graph 3 — Driver-Based Critical Exposure

### Chart Type
Bar Chart

### Required Columns
- driver_id
- stress_score
- hr
- message
- is_ekg_quality

### Required Processing
- valid row filtering
- critical event masking

### Metric Definition

critical_event_count per driver

Critical event:
- stress_score >= 8
- hr >= 100

### Expected Output DataFrame

| driver_id | critical_event_count | valid_count |

### Output Figure

outputs/figures/page_04_driver_critical_exposure.png

### Open Questions

- Should exposure be normalized by valid duration?
- Are all drivers recorded for equal duration?

---

# PAGE 5 — SHIFT-BASED STRESS ANALYSIS

## Graph 1 — Hourly Average Stress by Shift

### Chart Type
3 Line Charts

### Required Columns
- timestamp
- stress_score
- message
- is_ekg_quality

### Required Processing
- valid row filtering
- shift assignment
- hour extraction

### Metric Definition

mean(stress_score)
grouped by:
- shift
- hour

### Expected Output DataFrame

| shift | hour | avg_stress | valid_count |

### Output Figure

outputs/figures/page_05_hourly_stress_by_shift.png

### Open Questions

- Use real hour or shift-relative hour?
(Currently real hour)

---

## Graph 2 — Daily Average Stress

### Chart Type
Line Chart

### Required Columns
- timestamp
- stress_score
- message
- is_ekg_quality

### Required Processing
- valid row filtering
- date extraction

### Metric Definition

mean(stress_score)
grouped by date

### Expected Output DataFrame

| date | avg_stress | valid_count |

### Output Figure

outputs/figures/page_05_daily_avg_stress.png

### Open Questions

- How should daily shift color be assigned if multiple shifts exist in one day?

---

# PAGE 6 — SHIFT-BASED FATIGUE ANALYSIS

## Graph 1 — Hourly Average Fatigue by Shift

### Chart Type
3 Line Charts

### Required Columns
- timestamp
- fatigue_score
- message
- is_ekg_quality

### Required Processing
- valid row filtering
- shift assignment
- hour extraction

### Metric Definition

mean(fatigue_score)
grouped by:
- shift
- hour

### Expected Output DataFrame

| shift | hour | avg_fatigue | valid_count |

### Output Figure

outputs/figures/page_06_hourly_fatigue_by_shift.png

---

## Graph 2 — End-of-Shift Fatigue

### Chart Type
Bar Chart

### Required Columns
- timestamp
- fatigue_score
- message
- is_ekg_quality

### Required Processing
- valid row filtering
- shift assignment
- end-of-shift window extraction

### Metric Definition

mean(fatigue_score)
during last 60 minutes of shift

### Expected Output DataFrame

| shift | avg_end_shift_fatigue | valid_count |

### Output Figure

outputs/figures/page_06_end_shift_fatigue.png

### Open Questions

- Are shift boundaries fixed?
- Is data continuous enough for last-60-minute analysis?

---

# PAGE 7 — DRIVER-BASED PHYSIOLOGICAL EXPOSURE

## Graph 1 — Stress-Fatigue Driver Profile

### Chart Type
Scatter Plot

### Required Columns
- driver_id
- stress_score
- fatigue_score
- message
- is_ekg_quality

### Metric Definition

mean(stress_score)
mean(fatigue_score)
grouped by driver

### Expected Output DataFrame

| driver_id | avg_stress | avg_fatigue | valid_count |

### Output Figure

outputs/figures/page_07_driver_profile.png

---

## Graph 2 — Critical Load Density

### Chart Type
Bubble Chart

### Required Columns
- driver_id
- stress_score
- hr
- message
- is_ekg_quality

### Metric Definition

Bubble size:
critical_event_count

Y axis:
avg_stress

### Expected Output DataFrame

| driver_id | avg_stress | critical_event_count | valid_count |

### Output Figure

outputs/figures/page_07_driver_critical_density.png

---

# PAGE 8 — CRITICAL EVENT TIME ANALYSIS

## Graph 1 — Hourly Critical Event Ratio

### Chart Type
Line Chart

### Required Columns
- timestamp
- stress_score
- hr
- message
- is_ekg_quality

### Metric Definition

critical_event_ratio =
critical_event_count / valid_count * 100

grouped by hour

### Expected Output DataFrame

| hour | critical_event_count | valid_count | critical_event_ratio |

### Output Figure

outputs/figures/page_08_hourly_critical_ratio.png

---

## Graph 2 — Daily Critical Event Ratio

### Chart Type
Line Chart

### Required Columns
- timestamp
- stress_score
- hr
- message
- is_ekg_quality

### Metric Definition

critical_event_ratio =
critical_event_count / valid_count * 100

grouped by date

### Expected Output DataFrame

| date | critical_event_count | valid_count | critical_event_ratio |

### Output Figure

outputs/figures/page_08_daily_critical_ratio.png

---

# PAGE 9 — STRESS–HEART RATE RELATIONSHIP

## Graph 1 — Stress vs Heart Rate Scatter

### Chart Type
Scatter Plot

### Required Columns
- stress_score
- hr
- message
- is_ekg_quality

### Metric Definition

All valid rows.

Optional:
Pearson correlation coefficient.

### Expected Output DataFrame

| stress_score | hr |

### Output Figure

outputs/figures/page_09_stress_hr_scatter.png

---

## Graph 2 — Heart Rate by Stress Category

### Chart Type
Boxplot

### Required Columns
- stress_score
- hr
- message
- is_ekg_quality

### Required Processing

Stress categories:
- 0–3 → low
- 4–5 → medium
- 6–7 → high
- 8–9 → critical

### Expected Output DataFrame

| stress_category | hr |

### Output Figure

outputs/figures/page_09_hr_by_stress_category.png

---

# GLOBAL OPEN QUESTIONS

## Data

- exact timestamp column name
- exact stress column name
- exact fatigue column name
- exact HR column name
- exact driver column name
- whether route/line columns exist

## Time

- Is each row exactly 1 minute?
- Are there missing minutes?
- How should night shift crossing midnight be handled?

## Reporting

- Should driver exposure be normalized?
- Should shift colors be fixed globally?
- How should dominant shift per day be determined?

---

# ENGINEERING RULES

1. Never filter inside plotting functions.
2. Never duplicate shift logic.
3. Never hardcode thresholds across multiple files.
4. Every metric function should return a dataframe.
5. Every figure should have a stable output path.
6. All thresholds and shift definitions should live in config.
7. Use reusable metric functions instead of page-specific logic.