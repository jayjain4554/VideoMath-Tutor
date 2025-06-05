# from fastapi import FastAPI, UploadFile, File, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from typing import List, Optional, Dict, Any
# from PIL import Image, ImageEnhance, ImageFilter
# import numpy as np
# import cv2
# import os
# import tempfile
# import subprocess
# import logging
# import asyncio
# from pathlib import Path
# import shutil

# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# app = FastAPI(
#     title="Math OCR API",
#     description="Extract LaTeX from mathematical expressions in images",
#     version="1.0.0"
# )

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# class MathOCRProcessor:
#     """Simplified OCR processor with better error handling."""
    
#     def __init__(self):
#         self.check_dependencies()
    
#     def check_dependencies(self):
#         """Check which OCR engines are available."""
#         self.tesseract_available = shutil.which('tesseract') is not None
#         self.pix2tex_available = self._check_pix2tex()
        
#         logger.info(f"Tesseract available: {self.tesseract_available}")
#         logger.info(f"Pix2Tex available: {self.pix2tex_available}")
    
#     def _check_pix2tex(self) -> bool:
#         """Check if Pix2Tex is available."""
#         try:
#             import pix2tex
#             return True
#         except ImportError:
#             try:
#                 # Try running as CLI
#                 result = subprocess.run(
#                     ["pix2tex", "--help"],
#                     capture_output=True,
#                     text=True,
#                     timeout=5
#                 )
#                 return result.returncode == 0
#             except:
#                 return False
    
#     def preprocess_image(self, image_path: str) -> str:
#         """Simple but effective image preprocessing."""
#         try:
#             # Read image
#             img = cv2.imread(image_path)
#             if img is None:
#                 raise ValueError("Could not read image")
            
#             # Convert to grayscale
#             if len(img.shape) == 3:
#                 gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#             else:
#                 gray = img
            
#             # Resize if too small (minimum 200px width)
#             height, width = gray.shape
#             if width < 200:
#                 scale = 200 / width
#                 new_width = int(width * scale)
#                 new_height = int(height * scale)
#                 gray = cv2.resize(gray, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
            
#             # Apply denoising
#             denoised = cv2.fastNlMeansDenoising(gray)
            
#             # Apply adaptive thresholding
#             binary = cv2.adaptiveThreshold(
#                 denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
#                 cv2.THRESH_BINARY, 11, 2
#             )
            
#             # Save processed image
#             processed_path = image_path.replace('.png', '_processed.png')
#             cv2.imwrite(processed_path, binary)
            
#             return processed_path
            
#         except Exception as e:
#             logger.error(f"Preprocessing failed: {e}")
#             return image_path  # Return original if preprocessing fails
    
#     def extract_with_tesseract(self, image_path: str) -> str:
#         """Extract text using Tesseract OCR."""
#         try:
#             if not self.tesseract_available:
#                 return "Tesseract not available"
            
#             # Try to find Tesseract executable
#             tesseract_cmd = 'tesseract'
            
#             # Common Windows installation paths
#             windows_paths = [
#                 r'C:\Program Files\Tesseract-OCR\tesseract.exe',
#                 r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
#                 r'C:\Users\{}\AppData\Local\Tesseract-OCR\tesseract.exe'.format(os.getenv('USERNAME', '')),
#             ]
            
#             # Check if tesseract is in PATH, if not try common Windows paths
#             if os.name == 'nt':  # Windows
#                 tesseract_found = False
#                 for path in windows_paths:
#                     if os.path.exists(path):
#                         tesseract_cmd = path
#                         tesseract_found = True
#                         break
                
#                 if not tesseract_found and not shutil.which('tesseract'):
#                     return "Tesseract not found. Please install from: https://github.com/UB-Mannheim/tesseract/wiki"
            
#             # Use Tesseract with specific config for math
#             cmd = [
#                 tesseract_cmd, image_path, 'stdout',
#                 '-c', 'tessedit_char_whitelist=0123456789+-=()[]{}*/\\^_.abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ',
#                 '--psm', '6'
#             ]
            
#             result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
#             if result.returncode == 0:
#                 text = result.stdout.strip()
#                 if text:
#                     return f"Extracted text: {text}"
#                 else:
#                     return "No text detected"
#             else:
#                 return f"Tesseract error: {result.stderr.strip()}"
                
#         except subprocess.TimeoutExpired:
#             return "Tesseract timeout"
#         except Exception as e:
#             return f"Tesseract error: {str(e)}"
    
#     def extract_with_pix2tex_python(self, image_path: str) -> str:
#         """Extract LaTeX using Pix2Tex Python API."""
#         try:
#             from pix2tex.cli import LatexOCR
            
#             model = LatexOCR()
#             latex = model(image_path)
            
#             if latex and latex.strip():
#                 return latex.strip()
#             else:
#                 return "No LaTeX detected"
            
#         except Exception as e:
#             return f"Pix2Tex Python error: {str(e)}"
    
