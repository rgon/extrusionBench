# extrusionBench
Parametric Aluminium Profile Extrusions for FreeCAD

![extrusionBench](resources/repo/image.png)

## CAD Models
Designed for [DOLD Mechatronik](https://www.dold-mechatronik.de)
CAD Data sourced from [here](https://www.dold-mechatronik.de/CAD-Data)

<details>
<summary>Extraction script:</summary>
Requires `apt install unrar-free`
```bash
cd resources/profiles/dold
wget https://www.dold-mechatronik.de/documents/CAD/Aluminiumprofile/20-I-Typ-Nut-5-STEP-Daten.zip
wget https://www.dold-mechatronik.de/documents/CAD/Aluminiumprofile/30-I-Typ-Nut-6-STEP-Daten.zip
wget https://www.dold-mechatronik.de/documents/CAD/Aluminiumprofile/40-I-Typ-Nut-8-STEP-Daten.zip

# unzip all files and delete source
for f in *.zip; do unzip "$f" && rm "$f"; done
# unzip resulting zips
for f in *.zip; do unzip "$f" && rm "$f"; done
# unrar resulting rar files
for f in *.zip; do unrar -x "$f" && rm "$f"; done


```
</details>