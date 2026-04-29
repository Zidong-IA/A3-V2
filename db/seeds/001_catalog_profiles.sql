-- Ejecutar en el SQL Editor de Supabase después de 002_catalog_tables.sql
-- Catálogo de PERFILES diagnósticos A3 — Datos reales del catálogo 2025
-- Fuente: PDF "A3 - Catalogo 2025" páginas 10-17

INSERT INTO catalog_profiles (code, name, category, species, description, price) VALUES

-- ── PARASITOLÓGICO ────────────────────────────────────────────────────────────
('101', 'Perfil Parasitológico I',   'Parasitológico', 'ambos',  '3 muestras seriadas de Coprológico', 30000),
('102', 'Perfil Parasitológico II',  'Parasitológico', 'ambos',  'Coprológico y Coproscópico', 23000),
('103', 'Perfil Parasitológico III', 'Parasitológico', 'ambos',  '3 muestras seriadas de Coproscópico', 40000),
('104', 'Perfil Parasitológico IV',  'Parasitológico', 'ambos',  'Parcial de Orina y Coprológico', 25000),

-- ── GENERAL ───────────────────────────────────────────────────────────────────
('151', 'Perfil General', 'General', 'ambos', 'Cuadro Hemático, Parcial de Orina, Coprológico', 32000),

-- ── PREQUIRÚRGICO ─────────────────────────────────────────────────────────────
('152', 'Perfil Prequirúrgico I',    'Prequirúrgico', 'ambos', 'Cuadro Hemático, ALT, Creatinina', 24000),
('153', 'Perfil Prequirúrgico II',   'Prequirúrgico', 'ambos', 'Cuadro Hemático, ALT, Creatinina, Glucosa', 36000),
('154', 'Perfil Prequirúrgico III',  'Prequirúrgico', 'ambos', 'Cuadro Hemático, ALT, Creatinina, BUN/UREA, Parcial Orina', 38000),
('155', 'Perfil Prequirúrgico IV',   'Prequirúrgico', 'ambos', 'Cuadro Hemático, ALT, Creatinina, Parcial Orina', 36000),
('156', 'Perfil Prequirúrgico V',    'Prequirúrgico', 'ambos', 'Cuadro Hemático, ALT, Creatinina, Coprológico', 27000),
('157', 'Perfil Prequirúrgico VI',   'Prequirúrgico', 'ambos', 'Cuadro Hemático, ALT, Creatinina, Hemoparásitos', 30000),
('158', 'Perfil Prequirúrgico VII',  'Prequirúrgico', 'ambos', 'Cuadro Hemático, ALT, Creatinina, PT, PTT', 58000),
('159', 'Perfil Prequirúrgico VIII', 'Prequirúrgico', 'ambos', 'Cuadro Hemático, ALT, Creatinina, BUN/UREA, Fosfatasa Alcalina', 48000),
('160', 'Perfil Prequirúrgico IX',   'Prequirúrgico', 'ambos', 'Cuadro Hemático, ALT, Creatinina, BUN/UREA, Fosfatasa Alcalina, Hemoparásitos', 55000),
('161', 'Perfil Prequirúrgico X',    'Prequirúrgico', 'ambos', 'PT, PTT, Dímero D', 90000),
('162', 'Perfil Prequirúrgico XI',   'Prequirúrgico', 'ambos', 'Cuadro Hemático, Creatinina', 20000),