#     def extract_with_pix2tex_cli(self, image_path: str) -> str:
#         """Extract LaTeX using Pix2Tex CLI."""
#         try:
#             cmd = ['pix2tex', image_path]
#             result = subprocess.run(cmd, capture_output=True, text=True, timeout=35)
            
#             if result.returncode == 0:
#                 latex = result.stdout.strip()
#                 if latex:
#                     return latex
#                 else:
#                     return "No LaTeX detected"
#             else:
#                 return f"Pix2Tex CLI error: {result.stderr.strip()}"
                
#         except subprocess.TimeoutExpired:
#             return "Pix2Tex timeout"
#         except Exception as e:
#             return f"Pix2Tex CLI error: {str(e)}"
    
#     async def process_image(self, image_file: UploadFile) -> Dict[str, Any]:
#         """Process a single image with multiple OCR attempts."""
#         temp_files = []
        
#         try:
#             # Save uploaded file
#             with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
#                 content = await image_file.read()
#                 tmp.write(content)
#                 original_path = tmp.name
#                 temp_files.append(original_path)
            
#             # Validate image
#             try:
#                 with Image.open(original_path) as img:
#                     width, height = img.size
#                     logger.info(f"Image size: {width}x{height}")
#             except Exception as e:
#                 raise ValueError(f"Invalid image: {e}")
            
#             # Preprocess image
#             processed_path = self.preprocess_image(original_path)
#             if processed_path != original_path:
#                 temp_files.append(processed_path)
            
#             # Try different OCR methods
#             ocr_results = []
            
#             # Method 1: Pix2Tex Python API
#             if self.pix2tex_available:
#                 try:
#                     result = self.extract_with_pix2tex_python(processed_path)
#                     ocr_results.append({"method": "Pix2Tex Python", "result": result})
#                 except:
#                     pass
            
#             # Method 2: Pix2Tex CLI
#             if self.pix2tex_available:
#                 try:
#                     result = self.extract_with_pix2tex_cli(processed_path)
#                     ocr_results.append({"method": "Pix2Tex CLI", "result": result})
#                 except:
#                     pass
            
#             # Method 3: Tesseract
#             if self.tesseract_available:
#                 result = self.extract_with_tesseract(processed_path)
#                 ocr_results.append({"method": "Tesseract", "result": result})
            
#             # If no OCR engines available, return error
#             if not ocr_results:
#                 return {
#                     "filename": image_file.filename,
#                     "status": "error",
#                     "error": "No OCR engines available. Please install Tesseract or Pix2Tex."
#                 }
            
#             # Find the best result (prefer Pix2Tex results)
#             best_result = None
#             for result in ocr_results:
#                 if "error" not in result["result"].lower() and "not available" not in result["result"].lower():
#                     best_result = result
#                     break
            
#             if not best_result:
#                 best_result = ocr_results[0]  # Use first result if all failed
            
#             return {
#                 "filename": image_file.filename,
#                 "status": "success",
#                 "best_result": best_result,
#                 "all_results": ocr_results,
#                 "image_info": {
#                     "width": width,
#                     "height": height,
#                     "aspect_ratio": width / height
#                 }
#             }
            
#         except Exception as e:
#             logger.error(f"Error processing {image_file.filename}: {e}")
#             return {
#                 "filename": image_file.filename,
#                 "status": "error",
#                 "error": str(e)
#             }
#         finally:
#             # Cleanup
#             for file_path in temp_files:
#                 try:
#                     if os.path.exists(file_path):
#                         os.remove(file_path)
#                 except:
#                     pass

# # Initialize processor
# processor = MathOCRProcessor()

# @app.get("/")
# async def root():
#     """API health check and status."""
#     return {
#         "message": "Math OCR API is running",
#         "status": "healthy",
#         "ocr_engines": {
#             "tesseract": processor.tesseract_available,
#             "pix2tex": processor.pix2tex_available
#         },
#         "recommendations": {
#             "install_tesseract": "sudo apt-get install tesseract-ocr" if not processor.tesseract_available else None,
#             "install_pix2tex": "pip install pix2tex" if not processor.pix2tex_available else None
#         }
#     }

# @app.post("/ocr/single")
# async def extract_single_image(file: UploadFile = File(...)):
#     """Extract mathematical expressions from a single image."""
    
#     # Validate file type
#     if not file.content_type or not file.content_type.startswith('image/'):
#         raise HTTPException(status_code=400, detail="File must be an image")
    
#     result = await processor.process_image(file)
    
#     if result["status"] == "error":
#         raise HTTPException(status_code=400, detail=result["error"])
    
#     return result

# @app.post("/ocr")
# async def extract_multiple_images(files: List[UploadFile] = File(...)):
#     """Extract mathematical expressions from multiple images."""
    
#     if not files:
#         raise HTTPException(status_code=400, detail="No files provided")
    
#     # Validate all files
#     for file in files:
#         if not file.content_type or not file.content_type.startswith('image/'):
#             raise HTTPException(status_code=400, detail=f"File {file.filename} must be an image")
    
#     # Process all images
#     results = []
#     for file in files:
#         result = await processor.process_image(file)
#         results.append(result)
    
