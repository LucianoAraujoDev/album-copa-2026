# data.py — Seções e figurinhas do álbum Copa do Mundo 2026
# Estrutura baseada em álbuns Panini típicos de Copa

SECOES_COPA = [
    {
        "nome": "Abertura",
        "emoji": "🌟",
        "figurinhas": list(range(1, 19)),
    },
    {
        "nome": "Estádios",
        "emoji": "🏟️",
        "figurinhas": list(range(19, 37)),
    },
    {
        "nome": "México",
        "emoji": "MEX",
        "figurinhas": list(range(37, 57)),
    },
    {
        "nome": "África do Sul",
        "emoji": "RSA",
        "figurinhas": list(range(57, 77)),
    },
    {
        "nome": "Coréia do Sul",
        "emoji": "KOR",
        "figurinhas": list(range(77, 97)),
    },
    {
        "nome": "República Theca",
        "emoji": "CZE",
        "figurinhas": list(range(97, 117)),
    },
    {
        "nome": "Canadá",
        "emoji": "CAN",
        "figurinhas": list(range(117, 137)),
    },
    {
        "nome": "Bósnia-Herzegovina",
        "emoji": "BIH",
        "figurinhas": list(range(137, 157)),
    },
    {
        "nome": "Catar",
        "emoji": "Qat",
        "figurinhas": list(range(157, 177)),
    },
    {
        "nome": "Suíça",
        "emoji": "SUI",
        "figurinhas": list(range(177, 197)),
    },
    {
        "nome": "Brasil",
        "emoji": "🇧🇷",  # Atualizado para o emoji da bandeira para ficar mais visual
        "figurinhas": list(range(197, 217)),
    },
    {
        "nome": "Marrocos",
        "emoji": "MAR",
        "figurinhas": list(range(217, 237)),
    },
    {
        "nome": "Haiti",
        "emoji": "HAI",
        "figurinhas": list(range(237, 257)),
    },
    {
        "nome": "Escócia",
        "emoji": "SCO",
        "figurinhas": list(range(257, 277)),
    },
    {
        "nome": "Estados Unidos",  # Corrigido: adicionada a vírgula
        "emoji": "USA",           # Corrigido: adicionadas as aspas e a vírgula
        "figurinhas": list(range(277, 297)),
    },
    {
        "nome": "Paraguai",
        "emoji": "PAR",
        "figurinhas": list(range(297, 317)),
    },
    {
        "nome": "Austrália",
        "emoji": "AUS",
        "figurinhas": list(range(317, 337)),
    },
    {
        "nome": "Turquia",
        "emoji": "TUR",
        "figurinhas": list(range(337, 357)),
    },
    {
        "nome": "Alemanha",
        "emoji": "GER",
        "figurinhas": list(range(357, 377)),
    },
    {
        "nome": "Curaçao",
        "emoji": "CUW",
        "figurinhas": list(range(377, 397)),
    },
    {
        "nome": "Costa do Marfim",
        "emoji": "CIV",
        "figurinhas": list(range(397, 417)),
    },
    {
        "nome": "Equador",
        "emoji": "ECU",
        "figurinhas": list(range(417, 437)),
    },
    {
        "nome": "Holanda",
        "emoji": "NED",
        "figurinhas": list(range(437, 457)),
    },
    {
        "nome": "Japão",
        "emoji": "JPN",
        "figurinhas": list(range(457, 477)),
    },
    {
        "nome": "Suécia",
        "emoji": "SWE",
        "figurinhas": list(range(477, 497)),
    },
    {
        "nome": "Tunísia",
        "emoji": "TUN",
        "figurinhas": list(range(497, 517)),
    },
    {
        "nome": "Bélgica",
        "emoji": "BEL",
        "figurinhas": list(range(517, 537)),
    },
    {
        "nome": "Egito",
        "emoji": "EGY",
        "figurinhas": list(range(537, 557)),
    },
    {
        "nome": "Irã",
        "emoji": "IRN",
        "figurinhas": list(range(557, 577)),
    },
    {
        "nome": "Nova Zelândia",
        "emoji": "NZL",
        "figurinhas": list(range(577, 597)),
    },
    {
        "nome": "Espanha",
        "emoji": "ESP",
        "figurinhas": list(range(597, 617)),
    },
    {
        "nome": "Cabo Verde",
        "emoji": "CBV",
        "figurinhas": list(range(617, 637)),
    },
    {
        "nome": "Arábia Saudita",
        "emoji": "KSA",
        "figurinhas": list(range(637, 657)),
    },
    {
        "nome": "Uruguai",
        "emoji": "URU",
        "figurinhas": list(range(657, 677)),
    },
    {
        "nome": "França",
        "emoji": "FRA",
        "figurinhas": list(range(677, 697)),
    },
    {
        "nome": "Senegal",
        "emoji": "SEN",
        "figurinhas": list(range(697, 717)),
    },
    {
        "nome": "Iraque",
        "emoji": "IRQ",
        "figurinhas": list(range(717, 737)),
    },
    {
        "nome": "Noruega",
        "emoji": "NOR",
        "figurinhas": list(range(737, 757)),
    },
    {
        "nome": "Argentina",
        "emoji": "ARG",
        "figurinhas": list(range(757, 777)),
    },
    {
        "nome": "Argélia",
        "emoji": "ALG",
        "figurinhas": list(range(777, 797)),
    },
    {
        "nome": "Áustria",
        "emoji": "AUT",
        "figurinhas": list(range(797, 817)),
    },
    {
        "nome": "Jordânia",
        "emoji": "JOR",
        "figurinhas": list(range(817, 837)),
    },
    {
        "nome": "Portugal",        # Corrigido: adicionadas as aspas e a vírgula
        "emoji": "POR",
        "figurinhas": list(range(837, 857)),  # Ajustado: o range recua para cobrir o buraco do Brasil removido
    },
    {
        "nome": "Congo",
        "emoji": "COD",
        "figurinhas": list(range(857, 877)),  # Reajustado sequencialmente
    },
    {
        "nome": "Uzbequistão",
        "emoji": "UZB",
        "figurinhas": list(range(877, 897)),  # Reajustado sequencialmente
    },
    {
        "nome": "Colômbia",
        "emoji": "COL",
        "figurinhas": list(range(897, 917)),  # Reajustado sequencialmente
    },
    {
        "nome": "Inglaterra",
        "emoji": "ENG",
        "figurinhas": list(range(917, 937)),  # Reajustado sequencialmente
    },
    {
        "nome": "Croácia",
        "emoji": "CRO",
        "figurinhas": list(range(937, 957)),  # Reajustado sequencialmente
    },
    {
        "nome": "Gana",
        "emoji": "GHA",
        "figurinhas": list(range(957, 977)),  # Reajustado sequencialmente
    },
    {
        "nome": "Panamá",
        "emoji": "PAN",
        "figurinhas": list(range(977, 997)),  # Reajustado sequencialmente
    },
    {
        "nome": "Encerramento",
        "emoji": "🏅",
        "figurinhas": list(range(997, 1011)),  # Fechamento perfeito em 1010 figurinhas totais
    },
]
