import os
import django
import random
from django.core.files import File
from django.conf import settings

# Configurar entorno Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'studybud.settings')
django.setup()

from base.models import CultivationTechnique, PlantGuide

# Datos de ejemplo para las técnicas de cultivo
techniques_data = [
    {
        'name': 'Vertical',
        'description': 'El cultivo vertical aprovecha el espacio vertical para cultivar plantas, ideal para espacios pequeños como apartamentos o patios urbanos. Permite cultivar más plantas en menos espacio horizontal.',
        'setup_instructions': '''
1. Elige una estructura vertical: puede ser un sistema de estanterías, una pared con bolsillos de tela, tubos de PVC verticales con agujeros, o palés reciclados.

2. Asegura que la estructura esté bien fijada a la pared o que tenga una base estable para evitar caídas.

3. Prepara un buen sustrato mezclando tierra para macetas, compost y perlita para mejorar el drenaje.

4. Instala un sistema de riego por goteo o planifica un horario regular de riego manual, teniendo en cuenta que las plantas superiores pueden necesitar más agua ya que se secan más rápido.

5. Planta tus semillas o plántulas en los espacios designados, asegurándote de que cada planta tenga suficiente espacio para crecer.

6. Coloca tu jardín vertical en un lugar donde reciba la cantidad adecuada de luz solar según las necesidades de tus plantas.
        ''',
        'maintenance_tips': '''
- Revisa el sistema de riego regularmente para asegurarte de que todas las plantas reciben agua adecuadamente.
- Rota las plantas periódicamente si notas que algunas reciben menos luz que otras.
- Fertiliza cada 2-3 semanas durante la temporada de crecimiento.
- Poda regularmente para mantener un crecimiento compacto y saludable.
- Inspecciona las plantas en busca de plagas o enfermedades, especialmente en las áreas menos accesibles.
- Reemplaza el sustrato anualmente o cuando notes que se ha compactado demasiado.
        ''',
        'recommended_plants': '''
- Hierbas aromáticas: albahaca, tomillo, romero, menta, cilantro
- Vegetales de hoja verde: lechuga, espinaca, rúcula, col rizada
- Fresas
- Plantas pequeñas como rábanos y cebollas verdes
- Flores comestibles: caléndula, capuchina
- Plantas ornamentales pequeñas y colgantes
        ''',
        'space_requirements': 'Requiere muy poco espacio horizontal, ideal para balcones, paredes exteriores o interiores con buena luz. Necesita una pared o estructura vertical resistente que pueda soportar el peso de las plantas, tierra y agua.',
        'difficulty_level': 'Medium',
        'estimated_cost': '$50-150 dependiendo de los materiales y tamaño',
        'materials_needed': '''
- Estructura vertical (estanterías, palés, tubos PVC, bolsillos de tela)
- Tornillos y soportes para fijar a la pared (si es necesario)
- Sustrato para macetas
- Compost
- Sistema de riego por goteo (opcional pero recomendado)
- Temporizador de riego (opcional)
- Bandejas o sistema para recoger el exceso de agua
- Plantas o semillas
        ''',
        'benefits': '''
- Maximiza el espacio de cultivo en áreas pequeñas
- Puede mejorar la estética de paredes o espacios vacíos
- Facilita el acceso a las plantas para su mantenimiento
- Puede actuar como aislante térmico y acústico para el hogar
- Mejora la calidad del aire interior
- Permite cultivar alimentos frescos incluso en espacios urbanos limitados
        ''',
        'limitations': '''
- Requiere un sistema de riego más complejo
- Las plantas superiores pueden secarse más rápido
- Limitado a plantas de tamaño pequeño o mediano
- Puede ser difícil de mover una vez instalado
- Requiere una estructura sólida para soportar el peso
- Algunas plantas pueden no adaptarse bien al crecimiento vertical
        '''
    },
    {
        'name': 'Wall-mounted',
        'description': 'Los jardines montados en pared son sistemas de cultivo que se adhieren directamente a superficies verticales, creando jardines vivos que funcionan como arte natural. Perfectos para decorar espacios interiores o exteriores mientras cultivas plantas.',
        'setup_instructions': '''
1. Selecciona una pared que reciba la cantidad adecuada de luz para tus plantas y asegúrate de que sea lo suficientemente fuerte para soportar el peso del sistema.

2. Elige tu sistema de montaje en pared: marcos con bolsillos, paneles modulares, macetas especiales para pared o construye uno personalizado con materiales reciclados.

3. Instala una barrera impermeable entre la pared y el sistema de cultivo para proteger la pared de la humedad.

4. Monta el sistema siguiendo las instrucciones del fabricante o tu diseño personalizado, asegurándote de que esté nivelado y bien sujeto.

5. Instala un sistema de riego por goteo o planifica un método de riego manual que no dañe la pared.

6. Prepara un sustrato ligero mezclando tierra para macetas, perlita y vermiculita para reducir el peso total.

7. Planta especies adecuadas para jardines verticales, considerando sus necesidades de luz y agua según la ubicación.
        ''',
        'maintenance_tips': '''
- Riega con cuidado para evitar excesos que puedan dañar la pared.
- Revisa regularmente que el sistema esté bien sujeto y no haya signos de humedad en la pared.
- Fertiliza con fertilizantes líquidos diluidos para no saturar el sustrato.
- Rota las plantas si notas que algunas no reciben suficiente luz.
- Poda regularmente para mantener un aspecto ordenado y evitar que las plantas crezcan demasiado.
- Reemplaza las plantas que no se adapten bien o mueran.
- Limpia periódicamente las hojas para eliminar el polvo, especialmente en interiores.
        ''',
        'recommended_plants': '''
- Plantas suculentas y cactus (para sistemas con poco riego)
- Helechos y plantas de sombra (para interiores con poca luz)
- Hierbas aromáticas: tomillo, orégano, menta
- Plantas colgantes: pothos, hiedra, planta del dinero
- Plantas con flores pequeñas: violetas africanas, begonias
- Plantas purificadoras de aire: sansevierias, espatifilos
- Musgos y plantas epífitas para sistemas hidropónicos
        ''',
        'space_requirements': 'Requiere una pared libre con buena iluminación. El espacio horizontal necesario es mínimo, apenas unos centímetros de profundidad. Ideal para pasillos, cocinas, salas de estar o patios pequeños.',
        'difficulty_level': 'Medium',
        'estimated_cost': '$100-300 dependiendo del sistema y tamaño',
        'materials_needed': '''
- Sistema de montaje en pared (comercial o DIY)
- Barrera impermeable o lámina plástica
- Tornillos y tacos adecuados para el tipo de pared
- Sustrato ligero
- Sistema de riego por goteo (recomendado)
- Bandeja o sistema para recoger exceso de agua
- Plantas adecuadas para jardines verticales
        ''',
        'benefits': '''
- Funciona como elemento decorativo y mejora la estética del espacio
- No ocupa espacio útil en el suelo
- Mejora la calidad del aire y la acústica de la habitación
- Puede ayudar a regular la temperatura interior
- Permite tener plantas al alcance en espacios pequeños
- Crea un punto focal interesante en cualquier habitación
        ''',
        'limitations': '''
- Puede dañar las paredes si no se instala correctamente
- El riego puede ser complicado y requiere atención para evitar goteos
- Limitado a plantas de tamaño pequeño o mediano
- Algunas paredes pueden no ser adecuadas para soportar el peso
- Puede ser costoso si se opta por sistemas comerciales
- Difícil de reubicar una vez instalado
        '''
    },
    {
        'name': 'Hydroponics',
        'description': 'La hidroponía es un método de cultivo que utiliza soluciones minerales en agua sin suelo. Las raíces de las plantas reciben una solución nutritiva equilibrada disuelta en agua con todos los elementos químicos esenciales para su desarrollo.',
        'setup_instructions': '''
1. Elige un sistema hidropónico adecuado para tu espacio y experiencia: NFT (Técnica de Película Nutritiva), DWC (Cultivo en Agua Profunda), Sistema de Mecha, Aeropónico, o Sistema de Flujo y Reflujo.

2. Adquiere o construye los componentes necesarios: depósitos, bombas, tuberías, medios de cultivo (si es necesario), y soportes para plantas.

3. Instala el sistema en un lugar con acceso a electricidad y donde puedas controlar la luz y temperatura.

4. Prepara la solución nutritiva siguiendo las instrucciones del fabricante, midiendo cuidadosamente el pH (idealmente entre 5.5 y 6.5) y la conductividad eléctrica (EC).

5. Coloca las plantas en el sistema, ya sea mediante trasplante desde semilleros o utilizando medios de cultivo como lana de roca, arcilla expandida o fibra de coco.

6. Configura el sistema de iluminación si cultivas en interiores, asegurando que las plantas reciban la cantidad y tipo de luz adecuados.

7. Programa los ciclos de riego según el sistema elegido y las necesidades de tus plantas.
        ''',
        'maintenance_tips': '''
- Monitorea diariamente el nivel de agua y la solución nutritiva.
- Verifica el pH y EC regularmente, ajustando según sea necesario.
- Cambia la solución nutritiva completamente cada 2-3 semanas.
- Limpia el sistema regularmente para prevenir algas y obstrucciones.
- Revisa que las bombas y sistemas eléctricos funcionen correctamente.
- Inspecciona las raíces en busca de signos de enfermedades o problemas.
- Mantén el área limpia para prevenir plagas y enfermedades.
- Asegura una buena circulación de aire para evitar problemas de humedad.
        ''',
        'recommended_plants': '''
- Lechugas y verduras de hoja verde (espinacas, rúcula, kale)
- Hierbas aromáticas (albahaca, cilantro, menta, perejil)
- Fresas
- Tomates cherry
- Pepinos
- Pimientos
- Plantas ornamentales como lechuga de agua o jacinto de agua
- Flores comestibles
        ''',
        'space_requirements': 'Adaptable a casi cualquier espacio, desde pequeños sistemas de sobremesa hasta instalaciones comerciales grandes. Ideal para interiores, garajes, sótanos o invernaderos. Requiere acceso a electricidad y preferiblemente un lugar donde los posibles derrames de agua no causen problemas.',
        'difficulty_level': 'Hard',
        'estimated_cost': '$150-500 para sistemas básicos, más para sistemas avanzados',
        'materials_needed': '''
- Depósitos o contenedores para la solución nutritiva
- Bomba de agua (para la mayoría de los sistemas)
- Tuberías y conectores
- Medio de cultivo (arcilla expandida, lana de roca, etc.)
- Nutrientes hidropónicos
- Medidor de pH y EC
- Ajustadores de pH
- Luces de cultivo (para interiores)
- Temporizador para bombas y luces
- Soportes para plantas o red de enrejado
        ''',
        'benefits': '''
- Mayor rendimiento en menos espacio comparado con la agricultura tradicional
- Crecimiento más rápido de las plantas
- Control preciso de nutrientes
- Uso eficiente del agua (hasta 90% menos que el cultivo en suelo)
- Menos problemas con malezas y algunas plagas del suelo
- Posibilidad de cultivar todo el año independientemente del clima
- No requiere suelo fértil, ideal para áreas urbanas
- Menor uso de pesticidas en muchos casos
        ''',
        'limitations': '''
- Requiere conocimientos técnicos y monitoreo constante
- Dependencia de electricidad
- Costo inicial más alto que el cultivo en suelo
- Riesgo de fallo del sistema que puede dañar rápidamente las plantas
- Mayor susceptibilidad a enfermedades de raíz si hay contaminación
- Requiere soluciones nutritivas específicas y control de pH
- Puede ser complicado para principiantes
        '''
    },
    {
        'name': 'Recycled Materials',
        'description': 'El cultivo con materiales reciclados utiliza objetos reutilizados como contenedores, estructuras o componentes para crear jardines sostenibles. Esta técnica reduce residuos, ahorra dinero y permite cultivar plantas de forma creativa y ecológica.',
        'setup_instructions': '''
1. Recolecta materiales reciclables que puedan servir como contenedores: botellas plásticas, llantas viejas, palés de madera, cubos, cajas, cajones, tubos de PVC, zapatos viejos, latas, etc.

2. Limpia bien todos los materiales, especialmente si contenían productos químicos. Para contenedores de alimentos o productos de limpieza, lávalos con agua caliente y jabón.

3. Modifica los materiales según sea necesario: haz agujeros de drenaje en la parte inferior de los contenedores, pinta las llantas o palés para protegerlos de la intemperie, refuerza estructuras si es necesario.

4. Si usas materiales que pueden liberar sustancias tóxicas (como algunas maderas tratadas), considera forrarlos con plástico o geotextil para crear una barrera.

5. Prepara un buen sustrato mezclando tierra para macetas con compost casero si lo tienes disponible.

6. Organiza tus contenedores reciclados según el espacio disponible: vertical, horizontal, colgante o combinados en una estructura.

7. Planta especies adecuadas al tamaño y profundidad de cada contenedor reciclado.
        ''',
        'maintenance_tips': '''
- Revisa regularmente la integridad de los materiales reciclados, especialmente después de condiciones climáticas extremas.
- Asegúrate de que los agujeros de drenaje no se obstruyan.
- Rota los cultivos para evitar el agotamiento de nutrientes en contenedores pequeños.
- Aplica compost o fertilizante orgánico regularmente, ya que los contenedores reciclados pueden tener limitaciones de nutrientes.
- Protege los materiales biodegradables (como madera o cartón) de la excesiva humedad o aplica tratamientos naturales para prolongar su vida útil.
- Reemplaza los materiales que se deterioren demasiado con nuevos elementos reciclados.
- Adapta el riego según el material del contenedor (algunos retienen más humedad que otros).
        ''',
        'recommended_plants': '''
- Para botellas plásticas y contenedores pequeños: hierbas aromáticas, fresas, lechugas, rábanos
- Para llantas: papas, tomates, calabacines, flores
- Para palés verticales: plantas de raíces poco profundas como lechugas, espinacas, hierbas
- Para tubos de PVC: lechugas, espinacas, cebollas verdes, hierbas
- Para cajas y cajones: casi cualquier vegetal según la profundidad
- Para zapatos viejos y contenedores inusuales: suculentas, flores pequeñas, hierbas
- Plantas trepadoras para estructuras verticales: guisantes, judías, pepinos pequeños
        ''',
        'space_requirements': 'Extremadamente flexible, adaptable a cualquier espacio desde un alféizar de ventana hasta un patio trasero completo. Ideal para balcones, terrazas, patios pequeños, o incluso espacios interiores con buena luz.',
        'difficulty_level': 'Easy',
        'estimated_cost': '$10-50 principalmente para tierra y semillas',
        'materials_needed': '''
- Materiales reciclados diversos (botellas, llantas, palés, etc.)
- Herramientas básicas (tijeras, cuchillo, taladro para agujeros de drenaje)
- Pintura no tóxica o sellador (opcional)
- Tierra para macetas
- Compost
- Semillas o plántulas
- Geotextil o plástico para forrar si es necesario
- Cuerdas, alambres o sujetadores para crear estructuras
- Regadera o sistema de riego básico
        ''',
        'benefits': '''
- Reduce la cantidad de residuos que van a vertederos
- Costo muy bajo o nulo para los contenedores
- Fomenta la creatividad y personalización del espacio
- Ideal para enseñar a niños sobre sostenibilidad y cultivo
- Permite cultivar en espacios no convencionales
- Flexibilidad para cambiar y adaptar el diseño
- Contribuye a la economía circular y sostenibilidad
        ''',
        'limitations': '''
- Algunos materiales reciclados pueden degradarse rápidamente
- Posible preocupación por lixiviación de químicos de ciertos materiales
- Puede requerir más mantenimiento que sistemas convencionales
- Limitaciones de tamaño para plantas de raíces profundas
- Estética que puede no agradar a todos
- Algunos materiales pueden retener demasiada o muy poca humedad
- Posible necesidad de reemplazar contenedores con frecuencia
        '''
    },
    {
        'name': 'Aquaponics',
        'description': 'La acuaponía es un sistema simbiótico que combina la acuicultura (cría de peces) con la hidroponía (cultivo de plantas sin suelo). Los desechos de los peces proporcionan nutrientes para las plantas, mientras que las plantas filtran el agua para los peces.',
        'setup_instructions': '''
1. Elige el tipo de sistema acuapónico: sistema de camas de cultivo con medio, sistema NFT (Técnica de Película Nutritiva), o sistema de balsas flotantes (Deep Water Culture).

2. Prepara los componentes principales: tanque para peces, filtro de sólidos (opcional), biofiltro, camas de cultivo o canales para plantas, y bomba de agua.

3. Instala el sistema en un lugar nivelado con acceso a electricidad, preferiblemente protegido de condiciones climáticas extremas.

4. Conecta los componentes con tuberías asegurando un flujo adecuado: del tanque de peces al filtro, luego al biofiltro, a las camas de cultivo y de vuelta al tanque.

5. Llena el sistema con agua desclorada y déjalo ciclar durante 2-4 semanas para establecer las bacterias nitrificantes necesarias (puedes acelerar este proceso añadiendo bacterias comerciales).

6. Monitorea los niveles de amoníaco, nitritos y nitratos durante el ciclo inicial. Cuando el amoníaco y los nitritos estén en cero y haya presencia de nitratos, el sistema está listo.

7. Introduce los peces gradualmente, comenzando con pocos ejemplares y aumentando la población lentamente.

8. Planta las especies vegetales adecuadas según tu sistema y las condiciones locales.
        ''',
        'maintenance_tips': '''
- Alimenta a los peces regularmente según su especie y tamaño, pero evita la sobrealimentación.
- Monitorea la calidad del agua semanalmente: pH (6.8-7.2 ideal), amoníaco, nitritos, nitratos, temperatura y oxígeno disuelto.
- Mantén el nivel del agua, añadiendo agua desclorada cuando sea necesario para compensar la evaporación.
- Limpia los filtros regularmente para evitar obstrucciones.
- Revisa que la bomba y aireadores funcionen correctamente.
- Retira plantas muertas o enfermas inmediatamente.
- Observa el comportamiento de los peces para detectar posibles problemas de salud.
- Realiza cambios parciales de agua (5-10%) mensualmente si es necesario.
- Equilibra la cantidad de peces con la superficie de cultivo (regla general: 1 kg de pez por 10-20 litros de agua).
        ''',
        'recommended_plants': '''
- Plantas de hojas verdes: lechuga, espinaca, acelga, kale, rúcula
- Hierbas aromáticas: albahaca, menta, cilantro, perejil, cebollino
- Fresas
- Tomates cherry (en sistemas más establecidos con altos niveles de nutrientes)
- Pepinos
- Pimientos
- Brócoli y coliflor
- Plantas ornamentales como lechuga de agua
        ''',
        'space_requirements': 'Requiere más espacio que otros métodos de cultivo, desde sistemas pequeños de 1-2 m² hasta instalaciones grandes. Necesita una superficie nivelada que pueda soportar el peso considerable del agua. Ideal para patios, invernaderos, garajes o espacios dedicados.',
        'difficulty_level': 'Hard',
        'estimated_cost': '$300-1000 para sistemas básicos, más para sistemas avanzados',
        'materials_needed': '''
- Tanque para peces (plástico alimentario, fibra de vidrio o similar)
- Contenedores o camas para plantas
- Bomba de agua sumergible
- Aireador o bomba de aire con piedras difusoras
- Tuberías y accesorios de plomería
- Medio de cultivo (grava, arcilla expandida, etc.) para algunos sistemas
- Kit de prueba de agua para acuarios
- Temporizador para la bomba
- Peces adecuados (tilapia, carpa, goldfish, etc.)
- Alimento para peces
- Bacterias nitrificantes (opcional, para acelerar el ciclo)
        ''',
        'benefits': '''
- Sistema cerrado que utiliza hasta un 90% menos de agua que la agricultura convencional
- Produce dos fuentes de alimento: vegetales y proteína (peces)
- No requiere fertilizantes químicos
- Crecimiento más rápido de las plantas que en el suelo
- Menor incidencia de plagas y enfermedades del suelo
- Cultivo orgánico por naturaleza
- Puede funcionar todo el año en condiciones controladas
- Altamente productivo en espacios relativamente pequeños
        ''',
        'limitations': '''
- Requiere conocimientos tanto de acuicultura como de cultivo de plantas
- Dependencia de electricidad para bombas y aireadores
- Costo inicial elevado
- Complejidad en el equilibrio del ecosistema
- Vulnerabilidad a fallos del sistema (un corte eléctrico puede ser fatal)
- Requiere monitoreo constante de parámetros del agua
- Limitaciones en los tipos de plantas en sistemas nuevos
- Mayor curva de aprendizaje que otros métodos de cultivo
        '''
    }
]

# Función para crear técnicas de cultivo
def create_techniques():
    print("Creando técnicas de cultivo...")
    
    # Verificar si ya existen técnicas
    if CultivationTechnique.objects.exists():
        print("Ya existen técnicas de cultivo en la base de datos. No se crearán nuevas.")
        return
    
    # Crear técnicas
    for technique_data in techniques_data:
        # Crear la tu00e9cnica sin imu00e1genes inicialmente
        technique = CultivationTechnique(
            name=technique_data['name'],
            description=technique_data['description'],
            setup_instructions=technique_data['setup_instructions'],
            maintenance_tips=technique_data['maintenance_tips'],
            recommended_plants=technique_data['recommended_plants'],
            space_requirements=technique_data['space_requirements'],
            difficulty_level=technique_data['difficulty_level'],
            estimated_cost=technique_data['estimated_cost'],
            materials_needed=technique_data['materials_needed'],
            benefits=technique_data['benefits'],
            limitations=technique_data['limitations'],
            # Usar None para las imu00e1genes
            main_image=None,
            step_images=None
        )
        
        # Guardar la técnica
        technique.save()
        print(f"Técnica creada: {technique.name}")

if __name__ == "__main__":
    create_techniques()
    print("Proceso completado.")