-- ── CACHORROS ─────────────────────────────────────────────────────────────────
('201', 'Perfil Cachorros I',    'Cachorros', 'ambos',  'Cuadro Hemático, Parcial de Orina, Coprológico, Hemoparásitos', 39000),
('202', 'Perfil Cachorros II',   'Cachorros', 'canino', 'Cuadro Hemático, Parvovirus Canino (Ag)', 46000),
('203', 'Perfil Cachorros III',  'Cachorros', 'canino', 'Cuadro Hemático, Distemper Canino (Ag), Parvovirus Canino (Ag), Coronavirus (Ag)', 113000),
('204', 'Perfil Cachorros IV',   'Cachorros', 'canino', 'Cuadro Hemático, Parvovirus Canino (Ag), Coronavirus (Ag)', 65000),
('205', 'Perfil Cachorros V',    'Cachorros', 'canino', 'Cuadro Hemático, Parvovirus Canino (Ag), Coronavirus Canino (Ag), Giardia (Ag)', 80000),
('206', 'Perfil Cachorros VI',   'Cachorros', 'canino', 'Cuadro Hemático, Distemper Canino (Ag)', 53000),
('207', 'Perfil Cachorros VII',  'Cachorros', 'ambos',  'Cuadro Hemático, Coprológico', 19000),
('208', 'Perfil Cachorros VIII', 'Cachorros', 'canino', 'Cuadro Hemático, Coprológico, Parvovirus Canino (Ag), Coronavirus (Ag)', 75000),
('209', 'Perfil Cachorros IX',   'Cachorros', 'canino', 'Cuadro Hemático, Coprológico, Parvovirus Canino (Ag)', 52000),
('210', 'Perfil Cachorros X',    'Cachorros', 'canino', 'Cuadro Hemático, Distemper Canino (Ag), Parvovirus Canino (Ag)', 89000),
('211', 'Perfil Cachorros XI',   'Cachorros', 'canino', 'Cuadro Hemático, Distemper Canino (Ag) y Adenovirus', 75000),
('212', 'Perfil Cachorros XII',  'Cachorros', 'ambos',  'Cuadro Hemático, Coproscópico', 26000),

-- ── HEMOPARÁSITOS ─────────────────────────────────────────────────────────────
('251', 'Perfil Hemoparásitos I',   'Hemoparásitos', 'canino', 'Cuadro Hemático, Snap 4DX (Anaplasma, Ehrlichia, Borrelia, Dirofilaria) ELISA SNAP', 140000),
('252', 'Perfil Hemoparásitos II',  'Hemoparásitos', 'canino', 'Cuadro Hemático, Lámina Hemoparásitos y Test Ehrlichia canis', 62000),
('253', 'Perfil Hemoparásitos III', 'Hemoparásitos', 'canino', 'Cuadro Hemático, Test Ehrlichia canis', 55000),
('254', 'Perfil Hemoparásitos IV',  'Hemoparásitos', 'ambos',  'Cuadro Hemático y Lámina Hemoparásitos', 20000),
('255', 'Perfil Hemoparásitos V',   'Hemoparásitos', 'canino', 'Cuadro Hemático, Ehrlichia canis y Anaplasma, Lámina Hemoparásitos', 88000),

-- ── FELINOS ───────────────────────────────────────────────────────────────────
('301', 'Perfil Felinos I', 'Felino General', 'felino', 'Cuadro Hemático, Creatinina, GGT, Coproscópico', 43000),
('302', 'Perfil Felino II', 'Felino General', 'felino', 'Creatinina, BUN/UREA, GGT', 27000),
('303', 'Perfil Felino III','Felino General', 'felino', 'Cuadro Hemático, GGT, Creatinina', 20000),
('304', 'Perfil Felino IV', 'Felino General', 'felino', 'Cuadro Hemático, AST, GGT, Creatinina', 32000),
('305', 'Perfil Felino V',  'Felino General', 'felino', 'Cuadro Hemático, ALT, Creatinina, FelV-FIV', 80000),

