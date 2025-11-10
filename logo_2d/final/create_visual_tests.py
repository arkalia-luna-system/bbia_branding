#!/usr/bin/env python3
"""
Script pour créer des mockups de test visuel du logo BBIA
Génère des images de test sur différents fonds pour vérifier la lisibilité
"""
import os
from PIL import Image, ImageDraw, ImageFont

# Couleurs de test
COLORS = {
    "fond_clair": "#FFFFFF",  # Blanc
    "fond_sombre": "#1A1A1A",  # Noir/gris foncé
    "fond_turquoise": "#008181",  # Turquoise BBIA
    "fond_bleu": "#0066FF",  # Bleu BBIA officiel
}

# Taille des mockups
MOCKUP_SIZE = (800, 600)
LOGO_SIZE = (400, 400)  # Taille du logo dans le mockup


def create_mockup(background_color, logo_path, output_path, label):
    """Crée un mockup avec un fond de couleur et le logo centré"""
    # Créer l'image de fond
    img = Image.new("RGB", MOCKUP_SIZE, background_color)
    draw = ImageDraw.Draw(img)

    # Charger le logo
    try:
        logo = Image.open(logo_path)
        # Redimensionner le logo
        logo.thumbnail(LOGO_SIZE, Image.Resampling.LANCZOS)

        # Centrer le logo
        x = (MOCKUP_SIZE[0] - logo.size[0]) // 2
        y = (MOCKUP_SIZE[1] - logo.size[1]) // 2

        # Coller le logo (avec transparence si PNG)
        if logo.mode == "RGBA":
            img.paste(logo, (x, y), logo)
        else:
            img.paste(logo, (x, y))

        # Ajouter un label en bas
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 20)
        except (OSError, IOError):
            font = ImageFont.load_default()

        text = f"Test: {label} ({background_color})"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_x = (MOCKUP_SIZE[0] - text_width) // 2
        text_y = MOCKUP_SIZE[1] - 40

        # Couleur du texte selon le fond
        if background_color == "#FFFFFF":
            text_color = "#000000"
        else:
            text_color = "#FFFFFF"

        draw.text((text_x, text_y), text, fill=text_color, font=font)

    except Exception as e:
        print(f"⚠️  Erreur lors du chargement du logo {logo_path}: {e}")
        # Dessiner un rectangle pour indiquer l'emplacement du logo
        x = (MOCKUP_SIZE[0] - LOGO_SIZE[0]) // 2
        y = (MOCKUP_SIZE[1] - LOGO_SIZE[1]) // 2
        draw.rectangle(
            [x, y, x + LOGO_SIZE[0], y + LOGO_SIZE[1]], outline="#CCCCCC", width=2
        )
        draw.text(
            (x + 10, y + 10),
            f"Logo non trouvé:\n{logo_path}",
            fill="#CCCCCC",
            font=ImageFont.load_default(),
        )

    # Sauvegarder
    img.save(output_path, "PNG")
    print(f"✅ Mockup créé: {output_path}")


def main():
    """Fonction principale"""
    print("=" * 70)
    print("🎨 CRÉATION DES MOCKUPS DE TEST VISUEL")
    print("=" * 70)

    # Dossier de sortie
    output_dir = "tests_visuels"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"📁 Dossier créé: {output_dir}/")

    # Logo à tester (Mark Only pour les tests)
    # Essayer d'abord le PNG, puis le SVG, puis le favicon
    logo_path = "bbia_mark_only_v2.png"

    if not os.path.exists(logo_path):
        print(f"⚠️  PNG non trouvé: {logo_path}")
        # Essayer le SVG
        svg_path = "bbia_mark_only_v2.svg"
        if os.path.exists(svg_path):
            print(f"   ✅ Utilisation du SVG: {svg_path}")
            # Convertir SVG en PNG temporaire
            try:
                import cairosvg

                logo_path = "bbia_mark_only_v2_temp.png"
                with open(svg_path, "rb") as f:
                    svg_data = f.read()
                cairosvg.svg2png(bytestring=svg_data, write_to=logo_path)
                print("   ✅ SVG converti en PNG temporaire")
            except ImportError:
                print("   ❌ cairosvg non installé, impossible de convertir SVG")
                logo_path = None
            except Exception as e:
                print(f"   ❌ Erreur conversion SVG: {e}")
                logo_path = None
        else:
            print(f"   ⚠️  SVG non trouvé: {svg_path}")
            # Essayer le favicon
            logo_path = "bbia_favicon_32x32.png"
            if not os.path.exists(logo_path):
                print("❌ Aucun logo trouvé (PNG, SVG, favicon)")
                return
            else:
                print(f"   ✅ Utilisation du favicon: {logo_path}")

    print(f"\n📸 Logo utilisé: {logo_path}")
    print(f"📁 Dossier de sortie: {output_dir}/\n")

    # Créer tous les mockups
    for name, color in COLORS.items():
        output_file = os.path.join(output_dir, f"mockup_{name}.png")
        create_mockup(color, logo_path, output_file, name.replace("_", " ").title())

    print(f"\n✅ {len(COLORS)} mockups créés dans {output_dir}/")
    print("\n📋 Fichiers créés:")
    for name in COLORS.keys():
        print(f"   • mockup_{name}.png")

    print("\n💡 Instructions:")
    print("   1. Ouvrir les mockups dans un visualiseur d'images")
    print("   2. Vérifier la lisibilité du logo sur chaque fond")
    print("   3. Noter les problèmes éventuels de contraste")
    print("   4. Documenter les résultats dans VALIDATION_FINALE.md")


if __name__ == "__main__":
    main()