#     # Summary
#     successful = sum(1 for r in results if r["status"] == "success")
#     failed = len(results) - successful
    
#     return {
#         "summary": {
#             "total": len(results),
#             "successful": successful,
#             "failed": failed
#         },
#         "results": results
#     }

# @app.get("/debug")
# async def debug_info():
#     """Debug information about the system."""
#     return {
#         "ocr_engines": {
#             "tesseract_available": processor.tesseract_available,
#             "pix2tex_available": processor.pix2tex_available,
#         },
#         "system_info": {
#             "tesseract_path": shutil.which('tesseract'),
#             "python_path": shutil.which('python'),
#         }
#     }


# from sympy import symbols, Eq, solve
# from sympy.parsing.sympy_parser import parse_expr
# from fastapi import Body

# @app.post("/solve")
# async def solve_expression(payload: dict = Body(...)):
#     try:
#         expr_str = payload.get("expression", "")
#         expr_str = expr_str.replace("^", "**")  # normalize power symbol
#         x = symbols("x")
#         if "=" in expr_str:
#             lhs, rhs = expr_str.split("=")
#             eq = Eq(parse_expr(lhs), parse_expr(rhs))
#             solution = solve(eq, x)
#             return {"solution": str(solution), "steps": f"Solved for x in: {eq}"}
#         else:
#             return {"solution": "Not an equation", "steps": "No '=' found"}
#     except Exception as e:
#         return {"error": str(e)}


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)











# from fastapi import FastAPI, UploadFile, File, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from typing import List, Optional, Dict, Any
# from PIL import Image, ImageEnhance, ImageFilter, ImageOps
# import numpy as np
# import cv2
# import os
# import tempfile
# import subprocess
# import logging
# import asyncio
# from pathlib import Path
# import shutil
# import re
# import json
# from concurrent.futures import ThreadPoolExecutor
# import time

# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# app = FastAPI(
#     title="Enhanced Math OCR API",
#     description="Extract LaTeX from mathematical expressions in images with advanced preprocessing",
#     version="2.0.0"
# )

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# class EnhancedMathOCRProcessor:
#     """Enhanced OCR processor with advanced preprocessing and better accuracy."""
    
#     def __init__(self):
#         self.check_dependencies()
#         self.executor = ThreadPoolExecutor(max_workers=3)
        
#         # Common LaTeX cleaning patterns
#         self.cleanup_patterns = [
#             # Remove image filename references
#             (r'.*\.png[:：]\s*', ''),
#             # Remove problematic display style commands
#             (r'\\displaystyle\s*', ''),
#             # Clean up array environments
#             (r'\\begin\{array\}[^}]*\}(.*?)\\end\{array\}', self._clean_array_content),
#             # Fix spacing commands
#             (r'\\(quad|qquad)', ' '),
#             # Remove excessive left/right commands
#             (r'\\(left|right)\s*', ''),
#             # Clean up operatorname
#             (r'\\operatorname\{([^}]+)\}', r'\\text{\1}'),
#             # Fix fraction formatting
#             (r'\\frac\s*\{\s*([^}]+)\s*\}\s*\{\s*([^}]+)\s*\}', r'\\frac{\1}{\2}'),
#             # Remove excessive braces
#             (r'\{\{([^}]+)\}\}', r'{\1}'),
#             # Clean up multiple spaces
#             (r'\s+', ' '),
#         ]
    
#     def _clean_array_content(self, match):
#         """Clean array content to extract meaningful math."""
#         content = match.group(1) if hasattr(match, 'group') else match
#         return content.replace('\\\\', ', ').replace('&', '').strip()
    
#     def check_dependencies(self):
#         """Check which OCR engines are available with better detection."""
#         # Check Tesseract
#         self.tesseract_available = False
#         self.tesseract_path = None
        
#         # Try common paths and PATH
#         tesseract_paths = [
#             'tesseract',  # In PATH
#             r'C:\Program Files\Tesseract-OCR\tesseract.exe',
#             r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
#             '/usr/bin/tesseract',
#             '/usr/local/bin/tesseract',
#         ]
        
#         for path in tesseract_paths:
#             try:
#                 result = subprocess.run([path, '--version'], 
#                                       capture_output=True, text=True, timeout=5)
#                 if result.returncode == 0:
#                     self.tesseract_available = True
#                     self.tesseract_path = path
#                     logger.info(f"Tesseract found at: {path}")
#                     break
#             except:
#                 continue
        
#         # Check Pix2Tex
#         self.pix2tex_available = self._check_pix2tex()
        
#         logger.info(f"OCR Engines - Tesseract: {self.tesseract_available}, Pix2Tex: {self.pix2tex_available}")
    
#     def _check_pix2tex(self) -> bool:
#         """Enhanced Pix2Tex detection."""
#         # Try Python import first
#         try:
#             import pix2tex
#             from pix2tex.cli import LatexOCR
#             # Try to initialize to make sure it works
#             model = LatexOCR()
#             return True
#         except Exception as e:
#             logger.info(f"Pix2Tex Python import failed: {e}")
        
