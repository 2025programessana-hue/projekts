AI Darbināts CV Vērtētājs (Gemini Flash 2.5 + Python, ar API atbalstu)

Šis projekts salīdzina darba aprakstu ar 3 kandidātu CV, izmantojot Google Gemini Flash 2.5.



1. Ievieto savu API atslēgu failā `API.txt` (tajā pašā mapē, kur `main.py`).  
   Piemērs:
   ```
   AIzaSyA...tava_atrslēga...
   ```

2. Ievieto darba aprakstu un CV tekstus mapē `sample_inputs/`:
   - jd.txt
   - cv1.txt
   - cv2.txt
   - cv3.txt

3. Instalē atkarības un palaid skriptu:
   ```bash
   pip install -r requirements.txt
   python main.py
   ```

4. Rezultāti tiks saglabāti mapē `outputs/`.
