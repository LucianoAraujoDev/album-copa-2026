# data.py — Seções e figurinhas do álbum Copa do Mundo 2026
# Estrutura idêntica ao álbum físico (Numeração por prefixo de seleção)

# Lista auxiliar para mapear o prefixo/identificador de numeração de cada seção
ESTRUTURA_ALBUM = [
    {"nome": "Especiais", "emoji": "FWC", "prefixo": "FWC", "tamanho": 18},
    {"nome": "México", "emoji": "🇲🇽", "prefixo": "MEX", "tamanho": 20},
    {"nome": "África do Sul", "emoji": "🇿🇦", "prefixo": "RSA", "tamanho": 20},
    {"nome": "Coréia do Sul", "emoji": "🇰🇷", "prefixo": "KOR", "tamanho": 20},
    {"nome": "República Theca", "emoji": "🇨🇿", "prefixo": "CZE", "tamanho": 20},
    {"nome": "Canadá", "emoji": "🇨🇦", "prefixo": "CAN", "tamanho": 20},
    {"nome": "Bósnia-Herzegovina", "emoji": "🇧🇦", "prefixo": "BIH", "tamanho": 20},
    {"nome": "Catar", "emoji": "🇶🇦", "prefixo": "QAT", "tamanho": 20},
    {"nome": "Suíça", "emoji": "🇨🇭", "prefixo": "SUI", "tamanho": 20},
    {"nome": "Brasil", "emoji": "🇧🇷", "prefixo": "BRA", "tamanho": 20},
    {"nome": "Marrocos", "emoji": "🇲🇦", "prefixo": "MAR", "tamanho": 20},
    {"nome": "Haiti", "emoji": "🇭🇹", "prefixo": "HAI", "tamanho": 20},
    {"nome": "Escócia", "emoji": "🏴%A0󠁢󠁳󠁣󠁴󠁿", "prefixo": "SCO", "tamanho": 20},
    {"nome": "Estados Unidos", "emoji": "🇺🇸", "prefixo": "USA", "tamanho": 20},
    {"nome": "Paraguai", "emoji": "🇵🇾", "prefixo": "PAR", "tamanho": 20},
    {"nome": "Austrália", "emoji": "🇦🇺", "prefixo": "AUS", "tamanho": 20},
    {"nome": "Turquia", "emoji": "🇹🇷", "prefixo": "TUR", "tamanho": 20},
    {"nome": "Alemanha", "emoji": "🇩🇪", "prefixo": "GER", "tamanho": 20},
    {"nome": "Curaçao", "emoji": "🇨🇼", "prefixo": "CUW", "tamanho": 20},
    {"nome": "Costa do Marfim", "emoji": "🇨🇮", "prefixo": "CIV", "tamanho": 20},
    {"nome": "Equador", "emoji": "🇪🇨", "prefixo": "ECU", "tamanho": 20},
    {"nome": "Holanda", "emoji": "🇳🇱", "prefixo": "NED", "tamanho": 20},
    {"nome": "Japão", "emoji": "🇯🇵", "prefixo": "JPN", "tamanho": 20},
    {"nome": "Suécia", "emoji": "🇸🇪", "prefixo": "SWE", "tamanho": 20},
    {"nome": "Tunísia", "emoji": "🇹🇳", "prefixo": "TUN", "tamanho": 20},
    {"nome": "Bélgica", "emoji": "🇧🇪", "prefixo": "BEL", "tamanho": 20},
    {"nome": "Egito", "emoji": "🇪🇬", "prefixo": "EGY", "tamanho": 20},
    {"nome": "Irã", "emoji": "🇮🇷", "prefixo": "IRN", "tamanho": 20},
    {"nome": "Nova Zelândia", "emoji": "🇳🇿", "prefixo": "NZL", "tamanho": 20},
    {"nome": "Espanha", "emoji": "🇪🇸", "prefixo": "ESP", "tamanho": 20},
    {"nome": "Cabo Verde", "emoji": "🇨🇻", "prefixo": "CPV", "tamanho": 20},
    {"nome": "Arábia Saudita", "emoji": "🇸🇦", "prefixo": "KSA", "tamanho": 20},
    {"nome": "Uruguai", "emoji": "🇺🇾", "prefixo": "URU", "tamanho": 20},
    {"nome": "França", "emoji": "🇫🇷", "prefixo": "FRA", "tamanho": 20},
    {"nome": "Senegal", "emoji": "🇸🇳", "prefixo": "SEN", "tamanho": 20},
    {"nome": "Iraque", "emoji": "🇮🇶", "prefixo": "IRQ", "tamanho": 20},
    {"nome": "Noruega", "emoji": "🇳🇴", "prefixo": "NOR", "tamanho": 20},
    {"nome": "Argentina", "emoji": "🇦🇷", "prefixo": "ARG", "tamanho": 20},
    {"nome": "Argélia", "emoji": "🇩🇿", "prefixo": "ALG", "tamanho": 20},
    {"nome": "Áustria", "emoji": "🇦🇹", "prefixo": "AUT", "tamanho": 20},
    {"nome": "Jordânia", "emoji": "🇯🇴", "prefixo": "JOR", "tamanho": 20},
    {"nome": "Portugal", "emoji": "🇵🇹", "prefixo": "POR", "tamanho": 20},
    {"nome": "Congo", "emoji": "🇨🇩", "prefixo": "COD", "tamanho": 20},
    {"nome": "Uzbequistão", "emoji": "🇺🇿", "prefixo": "UZB", "tamanho": 20},
    {"nome": "Colômbia", "emoji": "🇨🇴", "prefixo": "COL", "tamanho": 20},
    {"nome": "Inglaterra", "emoji": "🏴%A0󠁢󠁥󠁮󠁧󠁿", "prefixo": "ENG", "tamanho": 20},
    {"nome": "Croácia", "emoji": "🇭🇷", "prefixo": "CRO", "tamanho": 20},
    {"nome": "Gana", "emoji": "🇬🇭", "prefixo": "GHA", "tamanho": 20},
    {"nome": "Panamá", "emoji": "🇵🇦", "prefixo": "PAN", "tamanho": 20},
]

# Construção dinâmica da lista final SECOES_COPA
SECOES_COPA = []

for secao in ESTRUTURA_ALBUM:
    # Cria a lista de figurinhas como strings: ["🇲🇽 1", "🇲🇽 2", ... "🇲🇽 20"]
    # Se você preferir usar as siglas (ex: "MEX 1"), basta trocar secao["emoji"] por secao["prefixo"] abaixo.
    lista_figurinhas = [f"{secao['prefixo']} {i}" for i in range(1, secao["tamanho"] + 1)]
    
    SECOES_COPA.append({
        "nome": secao["nome"],
        "emoji": secao["prefixo"],
        "figurinhas": lista_figurinhas
    })