#         # Try CLI
#         try:
#             result = subprocess.run(["pix2tex", "--help"], 
#                                   capture_output=True, text=True, timeout=10)
#             return result.returncode == 0
#         except:
#             pass
        
#         return False
    
#     def advanced_preprocess_image(self, image_path: str) -> List[str]:
#         """Advanced preprocessing with multiple variants for better OCR."""
#         processed_paths = []
        
#         try:
#             # Read original image
#             img = cv2.imread(image_path)
#             if img is None:
#                 logger.error("Could not read image")
#                 return [image_path]
            
#             # Convert to grayscale
#             if len(img.shape) == 3:
#                 gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#             else:
#                 gray = img.copy()
            
#             height, width = gray.shape
#             logger.info(f"Original image size: {width}x{height}")
            
#             # Ensure minimum size for better OCR
#             min_width = 300
#             if width < min_width:
#                 scale = min_width / width
#                 new_width = int(width * scale)
#                 new_height = int(height * scale)
#                 gray = cv2.resize(gray, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
#                 logger.info(f"Resized to: {new_width}x{new_height}")
            
#             # Variant 1: Enhanced contrast with adaptive thresholding
#             try:
#                 # Noise reduction
#                 denoised = cv2.fastNlMeansDenoising(gray)
                
#                 # Enhance contrast
#                 clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
#                 enhanced = clahe.apply(denoised)
                
#                 # Adaptive threshold
#                 binary1 = cv2.adaptiveThreshold(
#                     enhanced, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
#                     cv2.THRESH_BINARY, 15, 2
#                 )
                
#                 path1 = image_path.replace('.png', '_enhanced.png')
#                 cv2.imwrite(path1, binary1)
#                 processed_paths.append(path1)
                
#             except Exception as e:
#                 logger.warning(f"Enhanced preprocessing failed: {e}")
            
#             # Variant 2: High contrast black/white
#             try:
#                 # Apply blur to reduce noise
#                 blurred = cv2.GaussianBlur(gray, (3, 3), 0)
                
#                 # Strong threshold for high contrast
#                 _, binary2 = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                
#                 # Morphological operations to clean up
#                 kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
#                 binary2 = cv2.morphologyEx(binary2, cv2.MORPH_CLOSE, kernel)
                
#                 path2 = image_path.replace('.png', '_binary.png')
#                 cv2.imwrite(path2, binary2)
#                 processed_paths.append(path2)
                
#             except Exception as e:
#                 logger.warning(f"Binary preprocessing failed: {e}")
            
#             # Variant 3: Inverted (white text on black background)
#             try:
#                 # Some math content might be white on dark background
#                 inverted = cv2.bitwise_not(gray)
                
#                 # Apply same adaptive threshold to inverted
#                 binary3 = cv2.adaptiveThreshold(
#                     inverted, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
#                     cv2.THRESH_BINARY, 11, 2
#                 )
                
#                 path3 = image_path.replace('.png', '_inverted.png')
#                 cv2.imwrite(path3, binary3)
#                 processed_paths.append(path3)
                
#             except Exception as e:
#                 logger.warning(f"Inverted preprocessing failed: {e}")
            
#             # If no preprocessing succeeded, return original
#             if not processed_paths:
#                 processed_paths.append(image_path)
                
#             return processed_paths
            
#         except Exception as e:
#             logger.error(f"All preprocessing failed: {e}")
#             return [image_path]
    
#     def clean_latex_result(self, latex_text: str) -> str:
#         """Advanced LaTeX cleaning with multiple passes."""
#         if not latex_text or not isinstance(latex_text, str):
#             return "No readable LaTeX detected"
        
#         cleaned = latex_text.strip()
        
#         # Apply all cleanup patterns
#         for pattern, replacement in self.cleanup_patterns:
#             if callable(replacement):
#                 cleaned = re.sub(pattern, replacement, cleaned, flags=re.IGNORECASE | re.DOTALL)
#             else:
#                 cleaned = re.sub(pattern, replacement, cleaned, flags=re.IGNORECASE | re.DOTALL)
        
#         # Additional specific fixes
#         cleaned = cleaned.strip()
        
#         # Remove common OCR artifacts
#         cleaned = re.sub(r'[|}{]+$', '', cleaned)  # Remove trailing artifacts
#         cleaned = re.sub(r'^[|}{]+', '', cleaned)  # Remove leading artifacts
        
#         # Fix common math symbols that get misrecognized
#         symbol_fixes = {
#             r'\bx\s*2\b': 'x^2',
#             r'\by\s*2\b': 'y^2',
#             r'\b(\w)\s*2\b': r'\1^2',
#             r'(\d+)\s*x\b': r'\1x',
#             r'(\d+)\s*y\b': r'\1y',
#             r'\s*=\s*': ' = ',
#             r'\s*\+\s*': ' + ',
#             r'\s*-\s*': ' - ',
#             r'\s*\*\s*': ' \\cdot ',
#         }
        
#         for pattern, replacement in symbol_fixes.items():
#             cleaned = re.sub(pattern, replacement, cleaned)
        
