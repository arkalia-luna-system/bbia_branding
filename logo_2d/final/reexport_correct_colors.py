#!/usr/bin/env python3
"""
Script pour réexporter les logos avec les bonnes couleurs depuis Inkscape
Utilise Inkscape en ligne de commande pour garantir les couleurs correctes
"""
import os
import subprocess
from pathlib import Path


def reexport_with_inkscape(svg_file, output_png, width=None, height=None):
    """Réexporte un SVG en PNG avec Inkscape pour préserver les couleurs"""
    svg_path = Path(svg_file).absolute()
    png_path = Path(output_png).absolute()

    if not svg_path.exists():
        print(f"❌ SVG non trouvé: {svg_path}")
        return False

    # Commande Inkscape pour exporter en PNG
    cmd = [
        "inkscape",
        str(svg_path),
        "--export-type=png",
        f"--export-filename={png_path}",
        "--export-background=white",  # Fond blanc pour transparence
        "--export-background-opacity=0",  # Transparence
    ]

    # Ajouter les dimensions si spécifiées
    if width:
        cmd.append(f"--export-width={width}")
    if height:
        cmd.append(f"--export-height={height}")

    try:
        print(f"📸 Export: {svg_path.name} → {png_path.name}")
        subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("   ✅ Export réussi")
        return True
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Erreur: {e.stderr}")
        return False
    except FileNotFoundError:
        print("   ❌ Inkscape non trouvé dans le PATH")
        print("   💡 Utilisez cairosvg comme alternative")
        return False


def reexport_with_cairosvg(svg_file, output_png, width=None, height=None):
    """Réexporte un SVG en PNG avec cairosvg (alternative)"""
    try:
        import cairosvg
    except ImportError:
        print("❌ cairosvg non installé")
        print("   Installer avec: pip install cairosvg")
        return False

    svg_path = Path(svg_file).absolute()
    png_path = Path(output_png).absolute()

    if not svg_path.exists():
        print(f"❌ SVG non trouvé: {svg_path}")
        return False

    try:
        print(f"📸 Export (cairosvg): {svg_path.name} → {png_path.name}")

        # Lire le SVG
        with open(svg_path, "rb") as f:
            svg_data = f.read()

        # Exporter en PNG
        if width and height:
            cairosvg.svg2png(
                bytestring=svg_data,
                write_to=str(png_path),
                output_width=width,
                output_height=height,
            )
        elif width:
            cairosvg.svg2png(
                bytestring=svg_data, write_to=str(png_path), output_width=width
            )
        else:
            cairosvg.svg2png(bytestring=svg_data, write_to=str(png_path))

        print("   ✅ Export réussi")
        return True
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False


def main():
    """Fonction principale"""
    print("=" * 70)
    print("🎨 RÉEXPORT AVEC BONNES COULEURS")
    print("=" * 70)

    current_dir = Path(".")

    # FICHIERS SVG SOURCES EXACTS - UTILISER UNIQUEMENT CES FICHIERS
    svg_files = {
        "bbia_mark_only_v2_SOURCE.svg": [
            ("bbia_mark_only_v2.png", None, None),  # Taille originale
            ("bbia_mark_only_512x512.png", 512, 512),
            ("bbia_favicon_32x32.png", 32, 32),
        ],
        "bbia_logo_vertical_v2_SOURCE.svg": [
            ("bbia_logo_vertical_v2.png", None, None),
        ],
        "bbia_logo_horizontal_SOURCE.svg": [
            ("bbia_logo_horizontal.png", 1024, None),  # Largeur 1024px
        ],
    }
    
    print("   ✅ Mark Only: bbia_mark_only_v2_SOURCE.svg")
    print("   ✅ Vertical: bbia_logo_vertical_v2_SOURCE.svg")
    print("   ✅ Horizontal: bbia_logo_horizontal_SOURCE.svg")

    # Vérifier si Inkscape est disponible
    inkscape_available = False
    try:
        result = subprocess.run(
            ["inkscape", "--version"], capture_output=True, text=True
        )
        if result.returncode == 0:
            inkscape_available = True
            print(f"✅ Inkscape trouvé: {result.stdout.strip()}")
    except FileNotFoundError:
        print("⚠️  Inkscape non trouvé, utilisation de cairosvg")

    print("\n📸 Réexport des fichiers...\n")

    success_count = 0
    total_count = 0

    for svg_file, outputs in svg_files.items():
        svg_path = current_dir / svg_file

        if not svg_path.exists():
            print(f"❌ SVG non trouvé: {svg_file}")
            continue

        print(f"📄 {svg_file}:")

        for png_file, width, height in outputs:
            total_count += 1
            png_path = current_dir / png_file

            if inkscape_available:
                if reexport_with_inkscape(svg_path, png_path, width, height):
                    success_count += 1
            else:
                if reexport_with_cairosvg(svg_path, png_path, width, height):
                    success_count += 1

        print()

    print("✅ Résumé:")
    print(f"   • {success_count}/{total_count} fichiers exportés avec succès")

    if success_count == total_count:
        print("\n💡 Tous les fichiers ont été réexportés avec les bonnes couleurs !")
        print("   Vérifiez maintenant que les couleurs sont correctes.")
    else:
        print("\n⚠️  Certains fichiers n'ont pas pu être exportés")
        print("   Vérifiez les erreurs ci-dessus")


if __name__ == "__main__":
    main()