-- ── INFECCIOSAS FELINAS ───────────────────────────────────────────────────────
('351', 'Perfil Infecciosas Felinas I',    'Infecciosas Felinas', 'felino', 'Cuadro Hemático, Snap Triple Felino (FelV-FIV y Dirofilaria) ELISA SNAP IDEXX', 140000),
('352', 'Perfil Infecciosas Felinas II',   'Infecciosas Felinas', 'felino', 'Cuadro Hemático, FelV-FIV', 65000),
('353', 'Perfil Infecciosas Felinas III',  'Infecciosas Felinas', 'felino', 'Cuadro Hemático, Toxoplasma (Anticuerpo)', 60000),
('354', 'Perfil Infecciosas Felinas IV',   'Infecciosas Felinas', 'felino', 'Cuadro Hemático, FIV-FelV, PIF (ELISA INMUNOCOMB)', 165000),
('355', 'Perfil Infecciosas Felinas V',    'Infecciosas Felinas', 'felino', 'Cuadro Hemático, FIV-FelV y Dirofilaria (ELISA SNAP IDEXX), PIF (ELISA INMUNOCOMB)', 235000),
('356', 'Perfil Infecciosas Felina VI',    'Infecciosas Felinas', 'felino', 'Cuadro Hemático, Panleucopenia Felina (Antígeno)', 60000),
('357', 'Perfil Infecciosas Felina VII',   'Infecciosas Felinas', 'felino', 'FIV-FelV, PIF (ELISA INMUNOCOMB)', 150000),
('358', 'Perfil Infecciosas Felina VIII',  'Infecciosas Felinas', 'felino', 'FIV-FelV-Dirofilaria (ELISA SNAP IDEXX), PIF (ELISA INMUNOCOMB)', 220000),
('359', 'Perfil Infecciosas Felina IX',    'Infecciosas Felinas', 'felino', 'Cuadro Hemático, FIV-FelV, Hemoparásitos', 70000),
('360', 'Perfil Infecciosas Felina X',     'Infecciosas Felinas', 'felino', 'Cuadro Hemático, Herpesvirus Felino (Ac) Vcheck, Panleucopenia (Ac) Vcheck, Calicivirus (Ac) Vcheck', 160000),
('361', 'Perfil Infecciosas Felina XI',    'Infecciosas Felinas', 'felino', 'Herpesvirus Felino (Ac) Vcheck, Panleucopenia (Ac) Vcheck, Calicivirus (Ac) Vcheck', 150000),

-- ── HEPÁTICO CANINO ───────────────────────────────────────────────────────────
('401', 'Perfil Hepático Canino I',   'Hepático', 'canino', 'Cuadro Hemático, ALT, AST, Fosfatasa Alcalina', 37000),
('402', 'Perfil Hepático Canino II',  'Hepático', 'canino', 'Cuadro Hemático, ALT, AST, Bilirrubinas Diferenciadas', 38000),
('403', 'Perfil Hepático Canino III', 'Hepático', 'canino', 'Cuadro Hemático, ALT, AST, GGT, Fosfatasa Alcalina, Bilirrubinas Diferenciadas', 53000),
('404', 'Perfil Hepático Canino IV',  'Hepático', 'canino', 'ALT, AST, GGT, Fosfatasa Alcalina, Bilirrubinas Diferenciadas', 44000),

-- ── HEPÁTICO FELINO ───────────────────────────────────────────────────────────
('451', 'Perfil Hepático Felino I',   'Hepático', 'felino', 'Cuadro Hemático, ALT, GGT, Fosfatasa Alcalina', 37000),
('452', 'Perfil Hepático Felino II',  'Hepático', 'felino', 'Cuadro Hemático, ALT, GGT, Bilirrubinas Diferenciadas', 38000),
('453', 'Perfil Hepático Felino III', 'Hepático', 'felino', 'Cuadro Hemático, ALT, GGT, Fosfatasa Alcalina, Bilirrubinas Diferenciadas', 49000),
('454', 'Perfil Hepático Felino IV',  'Hepático', 'felino', 'ALT, AST, GGT, Fosfatasa Alcalina, Bilirrubinas Diferenciadas', 44000),
('455', 'Perfil Hepático Felino V',   'Hepático', 'felino', 'ALT, AST, GGT, Bilirrubinas Diferenciadas', 35000),