#         # Final cleanup
#         cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        
#         # Validate result
#         if len(cleaned) < 2 or cleaned.lower() in ['error', 'none', 'null']:
#             return "No readable LaTeX detected"
        
#         return cleaned
    
#     def extract_with_tesseract(self, image_path: str) -> str:
#         """Enhanced Tesseract extraction with better configuration."""
#         try:
#             if not self.tesseract_available:
#                 return "Tesseract not available"
            
#             # Use optimized Tesseract configuration for math
#             cmd = [
#                 self.tesseract_path, image_path, 'stdout',
#                 '-c', 'tessedit_char_whitelist=0123456789+-=()[]{}*/\\^_.abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ',
#                 '--psm', '6',  # Uniform block of text
#                 '--oem', '3',  # Default OCR Engine Mode
#                 '-c', 'preserve_interword_spaces=1'
#             ]
            
#             result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
#             if result.returncode == 0:
#                 text = result.stdout.strip()
#                 if text:
#                     # Convert common patterns to LaTeX
#                     text = self._convert_text_to_latex(text)
#                     return text
#                 else:
#                     return "No text detected"
#             else:
#                 return f"Tesseract error: {result.stderr.strip()}"
                
#         except subprocess.TimeoutExpired:
#             return "Tesseract timeout"
#         except Exception as e:
#             return f"Tesseract error: {str(e)}"
    
#     def _convert_text_to_latex(self, text: str) -> str:
#         """Convert plain text to LaTeX format."""
#         # Basic text to LaTeX conversion
#         conversions = [
#             (r'(\w+)\^(\d+)', r'\1^{\2}'),  # x^2 -> x^{2}
#             (r'(\d+)/(\d+)', r'\\frac{\1}{\2}'),  # 1/2 -> \frac{1}{2}
#             (r'sqrt\(([^)]+)\)', r'\\sqrt{\1}'),  # sqrt(x) -> \sqrt{x}
#             (r'(\w+)_(\w+)', r'\1_{\2}'),  # x_1 -> x_{1}
#         ]
        
#         for pattern, replacement in conversions:
#             text = re.sub(pattern, replacement, text)
        
#         return text
    
#     def extract_with_pix2tex_python(self, image_path: str) -> str:
#         """Enhanced Pix2Tex Python extraction with better error handling."""
#         try:
#             from pix2tex.cli import LatexOCR
            
#             model = LatexOCR()
#             latex = model(image_path)
            
#             if latex and latex.strip():
#                 return latex.strip()
#             else:
#                 return "No LaTeX detected"
            
#         except ImportError:
#             return "Pix2Tex not installed"
#         except Exception as e:
#             return f"Pix2Tex Python error: {str(e)}"
    
#     def extract_with_pix2tex_cli(self, image_path: str) -> str:
#         """Enhanced Pix2Tex CLI extraction."""
#         try:
#             cmd = ['pix2tex', image_path]
#             result = subprocess.run(cmd, capture_output=True, text=True, timeout=45)
            
#             if result.returncode == 0:
#                 latex = result.stdout.strip()
#                 if latex:
#                     return latex
#                 else:
#                     return "No LaTeX detected"
#             else:
#                 return f"Pix2Tex CLI error: {result.stderr.strip()}"
                
#         except subprocess.TimeoutExpired:
#             return "Pix2Tex timeout"
#         except Exception as e:
#             return f"Pix2Tex CLI error: {str(e)}"
    
#     def score_ocr_result(self, result: str) -> float:
#         """Score OCR results to determine the best one."""
#         if not result or isinstance(result, str) and any(word in result.lower() for word in ['error', 'timeout', 'not available', 'not detected']):
#             return 0.0
        
#         score = 1.0
        
#         # Higher score for LaTeX commands
#         latex_commands = len(re.findall(r'\\[a-zA-Z]+', result))
#         score += latex_commands * 0.5
        
#         # Higher score for math symbols
#         math_symbols = len(re.findall(r'[=+\-*/^_{}()]', result))
#         score += math_symbols * 0.1
        
#         # Lower score for very short results
#         if len(result) < 5:
#             score *= 0.5
        
#         # Lower score for results with many spaces (often OCR errors)
#         space_ratio = result.count(' ') / max(len(result), 1)
#         if space_ratio > 0.5:
#             score *= 0.7
        
#         return score
    
#     async def process_image(self, image_file: UploadFile) -> Dict[str, Any]:
#         """Enhanced image processing with multiple OCR attempts and preprocessing."""
#         temp_files = []
        
#         try:
#             # Save uploaded file
#             with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
#                 content = await image_file.read()
#                 tmp.write(content)
#                 original_path = tmp.name
#                 temp_files.append(original_path)
            
#             # Validate image
#             try:
#                 with Image.open(original_path) as img:
#                     width, height = img.size
#                     logger.info(f"Processing image: {width}x{height}")
                    
#                     # Convert to RGB if needed
#                     if img.mode != 'RGB':
#                         img = img.convert('RGB')
#                         rgb_path = original_path.replace('.png', '_rgb.png')
#                         img.save(rgb_path)
#                         temp_files.append(rgb_path)
#                         original_path = rgb_path
                        
