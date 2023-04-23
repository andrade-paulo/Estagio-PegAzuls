def EstimaPesoAsa(corda_ref, envergadura_ref, massa_ref, nova_corda, nova_envergadura):
    # Estima o peso da asa a partir das referências de uma asa anterior
    nova_massa = massa_ref * (nova_corda / corda_ref) * (nova_envergadura / envergadura_ref)
    return nova_massa