-- ── RENAL ─────────────────────────────────────────────────────────────────────
('501', 'Perfil Renal I',    'Renal', 'ambos', 'Cuadro Hemático, Parcial de Orina, BUN/UREA, Creatinina', 34000),
('502', 'Perfil Renal II',   'Renal', 'ambos', 'BUN/UREA, Creatinina, Parcial de Orina', 25000),
('503', 'Perfil Renal III',  'Renal', 'ambos', 'BUN/UREA, Creatinina', 18000),
('504', 'Perfil Renal IV',   'Renal', 'ambos', 'Cuadro Hemático, Parcial de Orina', 22000),
('505', 'Perfil Renal V',    'Renal', 'ambos', 'SDMA, Parcial de Orina', 155000),
('506', 'Perfil Renal VI',   'Renal', 'ambos', 'SDMA, Creatinina', 151000),
('507', 'Perfil Renal VII',  'Renal', 'ambos', 'Cuadro Hemático, BUN/UREA, Creatinina, Sodio, Potasio, Fósforo', 65000),
('508', 'Perfil Renal VIII', 'Renal', 'ambos', 'Cuadro Hemático, BUN/UREA, Creatinina, SDMA, Parcial de Orina', 162000),

-- ── PANCREÁTICO ───────────────────────────────────────────────────────────────
('551', 'Perfil Pancreático I',   'Pancreático', 'ambos',  'Cuadro Hemático, Amilasa, ALT, Glucosa', 37000),
('552', 'Perfil Pancreático II',  'Pancreático', 'ambos',  'Cuadro Hemático, Lipasa, Amilasa', 28000),
('553', 'Perfil Pancreático III', 'Pancreático', 'ambos',  'Cuadro Hemático, Amilasa, Lipasa, ALT, Glucosa', 45000),
('554', 'Perfil Pancreático IV',  'Pancreático', 'canino', 'Cuadro Hemático, Lipasa Pancreática Canina', 70000),
('555', 'Perfil Pancreático V',   'Pancreático', 'felino', 'Cuadro Hemático, Lipasa Pancreática Felina', 72000),
('556', 'Perfil Pancreático VI',  'Pancreático', 'canino', 'Cuadro Hemático, Lipasa Pancreática Canina, Amilasa', 74000),
('557', 'Perfil Pancreático VII', 'Pancreático', 'felino', 'Cuadro Hemático, Lipasa Pancreática Felina, Amilasa', 76000),

-- ── TIROIDEO ──────────────────────────────────────────────────────────────────
('601', 'Perfil Tiroideo Felino I',  'Tiroideo', 'felino', 'T3 Total, T4 Total', 62000),
('602', 'Perfil Tiroideo Canino I',  'Tiroideo', 'canino', 'T4 Canino, Colesterol', 39000),
('603', 'Perfil Tiroideo Canino II', 'Tiroideo', 'canino', 'TSH, T4 Canino', 60000),
('604', 'Perfil Tiroideo Canino III','Tiroideo', 'canino', 'TSH, T4 Canino, Colesterol', 70000),
('605', 'Perfil Tiroideo Canino IV', 'Tiroideo', 'canino', 'TSH, T4 Canino, Colesterol, Triglicéridos', 80000),
('606', 'Perfil Tiroideo Canino V',  'Tiroideo', 'canino', 'TSH Canino Vcheck, T4 Canino Vcheck, Colesterol', 120000),
('607', 'Perfil Tiroideo Canino VI', 'Tiroideo', 'canino', 'TSH Canino Vcheck, T4 Canino Vcheck, Colesterol, Triglicéridos', 135000),
('608', 'Perfil Tiroideo Felino II', 'Tiroideo', 'felino', 'T3 Total, T4 Total Felina Vcheck', 88000),
('609', 'Perfil Tiroideo Felino III','Tiroideo', 'felino', 'T3 Total, T4 Total, Colesterol, Triglicéridos', 80000),
('610', 'Perfil Tiroideo Canino VII','Tiroideo', 'canino', 'Cortisol, Colesterol, Triglicéridos', 49000),