#             except Exception as e:
#                 raise ValueError(f"Invalid image: {e}")
            
#             # Advanced preprocessing - create multiple variants
#             processed_paths = self.advanced_preprocess_image(original_path)
#             temp_files.extend(processed_paths)
            
#             # Collect all OCR results
#             all_results = []
            
#             # Try each preprocessing variant with available OCR engines
#             for i, proc_path in enumerate(processed_paths):
#                 variant_name = f"variant_{i+1}"
                
#                 # Pix2Tex Python API
#                 if self.pix2tex_available:
#                     try:
#                         result = self.extract_with_pix2tex_python(proc_path)
#                         cleaned = self.clean_latex_result(result)
#                         score = self.score_ocr_result(cleaned)
#                         all_results.append({
#                             "method": f"Pix2Tex Python ({variant_name})",
#                             "result": cleaned,
#                             "raw_result": result,
#                             "score": score,
#                             "preprocessing": variant_name
#                         })
#                     except Exception as e:
#                         logger.warning(f"Pix2Tex Python failed on {variant_name}: {e}")
                
#                 # Pix2Tex CLI
#                 if self.pix2tex_available:
#                     try:
#                         result = self.extract_with_pix2tex_cli(proc_path)
#                         cleaned = self.clean_latex_result(result)
#                         score = self.score_ocr_result(cleaned)
#                         all_results.append({
#                             "method": f"Pix2Tex CLI ({variant_name})",
#                             "result": cleaned,
#                             "raw_result": result,
#                             "score": score,
#                             "preprocessing": variant_name
#                         })
#                     except Exception as e:
#                         logger.warning(f"Pix2Tex CLI failed on {variant_name}: {e}")
                
#                 # Tesseract
#                 if self.tesseract_available:
#                     try:
#                         result = self.extract_with_tesseract(proc_path)
#                         cleaned = self.clean_latex_result(result)
#                         score = self.score_ocr_result(cleaned)
#                         all_results.append({
#                             "method": f"Tesseract ({variant_name})",
#                             "result": cleaned,
#                             "raw_result": result,
#                             "score": score,
#                             "preprocessing": variant_name
#                         })
#                     except Exception as e:
#                         logger.warning(f"Tesseract failed on {variant_name}: {e}")
            
#             # If no OCR engines available
#             if not all_results:
#                 return {
#                     "filename": image_file.filename,
#                     "status": "error",
#                     "error": "No OCR engines available. Please install Tesseract or Pix2Tex.",
#                     "recommendations": {
#                         "tesseract": "Install from: https://github.com/UB-Mannheim/tesseract/wiki",
#                         "pix2tex": "Install with: pip install pix2tex[gui]"
#                     }
#                 }
            
#             # Sort results by score (highest first)
#             all_results.sort(key=lambda x: x.get('score', 0), reverse=True)
            
#             # Find the best result
#             best_result = all_results[0]
            
#             # Filter out low-quality results for display
#             quality_results = [r for r in all_results if r.get('score', 0) > 0.1]
            
#             return {
#                 "filename": image_file.filename,
#                 "status": "success",
#                 "best_result": best_result,
#                 "all_results": quality_results[:5],  # Top 5 results
#                 "image_info": {
#                     "width": width,
#                     "height": height,
#                     "aspect_ratio": round(width / height, 2)
#                 },
#                 "processing_info": {
#                     "preprocessing_variants": len(processed_paths),
#                     "total_attempts": len(all_results),
#                     "engines_used": list(set(r["method"].split(" (")[0] for r in all_results))
#                 }
#             }
            
#         except Exception as e:
#             logger.error(f"Error processing {image_file.filename}: {e}")
#             return {
#                 "filename": image_file.filename,
#                 "status": "error",
#                 "error": str(e)
#             }
#         finally:
#             # Cleanup temporary files
#             for file_path in temp_files:
#                 try:
#                     if os.path.exists(file_path):
#                         os.remove(file_path)
#                 except Exception as e:
#                     logger.warning(f"Failed to cleanup {file_path}: {e}")

# # Initialize enhanced processor
# processor = EnhancedMathOCRProcessor()

# @app.get("/")
# async def root():
#     """Enhanced API health check and status."""
#     return {
#         "message": "Enhanced Math OCR API is running",
#         "version": "2.0.0",
#         "status": "healthy",
#         "ocr_engines": {
#             "tesseract": {
#                 "available": processor.tesseract_available,
#                 "path": processor.tesseract_path
#             },
#             "pix2tex": {
#                 "available": processor.pix2tex_available
#             }
#         },
#         "features": [
#             "Advanced image preprocessing",
#             "Multiple OCR engine support",
#             "Intelligent result scoring",
#             "Enhanced LaTeX cleaning",
#             "Batch processing support"
#         ],
#         "recommendations": {
#             "install_tesseract": "https://github.com/UB-Mannheim/tesseract/wiki" if not processor.tesseract_available else None,
#             "install_pix2tex": "pip install pix2tex[gui]" if not processor.pix2tex_available else None
#         }
#     }

