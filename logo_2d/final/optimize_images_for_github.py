#!/usr/bin/env python3
"""
Script pour optimiser les images pour GitHub
Réduit la taille des PNG et crée des versions optimisées
"""
import os
from pathlib import Path
from PIL import Image


def optimize_image(input_path, output_path, max_size=None, quality=85):
    """Optimise une image PNG pour GitHub en gardant la transparence"""
    try:
        img = Image.open(input_path)

        # Garder la transparence si présente (RGBA, LA, P)
        if img.mode == "P":
            # Palette avec transparence
            img = img.convert("RGBA")
        elif img.mode == "LA":
            # Niveaux de gris avec alpha
            img = img.convert("RGBA")
        # Si déjà RGBA, garder tel quel
        # Si RGB, convertir en RGBA pour uniformité
        elif img.mode == "RGB":
            img = img.convert("RGBA")

        # Redimensionner si max_size spécifié
        if max_size:
            # Gérer les tuples avec None
            if isinstance(max_size, tuple):
                if max_size[0] is not None and max_size[1] is not None:
                    img.thumbnail(max_size, Image.Resampling.LANCZOS)
                elif max_size[0] is not None:
                    # Redimensionner en gardant le ratio
                    ratio = max_size[0] / img.size[0]
                    new_height = int(img.size[1] * ratio)
                    img = img.resize(
                        (max_size[0], new_height), Image.Resampling.LANCZOS
                    )
                elif max_size[1] is not None:
                    # Redimensionner en gardant le ratio
                    ratio = max_size[1] / img.size[1]
                    new_width = int(img.size[0] * ratio)
                    img = img.resize((new_width, max_size[1]), Image.Resampling.LANCZOS)
            else:
                img.thumbnail(max_size, Image.Resampling.LANCZOS)

        # Sauvegarder avec optimisation en gardant la transparence
        img.save(output_path, "PNG", optimize=True, compress_level=9)

        original_size = os.path.getsize(input_path) / 1024  # KB
        new_size = os.path.getsize(output_path) / 1024  # KB
        reduction = ((original_size - new_size) / original_size) * 100

        print(f"   ✅ {os.path.basename(output_path)}")
        print(
            f"      {original_size:.1f}KB → {new_size:.1f}KB ({reduction:.1f}% réduction)"
        )

        return True
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False


def create_thumbnail(input_path, output_path, size=(128, 128)):
    """Crée une version thumbnail"""
    try:
        img = Image.open(input_path)

        # Gérer les tuples avec None
        if isinstance(size, tuple) and (size[0] is None or size[1] is None):
            if size[0] is not None:
                ratio = size[0] / img.size[0]
                new_height = int(img.size[1] * ratio)
                size = (size[0], new_height)
            elif size[1] is not None:
                ratio = size[1] / img.size[1]
                new_width = int(img.size[0] * ratio)
                size = (new_width, size[1])

        # Conserver la transparence si présente
        if img.mode in ("RGBA", "LA"):
            img.thumbnail(size, Image.Resampling.LANCZOS)
            img.save(output_path, "PNG", optimize=True)
        else:
            img.thumbnail(size, Image.Resampling.LANCZOS)
            img.save(output_path, "PNG", optimize=True)

        print(f"   ✅ Thumbnail créé: {os.path.basename(output_path)}")
        return True
    except Exception as e:
        print(f"   ❌ Erreur thumbnail: {e}")
        return False


