def retornar_status_inteiro(valor):
    if valor == 'AT':
        return "Ativo"
    elif valor == 'CA':
        return "CAR em conflito"
    elif valor == 'SU':
        return "Suspenso"
    else:
        return "em Manutenção"

def retornar_lei(objeto):
    if objeto is None:
        return "Sem Lei"
    else:
        return str(objeto)


def deve_incluir_por_percentual(area_sobreposicao: float, area_total: float, percentual_limite: float) -> bool:
    """Define se um item deve ser incluído com base no percentual de sobreposição.

    - Retorna True quando o percentual de sobreposição é menor que o limite.
    - Se a área total não for positiva (<= 0) ou nula, não aplica a regra e retorna True.
    - Em caso de erro de cálculo, retorna True por segurança.
    """
    try:
        if area_total is None or area_total <= 0:
            return True
        percentual_sobreposicao = area_sobreposicao / area_total
        return percentual_sobreposicao < percentual_limite
    except Exception:
        return True