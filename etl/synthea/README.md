# Synthea Synthetic Data Generation

## Purpose

IndiCare uses synthetic healthcare data generated using Synthea for
educational heart disease prediction and database implementation.

No real patient data is used.

## Data Generation

The synthetic patient population was generated using Synthea.

Population size:

5000 patients

Example generation command:

```text
.\run_synthea -p 5000 Massachusetts "Cardiovascular Disease"