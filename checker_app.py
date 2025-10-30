from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import math 

app = Flask(__name__, template_folder='.')
CORS(app) 

# -------------------------------------------------------------------
# 1. "BANCO DE DADOS FALSO"
# -------------------------------------------------------------------
CPUS = {
    "1": { "id": "1", "name": "AMD Ryzen 5 5600X", "socket": "AM4", "ram_support_types": ["DDR4"], "tier": 7, "tdp": 65, "image_url": "static/images/amd-ryzen-5-5600x.jpg" },
    "2": { "id": "2", "name": "Intel Core i5-13600K", "socket": "LGA1700", "ram_support_types": ["DDR4", "DDR5"], "tier": 9, "tdp": 125, "image_url": "static/images/intel-i5-13600k.jpg" }
}
MOTHERBOARDS = {
    "101": { "id": "101", "name": "ASUS TUF B550M-PLUS", "socket": "AM4", "ram_type": "DDR4", "image_url": "static/images/asus-tuf-b550m-plus.jpg" },
    "102": { "id": "102", "name": "Gigabyte Z790 AORUS", "socket": "LGA1700", "ram_type": "DDR5", "image_url": "static/images/gigabyte-z790-aorus.jpg" },
    "103": { "id": "103", "name": "ASRock B660M Steel Legend", "socket": "LGA1700", "ram_type": "DDR4", "image_url": "static/images/asrock-b660m-steel-legend.jpg" }
}
RAM_MODULES = {
    "201": { "id": "201", "name": "Corsair Vengeance 16GB (DDR4)", "type": "DDR4", "image_url": "static/images/corsair-vengeance-16gb-ddr4.jpg" },
    "202": { "id": "202", "name": "Kingston Fury 32GB (DDR5)", "type": "DDR5", "image_url": "static/images/kingston-fury-32gb-ddr5.jpg" }
}
GPUS = {
    "301": { "id": "301", "name": "NVIDIA RTX 3060", "min_psu_watts": 550, "tier": 7, "length_mm": 242, "tdp": 170, "image_url": "static/images/nvidia-rtx-3060.png" },
    "302": { "id": "302", "name": "NVIDIA RTX 4080", "min_psu_watts": 750, "tier": 10, "length_mm": 304, "tdp": 320, "image_url": "static/images/nvidia-rtx-4080.png" }
}
PSUS = {
    "401": { "id": "401", "name": "Corsair CV650 (650W)", "wattage": 650, "image_url": "static/images/corsair-cv650.jpg" },
    "402": { "id": "402", "name": "Corsair RM850x (850W)", "wattage": 850, "image_url": "static/images/corsair-rm850x.jpg" }
}
COOLERS = {
    "501": { "id": "501", "name": "Cooler Box Original AMD", "height_mm": 70, "supported_sockets": ["AM4"], "image_url": "static/images/amd-cooler-box.jpg" },
    "502": { "id": "502", "name": "Deepcool AG400", "height_mm": 150, "supported_sockets": ["AM4", "AM5", "LGA1700", "LGA1200"], "image_url": "static/images/deepcool-ag400.jpg" },
    "503": { "id": "503", "name": "Water Cooler Corsair H100i", "height_mm": 52, "supported_sockets": ["AM4", "AM5", "LGA1700"], "image_url": "static/images/corsair-h100i-wc.jpg" }
}
CASES = { 
    "601": { "id": "601", "name": "Gabinete Gamer Mancer Goblin", "gpu_max_length_mm": 280, "cooler_max_height_mm": 160, "image_url": "static/images/mancer-goblin.jpg" },
    "602": { "id": "602", "name": "Gabinete Corsair 4000D Airflow", "gpu_max_length_mm": 360, "cooler_max_height_mm": 170, "image_url": "static/images/corsair-4000d-airflow.jpg" }
}

