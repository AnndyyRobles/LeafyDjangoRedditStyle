def generate_prompt(model):
    """Genera un prompt descriptivo basado en los datos del modelo de cultivo"""
    techniques = {
        'vertical': 'sistema de cultivo vertical con múltiples niveles',
        'pared': 'sistema de cultivo montado en pared',
        'hidroponia': 'sistema hidropónico sin suelo',
        'reciclados': 'huerto urbano usando materiales reciclados',
        'acuaponia': 'sistema acuapónico que combina peces y plantas'
    }
    
    locations = {
        'interior': 'diseñado para espacios interiores',
        'exterior': 'diseñado para espacios exteriores'
    }
    
    # Prompt básico con información esencial
    prompt = f"Crea un modelo 3D detallado de un {techniques[model.technique]} para agricultura urbana, "
    prompt += f"{locations[model.location]}, "
    prompt += f"con dimensiones de {model.width}cm de ancho, {model.height}cm de alto y {model.length}cm de largo. "
    prompt += f"Los materiales incluyen: {model.materials_description}. "
    
    # Agregar especificaciones extra si existen
    if model.extra_specifications:
        prompt += f"Especificaciones adicionales: {model.extra_specifications}. "
    
    prompt += "El modelo debe ser moderno, práctico y apropiado para su visualización en una app de agricultura urbana."
    
    return prompt