#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Version simple pour obtenir la résolution de l'écran

def get_resolution():
    """Fonction simple pour obtenir la résolution de l'écran"""
    try:
        # Méthode 1: tkinter (le plus simple et léger)
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()  # Masquer la fenêtre
        
        width = root.winfo_screenwidth()
        height = root.winfo_screenheight()
        
        root.destroy()
        return width, height
        
    except ImportError:
        try:
            # Méthode 2: Commande système xrandr
            import subprocess
            result = subprocess.run(['xrandr'], capture_output=True, text=True)
            
            for line in result.stdout.split('\n'):
                if ' connected ' in line and '*' in line:
                    # Trouver la résolution active (avec *)
                    parts = line.split()
                    for part in parts:
                        if 'x' in part and '*' in part:
                            resolution = part.split('*')[0]
                            width, height = map(int, resolution.split('x'))
                            return width, height
        except:
            pass
    
    # Si aucune méthode ne fonctionne
    return None, None

# Test simple
if __name__ == "__main__":
    width, height = get_resolution()
    if width and height:
        print(f"Résolution de l'écran: {width} x {height} pixels")
    else:
        print("Impossible de détecter la résolution de l'écran")