# --- ATUALIZADO: Lojas com Coordenadas ---
REPAIR_SHOPS = {
    "1001": { "id": "1001", "name": "ConsertaPC Rápido", "type": "pc", "address": "Rua Fictícia, 123 - Centro", "phone": "(21) 99999-1111", "lat": -22.9068, "lng": -43.1729 },
    "1002": { "id": "1002", "name": "SalvaCelular", "type": "celular", "address": "Av. Principal, 456 - Bairro Novo", "phone": "(21) 98888-2222", "lat": -22.9519, "lng": -43.1822 },
    "1003": { "id": "1003", "name": "Dr. Computador & Cia", "type": "pc", "address": "Praça da Tecnologia, 789", "phone": "(21) 97777-3333", "lat": -22.9035, "lng": -43.1795 },
    "1004": { "id": "1004", "name": "Rei do Smartphone", "type": "celular", "address": "Rua Fictícia, 130 - Centro", "phone": "(21) 96666-4444", "lat": -22.9075, "lng": -43.1740 },
    "1005": { "id": "1005", "name": "PC-Help Soluções", "type": "pc", "address": "Av. Principal, 999 - Bairro Novo", "phone": "(21) 95555-5555", "lat": -22.9530, "lng": -43.1830 },
    "1006": { "id": "1006", "name": "Help Informática", "type": "pc", "address": "Rua da Passagem, 50 - Loja B", "phone": "(21) 94444-1111", "lat": -22.9497, "lng": -43.1818 },
    "1007": { "id": "1007", "name": "Solução Notebook", "type": "pc", "address": "Travessa dos Tamoios, 15", "phone": "(21) 93333-2222", "lat": -22.9320, "lng": -43.1799 },
    "1008": { "id": "1008", "name": "SOS Celulares", "type": "celular", "address": "Largo do Machado, 22", "phone": "(21) 92222-3333", "lat": -22.9304, "lng": -43.1788 },
    "1009": { "id": "1009", "name": "Smart Reparo", "type": "celular", "address": "Rua Sete de Setembro, 101", "phone": "(21) 91111-4444", "lat": -22.9048, "lng": -43.1784 }
}
VERIFIED_SHOPS = {
    "2001": { 
        "id": "2001", 
        "name": "Reparo Justo PC", 
        "type": "pc", 
        "address": "Av. Confiança, 10 - Centro", 
        "phone": "(21) 90000-1111",
        "rating": 5, 
        "review": "Preço justo e não tentaram 'empurrar' peças extra.",
        "lat": -22.9050, "lng": -43.1760 # <-- NOVO
    },
    "2002": { 
        "id": "2002", 
        "name": "Celular Honesto", 
        "type": "celular", 
        "address": "Rua da Garantia, 20 - Lapa", 
        "phone": "(21) 90000-2222",
        "rating": 4, 
        "review": "Serviço rápido, mas um pouco mais caro. O problema foi resolvido.",
        "lat": -22.9135, "lng": -43.1800 # <-- NOVO
    },
    "2003": { 
        "id": "2003", 
        "name": "InfoFiel", 
        "type": "pc", 
        "address": "Rua do Técnico, 30", 
        "phone": "(21) 90000-3333",
        "rating": 5, 
        "review": "Especialista em PCs, muito confiável.",
        "lat": -22.9080, "lng": -43.1810 # <-- NOVO
    }
}
# --- FIM DA ATUALIZAÇÃO ---