def main():
    """Fonction principale"""
    print("=" * 70)
    print("🖼️  OPTIMISATION DES IMAGES POUR GITHUB")
    print("=" * 70)

    current_dir = Path(".")

    # Images à optimiser
    # Utiliser SVG si PNG manquant, les convertir d'abord
    images_to_optimize = {}

    # Mark Only
    if (current_dir / "bbia_mark_only_v2.png").exists():
        images_to_optimize["bbia_mark_only_v2.png"] = {
            "github": ("bbia_mark_only_github.png", (512, 512)),
            "thumbnail": ("bbia_mark_only_thumb.png", (128, 128)),
        }
    elif (current_dir / "bbia_mark_only_v2.svg").exists():
        # Convertir SVG en PNG d'abord
        try:
            import cairosvg

            svg_path = current_dir / "bbia_mark_only_v2.svg"
            png_path = current_dir / "bbia_mark_only_v2.png"
            with open(svg_path, "rb") as f:
                svg_data = f.read()
            cairosvg.svg2png(bytestring=svg_data, write_to=str(png_path))
            images_to_optimize["bbia_mark_only_v2.png"] = {
                "github": ("bbia_mark_only_github.png", (512, 512)),
                "thumbnail": ("bbia_mark_only_thumb.png", (128, 128)),
            }
            print("   ℹ️  SVG converti en PNG pour optimisation")
        except Exception as e:
            print(f"   ⚠️  Impossible de convertir SVG: {e}")

    # Logo Vertical
    if (current_dir / "bbia_logo_vertical_v2.png").exists():
        images_to_optimize["bbia_logo_vertical_v2.png"] = {
            "github": ("bbia_logo_vertical_github.png", (400, None)),
            "thumbnail": ("bbia_logo_vertical_thumb.png", (200, None)),
        }
    elif (current_dir / "bbia_logo_vertical_v2.svg").exists():
        try:
            import cairosvg

            svg_path = current_dir / "bbia_logo_vertical_v2.svg"
            png_path = current_dir / "bbia_logo_vertical_v2.png"
            with open(svg_path, "rb") as f:
                svg_data = f.read()
            cairosvg.svg2png(bytestring=svg_data, write_to=str(png_path))
            images_to_optimize["bbia_logo_vertical_v2.png"] = {
                "github": ("bbia_logo_vertical_github.png", (400, None)),
                "thumbnail": ("bbia_logo_vertical_thumb.png", (200, None)),
            }
            print("   ℹ️  SVG converti en PNG pour optimisation")
        except Exception as e:
            print(f"   ⚠️  Impossible de convertir SVG: {e}")

    # Logo Horizontal
    if (current_dir / "bbia_logo_horizontal.png").exists():
        images_to_optimize["bbia_logo_horizontal.png"] = {
            "github": ("bbia_logo_horizontal_github.png", (600, None)),
            "thumbnail": ("bbia_logo_horizontal_thumb.png", (300, None)),
        }
    elif (current_dir / "bbia_logo_horizontal.svg").exists():
        try:
            import cairosvg

            svg_path = current_dir / "bbia_logo_horizontal.svg"
            png_path = current_dir / "bbia_logo_horizontal.png"
            with open(svg_path, "rb") as f:
                svg_data = f.read()
            cairosvg.svg2png(bytestring=svg_data, write_to=str(png_path))
            images_to_optimize["bbia_logo_horizontal.png"] = {
                "github": ("bbia_logo_horizontal_github.png", (600, None)),
                "thumbnail": ("bbia_logo_horizontal_thumb.png", (300, None)),
            }
            print("   ℹ️  SVG converti en PNG pour optimisation")
        except Exception as e:
            print(f"   ⚠️  Impossible de convertir SVG: {e}")

    # Mark Only 512x512
    if (current_dir / "bbia_mark_only_512x512.png").exists():
        images_to_optimize["bbia_mark_only_512x512.png"] = {
            "github": ("bbia_mark_only_512_github.png", (512, 512))
        }

    print("\n📸 Optimisation des images...\n")

    success_count = 0
    total_count = 0

    for input_file, outputs in images_to_optimize.items():
        input_path = current_dir / input_file

        if not input_path.exists():
            print(f"⚠️  Fichier non trouvé: {input_file}")
            continue

        print(f"📄 {input_file}:")

        # Version GitHub optimisée
        if "github" in outputs:
            total_count += 1
            output_file, max_size = outputs["github"]
            output_path = current_dir / output_file
            if optimize_image(input_path, output_path, max_size):
                success_count += 1

        # Thumbnail
        if "thumbnail" in outputs:
            total_count += 1
            output_file, size = outputs["thumbnail"]
            output_path = current_dir / output_file
            if create_thumbnail(input_path, output_path, size):
                success_count += 1

        print()

    print("✅ Résumé:")
    print(f"   • {success_count}/{total_count} images optimisées avec succès")

    if success_count == total_count:
        print("\n💡 Toutes les images ont été optimisées pour GitHub !")
        print("   Les versions '_github.png' sont prêtes pour le README.")
    else:
        print("\n⚠️  Certaines images n'ont pas pu être optimisées")


if __name__ == "__main__":
    main()