# @app.post("/ocr/single")
# async def extract_single_image(file: UploadFile = File(...)):
#     """Extract mathematical expressions from a single image with enhanced processing."""
    
#     # Validate file type
#     if not file.content_type or not file.content_type.startswith('image/'):
#         raise HTTPException(status_code=400, detail="File must be an image")
    
#     # Check file size (limit to 10MB)
#     if hasattr(file, 'size') and file.size > 10 * 1024 * 1024:
#         raise HTTPException(status_code=400, detail="File too large (max 10MB)")
    
#     start_time = time.time()
#     result = await processor.process_image(file)
#     processing_time = round(time.time() - start_time, 2)
    
#     result["processing_time_seconds"] = processing_time
    
#     if result["status"] == "error":
#         raise HTTPException(status_code=400, detail=result["error"])
    
#     return result

# @app.post("/ocr")
# async def extract_multiple_images(files: List[UploadFile] = File(...)):
#     """Extract mathematical expressions from multiple images with enhanced processing."""
    
#     if not files:
#         raise HTTPException(status_code=400, detail="No files provided")
    
#     if len(files) > 10:
#         raise HTTPException(status_code=400, detail="Too many files (max 10)")
    
#     # Validate all files
#     for file in files:
#         if not file.content_type or not file.content_type.startswith('image/'):
#             raise HTTPException(status_code=400, detail=f"File {file.filename} must be an image")
    
#     # Process all images
#     start_time = time.time()
#     results = []
    
#     for file in files:
#         result = await processor.process_image(file)
#         results.append(result)
    
#     processing_time = round(time.time() - start_time, 2)
    
#     # Summary statistics
#     successful = sum(1 for r in results if r["status"] == "success")
#     failed = len(results) - successful
    
#     # Aggregate best results
#     best_results = []
#     for r in results:
#         if r["status"] == "success" and r.get("best_result"):
#             best_results.append({
#                 "filename": r["filename"],
#                 "latex": r["best_result"]["result"],
#                 "method": r["best_result"]["method"],
#                 "score": r["best_result"]["score"]
#             })
    
#     return {
#         "summary": {
#             "total": len(results),
#             "successful": successful,
#             "failed": failed,
#             "processing_time_seconds": processing_time
#         },
#         "best_results": best_results,
#         "detailed_results": results
#     }

# @app.get("/debug")
# async def debug_info():
#     """Enhanced debug information."""
#     return {
#         "ocr_engines": {
#             "tesseract": {
#                 "available": processor.tesseract_available,
#                 "path": processor.tesseract_path
#             },
#             "pix2tex": {
#                 "available": processor.pix2tex_available
#             }
#         },
#         "system_info": {
#             "tesseract_path": shutil.which('tesseract'),
#             "python_path": shutil.which('python'),
#             "opencv_version": cv2.__version__,
#             "numpy_version": np.__version__
#         },
#         "preprocessing_features": [
#             "Adaptive thresholding",
#             "Noise reduction",
#             "Contrast enhancement",
#             "Multiple variants",
#             "Automatic inversion detection"
#         ]
#     }

# @app.get("/health")
# async def health_check():
#     """Simple health check endpoint."""
#     return {"status": "healthy", "timestamp": time.time()}

# if __name__ == "__main__":
#     import uvicorn
#     print("🚀 Starting Enhanced Math OCR API...")
#     print("📚 Features: Advanced preprocessing, multiple OCR engines, intelligent scoring")
#     uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")








