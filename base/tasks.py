import os
import requests
import replicate
from celery import shared_task
from django.core.files.base import ContentFile
from django.conf import settings
from .models import Cultivation3DModel

@shared_task(name='base.tasks.generate_3d_model')
def generate_3d_model(model_id):
    """
    Task to generate 3D model asynchronously
    """
    print(f"Starting task for model_id: {model_id}")
    model = Cultivation3DModel.objects.get(id=model_id)
    
    try:
        # Configure Replicate API key
        os.environ["REPLICATE_API_TOKEN"] = settings.REPLICATE_API_KEY
        
        # 1. Update status
        model.status = 'generating_image'
        model.save()
        print(f"Status updated to generating_image for model_id: {model_id}")
        
        # 2. Generate image with Flux
        print(f"Running Flux for model_id: {model_id} with prompt: {model.prompt[:100]}...")
        flux_output = replicate.run(
            "black-forest-labs/flux-1.1-pro",
            input={
                "prompt": model.prompt,
                "width": 768,
                "height": 768,
                "num_inference_steps": 40
            }
        )
        print(f"Flux raw output for model_id: {model_id}: {flux_output}")
        print(f"Flux output type: {type(flux_output)}")
        
        # Extract URL from FileOutput object
        image_url = None
        
        # Try to get the URL no matter what format it's in
        try:
            # If it's a FileOutput object
            if hasattr(flux_output, 'url'):
                image_url = flux_output.url
            # If it's a FileOutput object that needs to be converted to string
            elif hasattr(flux_output, '__str__'):
                image_url = str(flux_output)
            # If it's a list
            elif isinstance(flux_output, list) and len(flux_output) > 0:
                if hasattr(flux_output[0], 'url'):
                    image_url = flux_output[0].url
                elif hasattr(flux_output[0], '__str__'):
                    image_url = str(flux_output[0])
                else:
                    image_url = flux_output[0]
            # If it's a string
            elif isinstance(flux_output, str):
                image_url = flux_output
            # If it's a dict
            elif isinstance(flux_output, dict) and 'url' in flux_output:
                image_url = flux_output['url']
        except Exception as e:
            print(f"Error extracting image URL: {e}")
        
        print(f"Extracted image URL: {image_url}")
        
        if image_url:
            print(f"Image URL for model_id: {model_id}: {image_url}")
            
            try:
                # Try to download the image
                response = requests.get(image_url, timeout=30)
                
                if response.status_code == 200:
                    print(f"Successfully downloaded image for model_id: {model_id}")
                    
                    # Save the image
                    model.generated_image.save(
                        f"3d_model_image_{model.id}.png",
                        ContentFile(response.content)
                    )
                    
                    # 3. Update status
                    model.status = 'generating_model'
                    model.save()
                    print(f"Status updated to generating_model for model_id: {model_id}")
                    
                    # 4. Generate 3D model with Trellis
                    print(f"Running Trellis for model_id: {model_id} with image: {image_url}")
                    trellis_output = replicate.run(
                        "firtoz/trellis:4876f2a8da1c544772dffa32e8889da4a1bab3a1f5c1937bfcfccb99ae347251",
                        input={
                            "images": [image_url], 
                            "generate_model": True,  
                            "generate_color": True,  
                            "texture_size": 2048,    
                            "mesh_simplify": 0.9     
                        }
                    )
                    print(f"Trellis raw output for model_id: {model_id}: {trellis_output}")
                    print(f"Trellis output type: {type(trellis_output)}")
                    
                    # Extract GLB URL
                    glb_url = None
                    
                    try:
                        # If it's a dict with 'model_file' key
                        if isinstance(trellis_output, dict) and 'model_file' in trellis_output:
                            glb_url = trellis_output['model_file']
                        # If it's an object with model_file attribute
                        elif hasattr(trellis_output, 'model_file'):
                            glb_url = trellis_output.model_file
                        # If it's a string that ends with .glb
                        elif isinstance(trellis_output, str) and trellis_output.endswith('.glb'):
                            glb_url = trellis_output
                    except Exception as e:
                        print(f"Error extracting GLB URL: {e}")
                    
                    print(f"Extracted GLB URL: {glb_url}")
                    
                    if glb_url:
                        print(f"GLB URL for model_id: {model_id}: {glb_url}")
                        
                        try:
                            # Try to download the GLB
                            response = requests.get(glb_url, timeout=30)
                            
                            if response.status_code == 200:
                                print(f"Successfully downloaded GLB for model_id: {model_id}")
                                
                                # Save the GLB
                                model.glb_model.save(
                                    f"3d_model_{model.id}.glb",
                                    ContentFile(response.content)
                                )
                                
                                # 5. Update status to completed
                                model.status = 'completed'
                                model.save()
                                print(f"Status updated to completed for model_id: {model_id}")
                                return True
                            else:
                                print(f"Error downloading GLB: Status code {response.status_code}")
                                model.status = 'error'
                                model.error_message = f'Failed to download GLB file (status code: {response.status_code})'
                                model.save()
                                return False
                        except Exception as e:
                            print(f"Error downloading GLB: {e}")
                            model.status = 'error'
                            model.error_message = f'Error downloading GLB: {str(e)}'
                            model.save()
                            return False
                    else:
                        print(f"Error: Trellis did not return a valid GLB URL for model_id: {model_id}")
                        model.status = 'error'
                        model.error_message = 'Failed to generate 3D model (no GLB URL)'
                        model.save()
                        return False
                else:
                    print(f"Error downloading image: Status code {response.status_code}")
                    model.status = 'error'
                    model.error_message = f'Failed to download image (status code: {response.status_code})'
                    model.save()
                    return False
            except Exception as e:
                print(f"Error downloading image: {e}")
                model.status = 'error'
                model.error_message = f'Error downloading image: {str(e)}'
                model.save()
                return False
        else:
            print(f"Error: Could not extract a valid image URL from Flux output for model_id: {model_id}")
            model.status = 'error'
            model.error_message = 'Failed to extract image URL from Flux output'
            model.save()
            return False
            
    except Exception as e:
        print(f"Exception in task for model_id: {model_id}: {str(e)}")
        model.status = 'error'
        model.error_message = str(e)
        model.save()
        return False