-- ── SENIOR CANINO ─────────────────────────────────────────────────────────────
('651', 'Perfil Senior Canino I',   'Senior', 'canino', 'Cuadro Hemático, Creatinina, BUN/UREA, ALT, Glucosa', 39000),
('652', 'Perfil Senior Canino II',  'Senior', 'canino', 'Cuadro Hemático, Creatinina, BUN/UREA, Parcial Orina, T4 Canina', 73000),
('653', 'Perfil Senior Canino III', 'Senior', 'canino', 'Cuadro Hemático, BUN/UREA, Creatinina, ALT, Fosfatasa Alcalina, Parcial de Orina', 58000),
('654', 'Perfil Senior Canino IV',  'Senior', 'canino', 'Cuadro Hemático, Colesterol, Sodio, Cloro, Potasio, Calcio', 59000),
('655', 'Perfil Senior Canino V',   'Senior', 'canino', 'Cuadro Hemático, Glucosa, Creatinina, BUN/UREA, ALT, Fosfatasa Alcalina, Colesterol, Triglicéridos, Calcio, Parcial de Orina, T4 Canina', 130000),
('656', 'Perfil Senior Canino VI',  'Senior', 'canino', 'Cuadro Hemático, Glucosa, Creatinina, Fosfatasa Alcalina, Parcial de Orina', 46000),

-- ── SENIOR FELINO ─────────────────────────────────────────────────────────────
('657', 'Perfil Senior Felino I',  'Senior', 'felino', 'Cuadro Hemático, Creatinina, BUN/UREA, Parcial Orina, T4 Total', 75000),
('658', 'Perfil Senior Felino II', 'Senior', 'felino', 'Cuadro Hemático, Glucosa, Creatinina, BUN/UREA, ALT, Fosfatasa Alcalina, Colesterol, Triglicéridos, Calcio, Parcial de Orina, T4 Total', 130000),

-- ── DIABÉTICO ─────────────────────────────────────────────────────────────────
('701', 'Perfil Diabético I',   'Diabético', 'ambos', 'Parcial de Orina, Glucosa', 16000),
('702', 'Perfil Diabético II',  'Diabético', 'ambos', 'Cuadro Hemático, Parcial de Orina, Glucosa, Creatinina', 40000),
('703', 'Perfil Diabético III', 'Diabético', 'ambos', 'Cuadro Hemático, Glucosa, Insulina', 47000),
('704', 'Perfil Diabético IV',  'Diabético', 'ambos', 'Cuadro Hemático, Glucosa, Insulina, Fructosamina', 59000),
('705', 'Perfil Diabético V',   'Diabético', 'ambos', 'Glucosa, Insulina, Fructosamina', 50000),

-- ── DERMATOLÓGICO ─────────────────────────────────────────────────────────────
('751', 'Perfil Dermatológico I',        'Dermatológico', 'canino', 'Cuadro Hemático, Raspado de Piel, Fosfatasa Alcalina, Colesterol, T4 Canino', 70000),
('752', 'Perfil Dermatológico II',       'Dermatológico', 'ambos',  'Cuadro Hemático, Raspado de Piel, Cultivo y Antibiograma', 52000),
('753', 'Perfil Dermatológico III',      'Dermatológico', 'ambos',  'Cuadro Hemático, Raspado de Piel', 17000),
('754', 'Perfil Dermatológico IV',       'Dermatológico', 'canino', 'Cuadro Hemático, Raspado de Piel, T4 Canino, Colesterol, Triglicéridos, Fosfatasa Alcalina', 80000),
('755', 'Perfil Dermatológico Felino I', 'Dermatológico', 'felino', 'Cuadro Hemático, Raspado de Piel, Fosfatasa Alcalina, Colesterol, T4 Total', 70000),
('756', 'Perfil Dermatológico Felino II','Dermatológico', 'felino', 'Cuadro Hemático, Raspado de Piel, T4 Total, Colesterol, Triglicéridos, Fosfatasa Alcalina', 80000),

