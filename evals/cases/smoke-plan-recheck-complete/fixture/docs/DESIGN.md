# Accepted design D1
The exporter adds an explicit format=json option while retaining CSV as the default. Client A is separately deployed and enables JSON only after the exporter supports it. Client B sends no format option. A rollout is not complete until both A JSON and B default CSV acceptance pass. No CSV removal or B deployment is needed.