PREBUILTS = {
    # (O dicionário PREBUILTS completo)
    "1": { "id": "1", "name": "Custo-Benefício (AMD)", "description": "Excelente equilíbrio...", "category": "Custo-Benefício", "parts": {"CPU": "AMD Ryzen 5 5600X", "Placa-mãe": "ASUS TUF B550M-PLUS", "RAM": "Corsair Vengeance 16GB (DDR4)", "GPU": "NVIDIA RTX 3060", "Fonte": "Corsair CV650 (650W)", "Gabinete": "Gabinete Corsair 4000D Airflow", "Cooler": "Deepcool AG400"} },
    "2": { "id": "2", "name": "Custo-Benefício (Intel)", "description": "Ótima performance em jogos...", "category": "Custo-Benefício", "parts": {"CPU": "Intel Core i5-12400F", "Placa-mãe": "ASRock B660M Steel Legend", "RAM": "Corsair Vengeance 16GB (DDR4)", "GPU": "NVIDIA RTX 3060", "Fonte": "Corsair CV650 (650W)", "Gabinete": "Gabinete Corsair 4000D Airflow", "Cooler": "Deepcool AG400"} },
    "3": { "id": "3", "name": "Top de Linha (AMD)", "description": "Performance extrema para 4K...", "category": "Top de Linha", "parts": {"CPU": "AMD Ryzen 7 7800X3D", "Placa-mãe": "Gigabyte B650M AORUS (AM5)", "RAM": "Kingston Fury 32GB (DDR5)", "GPU": "NVIDIA RTX 4080", "Fonte": "Corsair RM850x (850W)", "Gabinete": "Gabinete Corsair 4000D Airflow", "Cooler": "Water Cooler Corsair H100i"} },
    "4": { "id": "4", "name": "Top de Linha (Intel)", "description": "O melhor da Intel para jogos...", "category": "Top de Linha", "parts": {"CPU": "Intel Core i5-13600K", "Placa-mãe": "Gigabyte Z790 AORUS", "RAM": "Kingston Fury 32GB (DDR5)", "GPU": "NVIDIA RTX 4080", "Fonte": "Corsair RM850x (850W)", "Gabinete": "Gabinete Corsair 4000D Airflow", "Cooler": "Water Cooler Corsair H100i"} },
    "5": { "id": "5", "name": "Opção Média (AMD)", "description": "Performance sólida para 1080p.", "category": "Opção Média", "parts": {"CPU": "AMD Ryzen 5 5600X", "Placa-mãe": "ASUS TUF B550M-PLUS", "RAM": "Corsair Vengeance 16GB (DDR4)", "GPU": "AMD Radeon RX 6650 XT", "Fonte": "Corsair CV650 (650W)", "Gabinete": "Gabinete Mancer Goblin", "Cooler": "Cooler Box Original AMD"} },
    "6": { "id": "6", "name": "Opção Média (Intel)", "description": "Eficiente para jogos e estudos.", "category": "Opção Média", "parts": {"CPU": "Intel Core i5-12400F", "Placa-mãe": "ASRock B660M Steel Legend", "RAM": "Corsair Vengeance 16GB (DDR4)", "GPU": "NVIDIA RTX 4060", "Fonte": "Corsair CV650 (650W)", "Gabinete": "Gabinete Mancer Goblin", "Cooler": "Deepcool AG400"} },
    "7": { "id": "7", "name": "Muito Barata (AMD)", "description": "Para jogos leves sem GPU dedicada.", "category": "Muito Barata", "parts": {"CPU": "AMD Ryzen 5 5600G (Gráficos Integrados)", "Placa-mãe": "ASUS Prime A520M", "RAM": "Corsair Vengeance 16GB (DDR4)", "GPU": "Gráficos Integrados Radeon Vega 7", "Fonte": "Fonte Mancer 500W", "Gabinete": "Gabinete Mancer Goblin", "Cooler": "Cooler Box Original AMD"} },
    "8": { "id": "8", "name": "Muito Barata (Intel)", "description": "Ponto de entrada para jogos.", "category": "Muito Barata", "parts": {"CPU": "Intel Core i3-12100F", "Placa-mãe": "Gigabyte H610M", "RAM": "Corsair Vengeance 16GB (DDR4)", "GPU": "NVIDIA GeForce GTX 1660 Super", "Fonte": "Fonte Mancer 500W", "Gabinete": "Gabinete Mancer Goblin", "Cooler": "Cooler Box Original Intel"} }
}

# -------------------------------------------------------------------
# 2. ROTAS PARA API (APIs)
# -------------------------------------------------------------------
@app.route('/api/get-cpus', methods=['GET'])
def get_cpus(): return jsonify(list(CPUS.values()))
@app.route('/api/get-motherboards', methods=['GET'])
def get_motherboards(): return jsonify(list(MOTHERBOARDS.values()))
@app.route('/api/get-ram', methods=['GET'])
def get_ram(): return jsonify(list(RAM_MODULES.values()))
@app.route('/api/get-gpus', methods=['GET'])
def get_gpus(): return jsonify(list(GPUS.values()))
@app.route('/api/get-psus', methods=['GET'])
def get_psus(): return jsonify(list(PSUS.values()))
@app.route('/api/get-coolers', methods=['GET'])
def get_coolers(): return jsonify(list(COOLERS.values()))
@app.route('/api/get-cases', methods=['GET'])
def get_cases(): return jsonify(list(CASES.values()))
@app.route('/api/get-prebuilts', methods=['GET'])
def get_prebuilts(): return jsonify(list(PREBUILTS.values()))

# Rotas de Assistência
@app.route('/api/get-pc-shops', methods=['GET'])
def get_pc_shops(): return jsonify([shop for shop in REPAIR_SHOPS.values() if shop['type'] == 'pc'])
@app.route('/api/get-celular-shops', methods=['GET'])
def get_celular_shops(): return jsonify([shop for shop in REPAIR_SHOPS.values() if shop['type'] == 'celular'])
@app.route('/api/get-verified-shops', methods=['GET'])
def get_verified_shops(): return jsonify(list(VERIFIED_SHOPS.values()))