-- ── ELECTROLITOS ──────────────────────────────────────────────────────────────
('801', 'Perfil Electrolitos I',   'Electrolitos', 'ambos', 'Sodio, Cloro, Calcio', 28000),
('802', 'Perfil Electrolitos II',  'Electrolitos', 'ambos', 'Sodio y Potasio', 19000),
('803', 'Perfil Electrolitos III', 'Electrolitos', 'ambos', 'Sodio, Cloro y Potasio', 28000),
('804', 'Perfil Electrolitos IV',  'Electrolitos', 'ambos', 'Calcio Total, Fósforo, Magnesio, Potasio, Sodio, Cloro', 60000),

-- ── CONVULSIVO ────────────────────────────────────────────────────────────────
('851', 'Perfil Convulsivo Canino I',  'Convulsivo', 'canino', 'Cuadro Hemático, Glucosa, ALT, Fosfatasa Alcalina, BUN/Urea, Calcio, Amonio, Electrolitos (Na, K, Cl)', 112000),
('852', 'Perfil Convulsivo Canino II', 'Convulsivo', 'canino', 'Cuadro Hemático, Glucosa, ALT, AST, Creatinina, BUN/Urea, Amonio, Parcial de Orina', 93000),
('861', 'Perfil Convulsivo Felino',    'Convulsivo', 'felino', 'Cuadro Hemático, Glucosa, GGT, BUN/Urea, Calcio, Amonio, Toxoplasma (Anticuerpo)', 100000),

-- ── CARDIACO ──────────────────────────────────────────────────────────────────
('901', 'Perfil Cardiaco I',   'Cardiaco', 'ambos', 'Cuadro Hemático, CK Fracción MB, Na, K', 43000),
('902', 'Perfil Cardiaco II',  'Cardiaco', 'ambos', 'Cuadro Hemático, CK NAC', 20000),
('903', 'Perfil Cardiaco III', 'Cardiaco', 'ambos', 'Cuadro Hemático, CK Fracción MB, CK NAC, Na, K', 55000),

-- ── TOXICOLÓGICO ──────────────────────────────────────────────────────────────
('951', 'Perfil Toxicológico Warfarina',           'Toxicológico', 'ambos',  'Cuadro Hemático, PT, PTT', 36000),
('952', 'Perfil Toxicológico Órgano Fosforados',   'Toxicológico', 'ambos',  'Cuadro Hemático, Magnesio, BUN/UREA, Creatinina, AST, ALT, Fosfatasa Alcalina, Bilirrubinas Diferenciadas, Amilasa', 90000),
('953', 'Perfil Toxicológico Chocolate y Metilxantinas', 'Toxicológico', 'ambos', 'Cuadro Hemático, Ca, ALT, Amonio, Creatinina', 69000),
('954', 'Perfil Toxicológico Ácido Acetil Salicílico',   'Toxicológico', 'ambos', 'Cuadro Hemático, Amonio, Glucosa, Creatinina, BUN/UREA, Parcial Orina, CK NAC', 93000),
('955', 'Perfil Toxicológico Metaldehído',         'Toxicológico', 'ambos',  'Cuadro Hemático, Creatinina, BUN/UREA, Parcial Orina, Fosfatasa Alcalina, ALT, AST, Glucosa', 78000),
('956', 'Perfil Toxicológico Felinos',             'Toxicológico', 'felino', 'Cuadro Hemático, GGT, Creatinina, BUN/UREA, Glucosa, Parcial Orina', 58000),

