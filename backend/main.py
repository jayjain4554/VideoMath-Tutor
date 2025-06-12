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
import re
import together
from sympy import symbols, Eq, solve
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Setup Together API
together.api_key = os.getenv("TOGETHER_API_KEY")  # Use env var like TOGETHER_API_KEY

# FastAPI setup
app = FastAPI(title="Math OCR API", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

transformations = standard_transformations + (implicit_multiplication_application,)


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

    def extract_with_pix2tex_cli(self, image_path: str) -> str:
        try:
            result = subprocess.run(['pix2tex', image_path], capture_output=True, text=True, timeout=60)
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
            results.append({"method": "Pix2Tex CLI", "result": self.extract_with_pix2tex_cli(processed_path)})
            if self.tesseract_available:
                results.append({"method": "Tesseract", "result": self.extract_with_tesseract(processed_path)})

            best_result = next((r for r in results if 'error' not in r['result'].lower()), results[0])
            best_result['cleaned'] = clean_latex_result(best_result['result'])

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
                if os.path.exists(path):
                    os.remove(path)


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


# -------- LaTeX Cleaning & Solver Section --------

def clean_latex_result(raw: str) -> str:
    raw = re.sub(r'^.*?:\s*', '', raw)
    raw = re.sub(r'\\begin{array}{.*?}|\\end{array}', '', raw)
    raw = raw.replace("\\qquad", "").replace("\\quad", "")
    raw = raw.replace("\\\\", "\n")
    equations = re.findall(r"\{\{(.*?)\}\}", raw)
    if not equations:
        equations = raw.splitlines()
    cleaned = [eq.strip() for eq in equations if any(op in eq for op in "=+-*/")]
    return "\n".join(cleaned)


def extract_equations_from_latex(latex: str) -> List[str]:
    latex = re.sub(r'\\begin{array}{.*?}|\\end{array}', '', latex)
    latex = re.sub(r'\\[a-zA-Z]+', '', latex)
    latex = latex.replace("{", "").replace("}", "")
    latex = latex.replace("\\\\", "\n")
    lines = [line.strip() for line in latex.splitlines() if any(op in line for op in "=+-*/")]
    return lines

def solve_with_together_ai(expr: str) -> str:
    try:
        prompt = f"Solve and explain step-by-step: {expr}"
        response = together.Complete.create(
            model="mistralai/Mixtral-8x7B-Instruct-v0.1",
            prompt=prompt,
            max_tokens=512,
            temperature=0.4,
            top_k=50,
            top_p=0.95,
            repetition_penalty=1.1,
        )
        # ✅ Corrected parsing
        return response['choices'][0]['text'].strip()
    except Exception as e:
        return f"Together AI error: {str(e)}"



@app.post("/solve")
async def solve_expression(payload: dict = Body(...)):
    raw_expr = payload.get("expression", "").strip()
    equations = extract_equations_from_latex(raw_expr)

    if not equations:
        return {"error": "No solvable equations found."}

    results = []
    for eq in equations:
        solution = solve_with_together_ai(eq)
        results.append({"expression": eq, "solution": solution})

    return {"total_equations": len(results), "results": results}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