# -------------------------------------------------------------------
# 3. "MOTOR DE REGRAS" (API)
# -------------------------------------------------------------------
@app.route('/api/check-build', methods=['POST'])
def check_build():
    build = request.json
    incompatibilities = []
    bottlenecks = []
    other_warnings = []
    # (Toda a lógica de verificação está aqui, sem mudanças)
    cpu = CPUS.get(build.get('cpu_id'))
    mobo = MOTHERBOARDS.get(build.get('mobo_id'))
    ram = RAM_MODULES.get(build.get('ram_id'))
    gpu = GPUS.get(build.get('gpu_id'))
    psu = PSUS.get(build.get('psu_id'))
    cooler = COOLERS.get(build.get('cooler_id'))
    case = CASES.get(build.get('case_id'))
    if cpu and mobo:
        if cpu['socket'] != mobo['socket']: incompatibilities.append(f"INCOMPATÍVEL: A CPU {cpu['name']} (soquete {cpu['socket']}) não é compatível com a placa-mãe {mobo['name']} (soquete {mobo['socket']}).")
    if ram and mobo:
        if ram['type'] != mobo['ram_type']: incompatibilities.append(f"INCOMPATÍVEL: A RAM {ram['name']} ({ram['type']}) não é compatível com a placa-mãe {mobo['name']} (requer {mobo['ram_type']}).")
    if cpu and mobo:
        if 'ram_support_types' in cpu and cpu['ram_support_types'] and mobo['ram_type'] not in cpu['ram_support_types']: other_warnings.append(f"AVISO: A placa-mãe {mobo['name']} usa {mobo['ram_type']}, que não é suportado nativamente pelo controlador de memória da CPU {cpu['name']}.")
    if psu and gpu:
        if 'wattage' in psu and 'min_psu_watts' in gpu and psu['wattage'] < gpu['min_psu_watts']: other_warnings.append(f"AVISO DE FONTE: A fonte {psu['name']} ({psu['wattage']}W) está abaixo do recomendado de {gpu['min_psu_watts']}W para a GPU {gpu['name']}.")
    if cpu and gpu:
        if 'tier' in cpu and 'tier' in gpu:
            if gpu['tier'] >= (cpu['tier'] + 3): bottlenecks.append(f"RISCO DE GARGALO: A GPU {gpu['name']} (Nível {gpu['tier']}) é mais potente que a CPU {cpu['name']} (Nível {cpu['tier']}).")
            elif cpu['tier'] >= (gpu['tier'] + 3): bottlenecks.append(f"RISCO DE GARGALO: A CPU {cpu['name']} (Nível {cpu['tier']}) é mais potente que a GPU {gpu['name']} (Nível {gpu['tier']}).")
    if cooler and mobo:
        if 'socket' in mobo and 'supported_sockets' in cooler and mobo['socket'] not in cooler['supported_sockets']: incompatibilities.append(f"INCOMPATÍVEL: O cooler {cooler['name']} não suporta o soquete {mobo['socket']} da placa-mãe.")
    if gpu and case:
        if 'length_mm' in gpu and 'gpu_max_length_mm' in case and gpu['length_mm'] > case['gpu_max_length_mm']: incompatibilities.append(f"INCOMPATÍVEL: A GPU {gpu['name']} ({gpu['length_mm']}mm) não cabe no gabinete {case['name']} (limite: {case['gpu_max_length_mm']}mm).")
    if cooler and case:
        if 'height_mm' in cooler and 'cooler_max_height_mm' in case and cooler['height_mm'] > case['cooler_max_height_mm']: incompatibilities.append(f"INCOMPATÍVEL: O cooler {cooler['name']} ({cooler['height_mm']}mm) é muito alto para o gabinete {case['name']} (limite: {case['cooler_max_height_mm']}mm).")

    response = { 'build_is_compatible': len(incompatibilities) == 0, 'incompatibilities': incompatibilities, 'bottlenecks': bottlenecks, 'other_warnings': other_warnings }
    return jsonify(response)

# -------------------------------------------------------------------
# 4. ROTA PARA CALCULAR CONSUMO (API)
# -------------------------------------------------------------------
@app.route('/api/calculate-wattage', methods=['POST'])
def calculate_wattage():
    build = request.json
    cpu = CPUS.get(build.get('cpu_id'))
    gpu = GPUS.get(build.get('gpu_id'))
    cpu_tdp = cpu.get('tdp', 0) if cpu else 0
    gpu_tdp = gpu.get('tdp', 0) if gpu else 0
    base_load = 120 
    total_estimated_tdp = cpu_tdp + gpu_tdp + base_load
    recommended_psu = math.ceil((total_estimated_tdp * 1.5) / 50) * 50
    recommended_psu = max(recommended_psu, 450) 
    response = { 'estimated_wattage': total_estimated_tdp, 'recommended_wattage': recommended_psu }
    return jsonify(response)

# -------------------------------------------------------------------
# 5. ROTA PARA SERVIR O FRONTEND (O index.html)
# -------------------------------------------------------------------
@app.route('/')
def serve_index():
    return render_template('index.html')

# -------------------------------------------------------------------
# 6. RODA O SERVIDOR (Apenas para testes locais)
# -------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True, port=5000)