-- ── REPRODUCTIVO ──────────────────────────────────────────────────────────────
('980', 'Perfil Control Estro I',         'Reproductivo', 'ambos',  'Citología Vaginal y Progesterona', 42000),
('981', 'Perfil Control Estro II',        'Reproductivo', 'ambos',  'Citología Vaginal y Progesterona Vcheck', 65000),
('985', 'Perfil Control Preñez Canina I', 'Reproductivo', 'canino', 'Progesterona y Preñez (Relaxina) Canina', 90000),
('986', 'Perfil Control Preñez Canina II','Reproductivo', 'canino', 'Progesterona Vcheck y Preñez (Relaxina) Canina', 65000),
('987', 'Perfil Control Preñez Felina',   'Reproductivo', 'felino', 'Progesterona y Preñez (Relaxina) Felina', 90000),

-- ── PANELES QUÍMICA LIOFILIZADA ───────────────────────────────────────────────
('1330', 'Panel Control de Salud',     'Bioquímica', 'ambos',  'Albúmina, ALT, Amilasa, AST, Calcio, CK, Creatinina, Glucosa, Fósforo, Bilirrubina Total, Triglicéridos, Proteína Total, BUN, Relación Albúmina/Globulina, Relación BUN/Creatinina, Globulinas', 108000),
('1331', 'Panel Función Hepática',     'Bioquímica', 'ambos',  'Albúmina, Fosfatasa Alcalina, ALT, AST, GGT, Ácidos Biliares Totales, Bilirrubina Total, Colesterol Total, Proteínas Totales, Relación Albúmina/Globulina, Globulina', 90000),
('1332', 'Panel Función Renal',        'Bioquímica', 'ambos',  'Albúmina, Calcio, Creatinina, Glucosa, Fósforo, tCO2, Ácido Úrico, BUN, Relación BUN/Creatinina', 90000),
('1333', 'Panel Pre-operativos',       'Bioquímica', 'ambos',  'Fosfatasa Alcalina, ALT, AST, CK, Creatinina, Glucosa, LDH, Proteínas Totales, BUN, Relación BUN/Creatinina', 90000),
('1334', 'Panel Inflamación Canina',   'Bioquímica', 'canino', 'Amilasa, Creatinina, Lipasa, BUN, Proteína C reactiva, Relación BUN/Creatinina', 90000),
('1335', 'Panel Inflamación Felina',   'Bioquímica', 'felino', 'Amiloide Sérico Felino, Lipasa, GGT, Fosfatasa Alcalina, Albúmina, Ácidos Biliares Totales, BUN, Creatinina', 90000),
('1336', 'Panel Comprensivo',          'Bioquímica', 'ambos',  'Albúmina, Fosfatasa Alcalina, ALT, Amilasa, Colinesterasa, Creatinina, Glucosa, Potasio, Sodio, Bilirrubina Total, Proteínas Totales, Ácido Úrico, BUN, Relación Albúmina/Globulina, Relación BUN/Creatinina, Globulina', 95000),
('1337', 'Panel Diagnóstico Primario', 'Bioquímica', 'ambos',  'Albúmina, Fosfatasa Alcalina, ALT, Creatinina, Glucosa, Proteínas Totales, BUN, Relación Albúmina/Globulina, Relación BUN/Creatinina, Globulina', 108000),
('1338', 'Panel Diabetes',             'Bioquímica', 'ambos',  'AST, ALT, Glucosa, Lactato, Fructosamina, Amilasa, Triglicéridos, Colesterol Total, Lipasa', 90000),
('1339', 'Panel Generales de Salud',   'Bioquímica', 'ambos',  'Albúmina, Creatinina, BUN, Lipasa, Amilasa, LDH, AST, Proteínas Totales, Bilirrubina Total, Calcio, CK, tCO2, GGT, Triglicéridos, Fósforo, Glucosa, Ácidos Biliares Totales, Fosfatasa Alcalina, ALT, Colesterol, Globulina, Relación Albúmina/Globulina, Relación BUN/Creatinina', 155000)

ON CONFLICT (code) DO UPDATE SET
    name        = EXCLUDED.name,
    category    = EXCLUDED.category,
    species     = EXCLUDED.species,
    description = EXCLUDED.description,
    price       = EXCLUDED.price,
    is_active   = EXCLUDED.is_active;
