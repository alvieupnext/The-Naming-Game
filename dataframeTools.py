def getConsensusIterationOfSubject(df, patient, convergenceRate, structure = 'SC'):
  patientRows = df.loc[df["subject"] == patient]
  iterationRows = patientRows[f"{structure}_{convergenceRate}"]
  return iterationRows.tolist()
