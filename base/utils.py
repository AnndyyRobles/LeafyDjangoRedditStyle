def generate_prompt(model):
    """Generates a descriptive prompt based on the cultivation model data"""
    techniques = {
        'vertical': 'vertical farming system with multiple levels',
        'wall': 'wall-mounted growing system',
        'hydroponics': 'hydroponic growing system without soil',
        'recycled': 'urban garden using recycled materials',
        'aquaponics': 'aquaponic system combining fish and plant cultivation'
    }
    
    locations = {
        'indoor': 'designed for indoor spaces',
        'outdoor': 'designed for outdoor spaces'
    }
    
    # Basic prompt with essential information
    prompt = f"Create a detailed 3D model of a {techniques[model.technique]} for urban farming, "
    prompt += f"{locations[model.location]}, "
    prompt += f"with dimensions {model.width}cm width, {model.height}cm height, and {model.length}cm length. "
    prompt += f"Materials include: {model.materials_description}. "
    
    # Add extra specifications if they exist
    if model.extra_specifications:
        prompt += f"Additional specifications: {model.extra_specifications}. "
    
    prompt += "The model should be modern, practical and appropriate for visualization in an urban farming app."
    
    return prompt