from fastapi import FastAPI, UploadFile, File, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any
from PIL import Image
import cv2
import os
import tempfile
import subprocess
import logging
import shutil
import openai
import re
from sympy import symbols, Eq, solve, simplify
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI setup
app = FastAPI(
    title="Math OCR API",
    description="Extract and solve LaTeX math expressions from images.",
    version="1.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

transformations = standard_transformations + (implicit_multiplication_application,)
openai.api_key = os.getenv("OPENAI_API_KEY")

class MathOCRProcessor:
    def __init__(self):
        self.tesseract_available = shutil.which('tesseract') is not None
        self.pix2tex_available = self._check_pix2tex()
        logger.info(f"Tesseract available: {self.tesseract_available}")
        logger.info(f"Pix2Tex available: {self.pix2tex_available}")

    def _check_pix2tex(self) -> bool:
        try:
            import pix2tex
            return True
        except ImportError:
            try:
                result = subprocess.run(["pix2tex", "--help"], capture_output=True, text=True, timeout=5)
                return result.returncode == 0
            except:
                return False

    def preprocess_image(self, image_path: str) -> str:
        try:
            img = cv2.imread(image_path)
            if img is None:
                raise ValueError("Could not read image")
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img
            if gray.shape[1] < 200:
                scale = 200 / gray.shape[1]
                gray = cv2.resize(gray, (int(gray.shape[1] * scale), int(gray.shape[0] * scale)), interpolation=cv2.INTER_CUBIC)
            denoised = cv2.fastNlMeansDenoising(gray)
            binary = cv2.adaptiveThreshold(denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
            processed_path = image_path.replace('.png', '_processed.png')
            cv2.imwrite(processed_path, binary)
            return processed_path
        except Exception as e:
            logger.error(f"Preprocessing failed: {e}")
            return image_path

    def extract_with_pix2tex_python(self, image_path: str) -> str:
        try:
            from pix2tex.cli import LatexOCR
            model = LatexOCR()
            return model(image_path).strip()
        except Exception as e:
            return f"Pix2Tex Python error: {e}"

    def extract_with_pix2tex_cli(self, image_path: str) -> str:
        try:
            result = subprocess.run(['pix2tex', image_path], capture_output=True, text=True, timeout=30)
            return result.stdout.strip() if result.returncode == 0 else f"Pix2Tex CLI error: {result.stderr.strip()}"
        except Exception as e:
            return f"Pix2Tex CLI error: {e}"

    def extract_with_tesseract(self, image_path: str) -> str:
        try:
            cmd = ['tesseract', image_path, 'stdout', '-c', 'tessedit_char_whitelist=0123456789+-=()[]{}*/\\^_.abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ', '--psm', '6']
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            return result.stdout.strip() if result.returncode == 0 else f"Tesseract error: {result.stderr.strip()}"
        except Exception as e:
            return f"Tesseract error: {e}"

    async def process_image(self, image_file: UploadFile) -> Dict[str, Any]:
        temp_files = []
        try:
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
                tmp.write(await image_file.read())
                original_path = tmp.name
                temp_files.append(original_path)

            with Image.open(original_path) as img:
                width, height = img.size

            processed_path = self.preprocess_image(original_path)
            if processed_path != original_path:
                temp_files.append(processed_path)

            results = []
            if self.pix2tex_available:
                results.append({"method": "Pix2Tex Python", "result": self.extract_with_pix2tex_python(processed_path)})
                results.append({"method": "Pix2Tex CLI", "result": self.extract_with_pix2tex_cli(processed_path)})
            if self.tesseract_available:
                results.append({"method": "Tesseract", "result": self.extract_with_tesseract(processed_path)})

            best_result = next((r for r in results if 'error' not in r['result'].lower()), results[0])

            return {
                "filename": image_file.filename,
                "status": "success",
                "best_result": best_result,
                "all_results": results,
                "image_info": {"width": width, "height": height, "aspect_ratio": width / height}
            }
        except Exception as e:
            return {"filename": image_file.filename, "status": "error", "error": str(e)}
        finally:
            for path in temp_files:
                if os.path.exists(path): os.remove(path)

processor = MathOCRProcessor()

@app.get("/")
async def root():
    return {
        "message": "Math OCR API is running",
        "ocr_engines": {
            "tesseract": processor.tesseract_available,
            "pix2tex": processor.pix2tex_available
        }
    }

@app.post("/ocr/single")
async def extract_single_image(file: UploadFile = File(...)):
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    result = await processor.process_image(file)
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@app.post("/ocr")
async def extract_multiple_images(files: List[UploadFile] = File(...)):
    if not files:
        raise HTTPException(status_code=400, detail="No files provided")
    results = [await processor.process_image(file) for file in files]
    return {
        "summary": {
            "total": len(results),
            "successful": sum(r["status"] == "success" for r in results),
            "failed": sum(r["status"] == "error" for r in results)
        },
        "results": results
    }

# --- Solver logic ---
def clean_latex_input(expr: str) -> str:
    expr = expr.replace("\\quad", " ").replace("\\left", "").replace("\\right", "")
    expr = re.sub(r"\\[a-zA-Z]+", "", expr)
    expr = expr.replace("{", "").replace("}", "").replace("^", "**").replace("\\", "").strip()
    return next((line.strip() for line in expr.splitlines() if any(op in line for op in ["=", "+", "-", "*", "/"])), expr)

from openai import OpenAIError

def solve_with_gpt(expr: str) -> str:
    try:
        openai.api_key = os.getenv("OPENAI_API_KEY")

        if not openai.api_key:
            return "OpenAI API key not configured."

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful and concise math tutor."},
                {"role": "user", "content": f"Solve and explain this math problem step-by-step: {expr}"}
            ],
            temperature=0.4,
            max_tokens=500
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"GPT fallback failed: {str(e)}"


@app.post("/solve")
async def solve_expression(payload: dict = Body(...)):
    try:
        expr_str = payload.get("expression", "").strip()
        expr_str = expr_str.replace("^", "**")

        x = symbols("x")
        if "=" in expr_str:
            lhs, rhs = expr_str.split("=")
            eq = Eq(parse_expr(lhs), parse_expr(rhs))
            solution = solve(eq, x)
            return {
                "solution": str(solution),
                "steps": f"Solved for x in: {eq}"
            }
        else:
            return {
                "solution": "Not an equation",
                "steps": "No '=' found"
            }

    except Exception as e:
        fallback = solve_with_gpt(expr_str)
        return {
            "solution": None,
            "steps": "SymPy failed to solve. Fallback result:",
            "gpt_fallback": fallback
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
